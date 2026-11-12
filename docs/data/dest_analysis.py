"""Summarise destination-study results (results/2026-11-12_dest_2023_<name>.json).

python docs/data/dest_analysis.py ireland_sw cornwall ...   (first name is the paired baseline)
Success = arrived_reporting + arrived_tracked. Runs share launch dates and seeds, so differences are paired.
"""
import json, sys, math, random, statistics as st
from collections import Counter

REGIONS = [  # (name, lat0, lat1, lon0, lon1); first match wins
    ("Azores", 36.5, 40.0, -32.0, -24.5), ("Madeira", 32.0, 33.5, -17.6, -16.0),
    ("Canaries", 27.3, 29.6, -18.5, -13.0), ("Ireland", 51.2, 55.6, -11.0, -5.9),
    ("Great Britain", 49.6, 61.0, -8.7, 2.0), ("France", 42.3, 51.3, -5.5, 8.5),
    ("Portugal", 36.8, 42.2, -10.0, -6.2), ("Spain", 35.8, 44.0, -10.0, 4.5),
    ("Africa", 14.0, 37.5, -18.5, 12.0), ("Iceland/Faroes", 61.0, 67.5, -25.0, -6.0),
    ("Norway", 57.5, 72.0, 4.0, 32.0)]

def region(lat, lon):
    for n, a, b, c, d in REGIONS:
        if a <= lat <= b and c <= lon <= d:
            return n
    return "other"

def load(name):
    return json.load(open(f"results/2026-11-12_dest_2023_{name}.json"))["result"]

def ok(r):
    return r["outcome"] in ("arrived_reporting", "arrived_tracked")

def boot_ci(x, n=4000, seed=1):
    rnd = random.Random(seed); m = len(x)
    s = sorted(sum(x[rnd.randrange(m)] for _ in range(m)) / m for _ in range(n))
    return s[int(0.025 * n)], s[int(0.975 * n)]

def main(names):
    base = {r["seed"]: ok(r) for r in load(names[0])["runs"]}
    rows = []
    for nm in names:
        d = load(nm); s = d["summary"]; runs = d["runs"]; n = len(runs)
        oc = Counter(r["outcome"] for r in runs)
        arr = [r for r in runs if r["outcome"].startswith("arrived")]
        tgt = d["scenario"]["target"]
        # arrivals inside the 40 km arrival circle but still at sea count for the aim point's country
        land = Counter((region(r["end"]["lat"], r["end"]["lon"]) if region(r["end"]["lat"], r["end"]["lon"]) != "other"
                        else region(tgt["lat"], tgt["lon"])) for r in arr if ok(r))
        days = [r["days"] for r in runs if ok(r)]
        diff = [100 * (ok(r) - base[r["seed"]]) for r in runs if r["seed"] in base]
        lo, hi = boot_ci(diff) if nm != names[0] else (0, 0)
        causes = Counter(f.split(":")[0].split(" (")[0] for r in runs for f in r["failures"][:1])
        rows.append(dict(name=nm, target=d["scenario"]["target"], succ=s["success_percent"], ci=s["success_ci95"],
                         any=s["any_arrival_percent"], lost=100 * oc["lost"] / n, aground=100 * oc["aground"] / n,
                         sea=100 * oc["at_sea_timeout"] / n, med=st.median(days) if days else None,
                         paired=(st.mean(diff), lo, hi), land=dict(land.most_common()), causes=dict(causes.most_common(5))))
    return rows

if __name__ == "__main__":
    rows = main(sys.argv[1:])
    rows_sorted = sorted(rows, key=lambda r: -r["succ"])
    print("| Aim point | Success (95% range) | vs %s, paired | Any landfall | Median days | Lost | Aground | At sea | Where successes landed |".replace("%s", sys.argv[1]))
    print("|---|---|---|---|---|---|---|---|---|")
    for r in rows_sorted:
        p = r["paired"]; pd = "—" if r["name"] == sys.argv[1] else f"{p[0]:+.1f} ({p[1]:+.1f} to {p[2]:+.1f})"
        land = ", ".join(f"{k} {v}" for k, v in r["land"].items())
        print(f"| {r['name']} | {r['succ']:.1f}% ({r['ci'][0]:.0f}–{r['ci'][1]:.0f}) | {pd} | {r['any']:.1f}% | {r['med']:.0f} | {r['lost']:.1f}% | {r['aground']:.1f}% | {r['sea']:.1f}% | {land} |")
    print()
    for r in rows_sorted:
        print(r["name"], r["target"], "first failures:", r["causes"])
