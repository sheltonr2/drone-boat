"""Time-domain simulation of one breaking-wave strike on the Rev C2 boat, and what it does to each part.
11 Nov 2026, grade D (physics model with textbook coefficients; no test data yet).

Transverse plane only: the boat is a rigid body free in sway and roll, hit on the hull side by the moving water of a
breaker. Flexible parts (bulb on the fin, wing on the spar, counterweight pod on its arm, tail on its boom, the stern
post with its gear) ride on it as spring-mass systems driven by the hull's acceleration where they are attached.

Published anchors used:
  * Wienke & Oumeraci (2005): a plunging breaker hits a cylinder at the wave speed with slamming coefficient 2*pi,
    decaying within about 0.4 radii of penetration; after that ordinary drag.
  * Southampton / SNAME-USYRU capsize tests: a breaking wave about 55% of boat length rolls a yacht (0.825 m for 1.5 m).
What is still assumed is listed in ASSUME below, each with a range that the Monte Carlo samples.
Run:  python strike_sim.py [Monte Carlo result json with knockdowns_by_hs_m]
"""
import json, math, sys
import numpy as np

G, RHO = 9.81, 1025.0
# ---- boat (designs/revC_geometry.json, build-files/source/design.py); heights are metres above the CG
M_BOAT, I_ROLL, GM = 26.4, 2.95, 0.19
CGZ = -0.036
Z = lambda z_design: z_design - CGZ
HULL_R, HULL_L, Z_HULL = 0.15, 1.5, Z(0.115)          # hull side treated as a cylinder lying in the water
FIN_Z = Z(np.linspace(-0.043, -0.387, 5)); FIN_CHORD, FIN_DZ = 0.16, 0.086
FIN_ADDED = RHO * math.pi * 0.08**2 * 0.43 / 5          # kg of water each strip carries
Z_BULB, BULB_ADDED, BULB_AREA = Z(-0.436), 0.83, 0.023
H_CRIT = 0.825

# ---- flexible parts: mass kg, height above CG, cantilever length m, EI N*m2, damping ratio
PARTS = {
    "fin root (bulb on fin)":      dict(m=14.5, z=Z_BULB,   L=0.436, EI=2501.0, zeta=0.08),
    "wing spar at upper bearing":  dict(m=1.2,  z=Z(0.80),  L=0.55,  EI=1730.0, zeta=0.03),
    "counterweight arm":           dict(m=1.0,  z=Z(0.276), L=0.26,  EI=52.7,   zeta=0.03),
    "tail boom":                   dict(m=0.25, z=Z(0.276), L=0.56,  EI=52.7,   zeta=0.03),
    "stern post (YB3, antenna)":   dict(m=0.9,  z=Z(0.51),  L=0.25,  EI=259.0,  zeta=0.03),
}
# strength (N*m at the root), scatter (COV) and what it is
STRENGTH = {
    "fin root (bulb on fin)":      (1103, 0.20, "hardwood + glass + carbon, estimate"),
    "keel-box joint (tenon)":      (700,  0.25, "tenon bearing at 10 MPa, estimate"),
    "wing spar at upper bearing":  (690,  0.15, "30 x 26 carbon tube at 600 MPa"),
    "counterweight arm":           (53,   0.15, "12 x 10 carbon tube at 600 MPa"),
    "tail boom":                   (53,   0.15, "12 x 10 carbon tube at 600 MPa"),
    "stern post (YB3, antenna)":   (115,  0.10, "20 x 1.5 6061-T6 tube, bends at about 1.3 x yield"),
    "rudder stock":                (75,   0.15, "12 mm 316 bar, plastic bending, yield 260 MPa"),
    "rudder servo (back-driven)":  (6.0,  0.20, "3 x the 2 N*m stall torque of the SW-1210SG, guess"),
}
RUD_AREA, RUD_ARM, RUD_TORQUE_ARM = 0.0276, 0.115, 0.038
WING_CHORD, WING_ROOT_ABOVE_WL, WING_BEARING_TO_ROOT = 0.30, 0.20, 0.055
POST_AREA = 0.012

