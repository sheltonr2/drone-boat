@echo off
REM Destination study, second batch (12 Nov 2026): seven more aim points and routes, to fill the gaps in the first six.
REM Rev C5, corrected simulator, 150 voyages per destination, 2023 weather, near-coast launch. About 6 hours.
REM Any landfall in Europe, Madeira, the Canaries or north-west Africa counts as across (not the Azores). docs/Destination_Study.md
cd /d "%~dp0"
echo ============================================================
echo  Destination study, batch 2: 7 destinations x 150 voyages
echo  Biscay, West Ireland, Hebrides, Cadiz, Morocco, Canaries by the northern arc, Azores
echo  Expected time: about 6 hours. Progress shows below.
echo  Started %date% %time%
echo ============================================================
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set LOG=..\collab\run_log_destinations2_2023.txt
echo Destination study batch 2, started %date% %time% > "%LOG%"
echo.
echo DESTINATION 1 of 7: biscay
echo ==== DESTINATION: biscay ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\biscay.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_biscay.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_biscay.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_biscay.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 2 of 7: ireland_west
echo ==== DESTINATION: ireland_west ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\ireland_west.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_ireland_west.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_ireland_west.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_ireland_west.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 3 of 7: hebrides
echo ==== DESTINATION: hebrides ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\hebrides.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_hebrides.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_hebrides.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_hebrides.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 4 of 7: cadiz
echo ==== DESTINATION: cadiz ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\cadiz.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_cadiz.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_cadiz.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_cadiz.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 5 of 7: morocco
echo ==== DESTINATION: morocco ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\morocco.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_morocco.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_morocco.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_morocco.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 6 of 7: canaries_arc
echo ==== DESTINATION: canaries_arc ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\canaries_arc.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_canaries_arc.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_canaries_arc.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_canaries_arc.json >> "%LOG%" 2>&1
echo.
echo DESTINATION 7 of 7: azores
echo ==== DESTINATION: azores ==== >> "%LOG%"
.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revC5_design.json --scenario ..\collab\destinations\azores.json --runs 150 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\dest_2023_azores.json >> "%LOG%" 2>&1
if exist ..\results\dest_2023_azores.json .venv\Scripts\python.exe ..\collab\summarize_mc.py ..\results\dest_2023_azores.json >> "%LOG%" 2>&1
echo === DONE %date% %time% >> "%LOG%"
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo  Upload this file to Claude:  collab\run_log_destinations2_2023.txt
echo ============================================================
pause
