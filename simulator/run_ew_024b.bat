@echo off
REM East-west run 024b: Gran Canaria and El Hierro via 20N 28W -> BVI, launches 1 Nov-20 Dec, two winters (docs/East_West_Study.md). Written by collab/east_west/make_ew.py.
REM 2 runs of 500 voyages, launches 2023-11-01 to 2023-12-20, weather seasons from 2023,2024, design revE1_design.json. About 1 h 04 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  East-west run 024b: Gran Canaria and El Hierro via 20N 28W -> BVI, launches 1 Nov-20 Dec, two winters
echo  2 runs x 500 voyages. Expected time: about 1 h 04 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_ew_024b.txt
REM Westbound weather (tropical box, winter months) lives in its own cache.
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo East-west run 024b: Gran Canaria and El Hierro via 20N 28W -> BVI, launches 1 Nov-20 Dec, two winters, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 2: gran_canaria_south__bvi_s   (started %time%)
if exist ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria_south__bvi_s already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria_south__bvi_s ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria_south__bvi_s.json --runs 500 --from 2023-11-01 --to 2023-12-20 --years 2023,2024 --out ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew024_2023+2024_gran_canaria_south__bvi_s_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew024_2023+2024_gran_canaria_south__bvi_s.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_024b.txt)
)
echo.
echo RUN 2 of 2: el_hierro_south__bvi_s   (started %time%)
if exist ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json (
  echo   already finished, skipping
  echo ==== RUN: el_hierro_south__bvi_s already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: el_hierro_south__bvi_s ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\el_hierro_south__bvi_s.json --runs 500 --from 2023-11-01 --to 2023-12-20 --years 2023,2024 --out ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew024_2023+2024_el_hierro_south__bvi_s_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew024_2023+2024_el_hierro_south__bvi_s.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_024b.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\ew024_2023+2024_*.json   Log: collab\run_log_ew_024b.txt
echo ============================================================
pause
