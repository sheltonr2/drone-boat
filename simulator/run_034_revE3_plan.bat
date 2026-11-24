@echo off
REM Run 034: Rev E3 (20 W stock solar) on the final plan, four weather years
REM Same scenario, launches and seeds as run 026 (Rev E1), so the difference is paired. Storm check after.
REM 1 runs, about 1 h 02 min. Written by collab/runs_034/make_runs.py (24 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_034_revE3_plan.txt
echo ============================================================
echo  Run 034: Rev E3 (20 W stock solar) on the final plan, four weather years
echo  1 runs. Expected time: about 1 h 02 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 034: Rev E3 (20 W stock solar) on the final plan, four weather years, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 1: Rev E3, 1000 voyages   (started !time!)
if exist ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Rev E3, 1000 voyages already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Rev E3, 1000 voyages ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\arrival\hatteras_stream__lizard_offing_hold_v2.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json --out ..\results\plan034_2021-2024_revE3_lizard_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan034_2021-2024_revE3_lizard_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_034_revE3_plan.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_034_revE3_plan.txt
echo ============================================================
