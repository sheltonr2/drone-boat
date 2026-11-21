"""Runs 026-033 (21 Nov 2026), asked for by Randolph ("let's do all 7"): writes the designs, scenarios and batch files.

  python collab/runs_026/make_runs.py

026 final plan on four weather years       027 DFM sensitivities (solar 30/20 W, stock 30 x 26 spar)
028 holding at the Lizard offing / Mount's Bay mouth (station-keeping and dead-boat drift)
029 Rev C5 scored boat-sim's way (one launch a day, 46 launches) for the #50 re-score
030 model fixes: storm winds in the loop (boat-sim #117) and knockdown severity
031 westbound sea states (fatigue input)    032 tropical-box weather for winters 2021-22 and 2022-23    033 those winters
Every run whose result file exists is skipped, so a batch can be restarted after a reboot.
"""
import json, os, sys, copy
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SIM = os.path.join(ROOT, "simulator")
sys.path.insert(0, os.path.join(ROOT, "collab", "east_west"))
import make_ew as EW

def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p

# ---------------------------------------------------------------- designs
E1 = jload("designs/revE1_design.json")
def variant(tag, note, fn):
    d = copy.deepcopy(E1); fn(d)
    d["name"] = f"Rev E1 study: {note}"; d["revision_note"] = f"{note} (study design, 21 Nov 2026; base Rev E1). " + E1["revision_note"]
    return jsave(d, f"designs/revE1_{tag}_study_design.json")
def solar(w):
    def f(d):
        d["power"]["solar_peak_w"] = float(w); d["power"]["panel_area_m2"] = round(0.235*w/40.0, 4)
    return f
variant("solar30", "30 W of solar instead of 40 W (smaller stock panels, DFM review item 1)", solar(30))
variant("solar20", "20 W of solar instead of 40 W (smaller stock panels, DFM review item 1)", solar(20))
variant("spar3026", "stock 30 x 26 carbon spar instead of 30 x 22 (DFM review item 2): wing-spar chance from the C2 strike table",
        lambda d: d["structure"].update(spar="C2"))

# ---------------------------------------------------------------- scenarios
PLAN = "collab/arrival/hatteras_stream__lizard_offing_hold_v2.json"
plan = jload(PLAN)
fix_both = jsave(dict(plan, name=plan["name"] + "; storm winds in the loop + knockdown severity",
                      storm_wind_correction=True, knockdown_severity=2.5), "collab/runs_026/plan_fix_both.json")
fix_storm = jsave(dict(plan, name=plan["name"] + "; storm winds in the loop", storm_wind_correction=True),
                  "collab/runs_026/plan_fix_storm.json")
fix_sev = jsave(dict(plan, name=plan["name"] + "; knockdown severity", knockdown_severity=2.5),
                "collab/runs_026/plan_fix_severity.json")

HOLDS = {"lizard": ("the Lizard offing", 49.85, -5.20), "mounts": ("the mouth of Mount's Bay", 49.97, -5.45)}
hold_sc = {}
for tag, (nm, la, lo) in HOLDS.items():
    base = dict(provider="bulk", failure_rate_set="planning", start={"lat": la, "lon": lo}, target={"lat": la, "lon": lo},
                waypoints=[], arrival_radius_km=0.0, europe_landfall_counts=False, atlantic_islands_count=False,
                watch_lines=plan["watch_lines"])
    hold_sc[f"station_{tag}"] = jsave(dict(base, name=f"Holding study: station-keeping at {nm}, 14 days (Rev E1)",
                                           initial_mode="station", station=[la, lo], max_days=14),
                                      f"collab/runs_026/hold_station_{tag}.json")
    hold_sc[f"drift_{tag}"] = jsave(dict(base, name=f"Holding study: dead boat drifting from {nm}, 30 days (Rev E1)",
                                         initial_mode="drift", failures_enabled=False, max_days=30),
                                    f"collab/runs_026/hold_drift_{tag}.json")

