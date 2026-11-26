@echo off
REM Run 037: Cornwall pickup points, holding, on the detailed coast (Lizard offing, Mount's Bay, two offshore spots)
REM Same window and seeds as runs 028/035; adds the accurate coast and two offshore candidates.
REM 8 runs, about 0 h 40 min. Written by collab/runs_036/make_runs.py (26 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_037_hold_cornwall.txt
echo ============================================================
echo  Run 037: Cornwall pickup points, holding, on the detailed coast (Lizard offing, Mount's Bay, two offshore spots)
echo  8 runs. Expected time: about 0 h 40 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 037: Cornwall pickup points, holding, on the detailed coast (Lizard offing, Mount's Bay, two offshore spots), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 8: station_lizard   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_station_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: station_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_station_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_station_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 2 of 8: drift_lizard   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_drift_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: drift_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_drift_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_drift_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 3 of 8: station_mounts   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_station_mounts.json (
  echo   already finished, skipping
  echo ==== RUN: station_mounts already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_mounts ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_mounts.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_station_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_mounts.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_station_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_mounts.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 4 of 8: drift_mounts   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_drift_mounts.json (
  echo   already finished, skipping
  echo ==== RUN: drift_mounts already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_mounts ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_mounts.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_drift_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_mounts.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_drift_mounts.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_mounts.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 5 of 8: station_lizard_deep   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_station_lizard_deep.json (
  echo   already finished, skipping
  echo ==== RUN: station_lizard_deep already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_lizard_deep ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_lizard_deep.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_station_lizard_deep.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_lizard_deep.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_station_lizard_deep.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_lizard_deep.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 6 of 8: drift_lizard_deep   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_drift_lizard_deep.json (
  echo   already finished, skipping
  echo ==== RUN: drift_lizard_deep already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_lizard_deep ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_lizard_deep.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_drift_lizard_deep.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_lizard_deep.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_drift_lizard_deep.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_lizard_deep.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 7 of 8: station_scilly_lizard   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_station_scilly_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: station_scilly_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_scilly_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_scilly_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_station_scilly_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_scilly_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_station_scilly_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_station_scilly_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo.
echo RUN 8 of 8: drift_scilly_lizard   (started !time!)
if exist ..\results\hold037_2021-2024_revE3_drift_scilly_lizard.json (
  echo   already finished, skipping
  echo ==== RUN: drift_scilly_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_scilly_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_scilly_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold037_2021-2024_revE3_drift_scilly_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_scilly_lizard.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold037_2021-2024_revE3_drift_scilly_lizard.json >> "%LOG%" 2>&1
  if exist ..\results\hold037_2021-2024_revE3_drift_scilly_lizard.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_037_hold_cornwall.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_037_hold_cornwall.txt
echo ============================================================
