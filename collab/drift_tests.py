"""Dead-boat drift from three possible drop points off Ocean City, MD, on four May dates.

Question: how far offshore must we launch so a boat that fails in its first days drifts
out to sea (or into the Gulf Stream) instead of back onto the coast?
Run from the simulator folder:  python ..\\collab\\drift_tests.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from drone_sim import design as D
from drone_sim.sim import run_voyage, DEFAULT_SCENARIO
from drone_sim.server import CACHE, jsonable

POINTS = {"25 km off (current plan)": (38.25, -74.65),
          "100 km off": (38.02, -74.01),
          "150 km off (shelf edge)": (37.86, -73.47)}
DATES = ["2022-05-15T12:00:00", "2023-05-15T12:00:00", "2024-05-15T12:00:00", "2025-05-15T12:00:00"]

rows = []
for name, (lat, lon) in POINTS.items():
    for date in DATES:
        sc = {**DEFAULT_SCENARIO, "start": {"lat": lat, "lon": lon}, "start_time": date, "max_days": 30,
              "initial_mode": "drift", "failures_enabled": False, "provider": "openmeteo", "waypoints": []}
        r = run_voyage(D.default_design(), sc, cache_dir=CACHE, log=lambda *a: None)
        row = dict(drop=name, start=date[:10], outcome=r["outcome"], days=r["days"], km=r["distance_km"],
                   end_lat=round(r["end"]["lat"], 2), end_lon=round(r["end"]["lon"], 2))
        rows.append(row)
        print(f"{name:26s} {date[:10]}  {r['outcome']:16s} {r['days']:5.1f} days  end {row['end_lat']}, {row['end_lon']}", flush=True)
out = os.path.join("..", "results", "drift_tests_ocean_city.json")
json.dump(jsonable(rows), open(out, "w"), indent=1)
print("Saved", out)
