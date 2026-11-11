@echo off
REM Switches the run queue off: removes the scheduled task. Request files and logs are left in place.
schtasks /delete /tn "DroneBoatRunQueue" /f
echo.
echo The run queue is off. Nothing will be started automatically any more.
pause
