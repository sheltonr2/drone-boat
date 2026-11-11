@echo off
REM Runs the 2024 drift tests, then the Rev C1 comparison (about 1.5 hours in all). Logs go to ..\collab\.
cd /d "%~dp0"
call run_drift_bulk_2024.bat < nul
call run_revC1_compare_2023.bat < nul
echo.
echo ALL DONE. Upload collab\run_log_drift_bulk_2024.txt and collab\run_log_revC1_compare_2023.txt
pause
