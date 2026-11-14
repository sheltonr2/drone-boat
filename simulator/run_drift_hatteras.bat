@echo off
REM Dead-boat drift tests from the Hatteras drop points (docs/Naval_Review.md, item 7). 13 Nov 2026.
REM Three drop points (inlet 10 km, 45 km on the Stream edge, 70 km east of Diamond Shoals), a drop every 3 days
REM 1 May - 15 June, 2023 and 2024 weather, three leeway factors: 288 runs of 30 days. About 10-20 minutes.
REM Output: ..\results\drift_tests_hatteras_bulk_2023-2024.json   Log: ..\collab\run_log_drift_hatteras.txt
cd /d "%~dp0"
echo ============================================================
echo  Dead-boat drift tests from the Hatteras drop points (288 runs)
echo  Expected time: about 10-20 minutes. Progress shows below; details go to the log.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
.venv\Scripts\python.exe ..\collab\drift_tests.py --set hatteras --bulk --years 2023,2024 --leeway 0.02,0.033,0.05 > ..\collab\run_log_drift_hatteras.txt 2>&1
type ..\collab\run_log_drift_hatteras.txt | findstr /c:"Summary" /c:"leeway" /c:"aground" /c:"Saved"
echo Finished %date% %time%
