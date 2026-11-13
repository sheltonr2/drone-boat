"""Results of the three reliability runs (docs/Reliability_Review.md, Results). Run from the repo root.

Each run used the same launch dates and seeds as the Rev D run (results/2026-11-12_bulk_mc_2023_revD_10km.json),
so differences are paired by seed. Success = arrived_reporting + arrived_tracked.
"""
import json, random, statistics as st
from collections import Counter
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
cat = lambda f: f.split(':')[0].split(' (')[0].split(' at ')[0].replace('One rudder', 'Rudder').replace('Rudder servo stripped by a wave strike', 'Rudder servo stripped')
def load(p): return {r['seed']: r for r in json.load(open(p))['result']['runs']}
base = load('results/2026-11-12_bulk_mc_2023_revD_10km.json')
def boot(d, n=4000, seed=1):
    rnd = random.Random(seed); m = len(d)
    v = sorted(sum(d[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
def first(r): return cat(r['failures'][0]) if r['failures'] else None
def leaky(r): return any(f.startswith('Leak started') or 'hull leaking' in f for f in r['failures'])
def report(name, path):
    R = load(path); seeds = sorted(set(R) & set(base)); n = len(seeds)
    d = [100*(ok(R[s]) - ok(base[s])) for s in seeds]; lo, hi = boot(d)
    print(f"\n== {name}: {100*sum(ok(R[s]) for s in seeds)/n:.1f}% vs Rev D {100*sum(ok(base[s]) for s in seeds)/n:.1f}%, "
          f"paired {st.mean(d):+.1f} ({lo:+.1f} to {hi:+.1f}); gained {sum(x > 0 for x in d)}, lost {sum(x < 0 for x in d)}")
    for lab, X in (('Rev D', base), (name, R)):
        lv = [X[s] for s in seeds if leaky(X[s])]
        print(f"  {lab:18s} voyages with a leak {len(lv):3d}, of which arrived {sum(map(ok, lv)):3d} ({100*sum(map(ok, lv))/max(1,len(lv)):.0f}%); "
              f"outcomes {dict(Counter(r['outcome'] for r in lv))}")
    print("  Losses by first failure (Rev D -> this run):")
    lb = Counter(first(base[s]) for s in seeds if not ok(base[s])); lr = Counter(first(R[s]) for s in seeds if not ok(R[s]))
    for k in sorted(set(lb) | set(lr), key=lambda k: -(lb[k] + lr[k])):
        print(f"    {str(k):45s} {lb[k]:3d} -> {lr[k]:3d}")
    print("  Voyages with each failure at any point (Rev D -> this run):")
    ab = Counter(c for s in seeds for c in {cat(f) for f in base[s]['failures']}); ar = Counter(c for s in seeds for c in {cat(f) for f in R[s]['failures']})
    for k in sorted(set(ab) | set(ar), key=lambda k: -(ab[k] + ar[k]))[:12]:
        print(f"    {k:45s} {ab[k]:3d} -> {ar[k]:3d}")
    return R
P = report('Bilge pump, pump-and-sail', 'results/2026-11-13_bulk_mc_2023_revD_pump_10km.json')
pf = [r for r in P.values() if any('Bilge pump failed' in f for f in r['failures'])]
print(f"  Pump failures: {len(pf)} voyage(s), outcomes {[r['outcome'] for r in pf]}")
rates = [float(f.split('(')[1].split(' kg')[0]) for r in P.values() for f in r['failures'] if f.startswith('Leak started (')]
print(f"  Leak rates {min(rates):.2f}-{max(rates):.2f} kg/day against a 500 kg/day pump: worst duty {100*max(rates)/500:.2f}%, "
      f"so at most {4*24*max(rates)/500:.2f} Wh/day of pumping")
report('Full reliability package', 'results/2026-11-13_bulk_mc_2023_revD_reliability_10km.json')
W = report('Weed pessimistic (clears ~0.03/day)', 'results/2026-11-13_bulk_mc_2023_revD_weed_pessimistic_10km.json')
