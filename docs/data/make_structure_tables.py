"""Per-knockdown chance of breaking each part, by wave height, for the voyage simulator (simulator/drone_sim/structure_tables.json).
Uses strike_sim.py. Rev C2 = parts as drawn before the structural review; Rev C3 = with its changes. 11 Nov 2026.
Run:  python make_structure_tables.py   (about 35 minutes)"""
import json, sys
import numpy as np
import strike_sim as S

SETS = {"gentle": dict(plunging_fraction=0.1, kappa=(0.4, 0.9)), "central": {}}
N = {"gentle": 60_000, "central": 20_000}
out = {"_about": "chance per knockdown of breaking each part, by significant wave height in 1 m bins (0-1, 1-2, ... 9+ m); "
                 "from docs/data/strike_sim.py; see docs/Structural_Review.md", "C2": {}, "C3": {}}
P3, S3 = S.with_options()
rng = np.random.default_rng(11)
for name, ch in SETS.items():
    A = dict(S.ASSUME, **ch)
    tabs = {"C2": {k: [] for k in S.STRENGTH}, "C3": {k: [] for k in S.STRENGTH}}
    for b in range(10):
        hs = b + 0.5
        if b < 2:                                   # almost no knockdowns below 2 m seas, and none that break anything
            for rev in tabs:
                for k in tabs[rev]: tabs[rev][k].append(0.0)
            continue
        for rev, parts, strength, area in (("C2", S.PARTS, S.STRENGTH, S.POST_AREA), ("C3", P3, S3, 0.006)):
            pf = S.p_fail(S.simulate(hs, N[name], rng, A, parts=parts, post_area=area)["peak"], rng, strength)
            for k in pf: tabs[rev][k].append(pf[k])
        print(name, b, {k: tabs["C3"][k][-1] for k in tabs["C3"]}, flush=True)
    for rev in ("C2", "C3"):
        out[rev][name] = tabs[rev]
    json.dump(out, open("../../simulator/drone_sim/structure_tables.json", "w"), indent=1)
