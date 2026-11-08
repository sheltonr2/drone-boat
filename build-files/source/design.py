"""Master geometry for the solar-sail ocean drone. All units mm.
Coordinates: x aft from bow (0..1500), y to port, z up from hull bottom at midships."""
import numpy as np

L = 1500.0
BMAX = 200.0          # max half-beam (400 mm beam)
X_BMAX = 0.55         # fraction of L where beam is max
B_TRANSOM = 150.0     # transom half-beam
DECK_Z = 230.0
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
BULB = dict(length=320, dia=68, nose_x=579, axis_z=-430 - 4, max_at=0.40)   # lead, ~8 kg
RUDDER = dict(stock_x=1400, chord=120, stock_from_le=22, top_z=40, bot_z=-190, t=0.12, stock_d=12)
LEAD_DENSITY = 11.34e-6  # kg/mm^3

# ---- rig ----------------------------------------------------------------
MAST_X = 600.0
SPAR_OD = 25.0
WING = dict(chord=300, span=1000, pivot_from_le=66, root_z=300, t=0.15)
MAST_TUBE = dict(od=60.3, id=52.5, top_z=250)          # 2 in. sch 40 PVC, bonded hull-to-deck
BEARING = dict(id=25, od=37, w=7, name="6805-2RS stainless")
BOOM = dict(od=12.0, z=276, length=600)                # spar axis to tail pivot
TAIL = dict(chord=120, span=200, pivot_from_le=24, bot_z=300, t=0.12, pivot_d=6)

# ---- deck & stern -------------------------------------------------------
HATCH = dict(x0=330, x1=530, w=220, lid_margin=30)
SOLAR = [dict(x0=650, x1=1070, w=280), dict(x0=1080, x1=1480, w=280)]
STUB = dict(x=1530, od=20.0, bot_z=150, top_z=650)
VANE_Z = 650
ANT_Z = 560

# ---- interior -----------------------------------------------------------
BATTERY = dict(x0=780, x1=960, w=80, h=170)
EBOX = dict(x0=980, x1=1220, w=160, h=90)

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
