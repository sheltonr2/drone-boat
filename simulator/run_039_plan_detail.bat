@echo off
REM Run 039: the eastbound final plan on the detailed coasts at Hatteras and Cornwall (Rev E3)
REM Same launches and seeds as runs 026 (Rev E1) and 034 (Rev E3), so the coastline's effect is paired.
REM 1 runs, about 1 h 02 min. Written by collab/runs_036/make_runs.py (26 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_039_plan_detail.txt
echo ============================================================
echo  Run 039: the eastbound final plan on the detailed coasts at Hatteras and Cornwall (Rev E3)
echo  1 runs. Expected time: about 1 h 02 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 039: the eastbound final plan on the detailed coasts at Hatteras and Cornwall (Rev E3), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 1: final plan, detailed coast, 1000 voyages   (started !time!)
if exist ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json (
  echo   already finished, skipping
  echo ==== RUN: final plan, detailed coast, 1000 voyages already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: final plan, detailed coast, 1000 voyages ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\plan_detail_coast.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json >> "%LOG%" 2>&1
  if exist ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json >> "%LOG%" 2>&1
  if exist ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json --out ..\results\plan039_2021-2024_revE3_lizard_offing_detail_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan039_2021-2024_revE3_lizard_offing_detail.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_039_plan_detail.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_039_plan_detail.txt
echo ============================================================
