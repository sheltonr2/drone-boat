@echo off
REM Electronics study (12 Nov 2026): Rev C5 with better-protected electronics, using GUESSED rates for potting, conformal
REM coating and an encapsulated RockBLOCK Plus. 250 voyages, 2023 weather, near-coast launch. About 1 hour 20 minutes. docs/Electronics_Review.md
REM Needs the 2023 bulk weather data already on this PC (run_bulk.bat). Log: ..\collab\run_log_electronics_2023.txt
cd /d "%~dp0"
echo ============================================================
echo  Electronics study: Rev C5, better-protected electronics (250 voyages)
echo  Compare with the C5 step of run_fixed_compare_2023.bat
echo  Expected time: about 1 hour 20 minutes. Progress shows below.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_electronics_2023.txt
echo Electronics study 2023, started %date% %time% > "%LOG%"
echo.
echo STEP 1 of 1: Rev C5, better-protected electronics
echo ==== Rev C5, better-protected electronics ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_electronics_study_design.json --scenario ..\collab\bulk_mc_2023_10km_electronics.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revC5_electronics_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revC5_electronics_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revC5_electronics_10km.json >> "%LOG%" 2>&1
echo.
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Upload this file to Claude:  collab\run_log_electronics_2023.txt
echo ============================================================
pause
