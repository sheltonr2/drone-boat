@echo off
REM Run 040c: re-fetch the UKHO Wrecks and Obstructions for the three coast boxes (about a minute).
REM In run 040 the polygon layer was saved under the same truncated file name as the point layer and replaced it;
REM fetch_depth_data.py now names each file by its service and layer id. Output: docs\data\coast\raw_040\
cd /d "%~dp0\.."
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=collab\run_log_040c_ukho_wrecks.txt
echo ============================================================
echo  Run 040c: UKHO Wrecks and Obstructions, re-fetch (about a minute)
echo  Started %date% %time%
echo ============================================================
echo Run 040c: UKHO wrecks re-fetch, started %date% %time% >> "%LOG%"
simulator\.venv-bulk\Scripts\python.exe docs\data\coast\fetch_depth_data.py --only wrecks --out docs\data\coast\raw_040 --log "%LOG%"
echo === DONE %date% %time% >> "%LOG%"
echo Finished %date% %time%
