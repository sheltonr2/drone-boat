"""Monte Carlo: many voyages with different failure draws and (optionally) start dates."""
import copy
import math, os, time, datetime as dt
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from .sim import Voyage, prepare_design, DEFAULT_SCENARIO
from .env import make_provider, LandMask, to_epoch, from_epoch, destination, bearing_deg, haversine_km

OUTCOMES = ["arrived_reporting", "arrived_silent", "at_sea_timeout", "aground", "lost"]


def _one(args):
    design, sc, cache_dir, i = args
    try:
        r = Voyage(design, sc, cache_dir=cache_dir, log=lambda *a: None).run()
    except Exception as e:  # keep the batch alive
        return dict(i=i, error=str(e))
    ser = r["series"]
    step = max(1, len(ser)//150)
    track = [[s["lat"], s["lon"]] for s in ser[::step]] + [[r["end"]["lat"], r["end"]["lon"]]]
    fatal = [e["msg"] for e in r["events"] if e["kind"] == "failure"]
    return dict(i=i, start_time=sc["start_time"], seed=sc["seed"], outcome=r["outcome"], days=r["days"],
                distance_km=r["distance_km"], airtime_usd=r["airtime_usd"], knockdowns=r["knockdowns"],
                capsizes=r["capsizes"], failures=fatal, end=r["end"], track=track, stats=r["stats"],
                last_report_day=r.get("last_report_day"))


def start_times(window, n, rng):
    if not window or not window.get("from"):
        return None
    t0, t1 = to_epoch(window["from"]), to_epoch(window.get("to") or window["from"])
    years = window.get("years") or []
    out = []
    for k in range(n):
        t = t0 + rng.random()*(max(t1 - t0, 0))
        if years:
            d = from_epoch(t); y = years[k % len(years)]
            try: d = d.replace(year=int(y))
            except ValueError: d = d.replace(year=int(y), day=28)
            t = d.timestamp()
        out.append(from_epoch(t).strftime("%Y-%m-%dT%H:%M:%S"))
    return out


def corridor(sc, n=12):
    a, b = sc["start"], sc["target"]
    pts = []
    d = haversine_km(a["lat"], a["lon"], b["lat"], b["lon"])
    brg = bearing_deg(a["lat"], a["lon"], b["lat"], b["lon"])
    for k in range(n + 1):
        pts.append(destination(a["lat"], a["lon"], brg, d*1000*k/n))
    return pts


def run_montecarlo(design, scenario, n_runs=50, window=None, processes=None, cache_dir="cache", log=print,
                   progress=None, cancelled=lambda: False):
    sc0 = {**copy.deepcopy(DEFAULT_SCENARIO), **scenario}
    rng = np.random.default_rng(sc0.get("seed", 1))
    prepare_design(design, cache_dir, log)                       # build polar once (disk cache)
    LandMask(cache_dir, allow_download=sc0["provider"] != "synthetic", log=log)
    starts = start_times(window, n_runs, rng)
    scs = []
    for i in range(n_runs):
        sc = copy.deepcopy(sc0); sc["seed"] = int(sc0.get("seed", 1)*1000 + i)
        if starts: sc["start_time"] = starts[i]
        scs.append(sc)
    if sc0["provider"] == "openmeteo":
        prov = make_provider("openmeteo", cache_dir, log, sc0["grid_deg"], fine_grid=sc0.get("fine_grid"))
        # Only the months each voyage can actually be at sea (not every month between the first and last start).
        months, horizon = set(), min(sc0["max_days"], 150)
        for s in scs:
            d0 = from_epoch(to_epoch(s["start_time"])).replace(day=1)
            d1 = from_epoch(min(to_epoch(s["start_time"]) + horizon*86400, time.time() - 3*86400))
            while d0 <= d1:
                months.add(int(d0.strftime("%Y%m"))); d0 = (d0 + dt.timedelta(days=32)).replace(day=1)
        log(f"Downloading historic data along the route corridor for {len(months)} months (cached for later runs) ...")
        prov.prefetch(corridor(sc0), 0, 0, log=log, months=months)
    processes = processes or max(1, (os.cpu_count() or 2) - 1)
    results = []
    t_start = time.time()
    if processes == 1:
        for i, sc in enumerate(scs):
            if cancelled(): break
            results.append(_one((design, sc, cache_dir, i)))
            if progress: progress(len(results)/n_runs, results[-1])
    else:
        with ProcessPoolExecutor(max_workers=processes) as ex:
            futs = [ex.submit(_one, (design, sc, cache_dir, i)) for i, sc in enumerate(scs)]
            for f in as_completed(futs):
                if cancelled():
                    for g in futs: g.cancel()
                    break
                results.append(f.result())
                if progress: progress(len(results)/n_runs, results[-1])
    results.sort(key=lambda r: r["i"])
    return dict(summary=summarize(results), runs=results, wall_s=round(time.time() - t_start, 1),
                scenario=sc0, design_name=design.get("name"))


def summarize(results):
    ok = [r for r in results if "error" not in r]
    n = max(len(ok), 1)
    counts = {o: sum(1 for r in ok if r["outcome"] == o) for o in OUTCOMES}
    arr = [r["days"] for r in ok if r["outcome"].startswith("arrived")]
    causes = {}
    for r in ok:
        if r["outcome"] in ("lost", "aground", "at_sea_timeout"):
            key = r["failures"][-1] if r["failures"] else r["outcome"].replace("_", " ")
            key = key.split(" (")[0].split(":")[0].split(" at ")[0]
            causes[key] = causes.get(key, 0) + 1
    pct = lambda k: round(100*counts[k]/n, 1)
    def ci(p, n):
        z = 1.96; ph = p/100
        den = 1 + z*z/n; c = (ph + z*z/(2*n))/den; h = z*math.sqrt(ph*(1 - ph)/n + z*z/(4*n*n))/den
        return [round(100*max(c - h, 0), 1), round(100*min(c + h, 1), 1)]
    success = pct("arrived_reporting")
    # Odds by launch month (idea from jcolter11374/boat-sim): which months to launch in.
    by_month = {}
    for r in ok:
        mth = (r.get("start_time") or "")[:7][-2:]
        if not mth.isdigit():
            continue
        b = by_month.setdefault(mth, dict(runs=0, arrived_reporting=0))
        b["runs"] += 1; b["arrived_reporting"] += r["outcome"] == "arrived_reporting"
    for b in by_month.values():
        b["success_percent"] = round(100*b["arrived_reporting"]/b["runs"], 1)
        b["success_ci95"] = ci(b["success_percent"], b["runs"])
    by_month = dict(sorted(by_month.items()))
    return dict(runs=len(ok), errors=len(results) - len(ok), counts=counts,
                percent={k: pct(k) for k in OUTCOMES},
                success_percent=success, success_ci95=ci(success, n), by_launch_month=by_month,
                any_arrival_percent=round(pct("arrived_reporting") + pct("arrived_silent"), 1),
                arrival_days=dict(median=float(np.median(arr)) if arr else None,
                                  p10=float(np.percentile(arr, 10)) if arr else None,
                                  p90=float(np.percentile(arr, 90)) if arr else None, all=arr),
                failure_causes=dict(sorted(causes.items(), key=lambda kv: -kv[1])),
                mean_airtime_usd=round(float(np.mean([r["airtime_usd"] for r in ok])), 2) if ok else 0,
                mean_knockdowns=round(float(np.mean([r["knockdowns"] for r in ok])), 1) if ok else 0)
