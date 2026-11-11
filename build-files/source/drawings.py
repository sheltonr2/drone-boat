import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Polygon, Circle, Ellipse
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import design as D
import parts as Pm
from sheet import *

OUT = "out"
STATIONS = np.arange(0, 1501, 150)

# ------------------------------------------------------------------ geometry helpers
def hull_profile():
    x = np.linspace(0, D.L, 301)
    top = np.c_[x, D.deck_z(x)]; bot = np.c_[x, D.keel_z(x)]
    return np.r_[bot, top[::-1]]

def hull_plan():
    x = np.linspace(0, D.L, 301); b = D.half_beam(x)
    return np.r_[np.c_[x, b], np.c_[x[::-1], -b[::-1]]]

def fin_poly():
    F = D.FIN
    return np.array([[F['root_le_x'], F['root_z']], [F['root_le_x'] + F['root_chord'], F['root_z']],
                     [F['tip_le_x'] + F['tip_chord'], F['tip_z']], [F['tip_le_x'], F['tip_z']]])

def bulb_profile():
    xl = np.linspace(0, D.BULB['length'], 200); r = D.bulb_radius(xl)
    x = D.BULB['nose_x'] + xl; z = D.BULB['axis_z']
    return np.r_[np.c_[x, z + r], np.c_[x[::-1], z - r[::-1]]]

def rudder_poly():
    R = D.RUDDER; le = R['stock_x'] - R['stock_from_le']
    return np.array([[le, R['top_z']], [le + R['chord'], R['top_z']], [le + R['chord'] - 8, R['bot_z']], [le + 6, R['bot_z']]])

def wing_rect():
    W = D.WING; le = D.MAST_X - W['pivot_from_le']
    return le, le + W['chord'], W['root_z'], W['root_z'] + W['span']

def poly(ax, P, **kw):
    kw.setdefault("fill", False); kw.setdefault("lw", MED); kw.setdefault("ec", INK)
    ax.add_patch(Polygon(P, closed=True, **kw))

def foil_xy(t, c, x0=0, y0=0, rot=0):
    xs, ys = D.naca(t, c, 90)
    return np.c_[xs + x0, ys + y0]

# ------------------------------------------------------------------ D00 cover / index
def sheet_cover(pdf, index):
    fig, bg = new_sheet("D00", "Cover, index and general notes")
    bg.text(20, 262, "Solar-sail ocean drone, 1.5 m", fontsize=20, weight="bold")
    bg.text(20, 252, "Drawing set for the custom-built parts, with 3D-print files and full-size templates", fontsize=10, color=BLUE)
    y = table(bg, 20, 240, ["Sheet", "Title"], index, [18, 120], fs=6.3, rh=4.4)
    rows = [[p['id'], p['name'], p['qty'], p['mat']] for p in Pm.PARTS.values()]
    table(bg, 170, 240, ["Part", "3D-printed part", "Qty", "Material / settings"], rows, [12, 95, 9, 62], fs=5.6, rh=4.1)
    notes(bg, 20, y - 6, "General notes", [
        "1. All dimensions in millimetres. Model origin: x aft from the bow, z up from the hull bottom at midships, y to port.",
        f"2. Design waterline (DWL) z = {D.DWL:.0f} at about {D.MASS_KG:.1f} kg all-up mass (Rev B: z 90 at about 21 kg).",
        "3. Printed parts: 0.4 mm nozzle, 0.2 mm layers, 4+ walls. Use ASA outdoors in UV; PETG is fine below deck.",
        "   STL files are in print orientation; no supports needed except where a sheet says so.",
        "4. Bought-in parts follow the Recommended Parts list in the build plan. Servo tab spacing, AS5600 board size and",
        "   patch-antenna footprint vary by supplier: printed parts use slots and recesses rather than fixed hole patterns.",
        "5. Full-size cutting templates (hull frames, foils, wing, hatch) are in Templates.pdf (tiled on Letter, 1:1)",
        "   and as DXF files. Check the 100 mm scale bar on every printed page before cutting.",
        "6. All fasteners and shafts 316 stainless. Bed every hull penetration in polyurethane sealant.",
        "7. This is a hobby design, not a classed or certified vessel. Tank-test self-righting before going to sea.",
        "",
        "Rev B (2026-11-08): wing counterweight moved from the wing's nose pocket to pod P18 on a 300 mm forward arm.",
        "Rev C (2026-11-10), after the first real-weather Monte Carlo (leaks, wing damage and steering failures were the top losses):",
        "   1. Hull foam-filled behind two glassed-in bulkheads (x 300, 1260), battery in its own sealed box: a leak can't swamp it (D03, D09).",
        "   2. Twin rudders, 100 mm either side of the centreline, each with its own trunk, servo and tiller: either one steers alone (D05).",
        "   3. Wing spar 30 x 26 carbon on 6806-2RS bearings (was 25 mm / 6805): about 1.8x the bending strength (D06, D07, P07, P08).",
        "   4. Bulb D72 (was D68), about 9.2 kg, to hold stability at the higher mass (D04, P14).",
        "   5. YB3 backup tracker platform P19 and all-round white light P20 on the stub; label areas (D01, D07, D09).",
        "   Removed: thruster provision and the backup D-cell. Mass about 25 kg, DWL z 98, still self-righting from 180 deg.",
        "Rev C1 (2026-11-11): electronics box raised onto a shelf (bottom z 118, was 60), above the 3 L sump at the low point of the dry bay;",
        "   cable glands on the box top with drip loops, gel-filled connectors, desiccant. A leak no longer sits against the box (D03, D09).",
        "Rev C2 (2026-11-11): keel fin rebuilt after a strength check: hardwood core, 6 x 6 oz glass and a carbon strip each side, 60 mm tenon into",
        "   a keel-box socket, two ply floors across the hull (D04, T12, T13, T19, T20). About +1.1 kg. Proof-load before launch.",
        "Rev C3 (2026-11-11), after the whole-boat structural review (docs/Structural_Review.md): 1. YB3 moved from the stern post to a well in the foredeck;",
        "   post is now 20 x 2 fibreglass tube (D01, D07, P19). 2. Counterweight arm is a 12 mm solid fibreglass rod (D06). 3. Spring servo-saver and tiller",
        f"   stops on each rudder (D05). 4. Spar 30 x 22 carbon, bearings 130 apart in a longer P07 (D06, D07). 5. Second inner ply over the sump (D03). {D.MASS_KG:.1f} kg, DWL z {D.DWL:.0f}.",
        "Rev C4 (2026-11-11), after the research review (docs/Research_Review.md): mast bearings are acetal (Delrin-type) with glass balls, floating on O-rings, with",
        "   plain catcher lands in P07 for wave loads, and a V-ring seal on the spar (D07, P07). Notes added: fin glue-up and rod bedding (D04), rudder trunks (D05).",
        "   ALL printed parts that see sun or sea: 2 coats of epoxy, then paint. Antifouling: 3 coats of ablative copper paint on hull, fin, bulb and rudders.",
        f"Rev C5 (2026-11-11): wing 800 x 375 (was 1000 x 300), same area, spar 995 long, after docs/Wing_Shape_Study.md (D01, D06, T15). {D.MASS_KG:.1f} kg, DWL z {D.DWL:.0f}."], fs=5.4, lh=3.05)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D01 general arrangement
