"""Arrival behaviour (Randolph, 15 Nov 2026): on arrival the boat goes to a holding pattern somewhere safe but as close
to the coast as possible, for an easy pickup. docs/Launch_Plan.md "Arrival and holding".

    python collab/arrival/make_arrival.py     # writes collab/arrival/hatteras_stream__falmouth_hold.json and the batch

The simulator ends a voyage at the target; here the target is the holding point itself, with a 3 km arrival radius,
and approach waypoints keep the boat south of the Isles of Scilly, Wolf Rock and the Lizard and east of the Manacles.
A landfall anywhere in Europe still scores as an arrival; the analysis separates boats that reached the holding point.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
base = json.load(open(os.path.join(ROOT, "collab", "launch_points", "hatteras_stream__cornwall.json")))
HOLD = (50.100, -4.990)   # Falmouth Bay, about 5 km SE of Pendennis Point and 5 km E of Rosemullion Head, 20-30 m
APPROACH = [[49.820, -6.600],   # 7 km SW of Bishop Rock (49.873 N 6.446 W)
            [49.830, -5.800],   # 13 km S of Wolf Rock (49.945 N 5.808 W)
            [49.850, -5.200],   # 12 km S of the Lizard (49.957 N 5.206 W)
            [50.020, -4.900]]   # 10 km E of the Manacles (50.045 N 5.040 W)
WATCH = {"seven_stones": [[50.060, -6.072], [50.055, -6.130]],
         "scilly": [[49.873, -6.446], [49.965, -6.400], [49.980, -6.320], [49.965, -6.255],
                    [49.900, -6.270], [49.880, -6.350], [49.873, -6.446]],
         "wolf_rock": [[49.945, -5.812], [49.945, -5.804]],
         "runnelstone": [[50.020, -5.672], [50.025, -5.665]],
         "manacles": [[50.040, -5.050], [50.050, -5.035]],
         "lizard_point": [[49.957, -5.215], [49.955, -5.195]]}
MOUNTS = (50.050, -5.480)   # Mount's Bay, about 6 km SE of Penzance, 5 km off St Michael's Mount, 30-40 m
APPROACH_MB = [[49.820, -6.600],   # 7 km SW of Bishop Rock
               [49.860, -5.800]]   # 9 km S of Wolf Rock, then NE into the bay, 9 km clear of the Runnelstone
WATCH["low_lee_mountamopus"] = [[50.090, -5.520], [50.085, -5.470]]
SCEN = {"falmouth_hold": ("Falmouth Bay", HOLD, APPROACH),
        "mounts_bay_hold": ("Mount's Bay", MOUNTS, APPROACH_MB)}
runs = []
for tag, (nm, pt, app) in SCEN.items():
    sc = dict(base, name=f"Arrival study: Hatteras 45 km -> holding point in {nm} (Rev E1)",
              target={"lat": pt[0], "lon": pt[1]}, arrival_radius_km=3.0,
              waypoints=base["waypoints"] + app, watch_lines=WATCH)
    json.dump(sc, open(os.path.join(HERE, f"hatteras_stream__{tag}.json"), "w"), indent=1)
    runs.append(tag)
log = r"..\collab\run_log_arrival.txt"
L = ["@echo off",
     "REM Arrival study (docs/Launch_Plan.md \"Arrival and holding\"): Rev E1, 45 km off Hatteras -> a holding point,",
     "REM Falmouth Bay and Mount's Bay, 500 voyages each, 2023+2024, the same launch dates and seeds as run 017.",
     "REM About 80 min. A run whose result exists is skipped. Written by collab/arrival/make_arrival.py.",
     'cd /d "%~dp0"', "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}",
     "echo ============================================================",
     "echo  Arrival study: Hatteras to holding points in Falmouth Bay and Mount's Bay",
     "echo  2 runs x 500 voyages, about 80 minutes. Started %date% %time%",
     "echo ============================================================",
     'echo Arrival study, started %date% %time% >> "%LOG%"']
for k, tag in enumerate(runs, 1):
    out = rf"..\results\arrival_2023+2024_revE1_hatteras_stream__{tag}.json"
    L += ["echo.", f"echo RUN {k} of {len(runs)}: {tag}   (started %time%)", f"if exist {out} (", "  echo   already finished, skipping", ") else (",
          f'  echo ==== RUN: {tag} ==== >> "%LOG%"',
          rf'  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\arrival\hatteras_stream__{tag}.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out {out} >> "%LOG%" 2>&1',
          rf'  if exist {out} .venv\Scripts\python.exe ..\collab\summarize_mc.py {out} >> "%LOG%" 2>&1',
          f"  if exist {out} (echo   finished %time%) else (echo   FAILED: see {log})", ")"]
L += ['echo === DONE %date% %time% >> "%LOG%"', "echo  ALL DONE %date% %time%"]
open(os.path.join(ROOT, "simulator", "run_arrival.bat"), "w", newline="\r\n").write("\n".join(L) + "\n")
print("ok", runs)
