@echo off
REM Run 043b part 1: approaches further south of Scilly, Cornwall holds upwind
REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_043b1_east.txt
echo ------------------------------------------------------------
echo  Run 043b part 1: approaches further south of Scilly, Cornwall holds upwind: 4 runs
echo ------------------------------------------------------------
echo Run 043b part 1: approaches further south of Scilly, Cornwall holds upwind, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 4: approach B60   (started !time!)
if exist ..\results\plan043b_2021-2024_revE3_B60_v2.json (
  echo   already finished, skipping
  echo ==== RUN: approach B60 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: approach B60 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\plan_B60.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043b_2021-2024_revE3_B60_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043b_2021-2024_revE3_B60_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043b_2021-2024_revE3_B60_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043b_2021-2024_revE3_B60_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043b_2021-2024_revE3_B60_v2.json --out ..\results\plan043b_2021-2024_revE3_B60_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043b_2021-2024_revE3_B60_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b1_east.txt)
)
echo.
echo RUN 2 of 4: approach B90   (started !time!)
if exist ..\results\plan043b_2021-2024_revE3_B90_v2.json (
  echo   already finished, skipping
  echo ==== RUN: approach B90 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: approach B90 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\plan_B90.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043b_2021-2024_revE3_B90_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043b_2021-2024_revE3_B90_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043b_2021-2024_revE3_B90_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043b_2021-2024_revE3_B90_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043b_2021-2024_revE3_B90_v2.json --out ..\results\plan043b_2021-2024_revE3_B90_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043b_2021-2024_revE3_B90_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b1_east.txt)
)
echo.
echo RUN 3 of 4: Cornwall hold lizard_deep_SW20   (started !time!)
if exist ..\results\hold043b_2021-2024_revE3_station_lizard_deep_SW20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Cornwall hold lizard_deep_SW20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Cornwall hold lizard_deep_SW20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_lizard_deep_SW20.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold043b_2021-2024_revE3_station_lizard_deep_SW20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2021-2024_revE3_station_lizard_deep_SW20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2021-2024_revE3_station_lizard_deep_SW20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2021-2024_revE3_station_lizard_deep_SW20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b1_east.txt)
)
echo.
echo RUN 4 of 4: Cornwall hold lizard_deep_W20   (started !time!)
if exist ..\results\hold043b_2021-2024_revE3_station_lizard_deep_W20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Cornwall hold lizard_deep_W20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Cornwall hold lizard_deep_W20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_lizard_deep_W20.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold043b_2021-2024_revE3_station_lizard_deep_W20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2021-2024_revE3_station_lizard_deep_W20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2021-2024_revE3_station_lizard_deep_W20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2021-2024_revE3_station_lizard_deep_W20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b1_east.txt)
)
echo === DONE %date% %time% >> "%LOG%"
endlocal
