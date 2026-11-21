@echo off
REM Run 033: BVI backup on winters 2021-22 and 2022-23 (Mindelo, Gran Canaria south, El Hierro south)
REM Same set-up as run 024 (two winters) on two more; needs run 032's weather first. With 024 this gives four winters.
REM 3 runs, about 1 h 35 min. Written by collab/runs_026/make_runs.py (21 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_033_ew_two_more_winters.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ============================================================
echo  Run 033: BVI backup on winters 2021-22 and 2022-23 (Mindelo, Gran Canaria south, El Hierro south)
echo  3 runs. Expected time: about 1 h 35 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 033: BVI backup on winters 2021-22 and 2022-23 (Mindelo, Gran Canaria south, El Hierro south), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 3: mindelo__bvi_s   (started !time!)
if exist ..\results\ew033_2021+2022_mindelo__bvi_s.json (
  echo   already finished, skipping
  echo ==== RUN: mindelo__bvi_s already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: mindelo__bvi_s ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\mindelo__bvi_s.json --runs 500 --from 2021-11-15 --to 2022-01-10 --years 2021,2022 --out ..\results\ew033_2021+2022_mindelo__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_mindelo__bvi_s.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew033_2021+2022_mindelo__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_mindelo__bvi_s.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew033_2021+2022_mindelo__bvi_s.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew033_2021+2022_mindelo__bvi_s_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_mindelo__bvi_s.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_033_ew_two_more_winters.txt)
)
echo.
echo RUN 2 of 3: gran_canaria_south__bvi_s   (started !time!)
if exist ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria_south__bvi_s already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria_south__bvi_s ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria_south__bvi_s.json --runs 500 --from 2021-11-01 --to 2021-12-20 --years 2021,2022 --out ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew033_2021+2022_gran_canaria_south__bvi_s_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_gran_canaria_south__bvi_s.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_033_ew_two_more_winters.txt)
)
echo.
echo RUN 3 of 3: el_hierro_south__bvi_s   (started !time!)
if exist ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json (
  echo   already finished, skipping
  echo ==== RUN: el_hierro_south__bvi_s already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: el_hierro_south__bvi_s ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\el_hierro_south__bvi_s.json --runs 500 --from 2021-11-01 --to 2021-12-20 --years 2021,2022 --out ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew033_2021+2022_el_hierro_south__bvi_s_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew033_2021+2022_el_hierro_south__bvi_s.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_033_ew_two_more_winters.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_033_ew_two_more_winters.txt
echo ============================================================
