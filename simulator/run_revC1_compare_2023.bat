@echo off
REM Rev C1 (electronics box above the flood level) from the near-coast launch, on the same 250 voyages
REM (2023 bulk data, 1 May - 15 June) as the Rev C run of 10 Nov. About 1 hour with all cores.
REM Run it after run_bulk.bat has finished. Log: ..\collab\run_log_revC1_compare_2023.txt
cd /d "%~dp0"
echo ============================================================
echo  Rev C1 comparison (250 voyages, 2023 weather)
echo  Expected time: about 1 hour. Progress shows below; details go to the log.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_revC1_compare_2023.txt
echo Rev C1 comparison 2023, started %date% %time% > "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC1_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revC1_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revC1_10km.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revC1_10km.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%"
echo Upload collab\run_log_revC1_compare_2023.txt
echo Finished %date% %time%
pause