ASSUME = dict(
    plunging_fraction=0.2,       # share of knockdown breakers that are plunging (steep front, slam); the rest spilling
    kappa=(0.6, 1.1),            # water speed in the crest as a fraction of the breaker's speed
    cs0=(math.pi, 2 * math.pi),  # peak slamming coefficient (von Karman to Wagner)
    spill_time=(0.2, 0.6),       # s, time for a spilling roller to engage the whole hull side
    depth_scale=(0.1, 0.3),      # depth over which the moving water fades, as a fraction of breaker height
    jet_thickness=(0.1, 0.3),    # plunging: thickness of the falling jet, fraction of breaker height (0.8 of water density)
    jet_centre=(0.2, 1.0),       # plunging: height of the jet's centre above the boat's waterline, fraction of breaker height
    roller_thickness=(0.05, 0.2),  # spilling: thickness of the foam roller above the waterline (half water density)
    misalign_deg=25.0,           # std dev of the angle between wave direction and wind direction (wing feathers to wind)
    wing_aoa_deg=8.0,            # wing angle to the wind while sailing
    wing_align_time=0.08,        # s, time for the free wing to swing into line with the water
)

def simulate(hs, n, rng, A=ASSUME, parts=PARTS, dt=2e-4, T=0.45, post_area=POST_AREA):
    hb_s = 0.25 * hs
    hb = hb_s * np.sqrt((H_CRIT / hb_s)**2 - np.log(rng.random(n)) / 2)
    c = np.sqrt(G * 8.5 * hb / (2 * np.pi))
    sin_t = np.abs(np.sin(rng.uniform(0, np.pi, n)))
    u0 = rng.uniform(*A["kappa"], n) * c * sin_t                       # lateral water speed at the surface
    plunging = rng.random(n) < A["plunging_fraction"]
    cs0 = rng.uniform(*A["cs0"], n); t_sp = rng.uniform(*A["spill_time"], n)
    delta = rng.uniform(*A["depth_scale"], n) * hb
    tj = rng.uniform(*A["jet_thickness"], n) * hb; hc = rng.uniform(*A["jet_centre"], n) * hb
    tr = rng.uniform(*A["roller_thickness"], n) * hb
    lo = np.where(plunging, hc - tj / 2, 0.0); hi = np.where(plunging, hc + tj / 2, tr)   # band of moving water above the waterline
    dens = np.where(plunging, 0.8, 0.5)
    beta = np.radians(np.abs(rng.normal(0, A["misalign_deg"], n)) + A["wing_aoa_deg"])
    L_e = HULL_L * np.maximum(sin_t, 0.3)
    # water speed at each fin strip and at the bulb (depth below the waterline; waterline is 0.10 above the hull bottom)
    depth = lambda z: np.maximum(0.10 + CGZ - z, 0.0)
    u_fin = u0[:, None] * np.exp(-depth(FIN_Z)[None, :] / delta[:, None]); u_b = u0 * np.exp(-depth(Z_BULB) / delta)
    # mass matrix with added mass of fin and bulb
    za = np.r_[FIN_Z, Z_BULB]; ma = np.r_[np.full(5, FIN_ADDED), BULB_ADDED]
    M11, M12, M22 = M_BOAT + ma.sum(), (ma * za).sum(), I_ROLL + (ma * za**2).sum()
    det = M11 * M22 - M12**2
    v = np.zeros(n); w = np.zeros(n); phi = np.zeros(n); pen = np.zeros(n)
    q = {k: np.zeros(n) for k in parts}; qd = {k: np.zeros(n) for k in parts}; peak = {k: np.zeros(n) for k in parts}
    om = {k: math.sqrt(3 * p["EI"] / p["L"]**3 / p["m"]) for k, p in parts.items()}
    kk = {k: 3 * p["EI"] / p["L"]**3 for k, p in parts.items()}
    u_rud = u0 * np.exp(-0.143 / delta)                                  # water speed at the middle of the rudder blades
    a_peak = np.zeros(n); v_rud = np.zeros(n); t50 = np.full(n, np.nan); w_peak = np.zeros(n)
    w_lo, w_hi = np.clip(lo, WING_ROOT_ABOVE_WL, WING_ROOT_ABOVE_WL + 1.0), np.clip(hi, WING_ROOT_ABOVE_WL, WING_ROOT_ABOVE_WL + 1.0)
    s_imm = w_hi - w_lo                                                  # wing span in the moving water
    w_arm = WING_BEARING_TO_ROOT + (w_lo + w_hi) / 2 - WING_ROOT_ABOVE_WL
    cn = np.minimum(2 * np.pi * 0.6 * np.sin(beta), 1.1)               # normal-force coefficient of the wing in water
    post_wet = (lo < 0.50) & (hi > 0.38)
    for i in range(int(T / dt)):
        t = i * dt
        urel = u0 - (v + w * Z_HULL)
        C = np.where(plunging, 1 + (cs0 - 1) * np.clip(1 - pen / (0.41 * HULL_R), 0, 1), np.minimum(t / t_sp, 1.0))
        Fh = RHO * HULL_R * L_e * C * urel * np.abs(urel)
        pen += np.maximum(urel, 0) * dt
        vf = v[:, None] + w[:, None] * FIN_Z[None, :] - u_fin
        Ff = -0.5 * RHO * 1.2 * FIN_CHORD * FIN_DZ * vf * np.abs(vf)
        vb = v + w * Z_BULB - u_b
        Fb = -0.5 * RHO * 1.0 * BULB_AREA * vb * np.abs(vb)
        F = Fh + Ff.sum(1) + Fb
        Mo = Fh * Z_HULL + (Ff * FIN_Z[None, :]).sum(1) + Fb * Z_BULB - M_BOAT * G * GM * np.sin(phi)
        a = (M22 * F - M12 * Mo) / det; al = (M11 * Mo - M12 * F) / det
        # flexible parts, driven by the acceleration where they are attached
        for k, p in parts.items():
            ab = a + al * p["z"]
            f_ext = 0.0
            if k.startswith("wing"):
                ur = u0 - (v + w * p["z"])
                f_ext = 0.5 * RHO * dens * ur * np.abs(ur) * WING_CHORD * s_imm * cn * math.exp(-t / A["wing_align_time"]) * w_arm / p["L"]
            elif k.startswith("stern"):
                ur = u0 - (v + w * p["z"])
                f_ext = np.where(post_wet, 0.5 * RHO * dens * 1.2 * post_area * ur * np.abs(ur), 0.0)
            elif k.startswith("counter") or k.startswith("tail"):
                ab = ab * np.sin(beta)                                   # only the part of the jolt across the arm bends it
            qdd = -ab + f_ext / p["m"] - 2 * p["zeta"] * om[k] * qd[k] - om[k]**2 * q[k]
            qd[k] += qdd * dt; q[k] += qd[k] * dt
            peak[k] = np.maximum(peak[k], np.abs(kk[k] * q[k] * p["L"]))
        v += a * dt; w += al * dt; phi += w * dt
        a_peak = np.maximum(a_peak, np.abs(a + al * Z_HULL)); w_peak = np.maximum(w_peak, np.abs(w))
        v_rud = np.maximum(v_rud, np.abs(v + w * Z(-0.043) - u_rud))
        hit = np.isnan(t50) & (v + w * Z_HULL >= 0.5 * u0); t50[hit] = t
    # the wing slapping into the water as the boat goes over: tip speed from the roll rate, wet for wing_align_time
    vt = np.abs(w) * 1.15; sw = np.minimum(vt * A["wing_align_time"], 1.0)
    slap = 0.5 * RHO * WING_CHORD * cn * vt**2 * sw * (1.05 - sw / 2)
    key = [k for k in parts if k.startswith("wing")][0]
    strike_only = peak[key].copy(); peak[key] = np.maximum(peak[key], slap)
    f_rud = 0.5 * RHO * 1.2 * RUD_AREA * v_rud**2
    peak["rudder stock"] = f_rud * RUD_ARM
    peak["rudder servo (back-driven)"] = f_rud * RUD_TORQUE_ARM
    peak["keel-box joint (tenon)"] = peak["fin root (bulb on fin)"]
    static_fin = 9.2 * (1 - 1.025 / 11.34) * G * 0.436
    peak["fin root (bulb on fin)"] = peak["fin root (bulb on fin)"] + static_fin * 0.8
    peak["keel-box joint (tenon)"] = peak["keel-box joint (tenon)"] + static_fin * 0.8
    return dict(wing_strike=strike_only, wing_slap=slap, peak=peak, hb=hb, c=c, u0=u0, dv=v + w * Z_HULL, a_peak=a_peak, w_end=w, w_peak=w_peak, t50=t50, plunging=plunging, phi=phi)

