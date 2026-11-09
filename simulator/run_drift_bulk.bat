@echo off
REM Dead-boat drift tests on the downloaded bulk data (2023): 4 drop points x a drop every 3 days, 1 May - 15 June.
REM Uses the leeway drift model (9 Nov 2026) at 2%, 3.3% and 5% of the wind (sensitivity). No downloads. Output: ..\collab\run_log_drift_bulk.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
.venv\Scripts\python.exe ..\collab\drift_tests.py --bulk --years 2023 --leeway 0.02,0.033,0.05 > ..\collab\run_log_drift_bulk.txt 2>&1
type ..\collab\run_log_drift_bulk.txt
echo Upload collab\run_log_drift_bulk.txt
pause
