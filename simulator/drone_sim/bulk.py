"""Bulk weather and ocean data: download whole months once, then simulate at full CPU speed.

Open-Meteo serves these same datasets one location at a time, and its free limit (about
10,000 location-calls a day) makes a real-weather Monte Carlo take days. Here we fetch each
month for the whole North Atlantic box in one request per source, from the agencies that
produce the data:

  era5  ECMWF ERA5 reanalysis, 0.25 deg, hourly (Copernicus Climate Data Store, free account)
        wind u/v at 10 m, gusts, solar radiation, cloud cover, 2 m air temperature, SST
  smoc  Copernicus Marine SMOC surface currents, 1/12 deg, hourly: total current =
        Eulerian + tides + Stokes drift (the same current Open-Meteo serves)
  wav   Copernicus Marine MFWAM waves, 1/12 deg, 3-hourly: Hs, mean and peak period,
        mean direction, primary swell height

Each month is stored as float16 .npy arrays (time, lat, lon) plus meta.json under
<workspace>/cache/bulk/<source>/<YYYYMM>/. The simulator memory-maps them, so every worker
process shares one copy in the operating system's file cache.

Setup (once, on your computer):  copernicusmarine login  and a CDS API token in ~/.cdsapirc
(simulator/setup_bulk_data.bat does both). Credentials stay on your computer.
"""
import datetime as dt
import glob
import json
import math
import os
import shutil
import threading
import time
import zipfile

import numpy as np

# Default box: Cape Hatteras / Ocean City to the Channel and Biscay, Newfoundland to the Azores
DEFAULT_BOX = dict(lat=(26.0, 60.0), lon=(-82.0, 0.0))

ERA5_DATASET = "reanalysis-era5-single-levels"
ERA5_VARS = {  # CDS request name -> (short names it may come back as, our name, transform)
    "10m_u_component_of_wind": (("u10",), "wind_u", "id"),
    "10m_v_component_of_wind": (("v10",), "wind_v", "id"),
    "10m_wind_gust_since_previous_post_processing": (("fg10", "10fg", "i10fg"), "gust", "id"),
    "surface_solar_radiation_downwards": (("ssrd",), "sw_rad", "per_hour"),
    "total_cloud_cover": (("tcc",), "cloud", "percent"),
    "2m_temperature": (("t2m", "2t"), "air_t", "k_to_c"),
    "sea_surface_temperature": (("sst",), "sst", "k_to_c"),
}
MARINE = {
    "smoc": dict(dataset="cmems_mod_glo_phy_anfc_merged-uv_PT1H-i",
                 vars={"utotal": "cur_u", "vtotal": "cur_v"}),
    "wav": dict(dataset="cmems_mod_glo_wav_anfc_0.083deg_PT3H-i",
                vars={"VHM0": "hs", "VTM10": "tp_m10", "VTPK": "tp_pk", "VMDR": "wave_dir", "VHM0_SW1": "swell_hs"},
                # The 1/12 deg forecast archive starts in November 2022 (found 14 Nov 2026). Earlier months come from
                # the WAVERYS reanalysis (GLOBAL_MULTIYEAR_WAV_001_032): same variables, 0.2 deg grid, 3-hourly,
                # from 1980; its interim dataset carries it towards the present. Each month stores its own grid.
                older=("cmems_mod_glo_wav_my_0.2deg_PT3H-i", "cmems_mod_glo_wav_myint_0.2deg_PT3H-i"), older_before=202211),
}
SOURCES = ("era5", "smoc", "wav")
FIELD_SOURCE = {"wind_u": "era5", "wind_v": "era5", "gust": "era5", "sw_rad": "era5", "cloud": "era5",
                "air_t": "era5", "sst": "era5", "cur_u": "smoc", "cur_v": "smoc",
                "hs": "wav", "tp_m10": "wav", "tp_pk": "wav", "wave_dir": "wav", "swell_hs": "wav"}


def bulk_dir(cache_dir):
    return os.path.join(cache_dir, "bulk")


def month_list(spec):
    """'2023-05..2023-10,2024-05..2024-10' -> [202305, ..., 202410]"""
    out = []
    for part in [p.strip() for p in spec.split(",") if p.strip()]:
        a, _, b = part.partition("..")
        y0, m0 = map(int, a.split("-")); y1, m1 = map(int, (b or a).split("-"))
        y, m = y0, m0
        while (y, m) <= (y1, m1):
            out.append(y*100 + m)
            y, m = (y + (m == 12), m % 12 + 1)
    return sorted(set(out))


