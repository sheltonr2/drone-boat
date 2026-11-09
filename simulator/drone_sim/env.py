"""Environment providers.

OpenMeteoProvider: historic hourly data from Open-Meteo (no API key):
  * ERA5 reanalysis (archive-api.open-meteo.com): 10 m wind, gusts, shortwave radiation,
    cloud cover, air temperature - available 1940 to present.
  * Marine API (marine-api.open-meteo.com): waves (height, period, direction), ocean
    currents (Eulerian + waves + tides), sea level incl. tides, sea-surface temperature.
    Currents and sea level start January 2022.
Data is fetched lazily on a lat/lon grid around the boat, cached on disk, and interpolated
bilinearly in space and linearly in time.

SyntheticProvider: offline North-Atlantic-like weather (westerlies, travelling lows, Gulf
Stream, tides, solar) for testing without internet.

Conventions returned by sample(): wind_u/wind_v = velocity the air moves toward (east,
north) m/s at 10 m; cur_u/cur_v likewise for water; wave_dir = direction waves come FROM
(deg, clockwise from north).
"""
import json, math, os, time, urllib.request, urllib.parse, datetime as dt
import numpy as np

EPOCH = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
FIELDS = ["wind_u", "wind_v", "gust", "sw_rad", "cloud", "air_t",
          "hs", "tp", "wave_dir", "swell_hs", "cur_u", "cur_v", "sst", "sea_level"]


def to_epoch(s):
    if isinstance(s, (int, float)): return float(s)
    d = dt.datetime.fromisoformat(s.replace("Z", ""))
    if d.tzinfo is None: d = d.replace(tzinfo=dt.timezone.utc)
    return (d - EPOCH).total_seconds()


def from_epoch(t):
    return EPOCH + dt.timedelta(seconds=float(t))


def _speed_to_ms(unit):
    u = (unit or "").lower().replace(" ", "")
    return {"km/h": 1/3.6, "kmh": 1/3.6, "m/s": 1.0, "ms": 1.0, "kn": 0.514444, "knots": 0.514444,
            "mp/h": 0.44704, "mph": 0.44704}.get(u, 1/3.6 if "km" in u else 1.0)


class OpenMeteoLimit(RuntimeError):
    """Open-Meteo's free daily limit is used up. Everything downloaded so far is cached."""


class _UsageLedger:
    """Rough count of Open-Meteo calls (one per location per request), kept in the cache folder so
    separate runs on the same day share it. Free limits: 600/min, 5,000/hour, 10,000/day."""
    HOUR_BUDGET, DAY_BUDGET = 4500, 9500

    def __init__(self, folder):
        self.path = os.path.join(folder, "usage.json")

    def _load(self):
        try:
            return [tuple(x) for x in json.load(open(self.path)) if time.time() - x[0] < 90000]
        except Exception:
            return []

    def used(self):
        now = time.time(); rows = self._load()
        day0 = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        return (sum(w for t, w in rows if now - t < 3600), sum(w for t, w in rows if t >= day0), rows)

    def add(self, w):
        rows = self._load(); rows.append((time.time(), w))
        try:
            tmp = self.path + f".{os.getpid()}.tmp"
            json.dump(rows, open(tmp, "w")); os.replace(tmp, self.path)
        except Exception:
            pass

    def wait_for(self, w, log):
        """Sleep until w more calls fit in the hourly budget; raise OpenMeteoLimit if the day's budget is spent."""
        while True:
            hour, day, rows = self.used()
            if day + w > self.DAY_BUDGET:
                raise OpenMeteoLimit(
                    f"Open-Meteo's free daily limit is nearly used up ({day:.0f} of about 10,000 calls today, UTC). "
                    "Everything downloaded so far is cached. Run the same command again after 00:00 UTC "
                    "(7 pm Eastern) and it carries on from where it stopped.")
            if hour + w <= self.HOUR_BUDGET:
                return
            oldest = min(t for t, _ in rows if time.time() - t < 3600)
            pause = max(60, int(oldest + 3600 - time.time()) + 5)
            log(f"Pausing {pause//60} min to stay under Open-Meteo's hourly limit ({hour:.0f} calls in the last hour) ...")
            time.sleep(pause)


