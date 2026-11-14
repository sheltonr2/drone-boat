"""Rev E on the new route (Hatteras -> Cornwall): baseline, slower-boat checks and drop points clear of Diamond
Shoals (docs/Naval_Review.md, docs/Launch_Plan.md). All runs 500 voyages, 2023 and 2024 weather, the same seeds as
stage C. Run from the repo root."""
import json, random, statistics as st, sys
from collections import Counter
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
def L(p): return {r['seed']: r for r in json.load(open(p))['result']['runs']}
P = 'results/2026-11-13_plan_2023+2024_revE_{}__cornwall.json'
R = {k: L(P.format(k)) for k in ('hatteras', 'slow10_hatteras', 'slow20_hatteras', 'hatteras_stream', 'hatteras_east', 'hatteras_dogleg')}
R['revD_hatteras'] = L('results/2026-11-13_launch_2023+2024_hatteras__cornwall.json')
seeds = sorted(set.intersection(*(set(v) for v in R.values())))
def boot(d, n=4000):
    rnd = random.Random(1); m = len(d); v = sorted(sum(d[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
def paired(a, b):
    d = [100*(ok(R[a][s]) - ok(R[b][s])) for s in seeds]; lo, hi = boot(d); return st.mean(d), lo, hi
def shoal(k):
    w = [R[k][s].get('watch_min_km', {}).get('diamond_shoals') for s in seeds]
    w = [x for x in w if x is not None]
    if not w: return None
    return {lim: 100*sum(x < lim for x in w)/len(w) for lim in (2, 5, 10)}, len(w)
print(f"{len(seeds)} paired voyages\n")
print(f"{'run':18s} {'success':>8s}  {'median days':>11s}  {'at sea':>7s}  {'lost':>5s}  {'aground':>7s}  shoals <2/<5/<10 km")
for k in ('revD_hatteras', 'hatteras', 'slow10_hatteras', 'slow20_hatteras', 'hatteras_stream', 'hatteras_east', 'hatteras_dogleg'):
    rr = [R[k][s] for s in seeds]; c = Counter(r['outcome'] for r in rr)
    days = st.median(r['days'] for r in rr if ok(r))
    sh = shoal(k); shs = ' / '.join(f"{v:.0f}%" for v in sh[0].values()) if sh else 'not recorded'
    print(f"{k:18s} {100*sum(map(ok, rr))/len(rr):7.1f}%  {days:11.0f}  {100*c['at_sea_timeout']/len(rr):6.1f}%  {100*c['lost']/len(rr):4.1f}%  {100*c['aground']/len(rr):6.1f}%  {shs}")
print("\nPaired differences (95% range):")
for a, b, lab in (('hatteras', 'revD_hatteras', 'Rev E vs Rev D, Hatteras Inlet -> Cornwall'),
                  ('slow10_hatteras', 'hatteras', 'Every sailing speed x0.9 vs as predicted'),
                  ('slow20_hatteras', 'hatteras', 'Every sailing speed x0.8 vs as predicted'),
                  ('hatteras_stream', 'hatteras', '45 km Stream-edge drop vs inlet'),
                  ('hatteras_east', 'hatteras', '70 km drop east of the shoals vs inlet'),
                  ('hatteras_dogleg', 'hatteras', 'Inlet with a south-east dog-leg vs inlet'),
                  ('hatteras_east', 'hatteras_stream', '70 km vs 45 km')):
    m, lo, hi = paired(a, b); print(f"  {lab:45s} {m:+5.1f} ({lo:+.1f} to {hi:+.1f})")
# The inlet baseline started before its scenario got the shoal watch line, so its own crossings were not recorded.
# The x0.9 run (same drop, recorded) stands in: what share crossed, and how they did in the simulator (no shoals).
w = {s: R['slow10_hatteras'][s]['watch_min_km']['diamond_shoals'] for s in seeds}
cross = [s for s in seeds if w[s] < 2]
print(f"\nInlet drop (x0.9 run): {len(cross)} of {len(seeds)} voyages passed within 2 km of the shoal line; "
      f"{100*sum(ok(R['slow10_hatteras'][s]) for s in cross)/max(1, len(cross)):.0f}% of them 'arrived' in the simulator, which has no shoals.")
print(f"If each of those had been lost on the shoals, that run's success would fall from "
      f"{100*sum(ok(R['slow10_hatteras'][s]) for s in seeds)/len(seeds):.1f}% to {100*sum(ok(R['slow10_hatteras'][s]) for s in seeds if s not in cross)/len(seeds):.1f}%.")
