"""Stage B of the launch-point study (docs/Launch_Point_Study.md): 4 launches x 3 destinations.

Run from the repo root. Reports, for each launch, the paired difference against Ocean City 10 km pooled over the
three destinations (each launch-destination run compared with Ocean City 10 km to the same destination, same seeds),
and the same for each destination pooled over launches (against SW Ireland from the same launch). Pooling over cells
gives a tighter estimate than any single cell; the bootstrap resamples seeds, keeping each seed's cells together.
Also adds the storm encounters on the new pairs (grade-D loss model, docs/Hurricane_Risk.md).
"""
import json, sys, random, statistics as st
import numpy as np
sys.path.insert(0, 'simulator')
from drone_sim.storms import StormClimatology

L = ['hatteras_stream', 'ocean_city_canyon', 'hatteras', 'ocean_city']
D = ['ireland_sw', 'cornwall', 'brittany']
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
load = lambda l, d: json.load(open(f'results/2026-11-13_launch_2023_{l}__{d}.json'))['result']['runs']
R = {(l, d): load(l, d) for l in L for d in D}
S = {k: {r['seed']: ok(r) for r in v} for k, v in R.items()}
seeds = sorted(S[('ocean_city', 'ireland_sw')])

def boot(f, n=4000, seed=1):
    rnd = random.Random(seed); m = len(seeds)
    v = sorted(f([seeds[rnd.randrange(m)] for _ in range(m)]) for _ in range(n))
    return f(seeds), v[int(.025*n)], v[int(.975*n)]

print("Pooled over destinations: launch minus Ocean City 10 km (same destination, same seeds)")
for l in L:
    f = lambda ss: 100*st.mean(S[(l, d)][s] - S[('ocean_city', d)][s] for s in ss for d in D)
    m = 100*st.mean(S[(l, d)][s] for s in seeds for d in D)
    print(f"  {l:18s} mean success {m:5.1f}%   paired {boot(f)[0]:+5.1f} ({boot(f)[1]:+.1f} to {boot(f)[2]:+.1f})")
print("Pooled over launches: destination minus SW Ireland (same launch, same seeds)")
for d in D:
    f = lambda ss: 100*st.mean(S[(l, d)][s] - S[(l, 'ireland_sw')][s] for s in ss for l in L)
    m = 100*st.mean(S[(l, d)][s] for s in seeds for l in L)
    b = boot(f); print(f"  {d:12s} mean success {m:5.1f}%   paired {b[0]:+5.1f} ({b[1]:+.1f} to {b[2]:+.1f})")
print("Hatteras Inlet (10 km) minus Hatteras 45 km, pooled over destinations")
f = lambda ss: 100*st.mean(S[('hatteras', d)][s] - S[('hatteras_stream', d)][s] for s in ss for d in D)
b = boot(f); print(f"  {b[0]:+.1f} ({b[1]:+.1f} to {b[2]:+.1f})")

clim = StormClimatology(); LOSS = {'TS': 0.30, 'HU': 0.70}; out = {}
print("Storm encounters (fraction of voyages within 200 km of a tropical storm or stronger; success after the grade-D loss model)")
for (l, d), runs in R.items():
    a = []; adj = 0.0; n = len(runs)
    for r in runs:
        tr = r.get('track')
        if not tr or len(tr[0]) < 3: continue
        v200 = clim.voyage(tr, r['start_time'], 200.0); a.append(np.mean([w >= 34 for _, w, _ in v200]))
        if ok(r):
            v100 = clim.voyage(tr, r['start_time'], 100.0)
            adj += 1 - np.mean([LOSS['HU'] if w >= 64 else LOSS['TS'] if w >= 34 else 0.0 for _, w, _ in v100])
    succ = 100*sum(map(ok, runs))/n
    out[f'{l}__{d}'] = dict(succ=succ, any200=100*float(np.mean(a)), adj=100*adj/n)
    print(f"  {l+'__'+d:32s} TS+ within 200 km {out[f'{l}__{d}']['any200']:5.1f}%   success {succ:5.1f} -> {100*adj/n:5.1f}")
json.dump(out, open('docs/data/launch_pairs_storms.json', 'w'), indent=1)
