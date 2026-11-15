@echo off
REM East-west screen: 6 launch points to the BVI, launches 1 Nov to 15 Jan, 2024-25 weather (docs/East_West_Study.md). Written by collab/east_west/make_ew.py.
REM 9 runs of 300 voyages, launches 2024-11-01 to 2025-01-15, weather seasons from 2024, design revE1_design.json. About 3 h 00 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  East-west screen: 6 launch points to the BVI, launches 1 Nov to 15 Jan, 2024-25 weather
echo  9 runs x 300 voyages. Expected time: about 3 h 00 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_ew_screen.txt
REM Westbound weather (tropical box, winter months) lives in its own cache.
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo East-west screen: 6 launch points to the BVI, launches 1 Nov to 15 Jan, 2024-25 weather, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 9: gran_canaria__bvi   (started %time%)
if exist ..\results\ew_2024_gran_canaria__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_gran_canaria__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 2 of 9: gran_canaria_south__bvi   (started %time%)
if exist ..\results\ew_2024_gran_canaria_south__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria_south__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria_south__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria_south__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_gran_canaria_south__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria_south__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria_south__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria_south__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria_south__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria_south__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria_south__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 3 of 9: el_hierro__bvi   (started %time%)
if exist ..\results\ew_2024_el_hierro__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: el_hierro__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: el_hierro__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\el_hierro__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_el_hierro__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_el_hierro__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_el_hierro__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_el_hierro__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_el_hierro__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_el_hierro__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_el_hierro__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 4 of 9: mindelo__bvi   (started %time%)
if exist ..\results\ew_2024_mindelo__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: mindelo__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: mindelo__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\mindelo__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_mindelo__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_mindelo__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_mindelo__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_mindelo__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_mindelo__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_mindelo__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_mindelo__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 5 of 9: madeira__bvi   (started %time%)
if exist ..\results\ew_2024_madeira__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: madeira__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: madeira__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\madeira__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_madeira__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_madeira__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_madeira__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_madeira__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_madeira__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_madeira__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_madeira__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 6 of 9: cadiz__bvi   (started %time%)
if exist ..\results\ew_2024_cadiz__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: cadiz__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: cadiz__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\cadiz__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_cadiz__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_cadiz__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_cadiz__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_cadiz__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_cadiz__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_cadiz__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_cadiz__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 7 of 9: lisbon__bvi   (started %time%)
if exist ..\results\ew_2024_lisbon__bvi.json (
  echo   already finished, skipping
  echo ==== RUN: lisbon__bvi already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: lisbon__bvi ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\lisbon__bvi.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_lisbon__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_lisbon__bvi.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_lisbon__bvi.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_lisbon__bvi.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_lisbon__bvi.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_lisbon__bvi_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_lisbon__bvi.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 8 of 9: gran_canaria__bvi_weedx2   (started %time%)
if exist ..\results\ew_2024_gran_canaria__bvi_weedx2.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__bvi_weedx2 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__bvi_weedx2 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__bvi_weedx2.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_gran_canaria__bvi_weedx2.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__bvi_weedx2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__bvi_weedx2.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__bvi_weedx2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__bvi_weedx2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__bvi_weedx2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__bvi_weedx2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 9 of 9: gran_canaria__barbados   (started %time%)
if exist ..\results\ew_2024_gran_canaria__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__barbados.json --runs 300 --from 2024-11-01 --to 2025-01-15 --years 2024 --out ..\results\ew_2024_gran_canaria__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\ew_2024_*.json   Log: collab\run_log_ew_screen.txt
echo ============================================================
pause
