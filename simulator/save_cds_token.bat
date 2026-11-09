@echo off
REM Saves your Climate Data Store API token from the clipboard to %USERPROFILE%\.cdsapirc
REM (the token is never shown on screen), then checks CDS access.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo First copy your API token from https://cds.climate.copernicus.eu/profile (the "API Token" box).
echo Reading it from the clipboard now ...
powershell -NoProfile -Command "Get-Clipboard -Raw" | .venv-bulk\Scripts\python.exe -c "import sys,re,os; t=sys.stdin.read().strip(); ok=re.fullmatch(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', t); p=os.path.join(os.path.expanduser('~'),'.cdsapirc'); (open(p,'w').write('url: https://cds.climate.copernicus.eu/api\nkey: '+t+'\n'), print('Saved the token to', p)) if ok else (print('The clipboard does not hold a CDS API token (36 characters like 1a2b3c4d-5e6f-...). Copy it from your CDS profile page and run this again.'), sys.exit(1))"
if errorlevel 1 (
  pause
  exit /b 1
)
echo.
echo Checking CDS access (one tiny request) ...
.venv-bulk\Scripts\python.exe -m drone_sim.cli cdscheck > ..\collab\cds_check.txt 2>&1
type ..\collab\cds_check.txt
echo.
echo If the last line says "CDS access is fine", double-click run_bulk.bat. Otherwise upload collab\cds_check.txt
pause
