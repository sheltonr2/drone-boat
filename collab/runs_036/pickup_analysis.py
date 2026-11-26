"""Pickup-point study (runs 036, 037, 038, 039; 26 Nov 2026): one table per candidate.

For each BVI candidate: the crossing from Mindelo (run 038: arrival %, days, groundings and where), and the hold there
(run 036: station-keeping within 1 km for 14 days). For each Cornwall candidate: the hold (run 037); the crossing to
the Lizard offing is run 039 (and run 042 for the southern approaches, when it has run).

Combined figure: P(pickup) = P(arrive) x P(still afloat and reporting when the recovery boat gets there), for a pickup
1, 3 or 7 days after arrival. The second factor is read from the station-keeping runs: the share of holds with no
grounding and no loss of the boat by that day. Usage: python collab/runs_036/pickup_analysis.py [results dir]
Writes collab/runs_036/pickup_analysis.json.
"""
import json, math, os, random, sys, datetime as dt
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "runs_026"))
from hold_analysis import val  # noqa: E402
from hold_analysis_036_037 import BVI, CORN, where_bvi  # noqa: E402

ok = lambda r: r["outcome"] in ("arrived_reporting", "arrived_tracked")


def boot(x, n=3000):
    rnd = random.Random(1); m = len(x)
    v = sorted(sum(x[rnd.randrange(m)] for _ in range(m)) / m for _ in range(n)); return round(v[int(.025 * n)], 1), round(v[int(.975 * n)], 1)


def find(rd, name):
    for f in (name, "2026-11-26_" + name, "2026-11-27_" + name):
        p = os.path.join(rd, f)
        if os.path.exists(p): return p
    return None


def survive(path, days=(1, 3, 7, 14)):
    """Share of station-keeping holds still afloat and not lost by each day."""
    runs = json.load(open(path))["result"]["runs"]; n = len(runs); out = {}
    for d in days:
        bad = sum(1 for r in runs if r["outcome"] in ("aground", "lost") and float(r["days"]) <= d)
        out[d] = round(100 * (1 - bad / n), 1)
    return out


def crossing(path):
    d = json.load(open(path)); runs = d["result"]["runs"]; n = len(runs)
    x = [100 * ok(r) for r in runs]; days = sorted(float(r["days"]) for r in runs if ok(r))
    g = Counter()
    for r in runs:
        if r["outcome"] == "aground":
            e = val(r["end"]); g[where_bvi(e["lat"], e["lon"]) if -66 < e["lon"] < -64 and 17.5 < e["lat"] < 19 else "elsewhere"] += 1
    arr_month = Counter()
    for r in runs:
        if ok(r):
            t = dt.datetime.fromisoformat(r["start_time"]) + dt.timedelta(days=float(r["days"])); arr_month[t.strftime("%b")] += 1
    s = d["result"]["summary"]
    sp = path[:-5] + "_storms.json"
    storm = json.load(open(sp))["table"]["all"]["p_any"] if os.path.exists(sp) else None
    return dict(runs=n, arrive=round(sum(x) / n, 1), ci95=boot(x), percent=s["percent"],
                days_median=round(days[len(days) // 2], 1) if days else None, groundings=dict(g.most_common()),
                arrival_months=dict(arr_month.most_common()), storm_p_any=storm)


def main():
    rd = sys.argv[1] if len(sys.argv) > 1 else "results"
    H = json.load(open(os.path.join(HERE, "hold_analysis_036_037.json")))
    res = dict(bvi={}, cornwall={})
    print(f"{'BVI candidate':26s} {'arrive%':>8s} {'95% CI':>13s} {'days':>5s} {'aground':>8s} | hold 14 d: {'aground':>7s} {'r50':>5s} {'r90':>5s}"
          f" | P(pickup) day 1 / 3 / 7")
    for tag, (nm, la, lo) in BVI.items():
        hs = H["bvi"].get(f"station_{tag}"); hd = H["bvi"].get(f"drift_{tag}")
        sf = find(rd, f"hold036_2022-2025_revE3_station_{tag}.json")
        cf = find(rd, f"ew038_2021-2024_revE3_mindelo__{tag}.json")
        e = dict(name=nm, lat=la, lon=lo, hold=hs, drift=hd)
        if sf: e["afloat_by_day"] = survive(sf)
        if cf:
            e["crossing"] = c = crossing(cf)
            if sf: e["p_pickup"] = {d: round(c["arrive"] * e["afloat_by_day"][d] / 100, 1) for d in (1, 3, 7)}
        res["bvi"][tag] = e
        c = e.get("crossing") or {}
        print(f"{nm:26s} {c.get('arrive', float('nan')):8.1f} {str(c.get('ci95', '')):>13s} {c.get('days_median') or 0:5.0f} "
              f"{c.get('percent', {}).get('aground', 0):7.1f}% | {hs['percent'].get('aground', 0):7.1f}% {hs['r50_km']:5.1f} {hs['r90_km']:5.1f}"
              f" | {e.get('p_pickup')}  groundings on the way: {c.get('groundings')}")
    print(f"\n{'Cornwall candidate':26s} hold 14 d: aground  r50   r90  | afloat by day 1/3/7/14")
    for tag, (nm, la, lo) in CORN.items():
        hs = H["cornwall"].get(f"station_{tag}"); sf = find(rd, f"hold037_2021-2024_revE3_station_{tag}.json")
        e = dict(name=nm, lat=la, lon=lo, hold=hs, drift=H["cornwall"].get(f"drift_{tag}"))
        if sf: e["afloat_by_day"] = survive(sf)
        res["cornwall"][tag] = e
        print(f"{nm:26s}            {hs['percent'].get('aground', 0):6.1f}% {hs['r50_km']:5.1f} {hs['r90_km']:5.1f} | {e.get('afloat_by_day')}")
    for lab, f in [("039 plan, Lizard offing", "plan039_2021-2024_revE3_lizard_offing_detail.json"),
                   ("042A south of Scilly, Lizard offing", "plan042_2021-2024_revE3_south_lizard_offing_detail.json"),
                   ("042B south of Scilly, 30 km S of Lizard", "plan042_2021-2024_revE3_south_lizard_deep_detail.json")]:
        p = find(rd, f)
        if p:
            d = json.load(open(p))["result"]; runs = d["runs"]; x = [100 * ok(r) for r in runs]
            res["cornwall"].setdefault("crossings", {})[lab] = dict(arrive=round(sum(x) / len(x), 1), ci95=boot(x), percent=d["summary"]["percent"])
            print(f"crossing {lab}: {round(sum(x)/len(x),1)}% {boot(x)}  {d['summary']['percent']}")
    json.dump(res, open(os.path.join(HERE, "pickup_analysis.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
