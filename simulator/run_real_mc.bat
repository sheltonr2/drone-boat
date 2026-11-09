@echo off
REM Real-weather Monte Carlo, Ocean City (100 km offshore drop) to SW Ireland.
REM 60 voyages launched 1 May - 15 June in 2023 and 2024, planning failure rates.
REM The weather download is about 23,000 Open-Meteo calls; the free limit is about 10,000 a day,
REM so this takes 2-3 days. Leave the computer ON and plugged in (it asks Windows not to sleep): when the
REM daily limit is hit it waits until 7:10 pm Eastern and carries on by itself. If it gets
REM interrupted anyway, just double-click this file again - everything downloaded is kept.
REM Progress goes to ..\collab\run_log_real_mc.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_real_mc.txt
if not exist ..\results mkdir ..\results
echo Real-weather Monte Carlo, started %date% %time% >> "%LOG%"
echo Running. This takes 2-3 days; keep the computer awake. Progress: collab\run_log_real_mc.txt
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)
if not exist .venv\Scripts\python.exe %PY% -m venv .venv >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m pip install -q --disable-pip-version-check -r requirements.txt >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m drone_sim.cli mc --wait-for-limits --scenario ..\collab\real_mc_2023-2024.json --runs 60 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\real_mc_ocmd100_ireland.json >> "%LOG%" 2>&1
if exist ..\results\real_mc_ocmd100_ireland.json (
  .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\real_mc_ocmd100_ireland.json >> "%LOG%" 2>&1
) else (
  echo No result file yet - see the messages above. >> "%LOG%"
)
echo === DONE %date% %time% >> "%LOG%"
echo Done. Upload collab\run_log_real_mc.txt and results\real_mc_ocmd100_ireland.json
pause
