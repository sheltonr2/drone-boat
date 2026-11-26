"""Runs 036-039 (26 Nov 2026), asked for by Randolph: "Set it up and run it, be sure the simulator's coastline is
accurate. Test multiple pickup points ... Also consider something near Jost Van Dyke and off Anegada. Run all the
simulations you have to get good numbers. You are planning this mission, what else do we need to run too?"

Every run uses the new detailed coastlines (scenario key "detail_coast", docs/data/coast/): OpenStreetMap shorelines
(every islet and cay) plus NOAA ENC charted hazards (drying and sub-1.8 m areas, rocks, obstructions, wrecks) in the
Virgin Islands and off Hatteras, and OpenStreetMap shorelines for west Cornwall and Scilly. Design: Rev E3.

036 BVI pickup points, holding: 7 candidates x (14 days station-keeping within 1 km, failures on; 30 days dead-boat
    drift), 500 voyages each, Feb-Apr 2022-2025 (when westbound boats arrive).
037 Cornwall pickup points, holding, redone on the accurate coast: Lizard offing, Mount's Bay mouth and two new
    offshore spots (30 km south of the Lizard; between Scilly and the Lizard), same set-up as 035/028, Aug-Oct 2021-2024.
038 BVI pickup points, the crossing: Mindelo -> each of the 7 candidates, 1000 voyages over four winters
    (2021-22 to 2024-25), launches 15 Nov-10 Jan, with the approach route each needs.
039 The eastbound final plan on the accurate coasts at both ends (Hatteras and Cornwall), Rev E3, paired with 026/034.
Run from the repo root: python collab/runs_036/make_runs.py
"""
import json, os, sys, copy
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(ROOT, "simulator")
sys.path.insert(0, os.path.join(ROOT, "collab", "east_west"))
import make_ew as EW
def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p

E3 = "designs/revE3_design.json"
CARIB = "docs/data/coast/detail_carib.json"
CORN = "docs/data/coast/detail_cornwall.json"
HATT = "docs/data/coast/detail_hatteras.json"
OUT = "collab/runs_036"

# ---------------------------------------------------------------- BVI candidates
BVI = {   # tag: (name, (lat, lon), approach waypoints from the east)
    "norman":         ("4 km south of Norman and Peter Islands (the current plan)", (18.300, -64.580), [[18.20, -63.90], [18.18, -64.45]]),
    "norman_offing":  ("18 km south of Norman Island, open Caribbean", (18.170, -64.580), [[18.15, -63.90]]),
    "ginger_se":      ("south-east of Ginger and Cooper Islands, upwind end of the chain", (18.330, -64.430), [[18.25, -63.90]]),
    "jvd_north":      ("4 km north of Jost Van Dyke, Atlantic side", (18.490, -64.750), [[18.95, -63.90], [18.85, -64.40]]),
    "anegada_west":   ("8 km west of Anegada's West End, clear of Horseshoe Reef", (18.720, -64.490), [[18.95, -63.90], [18.85, -64.40]]),
    "anegada_north":  ("9 km north of Anegada, Atlantic side", (18.820, -64.330), [[18.95, -63.90]]),
    "stcroix_north":  ("9 km north of Christiansted, St Croix (USVI)", (17.850, -64.750), [[17.87, -63.90]]),
}
base_ew = jload("collab/east_west/mindelo__bvi_s.json")
WATCH_BVI = base_ew["watch_lines"]
cross_sc, hold_bvi = {}, {}
for tag, (nm, (la, lo), wps) in BVI.items():
    sc = copy.deepcopy(base_ew)
    sc.update(name=f"BVI pickup study: Mindelo -> {nm} (Rev E3, detailed coast)", target={"lat": la, "lon": lo}, waypoints=wps,
              detail_coast=CARIB, note="run 038: BVI pickup points (26 Nov 2026)")
    cross_sc[tag] = jsave(sc, f"{OUT}/ew_mindelo__{tag}.json")
    hb = dict(provider="bulk", failure_rate_set="planning", start={"lat": la, "lon": lo}, target={"lat": la, "lon": lo},
              waypoints=[], arrival_radius_km=0.0, europe_landfall_counts=False, atlantic_islands_count=False,
              far_side="americas", watch_lines=WATCH_BVI, weed_zones=base_ew["weed_zones"], detail_coast=CARIB)
    hold_bvi[f"station_{tag}"] = jsave(dict(hb, name=f"BVI holding: station-keeping within 1 km, {nm}, 14 days (Rev E3)",
                                            initial_mode="station", station=[la, lo], station_radius_km=1.0, max_days=14),
                                       f"{OUT}/hold_station_{tag}.json")
    hold_bvi[f"drift_{tag}"] = jsave(dict(hb, name=f"BVI holding: dead boat drifting from {nm}, 30 days (Rev E3)",
                                          initial_mode="drift", failures_enabled=False, max_days=30),
                                     f"{OUT}/hold_drift_{tag}.json")

