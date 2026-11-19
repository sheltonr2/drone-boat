"""East-west screen to the British Virgin Islands (run 022, 16 Nov 2026; docs/East_West_Study.md section 9).
Rev E1, 300 voyages per pair, launches 1 Nov 2024 - 15 Jan 2025 on 2024-25 weather, same seeds in every pair.
Run from the repo root."""
import json, math, random, statistics as st, datetime as dt
from collections import Counter, defaultdict
P = "results/2026-11-16_ew_2024_{}.json"
LAB = ["gran_canaria__bvi", "gran_canaria_south__bvi", "el_hierro__bvi", "mindelo__bvi", "madeira__bvi", "cadiz__bvi",
       "lisbon__bvi", "gran_canaria__bvi_weedx2", "gran_canaria__barbados"]
NAME = {"gran_canaria__bvi": "Gran Canaria -> BVI", "gran_canaria_south__bvi": "Gran Canaria via 20N 28W -> BVI",
        "el_hierro__bvi": "El Hierro -> BVI", "mindelo__bvi": "Mindelo (Cape Verde) -> BVI", "madeira__bvi": "Madeira -> BVI",
        "cadiz__bvi": "Cadiz -> BVI", "lisbon__bvi": "Lisbon -> BVI", "gran_canaria__bvi_weedx2": "Gran Canaria -> BVI, weed x2",
        "gran_canaria__barbados": "Gran Canaria -> Barbados"}
HOLD = (18.30, -64.58)
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2*6371*math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
def area(e):
    la, lo = e['lat'], e['lon']
    if km((la, lo), HOLD) <= 3.5: return "BVI holding point"
    if 18.15 <= la <= 18.85 and -64.85 <= lo <= -64.15: return "BVI (other)"
    if 17.6 <= la <= 18.7 and -67.4 <= lo <= -64.5: return "Puerto Rico / US Virgin Is."
    if 16.9 <= la <= 18.4 and -63.6 <= lo <= -61.5: return "Anguilla-Antigua"
    if 14.0 <= la < 16.9 and -62.0 <= lo <= -60.8: return "Guadeloupe-Martinique"
    if 11.8 <= la < 14.0 and -62.0 <= lo <= -59.3: return "Windward Is. / Barbados"
    if lo < -67.4 and la < 25: return "Hispaniola and west"
    if la < 11.8 and lo < -50: return "South America"
    return "elsewhere"
def boot(x, n=4000):
    rnd = random.Random(1); m = len(x); v = sorted(sum(x[rnd.randrange(m)] for _ in range(m))/m for _ in range(n)); return v[int(.025*n)], v[int(.975*n)]
R = {l: {r['seed']: r for r in json.load(open(P.format(l)))['result']['runs']} for l in LAB}
S = {l: json.load(open(P.format(l + "_storms")))['table'] for l in LAB}
ref = R["gran_canaria__bvi"]
out = {}
for l in LAB:
    runs = list(R[l].values()); x = [100*ok(r) for r in runs]; lo, hi = boot(x)
    seeds = sorted(set(R[l]) & set(ref))
    dd = [100*(ok(R[l][s]) - ok(ref[s])) for s in seeds]; dlo, dhi = boot(dd)
    days = sorted(r['days'] for r in runs if ok(r))
    arr_month = Counter()
    for r in runs:
        if ok(r):
            t = dt.datetime.fromisoformat(r['start_time']) + dt.timedelta(days=r['days']); arr_month[t.strftime('%b')] += 1
    by_launch = defaultdict(list)
    for r in runs:
        t = dt.datetime.fromisoformat(r['start_time']); key = f"{t.strftime('%b')} {1 + (t.day - 1)//15 * 15:02d}"
        by_launch[(t.year, t.month, 0 if t.day <= 15 else 1)].append(ok(r))
    weed = sum(1 for r in runs for f in (r.get('failures') or []) if 'weed' in (f if isinstance(f, str) else f.get('msg', '')).lower())
    areas = Counter(area(r['end']) for r in runs if ok(r))
    hold = sum(1 for r in runs if ok(r) and km((r['end']['lat'], r['end']['lon']), HOLD) <= 3.5)
    w = defaultdict(list)
    for r in runs:
        for k, v in (r.get('watch_min_km') or {}).items():
            if v is not None: w[k].append(v)
    o = dict(name=NAME[l], success=st.mean(x), ci95=[lo, hi], vs_gc=[st.mean(dd), dlo, dhi],
             days_median=st.median(days), days_p10=days[len(days)//10], days_p90=days[9*len(days)//10],
             arrivals=sum(map(ok, runs)), arrive_by_month=dict(arr_month),
             march_share_of_voyages=100*arr_month.get('Mar', 0)/len(runs),
             by_launch_halfmonth={f"{y}-{m:02d} {'1-15' if h == 0 else '16-end'}": [len(v), round(100*st.mean(v), 1)] for (y, m, h), v in sorted(by_launch.items())},
             outcomes=dict(Counter(r['outcome'] for r in runs)), weed_events_per_voyage=weed/len(runs),
             storm_any_200km=100*S[l]['all']['p_any'], storm_hurricane=100*(S[l]['all']['p_C1-2'] + S[l]['all']['p_C3-5']),
             landfall_areas=dict(areas.most_common()), reached_holding=100*hold/len(runs),
             watch={k: dict(n=len(v), within1=100*sum(a < 1 for a in v)/len(runs), within2=100*sum(a < 2 for a in v)/len(runs),
                            within5=100*sum(a < 5 for a in v)/len(runs)) for k, v in w.items()})
    out[l] = o
    print(f"\n{o['name']}: success {o['success']:.1f}% ({lo:.1f}-{hi:.1f}); vs Gran Canaria->BVI {o['vs_gc'][0]:+.1f} ({dlo:+.1f} to {dhi:+.1f})")
    print(f"   days median {o['days_median']:.0f} (p10 {o['days_p10']:.0f}, p90 {o['days_p90']:.0f}); arrivals by month {dict(sorted(arr_month.items(), key=lambda kv: dt.datetime.strptime(kv[0], '%b').month))}; "
          f"March arrivals {o['march_share_of_voyages']:.0f}% of voyages")
    print("   success by launch half-month:", ", ".join(f"{k}: {v[1]:.0f}% ({v[0]})" for k, v in o['by_launch_halfmonth'].items()))
    print(f"   outcomes {o['outcomes']}; weed events/voyage {o['weed_events_per_voyage']:.2f}; storm (TS+ within 200 km) {o['storm_any_200km']:.1f}%, hurricane {o['storm_hurricane']:.2f}%")
    print(f"   landfall areas {o['landfall_areas']}; reached BVI holding point {o['reached_holding']:.1f}%")
    for k, v in o['watch'].items():
        print(f"   {k}: <1 km {v['within1']:.1f}%, <2 km {v['within2']:.1f}%, <5 km {v['within5']:.1f}% of voyages")
json.dump(out, open('docs/data/ew_screen_analysis.json', 'w'), indent=1)
