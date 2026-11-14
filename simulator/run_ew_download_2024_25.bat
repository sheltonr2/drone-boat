@echo off
REM East-west weather: Nov 2024 to Jul 2025, tropical box (docs/East_West_Study.md). Written by collab/east_west/make_ew.py. Approved by Randolph 13 Nov 2026
REM ("plan for an east to west crossing").
REM ERA5 winds (CDS) and Copernicus Marine currents and waves, tropical box 5,40,-80,-5 (lat0,lat1,lon0,lon1), months 2024-11..2025-07.
REM About 22 GB on disk and roughly 6-15 hours. Stored in simulator\workspace_ew, apart from the eastbound data.
REM It resumes where it stopped: queue it again and months already stored are skipped.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_ew_download_2024_25.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ============================================================
echo  East-west weather: Nov 2024 to Jul 2025, tropical box
echo  About 22 GB, roughly 6-15 hours. It resumes if stopped. Started %date% %time%
echo ============================================================
echo East-west weather: Nov 2024 to Jul 2025, tropical box, started %date% %time% >> "%LOG%"
if not exist .venv-bulk\Scripts\python.exe (
  echo .venv-bulk is missing: run setup_bulk_data.bat first. >> "%LOG%"
  echo .venv-bulk is missing: run setup_bulk_data.bat first.
  exit /b 1
)
powershell -NoProfile -Command "exit [int](((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB) -lt 52)" >nul 2>&1
if errorlevel 1 (
  echo Not enough free disk space ^(need 52 GB^) >> "%LOG%"
  echo Not enough free disk space ^(need 52 GB^): see %LOG%
  exit /b 1
)
powershell -NoProfile -Command "'Free space before: {0:N0} GB' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
REM Storm tracks for the tropics (NOAA HURDAT2), once: used by the storm-encounter check after each run.
if not exist ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv .venv-bulk\Scripts\python.exe ..\docs\data\make_hurdat_subset.py >> "%LOG%" 2>&1
echo Downloading. Each line below is one source-month; the full log is %LOG%
.venv-bulk\Scripts\python.exe -m drone_sim.cli download --box 5,40,-80,-5 --months 2024-11..2025-07 >> "%LOG%" 2>&1
powershell -NoProfile -Command "'Free space after: {0:N0} GB' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%" | findstr /c:"already stored" /c:"stored" /c:"failed" /c:"Wrote" /c:"DONE"
echo Finished %date% %time%
