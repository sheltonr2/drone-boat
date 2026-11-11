"""Physics-based estimate of keel-fin loss in breaking-wave knockdowns (Rev C / C1).  11 Nov 2026, grade D.

What it does
  1. Section properties and lateral bending strength of the fin root for several constructions.
  2. A load model for one breaking-wave strike: the hull is jerked sideways, and the 9 kg bulb, hanging
     0.44 m below on the fin, has to be dragged along through the fin (a mass on a cantilever spring).
  3. Monte Carlo over strikes -> chance the root moment exceeds the fin's strength, by sea state.
  4. Chance per voyage, using the knockdowns-by-wave-height that the voyage simulator logged on real weather.

Every assumption is a named constant below. The load side is uncertain by about a factor of 2 either way,
so read the results as "which constructions are safe by a wide margin", not as precise odds.
Run:  python keel_reliability.py [path to a Monte Carlo result json with knockdowns_by_hs_m]
"""
import json, math, sys
import numpy as np

G = 9.81
# ---------------------------------------------------------------- geometry (build-files/source/design.py)
ROOT_CHORD, T_RATIO, SPAN = 0.170, 0.12, 0.430          # m
BULB_KG, BULB_ARM = 9.2, 0.436                          # kg of lead; m from the fin root to the bulb axis
BOAT_KG, HULL_KG = 25.3, 25.3 - 9.2
H_CRIT = 0.825                                          # m, breaker height that knocks a 1.5 m hull down (failures.py)

def naca_outline(n=400):
    x = (1 - np.cos(np.linspace(0, np.pi, n))) / 2
    y = 5 * T_RATIO * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1036 * x**4)
    return x * ROOT_CHORD, y * ROOT_CHORD

def skin_I(t_skin):
    """Second moment of area (m^4) of the two skins about the chord line."""
    x, y = naca_outline(); ds = np.hypot(np.diff(x), np.diff(y)); ym = (y[1:] + y[:-1]) / 2
    return 2 * float(np.sum(ds * t_skin * ym**2))

def solid_I():
    x, y = naca_outline(); dx = np.diff(x); ym = (y[1:] + y[:-1]) / 2
    return float(np.sum(dx * (2 * ym)**3 / 12))

# two M10 316 threaded rods run the full span on the centreline (thread root 8.16 mm)
ROD_D, E_ROD, ROD_YIELD = 8.16e-3, 193e9, 450e6
EI_RODS = 2 * E_ROD * math.pi * ROD_D**4 / 64                      # N*m2
M_RODS_YIELD = 2 * ROD_YIELD * math.pi * ROD_D**3 / 32            # N*m, both rods at first yield
M_RODS_PLASTIC = 1.7 * M_RODS_YIELD                               # N*m, rods alone, fully plastic (fin folds)
# water: the fin swept sideways drags water with it
RHO = 1025.0
FIN_AREA = 0.160 * SPAN
FIN_ADDED_KG = RHO * math.pi * (0.160 / 2)**2 * SPAN               # added mass of a plate moving broadside
M_EFF = BULB_KG * (1 + 1.025 / 11.34) + FIN_ADDED_KG * 0.5         # kg, referred to the bulb (fin acts at mid-span)

def with_rods(k, EI_shell):
    """moment capacity at limiting curvature k: shell plus the rods (which stop adding once they yield)"""
    return k * EI_shell + min(k * EI_RODS, M_RODS_YIELD)

C_HALF = T_RATIO * ROOT_CHORD / 2                       # m, half thickness at the root (10.2 mm)

def wrinkling(E_f, E_c, G_c):                           # Hoff: face wrinkling stress on a foam core, Pa
    return 0.5 * (E_f * E_c * G_c) ** (1 / 3)

# materials (typical handbook values for hand lay-up; confirm with coupons)
E_GLASS, S_GLASS_C = 14e9, 200e6                        # 6 oz E-glass cloth, 2/3 of it 0/90: modulus, compressive strength
T_PLY = 0.20e-3                                         # m per 6 oz ply
E_WOOD, S_WOOD = 10e9, 70e6                             # ash/oak/mahogany-class hardwood: modulus, bending strength
E_CARBON, S_CARBON_C = 100e9, 450e6                     # hand-laid unidirectional carbon

def construction(name):
    """-> (EI in N*m2, moment capacity in N*m, added mass kg, note)"""
    if name == "as drawn: XPS core, 3 x 6 oz":
        I = skin_I(3 * T_PLY); s = min(S_GLASS_C, wrinkling(E_GLASS, 20e6, 8e6))
        return E_GLASS * I + EI_RODS, with_rods(s / (E_GLASS * C_HALF), E_GLASS * I), 0.0, "skin wrinkles on the soft core at %.0f MPa" % (s / 1e6)
    if name == "H80 PVC core, 3 x 6 oz":
        I = skin_I(3 * T_PLY); s = min(S_GLASS_C, wrinkling(E_GLASS, 90e6, 27e6))
        return E_GLASS * I + EI_RODS, with_rods(s / (E_GLASS * C_HALF), E_GLASS * I), 0.05, "skin wrinkling at %.0f MPa" % (s / 1e6)
    if name == "hardwood core, 6 x 6 oz":
        Ig, Iw = skin_I(6 * T_PLY), solid_I(); EI = E_GLASS * Ig + E_WOOD * Iw
        # first failure: glass skin in compression or wood at its outer fibre, at a common curvature
        k = min(S_GLASS_C / (E_GLASS * C_HALF), S_WOOD / (E_WOOD * C_HALF))
        return EI + EI_RODS, with_rods(k, EI), 0.60, "solid core, no wrinkling"
    if name == "hardwood core, 6 x 6 oz + carbon caps":
        Ig, Iw = skin_I(6 * T_PLY), solid_I(); Ic = 2 * (0.060 * 0.0015) * (C_HALF - 0.001)**2   # 60 x 1.5 mm UD each side
        EI = E_GLASS * Ig + E_WOOD * Iw + E_CARBON * Ic
        k = min(S_GLASS_C / (E_GLASS * C_HALF), S_WOOD / (E_WOOD * C_HALF), S_CARBON_C / (E_CARBON * C_HALF))
        return EI + EI_RODS, with_rods(k, EI), 0.75, "carbon reaches its limit first"
    raise KeyError(name)

