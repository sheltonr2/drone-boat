@echo off
REM Run 040: depth and hazard data for the detailed coastlines (docs/data/coast/fetch_depth_data.py).
REM Asked for by Randolph 26 Nov 2026 ("Add the UK and EMODnet depth data").
REM EMODnet Bathymetry DTM (~115 m, CC-BY) for west Cornwall, and UK Hydrographic Office open data (Open Government
REM Licence): Wrecks and Obstructions for Cornwall, the Virgin Islands and Hatteras, plus lists of the UKHO bathymetry
REM surveys that touch those areas. A few MB to a few hundred MB, minutes. Output: docs\data\coast\raw_040\
cd /d "%~dp0\.."
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=collab\run_log_040_depth_data.txt
echo ============================================================
echo  Run 040: EMODnet and UKHO depth and hazard data
echo  Expected time: a few minutes. Started %date% %time%
echo  Progress is shown below and kept in %LOG%
echo ============================================================
echo Run 040: depth and hazard data, started %date% %time% >> "%LOG%"
if not exist simulator\.venv-bulk\Scripts\python.exe (
  echo .venv-bulk is missing: run setup_bulk_data.bat first. >> "%LOG%"
  echo .venv-bulk is missing: run setup_bulk_data.bat first.
  exit /b 1
)
simulator\.venv-bulk\Scripts\python.exe docs\data\coast\fetch_depth_data.py --out docs\data\coast\raw_040 --log "%LOG%"
echo === DONE %date% %time% >> "%LOG%"
echo Finished %date% %time%
