@echo off
REM Run 043a part 1: eastbound plans and Cornwall holds on the v2 coasts
REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_043a1_east_v2.txt
echo ------------------------------------------------------------
echo  Run 043a part 1: eastbound plans and Cornwall holds on the v2 coasts: 10 runs
echo ------------------------------------------------------------
echo Run 043a part 1: eastbound plans and Cornwall holds on the v2 coasts, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 10: B: south of Scilly, hold 30 km S of the Lizard   (started !time!)
if exist ..\results\plan043a_2021-2024_revE3_B_v2.json (
  echo   already finished, skipping
  echo ==== RUN: B: south of Scilly, hold 30 km S of the Lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: B: south of Scilly, hold 30 km S of the Lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\plan_B.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043a_2021-2024_revE3_B_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043a_2021-2024_revE3_B_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043a_2021-2024_revE3_B_v2.json --out ..\results\plan043a_2021-2024_revE3_B_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 2 of 10: A: south of Scilly, Lizard offing   (started !time!)
if exist ..\results\plan043a_2021-2024_revE3_A_v2.json (
  echo   already finished, skipping
  echo ==== RUN: A: south of Scilly, Lizard offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: A: south of Scilly, Lizard offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\plan_A.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043a_2021-2024_revE3_A_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_A_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043a_2021-2024_revE3_A_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_A_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043a_2021-2024_revE3_A_v2.json --out ..\results\plan043a_2021-2024_revE3_A_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_A_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 3 of 10: old: 18 Nov plan   (started !time!)
if exist ..\results\plan043a_2021-2024_revE3_old_v2.json (
  echo   already finished, skipping
  echo ==== RUN: old: 18 Nov plan already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: old: 18 Nov plan ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\plan_old.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043a_2021-2024_revE3_old_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_old_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043a_2021-2024_revE3_old_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_old_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043a_2021-2024_revE3_old_v2.json --out ..\results\plan043a_2021-2024_revE3_old_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_old_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 4 of 10: B launched in April   (started !time!)
if exist ..\results\plan043a_2021-2024_revE3_B_april_v2.json (
  echo   already finished, skipping
  echo ==== RUN: B launched in April already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: B launched in April ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\plan_B.json --runs 1000 --from 2023-04-01 --to 2023-04-30 --years 2021,2022,2023,2024 --out ..\results\plan043a_2021-2024_revE3_B_april_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_april_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043a_2021-2024_revE3_B_april_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_april_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043a_2021-2024_revE3_B_april_v2.json --out ..\results\plan043a_2021-2024_revE3_B_april_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_april_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 5 of 10: B launched 21 May-15 Jun   (started !time!)
if exist ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json (
  echo   already finished, skipping
  echo ==== RUN: B launched 21 May-15 Jun already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: B launched 21 May-15 Jun ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\plan_B.json --runs 1000 --from 2023-05-21 --to 2023-06-15 --years 2021,2022,2023,2024 --out ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json --out ..\results\plan043a_2021-2024_revE3_B_latemay_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_latemay_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 6 of 10: B from the 70 km drop   (started !time!)
if exist ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json (
  echo   already finished, skipping
  echo ==== RUN: B from the 70 km drop already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: B from the 70 km drop ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\plan_B_drop70.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json --out ..\results\plan043a_2021-2024_revE3_B_drop70_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan043a_2021-2024_revE3_B_drop70_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 7 of 10: Cornwall hold station_lizard_deep   (started !time!)
if exist ..\results\hold043a_2021-2024_revE3_station_lizard_deep_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Cornwall hold station_lizard_deep already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Cornwall hold station_lizard_deep ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_station_lizard_deep.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold043a_2021-2024_revE3_station_lizard_deep_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_station_lizard_deep_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2021-2024_revE3_station_lizard_deep_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_station_lizard_deep_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 8 of 10: Cornwall hold drift_lizard_deep   (started !time!)
if exist ..\results\hold043a_2021-2024_revE3_drift_lizard_deep_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Cornwall hold drift_lizard_deep already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Cornwall hold drift_lizard_deep ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_drift_lizard_deep.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold043a_2021-2024_revE3_drift_lizard_deep_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_drift_lizard_deep_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2021-2024_revE3_drift_lizard_deep_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_drift_lizard_deep_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 9 of 10: Cornwall hold station_lizard   (started !time!)
if exist ..\results\hold043a_2021-2024_revE3_station_lizard_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Cornwall hold station_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Cornwall hold station_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_station_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold043a_2021-2024_revE3_station_lizard_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_station_lizard_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2021-2024_revE3_station_lizard_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_station_lizard_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo.
echo RUN 10 of 10: Cornwall hold drift_lizard   (started !time!)
if exist ..\results\hold043a_2021-2024_revE3_drift_lizard_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Cornwall hold drift_lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Cornwall hold drift_lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_drift_lizard.json --runs 500 --from 2023-08-15 --to 2023-10-15 --years 2021,2022,2023,2024 --out ..\results\hold043a_2021-2024_revE3_drift_lizard_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_drift_lizard_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2021-2024_revE3_drift_lizard_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2021-2024_revE3_drift_lizard_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a1_east_v2.txt)
)
echo === DONE %date% %time% >> "%LOG%"
endlocal
