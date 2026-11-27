@echo off
REM Run 043b part 2: BVI holds upwind, Mindelo launch windows
REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_043b2_ew.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ------------------------------------------------------------
echo  Run 043b part 2: BVI holds upwind, Mindelo launch windows: 11 runs
echo ------------------------------------------------------------
echo Run 043b part 2: BVI holds upwind, Mindelo launch windows, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 11: BVI hold norman_offing_E20   (started !time!)
if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_E20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_E20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_E20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_norman_offing_E20.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043b_2022-2025_revE3_station_norman_offing_E20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_E20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2022-2025_revE3_station_norman_offing_E20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_E20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 2 of 11: BVI hold norman_offing_E40   (started !time!)
if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_E40_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_E40 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_E40 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_norman_offing_E40.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043b_2022-2025_revE3_station_norman_offing_E40_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_E40_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2022-2025_revE3_station_norman_offing_E40_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_E40_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 3 of 11: BVI hold norman_offing_ESE20   (started !time!)
if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_ESE20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_ESE20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_ESE20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_norman_offing_ESE20.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043b_2022-2025_revE3_station_norman_offing_ESE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_ESE20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2022-2025_revE3_station_norman_offing_ESE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_norman_offing_ESE20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 4 of 11: BVI hold anegada_west_N15   (started !time!)
if exist ..\results\hold043b_2022-2025_revE3_station_anegada_west_N15_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold anegada_west_N15 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold anegada_west_N15 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_anegada_west_N15.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043b_2022-2025_revE3_station_anegada_west_N15_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_anegada_west_N15_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2022-2025_revE3_station_anegada_west_N15_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_anegada_west_N15_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 5 of 11: BVI hold anegada_west_N30   (started !time!)
if exist ..\results\hold043b_2022-2025_revE3_station_anegada_west_N30_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold anegada_west_N30 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold anegada_west_N30 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043b\hold_station_anegada_west_N30.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043b_2022-2025_revE3_station_anegada_west_N30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_anegada_west_N30_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043b_2022-2025_revE3_station_anegada_west_N30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043b_2022-2025_revE3_station_anegada_west_N30_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 6 of 11: Mindelo -> norman_offing, launches nov   (started !time!)
if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> norman_offing, launches nov already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> norman_offing, launches nov ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__norman_offing.json --runs 1000 --from 2021-11-15 --to 2021-12-10 --years 2021,2022,2023,2024 --out ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 7 of 11: Mindelo -> norman_offing, launches dec   (started !time!)
if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> norman_offing, launches dec already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> norman_offing, launches dec ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__norman_offing.json --runs 1000 --from 2021-12-11 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 8 of 11: Mindelo -> norman_offing, launches jan   (started !time!)
if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> norman_offing, launches jan already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> norman_offing, launches jan ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__norman_offing.json --runs 1000 --from 2022-01-11 --to 2022-02-05 --years 2022,2023,2024,2025 --out ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__norman_offing_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 9 of 11: Mindelo -> anegada_west, launches nov   (started !time!)
if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> anegada_west, launches nov already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> anegada_west, launches nov ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__anegada_west.json --runs 1000 --from 2021-11-15 --to 2021-12-10 --years 2021,2022,2023,2024 --out ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_nov__anegada_west_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 10 of 11: Mindelo -> anegada_west, launches dec   (started !time!)
if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> anegada_west, launches dec already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> anegada_west, launches dec ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__anegada_west.json --runs 1000 --from 2021-12-11 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_dec__anegada_west_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo.
echo RUN 11 of 11: Mindelo -> anegada_west, launches jan   (started !time!)
if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo -> anegada_west, launches jan already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo -> anegada_west, launches jan ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_043a\ew_mindelo__anegada_west.json --runs 1000 --from 2022-01-11 --to 2022-02-05 --years 2022,2023,2024,2025 --out ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043b_2021-2024_revE3_mindelo_jan__anegada_west_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043b2_ew.txt)
)
echo === DONE %date% %time% >> "%LOG%"
endlocal
