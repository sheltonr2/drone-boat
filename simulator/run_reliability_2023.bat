@echo off
REM Reliability study (12 Nov 2026, docs/Reliability_Review.md): three 250-voyage runs against Rev D as drawn (62.0%).
REM 2023 weather, near-coast launch, same seeds as the Rev D run. About 4 hours. A run that has its result file is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  Reliability study: 3 runs x 250 voyages (about 4 hours)
echo  1 bilge pump   2 pump + servos + weed fin   3 weed downside check
echo  Progress shows below. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_reliability_2023.txt
echo Reliability study, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 3: Rev D + bilge pump and pump-and-sail leak response   (started !time!)
if exist ..\results\bulk_mc_2023_revD_pump_10km.json (
  echo   already finished, skipping
) else (
  echo ==== RUN: Rev D + bilge pump and pump-and-sail leak response ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_pump_study_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revD_pump_10km.json >> "%LOG%" 2>&1
  if exist ..\results\bulk_mc_2023_revD_pump_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revD_pump_10km.json >> "%LOG%" 2>&1
  if exist ..\results\bulk_mc_2023_revD_pump_10km.json (echo   finished !time!) else (echo   FAILED: see collab\run_log_reliability_2023.txt)
)
echo.
echo RUN 2 of 3: Rev D + pump + sealed brushless servos, tail detent, weed-shedding fin (guessed factors)   (started !time!)
if exist ..\results\bulk_mc_2023_revD_reliability_10km.json (
  echo   already finished, skipping
) else (
  echo ==== RUN: Rev D + pump + sealed brushless servos, tail detent, weed-shedding fin (guessed factors) ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_reliability_study_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revD_reliability_10km.json >> "%LOG%" 2>&1
  if exist ..\results\bulk_mc_2023_revD_reliability_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revD_reliability_10km.json >> "%LOG%" 2>&1
  if exist ..\results\bulk_mc_2023_revD_reliability_10km.json (echo   finished !time!) else (echo   FAILED: see collab\run_log_reliability_2023.txt)
)
echo.
echo RUN 3 of 3: Rev D as drawn but weed clears in a month, not a week (downside check)   (started !time!)
if exist ..\results\bulk_mc_2023_revD_weed_pessimistic_10km.json (
  echo   already finished, skipping
) else (
  echo ==== RUN: Rev D as drawn but weed clears in a month, not a week (downside check) ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_weed_pessimistic_study_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revD_weed_pessimistic_10km.json >> "%LOG%" 2>&1
  if exist ..\results\bulk_mc_2023_revD_weed_pessimistic_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revD_weed_pessimistic_10km.json >> "%LOG%" 2>&1
  if exist ..\results\bulk_mc_2023_revD_weed_pessimistic_10km.json (echo   finished !time!) else (echo   FAILED: see collab\run_log_reliability_2023.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\bulk_mc_2023_revD_*_10km.json   Log: collab\run_log_reliability_2023.txt
echo ============================================================
pause