def _month_bounds(ym):
    y, m = divmod(ym, 100)
    start = dt.datetime(y, m, 1, tzinfo=dt.timezone.utc)
    end = dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=dt.timezone.utc) - dt.timedelta(seconds=1)
    return start, end


def _done(root, source, ym):
    return os.path.exists(os.path.join(root, source, str(ym), "meta.json"))


# ------------------------------------------------------------------ netCDF reading
def _open_nc(path):
    try:
        import netCDF4
        ds = netCDF4.Dataset(path)
        ds.set_auto_maskandscale(True)
        return ds
    except ImportError:
        from scipy.io import netcdf_file          # netCDF3 only (used by the offline tests)
        return netcdf_file(path, "r", mmap=False)


def _attr(var, name, default=None):
    try:
        return var.getncattr(name)
    except Exception:
        v = getattr(var, name, default)
        return v.decode() if isinstance(v, bytes) else v


def _read(var, sl):
    a = var[sl]
    if np.ma.isMaskedArray(a):
        a = a.astype(np.float32).filled(np.nan)
    a = np.asarray(a, dtype=np.float32)
    if not hasattr(var, "set_auto_maskandscale"):          # scipy reader: apply packing and fill by hand
        fill = _attr(var, "_FillValue")
        if fill is not None: a[a == np.float32(fill)] = np.nan
        sf, ao = _attr(var, "scale_factor"), _attr(var, "add_offset")
        if sf is not None: a = a*np.float32(sf)
        if ao is not None: a = a + np.float32(ao)
    return a


def _times_epoch(tvar):
    units = _attr(tvar, "units", "")
    vals = np.asarray(tvar[:], dtype=np.float64)
    unit, _, origin = units.partition(" since ")
    origin = origin.strip().replace("T", " ").replace("Z", "")
    o = dt.datetime.fromisoformat(origin[:19] if len(origin) >= 19 else (origin + " 00:00:00")[:19])
    o = o.replace(tzinfo=dt.timezone.utc).timestamp()
    mult = {"seconds": 1, "second": 1, "minutes": 60, "minute": 60, "hours": 3600, "hour": 3600,
            "days": 86400, "day": 86400}[unit.strip().lower()]
    return o + vals*mult


def _find(ds, names):
    for n in names:
        if n in ds.variables: return n
    return None


