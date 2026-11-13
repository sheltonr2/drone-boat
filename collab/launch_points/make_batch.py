"""Write a Windows batch file for a list of launch/destination pairs.
python collab/launch_points/make_batch.py <batch name> <title> <design file> <years> <runs> <pair> [<pair> ...]
  pair = launch__dest (a scenario file in this folder);  years = 2023 or 2023,2024
A finished pair is skipped on a rerun, so a batch stopped by a reboot picks up where it left off."""
import sys

# Minutes per 150 voyages on Randolph's PC. Was 40 on the old code; the faster code (installed 13 Nov after the
# bit-for-bit check, docs/Simulator_Speedup.md) ran 4.4x faster on real weather, so about 9.
MIN_PER_150 = 9

def main(name, title, design, years, runs, pairs):
    prefix = "launch"                      # result files are results\<prefix>_<years>_<label>.json
    if pairs and pairs[0].startswith("--prefix="):
        prefix = pairs[0].split("=", 1)[1]; pairs = pairs[1:]
    tag = years.replace(",", "+"); log = f"..\\collab\\run_log_{name}.txt"; mins = MIN_PER_150*len(pairs)*int(runs)//150 + 2*len(pairs)
    L = ["@echo off",
         f"REM {title} (docs/Launch_Point_Study.md). Written by collab/launch_points/make_batch.py.",
         f"REM {len(pairs)} runs of {runs} voyages, weather {years}, design {design}. About {mins//60} h {mins%60:02d} min.",
         "REM A run that already has its result file is skipped, so this file can be restarted after a reboot.",
         "setlocal EnableDelayedExpansion",
         'cd /d "%~dp0"',
         "echo ============================================================",
         f"echo  {title}",
         f"echo  {len(pairs)} runs x {runs} voyages. Expected time: about {mins//60} h {mins%60:02d} min.",
         "echo  Progress shows below, one line per run. Started %date% %time%",
         "echo ============================================================",
         "set PYTHONIOENCODING=utf-8", "set PYTHONUNBUFFERED=1", f"set LOG={log}",
         f'echo {title}, started %date% %time% >> "%LOG%"']
    for i, p in enumerate(pairs, 1):
        # a run may be "pair" or "pair=design.json=label" (its own design file and result label)
        lab, dsg = p, design
        if "=" in p:
            p, dsg, lab = p.split("=")
        out = f"..\\results\\{prefix}_{tag}_{lab}.json"
        L += ["echo.", f"echo RUN {i} of {len(pairs)}: {lab}   (started %time%)",
              f"if exist {out} (",
              "  echo   already finished, skipping",
              f'  echo ==== RUN: {lab} already finished, skipped ==== >> "%LOG%"',
              ") else (",
              f'  echo ==== RUN: {lab} ==== >> "%LOG%"',
              f'  .venv\\Scripts\\python.exe -m drone_sim.cli mc --design ..\\designs\\{dsg} --scenario ..\\collab\\launch_points\\{p}.json --runs {runs} --from 2023-05-01 --to 2023-06-15 --years {years} --out {out} >> "%LOG%" 2>&1',
              f'  if exist {out} .venv\\Scripts\\python.exe ..\\collab\\summarize_mc.py {out} >> "%LOG%" 2>&1',
              f"  if exist {out} (echo   finished !time!) else (echo   FAILED: see {log})",
              ")"]
    L += ['echo === DONE %date% %time% >> "%LOG%"', "echo.",
          "echo ============================================================",
          "echo  ALL DONE %date% %time%",
          f"echo  Results: results\\{prefix}_{tag}_*.json   Log: {log[3:]}",
          "echo ============================================================", "pause"]
    open(f"simulator/run_{name}.bat", "w", newline="\r\n").write("\n".join(L) + "\n")
    print(f"simulator/run_{name}.bat: {len(pairs)} runs, about {mins} min")

if __name__ == "__main__":
    a = sys.argv
    main(a[1], a[2], a[3], a[4], a[5], a[6:])
