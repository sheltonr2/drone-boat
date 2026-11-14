"""Sea states met along simulated voyage tracks, for the fatigue analysis (docs/Fatigue_Review.md).

Run from the simulator folder on the PC (it needs the bulk weather data):
  .venv\\Scripts\\python.exe ..\\collab\\seastates_along_tracks.py ..\\results\\<mc result>.json ..\\results\\seastates_<name>.json
For every voyage it walks the saved track every 3 hours (interpolating between track points) and samples
significant wave height, both wave periods and the wind. It writes hours spent in each (Hs, Tp) and wind bin,
pooled over all voyages and per voyage, so a fatigue cycle count can be built without the 35 GB of weather.
"""
import json, os, sys, math, datetime as dt
sys.path.insert(0, os.getcwd())
from drone_sim.bulk import BulkProvider, BulkDataMissing
from drone_sim.env import to_epoch
from drone_sim.server import CACHE

src, out = sys.argv[1], sys.argv[2]
R = json.load(open(src))["result"]["runs"]
P = BulkProvider(cache_dir=CACHE, log=lambda *a: None)
STEP_H = 3.0
HS = [0.25*i for i in range(41)]            # bin lower edges, m (0-10 m)
TP = [float(i) for i in range(2, 21)]       # s
WS = [float(i) for i in range(0, 31)]       # m/s
def b(edges, v): return max(0, min(len(edges) - 1, int(sum(v >= e for e in edges)) - 1))
grid = {}; wind = [0.0]*len(WS); per = []; n = 0; missing = 0.0
for k, r in enumerate(R):
    tr = r.get("track") or []
    if len(tr) < 2: continue
    t0 = to_epoch(r["start_time"]); hours = 0.0; hs_max = 0.0
    for (la0, lo0, d0), (la1, lo1, d1) in zip(tr[:-1], tr[1:]):
        steps = max(1, int(round((d1 - d0)*24/STEP_H)))
        for j in range(steps):
            f = (j + 0.5)/steps; d = d0 + f*(d1 - d0)
            try:
                e = P.sample(la0 + f*(la1 - la0), lo0 + f*(lo1 - lo0), t0 + d*86400)
            except BulkDataMissing:        # voyages that run past November: those hours are left out and counted
                missing += (d1 - d0)*24/steps; continue
            if not e.get("marine_ok"): continue
            h = (d1 - d0)*24/steps
            key = f"{b(HS, e['hs'])},{b(TP, e['tp'])}"
            grid[key] = grid.get(key, 0.0) + h
            wind[b(WS, math.hypot(e['wind_u'], e['wind_v']))] += h
            hours += h; hs_max = max(hs_max, e['hs']); n += 1
    per.append(dict(seed=r["seed"], outcome=r["outcome"], days=r["days"], hours_sampled=round(hours, 1), hs_max=round(hs_max, 2)))
    if k % 50 == 0: print(f"{k}/{len(R)} voyages, {n} samples", flush=True)
json.dump(dict(source=os.path.basename(src), step_h=STEP_H, hs_edges=HS, tp_edges=TP, ws_edges=WS,
               hours_by_hs_tp=grid, hours_by_wind=wind, hours_without_weather=round(missing, 1), voyages=per, tp_kind=P.wave_period), open(out, "w"), indent=1)
print("Saved", out)
