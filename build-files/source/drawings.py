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
        "2. Design waterline (DWL) z = 90 at about 21 kg all-up mass (hull 19.4 kg displacement + appendages).",
        "3. Printed parts: 0.4 mm nozzle, 0.2 mm layers, 4+ walls. Use ASA outdoors in UV; PETG is fine below deck.",
        "   STL files are in print orientation; no supports needed except where a sheet says so.",
        "4. Bought-in parts follow the Recommended Parts list in the build plan. Servo tab spacing, AS5600 board size and",
        "   patch-antenna footprint vary by supplier: printed parts use slots and recesses rather than fixed hole patterns.",
        "5. Full-size cutting templates (hull frames, foils, wing, hatch) are in Templates.pdf (tiled on Letter, 1:1)",
        "   and as DXF files. Check the 100 mm scale bar on every printed page before cutting.",
        "6. All fasteners and shafts 316 stainless. Bed every hull penetration in polyurethane sealant.",
        "7. This is a hobby design, not a classed or certified vessel. Tank-test self-righting before going to sea."], fs=6.2, lh=3.8)
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
    ax.plot([-20, 1520], [90, 90], color=WATER, lw=0.8); ax.text(-25, 90, "DWL", color=WATER, fontsize=5.5, ha="right", va="center")
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
    dim(ax, (1590, 90), (1590, -468), 0, "draft 558")
    dim(ax, (1590, 90), (1590, 1300), 0, "air draft 1210")
    dim(ax, (le, 1320), (te, 1320), 0, "300")
    dim(ax, (440, 300), (440, 1300), 0, "wing 1000")
    leader(ax, (700, -200), (300, -250), "Keel fin  NACA 0012\n170/150 chord  (D04)")
    leader(ax, (750, -434), (300, -400), "Lead bulb 8.2 kg  (D04)")
    leader(ax, (1440, -100), (1100, -330), "Spade rudder  (D05)")
    leader(ax, (te, 900), (1000, 1000), "Rigid wing sail\nNACA 0015  (D06)")
    leader(ax, (1250, 450), (1150, 760), "Tail flap on servo  (D06)")
    leader(ax, (S['x'], 400), (1250, 600), "Radar reflector")
    leader(ax, (S['x'] + 160, D.VANE_Z + 40), (1300, 1100), "Wind vane P01-P04\nantenna platform P05\non 20 mm stub  (D07)")
    leader(ax, (D.MAST_X, 200), (250, 520), "2 in. PVC mast tube +\nbearing housing P07  (D07)")
    ax.text(820, 150, "solar", fontsize=5, color=BLUE)

    ax2 = view(fig, 222, 200, (-30, 1620), (-235, 235), s, "PLAN (deck)")
    poly(ax2, hull_plan(), lw=THICK)
    ax2.plot([0, 1500], [0, 0], color=GREY, lw=0.25, ls="-.")
    H = D.HATCH
    ax2.add_patch(Rectangle((H['x0'], -H['w']/2), H['x1'] - H['x0'], H['w'], fill=False, lw=MED, ls="--"))
    ax2.add_patch(Rectangle((H['x0'] - 30, -H['w']/2 - 30), H['x1'] - H['x0'] + 60, H['w'] + 60, fill=False, lw=THIN))
    ax2.text((H['x0'] + H['x1'])/2, 0, "bolted\nhatch", fontsize=5, ha="center", va="center")
    ax2.add_patch(Circle((D.MAST_X, 0), D.MAST_TUBE['od']/2, fill=False, lw=MED))
    for i, P in enumerate(D.SOLAR):
        ax2.add_patch(Rectangle((P['x0'], -P['w']/2), P['x1'] - P['x0'], P['w'], fc="#cfe0f3", ec=BLUE, lw=THIN))
        ax2.text((P['x0'] + P['x1'])/2, 0, f"solar panel {i+1}\n~20 W  420 x 280", fontsize=5, ha="center", va="center", color=BLUE)
    ax2.add_patch(Circle((D.STUB['x'], 0), 10, fill=False, lw=MED))
    ax2.add_patch(Circle((D.MAST_X, 0), 700, fill=False, lw=0.3, ls=":", ec=GREY))
    ax2.text(D.MAST_X + 495, -215, "tail sweep R 700", fontsize=5, color=GREY, rotation=45)
    dim(ax2, (1500, -200), (1500, 200), 0, "")
    ax2.text(1515, 0, "beam 400\n(max at x 825)", fontsize=5.5, va="center")
    dim(ax2, (0, 215), (D.MAST_X, 215), 0, "600")
    dim(ax2, (0, -222), (H['x0'], -222), 0, "330")
    notes(bg, 225, 180, "Key data", [
        "Length overall 1500   Beam 400   Hull depth 230",
        "Draft 558 (DWL to bulb bottom)   Air draft 1210",
        "Displacement about 21 kg   Ballast 8.2 kg lead",
        "Wing 1000 x 300 (0.30 m2), free-rotating on 25 mm spar",
        "Solar about 40 W on deck   Battery 192 Wh LiFePO4",
        "Self-righting: verify in a tank test (Gate 3)"], fs=6.3)
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
    for wl in (30, 60, 90, 120, 150):
        xs = np.linspace(0, 1500, 300); m = D.keel_z(xs) < wl
        ax.plot(xs[m], np.full(m.sum(), wl), color=WATER if wl == 90 else GREY, lw=0.6 if wl == 90 else 0.25, ls="-" if wl == 90 else ":")
    ax2 = view(fig, 20, 152, (-20, 1520), (-10, 215), s, "")
    bg.text(20, 200, "HALF-BREADTH PLAN (deck edge solid, DWL blue, waterlines z 30/60/120/150 dotted)", fontsize=7, weight="bold")
    xs = np.linspace(0, 1500, 300)
    ax2.plot(xs, D.half_beam(xs), color=INK, lw=MED); ax2.plot([0, 1500], [0, 0], color=INK, lw=0.3)
    ax2.plot([1500, 1500], [0, D.B_TRANSOM], color=INK, lw=MED)
    for wl in (30, 60, 90, 120, 150):
        ax2.plot(xs, [D.half_beam_at(x, wl) for x in xs], color=WATER if wl == 90 else GREY, lw=0.4 if wl == 90 else 0.25, ls="-" if wl == 90 else ":")
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
    ax3.plot([-210, 210], [90, 90], color=WATER, lw=0.5)
    rows = []
    for i, x in enumerate(STATIONS):
        rows.append([i, int(x), f"{float(D.keel_z(x)):.1f}", f"{float(D.deck_z(x)):.1f}", f"{float(D.half_beam(x)):.1f}",
                     f"{D.half_beam_at(x, 30):.1f}", f"{D.half_beam_at(x, 60):.1f}", f"{D.half_beam_at(x, 90):.1f}",
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
        "dashed frame line = hull minus 11 mm), 2 x 6 oz glass outside, 1 x 6 oz inside, peel ply."], fs=6.0, lh=3.4)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D03 interior
