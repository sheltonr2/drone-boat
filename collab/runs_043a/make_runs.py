"""Run 043a (26 Nov 2026, evening): the decided plans on the v2 coastlines, using the four years of weather already
on the PC, while run 041 downloads the 2025 weather. Randolph: "Are there any sims running? Can we put sims in to run
for the next 10+ hours?"

v2 coastlines (docs/data/coast/detail_*_v2.json) add EMODnet shallows (under 2 m), UKHO wrecks and obstructions where
the seabed is under 5 m, and drop the non-dangerous wrecks v1 counted by mistake. Rev E3 throughout. Same windows and
seeds as runs 036-042, so every result pairs with its v1 twin and shows the depth data's effect.

Part 1, eastbound (2021-2024, 1,000 voyages each, launches 1-20 May unless noted):
  B  the decided plan: approach 40-45 km south of Scilly, hold 30 km south of the Lizard (pairs with 042B)
  A  the fallback: same approach, Lizard offing (pairs with 042A)
  old  the 18 Nov plan (pairs with 039)
  B in April, B 21 May-15 Jun (the edges of the usable window), B from the 70 km fallback drop (35.00N 75.05W)
  Cornwall holds, 500 each, mid-Aug to mid-Oct: station-keeping and dead-boat drift at both holds (pairs with 037)
Part 2, east-west (winters 2021-22 to 2024-25):
  Mindelo -> Norman offing (decided) and -> Anegada W, 1,000 each (pairs with 038)
  El Hierro via 20N 28W -> Norman offing, 1,000 (the fallback launch, 1 Nov-20 Dec)
  BVI holds, 500 each, Feb-Apr 2022-2025: station-keeping and drift at both points (pairs with 036)
One queue job (run_043a_v2_4yr.bat calls both parts), so the queue hands over only once.
Run from the repo root: python collab/runs_043a/make_runs.py
"""
import json, os, sys, copy
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(ROOT, "simulator")
sys.path.insert(0, os.path.join(ROOT, "collab", "east_west"))
import make_ew as EW
OUT = "collab/runs_043a"
E3 = "designs/revE3_design.json"
CARIB, CORN, HATT = (f"docs/data/coast/detail_{r}_v2.json" for r in ("carib", "cornwall", "hatteras"))
def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p
def v2(sc, name_suffix=" - v2 coasts"):
    s = copy.deepcopy(sc); dc = s.get("detail_coast")
    s["detail_coast"] = [d.replace(".json", "_v2.json") for d in dc] if isinstance(dc, list) else dc.replace(".json", "_v2.json")
    s["name"] = s["name"] + name_suffix; return s

# ---- part 1, eastbound
B = jsave(v2(jload("collab/runs_042/plan_south_deep.json")), f"{OUT}/plan_B.json")
A = jsave(v2(jload("collab/runs_042/plan_south.json")), f"{OUT}/plan_A.json")
OLD = jsave(v2(jload("collab/runs_036/plan_detail_coast.json")), f"{OUT}/plan_old.json")
b70 = v2(jload("collab/runs_042/plan_south_deep.json"), " - v2 coasts, 70 km fallback drop")
b70["start"] = {"lat": 35.00, "lon": -75.05}
B70 = jsave(b70, f"{OUT}/plan_B_drop70.json")
holds_c = {}
for tag in ("lizard_deep", "lizard"):
    for mode in ("station", "drift"):
        holds_c[f"{mode}_{tag}"] = jsave(v2(jload(f"collab/runs_036/hold_{mode}_{tag}.json")), f"{OUT}/hold_{mode}_{tag}.json")
# ---- part 2, east-west
cross = {t: jsave(v2(jload(f"collab/runs_036/ew_mindelo__{t}.json")), f"{OUT}/ew_mindelo__{t}.json") for t in ("norman_offing", "anegada_west")}
eh = copy.deepcopy(jload("collab/east_west/el_hierro_south__bvi_s.json"))
eh.update(name="BVI pickup study: El Hierro via 20N 28W -> 18 km south of Norman Island (Rev E3, v2 coasts)",
          target={"lat": 18.170, "lon": -64.580}, waypoints=[[20.0, -28.0], [18.15, -63.90]], detail_coast=CARIB,
          note="run 043a: the fallback launch to the decided BVI pickup point (26 Nov 2026)")
EHS = jsave(eh, f"{OUT}/ew_el_hierro_south__norman_offing.json")
holds_b = {}
for tag in ("norman_offing", "anegada_west"):
    for mode in ("station", "drift"):
        holds_b[f"{mode}_{tag}"] = jsave(v2(jload(f"collab/runs_036/hold_{mode}_{tag}.json")), f"{OUT}/hold_{mode}_{tag}.json")

