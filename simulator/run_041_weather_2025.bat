@echo off
REM Run 041: the 2025 weather, so every study can add a fifth year. Asked for by Randolph 26 Nov 2026
REM ("rerun with the 2025 weather").
REM Part 1, eastbound (North Atlantic box, simulator\workspace): May-Nov 2025, the 2025 season for the eastbound plan
REM and the Cornwall holding study. About 7 source-months x 3 sources, roughly 20 GB.
REM Part 2, east-west (tropical box 5,40,-80,-5, simulator\workspace_ew): Nov 2025-Jun 2026, the 2025-26 winter for
REM the Mindelo crossing and the BVI holding study (Feb-Apr 2026). 8 source-months x 3 sources, roughly 20 GB.
REM ERA5 takes 2-7 h a month at CDS, one request at a time, so this takes 2-4 days. It resumes where it stopped:
REM queue it again and months already stored are skipped. Logs: ..\collab\run_log_041_weather_2025.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_041_weather_2025.txt
echo ============================================================
echo  Run 041: 2025 weather, eastbound May-Nov 2025 then east-west Nov 2025-Jun 2026
echo  About 40 GB, roughly 2-4 days (ERA5 is 2-7 h a month at CDS). It resumes if stopped. Started %date% %time%
echo ============================================================
echo Run 041: 2025 weather, started %date% %time% >> "%LOG%"
if not exist .venv-bulk\Scripts\python.exe (
  echo .venv-bulk is missing: run setup_bulk_data.bat first. >> "%LOG%"
  echo .venv-bulk is missing: run setup_bulk_data.bat first.
  exit /b 1
)
powershell -NoProfile -Command "exit [int](((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB) -lt 60)" >nul 2>&1
if errorlevel 1 (
  echo Not enough free disk space ^(need 60 GB^) >> "%LOG%"
  echo Not enough free disk space ^(need 60 GB^): see %LOG%
  exit /b 1
)
powershell -NoProfile -Command "'Free space before: {0:N0} GB' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
echo [1/2] Eastbound box, May-Nov 2025. Each source-month is logged to %LOG%
echo [1/2] Eastbound box, May-Nov 2025 >> "%LOG%"
.venv-bulk\Scripts\python.exe -m drone_sim.cli download --months 2025-05..2025-11 >> "%LOG%" 2>&1
type "%LOG%" | findstr /c:"done in" /c:"failed" /c:"refused" /c:"finished"
echo [2/2] East-west tropical box, Nov 2025-Jun 2026. Each source-month is logged to %LOG%
echo [2/2] East-west tropical box, Nov 2025-Jun 2026 >> "%LOG%"
set DRONE_SIM_HOME=%~dp0workspace_ew
.venv-bulk\Scripts\python.exe -m drone_sim.cli download --box 5,40,-80,-5 --months 2025-11..2026-06 >> "%LOG%" 2>&1
set DRONE_SIM_HOME=
powershell -NoProfile -Command "'Free space after: {0:N0} GB' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%" | findstr /c:"already stored" /c:"done in" /c:"failed" /c:"refused" /c:"finished" /c:"DONE"
echo Finished %date% %time%
