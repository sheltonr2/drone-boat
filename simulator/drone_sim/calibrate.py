"""Turn field-test measurements into simulator settings (see docs/Field_Tests.md).

Idea from jcolter11374/boat-sim (docs/tow-test.md, vessel/calibrate.py): replace guessed
drag and stability numbers with an afternoon of measurements.

  python -m drone_sim.calibrate predict                      # what the model expects you to measure
  python -m drone_sim.calibrate tow 1,1.5,2,2.5,3 0.07,0.16,0.30,0.50,0.75
  python -m drone_sim.calibrate incline 1.0 0.30 3.1,3.0,3.2  # weight kg, shift m, heel angles deg
  (add --design my_design.json to any of them)
"""
import argparse, json, math
import numpy as np
from . import design as D
from .geometry import Boat
from .vpp import VPP

KN = 0.514444
G = 9.81


def _vpp(design):
    boat = Boat(design)
    return boat, VPP(boat, boat.stability_summary())


def tow_drag_kgf(design, speeds_kn, k=None):
    """Drag in kgf when the boat is towed straight and upright in flat calm water, rudder centred,
    wing feathered (zero angle of attack) and no wind. This is what a luggage scale on the tow line reads."""
    d = json.loads(json.dumps(design))
    if k is not None:
        d["hydro"]["form_factor"] = k
    _, vp = _vpp(d)
    u = np.asarray(speeds_kn, float)*KN
    z = np.zeros_like(u)
    fx = vp.forces(u, z, z, z, z, z, z, z, z + 5.0, z + 1.0)[0]
    return -np.asarray(fx)/G


def fit_form_factor(design, speeds_kn, pulls_kg):
    """Least-squares hull form factor from tow-test pulls. Drag is linear in the form factor,
    so two model runs (k = 1 and k = 2) give the slope and the rest."""
    s, p = np.asarray(speeds_kn, float), np.asarray(pulls_kg, float)
    d1, d2 = tow_drag_kgf(design, s, 1.0), tow_drag_kgf(design, s, 2.0)
    slope, rest = d2 - d1, d1 - (d2 - d1)
    k = float(np.sum(slope*(p - rest))/np.sum(slope*slope))
    fitted = rest + k*slope
    return dict(form_factor=round(k, 3), was=design["hydro"]["form_factor"],
                rows=[dict(speed_kn=float(a), measured_kg=float(b), model_kg=round(float(c), 3))
                      for a, b, c in zip(s, p, fitted)],
                rms_error_kg=round(float(np.sqrt(np.mean((fitted - p)**2))), 3))


def gm_from_inclining(weight_kg, shift_m, heel_deg, boat_mass_kg):
    """Classic inclining test: move a known weight across the deck and read the heel angle.
    GM = w x d / (displacement x tan(heel)). Use small angles (2 to 5 degrees)."""
    angles = np.radians(np.atleast_1d(np.asarray(heel_deg, float)))
    gm = weight_kg*shift_m/(boat_mass_kg*np.tan(angles))
    return dict(gm_m=round(float(np.mean(gm)), 4), each=[round(float(g), 4) for g in gm])


def predict(design):
    boat, _ = _vpp(design)
    st = boat.stability_summary(); m = boat.summary()["mass_kg"]
    speeds = [1.0, 1.5, 2.0, 2.5, 3.0]
    pulls = tow_drag_kgf(design, speeds)
    w, dshift = 1.0, 0.30
    heel = math.degrees(math.atan(w*dshift/(m*st["gm_m"])))
    return dict(mass_kg=round(m, 2), gm_m=round(st["gm_m"], 3),
                tow=[dict(speed_kn=s, pull_kg=round(float(p), 3)) for s, p in zip(speeds, pulls)],
                incline_example=f"Moving {w:g} kg by {dshift:g} m across the deck should heel the boat {heel:.1f} deg")


def main():
    ap = argparse.ArgumentParser(prog="drone_sim.calibrate")
    ap.add_argument("cmd", choices=["predict", "tow", "incline"])
    ap.add_argument("a", nargs="?"); ap.add_argument("b", nargs="?"); ap.add_argument("c", nargs="?")
    ap.add_argument("--design")
    ap.add_argument("--mass", type=float, help="weighed boat mass in kg (incline)")
    x = ap.parse_args()
    design = D.load(x.design) if x.design else D.default_design()
    nums = lambda s: [float(v) for v in s.split(",")]
    if x.cmd == "predict":
        out = predict(design)
    elif x.cmd == "tow":
        out = fit_form_factor(design, nums(x.a), nums(x.b))
        out["next"] = f'Put "form_factor": {out["form_factor"]} under "hydro" in your design file.'
    else:
        mass = x.mass or Boat(design).summary()["mass_kg"]
        out = gm_from_inclining(float(x.a), float(x.b), nums(x.c), mass)
        out["model_gm_m"] = round(Boat(design).stability_summary()["gm_m"], 4)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
