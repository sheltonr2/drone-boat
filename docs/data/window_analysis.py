"""Launch windows on four years of weather (runs 019a-c, 15 Nov 2026; docs/Launch_Plan.md).
Rev E1, 45 km off Hatteras -> Cornwall, 500 voyages per window, 2021-2024 weather. Run from the repo root."""
import json, sys, random, statistics as st
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, 'simulator')
from drone_sim.storms import StormClimatology
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
W = {"april": "April (1-30 Apr)", "may_early": "1-20 May (plan)", "may_late": "21 May-15 Jun"}
R = {w: json.load(open(f'results/2026-11-15_window_{w}_2021+2022+2023+2024_revE1_hatteras_stream__cornwall.json'))['result']['runs'] for w in W}
def boot(x, n=4000):
    rnd = random.Random(1); m = len(x); v = sorted(sum(x[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
yr = lambda r: int(r['start_time'][:4])
clim = StormClimatology(); LOSS = {'TS': 0.30, 'HU': 0.70}
out = {}
for w, runs in R.items():
    x = [100*ok(r) for r in runs]; lo, hi = boot(x)
    d = sorted(r['days'] for r in runs if ok(r))
    by = defaultdict(list)
    for r in runs: by[yr(r)].append(ok(r))
    a200 = []; adj = 0.0
    for r in runs:
        tr = r.get('track')
        if not tr or len(tr[0]) < 3: continue
        v = clim.voyage(tr, r['start_time'], 200.0); a200.append(np.mean([q >= 34 for _, q, _ in v]))
        if ok(r):
            v1 = clim.voyage(tr, r['start_time'], 100.0)
            adj += 1 - np.mean([LOSS['HU'] if q >= 64 else LOSS['TS'] if q >= 34 else 0.0 for _, q, _ in v1])
    out[w] = dict(label=W[w], n=len(runs), success=st.mean(x), ci95=[lo, hi], median_days=st.median(d), p90_days=d[int(.9*len(d))],
                  by_year={y: 100*st.mean(v) for y, v in sorted(by.items())}, n_by_year={y: len(v) for y, v in sorted(by.items())},
                  outcomes=dict(Counter(r['outcome'] for r in runs)), storm200=100*float(np.mean(a200)), storm_adjusted=100*adj/len(runs))
    o = out[w]
    print(f"{W[w]:16s} success {o['success']:.1f}% ({lo:.1f}-{hi:.1f}); median {o['median_days']:.0f} d, p90 {o['p90_days']:.0f}; "
          f"by year " + ", ".join(f"{y}: {v:.0f}%" for y, v in o['by_year'].items()) +
          f"; TS+ within 200 km {o['storm200']:.1f}%; after storm losses {o['storm_adjusted']:.1f}%")
    print("   outcomes", o['outcomes'])
# Paired differences where the seeds match
seeds = {w: {r['seed']: r for r in runs} for w, runs in R.items()}
common = set.intersection(*[set(s) for s in seeds.values()])
print(f"\n{len(common)} seeds common to all three windows (same seed = same random failures, different launch date)")
out['paired'] = {}
for w in ("april", "may_late"):
    dd = [100*(ok(seeds[w][s]) - ok(seeds['may_early'][s])) for s in sorted(common)]
    lo, hi = boot(dd); out['paired'][w] = [st.mean(dd), lo, hi]
    print(f"  {W[w]} minus 1-20 May: {st.mean(dd):+.1f} points ({lo:+.1f} to {hi:+.1f})")
# By year, pooled windows; 2023+2024 against run 017 (1 May-15 Jun on the same two years)
print("\nBy weather year, all windows pooled:")
for y in (2021, 2022, 2023, 2024):
    v = [ok(r) for w in R for r in R[w] if yr(r) == y]; print(f"  {y}: {100*st.mean(v):.1f}% of {len(v)}")
json.dump(out, open('docs/data/window_analysis.json', 'w'), indent=1)
