"""Run 028: holding study at the Lizard offing (49.85N 5.20W) and the mouth of Mount's Bay (49.97N 5.45W), Rev E1,
2021-2024 weather, 500 voyages each, arrival season (mid-August to mid-October launches into the hold).

  station: the autopilot starts in station mode and holds for 14 days, failures on (planning rates);
  drift:   a dead boat from the same point for 30 days, no failures (it is already dead).

Usage: python collab/runs_026/hold_analysis.py <results dir>   (default: results)
Writes collab/runs_026/hold_analysis.json and prints a summary.
"""
import ast, json, math, os, sys
from statistics import median

HOLDS = {"lizard": (49.85, -5.20), "mounts": (49.97, -5.45)}
NAMES = {"lizard": "Lizard offing", "mounts": "Mount's Bay mouth"}


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def val(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except Exception:  # noqa: BLE001
            return x
    return x


def where(lat, lon):
    """Rough name for where a grounded boat ends up."""
    if lon < -5.9: return "Isles of Scilly / west of Land's End"
    if lon < -5.55: return "Land's End to Penzance (west of Mount's Bay)"
    if lon < -5.25 and lat > 49.98: return "inside Mount's Bay"
    if lon < -5.1: return "Lizard peninsula"
    if lon < -4.95: return "Manacles to Falmouth"
    if lon < -4.4: return "Falmouth to Plymouth"
    if lon < -2.0: return "Devon / Dorset"
    return "further east / France"


def pct(a, n):
    return round(100.0 * a / n, 1) if n else 0.0


def q(xs, p):
    xs = sorted(xs)
    return round(xs[min(len(xs) - 1, int(p * len(xs)))], 1) if xs else None


def analyse(path, hold):
    d = json.load(open(path)); runs = d["result"]["runs"]; n = len(runs)
    out = dict(runs=n, outcomes={}, groundings={}, watch_within_1km={}, watch_within_2km={})
    maxd, t5, t10, ever5, ever10 = [], [], [], 0, 0
    aground_days, end_d = [], []
    wmin = {}
    for r in runs:
        oc = r["outcome"]; out["outcomes"][oc] = out["outcomes"].get(oc, 0) + 1
        tr = val(r["track"])
        ds = [km(hold, (p[0], p[1])) for p in tr]
        if len(tr) > 1:
            dt = [tr[i + 1][2] - tr[i][2] for i in range(len(tr) - 1)]
            tot = sum(dt) or 1
            t5.append(100 * sum(dt[i] for i in range(len(dt)) if ds[i] > 5) / tot)
            t10.append(100 * sum(dt[i] for i in range(len(dt)) if ds[i] > 10) / tot)
        m = max(ds) if ds else 0; maxd.append(m); ever5 += m > 5; ever10 += m > 10
        e = val(r["end"]); end_d.append(km(hold, (e["lat"], e["lon"])))
        if oc == "aground":
            w = where(e["lat"], e["lon"]); out["groundings"][w] = out["groundings"].get(w, 0) + 1
            aground_days.append(float(r["days"]))
        for k, v in (val(r.get("watch_min_km")) or {}).items():
            wmin.setdefault(k, []).append(float(v))
    out["percent"] = {k: pct(v, n) for k, v in out["outcomes"].items()}
    out["max_distance_km"] = dict(median=q(maxd, 0.5), p90=q(maxd, 0.9))
    out["end_distance_km"] = dict(median=q(end_d, 0.5), p90=q(end_d, 0.9))
    out["time_beyond_5km_percent"] = dict(median=q(t5, 0.5), p90=q(t5, 0.9))
    out["time_beyond_10km_percent"] = dict(median=q(t10, 0.5), p90=q(t10, 0.9))
    out["runs_ever_beyond_5km_percent"] = pct(ever5, n); out["runs_ever_beyond_10km_percent"] = pct(ever10, n)
    if aground_days:
        out["days_to_aground"] = dict(p10=q(aground_days, 0.1), median=q(aground_days, 0.5), p90=q(aground_days, 0.9))
    for k, v in wmin.items():
        out["watch_within_1km"][k] = pct(sum(x < 1 for x in v), n)
        out["watch_within_2km"][k] = pct(sum(x < 2 for x in v), n)
    out["failure_causes"] = d["result"]["summary"].get("failure_causes", {})
    return out


def main():
    rd = sys.argv[1] if len(sys.argv) > 1 else "results"
    res = {}
    for mode in ("station", "drift"):
        for h, pt in HOLDS.items():
            f = os.path.join(rd, f"hold028_2021-2024_revE1_{mode}_{h}.json")
            res[f"{mode}_{h}"] = a = analyse(f, pt)
            print(f"\n== {mode} at {NAMES[h]}: {a['runs']} runs")
            print("  outcomes %:", a["percent"])
            print("  max distance from hold km:", a["max_distance_km"], " end distance:", a["end_distance_km"])
            print("  time beyond 5 km %:", a["time_beyond_5km_percent"], " beyond 10 km %:", a["time_beyond_10km_percent"],
                  " runs ever >5 km:", a["runs_ever_beyond_5km_percent"], " >10 km:", a["runs_ever_beyond_10km_percent"])
            print("  groundings:", a["groundings"], " days to aground:", a.get("days_to_aground"))
            print("  within 1 km of:", {k: v for k, v in a["watch_within_1km"].items() if v})
            if mode == "station":
                print("  failure causes:", dict(list(a["failure_causes"].items())[:8]))
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hold_analysis.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
