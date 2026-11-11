"""Hand checks of the parts the strike simulation does not cover (Rev C2). 11 Nov 2026, grade D.
Each line: load case -> stress or load -> allowable -> factor of safety. Assumptions are in the code, next to the numbers.
Run:  python structural_checks.py
"""
import math
RHO, G = 1025.0, 9.81
T_PLY = 0.20e-3
GLASS_T, GLASS_C = 250e6, 200e6           # hand-laid 6 oz cloth, tension / compression, Pa
H80_SHEAR, H80_CRUSH = 1.15e6, 1.4e6      # Divinycell H80 data sheet
rows = []
def row(part, case, value, allow, unit, note=""):
    rows.append((part, case, value, allow, unit, allow / value if value else float("inf"), note))

def sandwich(p, b, t_tension, t_comp, core=0.010, k_m=1/8, k_v=1/2):
    """Long sandwich panel, width b, pressure p: skin stresses and core shear."""
    d = core + (t_tension + t_comp) / 2
    M, V = k_m * p * b**2, k_v * p * b
    return M / (t_tension * d), M / (t_comp * d), V / d

# ---- water pressure cases
c95, c999 = 4.8, 5.7                       # breaker speed at Hs 5 m, 95% and 99.9% (strike_sim.py)
p_slam = lambda c, cp=math.pi: 0.5 * RHO * cp * c**2      # local slam pressure, pressure coefficient pi averaged over a panel
p_green = lambda h: RHO * G * h                           # green water standing on the deck

# 1. Hull bottom over the sump: the only shell panel with no foam behind it (x 560-770, about 210 x 250 mm, curved)
for c, tag in ((c95, "1 in 20 strike"), (c999, "1 in 1,000 strike")):
    st, sc, tau = sandwich(p_slam(c), 0.21, 1 * T_PLY, 2 * T_PLY, k_m=1/10)
    row("Hull bottom over the sump (unbacked)", f"slam {p_slam(c)/1e3:.0f} kPa, {tag}: inner skin tension", st / 1e6, GLASS_T / 1e6, "MPa", "1 ply inside")
    row("Hull bottom over the sump (unbacked)", f"same: core shear", tau / 1e6, H80_SHEAR / 1e6, "MPa")
# 2. Foam-backed shell and deck: the skin sits on H80 and XPS, so the check is crushing of the foam under the skin
row("Hull and deck where foam-backed", f"slam {p_slam(c999)/1e3:.0f} kPa on XPS fill (250 kPa at 10% strain)", p_slam(c999) / 1e3, 250, "kPa", "local dent, not a hole")
# 3. Deck over the hatch well and the hatch lid (220 x 200 opening, nothing under it)
for lid, t in (("4 mm G10 lid", 4e-3),):
    p = p_slam(c999, 2.0)                  # water falling on the deck: stagnation pressure x 2
    sig = 0.287 * p * 0.21**2 / t**2       # simply supported square plate
    row("Hatch lid, " + lid, f"plunging jet on deck {p/1e3:.0f} kPa", sig / 1e6, 300, "MPa", "G10 flexural strength 300+ MPa")
    row("Hatch bolts (12 x M5 into inserts)", f"same, lifting when inverted: {p*0.22*0.20/12:.0f} N each", p * 0.22 * 0.20 / 12, 1500, "N", "brass insert in glass/foam: pull-out about 1.5 kN, check")
st, sc, tau = sandwich(p_slam(c999, 2.0), 0.21, 3 * T_PLY, 3 * T_PLY, core=0.006)
row("Hatch lid, 3 x 6 oz over 6 mm foam", "same", st / 1e6, GLASS_C / 1e6, "MPa")
row("Hatch lid, 3 x 6 oz over 6 mm foam", "same: core shear", tau / 1e6, H80_SHEAR / 1e6, "MPa", "must be H80, not XPS")

# 4. Mast: spar bearing loads into the printed housing P07 and the deck
for M, tag in ((690, "spar at its breaking load"), (1130, "30 x 22 spar at its breaking load")):
    R = M / 0.078                          # bearings 78 mm apart
    row("Bearing housing P07 (printed PETG)", f"{tag}: {R/1e3:.1f} kN on a 42 x 7 mm seat", R / (0.042 * 0.007) / 1e6, 50, "MPa", "PETG yield about 50 MPa; creeps above about 15")
    row("Mast tube to deck ring", f"{tag}: {R/1e3:.1f} kN sideways at the deck", R / (0.060 * 0.0106 * 1.0) / 1e6, 60, "MPa", "bearing of the tube on the deck skins + collar; needs a 60 mm wide glass collar")
# 5. Keel bolts and hull girder in a bottom slam (boat dropped off a crest, 3 m/s, about 50 g for a few ms)
a = 50 * G
row("Keel rods (2 x M10 316) in a bottom slam", "bulb 9.2 kg x 50 g", 9.2 * a / 2 / 58e-6 / 1e6, 450, "MPa", "tension in each rod")
M_h = 9.2 * a * 1.5 / 8
row("Hull girder in a bottom slam", f"bending {M_h:.0f} N*m amidships", M_h / (0.40 * 3 * T_PLY * 0.23) / 1e6, GLASS_C / 1e6, "MPa", "deck skins in compression")
# 6. Battery (2.35 kg with its box) on two straps and four bonded anchors
F = 2.35 * 60 * G
row("Battery straps and anchors P16", f"60 g jolt: {F:.0f} N shared by 4 anchors", F / 4 / (0.060 * 0.024) / 1e6, 5.0, "MPa", "epoxy bond of a printed part to the hull: 5 MPa shear, peel is worse")
# 7. Rudder trunks and bushings
Fr = 0.5 * RHO * 1.2 * 0.0276 * 4.0**2
row("Rudder lower bushing / trunk", f"blade broadside at 4 m/s: {Fr:.0f} N", Fr * (1 + 0.115 / 0.10), 3000, "N", "iglide J 12 mm bushing static rating, trunk glassed to hull and deck")
# 8. Wind alone
for v in (33, 50):
    q = 0.5 * 1.225 * v**2
    row("Wing spar, wind alone", f"{v} m/s, wing feathered (CdA 0.015 m2) / jammed broadside (0.36 m2)", q * 0.36 * 0.55, 690, "N*m", f"feathered {q*0.015*0.55:.0f} N*m")
# 9. Shock on boom-level masses from a bottom slam (velocity step w, not covered by the sideways strike)
for w in (1.0, 2.0, 3.0):
    for name, m, L, EI, cap in (("Counterweight arm, 12 x 10 carbon", 1.0, 0.26, 52.7, 53), ("Counterweight arm, 12 mm solid glass rod", 1.0, 0.26, 40.7, 119), ("Tail boom, 12 x 10 carbon", 0.25, 0.56, 52.7, 53)):
        row(name, f"bottom slam, velocity step {w:.0f} m/s (drop of {w*w/2/G*100:.0f} cm)", L * w * math.sqrt(3 * EI / L**3 * m), cap, "N*m")

print(f"{'part':42s} {'load case':78s} {'value':>8s} {'limit':>7s} unit  {'FoS':>5s}  note")
for part, case, v, a_, u, f, note in rows:
    flag = "  <-- FAILS" if f < 1 else ("  <-- marginal" if f < 1.5 else "")
    print(f"{part:42s} {case:78s} {v:8.1f} {a_:7.0f} {u:5s} {f:5.1f}  {note}{flag}")
