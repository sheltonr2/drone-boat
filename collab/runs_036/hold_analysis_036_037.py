"""Runs 036 (BVI) and 037 (Cornwall): holding at each candidate pickup point, on the detailed coastlines (Rev E3).

  station: the autopilot holds within 1 km for 14 days, failures on (planning rates);
  drift:   a dead boat drifts from the point for 30 days.

Per candidate it reports the outcome split, how far the boat strays (time-weighted: the radius it stays inside 50% and
90% of the time, pooled over every voyage), the share of time beyond 1, 2 and 5 km, and where groundings happen.
Usage: python collab/runs_036/hold_analysis_036_037.py [results dir]   -> collab/runs_036/hold_analysis_036_037.json
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs_026"))
from hold_analysis import km, val, pct, q, analyse  # noqa: E402

BVI = {"norman": ("Norman Island, 4 km S", 18.300, -64.580), "norman_offing": ("Norman offing, 18 km S", 18.170, -64.580),
       "ginger_se": ("Ginger Island SE", 18.330, -64.430), "jvd_north": ("Jost Van Dyke, 4 km N", 18.490, -64.750),
       "anegada_west": ("Anegada, 8 km W", 18.720, -64.490), "anegada_north": ("Anegada, 9 km N", 18.820, -64.330),
       "stcroix_north": ("St Croix, 9 km N", 17.850, -64.750)}
CORN = {"lizard": ("Lizard offing", 49.85, -5.20), "mounts": ("Mount's Bay mouth", 49.97, -5.45),
        "lizard_deep": ("Lizard, 30 km S", 49.70, -5.20), "scilly_lizard": ("Scilly-Lizard gap", 49.85, -5.75)}
ISLANDS = [("St Croix", 17.73, -64.75), ("St Thomas", 18.34, -64.93), ("St John", 18.33, -64.74), ("Jost Van Dyke", 18.45, -64.75),
           ("Tortola", 18.43, -64.62), ("Norman / Peter Islands", 18.33, -64.61), ("Cooper / Salt / Ginger", 18.37, -64.48),
           ("Virgin Gorda", 18.48, -64.40), ("Anegada / Horseshoe Reef", 18.73, -64.36), ("Culebra / Vieques", 18.25, -65.35)]


def where_bvi(lat, lon):
    return min(ISLANDS, key=lambda p: km((lat, lon), p[1:]))[0]


def spread(path, hold):
    """Time-weighted distance-from-hold quantiles pooled over all voyages, and time shares beyond 1/2/5 km."""
    d = json.load(open(path)); segs = []
    for r in d["result"]["runs"]:
        tr = val(r["track"])
        for i in range(len(tr) - 1):
            segs.append((km(hold, (tr[i][0], tr[i][1])), tr[i + 1][2] - tr[i][2]))
    segs.sort(); tot = sum(w for _, w in segs) or 1
    out, acc, want = {}, 0.0, [(0.5, "r50_km"), (0.9, "r90_km")]
    for dist, w in segs:
        acc += w
        while want and acc / tot >= want[0][0]:
            out[want.pop(0)[1]] = round(dist, 2)
    for lim in (1, 2, 5):
        out[f"time_beyond_{lim}km_percent"] = round(100 * sum(w for x, w in segs if x > lim) / tot, 1)
    return out


def run(rd, prefix, pts, corn):
    res = {}
    for tag, (nm, la, lo) in pts.items():
        for mode in ("station", "drift"):
            f = os.path.join(rd, f"{prefix}_{mode}_{tag}.json")
            if not os.path.exists(f): continue
            a = analyse(f, (la, lo))
            if not corn:   # replace the Cornwall place names with BVI ones
                d = json.load(open(f)); g = {}
                for r in d["result"]["runs"]:
                    if r["outcome"] == "aground":
                        e = val(r["end"]); w = where_bvi(e["lat"], e["lon"]); g[w] = g.get(w, 0) + 1
                a["groundings"] = g
            a.update(spread(f, (la, lo)))
            a.update(name=nm, lat=la, lon=lo, mode=mode)
            res[f"{mode}_{tag}"] = a
            print(f"{nm:26s} {mode:7s} n={a['runs']:4d} aground {a['percent'].get('aground', 0):5.1f}%  "
                  f"r50 {a['r50_km']:6.2f} r90 {a['r90_km']:6.2f} km  >1km {a['time_beyond_1km_percent']:5.1f}%  "
                  f">5km {a['time_beyond_5km_percent']:5.1f}%  max med {a['max_distance_km']['median']}  "
                  f"days-to-aground {a.get('days_to_aground')}  {a['percent']}")
            if a["groundings"]: print(f"{'':36s}groundings: {dict(sorted(a['groundings'].items(), key=lambda x: -x[1]))}")
    return res


def main():
    rd = sys.argv[1] if len(sys.argv) > 1 else "results"
    print("== Run 036: BVI candidates, Feb-Apr 2022-2025")
    bvi = run(rd, "hold036_2022-2025_revE3", BVI, False)
    print("\n== Run 037: Cornwall candidates, mid-Aug to mid-Oct 2021-2024")
    corn = run(rd, "hold037_2021-2024_revE3", CORN, True)
    json.dump(dict(bvi=bvi, cornwall=corn), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hold_analysis_036_037.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
