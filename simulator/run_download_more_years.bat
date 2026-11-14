@echo off
REM More weather years for the simulator (docs/Naval_Review.md, item 9). Approved by Randolph 13 Nov 2026.
REM Downloads ERA5 winds (CDS) and Copernicus Marine currents and waves for April 2021-2024 and May-November 2021
REM and 2022, the same North Atlantic box as before. About 18 source-months x 3 sources, roughly 55 GB on disk.
REM CDS requests queue one at a time, so this can take a day or more. It resumes where it stopped if the PC
REM sleeps or this window is closed: queue it again (the run queue skips months already stored).
REM It uses the logins already set up on this PC by setup_bulk_data.bat. Log: ..\collab\run_log_download_more_years.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_download_more_years.txt
echo ============================================================
echo  Weather download: April 2021-2024 and May-Nov 2021, 2022 (about 55 GB)
echo  Expected time: a day or more. It resumes if stopped. Started %date% %time%
echo ============================================================
echo Download of more weather years, started %date% %time% >> "%LOG%"
if not exist .venv-bulk\Scripts\python.exe (
  echo .venv-bulk is missing: run setup_bulk_data.bat first. >> "%LOG%"
  echo .venv-bulk is missing: run setup_bulk_data.bat first.
  exit /b 1
)
REM Stop if the drive has under 70 GB free, rather than filling it.
powershell -NoProfile -Command "exit [int](((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB) -lt 70)" >nul 2>&1
if errorlevel 1 (
  powershell -NoProfile -Command "'Free space on this drive: {0:N0} GB. Need 70 GB; download not started.' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
  echo Not enough free disk space ^(need 70 GB^): see %LOG%
  exit /b 1
)
powershell -NoProfile -Command "'Free space before: {0:N0} GB' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
echo Downloading. Each line below is one source-month; the full log is %LOG%
.venv-bulk\Scripts\python.exe -m drone_sim.cli download --months 2022-05..2022-11,2021-05..2021-11,2024-04,2023-04,2022-04,2021-04 >> "%LOG%" 2>&1
powershell -NoProfile -Command "'Free space after: {0:N0} GB' -f ((Get-PSDrive -Name ((Get-Location).Drive.Name)).Free/1GB)" >> "%LOG%"
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%" | findstr /c:"already stored" /c:"stored" /c:"failed" /c:"DONE"
echo Finished %date% %time%
