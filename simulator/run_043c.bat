@echo off
REM Run 043c: Rev F baseline, BVI holds fine-tuned, Mindelo to the upwind points, B90 checks.
REM About 6 hours: part 1 eastbound (5 runs, about 3 h), part 2 east-west (10 runs, about 3 h).
cd /d "%~dp0"
echo ============================================================
echo  Run 043c: Rev F baseline, BVI holds, Mindelo, B90 checks - 15 runs, about 6 hours
echo  Part 1 eastbound (about 3 h), then part 2 east-west (about 3 h). Started %date% %time%
echo  Logs: collab\run_log_043c1_east.txt and collab\run_log_043c2_ew.txt
echo ============================================================
call run_043c1_east.bat
call run_043c2_ew.bat
echo.
echo ============================================================
echo  ALL DONE %date% %time%
echo ============================================================
