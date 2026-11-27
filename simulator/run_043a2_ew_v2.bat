@echo off
REM Run 043a part 2: Mindelo and El Hierro to the BVI points, and BVI holds, on the v2 coasts
REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_043a2_ew_v2.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ------------------------------------------------------------
echo  Run 043a part 2: Mindelo and El Hierro to the BVI points, and BVI holds, on the v2 coasts: 7 runs
echo ------------------------------------------------------------
echo Run 043a part 2: Mindelo and El Hierro to the BVI points, and BVI holds, on the v2 coasts, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 7: Mindelo -> norman_offing   (started !time!)
if exist ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__norman_offing.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo.
echo RUN 2 of 7: Mindelo -> anegada_west   (started !time!)
if exist ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> anegada_west already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> anegada_west ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__anegada_west.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo.
echo RUN 3 of 7: El Hierro via 20N 28W -> norman_offing   (started !time!)
if exist ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: El Hierro via 20N 28W -> norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: El Hierro via 20N 28W -> norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_el_hierro_south__norman_offing.json --runs 1000 --from 2021-11-01 --to 2021-12-20 --years 2021,2022,2023,2024 --out ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo.
echo RUN 4 of 7: BVI hold station_norman_offing   (started !time!)
if exist ..\results\hold043a_2022-2025_revE3_station_norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold station_norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold station_norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_station_norman_offing.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043a_2022-2025_revE3_station_norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_station_norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2022-2025_revE3_station_norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_station_norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo.
echo RUN 5 of 7: BVI hold drift_norman_offing   (started !time!)
if exist ..\results\hold043a_2022-2025_revE3_drift_norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold drift_norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold drift_norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_drift_norman_offing.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043a_2022-2025_revE3_drift_norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_drift_norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2022-2025_revE3_drift_norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_drift_norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo.
echo RUN 6 of 7: BVI hold station_anegada_west   (started !time!)
if exist ..\results\hold043a_2022-2025_revE3_station_anegada_west_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold station_anegada_west already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold station_anegada_west ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_station_anegada_west.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043a_2022-2025_revE3_station_anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_station_anegada_west_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2022-2025_revE3_station_anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_station_anegada_west_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo.
echo RUN 7 of 7: BVI hold drift_anegada_west   (started !time!)
if exist ..\results\hold043a_2022-2025_revE3_drift_anegada_west_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold drift_anegada_west already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold drift_anegada_west ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\hold_drift_anegada_west.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043a_2022-2025_revE3_drift_anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_drift_anegada_west_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043a_2022-2025_revE3_drift_anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043a_2022-2025_revE3_drift_anegada_west_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043a2_ew_v2.txt)
)
echo === DONE %date% %time% >> "%LOG%"
endlocal
