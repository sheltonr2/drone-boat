@echo off
REM Dead-boat drift tests on the 2024 bulk data, the second year for the drop-point decision.
REM Run it after run_bulk.bat has finished downloading 2024 (May-November). Output: ..\collab\run_log_drift_bulk_2024.txt
cd /d "%~dp0"
echo ============================================================
echo  2024 dead-boat drift tests (192 runs)
echo  Expected time: about 20-30 minutes. Progress shows below; details go to the log.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
.venv\Scripts\python.exe ..\collab\drift_tests.py --bulk --years 2024 --leeway 0.02,0.033,0.05 > ..\collab\run_log_drift_bulk_2024.txt 2>&1
type ..\collab\run_log_drift_bulk_2024.txt
echo Upload collab\run_log_drift_bulk_2024.txt
echo Finished %date% %time%
pause
