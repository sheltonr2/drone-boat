"""Print a compact daily track of the dead-boat run, for comparing with boat-sim."""
import json, sys
d = json.load(open(sys.argv[1]))
r = d.get("result", d)
print("outcome", r["outcome"], "days", r["days"], "distance_km", r["distance_km"], "end", round(r["end"]["lat"], 3), round(r["end"]["lon"], 3))
last = -1
for s in r["series"]:
    day = int(s["t"] // 24)
    if day != last:
        last = day
        print(f"day {day:2d}  lat {s['lat']:.3f}  lon {s['lon']:.3f}  sog {s['sog']*1.944:.2f} kn  wind {s['tws']:.1f} m/s  hs {s['hs']:.1f} m  current {s['cur']*1.944:.2f} kn")
