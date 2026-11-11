"""Wing shape study: the same 0.30 m2 of wing, shorter and wider. 11 Nov 2026, grade D.
Speed from the simulator's own speed model (polar); knockdown loads from strike_sim.py ("measured" breaker model, Rev C3 spar).
Run from docs/data:  python wing_shape_study.py [Monte Carlo result json with knockdowns_by_hs_m]"""
import sys, json, copy
import numpy as np
sys.path.insert(0, "../../simulator")
from drone_sim import design as D
from drone_sim.sim import prepare_design
import strike_sim as S

SHAPES = [(1.0, 0.300), (0.9, 0.333), (0.8, 0.375), (0.7, 0.429), (0.6, 0.500)]
kd = None
if len(sys.argv) > 1:
    runs = [r for r in json.load(open(sys.argv[1]))["result"]["runs"] if r.get("knockdowns_by_hs_m")]
    kd = np.mean([r["knockdowns_by_hs_m"] for r in runs], axis=0)
A = dict(S.ASSUME, plunge_model="measured")
rng = np.random.default_rng(21)
TWS, TWA = (4.0, 7.0, 10.0, 14.0), (50, 70, 90, 120, 150)
print(f"{'span x chord':>13s} {'mass':>6s} {'GM':>6s} | mean speed kn at TWS " + " ".join(f"{t:>4.0f}" for t in TWS) + " | upwind VMG kn at 7 | slap 1-in-1000 N*m | spar breaks per knockdown Hs3 / Hs6 | per voyage")
base = None
for span, chord in SHAPES:
    d = D.default_design(); d = copy.deepcopy(d)
    d["wing"].update(span=span, chord=chord, pivot_from_le=round(0.22 * chord, 4))
    prep = prepare_design(d, cache_dir="/tmp/wingcache", log=lambda m: None)
    pol, boat = prep["polar"], prep["boat"]; st = boat.stability_summary()
    sp = [np.mean([float(pol(t, a, 0.2 * t, 1.0, ("u",))["u"]) for a in TWA]) * 1.944 for t in TWS]
    vmg = max(float(pol(7.0, a, 1.4, 1.0, ("u",))["u"]) * np.cos(np.radians(a)) for a in range(40, 80, 5)) * 1.944
    P3, S3 = S.with_options(); S.set_wing(span, chord, P3)
    pk = []
    for b in range(10):
        if b < 2: pk.append(0.0); continue
        r = S.simulate(b + 0.5, 30000, rng, A, parts=P3, post_area=0.006)
        pk.append(S.p_fail(r["peak"], rng, S3)["wing spar at upper bearing"])
        if b == 5: slap999 = np.percentile(r["wing_slap"], 99.9)
    pv = 1 - float(np.prod([(1 - pk[b]) ** kd[b] for b in range(10)])) if kd is not None else float("nan")
    row = (span, chord, boat.summary()["mass_kg"], st["gm_m"], sp, vmg, slap999, pk[3], pk[6], pv)
    if base is None: base = row
    print(f"{span:5.1f} x {chord:5.3f} {row[2]:6.2f} {row[3]:6.3f} |                       " + " ".join(f"{x:4.2f}" for x in sp)
          + f" | {vmg:5.2f} ({100*(vmg/base[5]-1):+.0f}%)     | {slap999:6.0f} ({100*slap999/base[6]:.0f}%)   | {pk[3]:.1e} / {pk[6]:.1e}          | {100*pv:5.1f}%   speed vs base {100*(np.mean(sp)/np.mean(base[4])-1):+.1f}%", flush=True)
S.set_wing(1.0, 0.30)
