@echo off
REM Near-coast launch (~10 km off Ocean City Inlet) vs the 100 km drop, on the 2023 bulk data, with the
REM refitted rig and leak rates (10 Nov 2026). 250 voyages each, same seeds, launched 1 May - 15 June 2023.
REM About 1 hour each with all cores. It can run while run_bulk.bat is still downloading; start it before
REM about 8 pm so it finishes before that window's own Monte Carlo begins. Log: ..\collab\run_log_launch_compare_2023.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_launch_compare_2023.txt
echo Launch-point comparison 2023, started %date% %time% > "%LOG%"
echo === NEAR-COAST, ~10 km off the inlet >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_10km_refit.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_10km_refit.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_10km_refit.json >> "%LOG%" 2>&1
echo === 100 km DROP >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --scenario ..\collab\bulk_mc_2023-2024.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_100km_refit.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_100km_refit.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_100km_refit.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%"
echo Upload collab\run_log_launch_compare_2023.txt and results\bulk_mc_2023_10km_refit.json and results\bulk_mc_2023_100km_refit.json
pause
