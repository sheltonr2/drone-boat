@echo off
REM One-time setup: lets Claude start simulator runs on this PC without you at the keyboard.
cd /d "%~dp0"
echo ============================================================
echo  Drone boat run queue: one-time setup
echo.
echo  This creates a Windows scheduled task, "DroneBoatRunQueue",
echo  that runs run_queue.bat in this folder every 5 minutes.
echo  run_queue.bat starts a simulator batch file when a request
echo  file appears in the "queue" folder here.
echo.
echo  What that means: anything able to write files into this
echo  project folder can start the run_*.bat files in it.
echo  To switch it off again, double-click remove_run_queue.bat.
echo ============================================================
echo.
pause
if not exist queue mkdir queue
schtasks /create /tn "DroneBoatRunQueue" /sc minute /mo 5 /tr "\"%~dp0run_queue.bat\"" /f
if errorlevel 1 goto :failed
echo.
echo Set up. Starting the queue once now...
schtasks /run /tn "DroneBoatRunQueue"
echo.
echo Done. If a run was waiting in the queue, its window opens in a few seconds.
echo Notes: the PC must be on and awake, and you must be signed in (locked is fine).
echo        On a laptop, Windows only starts the task on mains power unless you change that
echo        in Task Scheduler (task "DroneBoatRunQueue", Conditions tab).
pause
exit /b 0
:failed
echo.
echo Windows refused to create the task. Tell Claude what it said above.
pause
