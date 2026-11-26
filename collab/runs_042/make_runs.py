"""Run 042 (26 Nov 2026): safer approaches to Cornwall, found by run 039.

On the detailed coast (run 039) the final plan loses 39 of 1000 voyages on the Isles of Scilly (the leg from 49.6N 7.2W
to 49.7N 6.4W passes ~20 km south of them, and boats set north on that leg hit the Western Rocks) and 11 on Lizard
Point during the run in. Natural Earth 1:50m had no Scilly, so runs 026/034 never saw this. Run 037 found the hold
30 km south of the Lizard (49.70N 5.20W) loses 0.4% of boats in 14 days, against 12.8% at the Lizard offing.

Two variants, everything else identical to 039 (same launches, seeds, design Rev E3 and v1 detail coasts), so they
pair with it voyage for voyage. They test options; the plan stays as it is until Randolph decides.
  A south:      approach 40-45 km south of Scilly (49.35N 7.2W, 49.5N 6.4W, 49.7N 5.7W), hold at the Lizard offing as now.
  B south_deep: the same approach, then hold 30 km south of the Lizard (49.70N 5.20W).
Run from the repo root: python collab/runs_042/make_runs.py
"""
import json, os, copy
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(ROOT, "simulator")
OUT = "collab/runs_042"
E3 = "designs/revE3_design.json"
def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p

base = jload("collab/runs_036/plan_detail_coast.json")
HEAD = [[35.0, -74.9], [42.0, -48.0]]
assert base["waypoints"][:2] == HEAD
A = copy.deepcopy(base)
A.update(name="Arrival study: Hatteras 45 km -> Lizard offing hold, approach 40-45 km south of Scilly - detailed coast (Rev E3), run 042A",
         waypoints=HEAD + [[49.35, -7.2], [49.5, -6.4], [49.7, -5.7]])
B = copy.deepcopy(base)
B.update(name="Arrival study: Hatteras 45 km -> hold 30 km south of the Lizard, approach 40-45 km south of Scilly - detailed coast (Rev E3), run 042B",
         waypoints=HEAD + [[49.35, -7.2], [49.5, -6.4]], target={"lat": 49.70, "lon": -5.20})
runs = [("A: approach south of Scilly, Lizard offing hold", jsave(A, f"{OUT}/plan_south.json"), "plan042_2021-2024_revE3_south_lizard_offing_detail"),
        ("B: approach south of Scilly, hold 30 km south of the Lizard", jsave(B, f"{OUT}/plan_south_deep.json"), "plan042_2021-2024_revE3_south_lizard_deep_detail")]

PY = r".venv\Scripts\python.exe"
name, title = "042_approach_variants", "Run 042: safer approaches to Cornwall (south of Scilly; hold 30 km south of the Lizard), Rev E3, detailed coast"
log = rf"..\collab\run_log_{name}.txt"
L = ["@echo off", f"REM {title}", "REM Same launches and seeds as run 039 (1000 voyages, 1-20 May, 2021-2024). Written by collab/runs_042/make_runs.py (26 Nov 2026).",
     "REM A run whose result file exists is skipped, so this file can be restarted after a reboot.",
     "setlocal EnableDelayedExpansion", 'cd /d "%~dp0"', "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}",
     "echo ============================================================", f"echo  {title}",
     f"echo  {len(runs)} runs. Expected time: about 2 h 00 min.", "echo  Progress shows below, one line per run. Started %date% %time%",
     "echo ============================================================", f'echo {title}, started %date% %time% >> "%LOG%"']
for i, (lab, scen, out) in enumerate(runs, 1):
    o = rf"..\results\{out}.json"
    L += ["echo.", f"echo RUN {i} of {len(runs)}: {lab}   (started !time!)", f"if exist {o} (",
          "  echo   already finished, skipping", f'  echo ==== RUN: {lab} already finished, skipped ==== >> "%LOG%"', ") else (",
          f'  echo ==== RUN: {lab} ==== >> "%LOG%"',
          f'  {PY} -m drone_sim.cli mc --design ..\\{E3.replace("/", chr(92))} --scenario ..\\{scen.replace("/", chr(92))} '
          f'--runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out {o} >> "%LOG%" 2>&1',
          f'  if exist {o} {PY} ..\\collab\\summarize_mc.py {o} >> "%LOG%" 2>&1',
          f'  if exist {o} {PY} -m drone_sim.cli stormcheck --mc {o} --out {o[:-5]}_storms.json >> "%LOG%" 2>&1',
          f"  if exist {o} (echo   finished !time!) else (echo   FAILED: see {log})", ")"]
L += ['echo === DONE %date% %time% >> "%LOG%"', "echo.", "echo ============================================================",
      "echo  ALL DONE %date% %time%", f"echo  Log: {log[3:]}", "echo ============================================================"]
open(os.path.join(SIM, f"run_{name}.bat"), "w", newline="\r\n").write("\n".join(L) + "\n")
print(f"simulator/run_{name}.bat")
