@echo off
REM Destination study (12 Nov 2026): which aim point across the Atlantic gets the most boats there?
REM Rev C5, corrected simulator, 150 voyages per destination, 2023 weather, near-coast launch. About 5 hours.
REM Any landfall in Europe, Madeira, the Canaries or north-west Africa counts as across (not the Azores). docs/Destination_Study.md
cd /d "%~dp0"
echo ============================================================
echo  Destination study: 6 destinations x 150 voyages, 2023 weather
echo  Ireland, Cornwall, Brittany, Galicia, Portugal, Canary Islands
echo  Expected time: about 5 hours. Progress shows below.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_destinations_2023.txt
echo Destination study 2023, started %date% %time% > "%LOG%"
echo.
echo DESTINATION 1 of 6: ireland_sw
echo ==== DESTINATION: ireland_sw ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\ireland_sw.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_ireland_sw.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_ireland_sw.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_ireland_sw.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 2 of 6: cornwall
echo ==== DESTINATION: cornwall ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\cornwall.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_cornwall.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_cornwall.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_cornwall.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 3 of 6: brittany
echo ==== DESTINATION: brittany ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\brittany.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_brittany.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_brittany.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_brittany.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 4 of 6: galicia
echo ==== DESTINATION: galicia ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\galicia.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_galicia.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_galicia.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_galicia.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 5 of 6: portugal
echo ==== DESTINATION: portugal ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\portugal.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_portugal.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_portugal.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_portugal.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 6 of 6: canaries
echo ==== DESTINATION: canaries ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\canaries.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_canaries.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_canaries.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_canaries.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Upload this file to Claude:  collab\run_log_destinations_2023.txt
echo ============================================================
pause
