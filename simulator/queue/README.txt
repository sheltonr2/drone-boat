Run queue (see ..\setup_run_queue.bat)

A request is a file here ending in .run whose single line is the name of a batch file in the simulator folder,
for example:   run_revC5_2023.bat
Every 5 minutes run_queue.bat takes the first request, moves it to done\, and runs that batch file.
Only names of the form run_<letters, digits, _ or ->.bat are accepted; anything else goes to rejected\.
One run at a time: running.lock exists while a run is going. If the PC was switched off mid-run and the lock is
stale, put a file called unlock.run here to clear it.
queue_log.txt records every start, finish and rejection.
