@echo off
REM Hatteras drop points that clear Diamond Shoals: Rev E to Cornwall (docs/Launch_Point_Study.md). Written by collab/launch_points/make_batch.py.
REM 3 runs of 500 voyages, weather 2023,2024, design revE_design.json. About 1 h 36 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  Hatteras drop points that clear Diamond Shoals: Rev E to Cornwall
echo  3 runs x 500 voyages. Expected time: about 1 h 36 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_launch_shoals.txt
echo Hatteras drop points that clear Diamond Shoals: Rev E to Cornwall, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 3: revE_hatteras_stream__cornwall   (started %time%)
if exist ..\results\plan_2023+2024_revE_hatteras_stream__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: revE_hatteras_stream__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: revE_hatteras_stream__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE_design.json --scenario ..\collab\launch_points\hatteras_stream__cornwall.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\plan_2023+2024_revE_hatteras_stream__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE_hatteras_stream__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan_2023+2024_revE_hatteras_stream__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE_hatteras_stream__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_shoals.txt)
)
echo.
echo RUN 2 of 3: revE_hatteras_east__cornwall   (started %time%)
if exist ..\results\plan_2023+2024_revE_hatteras_east__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: revE_hatteras_east__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: revE_hatteras_east__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE_design.json --scenario ..\collab\launch_points\hatteras_east__cornwall.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\plan_2023+2024_revE_hatteras_east__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE_hatteras_east__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan_2023+2024_revE_hatteras_east__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE_hatteras_east__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_shoals.txt)
)
echo.
echo RUN 3 of 3: revE_hatteras_dogleg__cornwall   (started %time%)
if exist ..\results\plan_2023+2024_revE_hatteras_dogleg__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: revE_hatteras_dogleg__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: revE_hatteras_dogleg__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE_design.json --scenario ..\collab\launch_points\hatteras_dogleg__cornwall.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\plan_2023+2024_revE_hatteras_dogleg__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE_hatteras_dogleg__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan_2023+2024_revE_hatteras_dogleg__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE_hatteras_dogleg__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_shoals.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\plan_2023+2024_*.json   Log: collab\run_log_launch_shoals.txt
echo ============================================================
pause