def with_options():
    """The same boat with the changes recommended in docs/Structural_Review.md."""
    P = {k: dict(v) for k, v in PARTS.items()}; S = dict(STRENGTH)
    P["wing spar at upper bearing"].update(EI=2826.0); S["wing spar at upper bearing"] = (1130, 0.15, "30 x 22 carbon tube")
    P["counterweight arm"].update(EI=40.7); S["counterweight arm"] = (119, 0.10, "12 mm solid pultruded glass rod at 700 MPa")
    P["stern post (YB3, antenna)"].update(m=0.5, L=0.30, EI=139.0); S["stern post (YB3, antenna)"] = (185, 0.12, "20 x 2 pultruded glass tube, YB3 moved to the deck")
    S["rudder servo (back-driven)"] = (30.0, 0.2, "spring servo-saver in the linkage: the tiller gives, the servo does not see it")
    return P, S

def p_fail(peaks, rng, strength=STRENGTH):
    out = {}
    for k, (cap, cov, _) in strength.items():
        x = peaks[k]; capv = cap * np.exp(rng.normal(-cov**2 / 2, cov, len(x)))
        out[k] = float(np.mean(x > capv))
    return out

def per_voyage(pk_by_bin, kd):
    return {k: 1 - float(np.prod([(1 - pk_by_bin[b][k]) ** kd[b] for b in range(len(kd))])) for k in pk_by_bin[0]}

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    kd = None
    if len(sys.argv) > 1:
        runs = [r for r in json.load(open(sys.argv[1]))["result"]["runs"] if r.get("knockdowns_by_hs_m")]
        kd = np.mean([r["knockdowns_by_hs_m"] for r in runs], axis=0)
    print("ONE STRIKE AT Hs 5 m (60,000 strikes)")
    r = simulate(5.0, 60000, rng)
    pct = lambda x, m=None: tuple(np.nanpercentile(x if m is None else x[m], [50, 95, 99.9]))
    pl, sp = r["plunging"], ~r["plunging"]
    print("  breaker height m           median %.2f  95%% %.2f  99.9%% %.2f" % pct(r["hb"]))
    print("  breaker speed m/s          median %.1f  95%% %.1f  99.9%% %.1f" % pct(r["c"]))
    for name, m in (("plunging", pl), ("spilling", sp)):
        print(f"  {name}:")
        print("    hull speed picked up / water speed   median %.2f" % np.nanmedian((r["dv"] / np.maximum(r["u0"], 1e-6))[m]))
        print("    time to reach half the water speed s median %.3f  95%% %.3f" % tuple(np.nanpercentile(r["t50"][m], [50, 95])))
        print("    peak hull acceleration, g            median %.1f  95%% %.1f  99.9%% %.1f" % tuple(np.array(pct(r["a_peak"], m)) / G))
        print("    roll rate at 0.45 s, rad/s           median %.1f  95%% %.1f  99.9%% %.1f" % pct(np.abs(r["w_end"]), m))
    print("\n  Peak load in one strike, N*m (all strikes)           median    95%   99.9%   strength   median plunging")
    print("  wing spar: from the water of the strike alone, median %.0f  95%% %.0f  99.9%% %.0f; from the slap as it rolls, median %.0f  95%% %.0f  99.9%% %.0f"
          % (pct(r["wing_strike"]) + pct(r["wing_slap"])))
    for k, (cap, cov, note) in STRENGTH.items():
        a = pct(r["peak"][k]); print(f"  {k:32s} {a[0]:12.0f} {a[1]:6.0f} {a[2]:7.0f} {cap:9.0f}   {np.median(r['peak'][k][pl]):8.0f}   ({note})")
    variants = {
        "central (20% plunging)": {},
        "gentle (10% plunging, water at 0.4-0.9 of wave speed)": dict(plunging_fraction=0.1, kappa=(0.4, 0.9)),
        "hard (40% plunging, water at 0.8-1.2 of wave speed)": dict(plunging_fraction=0.4, kappa=(0.8, 1.2)),
    }
    for name, ch in variants.items():
        A = dict(ASSUME, **ch)
        bins = np.arange(0.5, 10, 1.0)
        pk = [p_fail(simulate(max(b, 1.0), 30000, rng, A)["peak"], rng) for b in bins]
        print(f"\nCHANCE OF BREAKING, {name}")
        print(f"  {'part':32s} per knockdown at Hs 3 m / 6 m" + ("    per voyage  (about %.0f knockdowns)" % kd.sum() if kd is not None else ""))
        pv = per_voyage(pk, kd) if kd is not None else {}
        P2, S2 = with_options()
        pk2 = [p_fail(simulate(max(b, 1.0), 30000, rng, A, parts=P2, post_area=0.006)["peak"], rng, S2) for b in bins]
        pv2 = per_voyage(pk2, kd) if kd is not None else {}
        for k in STRENGTH:
            print(f"  {k:32s} {pk[3][k]:10.1e} / {pk[6][k]:8.1e}" + (f"   {100*pv[k]:8.1f}%   with the changes: {pk2[3][k]:.1e} / {pk2[6][k]:.1e}  {100*pv2[k]:6.1f}%" if pv else ""))
