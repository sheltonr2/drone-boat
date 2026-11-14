@echo off
REM Sea states along the simulated Hatteras -> Cornwall tracks, for the fatigue analysis (docs/Fatigue_Review.md).
REM Reads the stage C result (Rev D, 500 voyages, 2023 and 2024) and the bulk weather. About 5-15 minutes.
REM Output: ..\results\seastates_hatteras__cornwall.json   Log: ..\collab\run_log_seastates.txt
cd /d "%~dp0"
echo ============================================================
echo  Sea states along the Hatteras -^> Cornwall tracks (fatigue input)
echo  Expected time: about 5-15 minutes. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
.venv\Scripts\python.exe ..\collab\seastates_along_tracks.py ..\results\launch_2023+2024_hatteras__cornwall.json ..\results\seastates_hatteras__cornwall.json > ..\collab\run_log_seastates.txt 2>&1
type ..\collab\run_log_seastates.txt
echo Finished %date% %time%
