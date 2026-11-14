@echo off
REM Rev E1 from 45 km off Hatteras to Cornwall (new plan baseline) (docs/Launch_Point_Study.md). Written by collab/launch_points/make_batch.py.
REM 1 runs of 500 voyages, weather 2023,2024, design revE1_design.json. About 0 h 32 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  Rev E1 from 45 km off Hatteras to Cornwall (new plan baseline)
echo  1 runs x 500 voyages. Expected time: about 0 h 32 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_plan_E1.txt
echo Rev E1 from 45 km off Hatteras to Cornwall (new plan baseline), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 1: revE1_hatteras_stream__cornwall   (started %time%)
if exist ..\results\plan_2023+2024_revE1_hatteras_stream__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: revE1_hatteras_stream__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: revE1_hatteras_stream__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\launch_points\hatteras_stream__cornwall.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\plan_2023+2024_revE1_hatteras_stream__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE1_hatteras_stream__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan_2023+2024_revE1_hatteras_stream__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\plan_2023+2024_revE1_hatteras_stream__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_plan_E1.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\plan_2023+2024_*.json   Log: collab\run_log_plan_E1.txt
echo ============================================================
pause
