@echo off
REM East-west study: northern route, Cornwall to New England, May-June launches (docs/East_West_Study.md). Written by collab/east_west/make_ew.py.
REM 1 runs of 300 voyages, launches 2023-05-15 to 2023-06-30, weather seasons from 2023,2024, design revE1_design.json. About 0 h 20 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  East-west study: northern route, Cornwall to New England, May-June launches
echo  1 runs x 300 voyages. Expected time: about 0 h 20 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_ew_northern.txt
echo East-west study: northern route, Cornwall to New England, May-June launches, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 1: cornwall__new_england   (started %time%)
if exist ..\results\ew_2023+2024_cornwall__new_england.json (
  echo   already finished, skipping
  echo ==== RUN: cornwall__new_england already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: cornwall__new_england ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\cornwall__new_england.json --runs 300 --from 2023-05-15 --to 2023-06-30 --years 2023,2024 --out ..\results\ew_2023+2024_cornwall__new_england.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2023+2024_cornwall__new_england.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2023+2024_cornwall__new_england.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2023+2024_cornwall__new_england.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2023+2024_cornwall__new_england.json --out ..\results\ew_2023+2024_cornwall__new_england_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2023+2024_cornwall__new_england.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_northern.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\ew_2023+2024_*.json   Log: collab\run_log_ew_northern.txt
echo ============================================================
pause
