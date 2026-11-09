@echo off
REM Next real-weather checks (Nov 2026):
REM  1. Dead-boat drift from three drop points off Ocean City on four May dates (about 10 minutes).
REM  2. Monte Carlo, Ocean City to SW Ireland, 80 voyages launched mid-April to mid-June 2022-2025.
REM     The first run downloads several thousand Open-Meteo blocks; Open-Meteo's free limit is
REM     5,000 calls an hour, so expect 1-3 hours. Leave the computer awake. Later runs use the cache.
REM Everything is written to ..\collab\run_log_next.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_next.txt
if not exist ..\results mkdir ..\results
echo Drone-boat next checks, started %date% %time% > "%LOG%"
echo Running. This can take 1-3 hours; progress goes to collab\run_log_next.txt
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)
if not exist .venv\Scripts\python.exe %PY% -m venv .venv >> "%LOG%" 2>&1
.venv\Scripts\python.exe -m pip install -q -r requirements.txt >> "%LOG%" 2>&1
echo === DRIFT TESTS >> "%LOG%"
.venv\Scripts\python.exe ..\collab\drift_tests.py >> "%LOG%" 2>&1
echo === MONTE CARLO >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --runs 80 --from 2022-04-15 --to 2022-06-15 --years 2022,2023,2024,2025 --out ..\results\real_mc_ocmd_ireland.json >> "%LOG%" 2>&1
.venv\Scripts\python.exe -c "import json; s=json.load(open('../results/real_mc_ocmd_ireland.json'))['result']['summary']; print(json.dumps({k: s[k] for k in ('runs','success_percent','success_ci95','any_arrival_percent','percent','arrival_days','failure_causes','by_launch_month','mean_airtime_usd','mean_knockdowns')}, indent=1, default=str))" >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
echo Done. Results are in collab\run_log_next.txt
pause
