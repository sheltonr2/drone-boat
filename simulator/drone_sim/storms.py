"""Tropical-cyclone encounter climatology for simulated voyages (HURDAT2 analog years).

Real-weather runs use ERA5, which smooths tropical cyclones: boat-sim measured ERA5's peak wind
near the centre at about 0.70 of the best-track wind for tropical storms, falling to about 0.42
for Category 4 (boat-sim #117). Synthetic weather has no tropical cyclones at all. So we
estimate the storm risk separately, from where storms have actually gone.

Method (analog years). For each simulated track (positions with days since launch) and each
season Y in the climatology, shift the voyage to the same calendar dates in year Y and ask:
did any tropical or subtropical cyclone of at least `min_wind_kt` pass within `radius_km` of the
boat at the same hour? The share of seasons with an encounter is the encounter probability
for that voyage. Averaged over many voyages, it gives the risk by launch month and route.
Storm tracks are interpolated linearly from 6-hourly best-track points to hourly.

Data: docs/data/hurdat2_atlantic_1981-2025_box.csv (NOAA NHC HURDAT2, public domain).
"""
import csv
import datetime as dt
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "data", "hurdat2_atlantic_1981-2025_box.csv"))
TROPICAL = {"TS", "HU", "SS", "TD", "SD"}
CATS = [("TS", 34, 64), ("C1-2", 64, 96), ("C3-5", 96, 999)]
# boat-sim #117: median ERA5 peak wind / best-track wind near the centre, by class (2012-2021, 25-60N 82W-5E)
ERA5_RATIO = {"TD": 0.72, "TS": 0.70, "C1": 0.66, "C2": 0.59, "C3": 0.53, "C4": 0.42, "C5": 0.31}


def saffir_simpson(kt):
    if kt < 34: return "TD"
    if kt < 64: return "TS"
    for c, lo in ((5, 137), (4, 113), (3, 96), (2, 83), (1, 64)):
        if kt >= lo: return f"C{c}"


