@echo off
REM Keeps the run queue in a window you can see. Double-click it and leave it open (minimised is fine).
REM Every minute it checks the queue folder and starts any waiting run_*.bat here, in this window, with its
REM banner and progress. While this window is open the scheduled task "DroneBoatRunQueue" stands aside, so
REM runs are never hidden. Close the window and the scheduled task takes over again (hidden on some PCs).
title Drone boat run queue
setlocal EnableExtensions
cd /d "%~dp0"
if not exist queue mkdir queue
echo ============================================================
echo  Drone boat run queue (window)
echo  Checks the queue folder every minute and runs waiting jobs here.
echo  Leave this window open. Closing it stops a running job.
echo  Started %date% %time%
echo ============================================================
:loop
echo.> queue\window.lock
call run_queue.bat window
timeout /t 60 /nobreak >nul
goto :loop
