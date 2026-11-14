"""Rev E1 on the planned route (45 km off Hatteras -> Cornwall), against Rev E on the same seeds, and the closest
approaches to the Seven Stones and the Isles of Scilly (docs/Design_RevE.md, docs/Launch_Plan.md). Run from the repo root."""
import json, random, statistics as st
from collections import Counter
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
def L(p): return {r['seed']: r for r in json.load(open(p))['result']['runs']}
E = L('results/2026-11-13_plan_2023+2024_revE_hatteras_stream__cornwall.json')
E1 = L('results/2026-11-14_plan_2023+2024_revE1_hatteras_stream__cornwall.json')
seeds = sorted(set(E) & set(E1))
def boot(d, n=4000):
    rnd = random.Random(1); m = len(d); v = sorted(sum(d[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
def ci(x):
    lo, hi = boot([100*v for v in x]); return lo, hi
out = {"paired_voyages": len(seeds)}
print(f"{len(seeds)} paired voyages (same seeds)\n")
for lab, R in (("Rev E", E), ("Rev E1", E1)):
    rr = [R[s] for s in seeds]; c = Counter(r['outcome'] for r in rr); okk = [ok(r) for r in rr]
    d = sorted(r['days'] for r in rr if ok(r)); lo, hi = ci(okk)
    row = dict(success=100*sum(okk)/len(rr), ci95=[lo, hi], median_days=st.median(d), p10_days=d[len(d)//10], p90_days=d[9*len(d)//10],
               outcomes={k: v for k, v in c.items()}, knockdowns_mean=st.mean(r['knockdowns'] for r in rr))
    out[lab] = row
    print(f"{lab:7s} success {row['success']:.1f}% ({lo:.1f}-{hi:.1f}); median {row['median_days']:.0f} d (p10 {row['p10_days']:.0f}, p90 {row['p90_days']:.0f}); "
          f"outcomes {dict(c)}; knockdowns/voyage {row['knockdowns_mean']:.0f}")
dd = [100*(ok(E1[s]) - ok(E[s])) for s in seeds]; lo, hi = boot(dd)
out["E1_minus_E"] = [st.mean(dd), lo, hi]
print(f"\nRev E1 - Rev E: {st.mean(dd):+.1f} points (95% range {lo:+.1f} to {hi:+.1f}); "
      f"{sum(1 for x in dd if x > 0)} voyages gained, {sum(1 for x in dd if x < 0)} lost")
fe = Counter(f for s in seeds for f in (E[s].get('failures') or []))
f1 = Counter(f for s in seeds for f in (E1[s].get('failures') or []))
def fname(f): return f if isinstance(f, str) else f.get('msg', str(f))
fe = Counter(fname(f) for s in seeds for f in (E[s].get('failures') or []))
f1 = Counter(fname(f) for s in seeds for f in (E1[s].get('failures') or []))
print("\nFailure events (all voyages), Rev E -> Rev E1:")
for k in sorted(set(fe) | set(f1), key=lambda k: -(fe[k] + f1[k]))[:14]:
    print(f"  {k[:60]:60s} {fe[k]:4d} -> {f1[k]:4d}")
out["failures"] = {k: [fe[k], f1[k]] for k in set(fe) | set(f1)}
# Cornwall end: closest approach of every voyage, and of the arrivals
print("\nCornwall end, Rev E1 (closest approach; the watch lines are approximate):")
out["watch"] = {}
for w in ("seven_stones", "scilly", "diamond_shoals"):
    allv = [E1[s]['watch_min_km'].get(w) for s in seeds if E1[s].get('watch_min_km')]
    allv = [x for x in allv if x is not None]
    arr = [E1[s]['watch_min_km'][w] for s in seeds if ok(E1[s]) and E1[s].get('watch_min_km', {}).get(w) is not None]
    share = {lim: 100*sum(x < lim for x in allv)/len(allv) for lim in (2, 5, 10)}
    sharea = {lim: 100*sum(x < lim for x in arr)/len(arr) for lim in (2, 5, 10)}
    out["watch"][w] = dict(all=share, arrivals=sharea, n=len(allv), median_km=st.median(allv))
    print(f"  {w:15s} all voyages <2/<5/<10 km: {share[2]:.0f}% / {share[5]:.0f}% / {share[10]:.0f}%   "
          f"arrivals: {sharea[2]:.0f}% / {sharea[5]:.0f}% / {sharea[10]:.0f}%   median {st.median(allv):.0f} km")
# Where the arrivals ended (rough areas)
def area(e):
    la, lo = e['lat'], e['lon']
    if 49.8 <= la <= 50.05 and -6.5 <= lo <= -6.15: return "Isles of Scilly"
    if 49.9 <= la <= 50.8 and -5.8 <= lo <= -3.5: return "Cornwall/Devon"
    if 51.3 <= la <= 55.5 and -10.6 <= lo <= -5.4: return "Ireland"
    if 48.0 <= la <= 49.0 and -5.3 <= lo <= -2.0: return "Brittany"
    if 50.0 <= la <= 51.9 and -5.6 <= lo <= -2.9: return "Bristol Channel/Wales"
    if 49.4 <= la <= 50.4 and -7.5 <= lo <= -5.0: return "off Cornwall/Scilly (target area)"
    return "elsewhere"
ends = Counter(area(E1[s]['end']) for s in seeds if ok(E1[s]))
out["arrival_areas"] = dict(ends)
print("\nWhere Rev E1 arrivals ended:", dict(ends.most_common()))
json.dump(out, open('docs/data/revE1_analysis.json', 'w'), indent=1)
