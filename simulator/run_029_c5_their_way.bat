@echo off
REM Run 029: Rev C5 on boat-sim's re-score set-up (46 daily launches, May-June 2023)
REM Compares with their first re-score (3 of 46) and our 48.0% (250 random launches).
REM 2 runs, about 0 h 12 min. Written by collab/runs_026/make_runs.py (21 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_029_c5_their_way.txt
echo ============================================================
echo  Run 029: Rev C5 on boat-sim's re-score set-up (46 daily launches, May-June 2023)
echo  2 runs. Expected time: about 0 h 12 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 029: Rev C5 on boat-sim's re-score set-up (46 daily launches, May-June 2023), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 2: their way: no waypoint, 51.4N 10.0W   (started !time!)
if exist ..\results\c5_029_2023_their_way.json (
  echo   already finished, skipping
  echo ==== RUN: their way: no waypoint, 51.4N 10.0W already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: their way: no waypoint, 51.4N 10.0W ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\runs_026\c5_their_way.json --runs 46 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\c5_029_2023_their_way.json >> "%LOG%" 2>&1
  if exist ..\results\c5_029_2023_their_way.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\c5_029_2023_their_way.json >> "%LOG%" 2>&1
  if exist ..\results\c5_029_2023_their_way.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_029_c5_their_way.txt)
)
echo.
echo RUN 2 of 2: our set-up on their 46 dates   (started !time!)
if exist ..\results\c5_029_2023_ours_46.json (
  echo   already finished, skipping
  echo ==== RUN: our set-up on their 46 dates already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: our set-up on their 46 dates ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\runs_026\c5_ours_46.json --runs 46 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\c5_029_2023_ours_46.json >> "%LOG%" 2>&1
  if exist ..\results\c5_029_2023_ours_46.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\c5_029_2023_ours_46.json >> "%LOG%" 2>&1
  if exist ..\results\c5_029_2023_ours_46.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_029_c5_their_way.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_029_c5_their_way.txt
echo ============================================================