def sheet_ga(pdf):
    fig, bg = new_sheet("D01", "General arrangement", "Scale 1:8.5 on tabloid")
    s = 8.5
    ax = view(fig, 16, 45, (-30, 1620), (-530, 1340), s, "PROFILE (starboard side, wing feathered aft)")
    poly(ax, hull_profile(), lw=THICK)
    poly(ax, fin_poly()); poly(ax, bulb_profile(), fc="#555", fill=True, ec=INK)
    poly(ax, rudder_poly())
    R = D.RUDDER
    ax.plot([R['stock_x']] * 2, [R['bot_z'] + 10, D.DECK_Z - 20], color=INK, lw=THIN, ls="--")
    ax.plot([-20, 1520], [D.DWL, D.DWL], color=WATER, lw=0.8); ax.text(-25, D.DWL, "DWL", color=WATER, fontsize=5.5, ha="right", va="center")
    for xb in D.BULKHEADS:
        ax.plot([xb, xb], [float(D.keel_z(xb)) + 11, float(D.deck_z(xb)) - 11], color=INK, lw=MED, ls="--")
    Y = D.YB3; NL = D.NAVLIGHT
    zy = float(D.deck_z(Y['x']))
    ax.add_patch(Rectangle((Y['x'] - Y['box'][0] / 2, zy - Y['box'][2]), Y['box'][0], Y['box'][2], fc="#f6c443", ec=INK, lw=THIN))
    ax.add_patch(Circle((D.STUB['x'] + NL['reach'], NL['z'] + 8), 12, fc="white", ec=INK, lw=THIN))
    MT = D.MAST_TUBE
    ax.add_patch(Rectangle((D.MAST_X - MT['od']/2, float(D.keel_z(D.MAST_X))), MT['od'], MT['top_z'] - float(D.keel_z(D.MAST_X)), fill=False, lw=THIN, ls="--"))
    le, te, z0, z1 = wing_rect()
    ax.add_patch(Rectangle((le, z0), te - le, z1 - z0, fill=False, lw=MED))
    ax.plot([D.MAST_X] * 2, [150, z1 - 10], color=INK, lw=THIN, ls="-.")
    B = D.BOOM; T = D.TAIL
    tp = D.MAST_X + B['length']
    ax.plot([D.MAST_X, tp], [B['z']] * 2, color=INK, lw=MED)
    ax.add_patch(Rectangle((tp - T['pivot_from_le'], T['bot_z']), T['chord'], T['span'], fill=False, lw=MED))
    ax.add_patch(Rectangle((tp - 30, 252), 60, 48, fill=False, lw=THIN))
    C = D.CWARM; px = D.MAST_X - C['reach']
    ax.plot([px, D.MAST_X], [C['z']] * 2, color=INK, lw=MED)
    ax.add_patch(Rectangle((px - C['pod_od']/2, C['pod_bot_z']), C['pod_od'], C['pod_h'], fc="#888", ec=INK, lw=THIN))
    S = D.STUB
    ax.plot([S['x']] * 2, [S['bot_z'], S['top_z']], color=INK, lw=1.4)
    ax.add_patch(Rectangle((D.L, 160), 30, 100, fill=False, lw=THIN))
    ax.plot([S['x'] - 75, S['x'] + 190], [D.VANE_Z + 8] * 2, color=INK, lw=MED)
    ax.add_patch(Rectangle((S['x'] + 120, D.VANE_Z + 8), 80, 80, fill=False, lw=THIN))
    ax.add_patch(Rectangle((S['x'] - 20, D.VANE_Z - 52), 40, 60, fill=False, lw=THIN))
    ax.add_patch(Rectangle((S['x'] + 10, D.ANT_Z), 80, 6, fill=True, fc=INK))
    ax.add_patch(Polygon([[S['x'], 330], [S['x'] + 70, 400], [S['x'], 470], [S['x'] - 70, 400]], fill=False, lw=THIN))
    for P in D.SOLAR:
        ax.plot([P['x0'], P['x1']], [float(D.deck_z(P['x0'])) + 3] * 2, color=BLUE, lw=2)
    dim(ax, (0, -510), (1500, -510), 0, "LOA 1500")
    zb = D.BULB['axis_z'] - D.BULB['dia'] / 2
    dim(ax, (1590, D.DWL), (1590, zb), 0, f"draft {D.DWL - zb:.0f}")
    dim(ax, (1590, D.DWL), (1590, D.WING_TOP_Z), 0, f"air draft {D.WING_TOP_Z - D.DWL:.0f}")
    dim(ax, (le, D.WING_TOP_Z + 20), (te, D.WING_TOP_Z + 20), 0, f"{D.WING['chord']}")
    dim(ax, (440, 300), (440, D.WING_TOP_Z), 0, f"wing {D.WING['span']}")
    leader(ax, (700, -200), (300, -250), "Keel fin  NACA 0012\n170/150 chord  (D04)")
    leader(ax, (750, D.BULB['axis_z']), (300, -400), f"Lead bulb {D.bulb_mass()[1]:.1f} kg  (D04)")
    leader(ax, (1440, -80), (1050, -330), "Twin spade rudders, 100 mm\neither side of centre  (D05)")
    leader(ax, (Y['x'], zy - 10), (60, 420), "C3: YB3 backup tracker in a\nforedeck well on P19  (D07)", ha="left")
    leader(ax, (D.STUB['x'] + NL['reach'], NL['z'] + 20), (1640, 820), "All-round white\nlight P20", ha="left")
    leader(ax, (D.BULKHEADS[1], 150), (1050, 60), "Watertight bulkheads x 300, 1260;\nhull foam-filled  (D09)")
    leader(ax, (te, 900), (1000, 1000), "Rigid wing sail\nNACA 0015  (D06)")
    leader(ax, (1250, 450), (1150, 760), "Tail flap on servo  (D06)")
    leader(ax, (S['x'], 400), (1250, 600), "Radar reflector")
    leader(ax, (S['x'] + 160, D.VANE_Z + 40), (1300, 1100), "Wind vane P01-P04\nantenna platform P05\non 20 mm stub  (D07)")
    leader(ax, (D.MAST_X, 200), (250, 520), "2 in. PVC mast tube +\nbearing housing P07  (D07)")
    leader(ax, (px, C['pod_bot_z'] + C['pod_h']), (120, 760), "Counterweight pod P18\non 300 mm arm  (D06)")
    ax.text(820, 150, "solar", fontsize=5, color=BLUE)

    ax2 = view(fig, 222, 200, (-30, 1620), (-235, 235), s, "PLAN (deck)")
    poly(ax2, hull_plan(), lw=THICK)
    ax2.plot([0, 1500], [0, 0], color=GREY, lw=0.25, ls="-.")
    H = D.HATCH
    ax2.add_patch(Rectangle((H['x0'], -H['w']/2), H['x1'] - H['x0'], H['w'], fill=False, lw=MED, ls="--"))
    ax2.add_patch(Rectangle((H['x0'] - 30, -H['w']/2 - 30), H['x1'] - H['x0'] + 60, H['w'] + 60, fill=False, lw=THIN))
    ax2.text((H['x0'] + H['x1'])/2, -55, "bolted\nhatch", fontsize=5, ha="center", va="center")
    ax2.add_patch(Circle((D.MAST_X, 0), D.MAST_TUBE['od']/2, fill=False, lw=MED))
    for i, P in enumerate(D.SOLAR):
        ax2.add_patch(Rectangle((P['x0'], -P['w']/2), P['x1'] - P['x0'], P['w'], fc="#cfe0f3", ec=BLUE, lw=THIN))
        ax2.text((P['x0'] + P['x1'])/2, 0, f"solar panel {i+1}\n~20 W  420 x 280", fontsize=5, ha="center", va="center", color=BLUE)
    ax2.add_patch(Circle((D.STUB['x'], 0), 10, fill=False, lw=MED))
    for yr in D.RUDDER_Y:
        le_r = D.RUDDER['stock_x'] - D.RUDDER['stock_from_le']
        ax2.add_patch(Polygon(foil_xy(0.12, D.RUDDER['chord'], le_r, yr), closed=True, fill=False, lw=THIN, ls="--"))
    for xb in D.BULKHEADS:
        hb = float(D.half_beam(xb)) - 11
        ax2.plot([xb, xb], [-hb, hb], color=INK, lw=MED, ls="--")
    ax2.add_patch(Rectangle((D.YB3['x'] - 75, -43), 150, 86, fc="#f6c443", ec=INK, lw=THIN))
    ax2.text(D.YB3['x'], 0, "YB3", fontsize=5, ha="center", va="center")
    ax2.text(1330, -150, "rudders (dashed,\nbelow hull)", fontsize=4.8, ha="center", color=GREY)
    ax2.add_patch(Circle((D.MAST_X, 0), 700, fill=False, lw=0.3, ls=":", ec=GREY))
    ax2.text(D.MAST_X + 495, -215, "tail sweep R 700", fontsize=5, color=GREY, rotation=45)
    ax2.add_patch(Circle((D.MAST_X, 0), D.CWARM['reach'] + D.CWARM['pod_od']/2, fill=False, lw=0.3, ls=":", ec=GREY))
    ax2.add_patch(Circle((D.MAST_X - D.CWARM['reach'], 0), D.CWARM['pod_od']/2, fc="#bbb", ec=INK, lw=THIN))
    ax2.plot([D.MAST_X - D.CWARM['reach'], D.MAST_X], [0, 0], color=INK, lw=MED)
    ax2.text(150, -135, "pod sweep R 332\n(keep deck clear\nabove z 255)", fontsize=5, color=GREY, ha="center", va="top")
    dim(ax2, (1500, -200), (1500, 200), 0, "")
    ax2.text(1515, 0, "beam 400\n(max at x 825)", fontsize=5.5, va="center")
    dim(ax2, (0, 215), (D.MAST_X, 215), 0, "600")
    dim(ax2, (0, -222), (H['x0'], -222), 0, "330")
    notes(bg, 225, 180, "Key data (Rev C)", [
        "Length overall 1500   Beam 400   Hull depth 230",
        f"Draft {D.DWL - zb:.0f} (DWL to bulb bottom)   Air draft {D.WING_TOP_Z - D.DWL:.0f}",
        f"Displacement about {D.MASS_KG:.0f} kg   Ballast {D.bulb_mass()[1]:.1f} kg lead + about 0.8 kg rig counterweight",
        f"Wing {D.WING['span']} x {D.WING['chord']} (0.30 m2; Rev C5), free-rotating on a 30 mm spar",
        "Two rudders, two servos; hull foam-filled, two bulkheads",
        "Solar about 40 W on deck   Battery 192 Wh LiFePO4 in a sealed box",
        "Self-righting from 180 deg (simulator): verify in a tank test (Gate 3)"], fs=6.3)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D02 hull lines
def sheet_lines(pdf):
    fig, bg = new_sheet("D02", "Hull lines and table of offsets", "Profile & plan 1:5, body plan 1:2.5")
    s = 5
    ax = view(fig, 20, 205, (-20, 1520), (-14, 270), s, "")
    bg.text(20, 262, "PROFILE", fontsize=7, weight="bold")
    poly(ax, hull_profile(), lw=MED)
    for i, x in enumerate(STATIONS):
        ax.plot([x, x], [float(D.keel_z(x)), float(D.deck_z(x))], color=GREY, lw=0.3)
        ax.text(x, -8, str(i), fontsize=5, ha="center", va="top")
    for wl in (30, 60, D.DWL, 120, 150):
        xs = np.linspace(0, 1500, 300); m = D.keel_z(xs) < wl
        ax.plot(xs[m], np.full(m.sum(), wl), color=WATER if wl == D.DWL else GREY, lw=0.6 if wl == D.DWL else 0.25, ls="-" if wl == D.DWL else ":")
    ax2 = view(fig, 20, 152, (-20, 1520), (-10, 215), s, "")
    bg.text(20, 200, "HALF-BREADTH PLAN (deck edge solid, DWL blue, waterlines z 30/60/120/150 dotted)", fontsize=7, weight="bold")
    xs = np.linspace(0, 1500, 300)
    ax2.plot(xs, D.half_beam(xs), color=INK, lw=MED); ax2.plot([0, 1500], [0, 0], color=INK, lw=0.3)
    ax2.plot([1500, 1500], [0, D.B_TRANSOM], color=INK, lw=MED)
    for wl in (30, 60, D.DWL, 120, 150):
        ax2.plot(xs, [D.half_beam_at(x, wl) for x in xs], color=WATER if wl == D.DWL else GREY, lw=0.4 if wl == D.DWL else 0.25, ls="-" if wl == D.DWL else ":")
    for x in STATIONS:
        ax2.plot([x, x], [0, float(D.half_beam(x))], color=GREY, lw=0.3)
    ax3 = view(fig, 15, 28, (-215, 215), (-10, 275), 2.5, "")
    bg.text(15, 146, "BODY PLAN (stations 0-5 left, 5-10 right)", fontsize=7, weight="bold")
    for i, x in enumerate(STATIONS):
        y, z = D.section(x)
        side = -1 if i <= 5 else 1
        ax3.plot(side * y, z, color=INK, lw=0.5)
        if i in (0, 5, 10) or True:
            ax3.text(side * (y[-1] + 3), z[-1] + 2, str(i), fontsize=4.8, ha="center")
    ax3.plot([0, 0], [-5, 270], color=INK, lw=0.3, ls="-.")
    ax3.plot([-210, 210], [D.DWL, D.DWL], color=WATER, lw=0.5)
    rows = []
    for i, x in enumerate(STATIONS):
        rows.append([i, int(x), f"{float(D.keel_z(x)):.1f}", f"{float(D.deck_z(x)):.1f}", f"{float(D.half_beam(x)):.1f}",
                     f"{D.half_beam_at(x, 30):.1f}", f"{D.half_beam_at(x, 60):.1f}", f"{D.half_beam_at(x, D.DWL):.1f}",
                     f"{D.half_beam_at(x, 150):.1f}"])
    table(bg, 205, 145, ["Stn", "x", "keel z", "deck z", "1/2 b deck", "1/2 b z30", "1/2 b z60", "1/2 b DWL", "1/2 b z150"],
          rows, [9, 11, 13, 13, 17, 16, 16, 17, 17], fs=5.4, rh=3.8)
    notes(bg, 205, 92, "Section formula (exact; use it for intermediate points)", [
        "Half-breadth at height z:  y = b(x) [1 - (1 - t)^2.2]^(1/2.2),  t = (z - keel z) / (deck z - keel z)",
        "b(x) = 200 [1 - (1 - x/825)^2]^0.6 forward of x 825;  200 - 50 ((x - 825)/675)^2 aft",
        "Keel z = 120 (1 - x/750)^2.2 forward of x 750;  60 ((x - 750)/750)^2 aft",
        "Deck z = 230 + 30 (1 - x/600)^2 forward of x 600;  230 aft",
        "",
        "Construction: 10 mm H80 foam strips over 11 MDF frames (Templates T01-T11, cut on the",
        "dashed frame line = hull minus 11 mm), 2 x 6 oz glass outside, 1 x 6 oz inside, peel ply.",
        f"Rev C: hull form unchanged; DWL now z {D.DWL:.0f} at about {D.MASS_KG:.0f} kg (the 1/2 b DWL column is at z {D.DWL:.0f})."], fs=6.0, lh=3.4)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D03 interior
