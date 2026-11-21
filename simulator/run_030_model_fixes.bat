@echo off
REM Run 030: model fixes on the final plan: storm winds in the loop (boat-sim #117) and knockdown severity
REM Same launches and seeds as run 026 (the 500-voyage runs pair with its first 500), so the effect of each fix is paired.
REM 3 runs, about 2 h 05 min. Written by collab/runs_026/make_runs.py (21 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_030_model_fixes.txt
echo ============================================================
echo  Run 030: model fixes on the final plan: storm winds in the loop (boat-sim #117) and knockdown severity
echo  3 runs. Expected time: about 2 h 05 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 030: model fixes on the final plan: storm winds in the loop (boat-sim #117) and knockdown severity, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 3: both fixes, 1000 voyages   (started !time!)
if exist ..\results\fix030_2021-2024_revE1_both.json (
  echo   already finished, skipping
  echo ==== RUN: both fixes, 1000 voyages already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: both fixes, 1000 voyages ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\plan_fix_both.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\fix030_2021-2024_revE1_both.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_both.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\fix030_2021-2024_revE1_both.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_both.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\fix030_2021-2024_revE1_both.json --out ..\results\fix030_2021-2024_revE1_both_storms.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_both.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_030_model_fixes.txt)
)
echo.
echo RUN 2 of 3: storm winds only, 500   (started !time!)
if exist ..\results\fix030_2021-2024_revE1_storm.json (
  echo   already finished, skipping
  echo ==== RUN: storm winds only, 500 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: storm winds only, 500 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\plan_fix_storm.json --runs 500 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\fix030_2021-2024_revE1_storm.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_storm.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\fix030_2021-2024_revE1_storm.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_storm.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_030_model_fixes.txt)
)
echo.
echo RUN 3 of 3: knockdown severity only, 500   (started !time!)
if exist ..\results\fix030_2021-2024_revE1_severity.json (
  echo   already finished, skipping
  echo ==== RUN: knockdown severity only, 500 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: knockdown severity only, 500 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\runs_026\plan_fix_severity.json --runs 500 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\fix030_2021-2024_revE1_severity.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_severity.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\fix030_2021-2024_revE1_severity.json >> "%LOG%" 2>&1
  if exist ..\results\fix030_2021-2024_revE1_severity.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_030_model_fixes.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_030_model_fixes.txt
echo ============================================================
