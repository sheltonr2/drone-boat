"""Command-line runs without the web UI.

  python -m drone_sim.cli voyage  --scenario my_scenario.json [--design my_design.json] [--out result.json]
  python -m drone_sim.cli mc      --scenario my_scenario.json --runs 200 --from 2022-06-01 --to 2022-06-30 --years 2022,2023,2024
  (add --wait-for-limits to sleep through Open-Meteo's daily limit and carry on the next day)
  python -m drone_sim.cli selftest            # checks Open-Meteo access and unit conversions
  python -m drone_sim.cli gridcheck [--scenario s.json]   # same voyage on a 1.0 and a 0.25 degree weather grid
"""
import argparse, json, os, sys, time, datetime as dt
from . import design as D
from .sim import run_voyage, DEFAULT_SCENARIO
from .montecarlo import run_montecarlo
from .server import jsonable, CACHE


def main():
    from .env import OpenMeteoLimit
    wait = "--wait-for-limits" in sys.argv
    if wait:
        sys.argv.remove("--wait-for-limits")
        if os.name == "nt":      # ask Windows not to sleep while this runs (no admin rights needed)
            try:
                import ctypes
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
            except Exception:
                pass
    while True:
        try:
            _main(); return
        except OpenMeteoLimit as e:
            if not wait:
                print(f"\nSTOPPED: {e}"); sys.exit(3)
            now = dt.datetime.now(dt.timezone.utc)
            nxt = (now + dt.timedelta(days=1)).replace(hour=0, minute=10, second=0, microsecond=0)
            print(f"\nDaily Open-Meteo limit reached. Everything so far is cached. Sleeping until "
                  f"{nxt.astimezone():%a %H:%M} local time, then carrying on. Leave the computer on and awake.", flush=True)
            time.sleep(max(60, (nxt - now).total_seconds()))


