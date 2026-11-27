"""Run 043b (27 Nov 2026): three new questions for the idle CPU while run 041 downloads the 2025 weather.
Randolph: "Go" (to the three proposed on 27 Nov). v2 coastlines, Rev E3, four years of weather already on the PC.

1. Approach further south of Scilly. Plan B (run 043a: 81.1%) still loses 18 of 1,000 boats on Scilly. Two variants of
   B with the approach legs about 60 and 90 km south of the islands, same hold (30 km S of the Lizard), same seeds as B.
2. Holding upwind of the pickup point. A boat can't hold against the trades and the stream; it is carried west.
   So hold upwind and let it drift towards the pickup point, not away from it. 14-day station-keeping (1 km, failures
   on) at points upwind of the decided points; compared with holding on the point itself (043a).
     BVI: 20 and 40 km east, and 20 km ESE, of the Norman offing; 15 and 30 km north of Anegada W (east is Anegada).
     Cornwall: 20 km SW and 20 km W of the hold 30 km south of the Lizard.
3. When to leave Mindelo. Three launch windows (15 Nov-10 Dec, 11 Dec-10 Jan, 11 Jan-5 Feb) to the Norman offing and
   to Anegada W, 1,000 each, with the storm check.
About 9 hours. One queue job (run_043b.bat calls both parts). Run from the repo root: python collab/runs_043b/make_runs.py
"""
import json, math, os, sys, copy
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "collab", "runs_043a")); sys.path.insert(0, os.path.join(ROOT, "collab", "east_west"))
import make_ew as EW
OUT = "collab/runs_043b"
def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p
def offset(lat, lon, km_e, km_n):
    return round(lat + km_n / 110.54, 4), round(lon + km_e / (111.32 * math.cos(math.radians(lat))), 4)

# 1. approaches
B = jload("collab/runs_043a/plan_B.json")
HEAD = B["waypoints"][:2]
appr = {}
for tag, wps, txt in (("B60", [[49.15, -7.2], [49.35, -6.3]], "about 60 km south of Scilly"),
                      ("B90", [[48.9, -7.2], [49.1, -6.2]], "about 90 km south of Scilly")):
    s = copy.deepcopy(B); s["waypoints"] = HEAD + wps
    s["name"] = f"Arrival study: Hatteras 45 km -> hold 30 km south of the Lizard, approach {txt} (Rev E3, v2 coasts), run 043b"
    appr[tag] = jsave(s, f"{OUT}/plan_{tag}.json")

# 2. upwind holds
def hold_at(base, tag, lat, lon, label):
    s = copy.deepcopy(jload(base)); s.update(start={"lat": lat, "lon": lon}, target={"lat": lat, "lon": lon}, station=[lat, lon])
    s["name"] = f"{label}: station-keeping within 1 km, 14 days (Rev E3, v2 coasts), run 043b"
    return jsave(s, f"{OUT}/hold_station_{tag}.json")
NO, AW, LD = (18.17, -64.58), (18.72, -64.49), (49.70, -5.20)
ups = {}
for tag, (la, lo), base, lab in [
        ("norman_offing_E20", offset(*NO, 20, 0), "collab/runs_043a/hold_station_norman_offing.json", "BVI, 20 km east of the Norman offing"),
        ("norman_offing_E40", offset(*NO, 40, 0), "collab/runs_043a/hold_station_norman_offing.json", "BVI, 40 km east of the Norman offing"),
        ("norman_offing_ESE20", offset(*NO, 18.5, -7.5), "collab/runs_043a/hold_station_norman_offing.json", "BVI, 20 km ESE of the Norman offing"),
        ("anegada_west_N15", offset(*AW, 0, 15), "collab/runs_043a/hold_station_anegada_west.json", "BVI, 15 km north of Anegada W"),
        ("anegada_west_N30", offset(*AW, 0, 30), "collab/runs_043a/hold_station_anegada_west.json", "BVI, 30 km north of Anegada W"),
        ("lizard_deep_SW20", offset(*LD, -14.1, -14.1), "collab/runs_043a/hold_station_lizard_deep.json", "Cornwall, 20 km SW of the hold 30 km S of the Lizard"),
        ("lizard_deep_W20", offset(*LD, -20, 0), "collab/runs_043a/hold_station_lizard_deep.json", "Cornwall, 20 km W of the hold 30 km S of the Lizard")]:
    ups[tag] = (hold_at(base, tag, la, lo, lab), la, lo)
