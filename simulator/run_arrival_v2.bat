@echo off
REM Arrival study (docs/Launch_Plan.md "Arrival and holding"): Rev E1, 45 km off Hatteras -> a holding point,
REM Falmouth Bay and Mount's Bay, 500 voyages each, 2023+2024, the same launch dates and seeds as run 017.
REM About 80 min. A run whose result exists is skipped. Written by collab/arrival/make_arrival.py.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_arrival_v2.txt
echo ============================================================
echo  Arrival study: Hatteras to holding points offshore: the Lizard offing and the mouth of Mount's Bay
echo  2 runs x 500 voyages, about 80 minutes. Started %date% %time%
echo ============================================================
echo Arrival study, started %date% %time% >> "%LOG%"
echo.
echo RUN 1 of 2: lizard_offing_hold_v2   (started %time%)
if exist ..\results\arrival_2023+2024_revE1_hatteras_stream__lizard_offing_hold_v2.json (
  echo   already finished, skipping
) else (
  echo ==== RUN: lizard_offing_hold_v2 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\arrival\hatteras_stream__lizard_offing_hold_v2.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\arrival_2023+2024_revE1_hatteras_stream__lizard_offing_hold_v2.json >> "%LOG%" 2>&1
  if exist ..\results\arrival_2023+2024_revE1_hatteras_stream__lizard_offing_hold_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\arrival_2023+2024_revE1_hatteras_stream__lizard_offing_hold_v2.json >> "%LOG%" 2>&1
  if exist ..\results\arrival_2023+2024_revE1_hatteras_stream__lizard_offing_hold_v2.json (echo   finished %time%) else (echo   FAILED: see ..\collab\run_log_arrival_v2.txt)
)
echo.
echo RUN 2 of 2: mounts_bay_offing_hold_v2   (started %time%)
if exist ..\results\arrival_2023+2024_revE1_hatteras_stream__mounts_bay_offing_hold_v2.json (
  echo   already finished, skipping
) else (
  echo ==== RUN: mounts_bay_offing_hold_v2 ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revE1_design.json --scenario ..\collab\arrival\hatteras_stream__mounts_bay_offing_hold_v2.json --runs 500 --from 2023-05-01 --to 2023-06-15 --years 2023,2024 --out ..\results\arrival_2023+2024_revE1_hatteras_stream__mounts_bay_offing_hold_v2.json >> "%LOG%" 2>&1
  if exist ..\results\arrival_2023+2024_revE1_hatteras_stream__mounts_bay_offing_hold_v2.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\arrival_2023+2024_revE1_hatteras_stream__mounts_bay_offing_hold_v2.json >> "%LOG%" 2>&1
  if exist ..\results\arrival_2023+2024_revE1_hatteras_stream__mounts_bay_offing_hold_v2.json (echo   finished %time%) else (echo   FAILED: see ..\collab\run_log_arrival_v2.txt)
)
echo === DONE %date% %time% >> "%LOG%"
echo  ALL DONE %date% %time%
