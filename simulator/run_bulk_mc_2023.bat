@echo off
REM Monte Carlo on the 2023 bulk data only (250 voyages from the 100 km drop, launched 1 May - 15 June 2023),
REM using every processor core. Run it once May-November 2023 are downloaded; run_bulk.bat can keep
REM downloading 2024 in its own window at the same time. Results go to ..\collab\run_log_bulk_2023.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_bulk_2023.txt
echo Bulk Monte Carlo 2023, started %date% %time% > "%LOG%"
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)
if not exist .venv\Scripts\python.exe %PY% -m venv .venv >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m pip install -q --disable-pip-version-check -r requirements.txt >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m drone_sim.cli mc --scenario ..\collab\bulk_mc_2023-2024.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_ocmd100_ireland.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_ocmd100_ireland.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_ocmd100_ireland.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%"
echo Upload collab\run_log_bulk_2023.txt and results\bulk_mc_2023_ocmd100_ireland.json
pause