def _main():
    ap = argparse.ArgumentParser(prog="drone_sim")
    ap.add_argument("cmd", choices=["voyage", "mc", "selftest", "gridcheck", "download", "bulkcheck", "cdscheck", "stormcheck"])
    ap.add_argument("--months", default="", help="for download: e.g. 2023-05..2023-10,2024-05..2024-10")
    ap.add_argument("--stride", type=int, default=1, help="for download: keep every Nth ocean grid point (1 = full 1/12 deg)")
    ap.add_argument("--sources", default="era5,smoc,wav"); ap.add_argument("--keep-raw", action="store_true")
    ap.add_argument("--mc", help="for stormcheck: a Monte Carlo result file"); ap.add_argument("--radius", type=float, default=200.0)
    ap.add_argument("--scenario"); ap.add_argument("--design"); ap.add_argument("--out")
    ap.add_argument("--runs", type=int, default=100); ap.add_argument("--from", dest="frm"); ap.add_argument("--to")
    ap.add_argument("--years", default=""); ap.add_argument("--processes", type=int)
    a = ap.parse_args()
    design = D.load(a.design) if a.design else D.default_design()
    sc = dict(DEFAULT_SCENARIO)
    if a.scenario: sc.update(json.load(open(a.scenario)))
    if a.cmd == "download":
        from .bulk import download, month_list
        if not a.months:
            print("Give the months, e.g. --months 2023-05..2023-10,2024-05..2024-10"); return
        errs = download(month_list(a.months), CACHE, sources=tuple(x for x in a.sources.split(",") if x),
                        stride=a.stride, keep_raw=a.keep_raw, log=lambda m: print(m, flush=True))
        if errs:
            print("Some months failed:"); [print("  " + e[:300]) for e in errs]
        return
    if a.cmd == "stormcheck":
        from .storms import StormClimatology, mc_storm_table
        mc = json.load(open(a.mc))["result"]
        tab = mc_storm_table(mc, StormClimatology(), radius_km=a.radius)
        print(f"Tropical-cyclone encounters within {a.radius:.0f} km (HURDAT2 1991-2025 analog seasons), {a.mc}")
        print(f"{'launch':7s} {'voyages':>7s} {'any TS+':>8s} {'95% CI':>13s} {'TS':>6s} {'Cat1-2':>7s} {'Cat3-5':>7s}")
        for k, v in tab.items():
            print(f"{k:7s} {v['voyages']:7d} {100*v['p_any']:7.1f}% {100*v['ci95_any'][0]:5.1f}-{100*v['ci95_any'][1]:4.1f}% "
                  f"{100*v['p_TS']:5.1f}% {100*v['p_C1-2']:6.1f}% {100*v['p_C3-5']:6.1f}%")
        if a.out: json.dump(dict(radius_km=a.radius, table=tab), open(a.out, "w"), indent=1)
        return
    if a.cmd == "cdscheck":
        from .bulk import cds_check
        cds_check(log=lambda m: print(m, flush=True)); return
    if a.cmd == "mc" and sc.get("provider") == "bulk":
        from .bulk import available_months
        have = set(available_months(CACHE))
        # launch months plus five more, so voyages are not cut short by the end of the data
        need = {int(f"{y}{m:02d}") for y in (a.years.split(",") if a.years else [a.frm[:4]])
                for m in range(int(a.frm[5:7]), min(12, int(a.to[5:7]) + 5) + 1)}
        if not need <= have:
            print(f"STOPPED: bulk data is missing for months {sorted(need - have)} "
                  f"(downloaded, all three sources: {sorted(have) or 'none'}). Finish the download first.")
            sys.exit(4)
    if a.cmd == "bulkcheck":
        from .bulk import compare_with_openmeteo, available_months
        print("Downloaded months (all three sources):", available_months(CACHE), flush=True)
        compare_with_openmeteo(CACHE, log=lambda m: print(m, flush=True))
        # same voyage on both data sources (Open-Meteo side comes from the cache of the Nov 8 grid check)
        v = dict(sc, start={"lat": 38.25, "lon": -74.65}, start_time="2024-05-15T12:00:00", failures_enabled=False)
        if 202405 in available_months(CACHE):
            for prov in ("openmeteo", "bulk"):
                t0 = time.time()
                try:
                    r = run_voyage(design, dict(v, provider=prov), cache_dir=CACHE, log=lambda *x: None)
                except Exception as e:  # noqa: BLE001 - the check is informative only
                    print(f"Same voyage on {prov}: could not run ({e})", flush=True); continue
                print(f"Same voyage (Ocean City 25 km, 15 May 2024, no failures) on {prov:9s}: {r['outcome']}, "
                      f"{r['days']} days, {r['distance_km']} km, mean {r['stats']['mean_sog_kn']} kn "
                      f"[{time.time() - t0:.0f} s]", flush=True)
        return
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
        procs = a.processes or ((os.cpu_count() or 2) if sc.get("provider") == "bulk" else None)
        from .console import Progress, say
        say(f"Monte Carlo: {design.get('name', 'design')}, {a.runs} voyages, {sc.get('name', '')[:70]}")
        say("Building the speed model first (10-30 s) ...")
        pg, ok = Progress("Voyages", a.runs), [0, 0]
        print(f"[{time.strftime('%H:%M:%S')}] Monte Carlo: {a.runs} voyages, {sc.get('name', '')[:70]}; {procs or 'auto'} processes", flush=True)
        def _prog(frac, res):
            ok[0] += 1; ok[1] += res.get("outcome") in ("arrived_reporting", "arrived_tracked")
            pg.update(ok[0], f"arrived so far: {ok[1]}")
            if ok[0] % 10 == 0 or ok[0] == a.runs:          # a line in the log too, so progress can be read remotely
                print(f"[{time.strftime('%H:%M:%S')}] {ok[0]}/{a.runs} voyages done, {ok[1]} arrived", flush=True)
        r = run_montecarlo(design, sc, n_runs=a.runs, window=win, processes=procs, cache_dir=CACHE, progress=_prog)
        s_ = r["summary"]; say(f"Done: {s_.get('success_percent')}% verified arrivals. Full results are in the log and the results file.")
        print(json.dumps(jsonable(r["summary"]), indent=1))
    out = a.out or f"result_{a.cmd}_{int(time.time())}.json"
    json.dump(jsonable(dict(kind="voyage" if a.cmd == "voyage" else "montecarlo", design=design, result=r)), open(out, "w"))
    if a.cmd == "voyage":
        print(f"{r['outcome']} after {r['days']} days, {r['distance_km']} km. Saved {out}")
    else:
        print(f"Saved {out}")


if __name__ == "__main__":
    main()
