"""Righting-arm curve and mass properties for a design, in the format of docs/data/revC_gz_curve.csv and
designs/revC_geometry.json. Asked for by boat-sim (issue #50, 24 Nov 2026) for Bluewater's Rev E1 motion.

Run from the repo root:  python docs/data/stability_export.py revE1 revE3
Writes docs/data/<rev>_gz_curve.csv and designs/<rev>_geometry.json for each revision named.
"""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "simulator"))
from drone_sim.geometry import Boat  # noqa: E402


def export(rev):
    design = json.load(open(os.path.join(ROOT, "designs", f"{rev}_design.json")))
    b = Boat(design); s = b.summary(); st = b.stability_summary(); g = st["gz_curve"]
    with open(os.path.join(HERE, f"{rev}_gz_curve.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["heel_deg", "gz_m", "trim_deg", "sink_m"])
        for a, z, t, k in zip(g["angle"], g["gz"], g["trim_deg"], g["sink"]):
            w.writerow([int(a), f"{z:.4f}", f"{t:.3f}", f"{k:.4f}"])
    out = dict(
        name=design.get("name", rev), units="SI (m, kg)",
        frame="x aft from bow, y to port, z up from hull bottom at midships",
        mass_kg=round(s["mass_kg"], 2), cg_m=[round(float(x), 3) for x in s["cg"]],
        waterline_z_m=round(float(s["waterline_z"]), 3),
        inertia_kg_m2=[[round(float(x), 3) for x in row] for row in b.inertia],
        inertia_note="About the CG, in the frame above (x roll axis, y pitch axis, z yaw axis); wing feathered.",
        stability=dict(gm_m=round(st["gm_m"], 3), max_gz_m=round(st["max_gz_m"], 3), angle_max_gz_deg=st["angle_max_gz"],
                       avs_deg=round(st["avs_deg"], 1), self_righting=bool(st["self_righting"])),
        files=dict(gz_curve=f"docs/data/{rev}_gz_curve.csv", our_simulator=f"designs/{rev}_design.json",
                   made_by="docs/data/stability_export.py"),
    )
    json.dump(out, open(os.path.join(ROOT, "designs", f"{rev}_geometry.json"), "w"), indent=1)
    print(rev, out["mass_kg"], "kg, GM", out["stability"]["gm_m"], "max GZ", out["stability"]["max_gz_m"], "at", out["stability"]["angle_max_gz_deg"])


if __name__ == "__main__":
    for r in sys.argv[1:] or ["revE1", "revE3"]:
        export(r)