def sheet_interior(pdf):
    fig, bg = new_sheet("D03", "Interior arrangement and systems", "Scale 1:7.5")
    s = 7.5
    ax = view(fig, 15, 165, (-20, 1560), (-40, 270), s, "INBOARD PROFILE")
    poly(ax, hull_profile(), lw=MED, ec=GREY)
    MT = D.MAST_TUBE; kz = float(D.keel_z(D.MAST_X))
    ax.add_patch(Rectangle((D.MAST_X - MT['od']/2, kz), MT['od'], MT['top_z'] - kz, fill=False, lw=MED))
    ax.add_patch(Rectangle((D.MAST_X - 27, MT['top_z'] - 80), 54, 85, fill=False, lw=THIN, hatch="////"))
    ax.plot([D.MAST_X] * 2, [150, 270], color=INK, lw=0.8)
    ax.add_patch(Rectangle((D.MAST_X - 8, 120), 16, 30, fc="#ddd", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((650, 0), 190, 40, fill=False, lw=MED, hatch="\\\\"))
    for xr in (707, 762):
        ax.plot([xr, xr], [-30, 40], color=INK, lw=1)
    B = D.BATTERY; E = D.EBOX
    ax.add_patch(Rectangle((B['x0'], 42), B['x1'] - B['x0'], B['h'], fc="#f4e3c3", ec=INK, lw=MED))
    ax.add_patch(Rectangle((E['x0'], 60), E['x1'] - E['x0'], E['h'], fc="#d9e8d4", ec=INK, lw=MED))
    R = D.RUDDER
    ax.add_patch(Rectangle((R['stock_x'] - 9, float(D.keel_z(R['stock_x']))), 18, 175 - float(D.keel_z(R['stock_x'])), fill=False, lw=MED))
    ax.plot([R['stock_x']] * 2, [-30, 185], color=INK, lw=0.8)
    ax.add_patch(Rectangle((1300, 120), 60, 48, fc="#eee", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((1380, 170), 90, 6, fc=INK))
    ax.add_patch(Rectangle((330, 230), 200, 8, fill=False, lw=MED))
    for xp in (500, 900, 1350):
        ax.add_patch(Circle((xp, float(D.keel_z(xp)) + 8), 5, fc=BLUE, ec=BLUE))
    leader(ax, (D.MAST_X + 27, 200), (330, 140), "Mast tube 2 in. sch 40 PVC,\nglassed to hull + deck")
    leader(ax, (D.MAST_X, 135), (200, 70), "6-wire capsule slip ring\n(tail servo power + signal)")
    leader(ax, (745, 20), (600, -25), "Keel box: 2 x M10 316 rods,\nG10 backing plate 190 x 60 x 10", ha="right")
    leader(ax, (870, 180), (830, 255), "Battery 12 V 15 Ah (strap anchors P16)")
    leader(ax, (1100, 150), (1050, 225), "IP68 box: Pixhawk, ESP32, RockBLOCK,\nGPS, GV-5 MPPT (tray P15)")
    leader(ax, (R['stock_x'], 100), (1500, 30), "Rudder tube, top at z 175\n(above DWL, no seal)")
    leader(ax, (1330, 168), (1180, 40), "Servo P12 + tiller P11")
    leader(ax, (500, float(D.keel_z(500)) + 8), (420, 60), "Leak probes (SOS) at\nlowest points", color=BLUE)
    ax.plot([0, 1500], [90, 90], color=WATER, lw=0.5)
    ax2 = view(fig, 15, 70, (-20, 1560), (-220, 220), s, "INTERIOR PLAN (below deck)")
    poly(ax2, hull_plan(), lw=MED, ec=GREY)
    ax2.add_patch(Circle((D.MAST_X, 0), MT['od']/2, fill=False, lw=MED))
    ax2.add_patch(Rectangle((650, -30), 190, 60, fill=False, lw=MED, hatch="\\\\"))
    ax2.add_patch(Rectangle((B['x0'], -B['w']/2 + 60), B['x1'] - B['x0'], B['w'], fc="#f4e3c3", ec=INK))
    ax2.add_patch(Rectangle((E['x0'], -E['w']/2), E['x1'] - E['x0'], E['w'], fc="#d9e8d4", ec=INK))
    ax2.add_patch(Circle((R['stock_x'], 0), 9, fill=False, lw=MED))
    ax2.add_patch(Rectangle((1300, -15), 60, 30, fc="#eee", ec=INK, lw=THIN))
    ax2.plot([1360, R['stock_x']], [0, 0], color=INK, lw=0.6)
    for xb in (B['x0'] - 10, B['x1'] + 10):
        for yb in (-12, 98):
            ax2.add_patch(Rectangle((xb - 6, yb - 6), 12, 12, fc=INK))
    ax2.plot([1100, 1250, 1530], [0, 60, 0], color=BLUE, lw=0.4, ls="--")
    ax2.plot([1000, D.MAST_X], [-50, -20], color=BLUE, lw=0.4, ls="--")
    ax2.text(1260, 70, "cable to stub (vane, antenna)", fontsize=5, color=BLUE)
    ax2.text(700, -70, "cable to slip ring", fontsize=5, color=BLUE)
    notes(bg, 15, 37 + 22, "Systems notes", [
        "Masses (approx, kg): hull + deck 4.5, fin 1.2, bulb 8.2, rudder 0.3, wing + spar + tail 1.6, battery 2.0, electronics + cables 1.2, solar 1.0, misc 1.0  -> about 21 kg.",
        "Battery sits beside the keel box to keep weight low and on the centreline; the IP68 box is aft of it so cables to the stub and rudder stay short.",
        "All penetrations use WetLink M10 on P17 pads. Solar cables enter through one penetrator per panel just inside the panel edge."], fs=6.0, lh=3.6)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D04 keel
def sheet_keel(pdf):
    fig, bg = new_sheet("D04", "Keel fin and lead bulb", "Scale 1:4")
    s = 4
    F = D.FIN
    ax = view(fig, 15, 45, (540, 920), (-480, 60), s, "FIN + BULB ELEVATION")
    poly(ax, fin_poly(), lw=MED)
    poly(ax, bulb_profile(), lw=MED, fc="#ccc", fill=True)
    for xr in (707, 762):
        ax.plot([xr, xr], [-490 + 50, 45], color=INK, lw=0.5, ls="--")
    ax.add_patch(Rectangle((650, 0), 190, 10, fill=False, lw=THIN, hatch="////"))
    dim(ax, (F['root_le_x'], 25), (F['root_le_x'] + F['root_chord'], 25), 0, "170 root chord")
    dim(ax, (F['tip_le_x'], -395), (F['tip_le_x'] + F['tip_chord'], -395), 0, "150 tip chord")
    dim(ax, (890, 0), (890, -430), 0, "430")
    dim(ax, (D.BULB['nose_x'], -485 + 10), (D.BULB['nose_x'] + 320, -485 + 10), 0, "bulb 320")
    dim(ax, (D.BULB['nose_x'] + 128, -434 - 34), (D.BULB['nose_x'] + 128, -434 + 34), 0, "D68")
    dim(ax, (657, 45), (707, 45), 0, "50"); dim(ax, (707, 45), (762, 45), 0, "55")
    leader(ax, (735, -200), (560, -150), "2 x M10 316 threaded rod,\nfull length, bonded in\nfin core and bulb")
    ax2 = view(fig, 120, 150, (-10, 180), (-15, 15), 1.3, "FIN ROOT SECTION  NACA 0012  (1:1.3)")
    P = foil_xy(0.12, 170); poly(ax2, P, lw=MED)
    for xr in (50, 105): ax2.add_patch(Circle((xr, 0), 5.5, fill=False, lw=THIN))
    ax2.plot([0, 170], [0, 0], color=GREY, lw=0.25, ls="-.")
    dim(ax2, (0, 15), (50, 15), 0, "50", fs=5); dim(ax2, (50, 15), (105, 15), 0, "55", fs=5)
    xl = np.arange(0, 321, 20)
    rows = [[int(v), f"{float(D.bulb_radius(v))*2:.1f}"] for v in xl]
    table(bg, 255, 252, ["from nose", "diameter"], rows, [20, 18], fs=5.5, rh=3.7)
    v, m = D.bulb_mass()
    notes(bg, 120, 125, "Fin construction", [
        "1. Hot-wire cut a blue XPS or Divinycell core with templates T12 (root) and T13 (tip).",
        "2. Bore 2 x 12 mm holes at 50 and 105 from the root LE; bond the M10 rods in with thickened epoxy.",
        "3. Glass 3 x 6 oz each side, +/-45 deg on the inner layer; fair, then 2-part epoxy primer.",
        "4. Rods pass 40 mm into the keel box and take 316 nuts on a G10 plate (190 x 60 x 10) glassed into the hull.",
        "", "Bulb", f"Volume {v/1e3:.0f} cm3 -> {m:.1f} kg of lead. Make a plaster mould from pattern P14a/b",
        "(printed), cast outdoors with PPE, then drill 2 x 12 mm holes 60 deep at the rod positions",
        "(91 + 37 and 91 + 92 mm from the nose, measured on the slot) and bond the rods in with epoxy.",
        "Fair with epoxy filler; seal with 2 coats epoxy barrier coat."], fs=6.0, lh=3.6)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D05 rudder
def sheet_rudder(pdf):
    fig, bg = new_sheet("D05", "Rudder, stock and steering", "Scale 1:2")
    R = D.RUDDER; s = 2
    le = R['stock_x'] - R['stock_from_le']
    ax = view(fig, 20, 45, (1340, 1540), (-215, 220), s, "RUDDER ELEVATION (looking to port)")
    poly(ax, rudder_poly(), lw=MED)
    kz = float(D.keel_z(R['stock_x']))
    ax.plot([1340, 1540], [kz, kz], color=GREY, lw=0.3, ls="--"); ax.text(1342, kz + 3, "hull bottom", fontsize=5, color=GREY)
    ax.add_patch(Rectangle((R['stock_x'] - 6, R['bot_z'] + 8), 12, 210 - R['bot_z'] - 8, fill=False, lw=THIN))
    ax.add_patch(Rectangle((R['stock_x'] - 9, kz), 18, 175 - kz, fill=False, lw=MED, hatch="////"))
    for zb in (kz, 175 - 15):
        ax.add_patch(Rectangle((R['stock_x'] - 9, zb), 18, 15, fc="#bbb", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((R['stock_x'] - 13, 180), 26, 16, fill=False, lw=MED))
    ax.plot([1340, 1540], [90, 90], color=WATER, lw=0.5)
    dim(ax, (le, R['top_z'] + 12), (le + R['chord'], R['top_z'] + 12), 0, "120 chord")
    dim(ax, (le, -205), (R['stock_x'], -205), 0, "22")
    dim(ax, (1525, R['top_z']), (1525, R['bot_z']), 0, "230 span")
    dim(ax, (1525, kz), (1525, 175), 0, "tube")
    leader(ax, (R['stock_x'], 120), (1450, 150), "Rudder tube: GRP or 316 tube,\nID 14, glassed to hull floor,\ntop at z 175 (85 above DWL)")
    leader(ax, (R['stock_x'] + 9, kz + 7), (1460, 20), "igus iglide J flange\nbushing 12 x 14 (x2)")
    leader(ax, (R['stock_x'] + 13, 188), (1460, 205), "Tiller arm P11")
    leader(ax, (R['stock_x'], -100), (1460, -120), "12 mm 316 stock,\nlength 420")
    ax2 = view(fig, 150, 200, (-5, 125), (-12, 12), 1, "BLADE SECTION  NACA 0012  (1:1)")
    poly(ax2, foil_xy(0.12, 120), lw=MED); ax2.add_patch(Circle((22, 0), 6, fill=False, lw=THIN))
    dim(ax2, (0, 11), (22, 11), 0, "22", fs=5)
    notes(bg, 150, 180, "Build", [
        "1. Print cores P13a/b, slide on the stock, pin with 4 mm 316 pins, epoxy the joint.",
        "2. Glass 2 x 6 oz over the blade, wrapping the tip; fair to template T14.",
        "3. Balanced rudder: about 15% of the area is ahead of the stock, so the servo",
        "   needs little holding torque and can be powered down between corrections.",
        "4. Stock: 12 mm 316 round bar, 420 long; 3 mm cross-hole for the tiller pin.",
        "5. Bottom bushing sits flush with the hull bottom; top bushing at the tube top.",
        "6. Stop the rudder at +/-35 deg with the servo end points (ArduPilot SERVO1_MIN/MAX)."], fs=6.2, lh=3.8)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D06 wing & tail
def sheet_wing(pdf):
    fig, bg = new_sheet("D06", "Wing sail and tail", "Elevation 1:6, plan 1:6, section 1:2")
    W = D.WING; T = D.TAIL; B = D.BOOM
    le, te, z0, z1 = wing_rect()
    ax = view(fig, 15, 45, (450, 1350), (230, 1340), 6, "WING + TAIL ELEVATION")
    ax.add_patch(Rectangle((le, z0), W['chord'], W['span'], fill=False, lw=MED))
    ax.plot([le, te], [z0 + 500] * 2, color=GREY, lw=0.4, ls="--"); ax.text(te + 5, z0 + 500, "core joint", fontsize=5, va="center")
    ax.plot([D.MAST_X] * 2, [240, z1 - 10], color=INK, lw=0.8, ls="-.")
    ax.add_patch(Rectangle((le + 4, z0 + 60), 25, 120, fc="#888", ec=INK, lw=THIN))
    tp = D.MAST_X + B['length']
    ax.plot([D.MAST_X, tp], [B['z']] * 2, color=INK, lw=1.2)
    ax.add_patch(Rectangle((D.MAST_X - 37, 256), 99, 40, fill=False, lw=THIN))
    ax.add_patch(Rectangle((tp - 28, 252), 92, 48, fill=False, lw=THIN))
    ax.add_patch(Rectangle((tp - T['pivot_from_le'], T['bot_z']), T['chord'], T['span'], fill=False, lw=MED))
    ax.plot([tp, tp], [T['bot_z'], T['bot_z'] + T['span']], color=INK, lw=0.4, ls="-.")
    dim(ax, (le, z1 + 20), (te, z1 + 20), 0, "300")
    dim(ax, (le, z1 + 45), (D.MAST_X, z1 + 45), 0, "66")
    dim(ax, (430 + 40, z0), (430 + 40, z1), 0, "1000")
    dim(ax, (D.MAST_X, 245), (tp, 245), 0, "boom 600 (spar to tail pivot)")
    dim(ax, (tp + 110, T['bot_z']), (tp + 110, T['bot_z'] + T['span']), 0, "200")
    leader(ax, (le + 16, z0 + 120), (700, 420), "Nose counterweight pocket\n(lead, balance on spar axis)")
    leader(ax, (D.MAST_X, 276), (700, 330), "Spar clamp P08")
    leader(ax, (tp + 10, 276), (1000, 380), "Tail servo housing P09")
    leader(ax, (tp + 40, 420), (1050, 600), "Tail fin P10a/b\nNACA 0012, 120 chord")
    ax2 = view(fig, 200, 160, (-10, 320), (-30, 30), 2, "WING SECTION  NACA 0015  (1:2)")
    poly(ax2, foil_xy(0.15, 300), lw=MED)
    ax2.add_patch(Circle((66, 0), 12.7, fill=False, lw=MED))
    ax2.add_patch(Rectangle((4, -6), 25, 12, fc="#888", ec=INK, lw=THIN))
    dim(ax2, (0, 28), (66, 28), 0, "66", fs=5); dim(ax2, (66, 28), (300, 28), 0, "234", fs=5)
    ax3 = view(fig, 200, 62, (-750, 150), (-60, 100), 6, "PLAN OF ROTATING RIG (1:6)")
    poly(ax3, np.c_[-(foil_xy(0.15, 300)[:, 0] - 66), foil_xy(0.15, 300)[:, 1]], lw=MED)
    ax3.plot([0, -600], [0, 0], color=INK, lw=1)
    P = foil_xy(0.12, 120); poly(ax3, np.c_[-(P[:, 0] - 24) - 600, P[:, 1]], lw=MED)
    ax3.add_patch(Circle((0, 0), 12.5, fill=False, lw=MED))
    ax3.annotate("", xy=(-120, 70), xytext=(130, 70), arrowprops=dict(arrowstyle="-|>", lw=0.6))
    ax3.text(5, 80, "apparent wind", fontsize=5.5, ha="center")
    ax3.text(-600, -40, "tail", fontsize=5.5, ha="center"); ax3.text(-80, -40, "wing", fontsize=5.5, ha="center")
    notes(bg, 200, 140, "Wing build", [
        "Core: two 500 mm XPS blocks hot-wire cut with template T15 (same root and tip), bored 25.4 mm for the spar.",
        "Skin: 2 x 6 oz glass, vacuum bagged if possible. Root and tip: 3 mm ply caps. Spar: 25 mm OD carbon tube, 1100 long.",
        "Balance the wing+tail assembly so its centre of mass is on the spar axis (lead in the nose pocket).",
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
    ax.add_patch(Rectangle((D.MAST_X - 26.15, MT['top_z'] - 80), 52.3, 80, fill=False, lw=MED, hatch="////"))
    ax.add_patch(Rectangle((D.MAST_X - 33, MT['top_z']), 66, 5, fill=False, lw=MED, hatch="////"))
    for zb in (MT['top_z'] - 2, MT['top_z'] - 80):
        ax.add_patch(Rectangle((D.MAST_X - 18.5, zb), 37, 7, fc="#999", ec=INK, lw=THIN))
    ax.add_patch(Rectangle((D.MAST_X - 12.5, 150), 25, 270, fill=False, lw=MED))
    ax.add_patch(Rectangle((D.MAST_X - 7, 115), 14, 35, fc="#ccc", ec=INK, lw=THIN))
    ax.plot([520, 680], [D.DECK_Z, D.DECK_Z], color=GREY, lw=0.4, ls="--"); ax.text(522, D.DECK_Z + 3, "deck", fontsize=5)
    ax.plot([520, 680], [kz, kz], color=GREY, lw=0.4, ls="--"); ax.text(522, kz + 3, "hull bottom", fontsize=5)
    dim(ax, (670, MT['top_z'] - 80), (670, MT['top_z'] + 5), 0, "85")
    dim(ax, (D.MAST_X - 30.15, 120), (D.MAST_X + 30.15, 120), 0, "OD 60.3")
    leader(ax, (D.MAST_X + 18, MT['top_z'] + 2), (640, 330), "6805-2RS 316 (x2)")
    leader(ax, (D.MAST_X + 12, 300), (640, 300), "Spar 25 OD carbon")
    leader(ax, (D.MAST_X + 7, 140), (640, 80), "Slip ring, 12.5 mm,\n6 wire, in spar end")
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
    notes(bg, 260, 250, "Notes", [
        "Spar: 25 mm OD carbon tube, 1150 long (z 150 to 1300).",
        "Slip ring in the spar's lower end carries 3 wires to the",
        "tail servo; it must turn freely through 360 deg.",
        "Lock the spar against lifting with a 316 collar under",
        "the lower bearing.",
        "",
        "Stub: 20 mm OD x 1.5 wall 6061 aluminium (anodised) or",
        "carbon tube, 500 long; cables run inside it to the",
        "vane cap and down through a WetLink in the transom.",
        "Vane shaft: 8 mm 316, 75 long, 2 x S608-2RS bearings."], fs=6.0, lh=3.6)
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
             ["D03", "Interior arrangement and systems"], ["D04", "Keel fin and lead bulb"], ["D05", "Rudder, stock and steering"],
             ["D06", "Wing sail and tail"], ["D07", "Mast step, spar and stern stub"], ["D08", "Deck hatch, solar layout, penetrations"]]
    for k, pr in enumerate(pairs):
        index.append([f"D{9 + k:02d}", "Printed parts " + ", ".join(p for _, p in pr)])
    with PdfPages(f"{OUT}/Drawings.pdf") as pdf:
        sheet_cover(pdf, index)
        sheet_ga(pdf); sheet_lines(pdf); sheet_interior(pdf); sheet_keel(pdf)
        sheet_rudder(pdf); sheet_wing(pdf); sheet_mast(pdf); sheet_deck(pdf)
        for k, pr in enumerate(pairs):
            sheet_parts(pdf, pr, f"D{9 + k:02d}")
    print("ok", len(index), "sheets")

if __name__ == "__main__":
    main()
