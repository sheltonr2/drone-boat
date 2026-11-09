"""Sensitivity batches behind docs/Failure_Rates.md section 6.
Usage: python docs/data/run_rate_variants_montecarlo.py planning-no-shakedown planning-second-tracker"""
import json, sys, time
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "simulator"))
from drone_sim import design as D
from drone_sim.montecarlo import run_montecarlo
from drone_sim.server import jsonable
win = {"from": "2022-04-01T00:00:00", "to": "2022-07-31T23:00:00", "years": [2022, 2023, 2024, 2025]}
variants = {
  "planning-no-shakedown": {"failures": {"early_life": {"burn_in_days": 0.0}}},
  "planning-second-tracker": {"failures": {"comms_silent": {"enabled": False}}},
}
for name in sys.argv[1:]:
    t = time.time()
    sc = {"provider": "synthetic", "failure_rate_set": "planning", "seed": 1, **variants[name]}
    r = run_montecarlo(D.default_design(), sc, n_runs=100, window=win, processes=2, cache_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "simulator", "workspace", "cache"), log=lambda *a: None)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results", f"2026-11-08_midatlantic_montecarlo_rates-{name}.json")
    json.dump(jsonable({"kind": "montecarlo", "design": D.default_design(), "result": r}), open(out, "w"))
    s = r["summary"]
    print(name, s["success_percent"], s["success_ci95"], s["percent"], s["failure_causes"], round(time.time()-t), flush=True)
