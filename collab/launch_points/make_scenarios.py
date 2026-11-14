"""Write the launch-point study scenarios (docs/Launch_Point_Study.md).  python collab/launch_points/make_scenarios.py
Stage A: every launch point aimed at south-west Ireland. Stage B (pairs) reuses LAUNCH and DEST."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MID = [42.0, -48.0]                       # south of the Grand Banks, as in the destination study
STREAM = [[30.0, -79.8], [32.0, -78.6], [35.0, -74.5]]   # along the Gulf Stream axis to past Cape Hatteras

# name: (label, lat, lon, km offshore, waypoints before the mid-ocean one)
LAUNCH = {
    "maine":            ("Maine: 10 km south of the outer islands off Mount Desert", 44.05, -68.17, 10, [[42.3, -66.0]]),
    "cape_cod":         ("Cape Cod: 10 km east of Chatham / Nauset", 41.70, -69.80, 10, [[40.0, -67.5]]),
    "montauk":          ("Montauk Point / Block Island: 10 km south-east", 41.00, -71.78, 10, [[40.0, -67.5]]),
    "barnegat":         ("New Jersey: 10 km east of Barnegat Inlet", 39.76, -73.98, 10, []),
    "ocean_city":       ("Ocean City, MD: 10 km off (current plan)", 38.32, -74.97, 10, []),
    "ocean_city_canyon": ("Ocean City, MD: 100 km off, at the shelf edge (Baltimore Canyon)", 38.10, -73.85, 100, []),
    "virginia_beach":   ("Virginia Beach: 10 km off, south of the Chesapeake Bay mouth", 36.83, -75.85, 10, []),
    "hatteras":         ("Hatteras Inlet, NC: 10 km off", 35.10, -75.72, 10, [[35.0, -74.9]]),
    "hatteras_stream":  ("Hatteras, NC: 45 km off, in the Gulf Stream's inshore edge", 34.95, -75.35, 45, [[35.0, -74.9]]),
    # 13 Nov: about half the "hatteras" tracks crossed Diamond Shoals, which the coastline file does not hold
    # (docs/Naval_Review.md). Two ways round: a dog-leg south-east first, or a drop point further out and east.
    "hatteras_dogleg":  ("Hatteras Inlet, NC: 10 km off, south-east dog-leg round Diamond Shoals", 35.10, -75.72, 10, [[34.80, -75.45], [35.0, -74.9]]),
    "hatteras_east":    ("Hatteras, NC: 70 km off, in the Gulf Stream east of Diamond Shoals", 35.00, -75.05, 70, []),
    "charleston":       ("Charleston, SC: 10 km off", 32.68, -79.77, 10, STREAM[1:]),
    "canaveral":        ("Cape Canaveral, FL: 10 km off", 28.41, -80.48, 10, STREAM),
    # 13 Nov: the first leg from "canaveral" crossed the cape (8 of 150 aground within a day, nothing broken).
    # Rerun with a first waypoint due east, into the Florida Current, as a real launch would steer.
    "canaveral_east":   ("Cape Canaveral, FL: 10 km off, heading east first", 28.41, -80.48, 10, [[28.42, -79.95]] + STREAM[1:]),
    "palm_beach":       ("Palm Beach, FL: 10 km off, in the Florida Current", 26.77, -79.93, 10, STREAM),
}
# name: (label, lat, lon, waypoints after the mid-ocean one); filled in for stage B from the destination study
DEST = {
    "ireland_sw": ("South-west Ireland (Mizen Head)", 51.35, -9.7, []),
    "cornwall":   ("Cornwall and the Isles of Scilly", 49.95, -6.3, []),       # stage B: same target and route as the
    "brittany":   ("Brittany (Pointe du Raz)", 48.04, -4.85, []),     # destination study (collab/destinations)
}

# Diamond Shoals: Cape Point to the end of the Outer Diamond Shoal (approximate; check chart 11555). The simulator
# reports each voyage's closest approach to this line; it does not change the voyage.
WATCH = {"diamond_shoals": [[35.22, -75.53], [35.15, -75.41]]}
# The Cornwall end (14 Nov 2026), approximate: the Seven Stones reef (lightvessel 50.060 N 6.072 W, reef to its west)
# and a ring round the Isles of Scilly through Bishop Rock (49.873 N 6.446 W) and the Western Rocks.
WATCH_CORNWALL = {"seven_stones": [[50.060, -6.072], [50.055, -6.130]],
                  "scilly": [[49.873, -6.446], [49.965, -6.400], [49.980, -6.320], [49.965, -6.255],
                             [49.900, -6.270], [49.880, -6.350], [49.873, -6.446]]}

def scenario(launch, dest):
    ll, la, lo, km, pre = LAUNCH[launch]; dl, dla, dlo, post = DEST[dest]
    return {"name": f"Launch study: {ll} to {dl}", "provider": "bulk", "start": {"lat": la, "lon": lo},
            "failure_rate_set": "planning", "target": {"lat": dla, "lon": dlo},
            "waypoints": [list(w) for w in pre] + [MID] + [list(w) for w in post], "waypoint_rule": "abeam",
            "atlantic_islands_count": "no_azores", "africa_landfall_counts": True,
            **({"watch_lines": {**(WATCH if launch.startswith("hatteras") else {}),
                                **(WATCH_CORNWALL if dest == "cornwall" else {})}}
               if launch.startswith("hatteras") or dest == "cornwall" else {})}

if __name__ == "__main__":
    import sys
    only = sys.argv[1:]                    # optional: launch names to (re)write; default all
    for l in (only or LAUNCH):
        for d in DEST:
            p = os.path.join(HERE, f"{l}__{d}.json")
            json.dump(scenario(l, d), open(p, "w"), indent=1)
            print(p)