class StormClimatology:
    def __init__(self, path=DEFAULT_CSV, years=(1991, 2025)):
        rows = {}
        for r in csv.reader(l for l in open(path) if not l.startswith("#")):
            if r[0] == "storm_id": continue
            sid, ts, lat, lon, w, st = r
            y = int(ts[:4])
            if not (years[0] <= y <= years[1]): continue
            t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc).timestamp()
            rows.setdefault(sid, []).append((t, float(lat), float(lon), float(w), st))
        self.years = list(range(years[0], years[1] + 1))
        # hourly points of tropical/subtropical systems: arrays t, lat, lon, wind, year
        T, LA, LO, W, Y = [], [], [], [], []
        for sid, pts in rows.items():
            pts.sort()
            for (t0, a0, o0, w0, s0), (t1, a1, o1, w1, s1) in zip(pts, pts[1:]):
                if s0 not in TROPICAL and s1 not in TROPICAL: continue
                n = max(1, int(round((t1 - t0)/3600)))
                for k in range(n):
                    f = k/n
                    w = w0 + (w1 - w0)*f if w0 >= 0 and w1 >= 0 else max(w0, w1)
                    st = s0 if f < 0.5 else s1
                    if st not in TROPICAL: continue
                    T.append(t0 + k*3600); LA.append(a0 + (a1 - a0)*f); LO.append(o0 + (o1 - o0)*f)
                    W.append(w); Y.append(int(dt.datetime.fromtimestamp(t0 + k*3600, dt.timezone.utc).year))
        self.t = np.array(T); self.lat = np.array(LA); self.lon = np.array(LO)
        self.w = np.array(W); self.y = np.array(Y)
        self.hour = np.round(self.t/3600).astype(np.int64)

    def voyage(self, track, start_time, radius_km=200.0, min_wind_kt=34.0):
        """Per analog year: max storm wind (kt) that came within radius_km of the boat (0 = none),
        and the closest approach (km). track: [[lat, lon, day], ...] or [[lat, lon], ...] (spread evenly over `days`)."""
        tr = np.asarray(track, dtype=float)
        if tr.shape[1] < 3:
            raise ValueError("track points need a time (lat, lon, days since launch)")
        d0 = dt.datetime.fromisoformat(start_time).replace(tzinfo=dt.timezone.utc)
        days = np.arange(0.0, tr[-1, 2] + 1e-9, 1/24)              # hourly along the voyage
        lat = np.interp(days, tr[:, 2], tr[:, 0]); lon = np.interp(days, tr[:, 2], tr[:, 1])
        res = []
        for Y in self.years:
            try: s = d0.replace(year=Y)
            except ValueError: s = d0.replace(year=Y, day=28)
            hrs = np.round((s.timestamp() + days*86400)/3600).astype(np.int64)
            m = (self.hour >= hrs[0]) & (self.hour <= hrs[-1]) & (self.w >= min_wind_kt)
            if not m.any():
                res.append((Y, 0.0, float("inf"))); continue
            idx = np.searchsorted(hrs, self.hour[m]); idx = np.clip(idx, 0, len(hrs) - 1)
            ok = hrs[idx] == self.hour[m]
            if not ok.any():
                res.append((Y, 0.0, float("inf"))); continue
            bl, bo = lat[idx[ok]], lon[idx[ok]]
            sl, so, sw = self.lat[m][ok], self.lon[m][ok], self.w[m][ok]
            dlat = np.radians(sl - bl); dlon = np.radians(so - bo)
            a = np.sin(dlat/2)**2 + np.cos(np.radians(bl))*np.cos(np.radians(sl))*np.sin(dlon/2)**2
            dist = 2*6371*np.arcsin(np.sqrt(np.clip(a, 0, 1)))
            inside = dist <= radius_km
            res.append((Y, float(sw[inside].max()) if inside.any() else 0.0, float(dist.min())))
        return res


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1 - p)/n + z*z/(4*n*n))/d
    return (max(0.0, c - h), min(1.0, c + h))


def mc_storm_table(mc, clim, radius_km=200.0, min_wind_kt=34.0, boot=2000, seed=1):
    """Encounter probabilities for a Monte Carlo result, overall and by launch month.
    Voyages in the same season share that season's storms, so the 95% interval comes from
    resampling whole seasons (bootstrap over analog years), not from counting voyage-years."""
    rows = []   # (group keys, year, wmax)
    for run in mc["runs"]:
        if not run.get("track") or len(run["track"][0]) < 3: continue
        mon = run["start_time"][5:7]
        for Y, wmax, dmin in clim.voyage(run["track"], run["start_time"], radius_km, min_wind_kt):
            rows.append((("all", mon), Y, wmax, run["i"]))
    years = clim.years; yi = {y: k for k, y in enumerate(years)}
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(years), size=(boot, len(years)))
    out = {}
    keys = sorted({k for ks, *_ in rows for k in ks})
    for key in keys:
        sel = [(Y, w, i) for ks, Y, w, i in rows if key in ks]
        per = {c: np.zeros(len(years)) for c in ("any", "TS", "C1-2", "C3-5")}; cnt = np.zeros(len(years))
        for Y, w, i in sel:
            k = yi[Y]; cnt[k] += 1
            if w >= 34: per["any"][k] += 1
            for c, lo, hi in CATS:
                if lo <= w < hi: per[c][k] += 1
        frac = per["any"]/np.maximum(cnt, 1)
        bs = frac[pick].mean(axis=1)
        out[key] = dict(voyages=len({i for _, _, i in sel}), seasons=len(years),
                        **{f"p_{c}": round(float(per[c].sum()/max(cnt.sum(), 1)), 4) for c in per},
                        ci95_any=[round(float(np.percentile(bs, 2.5)), 4), round(float(np.percentile(bs, 97.5)), 4)],
                        seasons_with_any=int((per["any"] > 0).sum()))
    return out
