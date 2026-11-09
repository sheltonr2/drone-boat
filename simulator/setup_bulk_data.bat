@echo off
REM One-time setup for bulk weather data (see drone_sim\bulk.py).
REM  1. Makes a separate Python environment (.venv-bulk) with the download tools.
REM  2. Signs you in to Copernicus Marine (you type your username and password here; they stay on this PC).
REM  3. Saves your Climate Data Store API token to %USERPROFILE%\.cdsapirc (you paste it; it stays on this PC).
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYV=
for %%v in (3.13 3.12 3.14) do (
  if not defined PYV ( py -%%v -c "import sys" >nul 2>nul && set PYV=-%%v )
)
if defined PYV (echo Using Python %PYV:~1% for the download tools.) else (echo Using your default Python for the download tools.)
if not exist .venv-bulk\Scripts\python.exe (
  if defined PYV (py %PYV% -m venv .venv-bulk) else (python -m venv .venv-bulk)
)
.venv-bulk\Scripts\python.exe -m pip install -q --disable-pip-version-check numpy netCDF4 cdsapi copernicusmarine
if errorlevel 1 (
  echo.
  echo The download tools would not install on this Python version.
  echo Install Python 3.13 from https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^),
  echo delete the .venv-bulk folder, and run this file again.
  pause
  exit /b 1
)
echo.
echo === Step 1 of 2: Copernicus Marine sign-in ===
echo Type the username and password of the Copernicus Marine account you just made.
.venv-bulk\Scripts\copernicusmarine.exe login
echo.
echo === Step 2 of 2: Climate Data Store API token ===
echo Copy the API token from https://cds.climate.copernicus.eu/profile, then press a key here.
pause
call save_cds_token.bat
echo.
echo Remember: the ERA5 licence must be accepted once on the dataset's Download page
echo ("ERA5 hourly data on single levels from 1940 to present", Terms of use).
echo Setup done. Next: double-click run_bulk.bat
pause
