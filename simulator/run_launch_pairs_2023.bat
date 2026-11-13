@echo off
REM Launch-point study, stage B: best 3 launch points + Ocean City x Cornwall and Brittany, then Canaveral rerun (docs/Launch_Point_Study.md). Written by collab/launch_points/make_batch.py.
REM 9 runs of 150 voyages, weather 2023, design revC5_design.json. About 6 h 00 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  Launch-point study, stage B: best 3 launch points + Ocean City x Cornwall and Brittany, then Canaveral rerun
echo  9 runs x 150 voyages. Expected time: about 6 h 00 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_launch_pairs_2023.txt
echo Launch-point study, stage B: best 3 launch points + Ocean City x Cornwall and Brittany, then Canaveral rerun, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 9: hatteras_stream__cornwall   (started %time%)
if exist ..\results\launch_2023_hatteras_stream__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras_stream__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras_stream__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\hatteras_stream__cornwall.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_hatteras_stream__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras_stream__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_hatteras_stream__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras_stream__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 2 of 9: hatteras_stream__brittany   (started %time%)
if exist ..\results\launch_2023_hatteras_stream__brittany.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras_stream__brittany already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras_stream__brittany ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\hatteras_stream__brittany.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_hatteras_stream__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras_stream__brittany.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_hatteras_stream__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras_stream__brittany.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 3 of 9: ocean_city_canyon__cornwall   (started %time%)
if exist ..\results\launch_2023_ocean_city_canyon__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city_canyon__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city_canyon__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\ocean_city_canyon__cornwall.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_ocean_city_canyon__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city_canyon__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_ocean_city_canyon__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city_canyon__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 4 of 9: ocean_city_canyon__brittany   (started %time%)
if exist ..\results\launch_2023_ocean_city_canyon__brittany.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city_canyon__brittany already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city_canyon__brittany ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\ocean_city_canyon__brittany.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_ocean_city_canyon__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city_canyon__brittany.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_ocean_city_canyon__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city_canyon__brittany.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 5 of 9: hatteras__cornwall   (started %time%)
if exist ..\results\launch_2023_hatteras__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\hatteras__cornwall.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_hatteras__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_hatteras__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 6 of 9: hatteras__brittany   (started %time%)
if exist ..\results\launch_2023_hatteras__brittany.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras__brittany already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras__brittany ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\hatteras__brittany.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_hatteras__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras__brittany.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_hatteras__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras__brittany.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 7 of 9: ocean_city__cornwall   (started %time%)
if exist ..\results\launch_2023_ocean_city__cornwall.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city__cornwall already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city__cornwall ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\ocean_city__cornwall.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_ocean_city__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city__cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_ocean_city__cornwall.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city__cornwall.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 8 of 9: ocean_city__brittany   (started %time%)
if exist ..\results\launch_2023_ocean_city__brittany.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city__brittany already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city__brittany ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\ocean_city__brittany.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_ocean_city__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city__brittany.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_ocean_city__brittany.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city__brittany.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo.
echo RUN 9 of 9: canaveral_east__ireland_sw   (started %time%)
if exist ..\results\launch_2023_canaveral_east__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: canaveral_east__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: canaveral_east__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\canaveral_east__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_canaveral_east__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_canaveral_east__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_canaveral_east__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_canaveral_east__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_pairs_2023.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\launch_2023_*.json   Log: collab\run_log_launch_pairs_2023.txt
echo ============================================================
pause
