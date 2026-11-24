@echo off
REM Run 035: holding study 2: station-keeping within 1 km at the Lizard offing and Mount's Bay mouth
REM Same seeds as run 028's station runs; only the station deadband changes (5 km to 1 km).
REM 2 runs, about 0 h 20 min. Written by collab/runs_034/make_runs.py (24 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_035_holding_1km.txt
echo ============================================================
echo  Run 035: holding study 2: station-keeping within 1 km at the Lizard offing and Mount's Bay mouth
echo  2 runs. Expected time: about 0 h 20 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 035: holding study 2: station-keeping within 1 km at the Lizard offing and Mount's Bay mouth, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 2: station1km_lizard   (started !time!)
if exist ..\results\hold035_2021-2024_revE1_station1km_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: station1km_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station1km_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_034\hold_station1km_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold035_2021-2024_revE1_station1km_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold035_2021-2024_revE1_station1km_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold035_2021-2024_revE1_station1km_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold035_2021-2024_revE1_station1km_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_035_holding_1km.txt)
)
echo.
echo RUN 2 of 2: station1km_mounts   (started !time!)
if exist ..\results\hold035_2021-2024_revE1_station1km_mounts.json (
  echo   already finished, skipping
  echo ==== RUN: station1km_mounts already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station1km_mounts ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_034\hold_station1km_mounts.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold035_2021-2024_revE1_station1km_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold035_2021-2024_revE1_station1km_mounts.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold035_2021-2024_revE1_station1km_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold035_2021-2024_revE1_station1km_mounts.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_035_holding_1km.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_035_holding_1km.txt
echo ============================================================
