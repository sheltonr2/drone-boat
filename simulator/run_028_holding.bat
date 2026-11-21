@echo off
REM Run 028: holding study: station-keeping and dead-boat drift at the Lizard offing and Mount's Bay mouth
REM Boats start at the holding point, 15 Aug-15 Oct (when crossings arrive), 2021-2024: 14 days holding, or 30 days drifting dead.
REM 4 runs, about 0 h 35 min. Written by collab/runs_026/make_runs.py (21 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_028_holding.txt
echo ============================================================
echo  Run 028: holding study: station-keeping and dead-boat drift at the Lizard offing and Mount's Bay mouth
echo  4 runs. Expected time: about 0 h 35 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 028: holding study: station-keeping and dead-boat drift at the Lizard offing and Mount's Bay mouth, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 4: station_lizard   (started !time!)
if exist ..\results\hold028_2021-2024_revE1_station_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: station_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\hold_station_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold028_2021-2024_revE1_station_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_station_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold028_2021-2024_revE1_station_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_station_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_028_holding.txt)
)
echo.
echo RUN 2 of 4: drift_lizard   (started !time!)
if exist ..\results\hold028_2021-2024_revE1_drift_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: drift_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\hold_drift_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold028_2021-2024_revE1_drift_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_drift_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold028_2021-2024_revE1_drift_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_drift_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_028_holding.txt)
)
echo.
echo RUN 3 of 4: station_mounts   (started !time!)
if exist ..\results\hold028_2021-2024_revE1_station_mounts.json (
  echo   already finished, skipping
  echo ==== RUN: station_mounts already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_mounts ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\hold_station_mounts.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold028_2021-2024_revE1_station_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_station_mounts.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold028_2021-2024_revE1_station_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_station_mounts.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_028_holding.txt)
)
echo.
echo RUN 4 of 4: drift_mounts   (started !time!)
if exist ..\results\hold028_2021-2024_revE1_drift_mounts.json (
  echo   already finished, skipping
  echo ==== RUN: drift_mounts already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_mounts ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\hold_drift_mounts.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold028_2021-2024_revE1_drift_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_drift_mounts.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold028_2021-2024_revE1_drift_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold028_2021-2024_revE1_drift_mounts.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_028_holding.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_028_holding.txt
echo ============================================================
