@echo off
REM Runs the shared checks agreed with boat-sim (issue #50) on real weather:
REM self-test, the dead-boat drift from 36.85N 75.70W on 2023-05-15, and the 1.0 vs 0.25 degree grid check.
REM Everything is written to ..\collab\run_log.txt. Needs internet (Open-Meteo, Natural Earth).
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log.txt
if not exist ..\results mkdir ..\results
echo Drone-boat collab checks, started %date% %time% > "%LOG%"
echo Running the checks. This can take 20-40 minutes; progress goes to collab\run_log.txt
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)
%PY% --version >> "%LOG%" 2>&1
if errorlevel 1 (
  echo PYTHON_MISSING >> "%LOG%"
  echo Python 3.10 or newer is needed: https://www.python.org/downloads/
  pause
  exit /b 1
)
if not exist .venv\Scripts\python.exe %PY% -m venv .venv >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m pip install -q -r requirements.txt >> "%LOG%" 2>&1
echo === SELFTEST >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli selftest >> "%LOG%" 2>&1
echo === DEAD BOAT >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli voyage --scenario ..\collab\dead_boat_2023-05-15.json --out ..\results\dead_boat_2023-05-15.json >> "%LOG%" 2>&1
.venv\Scripts\python.exe ..\collab\summarize_dead_boat.py ..\results\dead_boat_2023-05-15.json >> "%LOG%" 2>&1
echo === GRIDCHECK >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli gridcheck >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
echo Done. Results are in collab\run_log.txt
pause
