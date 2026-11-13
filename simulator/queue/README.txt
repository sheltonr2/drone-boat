Run queue (see ..\setup_run_queue.bat)

A request is a file here ending in .run whose single line is the name of a batch file in the simulator folder,
for example:   run_revC5_2023.bat
Every 5 minutes run_queue.bat takes the first request, moves it to done\, and runs that batch file.
Only names of the form run_<letters, digits, _ or ->.bat are accepted; anything else goes to rejected\.
One run at a time: running.lock exists while a run is going. If the PC was switched off mid-run and the lock is
stale, put a file called unlock.run here to clear it.
queue_log.txt records every start, finish and rejection.

Window: on some PCs the scheduled task runs hidden (no console window). Double-click run_queue_window.bat
and leave it open: it runs the queue in that window, with the banner and progress, and the scheduled task
stands aside while the window is open. Close it and the scheduled task takes over again.

Battery (13 Nov 2026): Windows' default made the scheduled task stop when the laptop was unplugged, which killed a
run on 12 Nov and left running.lock behind. fix_run_queue_battery.bat (once) turns that off; setup_run_queue.bat
now does it on creation. Every simulator run also asks Windows not to sleep while it is going. A closed lid still
sleeps the laptop unless the lid setting is "Do nothing"; a run paused by sleep resumes on wake.
