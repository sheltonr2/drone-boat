@echo off
REM Run 043a: the decided plans on the v2 coastlines (EMODnet + UKHO depth data), four years of weather already
REM on the PC. About 11 hours: part 1 eastbound (10 runs, about 8 h), part 2 east-west (7 runs, about 3 h).
cd /d "%~dp0"
echo ============================================================
echo  Run 043a: decided plans on the v2 coastlines, 17 runs, about 11 hours
echo  Part 1 eastbound (about 8 h), then part 2 east-west (about 3 h). Started %date% %time%
echo  Logs: collab\run_log_043a1_east_v2.txt and collab\run_log_043a2_ew_v2.txt
echo ============================================================
call run_043a1_east_v2.bat
call run_043a2_ew_v2.bat
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo ============================================================
