@echo off
REM Run 036: BVI pickup points, holding: station-keeping and dead-boat drift at 7 candidates (detailed coast)
REM Boats start at each candidate between 1 Feb and 30 Apr, 2022-2025: 14 days holding within 1 km, or 30 days drifting dead.
REM 14 runs, about 1 h 10 min. Written by collab/runs_036/make_runs.py (26 Nov 2026).
REM A run whose result file exists is skipped, so this file can be restarted after a reboot.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_036_hold_bvi.txt
set DRONE_SIM_HOME=%~dp0workspace_ew
if not exist workspace_ew\cache mkdir workspace_ew\cache
for %%f in (workspace\cache\*.*) do if not exist "workspace_ew\cache\%%~nxf" copy /y "%%f" "workspace_ew\cache\" >nul
echo ============================================================
echo  Run 036: BVI pickup points, holding: station-keeping and dead-boat drift at 7 candidates (detailed coast)
echo  14 runs. Expected time: about 1 h 10 min.
echo  Progress shows below, one line per run. Started %date% %time%
echo ============================================================
echo Run 036: BVI pickup points, holding: station-keeping and dead-boat drift at 7 candidates (detailed coast), started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 14: station_norman   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_norman.json (
  echo   already finished, skipping
  echo ==== RUN: station_norman already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_norman ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_norman.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_norman.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_norman.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_norman.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_norman.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 2 of 14: drift_norman   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_norman.json (
  echo   already finished, skipping
  echo ==== RUN: drift_norman already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_norman ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_norman.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_norman.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_norman.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_norman.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_norman.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 3 of 14: station_norman_offing   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_norman_offing.json (
  echo   already finished, skipping
  echo ==== RUN: station_norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_norman_offing.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_norman_offing.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_norman_offing.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_norman_offing.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_norman_offing.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 4 of 14: drift_norman_offing   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_norman_offing.json (
  echo   already finished, skipping
  echo ==== RUN: drift_norman_offing already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_norman_offing ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_norman_offing.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_norman_offing.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_norman_offing.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_norman_offing.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_norman_offing.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 5 of 14: station_ginger_se   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_ginger_se.json (
  echo   already finished, skipping
  echo ==== RUN: station_ginger_se already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_ginger_se ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_ginger_se.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_ginger_se.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_ginger_se.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_ginger_se.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_ginger_se.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 6 of 14: drift_ginger_se   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_ginger_se.json (
  echo   already finished, skipping
  echo ==== RUN: drift_ginger_se already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_ginger_se ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_ginger_se.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_ginger_se.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_ginger_se.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_ginger_se.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_ginger_se.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 7 of 14: station_jvd_north   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_jvd_north.json (
  echo   already finished, skipping
  echo ==== RUN: station_jvd_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_jvd_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_jvd_north.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_jvd_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_jvd_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_jvd_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_jvd_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 8 of 14: drift_jvd_north   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_jvd_north.json (
  echo   already finished, skipping
  echo ==== RUN: drift_jvd_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_jvd_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_jvd_north.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_jvd_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_jvd_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_jvd_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_jvd_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 9 of 14: station_anegada_west   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_anegada_west.json (
  echo   already finished, skipping
  echo ==== RUN: station_anegada_west already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_anegada_west ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_anegada_west.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_anegada_west.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_anegada_west.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_anegada_west.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_anegada_west.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 10 of 14: drift_anegada_west   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_anegada_west.json (
  echo   already finished, skipping
  echo ==== RUN: drift_anegada_west already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_anegada_west ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_anegada_west.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_anegada_west.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_anegada_west.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_anegada_west.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_anegada_west.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 11 of 14: station_anegada_north   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_anegada_north.json (
  echo   already finished, skipping
  echo ==== RUN: station_anegada_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_anegada_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_anegada_north.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_anegada_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_anegada_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_anegada_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_anegada_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 12 of 14: drift_anegada_north   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_anegada_north.json (
  echo   already finished, skipping
  echo ==== RUN: drift_anegada_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_anegada_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_anegada_north.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_anegada_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_anegada_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_anegada_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_anegada_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 13 of 14: station_stcroix_north   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_station_stcroix_north.json (
  echo   already finished, skipping
  echo ==== RUN: station_stcroix_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: station_stcroix_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_station_stcroix_north.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_station_stcroix_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_stcroix_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_station_stcroix_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_station_stcroix_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo.
echo RUN 14 of 14: drift_stcroix_north   (started !time!)
if exist ..\results\hold036_2022-2025_revE3_drift_stcroix_north.json (
  echo   already finished, skipping
  echo ==== RUN: drift_stcroix_north already finished, skipped ==== >> "%LOG%"
) else (
  echo ==== RUN: drift_stcroix_north ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE3_design.json --scenario ..\collab\runs_036\hold_drift_stcroix_north.json --runs 500 --from 2022-02-01 --to 2022-04-30 --years 2022,2023,2024,2025 --out ..\results\hold036_2022-2025_revE3_drift_stcroix_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_stcroix_north.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\hold036_2022-2025_revE3_drift_stcroix_north.json >> "%LOG%" 2>&1
  if exist ..\results\hold036_2022-2025_revE3_drift_stcroix_north.json (echo   finished !time!) else (echo   FAILED: see ..\collab\run_log_036_hold_bvi.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Log: collab\run_log_036_hold_bvi.txt
echo ============================================================
