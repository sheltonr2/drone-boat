@echo off
REM One-time fix (13 Nov 2026): lets the "DroneBoatRunQueue" scheduled task start and keep running on battery.
REM Windows' default for a new task is to kill it when the laptop is unplugged, which is what killed the
REM launch-study run on 12 Nov. This changes only that task's power settings. Safe to run more than once.
cd /d "%~dp0"
echo ============================================================
echo  Drone boat run queue: keep running on battery
echo.
echo  Changes the "DroneBoatRunQueue" scheduled task so that
echo  unplugging the laptop no longer stops a run.
echo ============================================================
echo.
powershell -NoProfile -Command "$s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 3); Set-ScheduledTask -TaskName 'DroneBoatRunQueue' -Settings $s | Out-Null; $t = Get-ScheduledTask -TaskName 'DroneBoatRunQueue'; 'Stops on battery:   ' + $t.Settings.StopIfGoingOnBatteries; 'Blocked on battery: ' + $t.Settings.DisallowStartIfOnBatteries"
if errorlevel 1 goto :failed
echo.
echo Done. Both lines above should say False.
echo Also: the simulator now keeps the laptop from sleeping while a run is going,
echo on mains or battery. Closing the lid still sleeps it unless the lid setting
echo (Control Panel, Power Options, "Choose what closing the lid does") is "Do nothing".
echo A run paused by sleep carries on when the laptop wakes; it is not lost.
pause
exit /b 0
:failed
echo.
echo Windows refused the change. Right-click this file and choose "Run as administrator",
echo or tell Claude what it said above.
pause
exit /b 1
