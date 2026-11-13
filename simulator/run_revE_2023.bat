@echo off
REM Rev E as drawn (13 Nov 2026): bilge pump and pump-and-sail, sealed rudder servos, tail detent, weed fairing (docs/Design_RevE.md).
REM 250 voyages, 2023 weather, near-coast launch, same seeds as the Rev D run. About 20 minutes on the faster code.
REM Needs the 2023 bulk weather data already on this PC (run_bulk.bat). Log: ..\collab\run_log_revE_2023.txt
cd /d "%~dp0"
echo ============================================================
echo  Rev E as drawn (250 voyages)
echo  Should land a little under the reliability package study (81%%): less weed credit, more mass
echo  Expected time: about 20 minutes. Progress shows below.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_revE_2023.txt
echo Rev E as drawn (250 voyages), started %date% %time% > "%LOG%"
echo.
echo Rev E as drawn (250 voyages)
echo ==== Rev E as drawn (250 voyages) ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revE_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revE_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revE_10km.json >> "%LOG%" 2>&1
echo.
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Upload this file to Claude:  collab\run_log_revE_2023.txt
echo ============================================================
pause
