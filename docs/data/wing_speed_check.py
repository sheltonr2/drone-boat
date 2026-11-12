"""Speed of the C4 (1.0 x 0.30 m) and C5 (0.8 x 0.375 m) wings with the old and new stall rules. 12 Nov 2026.
Run from docs/data:  python wing_speed_check.py"""
import sys, copy
import numpy as np
sys.path.insert(0, "../../simulator")
from drone_sim import design as D, vpp as V
from drone_sim.geometry import Boat

def polar(span, chord, rule):
    d = copy.deepcopy(D.default_design()); d["wing"].update(span=span, chord=chord, pivot_from_le=round(0.22 * chord, 4))
    b = Boat(d); vp = V.VPP(b, b.stability_summary())
    keep = V.WING_CL_STALL
    V.WING_CL_STALL = 1.03 if rule == "new" else -1.0      # -1 = old rule (cl_stall <= 0 falls back to it)
    try:
        return V.Polar(V.build_polar(vp))
    finally:
        V.WING_CL_STALL = keep

P = {(w, r): polar(*sh, r) for w, sh in (("C4", (1.0, 0.30)), ("C5", (0.8, 0.375))) for r in ("old", "new")}
spd = lambda p, tws, twa: float(p(tws, np.radians(twa), 0.2 * tws, 1.0, ("u",))["u"])
for rule in ("old", "new"):
    a, b = P[("C4", rule)], P[("C5", rule)]
    study = [(spd(b, t, x) / spd(a, t, x) - 1) for t in (4, 7, 10, 14) for x in (50, 70, 90, 120, 150)]
    john = [(spd(b, t, x) / max(spd(a, t, x), 1e-6) - 1) for t in (3, 7, 11, 15) for x in (50, 60, 75, 90, 110, 135, 150, 165)]
    down = [(spd(b, t, x) / spd(a, t, x) - 1) for t in (3, 7, 11, 15) for x in (135, 150, 165)]
    print(f"\n{rule} stall rule: C4 -> C5 speed change, study grid {100*np.mean(study):+.1f}%  John's grid {100*np.mean(john):+.1f}%  downwind {100*np.mean(down):+.1f}%")
    print("  wind m/s  " + " ".join(f"{x:>5d}" for x in (50, 60, 75, 90, 110, 135, 150, 165)))
    for t in (3, 7, 11, 15):
        print(f"  {t:7d}   " + " ".join(f"{100*(spd(b, t, x)/max(spd(a, t, x), 1e-6) - 1):+5.0f}" for x in (50, 60, 75, 90, 110, 135, 150, 165)))
    print("  C4 speed kn at 7 m/s: " + " ".join(f"{1.944*spd(a, 7, x):.2f}" for x in (50, 60, 75, 90, 110, 135, 150, 165)))
for w in ("C4", "C5"):
    print(f"{w}: old -> new rule, mean change over study grid {100*np.mean([spd(P[(w,'new')],t,x)/spd(P[(w,'old')],t,x)-1 for t in (4,7,10,14) for x in (50,70,90,120,150)]):+.1f}%")