class OpenMeteoProvider:
    WX_URL = "https://archive-api.open-meteo.com/v1/archive"
    MAR_URL = "https://marine-api.open-meteo.com/v1/marine"
    WX_VARS = ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "shortwave_radiation",
               "cloud_cover", "temperature_2m"]
    MAR_VARS = ["wave_height", "wave_period", "wave_direction", "swell_wave_height",
                "ocean_current_velocity", "ocean_current_direction", "sea_surface_temperature",
                "sea_level_height_msl"]

    def __init__(self, cache_dir="cache", res_deg=1.0, log=print, block=3, pause_s=0.3):
        self.cache = os.path.join(cache_dir, "openmeteo"); os.makedirs(self.cache, exist_ok=True)
        self.res = res_deg; self.log = log; self.block = block; self.pause = pause_s
        self.mem = {}           # (lat_i, lon_i, yyyymm) -> dict of arrays incl. 't'
        self.calls = 0
        self.ledger = _UsageLedger(self.cache)

    # ---------- grid helpers
    def _node(self, i, j):
        return round(i*self.res, 4), round(j*self.res, 4)

    @staticmethod
    def _month_range(ym):
        y, m = divmod(ym, 100)
        start = dt.date(y, m, 1)
        end = (dt.date(y + (m == 12), (m % 12) + 1, 1) - dt.timedelta(days=1))
        return start, end

    def _path(self, i, j, ym):
        lat, lon = self._node(i, j)
        return os.path.join(self.cache, f"{self.res:g}", f"{lat:+08.3f}_{lon:+09.3f}_{ym}.npz")

    def _get(self, i, j, ym):
        key = (i, j, ym)
        if key in self.mem: return self.mem[key]
        p = self._path(i, j, ym)
        if os.path.exists(p):
            z = np.load(p); d = {k: z[k] for k in z.files}; self.mem[key] = d; return d
        self._fetch_block(i, j, ym)
        return self.mem[key]

    # ---------- network
    def _http(self, url, params):
        q = urllib.parse.urlencode(params, safe=",")
        full = f"{url}?{q}"
        weight = max(1, str(params.get("latitude", "")).count(",") + 1)   # Open-Meteo counts each location
        self.ledger.wait_for(weight, self.log)
        hourly_waits = 0
        attempt = 0
        while attempt < 6:
            try:
                req = urllib.request.Request(full, headers={"User-Agent": "drone-sim/1.0 (research)"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    self.calls += 1
                    self.ledger.add(weight)
                    time.sleep(self.pause)
                    return json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                body = e.read().decode(errors="ignore")[:300]
                if e.code == 429:
                    reason = body.lower()
                    if "daily" in reason:
                        raise OpenMeteoLimit(
                            "Open-Meteo says the free daily limit is used up. Everything downloaded so far is "
                            "cached. Run the same command again after 00:00 UTC (7 pm Eastern) and it carries on.")
                    if "hourly" in reason and hourly_waits < 7:
                        hourly_waits += 1
                        self.log("Open-Meteo hourly limit reached; waiting 10 min (this can repeat for up to an hour) ...")
                        time.sleep(600); continue
                    wait = 65*(attempt + 1)
                    self.log(f"Open-Meteo rate limit reached ({body[:80] or 'no reason given'}); waiting {wait} s ...")
                    time.sleep(wait); attempt += 1; continue
                if e.code == 400:
                    raise RuntimeError(f"Open-Meteo rejected the request: {body}")
                time.sleep(5*(attempt + 1)); attempt += 1
            except OpenMeteoLimit:
                raise
            except Exception as e:  # network hiccup
                self.log(f"Network error ({e}); retrying"); time.sleep(5*(attempt + 1)); attempt += 1
        raise RuntimeError("Could not reach Open-Meteo after several attempts.")

    def _fetch_block(self, i0, j0, ym):
        start, end = self._month_range(ym)
        today = dt.date.today()
        if start > today: raise RuntimeError(f"No historic data for {start} (in the future).")
        end = min(end, today - dt.timedelta(days=2))
        nodes = [(i0 + di, j0 + dj) for di in range(-(self.block//2), self.block//2 + 1)
                 for dj in range(-(self.block//2), self.block//2 + 1)]
        nodes = [n for n in nodes if (n[0], n[1], ym) not in self.mem and not os.path.exists(self._path(n[0], n[1], ym))]
        if (i0, j0) not in nodes and (i0, j0, ym) not in self.mem:
            nodes.append((i0, j0))
        lats = [self._node(i, j)[0] for i, j in nodes]; lons = [self._node(i, j)[1] for i, j in nodes]
        base = dict(latitude=",".join(f"{x:.4f}" for x in lats), longitude=",".join(f"{x:.4f}" for x in lons),
                    start_date=start.isoformat(), end_date=end.isoformat(), timezone="GMT")
        self.log(f"Downloading {start:%Y-%m} weather + marine data for {len(nodes)} grid points near "
                 f"{lats[len(lats)//2]:.1f}, {lons[len(lons)//2]:.1f}")
        wx = self._http(self.WX_URL, dict(base, hourly=",".join(self.WX_VARS), wind_speed_unit="ms"))
        mar = self._http(self.MAR_URL, dict(base, hourly=",".join(self.MAR_VARS), cell_selection="sea"))
        if isinstance(wx, dict): wx = [wx]
        if isinstance(mar, dict): mar = [mar]
        for k, (i, j) in enumerate(nodes):
            d = self._parse(wx[k], mar[k])
            p = self._path(i, j, ym); os.makedirs(os.path.dirname(p), exist_ok=True)
            tmp = p + f".{os.getpid()}.tmp.npz"
            np.savez_compressed(tmp, **d)
            os.replace(tmp, p)
            self.mem[(i, j, ym)] = d

    @staticmethod
    def _arr(h, name, n):
        v = h.get(name)
        if v is None: return np.full(n, np.nan)
        return np.array([np.nan if x is None else float(x) for x in v])

    def _parse(self, wx, mar):
        hw = wx.get("hourly", {}); hm = mar.get("hourly", {}) if mar else {}
        t = np.array([to_epoch(s) for s in hw.get("time", [])])
        n = len(t)
        uw = wx.get("hourly_units", {}); um = mar.get("hourly_units", {}) if mar else {}
        ws = self._arr(hw, "wind_speed_10m", n)*_speed_to_ms(uw.get("wind_speed_10m", "m/s"))
        wd = self._arr(hw, "wind_direction_10m", n)
        gust = self._arr(hw, "wind_gusts_10m", n)*_speed_to_ms(uw.get("wind_gusts_10m", "m/s"))
        rad = np.radians(wd)
        d = dict(t=t, wind_u=-ws*np.sin(rad), wind_v=-ws*np.cos(rad), gust=gust,
                 sw_rad=self._arr(hw, "shortwave_radiation", n), cloud=self._arr(hw, "cloud_cover", n),
                 air_t=self._arr(hw, "temperature_2m", n))
        tm = np.array([to_epoch(s) for s in hm.get("time", [])]) if hm else t
        def onto(name, conv=1.0):
            a = self._arr(hm, name, len(tm))*conv
            if len(tm) == 0: return np.full(n, np.nan)
            if len(tm) == n and np.allclose(tm, t): return a
            return np.interp(t, tm, a, left=np.nan, right=np.nan)
        cs = onto("ocean_current_velocity", _speed_to_ms(um.get("ocean_current_velocity", "km/h")))
        cd = np.radians(onto("ocean_current_direction"))
        d.update(hs=onto("wave_height"), tp=onto("wave_period"), wave_dir=onto("wave_direction"),
                 swell_hs=onto("swell_wave_height"),
                 cur_u=cs*np.sin(cd), cur_v=cs*np.cos(cd),           # direction = heading toward
                 sst=onto("sea_surface_temperature"), sea_level=onto("sea_level_height_msl"))
        return d

    def todo(self, points, months, margin_deg=3.0):
        """Grid blocks along the points that are not cached yet, for a set of yyyymm months."""
        need = set()
        for lat, lon in points:
            for dlat in np.arange(-margin_deg, margin_deg + 1e-9, self.res*self.block):
                for dlon in np.arange(-margin_deg, margin_deg + 1e-9, self.res*self.block):
                    i, j = int(math.floor((lat + dlat)/self.res)), int(math.floor((lon + dlon)/self.res))
                    for ym in months:
                        need.add((i, j, ym))
        return [n for n in sorted(need) if not os.path.exists(self._path(*n)) and n not in self.mem]

    def prefetch(self, points, t0, t1, margin_deg=3.0, log=None, months=None):
        """Download every grid block along a list of (lat, lon) points for the months t0..t1
        (or for an explicit set of yyyymm months)."""
        if months is None:
            months = set()
            d = from_epoch(t0).replace(day=1)
            while d <= from_epoch(t1):
                months.add(int(d.strftime("%Y%m")))
                d = (d + dt.timedelta(days=32)).replace(day=1)
        todo = self.todo(points, months, margin_deg)
        for k, (i, j, ym) in enumerate(todo):
            if os.path.exists(self._path(i, j, ym)) or (i, j, ym) in self.mem:
                continue
            if log: log(f"Prefetch {k + 1}/{len(todo)}")
            self._fetch_block(i, j, ym)
        return len(todo)

    # ---------- sampling
    def sample(self, lat, lon, t):
        fi, fj = lat/self.res, lon/self.res
        i0, j0 = int(math.floor(fi)), int(math.floor(fj))
        wi, wj = fi - i0, fj - j0
        ym = int(from_epoch(t).strftime("%Y%m"))
        acc = {k: 0.0 for k in FIELDS}; wsum = {k: 0.0 for k in FIELDS}
        for di, dj, w in ((0, 0, (1-wi)*(1-wj)), (1, 0, wi*(1-wj)), (0, 1, (1-wi)*wj), (1, 1, wi*wj)):
            if w <= 0: continue
            d = self._get(i0 + di, j0 + dj, ym)
            tt = d["t"]
            if len(tt) == 0: continue
            k = np.searchsorted(tt, t)
            k = min(max(k, 1), len(tt) - 1)
            f = (t - tt[k-1])/max(tt[k] - tt[k-1], 1)
            f = min(max(f, 0.0), 1.0)
            if t > tt[-1] + 3600:      # beyond month end within this file -> next month
                continue
            for name in FIELDS:
                a, b = d[name][k-1], d[name][k]
                val = a*(1-f) + b*f
                if np.isfinite(val):
                    acc[name] += w*val; wsum[name] += w
        out = {}
        defaults = dict(hs=0.0, tp=5.0, wave_dir=0.0, swell_hs=0.0, cur_u=0.0, cur_v=0.0, sst=12.0,
                        sea_level=0.0, sw_rad=0.0, cloud=50.0, air_t=12.0, gust=0.0, wind_u=0.0, wind_v=0.0)
        for name in FIELDS:
            out[name] = acc[name]/wsum[name] if wsum[name] > 0 else defaults[name]
        out["marine_ok"] = wsum["hs"] > 0
        out["current_includes_stokes"] = True   # SMOC total current = Eulerian + waves (Stokes) + tides
        return out


# ---------------------------------------------------------------- synthetic provider
class SyntheticProvider:
    """Deterministic pseudo-climate for offline testing (not real weather)."""
    def __init__(self, seed=1, **kw):
        self.rng = np.random.default_rng(seed)
        n = 140
        self.lows = dict(t0=self.rng.uniform(-10, 375, n)*86400, lat0=self.rng.uniform(35, 62, n),
                         lon0=self.rng.uniform(-80, -40, n), r=self.rng.uniform(500, 1100, n)*1e3,
                         amp=self.rng.uniform(5, 17, n), speed=self.rng.uniform(8, 15, n), dlat=self.rng.uniform(-0.15, 0.35, n))

    def sample(self, lat, lon, t):
        doy = (from_epoch(t).timetuple().tm_yday)
        season = math.cos(2*math.pi*(doy - 15)/365)        # +1 mid-winter, -1 mid-summer
        # mean westerlies peaking near 50N
        u = (8.5 + 3*season)*math.exp(-((lat - 50)/12)**2) - 5*math.exp(-((lat - 22)/6)**2)
        v = 0.8*math.sin(math.radians(lon*3))
        # travelling lows (cyclonic, moving east)
        L = self.lows
        ty = t % (365.25*86400)
        days = (ty - L["t0"])/86400
        active = (days > 0) & (days < 9)
        if active.any():
            clat = L["lat0"][active] + L["dlat"][active]*days[active]*3
            clon = L["lon0"][active] + L["speed"][active]*86400*days[active]/(111e3*np.cos(np.radians(clat)))
            dx = (lon - clon)*111e3*math.cos(math.radians(lat)); dy = (lat - clat)*111e3
            r = np.hypot(dx, dy) + 1
            life = np.sin(np.pi*days[active]/9)*(0.65 + 0.35*season)
            sp = L["amp"][active]*life*(r/L["r"][active])*np.exp(0.5*(1 - (r/L["r"][active])**2))
            u += float(np.sum(-sp*dy/r)); v += float(np.sum(sp*dx/r))
        ws = math.hypot(u, v)
        hs = min(0.024*ws**2 + 0.6, 14.0); tp = 3.0 + 0.6*ws**0.8 + 2.0
        wave_dir = (math.degrees(math.atan2(-u, -v))) % 360
        # Gulf Stream / North Atlantic Drift: jet along a curve
        def jet(lat_c, width, sp):
            return sp*math.exp(-((lat - lat_c)/width)**2)
        gs_lat = 38 + 0.25*(lon + 70) if -75 < lon < -40 else (45 + 0.12*(lon + 40) if lon >= -40 else 35)
        cu = jet(gs_lat, 1.0, 1.2 if lon < -55 else 0.35) + 0.08
        cv = 0.15*math.exp(-((lat - gs_lat)/1.0)**2) if lon < -55 else 0.03
        # tides (M2) near shelves
        tide = 0.15*math.cos(2*math.pi*t/44712 + lon/10)
        cu += 0.05*tide; cv += 0.05*tide
        # sun
        decl = math.radians(23.44)*math.sin(2*math.pi*(doy - 80)/365)
        hour = ((t % 86400)/3600 + lon/15) % 24
        ha = math.radians(15*(hour - 12))
        sinel = math.sin(math.radians(lat))*math.sin(decl) + math.cos(math.radians(lat))*math.cos(decl)*math.cos(ha)
        cloud = 55 + 25*math.sin(t/86400*1.3 + lat)
        sw = max(sinel, 0)*1000*(1 - 0.65*cloud/100)
        sst = 26 - 0.42*(lat - 20) + 3*(-season) + (3 if abs(lat - gs_lat) < 2 and lon < -50 else 0)
        return dict(wind_u=u, wind_v=v, gust=ws*1.35, sw_rad=sw, cloud=cloud, air_t=sst - 1,
                    hs=hs, tp=tp, wave_dir=wave_dir, swell_hs=hs*0.5, cur_u=cu, cur_v=cv, sst=sst,
                    sea_level=tide, marine_ok=True)


# ---------------------------------------------------------------- land
class LandMask:
    """Point-in-polygon land test. Uses Natural Earth 50m land (downloaded once, cached) when
    available, otherwise a built-in coarse North Atlantic outline (~30-60 km accuracy)."""
    NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson"
    NE_COUNTRIES_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
    # Atlantic island groups that belong to European countries but sit far out in the ocean.
    # Whether a landfall there counts as reaching Europe is a scenario choice (atlantic_islands_count).
    ATLANTIC_ISLANDS = {"Azores": (36.5, 40.2, -31.6, -24.5), "Madeira": (32.3, 33.3, -17.6, -16.0),
                        "Canary Islands": (27.4, 29.6, -18.4, -13.0)}

    def __init__(self, cache_dir="cache", allow_download=True, log=print):
        self.polys = []
        p = os.path.join(cache_dir, "ne_50m_land.geojson")
        if not os.path.exists(p) and allow_download:
            try:
                os.makedirs(cache_dir, exist_ok=True)
                log("Downloading Natural Earth coastline (one time, ~2 MB) ...")
                urllib.request.urlretrieve(self.NE_URL, p)
            except Exception as e:
                log(f"Coastline download failed ({e}); using the built-in coarse outline.")
        if os.path.exists(p):
            try:
                gj = json.load(open(p, encoding="utf-8"))
                for f in gj["features"]:
                    g = f["geometry"]
                    rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
                    for poly in rings:
                        self._add(np.array(poly[0], float))
                self.source = "Natural Earth 1:50m"
            except Exception:
                self.polys = []
        if not self.polys:
            from .coast import COARSE
            for ring in COARSE:
                self._add(np.array(ring, float))
            self.source = "built-in coarse outline"
        # European countries (idea from jcolter11374/boat-sim #50): CONTINENT == "Europe" in Natural Earth,
        # kept only for rings that lie in Europe itself (France's and the Netherlands' Caribbean and
        # South American territories are part of those countries' shapes too).
        self.europe = []
        pc = os.path.join(cache_dir, "ne_50m_admin_0_countries.geojson")
        if not os.path.exists(pc) and allow_download:
            try:
                log("Downloading Natural Earth country borders (one time, ~4 MB) ...")
                urllib.request.urlretrieve(self.NE_COUNTRIES_URL, pc)
            except Exception as ex:
                log(f"Country download failed ({ex}); Europe is judged from a coarse outline.")
        if os.path.exists(pc):
            try:
                gj = json.load(open(pc, encoding="utf-8"))
                for f in gj["features"]:
                    if (f.get("properties") or {}).get("CONTINENT") != "Europe": continue
                    g = f["geometry"]
                    rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
                    for poly in rings:
                        r = np.array(poly[0], float)
                        if len(r) < 3: continue
                        if r[:, 1].mean() < 26 or r[:, 0].mean() < -35: continue   # overseas territories
                        self.europe.append((r[:, 0].min(), r[:, 0].max(), r[:, 1].min(), r[:, 1].max(), r))
            except Exception:
                self.europe = []
        self.europe_source = "Natural Earth countries" if self.europe else "coarse outline"

    def _add(self, ring):
        if len(ring) < 3: return
        self.polys.append((ring[:, 0].min(), ring[:, 0].max(), ring[:, 1].min(), ring[:, 1].max(), ring))

    @staticmethod
    def _inside(polys, lat, lon):
        for x0, x1, y0, y1, r in polys:
            if not (x0 <= lon <= x1 and y0 <= lat <= y1): continue
            x, y = r[:, 0], r[:, 1]
            xn, yn = np.roll(x, -1), np.roll(y, -1)
            cond = ((y > lat) != (yn > lat))
            if not cond.any(): continue
            xi = x[cond] + (lat - y[cond])*(xn[cond] - x[cond])/(yn[cond] - y[cond])
            if np.count_nonzero(xi > lon) % 2 == 1:
                return True
        return False

    def atlantic_island(self, lat, lon):
        for name, (a, b, c, d) in self.ATLANTIC_ISLANDS.items():
            if a <= lat <= b and c <= lon <= d: return name
        return None

    def in_europe(self, lat, lon, islands=False):
        """Is a landfall at (lat, lon) a landfall in Europe? Iceland, the Faroes, the British Isles and
        mainland Europe count; North Africa and Greenland don't. The Azores, Madeira and the Canaries
        count only when islands=True."""
        if self.atlantic_island(lat, lon):
            return bool(islands)
        if self.europe:
            if self._inside(self.europe, lat, lon): return True
            for b in range(0, 360, 45):          # the boat stops at the coast; allow ~5 km of slack
                la, lo = destination(lat, lon, b, 5000)
                if self._inside(self.europe, la, lo): return True
            return False
        # coarse fallback: the European side of the North Atlantic, minus Greenland and North Africa
        if lon < -32 or lon > 45 or lat < 34: return False
        if lat > 67.5 and lon < -10: return False                 # north-east Greenland
        if lat < 36.0 and lon < 11: return False                  # Morocco, Algeria
        return True

    def is_land(self, lat, lon):
        for x0, x1, y0, y1, r in self.polys:
            if not (x0 <= lon <= x1 and y0 <= lat <= y1): continue
            x, y = r[:, 0], r[:, 1]
            xn, yn = np.roll(x, -1), np.roll(y, -1)
            cond = ((y > lat) != (yn > lat))
            if not cond.any(): continue
            xi = x[cond] + (lat - y[cond])*(xn[cond] - x[cond])/(yn[cond] - y[cond])
            if np.count_nonzero(xi > lon) % 2 == 1:
                return True
        return False

    def land_ahead(self, lat, lon, bearing_deg, dist_km, steps=6):
        for k in range(1, steps + 1):
            la, lo = destination(lat, lon, bearing_deg, dist_km*1000*k/steps)
            if self.is_land(la, lo): return True
        return False

    def dist_to_land_km(self, lat, lon, max_km=300):
        for d in (5, 15, 30, 60, 100, 150, 220, 300):
            if d > max_km: break
            for b in range(0, 360, 30):
                la, lo = destination(lat, lon, b, d*1000)
                if self.is_land(la, lo): return float(d)
        return float(max_km)


# ---------------------------------------------------------------- geodesy
R_EARTH = 6371e3


def destination(lat, lon, bearing_deg, dist_m):
    p1, l1, b = math.radians(lat), math.radians(lon), math.radians(bearing_deg)
    d = dist_m/R_EARTH
    p2 = math.asin(math.sin(p1)*math.cos(d) + math.cos(p1)*math.sin(d)*math.cos(b))
    l2 = l1 + math.atan2(math.sin(b)*math.sin(d)*math.cos(p1), math.cos(d) - math.sin(p1)*math.sin(p2))
    return math.degrees(p2), (math.degrees(l2) + 540) % 360 - 180


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R_EARTH*math.asin(math.sqrt(min(a, 1.0)))/1000


def bearing_deg(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2); dl = math.radians(lon2 - lon1)
    x = math.sin(dl)*math.cos(p2); y = math.cos(p1)*math.sin(p2) - math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


class TwoGridProvider:
    """A fine grid where the currents are narrow and fast, a coarse grid everywhere else.

    The Gulf Stream and the North Atlantic Current are 50-100 km wide; a 1-degree grid smears them.
    On Nov 8, 2026 the same Ocean City -> Ireland voyage (May 2024) took 86 days at 1 degree and
    102 days at 0.25 degree, and the gap built up west of 40W. East of there both moved alike.
    (Idea from jcolter11374/boat-sim #50.)"""

    def __init__(self, coarse, fine, box):
        self.coarse, self.fine = coarse, fine
        self.lat0, self.lat1, self.lon0, self.lon1 = box

    def _pick(self, lat, lon):
        return self.fine if (self.lat0 <= lat <= self.lat1 and self.lon0 <= lon <= self.lon1) else self.coarse

    def sample(self, lat, lon, t):
        return self._pick(lat, lon).sample(lat, lon, t)

    def todo(self, points, months, margin_deg=3.0):
        out = []
        for p, m in ((self.coarse, margin_deg), (self.fine, 1.0)):
            pts = [(la, lo) for la, lo in points if (self._pick(la, lo) is p)]
            if pts: out += p.todo(pts, months, m)
        return out

    def prefetch(self, points, t0, t1, margin_deg=3.0, log=None, months=None):
        n = 0
        for p, m in ((self.coarse, margin_deg), (self.fine, 1.0)):
            pts = [(la, lo) for la, lo in points if (self._pick(la, lo) is p)]
            if pts: n += p.prefetch(pts, t0, t1, margin_deg=m, log=log, months=months)
        return n

    @property
    def calls(self):
        return self.coarse.calls + self.fine.calls


def make_provider(kind, cache_dir="cache", log=print, res_deg=1.0, seed=1, fine_grid=None):
    if kind == "synthetic":
        return SyntheticProvider(seed=seed)
    coarse = OpenMeteoProvider(cache_dir=cache_dir, res_deg=res_deg, log=log)
    if fine_grid and fine_grid.get("deg") and fine_grid["deg"] < res_deg:
        fine = OpenMeteoProvider(cache_dir=cache_dir, res_deg=fine_grid["deg"], log=log)
        return TwoGridProvider(coarse, fine, (fine_grid["lat"][0], fine_grid["lat"][1], fine_grid["lon"][0], fine_grid["lon"][1]))
    return coarse
