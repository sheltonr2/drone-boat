"""Dead-boat drift from candidate drop points off Ocean City, MD (default) or off Hatteras, NC (--set hatteras).

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

POINT_SETS = {"ocean_city": POINTS,
              # 13 Nov 2026: the plan moved to Hatteras (docs/Launch_Plan.md, docs/Naval_Review.md)
              "hatteras": {"Inlet, 10 km off": (35.10, -75.72),
                           "45 km off, Stream edge": (34.95, -75.35),
                           "70 km off, east of shoals": (35.00, -75.05)}}
# Diamond Shoals (approximate): the result reports each drift's closest approach, in km
WATCH = {"diamond_shoals": [[35.22, -75.53], [35.15, -75.41]]}

ap = argparse.ArgumentParser()
ap.add_argument("--set", default="ocean_city", choices=sorted(POINT_SETS), help="which drop points")
ap.add_argument("--bulk", action="store_true", help="use downloaded bulk data instead of Open-Meteo")
ap.add_argument("--years", default="2022,2023,2024,2025")
ap.add_argument("--days", type=float, default=30)
ap.add_argument("--leeway", default="0.033", help="comma list of downwind leeway factors, e.g. 0.02,0.033,0.05 (sensitivity)")
a = ap.parse_args()
POINTS = POINT_SETS[a.set]
years = [int(y) for y in a.years.split(",") if y]
if a.bulk:
    from drone_sim.bulk import available_months
    have = set(available_months(CACHE))
    need = [y*100 + m for y in years for m in (5, 6, 7)]
    missing = [n for n in need if n not in have]
    if missing:
        sys.exit(f"Bulk data missing for {missing}: let the download finish first (run_bulk.bat).")
    dates = [(dt.datetime(y, 5, 1, 12) + dt.timedelta(days=3*k)).isoformat() for y in years for k in range(16)]
else:
    dates = [f"{y}-05-15T12:00:00" for y in years]

from drone_sim.console import Progress
rows = []
_lws = [float(x) for x in a.leeway.split(',') if x]
_pg = Progress('Drift runs', len(_lws)*len(POINTS)*len(dates))
for lw in [float(x) for x in a.leeway.split(",") if x]:
  design = D.default_design()
  design.setdefault("drift", {}).update(leeway_downwind=lw, leeway_crosswind=lw*0.008/0.033)
  for name, (lat, lon) in POINTS.items():
    for date in dates:
        sc = {**DEFAULT_SCENARIO, "start": {"lat": lat, "lon": lon}, "start_time": date, "max_days": a.days,
              "initial_mode": "drift", "failures_enabled": False, "provider": "bulk" if a.bulk else "openmeteo",
              "waypoints": [], **({"watch_lines": WATCH} if a.set == "hatteras" else {})}
        r = run_voyage(design, sc, cache_dir=CACHE, log=lambda *x: None)
        row = dict(leeway=lw, drop=name, start=date[:10], outcome=r["outcome"], days=r["days"], km=r["distance_km"],
                   end_lat=round(r["end"]["lat"], 2), end_lon=round(r["end"]["lon"], 2),
                   **({"shoals_km": r["watch_min_km"]["diamond_shoals"]} if r.get("watch_min_km") else {}))
        rows.append(row); _pg.update(len(rows), f"aground so far: {sum(r_['outcome'] == 'aground' for r_ in rows)}")
        print(f"{lw:5.3f} {name:26s} {date[:10]}  {r['outcome']:16s} {r['days']:5.1f} days  end {row['end_lat']}, {row['end_lon']}", flush=True)
print("\nSummary (aground within the period / runs, median eastward progress):")
for lw in sorted({r["leeway"] for r in rows}):
  print(f" leeway {100*lw:.1f}% of wind")
  for name, (lat, lon) in POINTS.items():
    rr = [r for r in rows if r["drop"] == name and r["leeway"] == lw]
    ag = sum(r["outcome"] == "aground" for r in rr)
    east = sorted(r["end_lon"] - lon for r in rr if r["outcome"] != "aground")
    med = f"{east[len(east)//2]:+.1f} deg lon" if east else "n/a (none left at sea)"
    sh = [r["shoals_km"] for r in rr if r.get("shoals_km") is not None]
    shs = f"   within 5 km of Diamond Shoals {sum(x < 5 for x in sh)}/{len(rr)}" if a.set == "hatteras" else ""
    print(f"  {name:26s} aground {ag}/{len(rr)}   median east {med}{shs}")
tag = "bulk" if a.bulk else "openmeteo"
out = os.path.join("..", "results", f"drift_tests_{a.set}_{tag}_{'-'.join(map(str, years))}.json")
json.dump(jsonable(rows), open(out, "w"), indent=1)
print("Saved", out)
