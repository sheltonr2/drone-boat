@echo off
REM Run 031: sea states along the westbound Mindelo -> BVI tracks (run 024a), for the fatigue check (docs/Fatigue_Review.md).
REM About 10-20 minutes. Written by collab/runs_026/make_runs.py (21 Nov 2026).
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set DRONE_SIM_HOME=%~dp0workspace_ew
echo ============================================================
echo  Run 031: sea states along the westbound Mindelo -^> BVI tracks
echo  Expected time: about 10-20 minutes. Started %date% %time%
echo ============================================================
if exist ..\results\seastates_ew024_mindelo__bvi_s.json (echo   already finished, skipping) else (
  .venv\Scripts\python.exe ..\collab\seastates_along_tracks.py ..\results\ew024_2023+2024_mindelo__bvi_s.json ..\results\seastates_ew024_mindelo__bvi_s.json > ..\collab\run_log_031_seastates_ew.txt 2>&1
  type ..\collab\run_log_031_seastates_ew.txt
)
echo Finished %date% %time%
