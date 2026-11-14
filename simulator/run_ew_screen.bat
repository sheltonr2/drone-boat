@echo off
REM East-west screen: 6 launch points, 6 destinations, launches 20 Nov to 10 Feb, 2024-25 weather (docs/East_West_Study.md). Written by collab/east_west/make_ew.py.
REM 12 runs of 300 voyages, launches 2024-11-20 to 2025-02-10, weather seasons from 2024, design revE1_design.json. About 4 h 00 min.
REM A run that already has its result file is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ============================================================
echo  East-west screen: 6 launch points, 6 destinations, launches 20 Nov to 10 Feb, 2024-25 weather
echo  12 runs x 300 voyages. Expected time: about 4 h 00 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_ew_screen.txt
REM Westbound weather (tropical box, winter months) lives in its own cache.
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo East-west screen: 6 launch points, 6 destinations, launches 20 Nov to 10 Feb, 2024-25 weather, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 12: gran_canaria__barbados   (started %time%)
if exist ..\results\ew_2024_gran_canaria__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 2 of 12: gran_canaria_south__barbados   (started %time%)
if exist ..\results\ew_2024_gran_canaria_south__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria_south__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria_south__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria_south__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria_south__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria_south__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria_south__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria_south__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria_south__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria_south__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria_south__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 3 of 12: gran_canaria__st_lucia   (started %time%)
if exist ..\results\ew_2024_gran_canaria__st_lucia.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__st_lucia already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__st_lucia ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__st_lucia.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria__st_lucia.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__st_lucia.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__st_lucia.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__st_lucia.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__st_lucia.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__st_lucia_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__st_lucia.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 4 of 12: gran_canaria__martinique   (started %time%)
if exist ..\results\ew_2024_gran_canaria__martinique.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__martinique already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__martinique ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__martinique.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria__martinique.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__martinique.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__martinique.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__martinique.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__martinique.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__martinique_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__martinique.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 5 of 12: gran_canaria__antigua   (started %time%)
if exist ..\results\ew_2024_gran_canaria__antigua.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__antigua already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__antigua ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__antigua.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria__antigua.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__antigua.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__antigua.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__antigua.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__antigua.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__antigua_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__antigua.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 6 of 12: gran_canaria__puerto_rico   (started %time%)
if exist ..\results\ew_2024_gran_canaria__puerto_rico.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__puerto_rico already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__puerto_rico ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__puerto_rico.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria__puerto_rico.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__puerto_rico.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__puerto_rico.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__puerto_rico.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__puerto_rico.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__puerto_rico_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__puerto_rico.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 7 of 12: el_hierro__barbados   (started %time%)
if exist ..\results\ew_2024_el_hierro__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: el_hierro__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: el_hierro__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\el_hierro__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_el_hierro__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_el_hierro__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_el_hierro__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_el_hierro__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_el_hierro__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_el_hierro__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_el_hierro__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 8 of 12: mindelo__barbados   (started %time%)
if exist ..\results\ew_2024_mindelo__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: mindelo__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: mindelo__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\mindelo__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_mindelo__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_mindelo__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_mindelo__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_mindelo__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_mindelo__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_mindelo__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_mindelo__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 9 of 12: madeira__barbados   (started %time%)
if exist ..\results\ew_2024_madeira__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: madeira__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: madeira__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\madeira__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_madeira__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_madeira__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_madeira__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_madeira__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_madeira__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_madeira__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_madeira__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 10 of 12: cadiz__barbados   (started %time%)
if exist ..\results\ew_2024_cadiz__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: cadiz__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: cadiz__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\cadiz__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_cadiz__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_cadiz__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_cadiz__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_cadiz__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_cadiz__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_cadiz__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_cadiz__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 11 of 12: lisbon__barbados   (started %time%)
if exist ..\results\ew_2024_lisbon__barbados.json (
  echo   already finished, skipping
  echo ==== RUN: lisbon__barbados already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: lisbon__barbados ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\lisbon__barbados.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_lisbon__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_lisbon__barbados.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_lisbon__barbados.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_lisbon__barbados.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_lisbon__barbados.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_lisbon__barbados_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_lisbon__barbados.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo.
echo RUN 12 of 12: gran_canaria__barbados_weedx2   (started %time%)
if exist ..\results\ew_2024_gran_canaria__barbados_weedx2.json (
  echo   already finished, skipping
  echo ==== RUN: gran_canaria__barbados_weedx2 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: gran_canaria__barbados_weedx2 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\east_west\gran_canaria__barbados_weedx2.json --runs 300 --from 2024-11-20 --to 2025-02-10 --years 2024 --out ..\results\ew_2024_gran_canaria__barbados_weedx2.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados_weedx2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew_2024_gran_canaria__barbados_weedx2.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados_weedx2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew_2024_gran_canaria__barbados_weedx2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew_2024_gran_canaria__barbados_weedx2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew_2024_gran_canaria__barbados_weedx2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_ew_screen.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Results: results\ew_2024_*.json   Log: collab\run_log_ew_screen.txt
echo ============================================================
pause
