"""Structural failures in knockdowns: chance per knockdown of breaking each part, by wave height.

The numbers come from the breaking-wave strike simulation (docs/data/strike_sim.py, docs/Structural_Review.md) and are
stored in structure_tables.json next to this file. A design switches the model on with

    "structure": {"parts": "C3", "breakers": "gentle", "tracker_on_post": false}

parts     "C2" = the boat before the structural review, "C3" = with its changes
breakers  "gentle" or "central" (assumptions about how hard the breakers hit). "gentle" is the default because it is the
          set that reproduces the wing-loss rate the simulator was already calibrated to (0.0009 per knockdown).
None switches the model off; designs saved before Rev C3 load with it off.

The wing keeps its calibrated rate (failures.py, knockdown_damage). For C3 that rate is multiplied by the ratio of the
C3 to the C2 wing-spar chance from the strike simulation, so the stronger spar shows up as a relative improvement.
"""
import json, os

KEEL = ("keel-box joint (tenon)", "fin root (bulb on fin)")
POST = "stern post (YB3, antenna)"
ARM = "counterweight arm"
BOOM = "tail boom"
RUDDER = ("rudder servo (back-driven)", "rudder stock")
WING = "wing spar at upper bearing"


def load_tables(design):
    """-> dict(keel, post, arm, boom, rudder, wing_factor: lists of 10 by Hs bin; tracker_on_post) or None."""
    cfg = design.get("structure")
    if not cfg:
        return None
    with open(os.path.join(os.path.dirname(__file__), "structure_tables.json"), "r", encoding="utf-8") as fh:
        T = json.load(fh)
    parts, br = cfg.get("parts", "C3"), cfg.get("breakers", "gentle")
    t, base = T[parts][br], T["C2"][br]
    add = lambda keys: [min(sum(t[k][b] for k in keys), 1.0) for b in range(10)]
    tot2, tot3 = sum(base[WING]), sum(t[WING])
    overall = (tot3 / tot2) if tot2 > 0 else 1.0
    # one ratio for all wave heights (the per-height ratios are too noisy), and never below 0.1: the harsher "central"
    # set gives 0.1-0.2, so the stronger spar is not credited with more than a tenfold improvement
    wf = [min(max(overall, 0.1), 1.0)] * 10
    return dict(keel=add(KEEL), post=t[POST], arm=t[ARM], boom=t[BOOM], rudder=add(RUDDER), wing_factor=wf,
                tracker_on_post=bool(cfg.get("tracker_on_post", parts == "C2")), parts=parts, breakers=br)
