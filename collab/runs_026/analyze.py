"""Analysis of runs 026, 027, 029, 030 and 031 (21-22 Nov 2026). Run from the repo root: python collab/runs_026/analyze.py
Writes collab/runs_026/analysis.json. Run 028 (holding) is analysed by hold_analysis.py once it has run."""
import json, math, random, statistics as st, sys
from collections import Counter
sys.path.insert(0, 'simulator')
from drone_sim.storms import StormClimatology

ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
HOLD = (49.85, -5.20)
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2*6371*math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
def boot(x, n=4000):
    rnd = random.Random(1); m = len(x)
    v = sorted(sum(x[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
def load(p): return {r['seed']: r for r in json.load(open(p))['result']['runs']}
def reached(r): return ok(r) and km((r['end']['lat'], r['end']['lon']), HOLD) <= 3.5
def year(r): return int(r['start_time'][:4])
def paired(A, B, f=ok):
    s = sorted(set(A) & set(B)); d = [100*(f(A[k]) - f(B[k])) for k in s]; lo, hi = boot(d); return st.mean(d), lo, hi, len(s)
def msg(f): return f.get('msg', '') if isinstance(f, dict) else str(f)
def wingfail(r): return any(msg(f).startswith('Wing damaged') for f in r.get('failures', []))
def failures(runs):
    c = Counter()
    for r in runs:
        for f in r.get('failures', []):
            c[msg(f).split(':')[0].split(' (')[0][:60]] += 1
    return c
out = {}
R = 'results/2026-11-21_'

# ------------------------------------------------------------------ 026: the final plan on four years
P = load(R + 'plan026_2021-2024_revE1_lizard_offing_v2.json'); runs = list(P.values())
clim = StormClimatology()
LOSS = {'TS': 0.30, 'HU': 0.70}                 # grade-D storm loss model (docs/Hurricane_Risk.md), storm within 100 km
adj, enc_ts, enc_hu = [], 0, 0
for r in runs:
    tr = r.get('track'); loss = 0.0
    if tr and len(tr[0]) >= 3:
        # actual-year storms only: the voyage's own season (not the climatology average)
        v = [x for x in clim.voyage(tr, r['start_time'], 100.0) if x[0] == year(r)]
        w = max([x[1] for x in v], default=0)
        if w >= 64: enc_hu += 1; loss = LOSS['HU']
        elif w >= 34: enc_ts += 1; loss = LOSS['TS']
    adj.append(100*ok(r)*(1 - loss))
succ = [100*ok(r) for r in runs]; rch = [100*reached(r) for r in runs]
by_year = {y: dict(success=st.mean([100*ok(r) for r in runs if year(r) == y]), reached=st.mean([100*reached(r) for r in runs if year(r) == y]),
                   n=sum(year(r) == y for r in runs)) for y in sorted({year(r) for r in runs})}
W = {}
for k in ("seven_stones", "scilly", "wolf_rock", "runnelstone", "lizard_point", "manacles"):
    v = [r['watch_min_km'].get(k) for r in runs if r.get('watch_min_km')]
    W[k] = 100*sum(x is not None and x < 1 for x in v)/len(runs)
days = sorted(r['days'] for r in runs if ok(r))
out['026'] = dict(n=len(runs), success=st.mean(succ), ci=boot(succ), reached=st.mean(rch), reached_ci=boot(rch), by_year=by_year,
                  outcomes=dict(Counter(r['outcome'] for r in runs)), within_1km=W, days_median=st.median(days), days_p90=days[int(.9*len(days))],
                  storm_ts_100km=100*enc_ts/len(runs), storm_hu_100km=100*enc_hu/len(runs), after_storm_losses=st.mean(adj),
                  knockdowns_mean=st.mean(r['knockdowns'] for r in runs), failures=dict(failures(runs).most_common(8)))
o = out['026']
print(f"026 final plan, 1000 voyages 1-20 May 2021-24: success {o['success']:.1f}% ({o['ci'][0]:.1f}-{o['ci'][1]:.1f}), reached the Lizard hold "
      f"{o['reached']:.1f}% ({o['reached_ci'][0]:.1f}-{o['reached_ci'][1]:.1f}); after storm losses {o['after_storm_losses']:.1f}%")
print("   by year", {y: (round(v['success'], 1), round(v['reached'], 1)) for y, v in by_year.items()})
print("   outcomes", o['outcomes'], "| within 1 km", {k: round(v, 1) for k, v in W.items()}, "| days", o['days_median'], o['days_p90'])
print(f"   actual-year storm within 100 km: TS {o['storm_ts_100km']:.1f}%, hurricane {o['storm_hu_100km']:.1f}%")
print("   failures", o['failures'])

# ------------------------------------------------------------------ 027: DFM sensitivities, paired with run 025
B = load('results/2026-11-19_arrival_2023+2024_revE1_hatteras_stream__lizard_offing_hold_v2.json')
out['027'] = {'base_025': dict(success=st.mean([100*ok(r) for r in B.values()]), reached=st.mean([100*reached(r) for r in B.values()]))}
print(f"\n027 vs run 025 (base success {out['027']['base_025']['success']:.1f}%, reached {out['027']['base_025']['reached']:.1f}%):")
for tag in ('solar30', 'solar20', 'spar3026'):
    V = load(R + f'dfm027_2023+2024_revE1_{tag}_lizard_offing_v2.json'); vr = list(V.values())
    d = paired(V, B); dr = paired(V, B, reached)
    soc = [r['stats'].get('min_soc') for r in vr if r.get('stats', {}).get('min_soc') is not None]
    wing = sum(wingfail(r) for r in vr); wing_b = sum(wingfail(r) for r in B.values())
    out['027'][tag] = dict(success=st.mean([100*ok(r) for r in vr]), paired=d[:3], reached=st.mean([100*reached(r) for r in vr]), reached_paired=dr[:3],
                           outcomes=dict(Counter(r['outcome'] for r in vr)), wing_failures=wing, wing_failures_025=wing_b,
                           min_soc_median=st.median(soc) if soc else None, failures=dict(failures(vr).most_common(6)))
    o = out['027'][tag]
    print(f"   {tag:9s} success {o['success']:.1f}% ({d[0]:+.1f}, {d[1]:+.1f} to {d[2]:+.1f}); reached {o['reached']:.1f}% ({dr[0]:+.1f}, {dr[1]:+.1f} to {dr[2]:+.1f}); "
          f"wing failures {wing} vs {wing_b}; min SoC median {o['min_soc_median']}")
    print("            ", o['outcomes'], o['failures'])

# ------------------------------------------------------------------ 029: Rev C5 on boat-sim's 46 daily launches
out['029'] = {}
for tag in ('their_way', 'ours_46'):
    V = list(load(R + f'c5_029_2023_{tag}.json').values())
    ends = Counter()
    for r in V:
        la, lo = r['end']['lat'], r['end']['lon']
        if r['outcome'] == 'aground':
            ends["Nova Scotia" if 43 <= la <= 47.2 and -67 <= lo <= -59.5 else "Newfoundland" if 46.5 <= la <= 52 and -59.5 < lo <= -52
                 else "Maryland/Delaware/Virginia" if la < 39.5 and lo < -74 else "New England/Long Island" if lo < -67 else f"other ({la:.1f},{lo:.1f})"] += 1
    out['029'][tag] = dict(n=len(V), success=100*sum(ok(r) for r in V)/len(V), arrived=sum(ok(r) for r in V),
                           outcomes=dict(Counter(r['outcome'] for r in V)), aground_where=dict(ends),
                           days_median=st.median([r['days'] for r in V]))
    o = out['029'][tag]
    print(f"\n029 {tag}: {o['arrived']}/{o['n']} ({o['success']:.1f}%) outcomes {o['outcomes']} aground {o['aground_where']}")

# ------------------------------------------------------------------ 030: model fixes, paired with 026
out['030'] = {}
for tag in ('both', 'storm', 'severity'):
    V = load(R + f'fix030_2021-2024_revE1_{tag}.json'); vr = list(V.values())
    d = paired(V, P); dr = paired(V, P, reached)
    sh = [r.get('storm_hours', 0) for r in vr if 'storm_hours' in r]
    kd = st.mean(r['knockdowns'] for r in vr); kdb = st.mean(P[s]['knockdowns'] for s in V)
    wing = sum(wingfail(r) for r in vr); wing_b = sum(wingfail(P[s]) for s in V)
    out['030'][tag] = dict(n=len(vr), success=st.mean([100*ok(r) for r in vr]), paired=d[:3], reached_paired=dr[:3],
                           storm_hours_voyages=(sum(h > 0 for h in sh), len(sh)), storm_hours_mean_when_any=st.mean([h for h in sh if h > 0]) if any(h > 0 for h in sh) else 0,
                           storm_max_factor=max([r.get('storm_max_factor', 1) for r in vr], default=1), knockdowns=kd, knockdowns_026=kdb,
                           wing_failures=wing, wing_failures_026=wing_b, outcomes=dict(Counter(r['outcome'] for r in vr)))
    o = out['030'][tag]
    print(f"\n030 {tag} ({o['n']}): success {o['success']:.1f}% ({d[0]:+.1f}, {d[1]:+.1f} to {d[2]:+.1f} vs 026 same seeds); reached {dr[0]:+.1f}; "
          f"storm hours on {o['storm_hours_voyages']} voyages (mean {o['storm_hours_mean_when_any']:.0f} h, max factor {o['storm_max_factor']}); "
          f"knockdowns {kd:.1f} vs {kdb:.1f}; wing failures {wing} vs {wing_b}")
    print("    ", o['outcomes'])

json.dump(out, open('collab/runs_026/analysis.json', 'w'), indent=1, default=float)
