"""Re-run the rate-set Monte Carlo batches behind docs/Failure_Rates.md section 6 (about 5 min each on 2 cores).
Usage: python docs/data/run_rate_set_montecarlo.py planning historical original"""
import json, sys, time
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "simulator"))
from drone_sim import design as D
from drone_sim.montecarlo import run_montecarlo
from drone_sim.server import jsonable
win = {"from": "2022-04-01T00:00:00", "to": "2022-07-31T23:00:00", "years": [2022, 2023, 2024, 2025]}
for rs in sys.argv[1:]:
    t = time.time()
    sc = {"provider": "synthetic", "failure_rate_set": rs, "seed": 1}
    r = run_montecarlo(D.default_design(), sc, n_runs=100, window=win, processes=2, cache_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "simulator", "workspace", "cache"), log=lambda *a: None)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results", f"2026-11-08_midatlantic_montecarlo_rates-{rs}.json")
    json.dump(jsonable({"kind": "montecarlo", "design": D.default_design(), "result": r}), open(out, "w"))
    s = r["summary"]
    print(rs, s["success_percent"], s["success_ci95"], s["percent"], s["failure_causes"], round(time.time()-t), flush=True)
