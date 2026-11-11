"""Master geometry for the solar-sail ocean drone. All units mm.
Coordinates: x aft from bow (0..1500), y to port, z up from hull bottom at midships."""
import numpy as np

L = 1500.0
BMAX = 200.0          # max half-beam (400 mm beam)
X_BMAX = 0.55         # fraction of L where beam is max
B_TRANSOM = 150.0     # transom half-beam
DECK_Z = 230.0
DWL = 102.0           # Rev C3 design waterline at about 26.9 kg all-up (C2: 101 at 26.4; C/C1: 98 at 25.3; Rev B: 90 at about 21 kg)
MASS_KG = 26.9        # Rev C3 all-up mass, from the simulator mass model
SECTION_N = 2.2       # superellipse exponent of the sections (round bilge)

def half_beam(x):
    s = np.clip(np.asarray(x, float) / L, 0, 1)
    fwd = BMAX * np.clip(1 - (1 - s / X_BMAX) ** 2, 0, 1) ** 0.6
    aft = BMAX - (BMAX - B_TRANSOM) * ((s - X_BMAX) / (1 - X_BMAX)) ** 2
    return np.where(s <= X_BMAX, fwd, aft)

def keel_z(x):
    s = np.clip(np.asarray(x, float) / L, 0, 1)
    fwd = 120 * np.clip(1 - s / 0.5, 0, 1) ** 2.2
    aft = 60 * (np.clip(s - 0.5, 0, None) / 0.5) ** 2
    return np.where(s < 0.5, fwd, aft)

def deck_z(x):
    s = np.clip(np.asarray(x, float) / L, 0, 1)
    return DECK_Z + 30 * np.clip(1 - s / 0.4, 0, 1) ** 2

def section(x, n=60):
    """Half-section outline (y, z) at station x, keel to deck edge."""
    zk, zd, b = float(keel_z(x)), float(deck_z(x)), float(half_beam(x))
    t = np.linspace(0, 1, n) ** 2
    y = b * (1 - (1 - t) ** SECTION_N) ** (1 / SECTION_N)
    z = zk + t * (zd - zk)
    return y, z

def half_beam_at(x, z):
    zk, zd, b = float(keel_z(x)), float(deck_z(x)), float(half_beam(x))
    if z <= zk:
        return 0.0
    t = min((z - zk) / (zd - zk), 1.0)
    return b * (1 - (1 - t) ** SECTION_N) ** (1 / SECTION_N)

def naca(t, c=1.0, n=80):
    """Closed symmetric NACA 00xx outline, LE at 0, TE at c. Returns (x, y) CCW."""
    beta = np.linspace(0, np.pi, n)
    xc = (1 - np.cos(beta)) / 2
    yt = 5 * t * (0.2969 * np.sqrt(xc) - 0.1260 * xc - 0.3516 * xc**2 + 0.2843 * xc**3 - 0.1036 * xc**4)
    xs = np.concatenate([xc[::-1], xc[1:]]) * c
    ys = np.concatenate([yt[::-1], -yt[1:]]) * c
    return xs, ys

# ---- appendages -------------------------------------------------------
FIN = dict(root_chord=170, tip_chord=150, root_le_x=657, tip_le_x=670, root_z=0, tip_z=-430, t=0.12)
# Rev C2 (11 Nov 2026): solid hardwood core, 6 x 6 oz glass and a carbon strip each side, and a tenon into the keel box.
# The XPS-cored fin with 3 x 6 oz was about 3 times the static knockdown load: docs/Keel_Structure_Loads.md
FIN_BUILD = dict(core="hardwood", plies=6, carbon_w=60, carbon_t=1.5, carbon_x0=25, rods_x=(50, 105), tenon_h=60, tenon_x1=772)
KEELBOX = dict(x0=650, x1=772, w=60, h=60, plate_t=10)     # socket for the fin tenon; G10 plate 122 x 60 x 10 on top takes the rod nuts
FLOORS = ((650.0, 80.0), (800.0, 32.0))                    # (x, top z): 9 mm marine-ply floors glassed across the hull at the keel box
BULB = dict(length=320, dia=72, nose_x=579, axis_z=-430 - 6, max_at=0.40)   # Rev C: D72 (was D68), lead ~9.2 kg
RUDDER = dict(stock_x=1400, chord=120, stock_from_le=22, top_z=72, bot_z=-158, t=0.12, stock_d=12, trunk_top_z=175)   # Rev C: top at the hull surface 100 mm off centre
RUDDER_Y = (-100.0, 100.0)   # Rev C: twin rudders, each on its own stock, trunk and servo, 100 mm either side of the centreline
LEAD_DENSITY = 11.34e-6  # kg/mm^3

# ---- rig ----------------------------------------------------------------
MAST_X = 600.0
SPAR_OD = 30.0          # Rev C: 30 x 26 carbon (was 25 x 22)
SPAR_ID = 22.0          # Rev C3: 30 x 22 (was 30 x 26): 1.6 times the bending strength, same bearings and printed bores
SPAR_BOT_Z = 105.0      # Rev C3: spar reaches down to z 105 (was 150) for the wider bearing spacing
BEARING_SPACING = 130.0  # Rev C3: bearing centres 130 apart in a longer housing P07 (was 78)
WING = dict(chord=300, span=1000, pivot_from_le=66, root_z=300, t=0.15)
MAST_TUBE = dict(od=60.3, id=52.5, top_z=250)          # 2 in. sch 40 PVC, bonded hull-to-deck
BEARING = dict(id=30, od=42, w=7, name="6806-2RS stainless")   # Rev C (was 6805, 25 x 37 x 7)
BOOM = dict(od=12.0, z=276, length=600)                # spar axis to tail pivot
TAIL = dict(chord=120, span=200, pivot_from_le=24, bot_z=300, t=0.12, pivot_d=6)
# Rev B: counterweight pod on a 12 mm carbon arm, pod axis 300 forward of the spar axis, at boom height
CWARM = dict(reach=300, tube_len=244, od=12.0, z=276, pod_od=64, pod_h=74, pod_bot_z=264, lead_kg=0.8)   # unchanged in Rev C: the heavier spar sits on the pivot axis

