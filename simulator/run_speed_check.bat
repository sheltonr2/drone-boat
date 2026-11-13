@echo off
REM Speed-up check (13 Nov 2026). Runs the same 80 voyages (Rev D, 2023 real weather, two launch scenarios)
REM with the current simulator and with the faster one in speedup\drone_sim, and compares every field of the
REM results. ONLY if both comparisons are identical does it install the faster code (vpp.py, env.py) for
REM future runs. If anything differs, nothing is changed and the log says where. About 30 minutes.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set DRONE_SIM_HOME=%~dp0workspace
set LOG=..\collab\run_log_speed_check.txt
echo ============================================================
echo  Simulator speed-up check: old and new code, same 80 voyages
echo  Installs the faster code only if every result is identical.
echo  About 30 minutes. Started %date% %time%
echo ============================================================
echo Speed-up check, started %date% %time% > "%LOG%"
set PASS=1
for %%S in (canaveral__ireland_sw ocean_city__cornwall) do (
  echo.
  echo %%S: current code   ^(started !time!^)
  echo ==== %%S: current code, started !time! ==== >> "%LOG%"
  .venv\Scripts\python.exe -m drone_sim.cli mc --design ..\designs\revD_design.json --scenario ..\collab\launch_points\%%S.json --runs 40 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\results\speedcheck_old_%%S.json >> "%LOG%" 2>&1
  echo %%S: faster code    ^(started !time!^)
  echo ==== %%S: faster code, started !time! ==== >> "%LOG%"
  pushd speedup
  ..\.venv\Scripts\python.exe -m drone_sim.cli mc --design ..\..\designs\revD_design.json --scenario ..\..\collab\launch_points\%%S.json --runs 40 --from 2023-05-01 --to 2023-06-15 --years 2023 --out ..\..\results\speedcheck_new_%%S.json >> "..\%LOG%" 2>&1
  popd
  echo ==== %%S: finished !time! ==== >> "%LOG%"
  .venv\Scripts\python.exe tools\compare_results.py ..\results\speedcheck_old_%%S.json ..\results\speedcheck_new_%%S.json >> "%LOG%" 2>&1
  if errorlevel 1 (set PASS=0& echo   DIFFERENT: see collab\run_log_speed_check.txt) else (echo   identical)
)
echo.
if "%PASS%"=="1" (
  copy /Y speedup\drone_sim\vpp.py drone_sim\vpp.py >nul
  copy /Y speedup\drone_sim\env.py drone_sim\env.py >nul
  echo RESULT: PASS. Faster code installed for future runs, %date% %time% >> "%LOG%"
  echo RESULT: PASS. The faster code is now installed for future runs.
) else (
  echo RESULT: FAIL. Nothing installed; the simulator is unchanged, %date% %time% >> "%LOG%"
  echo RESULT: FAIL. Nothing was installed; the simulator is unchanged.
)
echo === DONE %date% %time% >> "%LOG%"
