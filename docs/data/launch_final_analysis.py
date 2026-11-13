"""Stage C of the launch-point study (docs/Launch_Point_Study.md): Rev D, 500 voyages per pair, alternating 2023 and
2024 weather, same seeds in all three runs. Run from the repo root. Paired differences resample seeds."""
import json, random, statistics as st, sys
import numpy as np
sys.path.insert(0, 'simulator')
from drone_sim.storms import StormClimatology
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
P = ['hatteras__ireland_sw', 'hatteras__cornwall', 'ocean_city__ireland_sw']
R = {p: {r['seed']: r for r in json.load(open(f'results/2026-11-13_launch_2023+2024_{p}.json'))['result']['runs']} for p in P}
seeds = sorted(set.intersection(*(set(v) for v in R.values())))
yr = {s: R['ocean_city__ireland_sw'][s]['start_time'][:4] for s in seeds}
def boot(f, ss, n=4000, seed=1):
    rnd = random.Random(seed); m = len(ss)
    v = sorted(f([ss[rnd.randrange(m)] for _ in range(m)]) for _ in range(n)); return f(ss), v[int(.025*n)], v[int(.975*n)]
print(f"{len(seeds)} voyages per pair, years {dict((y, sum(1 for s in seeds if yr[s] == y)) for y in sorted(set(yr.values())))}")
for p in P:
    line = f"  {p:26s} {100*st.mean(ok(R[p][s]) for s in seeds):5.1f}%"
    for y in sorted(set(yr.values())):
        ss = [s for s in seeds if yr[s] == y]; line += f"   {y}: {100*st.mean(ok(R[p][s]) for s in ss):5.1f}%"
    from collections import Counter
    c = Counter(R[p][s]['outcome'] for s in seeds); line += "   " + ", ".join(f"{k} {100*v/len(seeds):.1f}" for k, v in sorted(c.items()))
    print(line)
for a, b, lab in (('hatteras__ireland_sw', 'ocean_city__ireland_sw', 'Launch: Hatteras Inlet vs Ocean City (to SW Ireland)'),
                  ('hatteras__cornwall', 'hatteras__ireland_sw', 'Destination: Cornwall vs SW Ireland (from Hatteras Inlet)'),
                  ('hatteras__cornwall', 'ocean_city__ireland_sw', 'Best pair vs current plan: Hatteras Inlet -> Cornwall vs Ocean City -> SW Ireland')):
    print(lab)
    for y in ['all'] + sorted(set(yr.values())):
        ss = seeds if y == 'all' else [s for s in seeds if yr[s] == y]
        f = lambda q: 100*st.mean(ok(R[a][s]) - ok(R[b][s]) for s in q); m, lo, hi = boot(f, ss)
        print(f"   {y:4s} {m:+5.1f} ({lo:+.1f} to {hi:+.1f})")
clim = StormClimatology(); LOSS = {'TS': 0.30, 'HU': 0.70}
for p in P:
    a = []; adj = 0.0
    for s in seeds:
        r = R[p][s]; tr = r.get('track')
        if not tr or len(tr[0]) < 3: continue
        a.append(np.mean([w >= 34 for _, w, _ in clim.voyage(tr, r['start_time'], 200.0)]))
        if ok(r): adj += 1 - np.mean([LOSS['HU'] if w >= 64 else LOSS['TS'] if w >= 34 else 0.0 for _, w, _ in clim.voyage(tr, r['start_time'], 100.0)])
    print(f"  storms {p:26s} TS+ within 200 km {100*np.mean(a):5.1f}%   success after storm loss {100*adj/len(seeds):5.1f}%")
