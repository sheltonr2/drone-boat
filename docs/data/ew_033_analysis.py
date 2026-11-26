"""East-west runs 024 + 033 (26 Nov 2026; docs/East_West_Study.md section 12): the three best BVI pairs on four winters,
2021-22 and 2022-23 (run 033) plus 2023-24 and 2024-25 (run 024), 500 voyages per pair and pair of winters, same set-up.
Adapted from ew_024_analysis.py. Run from the repo root."""
import json, math, random, statistics as st, datetime as dt
from collections import Counter, defaultdict
HOLD = (18.30, -64.58)
F = {"mindelo": ["results/2026-11-26_ew033_2021+2022_mindelo__bvi_s.json", "results/2026-11-18_ew024_2023+2024_mindelo__bvi_s.json"],
     "gran_canaria_south": ["results/2026-11-26_ew033_2021+2022_gran_canaria_south__bvi_s.json", "results/2026-11-18_ew024_2023+2024_gran_canaria_south__bvi_s.json"],
     "el_hierro_south": ["results/2026-11-26_ew033_2021+2022_el_hierro_south__bvi_s.json", "results/2026-11-18_ew024_2023+2024_el_hierro_south__bvi_s.json"]}
NAME = {"mindelo": "Mindelo (Cape Verde), launches 15 Nov-10 Jan", "gran_canaria_south": "Gran Canaria via 20N 28W, launches 1 Nov-20 Dec",
        "el_hierro_south": "El Hierro via 20N 28W, launches 1 Nov-20 Dec"}
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2*6371*math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
def boot(x, n=4000):
    rnd = random.Random(1); m = len(x); v = sorted(sum(x[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
def season(r):
    t = dt.datetime.fromisoformat(r['start_time']); return f"{t.year}-{(t.year+1)%100:02d}" if t.month >= 7 else f"{t.year-1}-{t.year%100:02d}" if t.month < 7 and t.month <= 2 else str(t.year)
R = {k: {(j, r['seed']): r for j, p in enumerate(ps) for r in json.load(open(p))['result']['runs']} for k, ps in F.items()}
def storm_mix(ps):
    T = [json.load(open(p.replace('.json', '_storms.json')))['table']['all'] for p in ps]; n = sum(t['voyages'] for t in T)
    return {c: sum(t[c]*t['voyages'] for t in T)/n for c in ('p_any', 'p_TS', 'p_C1-2', 'p_C3-5')}
S = {k: storm_mix(ps) for k, ps in F.items()}
out = {}
for k, runs_d in R.items():
    runs = list(runs_d.values()); x = [100*ok(r) for r in runs]; lo, hi = boot(x)
    days = sorted(r['days'] for r in runs if ok(r))
    by_season = defaultdict(list)
    for r in runs: by_season[season(r)].append(ok(r))
    arr = Counter(); march = 0; launch_for_march = []
    by_half = defaultdict(list)
    for r in runs:
        t0 = dt.datetime.fromisoformat(r['start_time'])
        by_half[(t0.month, 0 if t0.day <= 15 else 1)].append(ok(r))
        if ok(r):
            t1 = t0 + dt.timedelta(days=r['days']); arr[t1.month] += 1
            if t1.month == 3: march += 1; launch_for_march.append(t0.timetuple().tm_yday if t0.month >= 7 else t0.timetuple().tm_yday + 365)
    hold = sum(1 for r in runs if ok(r) and km((r['end']['lat'], r['end']['lon']), HOLD) <= 3.5)
    weed = sum(1 for r in runs for f in (r.get('failures') or []) if 'weed' in (f if isinstance(f, str) else f.get('msg', '')).lower())
    w = defaultdict(list)
    for r in runs:
        for kk, v in (r.get('watch_min_km') or {}).items():
            if v is not None: w[kk].append(v)
    def doy(d):
        base = dt.date(2023, 1, 1) + dt.timedelta(days=d - 1); return base.strftime('%d %b')
    lm = sorted(launch_for_march)
    o = dict(name=NAME[k], n=len(runs), success=st.mean(x), ci95=[lo, hi],
             by_season={s: [len(v), 100*st.mean(v)] for s, v in sorted(by_season.items())},
             days_median=st.median(days), days_p10=days[len(days)//10], days_p90=days[9*len(days)//10],
             arrivals_by_month={dt.date(2000, m, 1).strftime('%b'): c for m, c in sorted(arr.items(), key=lambda kv: (kv[0] < 7, kv[0]))},
             march_share=100*march/len(runs),
             march_launch_p10_p50_p90=[doy(lm[len(lm)//10]), doy(lm[len(lm)//2]), doy(lm[9*len(lm)//10])] if lm else None,
             by_half_month={f"{dt.date(2000, m, 1).strftime('%b')} {'1-15' if h == 0 else '16-end'}": [len(v), 100*st.mean(v)] for (m, h), v in sorted(by_half.items(), key=lambda kv: (kv[0][0] < 7, kv[0]))},
             reached_hold=100*hold/len(runs), weed_per_voyage=weed/len(runs), outcomes=dict(Counter(r['outcome'] for r in runs)),
             storm_any=100*S[k]['p_any'], storm_hurricane=100*(S[k]['p_C1-2'] + S[k]['p_C3-5']), storm_major=100*S[k]['p_C3-5'],
             watch={kk: [100*sum(a < 1 for a in v)/len(runs), 100*sum(a < 2 for a in v)/len(runs)] for kk, v in w.items()})
    out[k] = o
    print(f"\n{o['name']}: success {o['success']:.1f}% ({lo:.1f}-{hi:.1f}); by season " + ", ".join(f"{s}: {v[1]:.1f}% of {v[0]}" for s, v in o['by_season'].items()))
    print(f"   days {o['days_median']:.0f} (p10 {o['days_p10']:.0f}, p90 {o['days_p90']:.0f}); arrivals by month {o['arrivals_by_month']}; March {o['march_share']:.0f}% of voyages; "
          f"launch dates of March arrivals p10/p50/p90 {o['march_launch_p10_p50_p90']}")
    print("   by launch half-month: " + ", ".join(f"{h}: {v[1]:.0f}% ({v[0]})" for h, v in o['by_half_month'].items()))
    print(f"   reached BVI hold {o['reached_hold']:.1f}%; weed/voyage {o['weed_per_voyage']:.2f}; storm TS+ within 200 km {o['storm_any']:.1f}%, hurricane {o['storm_hurricane']:.1f}% (major {o['storm_major']:.1f}%)")
    print(f"   outcomes {o['outcomes']}; within 1/2 km: " + ", ".join(f"{kk} {v[0]:.1f}/{v[1]:.1f}%" for kk, v in o['watch'].items()))
# Paired comparisons (same seeds, same launch dates only where the windows match: Gran Canaria and El Hierro)
def pair(a, b):
    s = sorted(set(R[a]) & set(R[b])); d = [100*(ok(R[a][i]) - ok(R[b][i])) for i in s]; l, h = boot(d); return st.mean(d), l, h, len(s)
print()
for a, b in (("mindelo", "gran_canaria_south"), ("mindelo", "el_hierro_south"), ("el_hierro_south", "gran_canaria_south")):
    m, l, h, n = pair(a, b); out[f"{a}_vs_{b}"] = [m, l, h]
    print(f"{a} minus {b}: {m:+.1f} points ({l:+.1f} to {h:+.1f}), {n} paired seeds")
json.dump(out, open('docs/data/ew_033_analysis.json', 'w'), indent=1)