DESIGNS = ["as drawn: XPS core, 3 x 6 oz", "H80 PVC core, 3 x 6 oz", "hardwood core, 6 x 6 oz", "hardwood core, 6 x 6 oz + carbon caps"]

# ---------------------------------------------------------------- load model for one strike
def strike_moments(EI, hs, n, rng, eta=(0.25, 0.85), tau=(0.05, 0.40)):
    """Peak fin-root moment (N*m) in n breaking-wave strikes at significant wave height hs."""
    hb_s = 0.25 * hs                                                 # breaking-crest height scale (failures.py)
    hb = hb_s * np.sqrt((H_CRIT / hb_s)**2 - np.log(rng.random(n)) / 2)   # Rayleigh tail above H_CRIT
    c_b = np.sqrt(G * 8.5 * hb / (2 * np.pi))                        # crest speed of a breaker of that height (steepness 1/8.5)
    s = np.abs(np.sin(rng.uniform(0, np.pi, n)))                     # beam-on = 1, end-on = 0
    dv_hull = rng.uniform(*eta, n) * c_b * s                         # how much of the crest speed the hull picks up
    lam = rng.uniform(0.5, 1.0, n)                                   # share of that seen at the bulb (the hull also rolls)
    rise = np.exp(rng.uniform(math.log(tau[0]), math.log(tau[1]), n))  # s, how fast the hull is accelerated
    k = 3 * EI / BULB_ARM**3                                         # cantilever stiffness at the bulb, N/m
    mu = M_EFF * HULL_KG / (M_EFF + HULL_KG)                                 # reduced mass of bulb against hull
    w = math.sqrt(k / mu)
    x = w * rise / 2; dlf = np.abs(np.sinc(x / np.pi))               # ramped velocity step: fast -> 1, slow -> 0
    m_dyn = BULB_ARM * lam * dv_hull * math.sqrt(k * mu) * dlf
    v_rel = lam * dv_hull                                            # fin and bulb swept sideways through the water
    m_drag = 0.5 * RHO * v_rel**2 * (1.2 * FIN_AREA * SPAN / 2 + 1.0 * 0.32 * 0.072 * BULB_ARM)
    m_static = BULB_KG * (1 - 1.025 / 11.34) * G * BULB_ARM * rng.uniform(0.6, 1.0, n)   # bulb weight with the boat on its side
    return np.hypot(m_dyn, m_drag) + m_static        # the two peaks do not coincide: root-sum-square

def p_fail(name, hs, rng, n=200_000, cov=0.20, **kw):
    EI, mcap, _, _ = construction(name)
    cap = mcap * np.exp(rng.normal(-cov**2 / 2, cov, n))             # strength scatter of hand lay-up
    return float(np.mean(strike_moments(EI, hs, n, rng, **kw) > cap))

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    static = BULB_KG * (1 - 1.025 / 11.34) * G * BULB_ARM
    print(f"Static moment at the fin root with the boat on its side: {static:.0f} N*m")
    print(f"\n{'construction':40s} {'EI N*m2':>8s} {'strength':>9s} {'x static':>8s} {'+kg':>5s}  note")
    for d in DESIGNS:
        EI, m, kg, note = construction(d)
        print(f"{d:40s} {EI:8.0f} {m:7.0f} N*m {m/static:7.1f}x {kg:5.2f}  {note}")
    print(f"Rods alone (after the shell has failed): yield {M_RODS_YIELD:.0f} N*m, fold at about {M_RODS_PLASTIC:.0f} N*m")
    print("Everyday rolling (30 deg each way, a few million cycles): about %.0f N*m at the root; glass lasts that long at about 25%% of its strength" % (static * 0.5 * 1.5))
    bins = np.arange(0.5, 10, 1.0)
    kd = None
    if len(sys.argv) > 1:
        runs = [r for r in json.load(open(sys.argv[1]))["result"]["runs"] if r.get("knockdowns_by_hs_m")]
        kd = np.mean([r["knockdowns_by_hs_m"] for r in runs], axis=0)
        print(f"\nKnockdowns per voyage by wave height (mean of {len(runs)} voyages): total {kd.sum():.0f}")
    for label, kw in (("central", {}), ("gentle strikes (hull picks up 15-50% of crest speed, slower)", dict(eta=(0.15, 0.5), tau=(0.10, 0.60))),
                      ("hard strikes (40-100%, faster)", dict(eta=(0.4, 1.0), tau=(0.03, 0.25)))):
        print(f"\nChance of breaking the fin in ONE knockdown, {label}")
        print(f"{'construction':40s} " + " ".join(f"Hs{b+0.5:>3.0f}m" for b in bins[2:8]) + ("   per voyage" if kd is not None else ""))
        for d in DESIGNS:
            p = np.array([p_fail(d, max(b, 1.0), rng, **kw) for b in bins])
            line = f"{d:40s} " + " ".join(f"{100*x:5.1f}%" for x in p[2:8])
            if kd is not None:
                surv = float(np.prod((1 - p[:len(kd)]) ** kd[:len(p)]))
                line += f"   {100*(1-surv):6.1f}%"
            print(line)
