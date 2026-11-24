"""Runs 034-035 (24 Nov 2026), asked for by Randolph ("do both"): writes the scenarios and batch files.
034 Rev E3 (20 W stock solar) on the final plan, the same launches and seeds as run 026 (Rev E1), so the difference is paired.
035 holding study 2: station-keeping with a 1 km deadband (scenario key station_radius_km, off by default = 5 km),
    which approximates the firmware's slow box, at the Lizard offing and the Mount's Bay mouth; same seeds as run 028.
Run from the repo root: python collab/runs_034/make_runs.py
"""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(ROOT, "simulator")
def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p

PLAN = "collab/arrival/hatteras_stream__lizard_offing_hold_v2.json"
Y4 = "2021,2022,2023,2024"
hold1 = {}
for tag, nm in (("lizard", "the Lizard offing"), ("mounts", "the mouth of Mount's Bay")):
    sc = jload(f"collab/runs_026/hold_station_{tag}.json")
    sc.update(name=f"Holding study 2: station-keeping at {nm} within 1 km, 14 days (Rev E1)", station_radius_km=1.0)
    hold1[f"station1km_{tag}"] = jsave(sc, f"collab/runs_034/hold_station1km_{tag}.json")

PY = r".venv\Scripts\python.exe"
def bat(name, title, runs, note, minutes, ew=False):
    """runs: list of (label, design, scenario, n, frm, to, years, out, stormcheck csv or None)."""
    log = rf"..\collab\run_log_{name}.txt"
    L = ["@echo off", f"REM {title}", f"REM {note}", f"REM {len(runs)} runs, about {minutes//60} h {minutes%60:02d} min. Written by collab/runs_034/make_runs.py (24 Nov 2026).",
         "REM A run whose result file exists is skipped, so this file can be restarted after a reboot.",
         "setlocal EnableDelayedExpansion", 'cd /d "%~dp0"', "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}"]
    if ew:
        L += ['set DRONE_SIM_HOME=%~dp0workspace_ew', 'if not exist workspace_ew\\cache mkdir workspace_ew\\cache',
              'for %%f in (workspace\\cache\\*.*) do if not exist "workspace_ew\\cache\\%%~nxf" copy /y "%%f" "workspace_ew\\cache\\" >nul']
    L += ["echo ============================================================", f"echo  {title}",
          f"echo  {len(runs)} runs. Expected time: about {minutes//60} h {minutes%60:02d} min.",
          "echo  Progress shows below, one line per run. Started %date% %time%",
          "echo ============================================================", f'echo {title}, started %date% %time% >> "%LOG%"']
    for i, (lab, design, scen, n, frm, to, years, out, storm) in enumerate(runs, 1):
        o = rf"..\results\{out}.json"
        L += ["echo.", f"echo RUN {i} of {len(runs)}: {lab}   (started !time!)", f"if exist {o} (",
              "  echo   already finished, skipping", f'  echo ==== RUN: {lab} already finished, skipped ==== >> "%LOG%"', ") else (",
              f'  echo ==== RUN: {lab} ==== >> "%LOG%"',
              f'  {PY} -m drone_sim.cli mc --design ..\\{design.replace("/", chr(92))} --scenario ..\\{scen.replace("/", chr(92))} '
              f'--runs {n} --from {frm} --to {to} --years {years} --out {o} >> "%LOG%" 2>&1',
              f'  if exist {o} {PY} ..\\collab\\summarize_mc.py {o} >> "%LOG%" 2>&1']
        if storm is not None:
            csv = f" --storm-csv {storm}" if storm else ""
            L += [f'  if exist {o} {PY} -m drone_sim.cli stormcheck --mc {o}{csv} --out {o[:-5]}_storms.json >> "%LOG%" 2>&1']
        L += [f"  if exist {o} (echo   finished !time!) else (echo   FAILED: see {log})", ")"]
    L += ['echo === DONE %date% %time% >> "%LOG%"', "echo.", "echo ============================================================",
          "echo  ALL DONE %date% %time%", f"echo  Log: {log[3:]}", "echo ============================================================"]
    open(os.path.join(SIM, f"run_{name}.bat"), "w", newline="\r\n").write("\n".join(L) + "\n")
    print(f"simulator/run_{name}.bat: {len(runs)} runs, about {minutes} min")


bat("034_revE3_plan", "Run 034: Rev E3 (20 W stock solar) on the final plan, four weather years",
    [("Rev E3, 1000 voyages", "designs/revE3_design.json", PLAN, 1000, "2023-05-01", "2023-05-20", Y4, "plan034_2021-2024_revE3_lizard_offing_v2", "")],
    "Same scenario, launches and seeds as run 026 (Rev E1), so the difference is paired. Storm check after.", 62)
bat("035_holding_1km", "Run 035: holding study 2: station-keeping within 1 km at the Lizard offing and Mount's Bay mouth",
    [(lab, "designs/revE1_design.json", scen, 500, "2023-08-15", "2023-10-15", Y4, f"hold035_2021-2024_revE1_{lab}", None) for lab, scen in hold1.items()],
    "Same seeds as run 028's station runs; only the station deadband changes (5 km to 1 km).", 20)