import datetime as dt
daily = [(dt.date(2023, 5, 1) + dt.timedelta(days=k)).isoformat() + "T12:00:00" for k in range(46)]
c5_theirs = jsave(dict(jload("collab/bulk_mc_2023_10km.json"), name="Rev C5 scored boat-sim's way: one launch a day 1 May-15 Jun 2023, "
                       "10 km off Ocean City, straight to 51.4N 10.0W (no waypoint)", target={"lat": 51.4, "lon": -10.0},
                       waypoints=[], start_times=daily), "collab/runs_026/c5_their_way.json")
c5_ours46 = jsave(dict(jload("collab/bulk_mc_2023_10km.json"), name="Rev C5, our 48.0% set-up (waypoint 42N 48W, target off Mizen Head) "
                       "on boat-sim's 46 daily launches", start_times=daily), "collab/runs_026/c5_ours_46.json")

# ---------------------------------------------------------------- batch files
PY = r".venv\Scripts\python.exe"
def bat(name, title, runs, note, minutes, ew=False):
    """runs: list of (label, design, scenario, n, frm, to, years, out, stormcheck csv or None)."""
    log = rf"..\collab\run_log_{name}.txt"
    L = ["@echo off", f"REM {title}", f"REM {note}", f"REM {len(runs)} runs, about {minutes//60} h {minutes%60:02d} min. Written by collab/runs_026/make_runs.py (21 Nov 2026).",
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

D = "designs/revE1_design.json"
Y4 = "2021,2022,2023,2024"
bat("026_final_plan", "Run 026: the final plan on four weather years (Hatteras 45 km to the Lizard offing, 1-20 May)",
    [("final plan, 1000 voyages", D, PLAN, 1000, "2023-05-01", "2023-05-20", Y4, "plan026_2021-2024_revE1_lizard_offing_v2", "")],
    "Rev E1, the decided route and holding point (run 025's scenario), launches 1-20 May 2021-2024. Storm check after.", 62)
bat("027_dfm_sensitivity", "Run 027: DFM sensitivities: smaller solar (30 W, 20 W) and the stock 30 x 26 spar",
    [(f"{lab}", f"designs/revE1_{lab}_study_design.json", PLAN, 500, "2023-05-01", "2023-06-15", "2023,2024",
      f"dfm027_2023+2024_revE1_{lab}_lizard_offing_v2", None) for lab in ("solar30", "solar20", "spar3026")],
    "Same launches and seeds as run 025 (Lizard offing v2, 500 voyages, 1 May-15 Jun 2023+2024), so differences are paired.", 95)
bat("028_holding", "Run 028: holding study: station-keeping and dead-boat drift at the Lizard offing and Mount's Bay mouth",
    [(lab, D, scen, 500, "2023-08-15", "2023-10-15", Y4, f"hold028_2021-2024_revE1_{lab}", None) for lab, scen in hold_sc.items()],
    "Boats start at the holding point, 15 Aug-15 Oct (when crossings arrive), 2021-2024: 14 days holding, or 30 days drifting dead.", 35)
bat("029_c5_their_way", "Run 029: Rev C5 on boat-sim's re-score set-up (46 daily launches, May-June 2023)",
    [("their way: no waypoint, 51.4N 10.0W", "designs/revC5_design.json", c5_theirs, 46, "2023-05-01", "2023-06-15", "2023", "c5_029_2023_their_way", None),
     ("our set-up on their 46 dates", "designs/revC5_design.json", c5_ours46, 46, "2023-05-01", "2023-06-15", "2023", "c5_029_2023_ours_46", None)],
    "Compares with their first re-score (3 of 46) and our 48.0% (250 random launches).", 12)
bat("030_model_fixes", "Run 030: model fixes on the final plan: storm winds in the loop (boat-sim #117) and knockdown severity",
    [("both fixes, 1000 voyages", D, fix_both, 1000, "2023-05-01", "2023-05-20", Y4, "fix030_2021-2024_revE1_both", ""),
     ("storm winds only, 500", D, fix_storm, 500, "2023-05-01", "2023-05-20", Y4, "fix030_2021-2024_revE1_storm", None),
     ("knockdown severity only, 500", D, fix_sev, 500, "2023-05-01", "2023-05-20", Y4, "fix030_2021-2024_revE1_severity", None)],
    "Same launches and seeds as run 026 (the 500-voyage runs pair with its first 500), so the effect of each fix is paired.", 125)

# 031: westbound sea states along the Mindelo -> BVI tracks (run 024a), for the fatigue check
L = ["@echo off", "REM Run 031: sea states along the westbound Mindelo -> BVI tracks (run 024a), for the fatigue check (docs/Fatigue_Review.md).",
     "REM About 10-20 minutes. Written by collab/runs_026/make_runs.py (21 Nov 2026).", 'cd /d "%~dp0"',
     "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", 'set DRONE_SIM_HOME=%~dp0workspace_ew',
     "echo ============================================================",
     "echo  Run 031: sea states along the westbound Mindelo -^> BVI tracks", "echo  Expected time: about 10-20 minutes. Started %date% %time%",
     "echo ============================================================",
     r"if exist ..\results\seastates_ew024_mindelo__bvi_s.json (echo   already finished, skipping) else (",
     rf"  {PY} ..\collab\seastates_along_tracks.py ..\results\ew024_2023+2024_mindelo__bvi_s.json ..\results\seastates_ew024_mindelo__bvi_s.json > ..\collab\run_log_031_seastates_ew.txt 2>&1",
     r"  type ..\collab\run_log_031_seastates_ew.txt", ")", "echo Finished %date% %time%"]
open(os.path.join(SIM, "run_031_seastates_ew.bat"), "w", newline="\r\n").write("\n".join(L) + "\n")
print("simulator/run_031_seastates_ew.bat")

# 032/033: two more tropical winters for the BVI backup
EW.download_bat("032_ew_download_2021_23", "Run 032: east-west weather for winters 2021-22 and 2022-23, tropical box",
                "2021-11..2022-06,2022-11..2023-06", 37, "roughly 1-3 days (ERA5 is 2-3 h a month at CDS)")
p = os.path.join(SIM, "run_032_ew_download_2021_23.bat"); s = open(p).read()
s = s.replace("Written by collab/east_west/make_ew.py. Approved by Randolph 13 Nov 2026", "Written by collab/runs_026/make_runs.py. Asked for by Randolph 21 Nov 2026")
s = s.replace('REM ("plan for an east to west crossing").', 'REM ("let\'s do all 7": item 6, a third and fourth winter for the BVI backup).')
open(p, "w", newline="").write(s)
TR = EW.TROPICS_CSV
bat("033_ew_two_more_winters", "Run 033: BVI backup on winters 2021-22 and 2022-23 (Mindelo, Gran Canaria south, El Hierro south)",
    [("mindelo__bvi_s", D, "collab/east_west/mindelo__bvi_s.json", 500, "2021-11-15", "2022-01-10", "2021,2022", "ew033_2021+2022_mindelo__bvi_s", TR),
     ("gran_canaria_south__bvi_s", D, "collab/east_west/gran_canaria_south__bvi_s.json", 500, "2021-11-01", "2021-12-20", "2021,2022", "ew033_2021+2022_gran_canaria_south__bvi_s", TR),
     ("el_hierro_south__bvi_s", D, "collab/east_west/el_hierro_south__bvi_s.json", 500, "2021-11-01", "2021-12-20", "2021,2022", "ew033_2021+2022_el_hierro_south__bvi_s", TR)],
    "Same set-up as run 024 (two winters) on two more; needs run 032's weather first. With 024 this gives four winters.", 95, ew=True)
