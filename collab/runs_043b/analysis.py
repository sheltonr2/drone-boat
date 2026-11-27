"""Run 043b analysis (27 Nov 2026), v2 coasts, Rev E3, four years.
1. Approaches about 60 and 90 km south of Scilly (B60, B90), each paired with 043a B (about 40-45 km south).
2. Holding upwind of each pickup point: station-keeping 14 days at a point 15-40 km up-wind, with every distance
   measured from the PICKUP point itself, against holding on the point (043a). P(pickup) = P(arrive) x P(afloat by day).
3. Mindelo launch windows (15 Nov-10 Dec, 11 Dec-10 Jan) to the Norman offing and Anegada W, against 043a's
   15 Nov-10 Jan. The 11 Jan-5 Feb window did not run: its voyages reach July 2022/2023, which the east-west weather
   workspace does not hold yet.
Usage: python collab/runs_043b/analysis.py [results dir]  -> collab/runs_043b/analysis.json
"""
import json, os, random, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "runs_026")); sys.path.insert(0, os.path.join(HERE, "..", "runs_036"))
from hold_analysis import val, where, analyse, km  # noqa: E402
from hold_analysis_036_037 import where_bvi  # noqa: E402
from pickup_analysis import survive  # noqa: E402
RD = sys.argv[1] if len(sys.argv) > 1 else "results"
ok = lambda r: r["outcome"] in ("arrived_reporting", "arrived_tracked")
def F(n): return os.path.join(RD, n)
def runs(n): return json.load(open(F(n)))["result"]["runs"]


def boot(x, n=3000):
    rnd = random.Random(1); m = len(x)
    v = sorted(sum(x[rnd.randrange(m)] for _ in range(m)) / m for _ in range(n)); return round(sum(x) / m, 1), round(v[int(.025 * n)], 1), round(v[int(.975 * n)], 1)


def place(e):
    if e["lon"] < -60 and e["lat"] > 30: return "Hatteras"
    if e["lon"] < -60: return where_bvi(e["lat"], e["lon"])
    if e["lat"] > 45: return where(e["lat"], e["lon"])
    return f"east Atlantic ({e['lat']:.2f}N {-e['lon']:.2f}W)"


def crossing(n, twin=None, paired=True):
    R = runs(n); x = [100 * ok(r) for r in R]
    g = Counter(place(val(r["end"])) for r in R if r["outcome"] == "aground")
    out = dict(n=len(R), arrive=boot(x), aground=round(100 * sum(r["outcome"] == "aground" for r in R) / len(R), 1),
               groundings=dict(g.most_common()), days_median=sorted(float(r["days"]) for r in R if ok(r))[sum(map(ok, R)) // 2])
    sp = F(n[:-5] + "_storms.json")
    if os.path.exists(sp): out["storm_p_any"] = json.load(open(sp))["table"]["all"]["p_any"]
    if twin:
        T = runs(twin)
        if paired:
            t = {r["seed"]: ok(r) for r in T}
            out["vs_twin"] = boot([100 * (ok(r) - t[r["seed"]]) for r in R if r["seed"] in t])
        else:
            out["twin_arrive"] = boot([100 * ok(r) for r in T])
    return out


def hold(n, pickup):
    """Hold statistics with distances from the pickup point (not the holding point)."""
    a = analyse(F(n), pickup); R = runs(n)
    g = Counter(place(val(r["end"])) for r in R if r["outcome"] == "aground")
    return dict(percent=a["percent"], afloat=survive(F(n)), groundings=dict(g.most_common()),
                end_km_from_pickup=a["end_distance_km"], max_km_from_pickup=a["max_distance_km"],
                days_to_aground=a.get("days_to_aground"))


P43a, P = "2026-11-27_plan043a_2021-2024_revE3_", "2026-11-27_plan043b_2021-2024_revE3_"
res = dict(east={}, holds={}, pickup={}, mindelo={})
res["east"]["B_043a"] = crossing(P43a + "B_v2.json")
for t in ("B60", "B90"):
    res["east"][t] = crossing(P + f"{t}_v2.json", P43a + "B_v2.json")

PICK = dict(norman_offing=(18.17, -64.58), anegada_west=(18.72, -64.49), lizard_deep=(49.70, -5.20))
HOLDS = dict(norman_offing=["E20", "E40", "ESE20"], anegada_west=["N15", "N30"], lizard_deep=["SW20", "W20"])
ARR = dict(norman_offing=crossing("2026-11-27_ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json")["arrive"][0],
           anegada_west=crossing("2026-11-27_ew043a_2021-2024_revE3_mindelo__anegada_west_v2.json")["arrive"][0],
           lizard_deep=res["east"]["B_043a"]["arrive"][0])
for pt, tags in HOLDS.items():
    yrs = "2021-2024" if pt == "lizard_deep" else "2022-2025"
    cases = {"on_point": f"2026-11-27_hold043a_{yrs}_revE3_station_{pt}_v2.json"}
    cases.update({t: f"2026-11-27_hold043b_{yrs}_revE3_station_{pt}_{t}_v2.json" for t in tags})
    for tag, fn in cases.items():
        h = hold(fn, PICK[pt]); k = f"{pt}_{tag}"; res["holds"][k] = h
        res["pickup"][k] = {d: round(ARR[pt] * h["afloat"][d] / 100, 1) for d in (1, 3, 7)}

for t in ("norman_offing", "anegada_west"):
    base = f"2026-11-27_ew043a_2021-2024_revE3_mindelo__{t}_v2.json"
    res["mindelo"][f"nov15-jan10__{t}"] = crossing(base)
    for w in ("nov", "dec"):
        res["mindelo"][f"{w}__{t}"] = crossing(f"2026-11-27_ew043b_2021-2024_revE3_mindelo_{w}__{t}_v2.json")
res["mindelo"]["jan"] = "not run: needs Jul 2022 and Jul 2023 in the east-west weather workspace"

json.dump(res, open(os.path.join(HERE, "analysis.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
