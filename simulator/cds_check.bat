@echo off
REM Checks access to the Climate Data Store (ERA5) and writes the result to ..\collab\cds_check.txt.
REM It never prints your API token. It sends at most one tiny data request.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
.venv-bulk\Scripts\python.exe -m drone_sim.cli cdscheck > ..\collab\cds_check.txt 2>&1
type ..\collab\cds_check.txt
echo.
echo Upload collab\cds_check.txt
pause
