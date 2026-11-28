@echo off
REM Run 043c part 2: BVI holds fine-tuned, Mindelo to the upwind points
REM Written by collab/runs_043a/make_runs.py (26 Nov 2026). A run whose result exists is skipped.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_043c2_ew.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ------------------------------------------------------------
echo  Run 043c part 2: BVI holds fine-tuned, Mindelo to the upwind points: 10 runs
echo ------------------------------------------------------------
echo Run 043c part 2: BVI holds fine-tuned, Mindelo to the upwind points, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 10: BVI hold norman_offing_ESE20   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_ESE20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_ESE20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043b\hold_station_norman_offing_ESE20.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 2 of 10: BVI hold norman_offing_E30   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_E30_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_E30 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_E30 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_norman_offing_E30.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_norman_offing_E30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_E30_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_norman_offing_E30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_E30_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 3 of 10: BVI hold norman_offing_ESE30   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE30_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_ESE30 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_ESE30 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_norman_offing_ESE30.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE30_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE30_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 4 of 10: BVI hold norman_offing_ESE40   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE40_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_ESE40 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_ESE40 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_norman_offing_ESE40.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE40_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE40_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE40_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_ESE40_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 5 of 10: BVI hold norman_offing_SE20   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_SE20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_SE20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_SE20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_norman_offing_SE20.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_norman_offing_SE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_SE20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_norman_offing_SE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_SE20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 6 of 10: BVI hold norman_offing_SE40   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_SE40_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold norman_offing_SE40 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold norman_offing_SE40 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_norman_offing_SE40.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_norman_offing_SE40_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_SE40_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_norman_offing_SE40_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_norman_offing_SE40_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 7 of 10: BVI hold anegada_west_N45   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_anegada_west_N45_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold anegada_west_N45 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold anegada_west_N45 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_anegada_west_N45.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_anegada_west_N45_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_anegada_west_N45_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_anegada_west_N45_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_anegada_west_N45_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 8 of 10: BVI hold anegada_west_NE30   (started !time!)
if exist ..\results\hold043c_2022-2025_revF_station_anegada_west_NE30_v2.json (
  echo   already finished, skipping
  echo ==== RUN: BVI hold anegada_west_NE30 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: BVI hold anegada_west_NE30 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\hold_station_anegada_west_NE30.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold043c_2022-2025_revF_station_anegada_west_NE30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_anegada_west_NE30_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold043c_2022-2025_revF_station_anegada_west_NE30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\hold043c_2022-2025_revF_station_anegada_west_NE30_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 9 of 10: Mindelo 15 Nov-10 Dec -> norman_offing_ESE20   (started !time!)
if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo 15 Nov-10 Dec -> norman_offing_ESE20 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo 15 Nov-10 Dec -> norman_offing_ESE20 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\ew_mindelo__norman_offing_ESE20.json --runs 1000 --from 2021-11-15 --to 2021-12-10 --years 2021,2022,2023,2024 --out ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__norman_offing_ESE20_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo.
echo RUN 10 of 10: Mindelo 15 Nov-10 Dec -> anegada_west_N30   (started !time!)
if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json (
  echo   already finished, skipping
  echo ==== RUN: Mindelo 15 Nov-10 Dec -> anegada_west_N30 already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: Mindelo 15 Nov-10 Dec -> anegada_west_N30 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revF_design.json --scenario ..\collab\runs_043c\ew_mindelo__anegada_west_N30.json --runs 1000 --from 2021-11-15 --to 2021-12-10 --years 2021,2022,2023,2024 --out ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json >> "%LOG%" 2>&1
  if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew043c_2021-2024_revF_mindelo_nov__anegada_west_N30_v2.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_043c2_ew.txt)
)
echo === DONE %date% %time% >> "%LOG%"
endlocal
