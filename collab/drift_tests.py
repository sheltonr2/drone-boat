"""Dead-boat drift from candidate drop points off Ocean City, MD.

Question: how far offshore must we launch so a boat that fails in its first days drifts
out to sea (or into the Gulf Stream) instead of back onto the coast?

Run from the simulator folder:
  python ..\\collab\\drift_tests.py                      # Open-Meteo, 15 May of 2022-2025 (the Nov 8 test)
  python ..\\collab\\drift_tests.py --bulk --years 2023  # bulk data, a drop every 3 days 1 May-15 June
Since 9 Nov 2026 the dead boat drifts by the leeway model (3.3% of the wind, near downwind).
"""
import argparse, datetime as dt, json, os, sys
sys.path.insert(0, os.getcwd())
from drone_sim import design as D
from drone_sim.sim import run_voyage, DEFAULT_SCENARIO
from drone_sim.server import CACHE, jsonable

POINTS = {"25 km off (old plan)": (38.25, -74.65),
          "50 km off": (38.18, -74.54),
          "100 km off (current plan)": (38.02, -74.01),
          "150 km off (shelf edge)": (37.86, -73.47)}

ap = argparse.ArgumentParser()
ap.add_argument("--bulk", action="store_true", help="use downloaded bulk data instead of Open-Meteo")
ap.add_argument("--years", default="2022,2023,2024,2025")
ap.add_argument("--days", type=float, default=30)
a = ap.parse_args()
years = [int(y) for y in a.years.split(",") if y]
if a.bulk:
    dates = [(dt.datetime(y, 5, 1, 12) + dt.timedelta(days=3*k)).isoformat() for y in years for k in range(16)]
else:
    dates = [f"{y}-05-15T12:00:00" for y in years]

rows = []
for name, (lat, lon) in POINTS.items():
    for date in dates:
        sc = {**DEFAULT_SCENARIO, "start": {"lat": lat, "lon": lon}, "start_time": date, "max_days": a.days,
              "initial_mode": "drift", "failures_enabled": False, "provider": "bulk" if a.bulk else "openmeteo",
              "waypoints": []}
        r = run_voyage(D.default_design(), sc, cache_dir=CACHE, log=lambda *x: None)
        row = dict(drop=name, start=date[:10], outcome=r["outcome"], days=r["days"], km=r["distance_km"],
                   end_lat=round(r["end"]["lat"], 2), end_lon=round(r["end"]["lon"], 2))
        rows.append(row)
        print(f"{name:26s} {date[:10]}  {r['outcome']:16s} {r['days']:5.1f} days  end {row['end_lat']}, {row['end_lon']}", flush=True)
print("\nSummary (aground within the period / runs, median eastward progress):")
for name, (lat, lon) in POINTS.items():
    rr = [r for r in rows if r["drop"] == name]
    ag = sum(r["outcome"] == "aground" for r in rr)
    east = sorted(r["end_lon"] - lon for r in rr if r["outcome"] != "aground")
    med = east[len(east)//2] if east else float("nan")
    print(f"  {name:26s} aground {ag}/{len(rr)}   median east {med:+.1f} deg lon")
tag = "bulk" if a.bulk else "openmeteo"
out = os.path.join("..", "results", f"drift_tests_ocean_city_{tag}.json")
json.dump(jsonable(rows), open(out, "w"), indent=1)
print("Saved", out)
