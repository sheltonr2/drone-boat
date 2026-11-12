"""Summarise launch-point study results (docs/Launch_Point_Study.md).

python docs/data/launch_analysis.py <baseline result.json> <result.json> ...
Success = arrived_reporting + arrived_tracked. Runs share launch dates and seeds, so differences from the
baseline are paired. Also reports what happens near the launch coast, and a fishing-ground sensitivity:
the simulator's pick-up risk is the same off every coast, so each success is re-weighted by
exp(-rate x days spent on the New England / Nova Scotia / Grand Banks fishing grounds) for two guessed rates.
"""
import json, sys, os, math, random, statistics as st
from collections import Counter

# rough boxes over the heavily fished shelves (lat0, lat1, lon0, lon1)
FISHING = [("Gulf of Maine and Georges Bank", 40.8, 45.2, -71.0, -65.5),
           ("Scotian Shelf", 42.5, 46.5, -65.5, -57.0),
           ("Grand Banks", 43.0, 48.5, -55.0, -47.5)]
EXTRA_RATES = (0.02, 0.05)    # extra pick-ups per day on those grounds: GUESSES bracketing the Microtransat record

def ok(r): return r["outcome"] in ("arrived_reporting", "arrived_tracked")

def days_on_grounds(track):
    d = 0.0
    for a, b in zip(track, track[1:]):
        la, lo = (a[0] + b[0])/2, (a[1] + b[1])/2
        if any(x0 <= la <= x1 and y0 <= lo <= y1 for _, x0, x1, y0, y1 in FISHING):
            d += b[2] - a[2]
    return d

def days_to_clear(track, start, km=200.0):
    """Days until the boat is first `km` from its launch point (a stand-in for 'off the shelf')."""
    for p in track:
        dx = (p[1] - start[1])*math.cos(math.radians(start[0]))*111.2; dy = (p[0] - start[0])*111.2
        if math.hypot(dx, dy) >= km: return p[2]
    return None

def boot_ci(x, n=4000, seed=1):
    rnd = random.Random(seed); m = len(x)
    s = sorted(sum(x[rnd.randrange(m)] for _ in range(m))/m for _ in range(n))
    return s[int(0.025*n)], s[int(0.975*n)]

def summarise(path, base=None):
    d = json.load(open(path))["result"]; runs = d["runs"]; n = len(runs); s = d["summary"]
    start = (d["scenario"]["start"]["lat"], d["scenario"]["start"]["lon"])
    oc = Counter(r["outcome"] for r in runs)
    succ = [r for r in runs if ok(r)]
    early = [r for r in runs if r["outcome"] in ("aground", "lost") and r["days"] < 21]
    home = [r for r in runs if r["outcome"] == "aground" and r["end"]["lon"] < -50]
    clear = [c for c in (days_to_clear(r.get("track") or [], start) for r in runs) if c is not None]
    grounds = [days_on_grounds(r.get("track") or []) for r in runs]
    adj = {k: 100*sum(math.exp(-k*g) for r, g in zip(runs, grounds) if ok(r))/n for k in EXTRA_RATES}
    out = dict(name=os.path.basename(path).replace(".json", "").split("_", 2)[-1], start=start, n=n,
               succ=s["success_percent"], ci=s["success_ci95"], med=st.median([r["days"] for r in succ]) if succ else None,
               lost=100*oc["lost"]/n, aground=100*oc["aground"]/n, sea=100*oc["at_sea_timeout"]/n,
               early=100*len(early)/n, home=100*len(home)/n, clear=st.median(clear) if clear else None,
               never_clear=100*(n - len(clear))/n, grounds=st.mean(grounds), adj=adj, ok={r["seed"]: ok(r) for r in runs},
               causes=dict(Counter(f.split(":")[0].split(" (")[0] for r in runs for f in r["failures"][:1]).most_common(4)))
    if base is not None:
        diff = [100*(v - base["ok"][k]) for k, v in out["ok"].items() if k in base["ok"]]
        out["paired"] = (st.mean(diff),) + boot_ci(diff)
    return out

if __name__ == "__main__":
    base = summarise(sys.argv[1]); rows = [base] + [summarise(p, base) for p in sys.argv[2:]]
    rows.sort(key=lambda r: -r["succ"])
    print("| Launch | Success (95% range) | vs baseline, paired | Median days | Lost | Aground | At sea | Lost or aground in 3 weeks | Aground on the home side | Days to get 200 km away | Fishing-ground days | Success if those grounds add 2% / 5% a day |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        p = r.get("paired"); pd = "—" if p is None else f"{p[0]:+.1f} ({p[1]:+.1f} to {p[2]:+.1f})"
        med = "—" if r["med"] is None else f"{r['med']:.0f}"; cl = "—" if r["clear"] is None else f"{r['clear']:.1f}"
        print(f"| {r['name']} | {r['succ']:.1f}% ({r['ci'][0]:.0f}–{r['ci'][1]:.0f}) | {pd} | {med} | {r['lost']:.1f}% | {r['aground']:.1f}% | {r['sea']:.1f}% | "
              f"{r['early']:.1f}% | {r['home']:.1f}% | {cl} | {r['grounds']:.1f} | {r['adj'][EXTRA_RATES[0]]:.1f}% / {r['adj'][EXTRA_RATES[1]]:.1f}% |")
    print()
    for r in rows: print(r["name"], r["start"], "never 200 km away:", f"{r['never_clear']:.0f}%", "first failures:", r["causes"])
