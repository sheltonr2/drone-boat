"""East-to-west study (docs/East_West_Study.md): scenario files and Windows batch files.

    python collab/east_west/make_ew.py            # writes collab/east_west/*.json and simulator/run_ew_*.bat

Westbound runs use "far_side": "americas" (a landfall anywhere in the Americas counts; Bermuda, the Canaries,
Madeira and Cape Verde don't) and their own weather cache (DRONE_SIM_HOME=simulator\\workspace_ew), because the
trade-wind route needs a tropical box (5-40N, 80W-5W) and winter months that the eastbound cache doesn't hold.
The northern-route check (Cornwall to New England) uses the eastbound cache, which already covers it.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from places import LAUNCH, DEST                                             # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
MIN_PER_150 = 9          # minutes per 150 voyages on Randolph's PC (eastbound, faster code)
TROPICS_CSV = r"..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv"
BOX = "5,40,-80,-5"

# Great Atlantic Sargassum Belt (docs/East_West_Study.md section 4): a GUESSED multiplier on the weed/line fouling
# rate inside the belt, by month (belt biomass peaks in June-July, lowest in winter). The eastbound default doubles the
# rate in the Sargasso Sea; that zone is kept as it was.
SARGASSO = dict(lat=[20.0, 35.0], lon=[-70.0, -40.0], factor=2.0)
BELT = dict(lat=[3.0, 22.0], lon=[-65.0, -15.0],
            factor_by_month={"12": 2, "1": 2, "2": 2, "3": 3, "4": 3, "5": 4, "6": 5, "7": 5, "8": 4, "9": 3, "10": 3, "11": 2})
BELT_PESS = dict(BELT, factor_by_month={k: 2*v for k, v in BELT["factor_by_month"].items()})

# Waypoints (abeam rule: passed once the boat is beyond them along the leg)
WEST_OF_CANARIES = [28.5, -20.0]     # mainland and Madeira starts: pass west of La Palma and El Hierro
SOUTH_ROUTE = [20.0, -28.0]          # the sailors' route: south "till the butter melts", then west in steadier trades


def scenario(launch, dest, waypoints=(), weed=BELT, tag=None):
    L, D = LAUNCH[launch], DEST[dest]
    wp = [list(w) for w in waypoints]
    name = f"East-west study: {L['name']} to {D['name']}" + (f" ({tag})" if tag else "")
    sc = {"name": name, "provider": "bulk", "start": {"lat": L["drop"][0], "lon": L["drop"][1]},
          "target": {"lat": D["target"][0], "lon": D["target"][1]}, "waypoints": wp, "waypoint_rule": "abeam",
          "failure_rate_set": "planning", "far_side": "americas", "atlantic_islands_count": False,
          "africa_landfall_counts": False}
    if weed is not None:
        sc["weed_zones"] = [SARGASSO, weed]
    return sc


# label -> (launch, dest, waypoints, weed, note)
RUNS = {
    "gran_canaria__barbados":       ("gran_canaria", "barbados", [], BELT, "the reference pair (Oshen PC13's route)"),
    "gran_canaria_south__barbados": ("gran_canaria", "barbados", [SOUTH_ROUTE], BELT, "south to 20N 28W first"),
    "gran_canaria__st_lucia":       ("gran_canaria", "st_lucia", [], BELT, "the ARC finish"),
    "gran_canaria__martinique":     ("gran_canaria", "martinique", [], BELT, "France: an EU landfall"),
    "gran_canaria__antigua":        ("gran_canaria", "antigua", [], BELT, "north end of the island chain"),
    "gran_canaria__puerto_rico":    ("gran_canaria", "puerto_rico", [], BELT, "a US landfall"),
    "el_hierro__barbados":          ("el_hierro", "barbados", [], BELT, "westernmost Canary, 230 km shorter"),
    "mindelo__barbados":            ("mindelo", "barbados", [], BELT, "Cape Verde, 1,100 km shorter"),
    "madeira__barbados":            ("madeira", "barbados", [WEST_OF_CANARIES], BELT, "Portuguese island, EU"),
    "cadiz__barbados":              ("cadiz", "barbados", [WEST_OF_CANARIES], BELT, "mainland Spain"),
    "lisbon__barbados":             ("lisbon", "barbados", [WEST_OF_CANARIES], BELT, "mainland Portugal"),
    "gran_canaria__barbados_weedx2": ("gran_canaria", "barbados", [], BELT_PESS, "weed rate in the belt doubled"),
    "cornwall__new_england":        ("cornwall", "new_england", [[45.0, -35.0]], None, "northern route against the westerlies"),
}


def bat(name, title, runs, design, window, years, n, ew_cache=True, prefix="ew", stormcheck=True):
    tag = years.replace(",", "+"); log = f"..\\collab\\run_log_{name}.txt"
    mins = MIN_PER_150*len(runs)*n//150 + 2*len(runs)
    L = ["@echo off",
         f"REM {title} (docs/East_West_Study.md). Written by collab/east_west/make_ew.py.",
         f"REM {len(runs)} runs of {n} voyages, launches {window[0]} to {window[1]}, weather seasons from {years}, "
         f"design {design}. About {mins//60} h {mins%60:02d} min.",
         "REM A run that already has its result file is skipped, so this file can be restarted after a reboot.",
         "setlocal EnableDelayedExpansion", 'cd /d "%~dp0"',
         "echo ============================================================", f"echo  {title}",
         f"echo  {len(runs)} runs x {n} voyages. Expected time: about {mins//60} h {mins%60:02d} min.",
         "echo  Progress shows below, one line per run. Started %date% %time%",
         "echo ============================================================",
         "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}"]
    if ew_cache:
        L += ["REM Westbound weather (tropical box, winter months) lives in its own cache.",
              'set DRONE_SIM_HOME=%~dp0workspace_ew',
              'if not exist workspace_ew\\cache mkdir workspace_ew\\cache',
              'for %%f in (workspace\\cache\\*.*) do if not exist "workspace_ew\\cache\\%%~nxf" copy /y "%%f" "workspace_ew\\cache\\" >nul']
    L += [f'echo {title}, started %date% %time% >> "%LOG%"']
    for i, lab in enumerate(runs, 1):
        out = f"..\\results\\{prefix}_{tag}_{lab}.json"
        L += ["echo.", f"echo RUN {i} of {len(runs)}: {lab}   (started %time%)",
              f"if exist {out} (",
              "  echo   already finished, skipping",
              f'  echo ==== RUN: {lab} already finished, skipped ==== >> "%LOG%"',
              ") else (",
              f'  echo ==== RUN: {lab} ==== >> "%LOG%"',
              f'  .venv\\Scripts\\python.exe -m drone_sim.cli mc --design ..\\designs\\{design} --scenario ..\\collab\\east_west\\{lab}.json '
              f'--runs {n} --from {window[0]} --to {window[1]} --years {years} --out {out} >> "%LOG%" 2>&1',
              f'  if exist {out} .venv\\Scripts\\python.exe ..\\collab\\summarize_mc.py {out} >> "%LOG%" 2>&1']
        if stormcheck:
            csv = f" --storm-csv {TROPICS_CSV}" if ew_cache else ""
            L += [f'  if exist {out} .venv\\Scripts\\python.exe -m drone_sim.cli stormcheck --mc {out}{csv} '
                  f'--out {out[:-5]}_storms.json >> "%LOG%" 2>&1']
        L += [f"  if exist {out} (echo   finished !time!) else (echo   FAILED: see {log})", ")"]
    L += ['echo === DONE %date% %time% >> "%LOG%"', "echo.",
          "echo ============================================================", "echo  ALL DONE %date% %time%",
          f"echo  Results: results\\{prefix}_{tag}_*.json   Log: {log[3:]}",
          "echo ============================================================", "pause"]
    p = os.path.join(ROOT, "simulator", f"run_{name}.bat")
    open(p, "w", newline="\r\n").write("\n".join(L) + "\n")
    print(f"simulator/run_{name}.bat: {len(runs)} runs, about {mins} min")


def download_bat(name, title, months, gb, hours):
    log = f"..\\collab\\run_log_{name}.txt"
    L = ["@echo off",
         f"REM {title} (docs/East_West_Study.md). Written by collab/east_west/make_ew.py. Approved by Randolph 13 Nov 2026",
         "REM (\"plan for an east to west crossing\").",
         f"REM ERA5 winds (CDS) and Copernicus Marine currents and waves, tropical box {BOX} (lat0,lat1,lon0,lon1), months {months}.",
         f"REM About {gb} GB on disk and {hours}. Stored in simulator\\workspace_ew, apart from the eastbound data.",
         "REM It resumes where it stopped: queue it again and months already stored are skipped.",
         'cd /d "%~dp0"', "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}",
         'set DRONE_SIM_HOME=%~dp0workspace_ew',
         'if not exist workspace_ew\\cache mkdir workspace_ew\\cache',
         'for %%f in (workspace\\cache\\*.*) do if not exist "workspace_ew\\cache\\%%~nxf" copy /y "%%f" "workspace_ew\\cache\\" >nul',
         "echo ============================================================",
         f"echo  {title}", f"echo  About {gb} GB, {hours}. It resumes if stopped. Started %date% %time%",
         "echo ============================================================",
         f'echo {title}, started %date% %time% >> "%LOG%"',
         'if not exist .venv-bulk\\Scripts\\python.exe (',
         '  echo .venv-bulk is missing: run setup_bulk_data.bat first. >> "%LOG%"',
         "  echo .venv-bulk is missing: run setup_bulk_data.bat first.", "  exit /b 1", ")",
         f'powershell -NoProfile -Command "exit [int](((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB) -lt {gb + 30})" >nul 2>&1',
         "if errorlevel 1 (",
         f'  echo Not enough free disk space ^(need {gb + 30} GB^) >> "%LOG%"',
         f"  echo Not enough free disk space ^(need {gb + 30} GB^): see %LOG%", "  exit /b 1", ")",
         'powershell -NoProfile -Command "\'Free space before: {0:N0} GB\' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"',
         "REM Storm tracks for the tropics (NOAA HURDAT2), once: used by the storm-encounter check after each run.",
         f'if not exist {TROPICS_CSV} .venv-bulk\\Scripts\\python.exe ..\\docs\\data\\make_hurdat_subset.py >> "%LOG%" 2>&1',
         "echo Downloading. Each line below is one source-month; the full log is %LOG%",
         f'.venv-bulk\\Scripts\\python.exe -m drone_sim.cli download --box {BOX} --months {months} >> "%LOG%" 2>&1',
         'powershell -NoProfile -Command "\'Free space after: {0:N0} GB\' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"',
         'echo === DONE %date% %time% >> "%LOG%"',
         'type "%LOG%" | findstr /c:"already stored" /c:"stored" /c:"failed" /c:"Wrote" /c:"DONE"',
         "echo Finished %date% %time%"]
    p = os.path.join(ROOT, "simulator", f"run_{name}.bat")
    open(p, "w", newline="\r\n").write("\n".join(L) + "\n")
    print(f"simulator/run_{name}.bat: download {months}")


def main():
    for lab, (l, d, wp, weed, note) in RUNS.items():
        sc = scenario(l, d, wp, weed, None if not lab.endswith("weedx2") else "weed in the belt x2")
        sc["note"] = note
        json.dump(sc, open(os.path.join(HERE, lab + ".json"), "w"), indent=1)
    # 020: the northern route the other way, on the eastbound weather already downloaded
    bat("ew_northern", "East-west study: northern route, Cornwall to New England, May-June launches",
        ["cornwall__new_england"], "revE1_design.json", ("2023-05-15", "2023-06-30"), "2023,2024", 300, ew_cache=False)
    # 021: tropical-box weather for the winter 2024-25 season (launches Nov-Feb need Nov-Jul)
    download_bat("ew_download_2024_25", "East-west weather: Nov 2024 to Jul 2025, tropical box", "2024-11..2025-07", 22,
                 "roughly 6-15 hours")
    # 022: screen launch points and destinations on that season
    screen = [k for k in RUNS if k not in ("cornwall__new_england",)]
    bat("ew_screen", "East-west screen: 6 launch points, 6 destinations, launches 20 Nov to 10 Feb, 2024-25 weather",
        screen, "revE1_design.json", ("2024-11-20", "2025-02-10"), "2024", 300)
    # 023: the second winter season, plus the summer months a May launch (Oshen's timing) needs
    download_bat("ew_download_more", "East-west weather: Nov 2023 to Oct 2024 and Aug-Oct 2025, tropical box",
                 "2023-11..2024-10,2025-08..2025-10", 33, "roughly 12-24 hours")


if __name__ == "__main__":
    main()