# ---------------------------------------------------------------- Cornwall candidates
plan = jload("collab/arrival/hatteras_stream__lizard_offing_hold_v2.json")
CORN_PTS = {"lizard": ("the Lizard offing (the current plan)", 49.85, -5.20),
            "mounts": ("the mouth of Mount's Bay", 49.97, -5.45),
            "lizard_deep": ("30 km south of the Lizard", 49.70, -5.20),
            "scilly_lizard": ("between Scilly and the Lizard, 25 km south-west of Land's End", 49.85, -5.75)}
hold_corn = {}
for tag, (nm, la, lo) in CORN_PTS.items():
    hb = dict(provider="bulk", failure_rate_set="planning", start={"lat": la, "lon": lo}, target={"lat": la, "lon": lo},
              waypoints=[], arrival_radius_km=0.0, europe_landfall_counts=False, atlantic_islands_count=False,
              watch_lines=plan["watch_lines"], detail_coast=CORN)
    hold_corn[f"station_{tag}"] = jsave(dict(hb, name=f"Cornwall holding: station-keeping within 1 km at {nm}, 14 days (Rev E3, detailed coast)",
                                             initial_mode="station", station=[la, lo], station_radius_km=1.0, max_days=14),
                                        f"{OUT}/hold_station_{tag}.json")
    hold_corn[f"drift_{tag}"] = jsave(dict(hb, name=f"Cornwall holding: dead boat drifting from {nm}, 30 days (Rev E3, detailed coast)",
                                           initial_mode="drift", failures_enabled=False, max_days=30),
                                      f"{OUT}/hold_drift_{tag}.json")

plan_detail = jsave(dict(plan, name=plan["name"].replace("(Rev E1)", "") + " - detailed coast at Hatteras and Cornwall (Rev E3)",
                         detail_coast=[HATT, CORN]), f"{OUT}/plan_detail_coast.json")

PY = r".venv\Scripts\python.exe"
def bat(name, title, runs, note, minutes, ew=False):
    """runs: list of (label, design, scenario, n, frm, to, years, out, stormcheck csv or None)."""
    log = rf"..\collab\run_log_{name}.txt"
    L = ["@echo off", f"REM {title}", f"REM {note}", f"REM {len(runs)} runs, about {minutes//60} h {minutes%60:02d} min. Written by collab/runs_036/make_runs.py (26 Nov 2026).",
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


Y4 = "2021,2022,2023,2024"
Y4W = "2022,2023,2024,2025"
TR = EW.TROPICS_CSV
bat("036_hold_bvi", "Run 036: BVI pickup points, holding: station-keeping and dead-boat drift at 7 candidates (detailed coast)",
    [(lab, E3, scen, 500, "2022-02-01", "2022-04-30", Y4W, f"hold036_2022-2025_revE3_{lab}", None) for lab, scen in hold_bvi.items()],
    "Boats start at each candidate between 1 Feb and 30 Apr, 2022-2025: 14 days holding within 1 km, or 30 days drifting dead.", 70, ew=True)
bat("037_hold_cornwall", "Run 037: Cornwall pickup points, holding, on the detailed coast (Lizard offing, Mount's Bay, two offshore spots)",
    [(lab, E3, scen, 500, "2023-08-15", "2023-10-15", Y4, f"hold037_2021-2024_revE3_{lab}", None) for lab, scen in hold_corn.items()],
    "Same window and seeds as runs 028/035; adds the accurate coast and two offshore candidates.", 40)
bat("038_ew_pickups", "Run 038: BVI pickup points, the crossing: Mindelo -> 7 candidates over four winters (detailed coast)",
    [(tag, E3, scen, 1000, "2021-11-15", "2022-01-10", Y4, f"ew038_2021-2024_revE3_mindelo__{tag}", TR) for tag, scen in cross_sc.items()],
    "Rev E3, launches 15 Nov-10 Jan of winters 2021-22 to 2024-25, the same seeds for every candidate. Storm check after each.", 360, ew=True)
bat("039_plan_detail", "Run 039: the eastbound final plan on the detailed coasts at Hatteras and Cornwall (Rev E3)",
    [("final plan, detailed coast, 1000 voyages", E3, plan_detail, 1000, "2023-05-01", "2023-05-20", Y4, "plan039_2021-2024_revE3_lizard_offing_detail", "")],
    "Same launches and seeds as runs 026 (Rev E1) and 034 (Rev E3), so the coastline's effect is paired.", 62)
