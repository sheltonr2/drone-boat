"""Command-line runs without the web UI.

  python -m drone_sim.cli voyage  --scenario my_scenario.json [--design my_design.json] [--out result.json]
  python -m drone_sim.cli mc      --scenario my_scenario.json --runs 200 --from 2022-06-01 --to 2022-06-30 --years 2022,2023,2024
  python -m drone_sim.cli selftest            # checks Open-Meteo access and unit conversions
  python -m drone_sim.cli gridcheck [--scenario s.json]   # same voyage on a 1.0 and a 0.25 degree weather grid
"""
import argparse, json, os, sys, time
from . import design as D
from .sim import run_voyage, DEFAULT_SCENARIO
from .montecarlo import run_montecarlo
from .server import jsonable, CACHE


def main():
    ap = argparse.ArgumentParser(prog="drone_sim")
    ap.add_argument("cmd", choices=["voyage", "mc", "selftest", "gridcheck"])
    ap.add_argument("--scenario"); ap.add_argument("--design"); ap.add_argument("--out")
    ap.add_argument("--runs", type=int, default=100); ap.add_argument("--from", dest="frm"); ap.add_argument("--to")
    ap.add_argument("--years", default=""); ap.add_argument("--processes", type=int)
    a = ap.parse_args()
    design = D.load(a.design) if a.design else D.default_design()
    sc = dict(DEFAULT_SCENARIO)
    if a.scenario: sc.update(json.load(open(a.scenario)))
    if a.cmd == "selftest":
        from .env import OpenMeteoProvider, to_epoch
        from .geometry import Boat
        print("1/3 Geometry and stability ...")
        b = Boat(design); st = b.stability_summary()
        print(f"    mass {b.summary()['mass_kg']:.1f} kg, GM {st['gm_m']:.3f} m, self-righting: {st['self_righting']}")
        print("2/3 Short voyage on synthetic weather (builds the polar the first time, ~1-3 min) ...")
        t = dict(sc, provider="synthetic", max_days=3)
        r = run_voyage(design, t, cache_dir=CACHE)
        print(f"    {r['distance_km']} km in {r['days']} days, outcome {r['outcome']}")
        print("3/3 Open-Meteo historic data ...")
        try:
            p = OpenMeteoProvider(cache_dir=CACHE, log=print)
            s = p.sample(47.0, -45.0, to_epoch("2023-07-01T12:00:00"))
            print(json.dumps(jsonable(s), indent=1))
            ok = s["marine_ok"] and abs(s["wind_u"]) + abs(s["wind_v"]) > 0
            print("Open-Meteo OK" if ok else "Open-Meteo returned no marine data at this point")
        except Exception as e:
            print(f"    Open-Meteo not reachable ({e}). Check your internet connection; synthetic weather still works.")
        return
    if a.cmd == "gridcheck":
        # Idea from jcolter11374/boat-sim #50: does a 1-degree grid blur the Gulf Stream core?
        # The 0.25-degree run makes about 16x as many Open-Meteo calls the first time (then cached).
        sc0 = dict(sc, failures_enabled=False)
        out = {}
        for res in (1.0, 0.25):
            r = run_voyage(design, dict(sc0, grid_deg=res), cache_dir=CACHE)
            out[res] = r
            print(f"grid {res:>4} deg: {r['outcome']}, {r['days']} days, {r['distance_km']} km, "
                  f"mean speed {r['stats']['mean_sog_kn']} kn")
        dd = out[0.25]["days"] - out[1.0]["days"]
        print(f"Difference: {dd:+.1f} days. Under about 3 days means the 1-degree grid is fine for Monte Carlo; "
              f"more than that, run Monte Carlo with \"grid_deg\": 0.25 (or 0.5) in your scenario file.")
        return
    if a.cmd == "voyage":
        r = run_voyage(design, sc, cache_dir=CACHE)
    else:
        win = dict(**({"from": a.frm + "T12:00:00", "to": (a.to or a.frm) + "T12:00:00"} if a.frm else {}),
                   years=[int(y) for y in a.years.split(",") if y.strip()]) if a.frm else None
        r = run_montecarlo(design, sc, n_runs=a.runs, window=win, processes=a.processes, cache_dir=CACHE)
        print(json.dumps(jsonable(r["summary"]), indent=1))
    out = a.out or f"result_{a.cmd}_{int(time.time())}.json"
    json.dump(jsonable(dict(kind="voyage" if a.cmd == "voyage" else "montecarlo", design=design, result=r)), open(out, "w"))
    if a.cmd == "voyage":
        print(f"{r['outcome']} after {r['days']} days, {r['distance_km']} km. Saved {out}")
    else:
        print(f"Saved {out}")


if __name__ == "__main__":
    main()
