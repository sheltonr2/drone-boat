@echo off
REM Run 043c part 1: Rev F baseline and B90 checks
REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_043c1_east.txt
echo ------------------------------------------------------------
echo  Run 043c part 1: Rev F baseline and B90 checks: 5 runs
echo ------------------------------------------------------------
echo Run 043c part 1: Rev F baseline and B90 checks, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 5: Rev F: plan B   (started !time!)
if exist ..\results\plan043c_2021-2024_revF_B_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Rev F: plan B already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Rev F: plan B ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043a\plan_B.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043c_2021-2024_revF_B_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043c_2021-2024_revF_B_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043c_2021-2024_revF_B_v2.json --out ..\results\plan043c_2021-2024_revF_B_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c1_east.txt)
)
echo.
echo RUN 2 of 5: Rev F: B90   (started !time!)
if exist ..\results\plan043c_2021-2024_revF_B90_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Rev F: B90 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Rev F: B90 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043b\plan_B90.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043c_2021-2024_revF_B90_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043c_2021-2024_revF_B90_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043c_2021-2024_revF_B90_v2.json --out ..\results\plan043c_2021-2024_revF_B90_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c1_east.txt)
)
echo.
echo RUN 3 of 5: Rev F: B90 launched in April   (started !time!)
if exist ..\results\plan043c_2021-2024_revF_B90_april_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Rev F: B90 launched in April already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Rev F: B90 launched in April ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043b\plan_B90.json --runs 1000 --from 2023-04-01 --to 2023-04-30 --years 2021,2022,2023,2024 --out ..\results\plan043c_2021-2024_revF_B90_april_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_april_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043c_2021-2024_revF_B90_april_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_april_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043c_2021-2024_revF_B90_april_v2.json --out ..\results\plan043c_2021-2024_revF_B90_april_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_april_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c1_east.txt)
)
echo.
echo RUN 4 of 5: Rev F: B90 launched 21 May-15 Jun   (started !time!)
if exist ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Rev F: B90 launched 21 May-15 Jun already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Rev F: B90 launched 21 May-15 Jun ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043b\plan_B90.json --runs 1000 --from 2023-05-21 --to 2023-06-15 --years 2021,2022,2023,2024 --out ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json --out ..\results\plan043c_2021-2024_revF_B90_latemay_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_latemay_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c1_east.txt)
)
echo.
echo RUN 5 of 5: Rev F: B90 from the 70 km drop   (started !time!)
if exist ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Rev F: B90 from the 70 km drop already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Rev F: B90 from the 70 km drop ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\plan_B90_drop70.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json --out ..\results\plan043c_2021-2024_revF_B90_drop70_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043c_2021-2024_revF_B90_drop70_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c1_east.txt)
)
echo === DONE %date% %time% >> "%LOG%"
endlocal
