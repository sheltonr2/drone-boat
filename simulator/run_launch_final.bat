@echo off
REM Launch study stage C: final check on Rev D, 2023 and 2024 weather (docs/Launch_Point_Study.md). Written by collab/launch_points/make_batch.py.
REM 3 runs of 500 voyages, weather 2023,2024, design revD_design.json. About 1 h 36 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  Launch study stage C: final check on Rev D, 2023 and 2024 weather
echo  3 runs x 500 voyages. Expected time: about 1 h 36 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_launch_final.txt
echo Launch study stage C: final check on Rev D, 2023 and 2024 weather, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 3: hatteras__ireland_sw   (started %time%)
if exist ..\results\launch_2023+2024_hatteras__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_design.json --scenario ..\collab\launch_points\hatteras__ireland_sw.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\launch_2023+2024_hatteras__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023+2024_hatteras__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023+2024_hatteras__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023+2024_hatteras__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_final.txt)
)
echo.
echo RUN 2 of 3: hatteras__cornwall   (started %time%)
if exist ..\results\launch_2023+2024_hatteras__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_design.json --scenario ..\collab\launch_points\hatteras__cornwall.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\launch_2023+2024_hatteras__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023+2024_hatteras__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023+2024_hatteras__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023+2024_hatteras__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_final.txt)
)
echo.
echo RUN 3 of 3: ocean_city__ireland_sw   (started %time%)
if exist ..\results\launch_2023+2024_ocean_city__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_design.json --scenario ..\collab\launch_points\ocean_city__ireland_sw.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\launch_2023+2024_ocean_city__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023+2024_ocean_city__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023+2024_ocean_city__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023+2024_ocean_city__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_final.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\launch_2023+2024_*.json   Log: collab\run_log_launch_final.txt
echo ============================================================
pause
