@echo off
REM Run 027: DFM sensitivities: smaller solar (30 W, 20 W) and the stock 30 x 26 spar
REM Same launches and seeds as run 025 (Lizard offing v2, 500 voyages, 1 May-15 Jun 2023+2024), so differences are paired.
REM 3 runs, about 1 h 35 min. Written by collab/runs_026/make_runs.py (21 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_027_dfm_sensitivity.txt
echo ============================================================
echo  Run 027: DFM sensitivities: smaller solar (30 W, 20 W) and the stock 30 x 26 spar
echo  3 runs. Expected time: about 1 h 35 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 027: DFM sensitivities: smaller solar (30 W, 20 W) and the stock 30 x 26 spar, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 3: solar30   (started !time!)
if exist ..\results\dfm027_2023+2024_revE1_solar30_lizard_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: solar30 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: solar30 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_solar30_study_design.json --scenario ..\collab\arrival\hatteras_stream__lizard_offing_hold_v2.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\dfm027_2023+2024_revE1_solar30_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\dfm027_2023+2024_revE1_solar30_lizard_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dfm027_2023+2024_revE1_solar30_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\dfm027_2023+2024_revE1_solar30_lizard_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_027_dfm_sensitivity.txt)
)
echo.
echo RUN 2 of 3: solar20   (started !time!)
if exist ..\results\dfm027_2023+2024_revE1_solar20_lizard_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: solar20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: solar20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_solar20_study_design.json --scenario ..\collab\arrival\hatteras_stream__lizard_offing_hold_v2.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\dfm027_2023+2024_revE1_solar20_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\dfm027_2023+2024_revE1_solar20_lizard_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dfm027_2023+2024_revE1_solar20_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\dfm027_2023+2024_revE1_solar20_lizard_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_027_dfm_sensitivity.txt)
)
echo.
echo RUN 3 of 3: spar3026   (started !time!)
if exist ..\results\dfm027_2023+2024_revE1_spar3026_lizard_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: spar3026 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: spar3026 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_spar3026_study_design.json --scenario ..\collab\arrival\hatteras_stream__lizard_offing_hold_v2.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\dfm027_2023+2024_revE1_spar3026_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\dfm027_2023+2024_revE1_spar3026_lizard_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dfm027_2023+2024_revE1_spar3026_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\dfm027_2023+2024_revE1_spar3026_lizard_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_027_dfm_sensitivity.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_027_dfm_sensitivity.txt
echo ============================================================
