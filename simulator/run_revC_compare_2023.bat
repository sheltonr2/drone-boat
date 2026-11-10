@echo off
REM Rev C vs Rev B, and near-coast vs 100 km, on the 2023 bulk data with the refitted rates (10 Nov 2026).
REM 250 voyages each, same seeds, launched 1 May - 15 June 2023, all cores. About 1 hour per run, 3 runs.
REM   1. Rev C, near-coast launch (~10 km off Ocean City Inlet)   - the plan
REM   2. Rev B, near-coast launch                                  - what the design changes are worth
REM   3. Rev C, 100 km drop                                        - what the launch point is worth
REM It can run while run_bulk.bat is still downloading. Log: ..\collab\run_log_revC_compare_2023.txt
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_revC_compare_2023.txt
set PY=.venv\Scripts\python.exe
echo Rev C comparison 2023, started %date% %time% > "%LOG%"
echo === 1. REV C, NEAR-COAST >> "%LOG%"
%PY% -m drone_sim.cli mc --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revC_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revC_10km.json %PY% ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revC_10km.json >> "%LOG%" 2>&1
echo === 2. REV B, NEAR-COAST >> "%LOG%"
%PY% -m drone_sim.cli mc --design ..\designs\revB_design.json --scenario ..\collab\bulk_mc_2023_10km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revB_10km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revB_10km.json %PY% ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revB_10km.json >> "%LOG%" 2>&1
echo === 3. REV C, 100 km DROP >> "%LOG%"
%PY% -m drone_sim.cli mc --scenario ..\collab\bulk_mc_100km.json --runs 250 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\bulk_mc_2023_revC_100km.json >> "%LOG%" 2>&1
if exist ..\results\bulk_mc_2023_revC_100km.json %PY% ..\collab\summarize_mc.py ..\results\bulk_mc_2023_revC_100km.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
type "%LOG%"
echo Upload collab\run_log_revC_compare_2023.txt and the three results\bulk_mc_2023_rev*.json files
pause
