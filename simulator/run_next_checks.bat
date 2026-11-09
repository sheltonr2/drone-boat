@echo off
REM Next real-weather checks (Nov 2026):
REM  1. Dead-boat drift from three drop points off Ocean City on four May dates (about 10 minutes).
REM  The real-weather Monte Carlo moved to run_real_mc.bat (it takes 2-3 days because of Open-Meteo limits).
REM Everything is written to ..\collab\run_log_next.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_next.txt
if not exist ..\results mkdir ..\results
echo Drone-boat next checks, started %date% %time% > "%LOG%"
echo Running. This takes about 10 minutes; progress goes to collab\run_log_next.txt
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)
if not exist .venv\Scripts\python.exe %PY% -m venv .venv >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m pip install -q -r requirements.txt >> "%LOG%" 2>&1
echo === DRIFT TESTS >> "%LOG%"
.venv\Scripts\python.exe ..\collab\drift_tests.py >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
echo Done. Results are in collab\run_log_next.txt
pause