def convert(nc_paths, wanted, out_dir, stride=1, log=print):
    """Write float16 memmap arrays + meta.json for one source-month.
    wanted: {netcdf_var_names(tuple) : (our_name, transform)}"""
    tmp = out_dir + ".partial"
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    grid = None; written = []
    for path in nc_paths:
        ds = _open_nc(path)
        try:
            tname = _find(ds, ("time", "valid_time"))
            latn = _find(ds, ("latitude", "lat")); lonn = _find(ds, ("longitude", "lon"))
            if not (tname and latn and lonn):
                continue
            times = _times_epoch(ds.variables[tname])
            lat = np.asarray(ds.variables[latn][:], dtype=np.float64)
            lon = np.asarray(ds.variables[lonn][:], dtype=np.float64)
            lon = np.where(lon > 180, lon - 360, lon)
            flip = lat[0] > lat[-1]
            if flip: lat = lat[::-1]
            lat_s, lon_s = lat[::stride], lon[::stride]
            g = dict(lat0=float(lat_s[0]), dlat=float(np.median(np.diff(lat_s))), nlat=len(lat_s),
                     lon0=float(lon_s[0]), dlon=float(np.median(np.diff(lon_s))), nlon=len(lon_s),
                     t0=float(times[0]), dt=float(np.median(np.diff(times))) if len(times) > 1 else 3600.0,
                     nt=len(times))
            if np.max(np.abs(np.diff(lat_s) - g["dlat"])) > 1e-3 or np.max(np.abs(np.diff(lon_s) - g["dlon"])) > 1e-3:
                raise RuntimeError(f"{os.path.basename(path)}: grid is not regular")
            if np.max(np.abs(np.diff(times) - g["dt"])) > 1 if len(times) > 1 else False:
                raise RuntimeError(f"{os.path.basename(path)}: time steps are not regular")
            if grid is None: grid = g
            elif any(abs(grid[k] - g[k]) > 1e-6 for k in ("lat0", "dlat", "lon0", "dlon", "t0", "dt")) or \
                    grid["nlat"] != g["nlat"] or grid["nlon"] != g["nlon"] or grid["nt"] != g["nt"]:
                raise RuntimeError(f"{os.path.basename(path)}: grid differs from the other files of this month")
            for names, (ours, tf) in wanted.items():
                vn = _find(ds, names)
                if vn is None or ours in written: continue
                var = ds.variables[vn]
                dims = list(var.dimensions)
                arr = np.lib.format.open_memmap(os.path.join(tmp, ours + ".npy"), mode="w+",
                                                dtype=np.float16, shape=(g["nt"], g["nlat"], g["nlon"]))
                step = 24
                for i in range(0, g["nt"], step):
                    sl = [slice(None)]*len(dims)
                    sl[dims.index(tname)] = slice(i, min(i + step, g["nt"]))
                    for d in dims:                       # surface level of any depth axis
                        if d not in (tname, latn, lonn): sl[dims.index(d)] = 0
                    a = _read(var, tuple(sl))
                    keep = [d for d in dims if d in (tname, latn, lonn)]
                    a = np.transpose(a, [keep.index(tname), keep.index(latn), keep.index(lonn)])
                    if flip: a = a[:, ::-1, :]
                    a = a[:, ::stride, ::stride]
                    if tf == "k_to_c": a = a - 273.15
                    elif tf == "percent": a = a*100.0
                    elif tf == "per_hour": a = a/3600.0      # J/m2 accumulated over the hour -> mean W/m2
                    arr[i:i + a.shape[0]] = a.astype(np.float16)
                arr.flush(); del arr
                written.append(ours)
        finally:
            ds.close()
    missing = [ours for ours, _ in wanted.values() if ours not in written]
    if grid is None or missing:
        raise RuntimeError(f"variables missing from the download: {missing or 'all'}")
    meta = dict(grid, vars=written, stride=stride, made=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    json.dump(meta, open(os.path.join(tmp, "meta.json"), "w"), indent=1)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.replace(tmp, out_dir)
    size = sum(os.path.getsize(p) for p in glob.glob(os.path.join(out_dir, "*.npy")))/1e9
    log(f"    stored {os.path.basename(os.path.dirname(out_dir))} {os.path.basename(out_dir)}: "
        f"{grid['nt']} times x {grid['nlat']} x {grid['nlon']} ({size:.2f} GB)")


# ------------------------------------------------------------------ downloaders
def _download_era5(ym, box, raw, log):
    import cdsapi
    start, end = _month_bounds(ym)
    days = [f"{d:02d}" for d in range(1, end.day + 1)]
    req = {"product_type": ["reanalysis"], "variable": list(ERA5_VARS), "year": [f"{start.year}"],
           "month": [f"{start.month:02d}"], "day": days, "time": [f"{h:02d}:00" for h in range(24)],
           "data_format": "netcdf", "download_format": "unarchived",
           "area": [box["lat"][1], box["lon"][0], box["lat"][0], box["lon"][1]]}
    target = os.path.join(raw, f"era5_{ym}.download")
    cdsapi.Client(quiet=True, progress=False).retrieve(ERA5_DATASET, req, target)
    files = []
    if zipfile.is_zipfile(target):              # mixed accumulated/instant fields can come back as a zip
        with zipfile.ZipFile(target) as z:
            for n in z.namelist():
                if n.endswith(".nc"):
                    p = os.path.join(raw, f"era5_{ym}_{os.path.basename(n)}"); open(p, "wb").write(z.read(n)); files.append(p)
        os.remove(target)
    else:
        p = os.path.join(raw, f"era5_{ym}.nc"); os.replace(target, p); files.append(p)
    return files


def _download_marine(name, ym, box, raw, log):
    import copernicusmarine, inspect
    spec = MARINE[name]
    start, end = _month_bounds(ym)
    fn = f"{name}_{ym}.nc"
    if os.path.exists(os.path.join(raw, fn)): os.remove(os.path.join(raw, fn))
    datasets = [spec["dataset"]]
    if spec.get("older") and int(ym) < spec["older_before"]:
        datasets = list(spec["older"])
    last = None
    for ds in datasets:
        try:
            return _subset_marine(ds, spec, ym, box, raw, fn, start, end)
        except Exception as e:  # noqa: BLE001 - out of this dataset's range: try the next one
            last = e
            if len(datasets) > 1: log(f"[Marine] {name} {ym}: {ds} failed ({type(e).__name__}); trying the next dataset")
    raise last


def _subset_marine(ds, spec, ym, box, raw, fn, start, end):
    import copernicusmarine, inspect
    kw = dict(dataset_id=ds, variables=list(spec["vars"]),
              minimum_longitude=box["lon"][0], maximum_longitude=box["lon"][1],
              minimum_latitude=box["lat"][0], maximum_latitude=box["lat"][1],
              start_datetime=start.strftime("%Y-%m-%dT%H:%M:%S"), end_datetime=end.strftime("%Y-%m-%dT%H:%M:%S"),
              output_filename=fn, output_directory=raw, overwrite=True, disable_progress_bar=True)
    ok = set(inspect.signature(copernicusmarine.subset).parameters)
    copernicusmarine.subset(**{k: v for k, v in kw.items() if k in ok})
    return [os.path.join(raw, fn)]


def _http_detail(e):
    """(status code, server's explanation) from a requests-style HTTPError, else (None, '')."""
    r = getattr(e, "response", None)
    code = getattr(r, "status_code", None)
    if r is None:
        return None, ""
    try:
        j = r.json()
        detail = " | ".join(str(j.get(k)) for k in ("title", "detail", "message", "traceback") if j.get(k))
    except Exception:
        detail = (getattr(r, "text", "") or "")[:500]
    return code, detail[:800] or "(no explanation in the response)"


def cds_check(log=print):
    """Diagnose CDS access without ever printing the token: config, versions, auth, one tiny request."""
    import re, sys, tempfile
    log(f"Python {sys.version.split()[0]}")
    for mod in ("cdsapi", "ecmwf.datastores", "requests"):
        try:
            m = __import__(mod, fromlist=["x"]); log(f"{mod} {getattr(m, '__version__', '?')}")
        except Exception as e:
            log(f"{mod}: not importable ({e})")
    rc = os.path.join(os.path.expanduser("~"), ".cdsapirc")
    url = key = None
    if not os.path.exists(rc):
        log(f"No {rc}. Run setup_bulk_data.bat again."); return
    for line in open(rc, encoding="utf-8", errors="replace"):
        k, _, v = line.partition(":")
        if k.strip() == "url": url = v.strip()
        if k.strip() == "key": key = v.strip()
    log(f".cdsapirc url: {url!r}")
    if not key:
        log(".cdsapirc has no key line."); return
    shape = "UUID (the current format)" if re.fullmatch(r"[0-9a-fA-F-]{36}", key) else (
        "UID:KEY (the old, retired format)" if ":" in key else "unexpected format")
    log(f".cdsapirc key: {len(key)} characters, {shape}" + ("; contains spaces or quotes" if re.search(r"[\s'\"]", key) else ""))
    import requests
    for path in ("/profiles/v1/account/verification/pat", "/retrieve/v1/processes/" + ERA5_DATASET):
        try:
            r = requests.get(url.rstrip("/") + path, headers={"PRIVATE-TOKEN": key}, timeout=60)
            log(f"GET {path}: HTTP {r.status_code} {r.text[:300]!r}")
        except Exception as e:
            log(f"GET {path}: {e}")
    log("Submitting one tiny request (2 m temperature, 1 hour, small box) ...")
    try:
        import cdsapi
        tgt = os.path.join(tempfile.gettempdir(), "cds_check.nc")
        cdsapi.Client(url=url, key=key, quiet=True, progress=False).retrieve(ERA5_DATASET, {
            "product_type": ["reanalysis"], "variable": ["2m_temperature"], "year": ["2024"], "month": ["05"],
            "day": ["15"], "time": ["12:00"], "data_format": "netcdf", "download_format": "unarchived",
            "area": [40, -75, 38, -73]}, tgt)
        log(f"Tiny request worked ({os.path.getsize(tgt)} bytes). CDS access is fine.")
    except Exception as e:
        code, detail = _http_detail(e)
        log(f"Tiny request failed: HTTP {code}: {detail or e}")


def download(months, cache_dir, box=None, sources=SOURCES, stride=1, keep_raw=False, log=print):
    """Fetch and convert every missing source-month. The two services run side by side; requests
    to each one are strictly one after another (CDS asks for that)."""
    box = box or DEFAULT_BOX
    root = bulk_dir(cache_dir); raw = os.path.join(root, "_raw"); os.makedirs(raw, exist_ok=True)
    json.dump(dict(box=box), open(os.path.join(root, "box.json"), "w"))
    todo = {s: [ym for ym in months if not _done(root, s, ym)] for s in sources}
    log(f"Bulk data in {root}")
    for s in sources:
        log(f"  {s}: {len(months) - len(todo[s])} of {len(months)} months already stored, {len(todo[s])} to fetch")
    errors = []

    def worker(label, items):
        for s, ym in items:
            for attempt in range(3):
                try:
                    t = time.time()
                    log(f"[{label}] requesting {s} {ym} ...")
                    files = _download_era5(ym, box, raw, log) if s == "era5" else _download_marine(s, ym, box, raw, log)
                    wanted = ({names: (ours, tf) for _, (names, ours, tf) in ERA5_VARS.items()} if s == "era5"
                              else {(k,): (v, "id") for k, v in MARINE[s]["vars"].items()})
                    convert(files, wanted, os.path.join(root, s, str(ym)),
                            stride=(1 if s == "era5" else stride), log=log)
                    if not keep_raw:
                        for f in files: os.remove(f)
                    log(f"[{label}] {s} {ym} done in {(time.time() - t)/60:.1f} min")
                    break
                except Exception as e:  # noqa: BLE001 - report and retry, then move on
                    code, detail = _http_detail(e)
                    if code and 400 <= code < 500:
                        # The service rejected the request itself. Retrying identical requests does not help,
                        # and CDS may disable accounts that keep sending invalid ones, so stop this lane.
                        log(f"[{label}] {s} {ym} was refused by the server (HTTP {code}). Server says: {detail}")
                        log(f"[{label}] Stopping {label} downloads. Run: python -m drone_sim.cli cdscheck")
                        errors.append(f"{s} {ym}: HTTP {code}: {detail}")
                        return
                    log(f"[{label}] {s} {ym} failed ({type(e).__name__}: {str(e)[:300]})"
                        + ("; retrying in 2 min" if attempt < 2 else "; giving up on this month for now"))
                    if attempt < 2: time.sleep(120)
                    else: errors.append(f"{s} {ym}: {e}")

    lanes = {"CDS": [("era5", ym) for ym in todo.get("era5", [])],
             "Marine": [(s, ym) for ym in months for s in ("smoc", "wav") if s in todo and ym in todo[s]]}
    threads = [threading.Thread(target=worker, args=(k, v), daemon=True) for k, v in lanes.items() if v]
    for th in threads: th.start()
    for th in threads: th.join()
    left = sum(1 for s in sources for ym in months if not _done(root, s, ym))
    log(f"Bulk download finished: {left} source-months still missing." + (" Run it again to retry them." if left else ""))
    return errors


def available_months(cache_dir):
    root = bulk_dir(cache_dir)
    sets = [set(int(os.path.basename(os.path.dirname(p))) for p in glob.glob(os.path.join(root, s, "*", "meta.json")))
            for s in SOURCES]
    return sorted(set.intersection(*sets)) if sets else []


# ------------------------------------------------------------------ the provider
class BulkDataMissing(RuntimeError):
    """A voyage reached a month that has not been downloaded."""


class _Month:
    def __init__(self, folder):
        m = json.load(open(os.path.join(folder, "meta.json")))
        self.__dict__.update(m)
        self.a = {v: np.load(os.path.join(folder, v + ".npy"), mmap_mode="r") for v in m["vars"]}
        self.t_end = self.t0 + (self.nt - 1)*self.dt


class _Source:
    def __init__(self, folder, name):
        self.folder, self.name, self.months = folder, name, {}

    def month(self, ym):
        if ym not in self.months:
            f = os.path.join(self.folder, self.name, str(ym))
            self.months[ym] = _Month(f) if os.path.exists(os.path.join(f, "meta.json")) else None
        return self.months[ym]


def _ym(t):
    d = dt.datetime.fromtimestamp(t, dt.timezone.utc)
    return d.year*100 + d.month


def _next_ym(ym):
    y, m = divmod(ym, 100)
    return (y + (m == 12))*100 + m % 12 + 1


class BulkProvider:
    """Samples the bulk arrays: bilinear in space, linear in time, NaN (land) corners skipped,
    wave direction averaged as a vector."""
    DEFAULTS = dict(hs=0.0, tp=5.0, wave_dir=0.0, swell_hs=0.0, cur_u=0.0, cur_v=0.0, sst=12.0,
                    sea_level=0.0, sw_rad=0.0, cloud=50.0, air_t=12.0, gust=0.0, wind_u=0.0, wind_v=0.0)

    def __init__(self, cache_dir="cache", log=print, wave_period="tp_m10"):
        self.root = bulk_dir(cache_dir); self.log = log; self.wave_period = wave_period
        if not os.path.isdir(self.root):
            raise RuntimeError("No bulk data yet. Run: python -m drone_sim.cli download --months 2023-05..2023-10")
        try:
            self.wave_period = json.load(open(os.path.join(self.root, "settings.json"))).get("wave_period", wave_period)
        except Exception:
            pass
        self.src = {s: _Source(self.root, s) for s in SOURCES}
        self.cache = {}
        self.warned = set()
        self.calls = 0

    def _corners(self, s, lat, lon, t):
        """(names, stacked corner values [nvar, 2, 2, 2], weights [2, 2, 2]) or None outside the data.
        Wave direction is carried as sin/cos so it averages correctly across north."""
        src = self.src[s]; ym = _ym(t)
        m = src.month(ym)
        if m is None:
            raise BulkDataMissing(f"bulk {s} data for {ym // 100}-{ym % 100:02d} is not downloaded "
                               f"(python -m drone_sim.cli download --months {ym // 100}-{ym % 100:02d})")
        k = max((t - m.t0)/m.dt, 0.0)   # before the first stored time of the month (3-hourly waves): hold it
        k0 = int(math.floor(k)); wt = min(max(k - k0, 0.0), 1.0)
        fi = (lat - m.lat0)/m.dlat; fj = (lon - m.lon0)/m.dlon
        i0, j0 = int(math.floor(fi)), int(math.floor(fj))
        if i0 < 0 or j0 < 0 or i0 + 1 >= m.nlat or j0 + 1 >= m.nlon:
            return None
        key = (s, ym, k0, i0, j0)
        hit = self.cache.get(key)
        if hit is None:
            if len(self.cache) > 20000: self.cache.clear()
            n = src.month(_next_ym(ym)) if k0 + 1 >= m.nt else None
            names, blocks = [], []
            for v, a in m.a.items():
                if k0 + 1 < m.nt:
                    c = np.asarray(a[k0:k0 + 2, i0:i0 + 2, j0:j0 + 2], dtype=np.float32)
                else:                    # last step of the month: pair it with the first of the next month
                    first = np.asarray(a[k0:k0 + 1, i0:i0 + 2, j0:j0 + 2], dtype=np.float32)
                    second = (np.asarray(n.a[v][0:1, i0:i0 + 2, j0:j0 + 2], dtype=np.float32)
                              if n is not None and n.nlat == m.nlat and n.nlon == m.nlon and v in n.a else first)
                    c = np.concatenate([first, second])
                if v == "wave_dir":
                    r = np.radians(c); names += ["_dir_s", "_dir_c"]; blocks += [np.sin(r), np.cos(r)]
                else:
                    names.append(v); blocks.append(c)
            stack = np.stack(blocks)
            hit = (names, np.where(np.isfinite(stack), stack, 0.0).astype(np.float32), np.isfinite(stack).astype(np.float32))
            self.cache[key] = hit
        wi, wj = fi - i0, fj - j0
        w2 = np.array([[(1 - wi)*(1 - wj), (1 - wi)*wj], [wi*(1 - wj), wi*wj]], dtype=np.float32)
        w = np.stack([w2*(1 - wt), w2*wt])
        return hit, w

    @staticmethod
    def _combine(hit, w):
        names, vals, ok = hit
        den = np.tensordot(ok, w, axes=3)
        num = np.tensordot(vals, w, axes=3)
        out = {}
        for k, name in enumerate(names):
            if den[k] > 1e-9: out[name] = float(num[k]/den[k])
        if "_dir_s" in out and "_dir_c" in out:
            out["wave_dir"] = math.degrees(math.atan2(out.pop("_dir_s"), out.pop("_dir_c"))) % 360
        return out

    def values(self, lat, lon, t):
        got = {}
        for s in SOURCES:
            r = self._corners(s, lat, lon, t)
            if r is None:
                if s not in self.warned:
                    self.warned.add(s)
                    self.log(f"Note: {lat:.2f}, {lon:.2f} is outside the downloaded {s} box; using neutral values there.")
                continue
            got.update(self._combine(*r))
        return got

    def sample(self, lat, lon, t):
        self.calls += 1
        got = self.values(lat, lon, t)
        out = dict(self.DEFAULTS)
        out.update({k: v for k, v in got.items() if k in out})
        if self.wave_period in got: out["tp"] = got[self.wave_period]
        out["marine_ok"] = "hs" in got
        out["current_includes_stokes"] = True   # SMOC total current = Eulerian + tides + Stokes drift
        return out


# ------------------------------------------------------------------ check against Open-Meteo
def compare_with_openmeteo(cache_dir, n_files=200, log=print, seed=1):
    """Sample the bulk arrays at points and hours already in the Open-Meteo cache and report the
    differences field by field. Same datasets underneath, so differences should be small, apart
    from Open-Meteo's own grid choices."""
    months = set(available_months(cache_dir))
    files = [p for p in glob.glob(os.path.join(cache_dir, "openmeteo", "*", "*.npz"))
             if int(os.path.basename(p).rsplit("_", 1)[1][:6]) in months]
    if not files:
        log("No Open-Meteo cache files overlap the downloaded bulk months, so there is nothing to compare.")
        return None
    rng = np.random.default_rng(seed)
    files = list(rng.choice(files, size=min(n_files, len(files)), replace=False))
    bp = BulkProvider(cache_dir, log=lambda *a: None)
    pairs = {k: ([], []) for k in ("wind_u", "wind_v", "gust", "sw_rad", "cloud", "air_t", "sst",
                                   "hs", "tp_m10", "tp_pk", "wave_dir", "swell_hs", "cur_u", "cur_v")}
    for p in files:
        lat, lon = [float(x) for x in os.path.basename(p).rsplit("_", 1)[0].split("_")]
        z = np.load(p)
        tt = z["t"]
        for k in range(0, len(tt), 6):
            t = float(tt[k])
            row = bp.values(lat, lon, t)
            for name in pairs:
                om_name = "tp" if name in ("tp_m10", "tp_pk") else name
                if name in row and om_name in z.files and np.isfinite(z[om_name][k]):
                    pairs[name][0].append(float(z[om_name][k])); pairs[name][1].append(row[name])
    lines = [f"Bulk data vs Open-Meteo cache: {len(files)} cached points, every 6th hour",
             f"{'field':10s} {'n':>7s} {'Open-Meteo mean':>16s} {'bulk mean':>10s} {'bias':>8s} {'RMS diff':>9s} {'corr':>6s}"]
    res = {}
    for name, (a, b) in pairs.items():
        if len(a) < 10: continue
        a, b = np.array(a), np.array(b)
        d = b - a
        if name == "wave_dir": d = (d + 180) % 360 - 180
        corr = float(np.corrcoef(a, b)[0, 1]) if name != "wave_dir" and np.std(a) > 0 and np.std(b) > 0 else float("nan")
        if name == "wave_dir":
            cm = lambda x: math.degrees(math.atan2(np.mean(np.sin(np.radians(x))), np.mean(np.cos(np.radians(x))))) % 360
            om_mean, bulk_mean = cm(a), cm(b)
        else:
            om_mean, bulk_mean = float(np.mean(a)), float(np.mean(b))
        res[name] = dict(n=len(a), om=om_mean, bulk=bulk_mean, bias=float(np.mean(d)),
                         rms=float(np.sqrt(np.mean(d**2))), corr=corr)
        r = res[name]
        lines.append(f"{name:10s} {r['n']:7d} {r['om']:16.3f} {r['bulk']:10.3f} {r['bias']:8.3f} {r['rms']:9.3f} {r['corr']:6.2f}")
    if "tp_m10" in res and "tp_pk" in res:
        best = "tp_m10" if res["tp_m10"]["rms"] <= res["tp_pk"]["rms"] else "tp_pk"
        lines.append(f"Wave period: Open-Meteo's wave_period matches {best} best "
                     f"(RMS {res[best]['rms']:.2f} s); the simulator uses that one.")
        json.dump(dict(wave_period=best), open(os.path.join(bulk_dir(cache_dir), "settings.json"), "w"))
    for line in lines: log(line)
    return res
