@echo off
REM Launch-point study, stage A: 12 launch points, all aimed at south-west Ireland (docs/Launch_Point_Study.md). Written by collab/launch_points/make_batch.py.
REM 12 runs of 150 voyages, weather 2023, design revC5_design.json. About 8 h 00 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  Launch-point study, stage A: 12 launch points, all aimed at south-west Ireland
echo  12 runs x 150 voyages. Expected time: about 8 h 00 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_launch_points_2023.txt
echo Launch-point study, stage A: 12 launch points, all aimed at south-west Ireland, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 12: ocean_city__ireland_sw   (started %time%)
if exist ..\results\launch_2023_ocean_city__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\ocean_city__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_ocean_city__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_ocean_city__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 2 of 12: hatteras_stream__ireland_sw   (started %time%)
if exist ..\results\launch_2023_hatteras_stream__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras_stream__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras_stream__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\hatteras_stream__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_hatteras_stream__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras_stream__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_hatteras_stream__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras_stream__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 3 of 12: hatteras__ireland_sw   (started %time%)
if exist ..\results\launch_2023_hatteras__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: hatteras__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: hatteras__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\hatteras__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_hatteras__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_hatteras__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_hatteras__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 4 of 12: ocean_city_canyon__ireland_sw   (started %time%)
if exist ..\results\launch_2023_ocean_city_canyon__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: ocean_city_canyon__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ocean_city_canyon__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\ocean_city_canyon__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_ocean_city_canyon__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city_canyon__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_ocean_city_canyon__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_ocean_city_canyon__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 5 of 12: virginia_beach__ireland_sw   (started %time%)
if exist ..\results\launch_2023_virginia_beach__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: virginia_beach__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: virginia_beach__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\virginia_beach__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_virginia_beach__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_virginia_beach__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_virginia_beach__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_virginia_beach__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 6 of 12: cape_cod__ireland_sw   (started %time%)
if exist ..\results\launch_2023_cape_cod__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: cape_cod__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: cape_cod__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\cape_cod__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_cape_cod__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_cape_cod__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_cape_cod__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_cape_cod__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 7 of 12: charleston__ireland_sw   (started %time%)
if exist ..\results\launch_2023_charleston__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: charleston__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: charleston__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\charleston__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_charleston__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_charleston__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_charleston__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_charleston__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 8 of 12: palm_beach__ireland_sw   (started %time%)
if exist ..\results\launch_2023_palm_beach__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: palm_beach__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: palm_beach__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\palm_beach__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_palm_beach__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_palm_beach__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_palm_beach__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_palm_beach__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 9 of 12: barnegat__ireland_sw   (started %time%)
if exist ..\results\launch_2023_barnegat__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: barnegat__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: barnegat__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\barnegat__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_barnegat__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_barnegat__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_barnegat__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_barnegat__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 10 of 12: montauk__ireland_sw   (started %time%)
if exist ..\results\launch_2023_montauk__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: montauk__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: montauk__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\montauk__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_montauk__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_montauk__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_montauk__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_montauk__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 11 of 12: canaveral__ireland_sw   (started %time%)
if exist ..\results\launch_2023_canaveral__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: canaveral__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: canaveral__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\canaveral__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_canaveral__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_canaveral__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_canaveral__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_canaveral__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo.
echo RUN 12 of 12: maine__ireland_sw   (started %time%)
if exist ..\results\launch_2023_maine__ireland_sw.json (
  echo   already finished, skipping
  echo ==== RUN: maine__ireland_sw already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: maine__ireland_sw ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\launch_points\maine__ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\launch_2023_maine__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_maine__ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\launch_2023_maine__ireland_sw.json >> "%LOG%" 2>&1
  if exist ..\results\launch_2023_maine__ireland_sw.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_launch_points_2023.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\launch_2023_*.json   Log: collab\run_log_launch_points_2023.txt
echo ============================================================
pause
