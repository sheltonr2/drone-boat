@echo off
REM Rev C5 against Rev C2 with the structural-failure model matched to measured buoy data (docs/Research_Review.md).
REM 250 voyages each on 2023 weather from the near-coast launch point. About 2 hours with all cores.
REM Needs the 2023 bulk weather data already on this PC (run_bulk.bat). Log: ..\collab\run_log_revC5_2023.txt
cd /d "%~dp0"
echo ============================================================
echo  Rev C5 run, strike model matched to buoy data (2 x 250 voyages)
echo  Step 1: Rev C5, the boat with the structural changes
echo  Step 2: Rev C2, the boat before them, same failure model
echo  Expected time: about 2 hours. Progress shows below.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_revC5_2023.txt
echo Rev C5 run 2023, started %date% %time% > "%LOG%"
echo.
echo STEP 1 of 2: Rev C5
echo ==== STEP 1: Rev C5, structural model on ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revC5_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revC5_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revC5_10km.json >> "%LOG%" 2>&1
echo.
echo STEP 2 of 2: Rev C2 with the same failure model
echo ==== STEP 2: Rev C2, structural model on ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC2_structure_measured_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revC2_structure_measured_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revC2_structure_measured_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revC2_structure_measured_10km.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Upload this file to Claude:  collab\run_log_revC5_2023.txt
echo ============================================================
pause