json.dump({k: [v[1], v[2]] for k, v in ups.items()}, open(os.path.join(ROOT, OUT, "upwind_points.json"), "w"), indent=1)

# 3. Mindelo windows
cross = {t: f"collab/runs_043a/ew_mindelo__{t}.json" for t in ("norman_offing", "anegada_west")}
WIN = [("nov", "2021-11-15", "2021-12-10"), ("dec", "2021-12-11", "2022-01-10"), ("jan", "2022-01-11", "2022-02-05")]

Y4, Y4W, TR = "2021,2022,2023,2024", "2022,2023,2024,2025", EW.TROPICS_CSV
P = "043b_2021-2024_revE3"
east = [(f"approach {t}", sc, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_{t}_v2", "") for t, sc in appr.items()]
east += [(f"Cornwall hold {t}", sc, 500, "2023-08-15", "2023-10-15", Y4, f"hold{P}_station_{t}_v2", None) for t, (sc, _, _) in ups.items() if t.startswith("lizard")]
ew = [(f"BVI hold {t}", sc, 500, "2022-02-01", "2022-04-30", Y4W, f"hold043b_2022-2025_revE3_station_{t}_v2", None) for t, (sc, _, _) in ups.items() if not t.startswith("lizard")]
# "years" names the year a window starts, so the January window uses 2022-2025 for the same four winters
ew += [(f"Mindelo -> {t}, launches {w}", sc, 1000, a, b, Y4W if a[:4] == "2022" else Y4, f"ew{P}_mindelo_{w}__{t}_v2", TR)
       for t, sc in cross.items() for w, a, b in WIN]

# write the .bat files with run 043a's writer (same format); importing it would rewrite 043a's files, so copy its part()
src = open(os.path.join(ROOT, "collab", "runs_043a", "make_runs.py")).read()
ns = {"os": os, "SIM": os.path.join(ROOT, "simulator"), "E3": "designs/revE3_design.json", "chr": chr}
exec(src[src.index("PY = r"):src.index("Y4, Y4W, TR")], ns)
ns["part"]("043b1_east", "Run 043b part 1: approaches further south of Scilly, Cornwall holds upwind", east, False)
ns["part"]("043b2_ew", "Run 043b part 2: BVI holds upwind, Mindelo launch windows", ew, True)
W = ["@echo off", "REM Run 043b: approaches further south of Scilly, holding upwind of the pickup points, Mindelo launch windows.",
     "REM About 9 hours: part 1 eastbound (4 runs, about 2.5 h), part 2 east-west (11 runs, about 6.5 h).", 'cd /d "%~dp0"',
     "echo ============================================================",
     "echo  Run 043b: Scilly approaches, upwind holding, Mindelo launch windows - 15 runs, about 9 hours",
     "echo  Part 1 eastbound (about 2.5 h), then part 2 east-west (about 6.5 h). Started %date% %time%",
     "echo  Logs: collab\\run_log_043b1_east.txt and collab\\run_log_043b2_ew.txt",
     "echo ============================================================",
     "call run_043b1_east.bat", "call run_043b2_ew.bat",
     "echo.", "echo ============================================================", "echo  ALL DONE %date% %time%",
     "echo ============================================================"]
open(os.path.join(ROOT, "simulator", "run_043b.bat"), "w", newline="\r\n").write("\n".join(W) + "\n")
print(len(east), "east;", len(ew), "east-west"); print(json.dumps({k: [v[1], v[2]] for k, v in ups.items()}))