def inner_profile(x0, x1, skin=11.0):
    x = np.linspace(x0, x1, 120)
    return np.r_[np.c_[x, D.keel_z(x) + skin], np.c_[x[::-1], D.deck_z(x[::-1]) - skin]]

def inner_plan(x0, x1, z=None, skin=11.0):
    x = np.linspace(x0, x1, 120)
    b = np.maximum(D.half_beam(x) - skin, 0)
    return np.r_[np.c_[x, b], np.c_[x[::-1], -b[::-1]]]

FOAM = dict(fc="#f3ecd9", ec="#b8a77a", lw=0.3, hatch="....")

def sheet_interior(pdf):
    fig, bg = new_sheet("D03", "Interior arrangement and systems", "Scale 1:7.5")
    s = 7.5
    ax = view(fig, 15, 165, (-20, 1560), (-40, 270), s, "INBOARD PROFILE (Rev C: foam fill shaded, dry spaces white)")
    poly(ax, hull_profile(), lw=MED, ec=GREY)
    b0, b1 = D.BULKHEADS
    for x0, x1 in ((0, b0), (b0, b1), (b1, D.L)):
        ax.add_patch(Polygon(inner_profile(x0, x1), closed=True, **FOAM))
    MT = D.MAST_TUBE; kz = float(D.keel_z(D.MAST_X))
    BB = D.BATTBOX; E = D.EBOX; B = D.BATTERY; R = D.RUDDER
    # dry spaces cut out of the foam (white)
    for (x0, z0, w, h) in [(D.MAST_X - MT['od']/2, kz, MT['od'], MT['top_z'] - kz), (BB['x0'], BB['z0'], BB['x1'] - BB['x0'], BB['z1'] - BB['z0']),
                           (E['x0'] - 8, E['z0'] - 6, E['x1'] - E['x0'] + 16, E['h'] + 14), (D.SUMP['x0'], 11, D.SUMP['x1'] - D.SUMP['x0'], D.SUMP['top_z'] - 11), (D.KEELBOX['x0'], 0, D.KEELBOX['x1'] - D.KEELBOX['x0'], 84), (330, 160, 200, 59),
                           (1295, 112, 70, 64), (R['stock_x'] - 14, 76, 28, 104)]:
        ax.add_patch(Rectangle((x0, z0), w, h, fc="white", ec="none"))
    for xb in D.BULKHEADS:
        ax.plot([xb, xb], [float(D.keel_z(xb)) + 11, float(D.deck_z(xb)) - 11], color=INK, lw=1.4)
    ax.add_patch(Rectangle((D.MAST_X - MT['od']/2, kz), MT['od'], MT['top_z'] - kz, fill=False, lw=MED))
    ax.add_patch(Rectangle((D.MAST_X - 27, MT['top_z'] - 80), 54, 85, fill=False, lw=THIN, hatch="////"))
    ax.plot([D.MAST_X] * 2, [150, 270], color=INK, lw=0.8)
    ax.add_patch(Rectangle((D.MAST_X - 8, 120), 16, 30, fc="#ddd", ec=INK, lw=THIN))
    KB = D.KEELBOX
    ax.add_patch(Rectangle((KB['x0'], 0), KB['x1'] - KB['x0'], KB['h'], fill=False, lw=MED, hatch="\\\\"))
    ax.add_patch(Rectangle((KB['x0'], KB['h']), KB['x1'] - KB['x0'], KB['plate_t'], fc="#bbb", ec=INK, lw=THIN))
    for xr in (707, 762):
        ax.plot([xr, xr], [-30, KB['h'] + KB['plate_t'] + 12], color=INK, lw=1)
    for xf, zf in D.FLOORS:
        ax.plot([xf, xf], [float(D.keel_z(xf)) + 11, zf], color=INK, lw=1.6)
    ax.add_patch(Rectangle((BB['x0'], BB['z0']), BB['x1'] - BB['x0'], BB['z1'] - BB['z0'], fill=False, lw=MED, ec=INK))
    ax.add_patch(Rectangle((B['x0'], 42), B['x1'] - B['x0'], B['h'], fc="#f4e3c3", ec=INK, lw=MED))
    ax.add_patch(Rectangle((E['x0'], E['z0']), E['x1'] - E['x0'], E['h'], fc="#d9e8d4", ec=INK, lw=MED))
    ax.plot([E['x0'] - 8, E['x1'] + 8], [E['z0'] - 3] * 2, color=INK, lw=1.2)
    ax.plot([D.SUMP['x0'], D.SUMP['x1']], [D.SUMP['top_z']] * 2, color=WATER, lw=0.6, ls="--")
    leader(ax, (D.SUMP['x0'] + 30, 30), (640, 318), "Sump: the only open space (3 L max), water line dashed", color=BLUE, ha="right")
    leader(ax, (E['x0'] + 40, E['z0'] - 3), (1010, 288), "C1: box on a glassed foam shelf, bottom z 118,\n70 mm above the sump; glands on top", ha="right")
    zt = D.hull_z_at(R['stock_x'], D.RUDDER_Y[1])
    ax.add_patch(Rectangle((R['stock_x'] - 9, zt), 18, R['trunk_top_z'] - zt, fill=False, lw=MED))
    ax.plot([R['stock_x']] * 2, [R['bot_z'] + 8, 196], color=INK, lw=0.8)
    ax.add_patch(Rectangle((1300, 120), 60, 48, fc="#eee", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((1380, 180), 50, 16, fc=INK))
    ax.add_patch(Rectangle((330, 230), 200, 8, fill=False, lw=MED))
    for xp in (560, 1000, 1330):
        zp = float(D.keel_z(xp)) + 14 if xp < b1 else 116
        ax.add_patch(Circle((xp, zp), 5, fc=BLUE, ec=BLUE))
    leader(ax, (D.MAST_X + 27, 200), (330, 140), "Mast tube 2 in. sch 40 PVC,\nglassed to hull + deck")
    leader(ax, (D.MAST_X, 135), (200, 70), "6-wire capsule slip ring\n(tail servo power + signal)")
    leader(ax, (700, 20), (600, -25), "C2: keel box takes the fin tenon (60 deep), 2 x M10 rods,\nG10 plate on top; ply floors at x 650 and x 800 (D04)", ha="right")
    leader(ax, (870, 210), (830, 258), "Sealed battery box (O-ring lid, removable), strapped down on P16")
    leader(ax, (1100, 190), (1060, 318), "IP68 box: Pixhawk, ESP32, RockBLOCK, GPS, GV-5 MPPT (tray P15)")
    leader(ax, (R['stock_x'], 120), (1500, 30), "Twin rudder trunks (x2,\n100 off centre), top z 175")
    leader(ax, (1330, 168), (1180, 40), "Servos P12 + tillers P11 (x2)\nin pockets in the aft foam")
    leader(ax, (150, 120), (20, 258), "Foam-filled, sealed (no fittings)", ha="left")
    leader(ax, (b0, 60), (250, -25), "Bulkhead x 300 (T17)", ha="right")
    leader(ax, (b1, 60), (1150, -25), "Bulkhead x 1260 (T18)", ha="right")
    leader(ax, (560, float(D.keel_z(560)) + 14), (60, 288), "Leak probes (SOS) at the low points of each dry space", color=BLUE)
    ax.plot([0, 1500], [D.DWL, D.DWL], color=WATER, lw=0.5)
    ax2 = view(fig, 15, 70, (-20, 1560), (-220, 220), s, "INTERIOR PLAN (below deck, at z 120)")
    poly(ax2, hull_plan(), lw=MED, ec=GREY)
    for x0, x1 in ((0, b0), (b0, b1), (b1, D.L)):
        ax2.add_patch(Polygon(inner_plan(x0, x1), closed=True, **FOAM))
    for (x0, y0, w, h) in [(BB['x0'], -BB['w']/2, BB['x1'] - BB['x0'], BB['w']), (E['x0'] - 8, -E['w']/2 - 8, E['x1'] - E['x0'] + 16, E['w'] + 16),
                           (650, -30, 190, 60), (330, -110, 200, 220)]:
        ax2.add_patch(Rectangle((x0, y0), w, h, fc="white", ec="none"))
    ax2.add_patch(Circle((D.MAST_X, 0), MT['od']/2, fc="white", ec=INK, lw=MED))
    for xb in D.BULKHEADS:
        hb = float(D.half_beam(xb)) - 11
        ax2.plot([xb, xb], [-hb, hb], color=INK, lw=1.4)
    ax2.add_patch(Rectangle((650, -30), 190, 60, fill=False, lw=MED, hatch="\\\\"))
    ax2.add_patch(Rectangle((BB['x0'], -BB['w']/2), BB['x1'] - BB['x0'], BB['w'], fill=False, lw=MED))
    ax2.add_patch(Rectangle((B['x0'], -B['w']/2), B['x1'] - B['x0'], B['w'], fc="#f4e3c3", ec=INK))
    ax2.add_patch(Rectangle((E['x0'], -E['w']/2), E['x1'] - E['x0'], E['w'], fc="#d9e8d4", ec=INK))
    for yr in D.RUDDER_Y:
        ax2.add_patch(Rectangle((1290, yr - 22), 80, 44, fc="white", ec="none"))
        ax2.add_patch(Circle((R['stock_x'], yr), 9, fill=False, lw=MED))
        ax2.add_patch(Rectangle((1300, yr - 15), 60, 30, fc="#eee", ec=INK, lw=THIN))
        ax2.plot([1360, R['stock_x']], [yr, yr], color=INK, lw=0.6)
    ax2.plot([1100, 1250, 1530], [0, 60, 0], color=BLUE, lw=0.4, ls="--")
    ax2.plot([1000, D.MAST_X], [-50, -20], color=BLUE, lw=0.4, ls="--")
    ax2.plot([1200, 1300], [-20, -100], color=BLUE, lw=0.4, ls="--"); ax2.plot([1200, 1300], [20, 100], color=BLUE, lw=0.4, ls="--")
    ax2.text(1260, 160, "servo cables through a\nWetLink in bulkhead 1260", fontsize=4.8, color=BLUE, ha="center")
    ax2.text(700, -70, "cable to slip ring", fontsize=5, color=BLUE)
    ax2.text(430, 0, "hatch\naccess", fontsize=5, ha="center", va="center")
    vf, vm, va = D.inner_volume(0, b0), D.inner_volume(b0, b1), D.inner_volume(b1, D.L)
    notes(bg, 15, 37 + 22, "Systems notes (Rev C)", [
        f"Inside volume: forward {vf:.1f} L (solid foam), dry bay {vm:.1f} L, aft {va:.1f} L (foam except the rudder trunks and servo pockets). XPS blocks at about 28 kg/m3, about 1.6 kg in all.",
        f"Fitted, removable blocks fill the dry bay around the boxes: aim for no more than {D.FREE_FLOOD_L:.0f} L of open space, so a leak can't add more than about 3 kg of water (12% of displacement). See D09.",
        f"Masses (approx, kg): hull + deck 4.5, bulkheads 0.2, foam 1.6, fin 2.1, bulb 9.2, rudders 1.0, servos + trunks 0.5, rig 2.7, battery + box 2.35, electronics 1.1, solar 1.0, post items 1.0, YB3 + cradle 0.4, keel box + floors 0.4, misc 0.4 -> about {D.MASS_KG:.1f} kg.",
        "C3: the hull bottom over the sump (x 560-770) has no foam behind it: give it a second ply of 6 oz inside."], fs=5.8, lh=3.5)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D04 keel
def sheet_keel(pdf):
    fig, bg = new_sheet("D04", "Keel fin, keel box and lead bulb (Rev C2)", "Scale 1:4, sections as noted")
    s = 4
    F = D.FIN; FB = D.FIN_BUILD; KB = D.KEELBOX
    ax = view(fig, 15, 40, (540, 920), (-480, 100), s, "FIN + BULB ELEVATION")
    poly(ax, fin_poly(), lw=MED)
    poly(ax, bulb_profile(), lw=MED, fc="#ccc", fill=True)
    # tenon, keel box, plate, floors
    ax.add_patch(Rectangle((F['root_le_x'], 0), FB['tenon_x1'] - 2 - F['root_le_x'], FB['tenon_h'], fc="#e9d3ae", ec=INK, lw=MED))
    ax.add_patch(Rectangle((KB['x0'], 0), KB['x1'] - KB['x0'], KB['h'], fill=False, lw=THIN, hatch="////"))
    ax.add_patch(Rectangle((KB['x0'], KB['h']), KB['x1'] - KB['x0'], KB['plate_t'], fc="#bbb", ec=INK, lw=THIN))
    for xr in (707, 762):
        ax.plot([xr, xr], [-490 + 50, KB['h'] + KB['plate_t'] + 12], color=INK, lw=0.5, ls="--")
        ax.add_patch(Rectangle((xr - 8.5, KB['h'] + KB['plate_t']), 17, 8, fc=INK))
    for xf, zf in D.FLOORS:
        ax.add_patch(Rectangle((xf - 4.5, float(D.keel_z(xf)) + 3), 9, zf - float(D.keel_z(xf)) - 3, fc="#c9a877", ec=INK, lw=THIN))
    xs = np.linspace(545, 915, 60); ax.plot(xs, D.keel_z(xs), color=INK, lw=MED)
    # carbon strip
    cx0 = F['root_le_x'] + FB['carbon_x0']
    ax.plot([cx0 + FB['carbon_w'] / 2] * 2, [-425, FB['tenon_h']], color="#333", lw=2.2, alpha=0.35)
    dim(ax, (F['root_le_x'], -60), (F['root_le_x'] + F['root_chord'], -60), 0, "170 root chord")
    dim(ax, (F['tip_le_x'], -395), (F['tip_le_x'] + F['tip_chord'], -395), 0, "150 tip chord")
    dim(ax, (890, 0), (890, -430), 0, "430")
    dim(ax, (625, 0), (625, FB['tenon_h']), 0, f"tenon {FB['tenon_h']}")
    dim(ax, (D.BULB['nose_x'], -485 + 10), (D.BULB['nose_x'] + 320, -485 + 10), 0, "bulb 320")
    zb, rb = D.BULB['axis_z'], D.BULB['dia'] / 2
    dim(ax, (D.BULB['nose_x'] + 128, zb - rb), (D.BULB['nose_x'] + 128, zb + rb), 0, f"D{D.BULB['dia']:.0f}")
    dim(ax, (657, 92), (707, 92), 0, "50"); dim(ax, (707, 92), (762, 92), 0, "55")
    leader(ax, (735, -200), (560, -150), "2 x M10 316 threaded rod,\nfull length, bonded between\nthe core halves and in the bulb")
    leader(ax, (cx0 + 30, -300), (850, -300), "carbon strip 60 x 1.5,\neach side, tip to top\nof tenon")
    leader(ax, (800, 25), (850, 60), "floor x 800\n(top z 32)")
    leader(ax, (650, 70), (560, 85), "floor x 650\n(top z 80)")
    leader(ax, (760, 65), (850, 92), "G10 plate 122 x 60 x 10,\n316 nuts + washers")
    # root section
    ax2 = view(fig, 120, 232, (-10, 180), (-15, 15), 1.3, "FIN ROOT SECTION  NACA 0012  (1:1.3)")
    P = foil_xy(0.12, 170); poly(ax2, P, lw=1.6, fc="#e9d3ae", fill=True)
    ax2.plot([0, 170], [0, 0], color=INK, lw=0.5)
    for xr in FB['rods_x']: ax2.add_patch(Circle((xr, 0), 5.5, fc="white", ec=INK, lw=THIN)); ax2.add_patch(Circle((xr, 0), 4.2, fc="#888", ec="none"))
    xq = np.linspace(FB['carbon_x0'], FB['carbon_x0'] + FB['carbon_w'], 30)
    xs_, ys_ = D.naca(0.12, 170, 200); up = ys_ > 0
    yq = np.interp(xq, xs_[up][np.argsort(xs_[up])], ys_[up][np.argsort(xs_[up])])
    for sg in (1, -1):
        ax2.fill_between(xq, sg * (yq - 0.6), sg * (yq - 0.6 - 1.5 * 1.6), color="#222")
    dim(ax2, (0, 15), (50, 15), 0, "50", fs=5); dim(ax2, (50, 15), (105, 15), 0, "55", fs=5)
    leader(ax2, (55, 9.0), (118, 13.5), "carbon strip let into the core, under the glass", fs=5)
    leader(ax2, (140, 0), (150, -12.5), "glue line between the two core halves", fs=5)
    leader(ax2, (20, -6.5), (0, -13.5), "6 x 6 oz glass (about 1.2 mm)", fs=5)
    # transverse section at the keel box
    xsct = 735.0
    ax3 = view(fig, 300, 150, (-150, 150), (-70, 110), 2.5, f"SECTION AT x {xsct:.0f}, LOOKING AFT  (1:2.5)")
    y, z = D.section(xsct, 120); m = z < 108
    outer = np.r_[np.c_[-y[m][::-1], z[m][::-1]], np.c_[y[m][1:], z[m][1:]]]
    ax3.plot(outer[:, 0], outer[:, 1], color=INK, lw=MED)
    yi, zi = np.maximum(y - 11, 0), z + 11; mi = (zi < 108) & (yi > 0)
    ax3.plot(np.r_[-yi[mi][::-1], yi[mi]], np.r_[zi[mi][::-1], zi[mi]], color=INK, lw=THIN)
    zf = D.FLOORS[0][1]; yf, zfv = np.maximum(D.section(D.FLOORS[0][0], 120)[0] - 11, 0), D.section(D.FLOORS[0][0], 120)[1] + 11
    mf = zfv <= zf
    ax3.add_patch(Polygon(np.r_[np.c_[-yf[mf][::-1], zfv[mf][::-1]], np.c_[yf[mf], zfv[mf]], [[yf[mf][-1], zf], [-yf[mf][-1], zf]]], closed=True, fc="#c9a877", ec=INK, lw=THIN, alpha=0.55))
    ax3.add_patch(Rectangle((-KB['w'] / 2, 0), KB['w'], KB['h'], fc="white", ec=INK, lw=MED, hatch="////"))
    ax3.add_patch(Rectangle((-10.2, -70), 20.4, 70 + FB['tenon_h'], fc="#e9d3ae", ec=INK, lw=MED))
    ax3.add_patch(Rectangle((-KB['w'] / 2, KB['h']), KB['w'], KB['plate_t'], fc="#bbb", ec=INK, lw=THIN))
    ax3.plot([0, 0], [-70, KB['h'] + KB['plate_t'] + 14], color=INK, lw=1.0)
    ax3.add_patch(Rectangle((-8.5, KB['h'] + KB['plate_t']), 17, 8, fc=INK))
    zl = float(np.interp(45, yf, zfv)) + 10
    for yl in (-45, 45): ax3.add_patch(Circle((yl, zl), 7.5, fc="white", ec=INK, lw=THIN))
    dim(ax3, (-KB['w'] / 2, 100), (KB['w'] / 2, 100), 0, "60", fs=5)
    dim(ax3, (60, 0), (60, KB['h']), 0, "60", fs=5)
    leader(ax3, (22, 12), (55, -58), "keel box: glass + thickened\nepoxy cast round the tenon", fs=5)
    leader(ax3, (80, 50), (95, 95), "floor at x 650 (beyond),\n9 ply, tabbed to the hull", fs=5)
    leader(ax3, (50, zl - 5), (75, -30), "limber holes D15, 45 off centre", fs=5)
    leader(ax3, (-90, 20), (-140, -30), "hull doubler: 3 extra plies\ninside, floor to floor", fs=5)
    leader(ax3, (-10, -40), (-70, -55), "fin", fs=5)
    xl = np.arange(0, 321, 20)
    rows = [[int(v), f"{float(D.bulb_radius(v))*2:.1f}"] for v in xl]
    table(bg, 255, 222, ["from nose", "diameter"], rows, [20, 18], fs=5.5, rh=3.7)
    v, m = D.bulb_mass()
    notes(bg, 120, 222, "Fin construction (Rev C2)", [
        "1. Core: two planks of straight-grained hardwood (white oak, ash or",
        "   sapele), each 10.5 thick x 175 x 495, grain along the span.",
        "2. Rout two half-round grooves (R5.5) in each plank at 50 and 105 from",
        "   the root LE, parallel to the LE. Glue the planks together round the",
        "   2 x M10 316 rods with thickened epoxy. Rods project 30 above the",
        "   tenon and 60 below the tip.",
        "3. Plane to templates T12 (root) and T13 (tip). The top 60 mm is the",
        "   tenon: keep the root section, cut it back to 113 long (x 657-770).",
        "4. Rout a recess 60 wide x 1.5 deep each side, 25-85 from the LE, full",
        "   length incl. the tenon. Bond in unidirectional carbon (pultruded",
        "   strip, or 5 layers of 300 g tape).",
        "5. Glass 6 x 6 oz each side, layers 2 and 5 at +/-45 deg, wrapped",
        "   round the LE; fair, then 2-part epoxy primer.",
        "", "Keel box, floors and hull",
        "6. Floors: 9 mm marine ply to T19 (x 650) and T20 (x 800), 2 x 6 oz",
        "   each side, tabbed to the hull with 3 x 6 oz, 50 mm each way.",
        "7. Doubler: 3 extra plies of 6 oz inside the hull bottom between the",
        "   floors, out to 120 either side.",
        "8. Keel box: wax the tenon, stand the fin in the hull slot, build 6 plies",
        "   of glass round the tenon and fill out to 60 wide with thickened",
        "   epoxy between the floor at x 650 and a ply end plate at x 772.",
        "9. G10 plate 122 x 60 x 10 on top, 316 nuts + washers, 15 N.m,",
        "   thread-lock. Seal the hull slot with polyurethane.",
        "10. PROOF TEST before paint: Field Test K (60 kg on the bulb).",
        "C4: sand glue faces to 80 grit and wipe twice with alcohol (oak",
        "   especially); glue the core with G/flex. Bed the rods fully in",
        "   epoxy, no voids; seal the end grain at tip and tenon."], fs=5.5, lh=3.1)
    notes(bg, 300, 138, "Why (docs/Keel_Structure_Loads.md)", [
        "The foam-cored fin with 3 x 6 oz was good for about 113 N.m at the root: 3 times the",
        "load of the bulb with the boat on its side (36 N.m). A breaking-wave strike is estimated",
        "at 65 N.m typically and 350 N.m once in 1,000. This fin is estimated at 1,100 N.m and",
        "the tenon joint at about 700 N.m. Both are hand calculations: the proof test decides.",
        "", "Bulb (Rev C: D72, was D68)", f"Volume {v/1e3:.0f} cm3 -> {m:.1f} kg of lead. Make a plaster mould from pattern P14a/b",
        "(printed), cast outdoors with PPE, then drill 2 x 12 mm holes 60 deep at the rod positions",
        "(91 + 37 and 91 + 92 mm from the nose, measured on the slot) and bond the rods in with epoxy.",
        "Fair with epoxy filler; seal with 2 coats epoxy barrier coat."], fs=5.8, lh=3.4)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D05 rudder
def sheet_rudder(pdf):
    fig, bg = new_sheet("D05", "Twin rudders, stocks and steering", "Scale 1:2")
    R = D.RUDDER; s = 2
    le = R['stock_x'] - R['stock_from_le']
    yr = D.RUDDER_Y[1]
    kz = D.hull_z_at(R['stock_x'], yr)
    tt = R['trunk_top_z']
    ax = view(fig, 20, 45, (1340, 1540), (-215, 230), s, "ONE RUDDER, ELEVATION (looking to port; both are the same)")
    poly(ax, rudder_poly(), lw=MED)
    ax.plot([1340, 1540], [kz, kz], color=GREY, lw=0.3, ls="--"); ax.text(1342, kz + 3, "hull surface at y 100", fontsize=5, color=GREY)
    ax.add_patch(Rectangle((R['stock_x'] - 6, R['bot_z'] + 8), 12, 210 - R['bot_z'] - 8, fill=False, lw=THIN))
    ax.add_patch(Rectangle((R['stock_x'] - 9, kz), 18, tt - kz, fill=False, lw=MED, hatch="////"))
    for zb in (kz, tt - 15):
        ax.add_patch(Rectangle((R['stock_x'] - 9, zb), 18, 15, fc="#bbb", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((R['stock_x'] - 12, tt), 24, 5, fc=BLUE, ec=INK, lw=THIN))
    ax.add_patch(Rectangle((R['stock_x'] - 13, 182), 26, 16, fill=False, lw=MED))
    ax.plot([1340, 1540], [D.DWL, D.DWL], color=WATER, lw=0.5)
    dim(ax, (le, R['top_z'] + 12), (le + R['chord'], R['top_z'] + 12), 0, "120 chord")
    dim(ax, (le, -205), (R['stock_x'], -205), 0, "22")
    dim(ax, (1525, R['top_z']), (1525, R['bot_z']), 0, "230 span")
    dim(ax, (1525, kz), (1525, tt), 0, "trunk")
    leader(ax, (R['stock_x'], 120), (1450, 150), "Trunk: GRP or 316 tube, ID 14,\nglassed through the hull and\nfoamed in; top at z 175")
    leader(ax, (R['stock_x'] + 12, tt + 3), (1450, 215), "Top seal: lip seal + rubber boot\n(the trunk top goes under\nin a knockdown)", color=BLUE)
    leader(ax, (R['stock_x'] + 9, kz + 7), (1460, 40), "igus iglide J flange\nbushing 12 x 14 (x2)")
    leader(ax, (R['stock_x'] + 13, 190), (1345, 225), "Tiller arm P11", ha="left")
    leader(ax, (R['stock_x'], -100), (1460, -120), "12 mm 316 stock,\nlength 360")
    # section through both rudders, looking forward
    ax3 = view(fig, 140, 50, (-200, 200), (-200, 260), 2.5, "SECTION AT x 1400, LOOKING FORWARD (1:2.5)")
    y, z = D.section(R['stock_x'])
    ax3.plot(y, z, color=INK, lw=MED); ax3.plot(-y, z, color=INK, lw=MED)
    ax3.plot([-y[-1], y[-1]], [z[-1], z[-1]], color=INK, lw=MED)
    yi = np.maximum(y - 11, 0); zi = z + 11
    ax3.add_patch(Polygon(np.r_[np.c_[-yi[::-1], zi[::-1]], np.c_[yi, zi], [[yi[-1], z[-1] - 11], [-yi[-1], z[-1] - 11]]], closed=True, **FOAM))
    for yy in D.RUDDER_Y:
        zh = D.hull_z_at(R['stock_x'], yy)
        ax3.add_patch(Rectangle((yy - 20, zh), 40, tt + 25 - zh, fc="white", ec="none"))
        ax3.add_patch(Rectangle((yy - 9, zh), 18, tt - zh, fill=False, lw=MED, hatch="////"))
        ax3.add_patch(Rectangle((yy - 7.2, R['bot_z']), 14.4, R['top_z'] - R['bot_z'], fc="#ddd", ec=INK, lw=MED))
        ax3.plot([yy, yy], [R['bot_z'] + 8, 198], color=INK, lw=0.6)
        ax3.add_patch(Rectangle((yy - 13, 182), 26, 16, fill=False, lw=THIN))
    ax3.plot([-200, 200], [D.DWL, D.DWL], color=WATER, lw=0.5)
    ax3.plot([0, 0], [-200, 255], color=GREY, lw=0.25, ls="-.")
    dim(ax3, (D.RUDDER_Y[0], -185), (D.RUDDER_Y[1], -185), 0, "200 between stocks")
    ax3.text(0, 140, "aft foam", fontsize=5, ha="center", color="#8a7a50")
    ax2 = view(fig, 345, 225, (-5, 125), (-12, 12), 1, "BLADE SECTION  NACA 0012  (1:1)")
    poly(ax2, foil_xy(0.12, 120), lw=MED); ax2.add_patch(Circle((22, 0), 6, fill=False, lw=THIN))
    dim(ax2, (0, 11), (22, 11), 0, "22", fs=5)
    notes(bg, 340, 205, "Build (make two of everything)", [
        "1. Print cores P13a/b (two sets), slide on each stock,",
        "   pin with 4 mm 316 pins, epoxy the joints.",
        "2. Glass 2 x 6 oz over each blade, wrapping the tip;",
        "   fair to template T14.",
        "3. Balanced: about 15% of the area is ahead of the",
        "   stock, so each servo needs little holding torque.",
        "4. Stocks: 12 mm 316 round bar, 360 long; 3 mm",
        "   cross-hole for each tiller pin.",
        "5. Trunk bottoms flush with the hull; glass a 40 mm",
        "   fillet pad where each meets the curved bottom.",
        "6. Each rudder has its own servo (P12), tiller (P11)",
        "   and cable. Either one alone can steer the boat.",
        "7. ArduPilot: two outputs set to GroundSteering.",
        "8. C3: a breaking wave can force a blade over with",
        "   4 x the servo's stall torque. Fit a spring servo-",
        "   saver (1/8-scale RC car type, 25T) on each servo,",
        "   and bond two G10 stop blocks beside each tiller",
        "   so it cannot pass +/-40 deg.",
        "9. C4: 316 corrodes in trapped, still sea water. Pack",
        "   each trunk with waterproof grease; pull and inspect",
        "   the stocks for pitting after the shakedown test.",
        "   If one servo jams, the mission manager trims the",
        "   other to compensate; if one goes limp it trails.",
        "8. Stop each rudder at +/-35 deg with the servo end",
        "   points. Check both blades clear the bulb's wake."], fs=5.8, lh=3.5)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D06 wing & tail
def sheet_wing(pdf):
    fig, bg = new_sheet("D06", "Wing sail and tail", "Elevation 1:6, plan 1:6, section 1:2")
    W = D.WING; T = D.TAIL; B = D.BOOM
    le, te, z0, z1 = wing_rect()
    ax = view(fig, 15, 45, (240, 1350), (230, 1340), 6, "WING, TAIL + COUNTERWEIGHT ELEVATION")
    ax.add_patch(Rectangle((le, z0), W['chord'], W['span'], fill=False, lw=MED))
    ax.plot([le, te], [z0 + W['span'] / 2] * 2, color=GREY, lw=0.4, ls="--"); ax.text(te + 5, z0 + W['span'] / 2, "core joint", fontsize=5, va="center")
    ax.plot([D.MAST_X] * 2, [240, z1 - 10], color=INK, lw=0.8, ls="-.")
    C = D.CWARM; px = D.MAST_X - C['reach']
    ax.plot([px, D.MAST_X], [C['z']] * 2, color=INK, lw=1.2)
    ax.add_patch(Rectangle((px - C['pod_od']/2, C['pod_bot_z']), C['pod_od'], C['pod_h'], fc="#bbb", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((px - C['pod_od']/2 + 4, C['pod_bot_z'] + 3), C['pod_od'] - 8, 46, fc="#666", ec="none"))
    tp = D.MAST_X + B['length']
    ax.plot([D.MAST_X, tp], [B['z']] * 2, color=INK, lw=1.2)
    ax.add_patch(Rectangle((D.MAST_X - 63, 265), 126, 40, fill=False, lw=THIN))
    ax.add_patch(Rectangle((tp - 28, 252), 92, 48, fill=False, lw=THIN))
    ax.add_patch(Rectangle((tp - T['pivot_from_le'], T['bot_z']), T['chord'], T['span'], fill=False, lw=MED))
    ax.plot([tp, tp], [T['bot_z'], T['bot_z'] + T['span']], color=INK, lw=0.4, ls="-.")
    dim(ax, (le, z1 + 20), (te, z1 + 20), 0, f"{D.WING['chord']}")
    dim(ax, (le, z1 + 45), (D.MAST_X, z1 + 45), 0, f"{D.WING['pivot_from_le']}")
    dim(ax, (430 + 40, z0), (430 + 40, z1), 0, f"{W['span']}")
    dim(ax, (D.MAST_X, 245), (tp, 245), 0, "boom 600 (spar to tail pivot)")
    dim(ax, (px, 245), (D.MAST_X, 245), 0, "300 (spar to pod axis)")
    dim(ax, (tp + 110, T['bot_z']), (tp + 110, T['bot_z'] + T['span']), 0, "200")
    leader(ax, (px, C['pod_bot_z'] + C['pod_h']), (330, 470), "Counterweight pod P18\nabout 0.8 kg lead shot + epoxy\non a 12 mm solid fibreglass\nrod, 246 long (C3)")
    leader(ax, (D.MAST_X, 276), (700, 330), "Spar clamp P08")
    leader(ax, (tp + 10, 276), (1000, 380), "Tail servo housing P09")
    leader(ax, (tp + 40, 420), (1050, 600), "Tail fin P10a/b\nNACA 0012, 120 chord")
    ax2 = view(fig, 200, 160, (-10, 395), (-34, 40), 2, "WING SECTION  NACA 0015  (1:2)")
    poly(ax2, foil_xy(0.15, W['chord']), lw=MED)
    ax2.add_patch(Circle((D.WING['pivot_from_le'], 0), D.SPAR_OD / 2 + 0.2, fill=False, lw=MED))
    dim(ax2, (0, 34), (D.WING['pivot_from_le'], 34), 0, f"{D.WING['pivot_from_le']}", fs=5); dim(ax2, (D.WING['pivot_from_le'], 34), (D.WING['chord'], 34), 0, f"{D.WING['chord'] - D.WING['pivot_from_le']}", fs=5)
    ax3 = view(fig, 200, 62, (-750, 360), (-60, 100), 6, "PLAN OF ROTATING RIG (1:6)")
    poly(ax3, np.c_[-(foil_xy(0.15, D.WING['chord'])[:, 0] - D.WING['pivot_from_le']), foil_xy(0.15, D.WING['chord'])[:, 1]], lw=MED)
    ax3.plot([0, -600], [0, 0], color=INK, lw=1)
    P = foil_xy(0.12, 120); poly(ax3, np.c_[-(P[:, 0] - 24) - 600, P[:, 1]], lw=MED)
    ax3.add_patch(Circle((0, 0), 12.5, fill=False, lw=MED))
    ax3.plot([0, 300], [0, 0], color=INK, lw=1); ax3.add_patch(Circle((300, 0), 32, fc="#bbb", ec=INK, lw=THIN))
    ax3.text(300, -50, "pod", fontsize=5.5, ha="center")
    ax3.annotate("", xy=(-120, 70), xytext=(130, 70), arrowprops=dict(arrowstyle="-|>", lw=0.6))
    ax3.text(5, 80, "apparent wind", fontsize=5.5, ha="center")
    ax3.text(-600, -40, "tail", fontsize=5.5, ha="center"); ax3.text(-80, -40, "wing", fontsize=5.5, ha="center")
    notes(bg, 200, 140, "Wing build", [
        "Core: two 400 mm XPS blocks hot-wire cut with template T15 (same root and tip), bored 30.4 mm for the spar (Rev C).",
        "Skin: 2 x 6 oz glass, vacuum bagged if possible. Root and tip: 3 mm ply caps. Spar: 30 x 22 carbon tube, 995 long.",
        "Rev C5: wing 800 x 375 (was 1000 x 300), same 0.30 m2, spar 82 from the leading edge: about half the load when a knockdown slaps the wing on the water, 4% slower.",
        "Balance: assemble wing, tail, boom, arm and pod; add lead shot + epoxy to P18 until the rig sits level on the spar at any heading.",
        "Expect about 0.85 kg (C5). The pod sweeps a 332 mm radius at z 264-338, about 15 mm over the hatch bolts: keep anything on deck in that circle below z 255.",
        "Tail angle sets the wing's angle of attack: about +/-8 deg tail gives the working range; 0 deg = wing feathered."], fs=5.9, lh=3.5)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D07 mast, stub
def sheet_mast(pdf):
    fig, bg = new_sheet("D07", "Mast step, spar and stern stub", "Scale 1:2 and 1:5")
    MT = D.MAST_TUBE
    ax = view(fig, 15, 45, (520, 680), (-10, 420), 2, "MAST STEP SECTION (1:2)")
    kz = float(D.keel_z(D.MAST_X))
    for sx in (-1, 1):
        ax.add_patch(Rectangle((D.MAST_X + sx * MT['id']/2 - (0 if sx > 0 else (MT['od'] - MT['id'])/2), kz),
                               (MT['od'] - MT['id'])/2, MT['top_z'] - kz, fc="#ddd", ec=INK, lw=THIN))
    HL = D.BEARING_SPACING + 2
    ax.add_patch(Rectangle((D.MAST_X - 26.15, MT['top_z'] - HL), 52.3, HL, fill=False, lw=MED, hatch="////"))
    ax.add_patch(Rectangle((D.MAST_X - 33, MT['top_z']), 66, 5, fill=False, lw=MED, hatch="////"))
    Bg = D.BEARING
    for zb in (MT['top_z'] - 2, MT['top_z'] - 2 - D.BEARING_SPACING):
        ax.add_patch(Rectangle((D.MAST_X - Bg['od']/2, zb), Bg['od'], 7, fc="#999", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((D.MAST_X - D.SPAR_OD/2, D.SPAR_BOT_Z), D.SPAR_OD, 420 - D.SPAR_BOT_Z, fill=False, lw=MED))
    ax.add_patch(Rectangle((D.MAST_X - 7, D.SPAR_BOT_Z - 35), 14, 35, fc="#ccc", ec=INK, lw=THIN))
    ax.plot([520, 680], [D.DECK_Z, D.DECK_Z], color=GREY, lw=0.4, ls="--"); ax.text(522, D.DECK_Z + 3, "deck", fontsize=5)
    ax.plot([520, 680], [kz, kz], color=GREY, lw=0.4, ls="--"); ax.text(522, kz + 3, "hull bottom", fontsize=5)
    dim(ax, (670, MT['top_z'] - HL), (670, MT['top_z'] + 5), 0, f"{HL + 5:.0f}")
    dim(ax, (540, MT['top_z'] + 1.5 - D.BEARING_SPACING), (540, MT['top_z'] + 1.5), 0, f"{D.BEARING_SPACING:.0f}")
    dim(ax, (D.MAST_X - 30.15, 40), (D.MAST_X + 30.15, 40), 0, "OD 60.3")
    for zb in (MT['top_z'] - 2 - 20, MT['top_z'] - 2 - D.BEARING_SPACING + 7):
        for sx in (-1, 1):
            ax.add_patch(Rectangle((D.MAST_X + sx * 15.3 - (0 if sx > 0 else 4), zb), 4, 20, fc="#e9d3ae", ec=INK, lw=THIN))
    ax.add_patch(Polygon([[D.MAST_X - 15, MT['top_z'] + 5], [D.MAST_X - 24, MT['top_z'] + 5], [D.MAST_X - 15, MT['top_z'] + 13]], closed=True, fc=INK))
    ax.add_patch(Polygon([[D.MAST_X + 15, MT['top_z'] + 5], [D.MAST_X + 24, MT['top_z'] + 5], [D.MAST_X + 15, MT['top_z'] + 13]], closed=True, fc=INK))
    leader(ax, (D.MAST_X + 20, MT['top_z'] + 2), (640, 345), "C4: 6806 acetal ball bearings,\nglass balls (x2), each floating\non a 42 x 1.5 O-ring")
    leader(ax, (D.MAST_X + 17, MT['top_z'] - 14), (640, 262), "C4: catcher land D30.6 x 20\n(spar touches above ~150 N)")
    leader(ax, (D.MAST_X + 22, MT['top_z'] + 8), (640, 395), "C4: V-ring seal VA-30 on the spar")
    leader(ax, (D.MAST_X + 15, 300), (640, 300), "Spar 30 x 22 carbon (C3)")
    leader(ax, (D.MAST_X + 7, D.SPAR_BOT_Z - 15), (640, 80), "Slip ring, 12.5 mm,\n6 wire, in spar end")
    leader(ax, (D.MAST_X + 26, 200), (640, 200), "Bearing housing P07")
    ax.text(D.MAST_X, 405, "wing root z 300 above", fontsize=5, ha="center")
    S = D.STUB
    ax2 = view(fig, 160, 45, (1480, 1700), (100, 760), 5, "STERN STUB (1:5)")
    ax2.add_patch(Rectangle((S['x'] - 10, S['bot_z']), 20, S['top_z'] - S['bot_z'], fill=False, lw=MED))
    ax2.plot([D.L, D.L], [60, 230], color=INK, lw=MED); ax2.text(D.L - 4, 120, "transom", rotation=90, fontsize=5, ha="right")
    ax2.add_patch(Rectangle((D.L, 160), 6, 100, fc="#ddd", ec=INK, lw=THIN))
    for zb in (160, 240):
        ax2.add_patch(Rectangle((D.L, zb), 44, 20, fill=False, lw=THIN, hatch="////"))
    ax2.add_patch(Rectangle((S['x'] - 14, D.ANT_Z - 25), 28, 25, fill=False, lw=THIN))
    ax2.add_patch(Rectangle((S['x'] + 10, D.ANT_Z - 5), 80, 5, fc=INK))
    ax2.add_patch(Rectangle((S['x'] + 30, D.ANT_Z), 40, 12, fc="#bbb", ec=INK, lw=THIN))
    ax2.add_patch(Rectangle((S['x'] - 20, D.VANE_Z - 30), 40, 30, fill=False, lw=THIN))
    ax2.add_patch(Rectangle((S['x'] - 20, D.VANE_Z), 40, 60, fill=False, lw=MED))
    ax2.add_patch(Rectangle((S['x'] - 23, D.VANE_Z + 60), 46, 22, fill=False, lw=THIN))
    ax2.plot([S['x'] - 75, S['x'] + 190], [D.VANE_Z + 82 - 4] * 2, color=INK, lw=MED)
    ax2.add_patch(Rectangle((S['x'] + 120, D.VANE_Z + 82 - 80), 80, 80, fill=False, lw=THIN))
    ax2.add_patch(Polygon([[S['x'], 330], [S['x'] + 70, 400], [S['x'], 470], [S['x'] - 70, 400]], fill=False, lw=THIN))
    dim(ax2, (1690, S['bot_z']), (1690, S['top_z']), 0, "stub 500")
    leader(ax2, (D.L + 22, 170), (1600, 150), "Transom bracket P06")
    leader(ax2, (S['x'] + 50, D.ANT_Z + 6), (1620, 520), "Iridium patch on P05")
    leader(ax2, (S['x'], D.VANE_Z - 15), (1600, 600), "Sensor cap P03")
    leader(ax2, (S['x'] + 20, D.VANE_Z + 30), (1630, 690), "Housing P01, arm P02")
    leader(ax2, (S['x'] + 50, 400), (1610, 380), "Davis 151 radar reflector")
    Y = D.YB3; NL = D.NAVLIGHT
    ax2.add_patch(Rectangle((S['x'] - 16, NL['z']), 32 + NL['reach'], 9, fill=False, lw=THIN))
    ax2.add_patch(Rectangle((S['x'] + NL['reach'] - 15, NL['z'] + 9), 30, 10, fc="white", ec=INK, lw=THIN))
    leader(ax2, (S['x'] + NL['reach'], NL['z'] + 15), (1610, 630), "All-round white light on P20")
    notes(bg, 260, 250, "Notes", [
        f"Spar: 30 x 22 carbon tube, {D.WING_TOP_Z - D.SPAR_BOT_Z:.0f} long (z {D.SPAR_BOT_Z:.0f} to {D.WING_TOP_Z}). Rev C3:",
        "1.6 x the strength of 30 x 26. Bearings 130 apart in the",
        "longer housing P07; give the mast tube a 60 mm wide glass",
        "collar where it meets the deck.",
        "C4 bearings: acetal rings and glass balls cannot rust or",
        "seize (stainless ones do, in still salt water) but carry only",
        "about 170 N. Each floats 0.3 in its seat on an O-ring; in a",
        "wave strike (several kN) the spar bears on the two plain",
        "lands. Grease the lands. A Delrin thrust collar clamped on",
        "the spar rests on the upper bearing and carries the rig.",
        "No drain in the mast tube: the slip ring sits at its foot.",
        "Slip ring in the spar's lower end carries 3 wires to the",
        "tail servo; it must turn freely through 360 deg.",
        "Lock the spar against lifting with a 316 collar under",
        "the lower bearing.",
        "",
        "Post (C3): 20 mm OD x 2 wall pultruded fibreglass tube,",
        "500 long (not aluminium or carbon: it must bend, not",
        "kink, when a wave jolts the boat); cables run inside it to the",
        "vane cap and down through a WetLink in the transom.",
        "Vane shaft: 8 mm 316, 75 long, 2 x S608-2RS bearings.",
        "",
        "On the post, bottom to top: radar reflector (z 330-470),",
        "Iridium patch P05 (z 560), light P20 (z 600), vane (z 650).",
        "",
        "YB3 (C3): in a glassed well in the foredeck, 176 x 106 x 38",
        f"deep, centred at x {D.YB3['x']:.0f}, cut into the solid bow foam, with a",
        "10 mm scupper slot to each deck edge. Cradle P19 on the",
        "well floor; the YB3's top is flush with the deck, 25 mm under",
        "the tail boom. It has its own battery and antenna: no cables."], fs=5.8, lh=3.4)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D08 deck & hatch
def sheet_deck(pdf):
    fig, bg = new_sheet("D08", "Deck hatch, solar layout and penetrations", "Hatch 1:2, deck 1:7.5")
    H = D.HATCH
    w, l, m = H['w'], H['x1'] - H['x0'], H['lid_margin']
    ax = view(fig, 15, 60, (-170, 170), (-160, 160), 2, "HATCH LID AND OPENING (1:2)")
    ax.add_patch(Rectangle((-l/2 - m, -w/2 - m), l + 2*m, w + 2*m, fill=False, lw=MED))
    ax.add_patch(Rectangle((-l/2, -w/2), l, w, fill=False, lw=MED, ls="--"))
    ax.add_patch(Rectangle((-l/2 - 12, -w/2 - 12), l + 24, w + 24, fill=False, lw=0.6, ec=BLUE))
    pts = hatch_bolts()
    for (x, y) in pts:
        ax.add_patch(Circle((x, y), 2.75, fill=False, lw=THIN))
    dim(ax, (-l/2 - m, w/2 + m + 10), (l/2 + m, w/2 + m + 10), 0, f"lid {l + 2*m:.0f}")
    dim(ax, (l/2 + m + 10, -w/2 - m), (l/2 + m + 10, w/2 + m), 0, f"{w + 2*m:.0f}")
    dim(ax, (-l/2, -w/2 - m - 10), (l/2, -w/2 - m - 10), 0, f"opening {l:.0f}")
    dim(ax, (-l/2 - m - 10, -w/2), (-l/2 - m - 10, w/2), 0, f"{w:.0f}")
    ax.text(0, 0, "lid: 4 mm G10 or\n3 x 6 oz glass over\n6 mm foam", fontsize=5.5, ha="center", va="center")
    leader(ax, (l/2 + 12, 0), (150, 60), "O-ring cord 4 mm EPDM\nin a 3 mm deep printed\nor routed groove", color=BLUE)
    notes(bg, 200, 250, "Hatch", [
        "12 x M5 316 bolts into bonded-in M5 inserts (or nuts glassed on a doubler).",
        "Doubler under the deck: 30 mm wide frame of 6 mm foam + 2 x 6 oz glass.",
        "Torque evenly; grease the O-ring with silicone grease; tape the seam for the crossing.",
        "Template T16 gives the opening, bolt holes and lid outline at 1:1."], fs=6.0, lh=3.6)
    ax2 = view(fig, 200, 110, (-20, 1560), (-220, 220), 7.5, "DECK PENETRATIONS (P17 pads + WetLink)")
    poly(ax2, hull_plan(), lw=MED)
    for P in D.SOLAR:
        ax2.add_patch(Rectangle((P['x0'], -P['w']/2), P['x1'] - P['x0'], P['w'], fc="#cfe0f3", ec=BLUE, lw=THIN))
    ax2.add_patch(Rectangle((H['x0'], -H['w']/2), l, w, fill=False, lw=THIN, ls="--"))
    ax2.add_patch(Circle((D.MAST_X, 0), 30, fill=False, lw=THIN))
    for (x, y, t) in [(660, -150, "solar 1"), (1090, -150, "solar 2"), (1490, 60, "transom: stub cable")]:
        ax2.add_patch(Circle((x, y), 6, fc=INK)); ax2.text(x + 12, y, t, fontsize=5, va="center")
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D09 subdivision, foam fill, labels (Rev C)
def bulkhead_outline(x, skin=11.0):
    y, z = D.section(x, 120)
    yi = np.maximum(y - skin, 0); zi = z + skin
    top = float(D.deck_z(x)) - skin
    m = zi <= top
    yi, zi = yi[m], zi[m]
    return np.r_[np.c_[-yi[::-1], zi[::-1]], np.c_[yi, zi], [[yi[-1], top], [-yi[-1], top]]]

def sheet_subdivision(pdf):
    fig, bg = new_sheet("D09", "Watertight subdivision, foam fill, battery box, labels", "Bulkheads 1:4, plan 1:7.5, labels 1:9")
    b0, b1 = D.BULKHEADS
    for k, (xb, tname, x0) in enumerate(((b0, "T17", 15), (b1, "T18", 120))):
        ax = view(fig, x0, 188, (-200, 200), (-10, 280), 4, f"BULKHEAD x {xb:.0f}  ({tname}, 1:4)")
        P = bulkhead_outline(xb)
        ax.add_patch(Polygon(P, closed=True, fc="#eef3f8", ec=INK, lw=MED))
        y, z = D.section(xb)
        ax.plot(y, z, color=GREY, lw=0.3, ls="--"); ax.plot(-y, z, color=GREY, lw=0.3, ls="--")
        ax.plot([-200, 200], [D.DWL, D.DWL], color=WATER, lw=0.4)
        w = P[:, 0].max() - P[:, 0].min(); h = P[:, 1].max() - P[:, 1].min()
        dim(ax, (P[:, 0].min(), P[:, 1].max() + 8), (P[:, 0].max(), P[:, 1].max() + 8), 0, f"{w:.0f}")
        dim(ax, (185, P[:, 1].min()), (185, P[:, 1].max()), 0, f"{h:.0f}")
        if xb == b1:
            for yy in (-60, 60):
                ax.add_patch(Circle((yy, 160), 5.25, fill=False, lw=THIN))
            ax.text(0, 185, "2 x WetLink M10\n(servo cables)", fontsize=4.5, ha="center")
    notes(bg, 228, 268, "Bulkheads", [
        "10 mm H80 foam, 2 x 6 oz glass each side. Cut on the solid line (hull inside, 11 mm in from the outside).",
        "Fit after the hull is off the mould, before the deck goes on. Glass in with 50 mm tapes both sides,",
        "on a thickened-epoxy fillet. They make three spaces: forward (solid foam), dry bay, aft (trunks and servos).",
        "No hatches or cables through bulkhead x 300. Bulkhead x 1260 carries the two servo cables in WetLinks.",
        "",
        "Leak test, each space: 0.1 bar of air through a temporary fitting with soapy water on every joint and",
        "penetration, then a 72-hour submersion of the finished hull before Field Test F (Failure_Rates.md, section 5)."], fs=5.9, lh=3.4)
    vf, vm, va = D.inner_volume(0, b0), D.inner_volume(b0, b1), D.inner_volume(b1, D.L)
    BB = D.BATTBOX; E = D.EBOX
    vbb = (BB['x1'] - BB['x0']) * BB['w'] * (BB['z1'] - BB['z0']) / 1e6
    veb = (E['x1'] - E['x0'] + 16) * (E['w'] + 16) * (E['h'] + 16) / 1e6
    other = 0.6 + 0.5 + 1.0
    foam_mid = vm - vbb - veb - other - D.FREE_FLOOD_L
    rows = [["Forward  0-300", f"{vf:.1f}", "nothing", f"{vf:.1f}", "0"],
            ["Dry bay  300-1260", f"{vm:.1f}", f"battery box {vbb:.1f}, IP68 box {veb:.1f}, mast tube, keel box, cable runs {other:.1f}", f"{foam_mid:.1f}", f"<= {D.FREE_FLOOD_L:.0f}"],
            ["Aft  1260-1500", f"{va:.1f}", "2 trunks, 2 servo pockets about 1.5", f"{va - 1.5:.1f}", "<= 0.5"]]
    tot_foam = vf + foam_mid + va - 1.5
    yb = table(bg, 228, 236, ["Space (x)", "Inside L", "Kept dry for", "Foam L", "Free L"], rows, [30, 15, 107, 15, 15], fs=5.4, rh=4.2)
    notes(bg, 228, yb - 3, "Foam fill", [
        f"About {tot_foam:.0f} L of extruded polystyrene (XPS, 25-30 kg/m3, closed cell), about {tot_foam * 28e-3:.1f} kg.",
        "Forward space: blocks bonded in solid with expanding PU adhesive before the deck goes on.",
        "Aft space: blocks bonded around the trunks; leave fitted pockets for the two servos (lids of foam, taped).",
        "Dry bay: numbered, removable blocks cut to fit around the boxes, taped together; they come out through the",
        f"hatch for maintenance. Fill until no more than {D.FREE_FLOOD_L:.0f} L of open space is left (pour water in to check, then dry).",
        "Why: a leak can then add at most about 3 kg of water (12% of displacement) and can't swamp the boat.",
        "C1: leave the open space as one sump at the low point (x 560-770, below z 45). Everything above it is foam, so the water",
        "stays 70 mm below the electronics shelf upright and at 30 deg of heel. Test J in Field_Tests.md checks this."], fs=5.8, lh=3.4)
    ax2 = view(fig, 15, 60, (-20, 1560), (-220, 220), 7.5, "DRY-BAY BLOCK LAYOUT (plan at z 120; numbers = removal order through the hatch)")
    poly(ax2, hull_plan(), lw=MED, ec=GREY)
    for x0, x1 in ((0, b0), (b0, b1), (b1, D.L)):
        ax2.add_patch(Polygon(inner_plan(x0, x1), closed=True, **FOAM))
    for (x0, y0, w, h) in [(BB['x0'], -BB['w']/2, BB['x1'] - BB['x0'], BB['w']), (E['x0'] - 8, -E['w']/2 - 8, E['x1'] - E['x0'] + 16, E['w'] + 16),
                           (650, -30, 190, 60)]:
        ax2.add_patch(Rectangle((x0, y0), w, h, fc="white", ec=INK, lw=THIN))
    ax2.add_patch(Circle((D.MAST_X, 0), D.MAST_TUBE['od']/2, fc="white", ec=INK, lw=THIN))
    for xb in D.BULKHEADS:
        hb = float(D.half_beam(xb)) - 11; ax2.plot([xb, xb], [-hb, hb], color=INK, lw=1.4)
    cuts = [330, 530, 650, 774, 966, 1230]
    for xc in cuts[1:-1]:
        hb = float(D.half_beam(xc)) - 11
        ax2.plot([xc, xc], [-hb, hb], color="#8a7a50", lw=0.4, ls="--")
    for n, xc in enumerate([(cuts[k] + cuts[k + 1]) / 2 for k in range(len(cuts) - 1)]):
        for sy in (-1, 1):
            ax2.text(xc, sy * 120, f"{2*n + (1 if sy < 0 else 2)}", fontsize=5.5, ha="center", va="center", color="#6b5a30")
    ax2.add_patch(Rectangle((D.HATCH['x0'], -D.HATCH['w']/2), D.HATCH['x1'] - D.HATCH['x0'], D.HATCH['w'], fill=False, lw=THIN, ls="--"))
    ax2.text(430, 0, "hatch", fontsize=5, ha="center", va="center")
    ax2.text(870, 0, "battery\nbox", fontsize=5, ha="center", va="center"); ax2.text(1100, 0, "IP68 box", fontsize=5, ha="center", va="center")
    # labels
    ax3 = view(fig, 240, 75, (-20, 1560), (-20, 300), 9, "LABEL AREAS (each side of the hull, both faces of the wing; 1:9)")
    poly(ax3, hull_profile(), lw=MED)
    ax3.add_patch(Rectangle((360, 140), 760, 70, fc="#ffe2c4", ec="#d26a1b", lw=THIN))
    ax3.text(740, 175, "RESEARCH VESSEL - UNMANNED - NOT ADRIFT\nPLEASE DO NOT REMOVE   REWARD FOR REPORT\n+ phone / email, FR / ES / GA lines", fontsize=4.6, ha="center", va="center")
    ax3.plot([0, 1500], [D.DWL, D.DWL], color=WATER, lw=0.4)
    notes(bg, 240, 62, "Labels and colour", [
        "Fluorescent orange deck, wing panels and label areas. Text black, 25 mm capitals; vinyl, sealed under clear epoxy.",
        "Wing: same text on both faces, lower half, so it reads with the boat heeled. Wording: Launch_Plan.md."], fs=5.8, lh=3.4)
    pdf.savefig(fig); plt.close(fig)

def hatch_bolts():
    H = D.HATCH; w, l = H['w'], H['x1'] - H['x0']; o = 18
    xs = np.linspace(-l/2 - o, l/2 + o, 4); ys = np.linspace(-w/2 - o, w/2 + o, 4)
    pts = [(x, -w/2 - o) for x in xs] + [(x, w/2 + o) for x in xs] + [(-l/2 - o, y) for y in ys[1:-1]] + [(l/2 + o, y) for y in ys[1:-1]]
    return pts

# ------------------------------------------------------------------ printed-part sheets
def load_part(stem):
    z = np.load(f"{OUT}/cache/{stem}.npz")
    return z['xs'], z['ys'], z['zs'], z['vol']

def read_stl(path):
    with open(path, "rb") as fh:
        fh.read(80); n = np.frombuffer(fh.read(4), "<u4")[0]
        data = np.frombuffer(fh.read(n * 50), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    return data["v"], data["n"]

def draw_part(fig, bg, stem, pid, x0, y0, w, h):
    P = Pm.PARTS[pid]
    xs, ys, zs, vol = load_part(stem)
    ext = [xs[-1] - xs[0], ys[-1] - ys[0], zs[-1] - zs[0]]
    ex, ey, ez = ext
    avail_w, avail_h = w - 4, h - 14 - 108
    for s in (0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5):
        if (ex + ey) / s + 12 <= avail_w and (ez + ey) / s + 6 <= h - 124:
            break
    title = f"{pid}  {P['name']}" + (f"   (qty {P['qty']})" if P['qty'] > 1 else "")
    if stem[3:4] in "ab" and stem[3] != "_":
        title += f"   [{stem.split('_',1)[1].replace('_',' ')}]"
    bg.text(x0, y0 + h - 2, title, fontsize=7.2, weight="bold", va="top")
    bg.text(x0, y0 + h - 7, f"File: stl/{stem}.stl     Views at 1:{s:g}     Print orientation: z up from the bed", fontsize=5.5, va="top", color=GREY)
    top = y0 + h - 14
    # front section y=0 (x-z)
    jy = np.argmin(np.abs(ys - 0)); sec = vol[:, jy, :].T
    fx, fy = x0 + 2, top - ez / s
    ax = view(fig, fx, fy, (xs[0], xs[-1]), (zs[0], zs[-1]), s)
    ax.contourf(xs, zs, sec.astype(float), levels=[0.5, 1.5], colors=["#c9d6e6"])
    ax.contour(xs, zs, sec.astype(float), levels=[0.5], colors=[INK], linewidths=0.5)
    ax.contour(xs, zs, vol.any(1).T.astype(float), levels=[0.5], colors=[GREY], linewidths=0.3, linestyles="--")
    ax.text(0.0, 1.02, "SECTION y = 0 (front)", transform=ax.transAxes, fontsize=5, va="bottom")
    # side (y-z)
    sx0 = fx + ex / s + 10
    ax2 = view(fig, sx0, fy, (ys[0], ys[-1]), (zs[0], zs[-1]), s)
    ax2.contour(ys, zs, vol.any(0).T.astype(float), levels=[0.5], colors=[INK], linewidths=0.5)
    jx = np.argmin(np.abs(xs - (0 if xs[0] < 0 < xs[-1] else (xs[0] + xs[-1]) / 2)))
    ax2.contour(ys, zs, vol[jx].T.astype(float), levels=[0.5], colors=[BLUE], linewidths=0.3)
    ax2.text(0.0, 1.02, "SIDE", transform=ax2.transAxes, fontsize=5, va="bottom")
    # top (x-y)
    ty = fy - 6 - ey / s
    ax3 = view(fig, fx, ty, (xs[0], xs[-1]), (ys[0], ys[-1]), s)
    ax3.contour(xs, ys, vol.any(2).T.astype(float), levels=[0.5], colors=[INK], linewidths=0.5)
    kz = np.argmin(np.abs(zs - (zs[0] + zs[-1]) / 2 * 0 - min(2.0, zs[-1] / 2)))
    ax3.contour(xs, ys, vol[:, :, kz].T.astype(float), levels=[0.5], colors=[BLUE], linewidths=0.3)
    ax3.text(0.0, -0.04, "TOP (blue: slice near the bed)", transform=ax3.transAxes, fontsize=5, va="top")
    # overall dims
    pad = 3
    xs_in = np.nonzero(vol.any((1, 2)))[0]; ys_in = np.nonzero(vol.any((0, 2)))[0]; zs_in = np.nonzero(vol.any((0, 1)))[0]
    X0, X1 = xs[xs_in[0]], xs[xs_in[-1]]; Y0, Y1 = ys[ys_in[0]], ys[ys_in[-1]]; Z0, Z1 = zs[zs_in[0]], zs[zs_in[-1]]
    tri, nrm = read_stl(f"{OUT}/stl/{stem}.stl")
    allv = tri.reshape(-1, 3); X0, Y0, Z0 = allv.min(0); X1, Y1, Z1 = allv.max(0)
    fs = 5
    bg.text(fx + (ex / s) / 2, fy - 1.5, f"{X1 - X0:.1f}", fontsize=fs, ha="center", va="top", color=BLUE)
    bg.text(fx - 1.5, fy + (ez / s) / 2, f"{Z1 - Z0:.1f}", fontsize=fs, ha="right", va="center", color=BLUE, rotation=90)
    bg.text(sx0 + (ey / s) / 2, fy - 1.5, f"{Y1 - Y0:.1f}", fontsize=fs, ha="center", va="top", color=BLUE)
    # iso
    ia = fig.add_axes([(x0 + w - 72) / SHEET_W, (y0 + 30) / SHEET_H, 70 / SHEET_W, 66 / SHEET_H], projection="3d")
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(nrm @ light, 0, 1)
    cols = np.c_[0.55 * shade + 0.15, 0.65 * shade + 0.15, 0.80 * shade + 0.15, np.ones(len(shade))]
    pc = Poly3DCollection(tri, facecolors=np.clip(cols, 0, 1), edgecolors="none", linewidths=0)
    ia.add_collection3d(pc)
    c = (tri.reshape(-1, 3).max(0) + tri.reshape(-1, 3).min(0)) / 2; r = (tri.reshape(-1, 3).max(0) - tri.reshape(-1, 3).min(0)).max() / 2
    ia.set_xlim(c[0] - r, c[0] + r); ia.set_ylim(c[1] - r, c[1] + r); ia.set_zlim(c[2] - r, c[2] + r)
    ia.view_init(elev=28, azim=-55); ia.set_box_aspect((1, 1, 1)); ia.axis("off")
    # dims table + notes
    rows = [[k, v] for k, v in P['dims'].items()]
    yb = table(bg, x0, y0 + 104, ["Feature", "Size"], rows, [34, 48], fs=5.4, rh=3.7)
    bg.text(x0, yb - 2.5, f"Material: {P['mat']}", fontsize=5.6, va="top", weight="bold")
    yy = yb - 8
    for ln in P['notes']:
        bg.text(x0, yy, "- " + ln, fontsize=5.4, va="top", wrap=True)
        yy -= 3.4
    return s

def sheet_parts(pdf, blocks, num):
    fig, bg = new_sheet(num, "3D-printed parts", "Views to scale as noted per part")
    for i, (stem, pid) in enumerate(blocks):
        x0 = 15 + i * 205
        h = 228
        draw_part(fig, bg, stem, pid, x0, 42, 198, h)
        if i == 0:
            bg.plot([218, 218], [42, 268], color=GREY, lw=0.3)
    pdf.savefig(fig); plt.close(fig)

def main():
    printed = [(stem, pid) for stem, pid, kw in Pm.BUILD if not stem.endswith("b_tail_fin_upper") and stem not in
               ("P13b_rudder_core_lower", "P14b_bulb_pattern_aft")]
    pairs = [printed[i:i+2] for i in range(0, len(printed), 2)]
    index = [["D00", "Cover, index and general notes"], ["D01", "General arrangement"], ["D02", "Hull lines and table of offsets"],
             ["D03", "Interior arrangement and systems"], ["D04", "Keel fin and lead bulb"], ["D05", "Twin rudders, stocks and steering"],
             ["D06", "Wing sail and tail"], ["D07", "Mast step, spar and stern stub"], ["D08", "Deck hatch, solar layout, penetrations"],
             ["D09", "Watertight subdivision, foam fill, battery box, labels"]]
    for k, pr in enumerate(pairs):
        index.append([f"D{10 + k:02d}", "Printed parts " + ", ".join(p for _, p in pr)])
    with PdfPages(f"{OUT}/Drawings.pdf") as pdf:
        sheet_cover(pdf, index)
        sheet_ga(pdf); sheet_lines(pdf); sheet_interior(pdf); sheet_keel(pdf)
        sheet_rudder(pdf); sheet_wing(pdf); sheet_mast(pdf); sheet_deck(pdf); sheet_subdivision(pdf)
        for k, pr in enumerate(pairs):
            sheet_parts(pdf, pr, f"D{10 + k:02d}")
    print("ok", len(index), "sheets")

if __name__ == "__main__":
    main()
