@echo off
REM Run queue: started every 5 minutes by the Windows scheduled task "DroneBoatRunQueue" (see setup_run_queue.bat).
REM It looks in the queue folder for a request file (*.run) whose one line names a batch file in THIS folder,
REM and runs it. Only names of the form run_<letters, digits, _ or ->.bat are accepted: no paths, no other commands.
REM One run at a time. Everything it does is written to queue\queue_log.txt.
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
if not exist queue mkdir queue
if not exist queue\done mkdir queue\done
if not exist queue\rejected mkdir queue\rejected
if exist queue\unlock.run del queue\running.lock 2>nul
if exist queue\unlock.run del queue\unlock.run
if exist queue\running.lock exit /b 0
set "REQ="
for %%F in (queue\*.run) do if not defined REQ set "REQ=%%~nxF"
if not defined REQ exit /b 0
set "TARGET="
set /p TARGET=<"queue\!REQ!"
if not defined TARGET goto :reject
echo(!TARGET!| findstr /r /x "run_[A-Za-z0-9_-]*\.bat" >nul
if errorlevel 1 goto :reject
if not exist "!TARGET!" goto :reject
echo ============================================================
echo  Run queue: starting !TARGET!
echo  (requested by queue\!REQ!, %date% %time%)
echo  You can keep using the PC. Closing this window stops the run.
echo ============================================================
echo %date% %time% STARTED !TARGET! (request !REQ!)>> queue\queue_log.txt
move /y "queue\!REQ!" "queue\done\!REQ!" >nul
echo !TARGET!> queue\running.lock
call "!TARGET!" < nul
cd /d "%~dp0"
del queue\running.lock 2>nul
echo %date% %time% FINISHED !TARGET!>> queue\queue_log.txt
exit /b 0
:reject
echo %date% %time% REJECTED request !REQ! (not a run_*.bat file in this folder)>> queue\queue_log.txt
move /y "queue\!REQ!" "queue\rejected\!REQ!" >nul
exit /b 1
