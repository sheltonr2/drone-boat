"""Run 043a analysis (27 Nov 2026): the decided plans on the v2 coastlines (EMODnet + UKHO depth data), each paired
with its v1 twin from runs 036-042 (same launches and seeds), so the difference is the depth data's effect.
Usage: python collab/runs_043a/analysis.py [results dir]  -> collab/runs_043a/analysis.json
"""
import json, os, random, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "runs_026")); sys.path.insert(0, os.path.join(HERE, "..", "runs_036"))
from hold_analysis import val, where, analyse  # noqa: E402
from hold_analysis_036_037 import spread, where_bvi  # noqa: E402
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
    out = dict(arrive=boot(x), aground=round(100 * sum(r["outcome"] == "aground" for r in R) / len(R), 1),
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


def hold(n, pt, twin):
    a = analyse(F(n), pt); a.update(spread(F(n), pt)); a["afloat_by_day"] = survive(F(n))
    b = analyse(F(twin), pt)
    return dict(percent=a["percent"], r50=a["r50_km"], r90=a["r90_km"], afloat=a["afloat_by_day"], days_to_aground=a.get("days_to_aground"),
                twin_percent=b["percent"], twin_afloat=survive(F(twin)))


P, V1 = "2026-11-27_plan043a_2021-2024_revE3_", "2026-11-26_"
res = dict(east={}, holds_cornwall={}, ew={}, holds_bvi={})
E = res["east"]
E["B"] = crossing(P + "B_v2.json", V1 + "plan042_2021-2024_revE3_south_lizard_deep_detail.json")
E["A"] = crossing(P + "A_v2.json", V1 + "plan042_2021-2024_revE3_south_lizard_offing_detail.json")
E["old"] = crossing(P + "old_v2.json", V1 + "plan039_2021-2024_revE3_lizard_offing_detail.json")
E["B_drop70"] = crossing(P + "B_drop70_v2.json", P + "B_v2.json")
E["B_april"] = crossing(P + "B_april_v2.json", P + "B_v2.json", paired=False)
E["B_latemay"] = crossing(P + "B_latemay_v2.json", P + "B_v2.json", paired=False)
Bv = {r["seed"]: ok(r) for r in runs(P + "B_v2.json")}
E["B_minus_A_v2"] = boot([100 * (Bv[r["seed"]] - ok(r)) for r in runs(P + "A_v2.json")])
E["B_minus_old_v2"] = boot([100 * (Bv[r["seed"]] - ok(r)) for r in runs(P + "old_v2.json")])
for tag, pt in (("lizard_deep", (49.70, -5.20)), ("lizard", (49.85, -5.20))):
    for mode in ("station", "drift"):
        res["holds_cornwall"][f"{mode}_{tag}"] = hold(f"2026-11-27_hold043a_2021-2024_revE3_{mode}_{tag}_v2.json", pt, f"{V1}hold037_2021-2024_revE3_{mode}_{tag}.json")
for tag in ("norman_offing", "anegada_west"):
    res["ew"][f"mindelo__{tag}"] = crossing(f"2026-11-27_ew043a_2021-2024_revE3_mindelo__{tag}_v2.json", f"{V1}ew038_2021-2024_revE3_mindelo__{tag}.json")
res["ew"]["el_hierro_south__norman_offing"] = crossing("2026-11-27_ew043a_2021-2024_revE3_el_hierro_south__norman_offing_v2.json",
                                                       "2026-11-27_ew043a_2021-2024_revE3_mindelo__norman_offing_v2.json", paired=False)
for tag, pt in (("norman_offing", (18.17, -64.58)), ("anegada_west", (18.72, -64.49))):
    for mode in ("station", "drift"):
        res["holds_bvi"][f"{mode}_{tag}"] = hold(f"2026-11-27_hold043a_2022-2025_revE3_{mode}_{tag}_v2.json", pt, f"{V1}hold036_2022-2025_revE3_{mode}_{tag}.json")
for tag in ("norman_offing", "anegada_west"):
    a = res["ew"][f"mindelo__{tag}"]["arrive"][0]; s = res["holds_bvi"][f"station_{tag}"]["afloat"]
    res["ew"][f"mindelo__{tag}"]["p_pickup"] = {d: round(a * s[d] / 100, 1) for d in (1, 3, 7)}
b = E["B"]["arrive"][0]; s = res["holds_cornwall"]["station_lizard_deep"]["afloat"]
E["B"]["p_pickup"] = {d: round(b * s[d] / 100, 1) for d in (1, 3, 7)}
a = E["A"]["arrive"][0]; s = res["holds_cornwall"]["station_lizard"]["afloat"]
E["A"]["p_pickup"] = {d: round(a * s[d] / 100, 1) for d in (1, 3, 7)}
json.dump(res, open(os.path.join(HERE, "analysis.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