PY = r".venv\Scripts\python.exe"
def part(name, title, runs, ew):
    log = rf"..\collab\run_log_{name}.txt"
    L = ["@echo off", f"REM {title}", "REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.",
         "setlocal EnableDelayedExpansion", 'cd /d "%~dp0"', "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}"]
    if ew:
        L += ['set DRONE_SIM_HOME=%~dp0workspace_ew', 'if not exist workspace_ew\\cache mkdir workspace_ew\\cache',
              'for %%f in (workspace\\cache\\*.*) do if not exist "workspace_ew\\cache\\%%~nxf" copy /y "%%f" "workspace_ew\\cache\\" >nul']
    L += ["echo ------------------------------------------------------------", f"echo  {title}: {len(runs)} runs",
          "echo ------------------------------------------------------------", f'echo {title}, started %date% %time% >> "%LOG%"']
    for i, (lab, scen, n, frm, to, years, out, storm) in enumerate(runs, 1):
        o = rf"..\results\{out}.json"
        L += ["echo.", f"echo RUN {i} of {len(runs)}: {lab}   (started !time!)", f"if exist {o} (",
              "  echo   already finished, skipping", f'  echo ==== RUN: {lab} already finished, skipped ==== >> "%LOG%"', ") else (",
              f'  echo ==== RUN: {lab} ==== >> "%LOG%"',
              f'  {PY} -m drone_sim.cli mc --design ..\\{E3.replace("/", chr(92))} --scenario ..\\{scen.replace("/", chr(92))} '
              f'--runs {n} --from {frm} --to {to} --years {years} --out {o} >> "%LOG%" 2>&1',
              f'  if exist {o} {PY} ..\\collab\\summarize_mc.py {o} >> "%LOG%" 2>&1']
        if storm is not None:
            L += [f'  if exist {o} {PY} -m drone_sim.cli stormcheck --mc {o}{" --storm-csv " + storm if storm else ""} --out {o[:-5]}_storms.json >> "%LOG%" 2>&1']
        L += [f"  if exist {o} (echo   finished !time!) else (echo   FAILED: see {log})", ")"]
    L += ['echo === DONE %date% %time% >> "%LOG%"', "endlocal"]
    open(os.path.join(SIM, f"run_{name}.bat"), "w", newline="\r\n").write("\n".join(L) + "\n")

Y4, Y4W, TR = "2021,2024".replace(",", ",2022,2023,"), "2022,2023,2024,2025", EW.TROPICS_CSV
P = "043a_2021-2024_revE3"
east = [("B: south of Scilly, hold 30 km S of the Lizard", B, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_B_v2", ""),
        ("A: south of Scilly, Lizard offing", A, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_A_v2", ""),
        ("old: 18 Nov plan", OLD, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_old_v2", ""),
        ("B launched in April", B, 1000, "2023-04-01", "2023-04-30", Y4, f"plan{P}_B_april_v2", ""),
        ("B launched 21 May-15 Jun", B, 1000, "2023-05-21", "2023-06-15", Y4, f"plan{P}_B_latemay_v2", ""),
        ("B from the 70 km drop", B70, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_B_drop70_v2", "")]
east += [(f"Cornwall hold {lab}", sc, 500, "2023-08-15", "2023-10-15", Y4, f"hold{P}_{lab}_v2", None) for lab, sc in holds_c.items()]
ew = [(f"Mindelo -> {t}", sc, 1000, "2021-11-15", "2022-01-10", Y4, f"ew{P}_mindelo__{t}_v2", TR) for t, sc in cross.items()]
ew += [("El Hierro via 20N 28W -> norman_offing", EHS, 1000, "2021-11-01", "2021-12-20", Y4, f"ew{P}_el_hierro_south__norman_offing_v2", TR)]
ew += [(f"BVI hold {lab}", sc, 500, "2022-02-01", "2022-04-30", Y4W, f"hold043a_2022-2025_revE3_{lab}_v2", None) for lab, sc in holds_b.items()]
part("043a1_east_v2", "Run 043a part 1: eastbound plans and Cornwall holds on the v2 coasts", east, False)
part("043a2_ew_v2", "Run 043a part 2: Mindelo and El Hierro to the BVI points, and BVI holds, on the v2 coasts", ew, True)
W = ["@echo off", "REM Run 043a: the decided plans on the v2 coastlines (EMODnet + UKHO depth data), four years of weather already",
     "REM on the PC. About 11 hours: part 1 eastbound (10 runs, about 8 h), part 2 east-west (7 runs, about 3 h).",
     'cd /d "%~dp0"',
     "echo ============================================================",
     "echo  Run 043a: decided plans on the v2 coastlines, 17 runs, about 11 hours",
     "echo  Part 1 eastbound (about 8 h), then part 2 east-west (about 3 h). Started %date% %time%",
     "echo  Logs: collab\\run_log_043a1_east_v2.txt and collab\\run_log_043a2_ew_v2.txt",
     "echo ============================================================",
     "call run_043a1_east_v2.bat", "call run_043a2_ew_v2.bat",
     "echo.", "echo ============================================================", "echo  ALL DONE %date% %time%",
     "echo ============================================================"]
open(os.path.join(SIM, "run_043a_v2_4yr.bat"), "w", newline="\r\n").write("\n".join(W) + "\n")
print(len(east), "east runs;", len(ew), "east-west runs")
