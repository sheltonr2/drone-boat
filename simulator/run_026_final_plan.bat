@echo off
REM Run 026: the final plan on four weather years (Hatteras 45 km to the Lizard offing, 1-20 May)
REM Rev E1, the decided route and holding point (run 025's scenario), launches 1-20 May 2021-2024. Storm check after.
REM 1 runs, about 1 h 02 min. Written by collab/runs_026/make_runs.py (21 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_026_final_plan.txt
echo ============================================================
echo  Run 026: the final plan on four weather years (Hatteras 45 km to the Lizard offing, 1-20 May)
echo  1 runs. Expected time: about 1 h 02 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 026: the final plan on four weather years (Hatteras 45 km to the Lizard offing, 1-20 May), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 1: final plan, 1000 voyages   (started !time!)
if exist ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: final plan, 1000 voyages already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: final plan, 1000 voyages ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\arrival\hatteras_stream__lizard_offing_hold_v2.json --runs 1000 --from 2023-05-01 --to 2023-05-20 --years 2021,2022,2023,2024 --out ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json --out ..\results\plan026_2021-2024_revE1_lizard_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\plan026_2021-2024_revE1_lizard_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_026_final_plan.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_026_final_plan.txt
echo ============================================================
