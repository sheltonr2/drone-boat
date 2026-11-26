@echo off
REM Run 038: BVI pickup points, the crossing: Mindelo -> 7 candidates over four winters (detailed coast)
REM Rev E3, launches 15 Nov-10 Jan of winters 2021-22 to 2024-25, the same seeds for every candidate. Storm check after each.
REM 7 runs, about 6 h 00 min. Written by collab/runs_036/make_runs.py (26 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_038_ew_pickups.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ============================================================
echo  Run 038: BVI pickup points, the crossing: Mindelo -> 7 candidates over four winters (detailed coast)
echo  7 runs. Expected time: about 6 h 00 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 038: BVI pickup points, the crossing: Mindelo -> 7 candidates over four winters (detailed coast), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 7: norman   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__norman.json (
  echo   already finished, skipping
  echo ==== RUN: norman already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: norman ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__norman.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__norman.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__norman.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__norman.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__norman.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__norman.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__norman_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__norman.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo.
echo RUN 2 of 7: norman_offing   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json (
  echo   already finished, skipping
  echo ==== RUN: norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__norman_offing.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__norman_offing_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__norman_offing.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo.
echo RUN 3 of 7: ginger_se   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json (
  echo   already finished, skipping
  echo ==== RUN: ginger_se already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: ginger_se ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__ginger_se.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__ginger_se_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__ginger_se.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo.
echo RUN 4 of 7: jvd_north   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json (
  echo   already finished, skipping
  echo ==== RUN: jvd_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: jvd_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__jvd_north.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__jvd_north_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__jvd_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo.
echo RUN 5 of 7: anegada_west   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json (
  echo   already finished, skipping
  echo ==== RUN: anegada_west already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: anegada_west ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__anegada_west.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__anegada_west_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_west.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo.
echo RUN 6 of 7: anegada_north   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json (
  echo   already finished, skipping
  echo ==== RUN: anegada_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: anegada_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__anegada_north.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__anegada_north_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__anegada_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo.
echo RUN 7 of 7: stcroix_north   (started !time!)
if exist ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json (
  echo   already finished, skipping
  echo ==== RUN: stcroix_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: stcroix_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\ew_mindelo__stcroix_north.json --runs 1000 --from 2021-11-15 --to 2022-01-10 --years 2021,2022,2023,2024 --out ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json .venv\Scripts\python.exe -m drone_sim.cli stormcheck --mc ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json --storm-csv ..\docs\data\hurdat2_atlantic_1981-2025_tropics.csv --out ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north_storms.json >> "%LOG%" 2>&1
  if exist ..\results\ew038_2021-2024_revE3_mindelo__stcroix_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_038_ew_pickups.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_038_ew_pickups.txt
echo ============================================================
