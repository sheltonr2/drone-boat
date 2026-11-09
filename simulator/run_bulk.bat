@echo off
REM Bulk real-weather run (Nov 2026):
REM  1. Download ERA5 (CDS) and Copernicus Marine currents + waves for May-November 2023 and 2024.
REM     Roughly 35 GB on disk and a few hours (CDS requests queue one at a time). It resumes if stopped.
REM  2. Check the bulk data against the Open-Meteo data already cached on this PC.
REM  3. Monte Carlo: 500 voyages from the 100 km drop off Ocean City, launched 1 May - 15 June,
REM     using every processor core.
REM Progress goes to ..\collab\run_log_bulk.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_bulk.txt
if not exist .venv-bulk\Scripts\python.exe (
  echo Run setup_bulk_data.bat first.
  pause
  exit /b 1
)
echo Bulk run, started %date% %time% >> "%LOG%"
echo Running. Downloads take a few hours; progress goes to collab\run_log_bulk.txt
echo === DOWNLOAD >> "%LOG%"
.venv-bulk\Scripts\python.exe -m drone_sim.cli download --months 2023-05..2023-11,2024-05..2024-11 >> "%LOG%" 2>&1
echo === CHECK AGAINST OPEN-METEO >> "%LOG%"
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)
if not exist .venv\Scripts\python.exe %PY% -m venv .venv >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m pip install -q --disable-pip-version-check -r requirements.txt >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m drone_sim.cli bulkcheck >> "%LOG%" 2>&1
echo === MONTE CARLO (all cores) >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --scenario ..\collab\bulk_mc_2023-2024.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\bulk_mc_ocmd100_ireland.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_ocmd100_ireland.json (
  .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_ocmd100_ireland.json >> "%LOG%" 2>&1
) else (
  echo No result file - see the messages above. >> "%LOG%"
)
echo === DONE %date% %time% >> "%LOG%"
echo Done. Upload collab\run_log_bulk.txt and results\bulk_mc_ocmd100_ireland.json
pause