# ---- deck & stern -------------------------------------------------------
HATCH = dict(x0=330, x1=530, w=220, lid_margin=30)
SOLAR = [dict(x0=650, x1=1070, w=280), dict(x0=1080, x1=1480, w=280)]
STUB = dict(x=1530, od=20.0, bot_z=150, top_z=650)
# Rev C additions on the stub: YB3 backup tracker platform (P19) and all-round white light (P20)
YB3 = dict(x=180.0, plate_l=170, plate_w=100, box=(150, 86, 32), kg=0.33, well=(176, 106, 38))   # Rev C3: in a well in the foredeck, centred at x 180, top flush with the deck so the tail boom (underside z 270) swings clear. Was on the stern post at z 480
POST_TUBE = "20 x 2 pultruded fibreglass tube"   # Rev C3 (was 20 x 1.5 aluminium): bends instead of kinking
CW_ARM = "12 mm solid pultruded fibreglass rod"  # Rev C3 (was 12 x 10 carbon tube): takes about six times the shock energy   # YB3 size approximate: confirm on the unit
NAVLIGHT = dict(z=600, reach=45, puck_d=30)
VANE_Z = 650
ANT_Z = 560

# ---- interior -----------------------------------------------------------
BATTERY = dict(x0=780, x1=960, w=80, h=170)
# Rev C: battery in its own sealed box (laminated foam/glass, O-ring lid like the hatch)
BATTBOX = dict(x0=774, x1=966, w=96, z0=34, z1=213, wall=4)   # removable; comes out through the hatch
# Rev C: watertight subdivision and foam fill
BULKHEADS = (300.0, 1260.0)          # glassed-in 10 mm foam bulkheads (templates T17, T18)
FOAM_DENSITY = 28e-9                 # kg/mm^3, extruded polystyrene (XPS) blocks
FREE_FLOOD_L = 3.0                   # target: floodable volume left in the dry bay after the fitted blocks
EBOX = dict(x0=980, x1=1220, w=160, h=90, z0=118)   # Rev C1 (11 Nov 2026): box raised on a shelf, bottom at z 118 (was 60), above the flood level
SUMP = dict(x0=560, x1=770, top_z=45)                # Rev C1: the only open space in the dry bay, at its low point; leak probe here

def hull_z_at(x, y):
    """Height of the outside hull surface at station x, distance y off the centreline (bottom half)."""
    zk, zd = float(keel_z(x)), float(deck_z(x))
    zz = np.linspace(zk, zd, 400)
    yy = np.array([half_beam_at(x, z) for z in zz])
    return float(np.interp(abs(y), yy, zz))

def inner_volume(x0, x1, skin=11.0, nx=120, nz=80):
    """Volume (litres) inside the hull skin between stations x0 and x1, up to the underside of the deck."""
    xs = np.linspace(x0, x1, nx); A = []
    for x in xs:
        zk, zd = float(keel_z(x)) + skin, float(deck_z(x)) - skin
        if zd <= zk: A.append(0.0); continue
        zz = np.linspace(zk, zd, nz)
        yy = np.array([max(half_beam_at(x, z) - skin, 0.0) for z in zz])
        A.append(2 * np.trapezoid(yy, zz))
    return float(np.trapezoid(A, xs)) / 1e6

def bulb_radius(xl):
    """Radius along bulb from nose (xl in 0..length)."""
    Lb, R, m = BULB['length'], BULB['dia'] / 2, BULB['max_at']
    u = np.clip(np.asarray(xl, float) / Lb, 0, 1)
    fwd = R * np.sqrt(np.clip(1 - ((m - u) / m) ** 2, 0, 1))
    aft = R * np.clip(1 - ((u - m) / (1 - m)) ** 2, 0, 1) ** 0.75
    return np.where(u <= m, fwd, aft)

def bulb_mass():
    xl = np.linspace(0, BULB['length'], 2001)
    r = bulb_radius(xl)
    vol = np.trapezoid(np.pi * r**2, xl)
    return vol, vol * LEAD_DENSITY

def displacement_to(z_wl, nx=301, nz=200):
    xs = np.linspace(0, L, nx)
    area = []
    for x in xs:
        zk = float(keel_z(x))
        if z_wl <= zk:
            area.append(0.0); continue
        zz = np.linspace(zk, z_wl, nz)
        yy = np.array([half_beam_at(x, z) for z in zz])
        area.append(2 * np.trapezoid(yy, zz))
    return np.trapezoid(area, xs)  # mm^3

if __name__ == "__main__":
    v, m = bulb_mass()
    print(f"bulb volume {v/1e3:.0f} cm3, lead mass {m:.2f} kg")
    for zw in (70, 80, 90, 100):
        print(zw, f"{displacement_to(zw)/1e6:.1f} kg")
