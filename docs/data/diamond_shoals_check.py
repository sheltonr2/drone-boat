"""How many simulated tracks from Hatteras Inlet pass over or near Diamond Shoals? (docs/Naval_Review.md)

The simulator's coastline (Natural Earth) has no shoals, so it treats them as open water. Diamond Shoals run about
8-9 miles (13-15 km) south-east from Cape Point, with as little as 1 m over them and breakers in any sea. Here the
shoal is a line from Cape Point (35.22 N, 75.53 W) to the end of the Outer Diamond Shoal (about 35.15 N, 75.41 W):
positions approximate, to be replaced by chart 11555. Saved tracks have a point every 0.6-0.8 days, so this
interpolates between them: a rough count, to be redone inside the simulator at its 5-minute step.
Run from the repo root."""
import json, math, sys
A = (35.22, -75.53); B = (35.15, -75.41)
def xy(p): return ((p[1] + 75.5)*111.2*math.cos(math.radians(35.15)), (p[0] - 35.15)*111.2)
ax, ay = xy(A); bx, by = xy(B)
def dseg(p):
    x, y = xy(p); t = max(0, min(1, ((x - ax)*(bx - ax) + (y - ay)*(by - ay))/((bx - ax)**2 + (by - ay)**2)))
    return math.hypot(x - ax - t*(bx - ax), y - ay - t*(by - ay))
ok = lambda r: r['outcome'] in ('arrived_reporting', 'arrived_tracked')
for f in sys.argv[1:]:
    R = json.load(open(f))['result']['runs']; n = 0; c = {2: 0, 5: 0, 10: 0}
    for r in R:
        t = r.get('track') or []
        if len(t) < 3: continue
        n += 1
        dmin = min(dseg((a[0] + (b[0] - a[0])*k/40, a[1] + (b[1] - a[1])*k/40)) for a, b in zip(t[:12], t[1:13]) for k in range(41))
        for lim in c: c[lim] += dmin < lim
    print(f.split('launch_')[-1][:-5], f"{n} voyages; closest approach to the shoal line under 2 km: {100*c[2]/n:.0f}%, under 5 km: {100*c[5]/n:.0f}%, under 10 km: {100*c[10]/n:.0f}%")
