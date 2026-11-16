"""Arrival study (run 021b, 16 Nov 2026; docs/Launch_Plan.md "Arrival and holding"): Rev E1, 45 km off Hatteras ->
holding points in Falmouth Bay and Mount's Bay, 500 voyages each, 2023+2024, the same seeds as run 017. Run from the repo root."""
import json, math, random, statistics as st
from collections import Counter
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2*6371*math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
def boot(x, n=4000):
    rnd = random.Random(1); m = len(x); v = sorted(sum(x[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
def L(p): return {r['seed']: r for r in json.load(open(p))['result']['runs']}
base = L('results/2026-11-14_plan_2023+2024_revE1_hatteras_stream__cornwall.json')
HOLD = {"falmouth_hold": (50.100, -4.990), "mounts_bay_hold": (50.050, -5.480)}
NAME = {"falmouth_hold": "Falmouth Bay", "mounts_bay_hold": "Mount's Bay"}
def area(e):
    la, lo = e['lat'], e['lon']
    if 49.8 <= la <= 50.05 and -6.5 <= lo <= -6.15: return "Isles of Scilly"
    if 49.9 <= la <= 50.4 and -5.75 <= lo <= -4.5: return "Cornwall (Land's End-Falmouth)"
    if 50.1 <= la <= 50.8 and -4.5 < lo <= -3.0: return "Cornwall/Devon east of Falmouth"
    if 50.0 <= la <= 51.9 and -5.75 <= lo <= -2.9: return "Cornwall north coast/Bristol Channel"
    if 51.3 <= la <= 55.5 and -10.6 <= lo <= -5.4: return "Ireland"
    if 47.0 <= la <= 49.0 and -5.3 <= lo <= -1.0: return "Brittany"
    return "elsewhere / offshore"
out = {}
for tag in HOLD:
    R = L(f'results/2026-11-16_arrival_2023+2024_revE1_hatteras_stream__{tag}.json'); seeds = sorted(set(R) & set(base))
    runs = [R[s] for s in seeds]
    reach = [km((r['end']['lat'], r['end']['lon']), HOLD[tag]) <= 3.5 and ok(r) for r in runs]
    succ = [100*ok(r) for r in runs]; lo, hi = boot(succ)
    dd = [100*(ok(R[s]) - ok(base[s])) for s in seeds]; dlo, dhi = boot(dd)
    rlo, rhi = boot([100*x for x in reach])
    # voyages that were arrivals in run 017 (stopped 40 km off Scilly): what happened on the extra leg?
    was = [s for s in seeds if ok(base[s])]
    after = Counter("reached holding point" if (ok(R[s]) and km((R[s]['end']['lat'], R[s]['end']['lon']), HOLD[tag]) <= 3.5)
                    else ("landfall elsewhere (counts as arrival)" if ok(R[s]) else R[s]['outcome']) for s in was)
    ends = Counter(area(r['end']) for r in runs if ok(r) and not km((r['end']['lat'], r['end']['lon']), HOLD[tag]) <= 3.5)
    lost_near = sum(1 for r in runs if r['outcome'] in ('aground', 'lost') and 49.7 <= r['end']['lat'] <= 50.4 and -6.8 <= r['end']['lon'] <= -4.5)
    d_extra = [R[s]['days'] - base[s]['days'] for s in was if ok(R[s])]
    W = {}
    for k in ("seven_stones", "scilly", "wolf_rock", "runnelstone", "lizard_point", "manacles", "low_lee_mountamopus"):
        v = [r['watch_min_km'].get(k) for r in runs if r.get('watch_min_km')]
        v = [x for x in v if x is not None]
        W[k] = {lim: 100*sum(x < lim for x in v)/len(runs) for lim in (1, 2, 5)}
    o = dict(name=NAME[tag], success=st.mean(succ), ci95=[lo, hi], vs_017=[st.mean(dd), dlo, dhi], reached_holding=100*st.mean(reach),
             reached_ci95=[rlo, rhi], of_017_arrivals=dict(after), n_017_arrivals=len(was), other_landfalls=dict(ends.most_common()),
             lost_or_aground_near_cornwall=lost_near, extra_days_median=st.median(d_extra) if d_extra else None,
             outcomes=dict(Counter(r['outcome'] for r in runs)), watch=W)
    out[tag] = o
    print(f"\n{o['name']}: success {o['success']:.1f}% ({lo:.1f}-{hi:.1f}); vs run 017 (stop 40 km off Scilly) {o['vs_017'][0]:+.1f} ({dlo:+.1f} to {dhi:+.1f})")
    print(f"   reached the holding point: {o['reached_holding']:.1f}% of all voyages ({rlo:.1f}-{rhi:.1f})")
    print(f"   of the {len(was)} voyages that arrived in run 017: {dict(after)}; extra days to the holding point, median {o['extra_days_median']}")
    print(f"   other landfalls counted as arrivals: {o['other_landfalls']}; lost/aground near Cornwall: {lost_near}")
    print(f"   outcomes {o['outcomes']}")
    for k, v in W.items(): print(f"   {k:20s} <1 km {v[1]:.1f}%  <2 km {v[2]:.1f}%  <5 km {v[5]:.1f}%")
json.dump(out, open('docs/data/arrival_analysis.json', 'w'), indent=1)
