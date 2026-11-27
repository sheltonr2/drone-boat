@echo off
REM Run 043b: approaches further south of Scilly, holding upwind of the pickup points, Mindelo launch windows.
REM About 9 hours: part 1 eastbound (4 runs, about 2.5 h), part 2 east-west (11 runs, about 6.5 h).
cd /d "%~dp0"
echo ============================================================
echo  Run 043b: Scilly approaches, upwind holding, Mindelo launch windows - 15 runs, about 9 hours
echo  Part 1 eastbound (about 2.5 h), then part 2 east-west (about 6.5 h). Started %date% %time%
echo  Logs: collab\run_log_043b1_east.txt and collab\run_log_043b2_ew.txt
echo ============================================================
call run_043b1_east.bat
call run_043b2_ew.bat
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo ============================================================
