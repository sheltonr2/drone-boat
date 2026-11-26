@echo off
REM Run 042: safer approaches to Cornwall (south of Scilly; hold 30 km south of the Lizard), Rev E3, detailed coast
REM Same launches and seeds as run 039 (1000 voyages, 1-20 May, 2021-2024). Written by collab/runs_042/make_runs.py (26 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_042_approach_variants.txt
echo ============================================================
echo  Run 042: safer approaches to Cornwall (south of Scilly; hold 30 km south of the Lizard), Rev E3, detailed coast
echo  2 runs. Expected time: about 2 h 00 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 042: safer approaches to Cornwall (south of Scilly; hold 30 km south of the Lizard), Rev E3, detailed coast, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 2: A: approach south of Scilly, Lizard offing hold   (started !time!)
if exist ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json (
  echo   already finished, skipping
  echo ==== RUN: A: approach south of Scilly, Lizard offing hold already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: A: approach south of Scilly, Lizard offing hold ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_042\plan_south.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json >> "%LOG%" 2>&1
  if exist ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json >> "%LOG%" 2>&1
  if exist ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json --out ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan042_2021-2024_revE3_south_lizard_offing_detail.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_042_approach_variants.txt)
)
echo.
echo RUN 2 of 2: B: approach south of Scilly, hold 30 km south of the Lizard   (started !time!)
if exist ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json (
  echo   already finished, skipping
  echo ==== RUN: B: approach south of Scilly, hold 30 km south of the Lizard already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: B: approach south of Scilly, hold 30 km south of the Lizard ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_042\plan_south_deep.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json >> "%LOG%" 2>&1
  if exist ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json >> "%LOG%" 2>&1
  if exist ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json --out ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan042_2021-2024_revE3_south_lizard_deep_detail.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_042_approach_variants.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_042_approach_variants.txt
echo ============================================================
