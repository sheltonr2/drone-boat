"""3D-printable parts, modelled in print orientation (bed = z 0). Units mm."""
import numpy as np
from sdf import *
import design as D

def teardrop(r, n=72):
    """Circle with a 45-degree pointed top so horizontal holes print without support.
    Returned in (u, v) with v = up."""
    a = np.linspace(-np.pi/4, np.pi + np.pi/4, n)   # from -45deg around the bottom... build below
    pts = [[r*np.cos(t), r*np.sin(t)] for t in np.linspace(np.pi*0.75, np.pi*2.25, n)]  # lower arc (CCW from 135 to 405 deg)
    pts.append([0, r*np.sqrt(2)])
    return np.array(pts)

def hole_x(r, x0, x1, y, z, tear=True):
    P = teardrop(r) if tear else circle_pts(r)
    return prism(P + [y, z], x0, x1, axis='x')          # x-axis prism uses (y, z)

def hole_y(r, y0, y1, x, z, tear=True):
    P = teardrop(r) if tear else circle_pts(r)
    # y-axis prism uses (z, x): rotate teardrop so the point is +z
    Q = np.c_[P[:, 1] + z, P[:, 0] + x]
    return prism(Q, y0, y1, axis='y')

def capsule_pts(len_, r, cx=0, cy=0, n=16):
    pts = []
    for sx, a0 in [(1, -90), (-1, 90)]:
        for a in np.radians(np.linspace(a0, a0 + 180, n)):
            pts.append([cx + sx*len_/2 + r*np.cos(a), cy + r*np.sin(a)])
    return np.array(pts)

PARTS = {}
def part(pid, name, qty, mat, notes, dims):
    def deco(fn):
        PARTS[pid] = dict(id=pid, name=name, qty=qty, mat=mat, notes=notes, dims=dims, build=fn)
        return fn
    return deco

# --------------------------------------------------------------- wind vane
@part("P01", "Wind-vane sensor housing", 1, "ASA or PETG, 100% walls 4",
      ["Two S608-2RS stainless bearings (8x22x7) press in from the top.",
       "AS5600 board sits on cap P03 inside the cavity; magnet on shaft end faces it.",
       "Bottom cavity is closed by cap P03, bonded with thickened epoxy."],
      {"OD": 40, "Height": 60, "Bearing seats": "2 x D22.1 x 7", "Cavity": "D32 x 34"})
def p01():
    body = cyl(20, 0, 60)
    cav = cyl(16, -1, 34)
    shaft = cyl(6, 33, 61)
    seat1 = cyl(11.05, 36, 43)
    seat2 = cyl(11.05, 53, 61)
    return diff(body, cav, shaft, seat1, seat2), ((-21, 21), (-21, 21), (0, 60))

@part("P02", "Wind-vane arm with fin and counterweight pocket", 1, "ASA or PETG",
      ["Printed upside-down: z=0 face is the top of the hub in service.",
       "Skirt (D41 inside) overlaps the housing top as a rain labyrinth.",
       "Fill the pocket with lead shot + epoxy until the arm balances on the shaft.",
       "M3 set screw (tap the D2.5 radial hole) locks the hub on the 8 mm shaft."],
      {"Arm length": "190 + 75", "Fin": "80 x 80 x 3", "Hub": "D46 x 22", "Shaft bore": "D8.1 x 9 blind"})
def p02():
    hub = cyl(23, 0, 22)
    skirt_cut = cyl(20.5, 10, 23)
    bore = cyl(4.05, 1, 11)
    arm = box(0, 190, -4, 4, 0, 8)
    fin = box(120, 200, -1.5, 1.5, 0, 80)
    cw = box(-75, 0, -9, 9, 0, 12)
    pocket = box(-70, -48, -6, 6, 2, 13)
    setscrew = hole_y(1.25, -24, 0, 0, 5)
    solid = union(hub, arm, fin, cw)
    return diff(solid, skirt_cut, bore, pocket, setscrew), ((-76, 201), (-24, 24), (0, 80))

@part("P03", "Sensor cap and stub-tube socket", 1, "ASA or PETG",
      ["Spigot (D31.6) slides into the P01 cavity; bond and seal with epoxy.",
       "Recess on top takes the AS5600 board (glue down); cable runs down the D8 hole into the 20 mm stub tube.",
       "Socket fits the 20 mm stub tube; M4 set screw (D3.3 tap hole).",
       "Printed socket-down as modelled."],
      {"Spigot": "D31.6 x 22", "Flange": "D40 x 4", "Socket": "OD28, ID20.4 x 30"})
def p03():
    socket = cyl(14, 0, 30)
    flange = cyl(20, 30, 34)
    spigot = cyl(15.8, 34, 56)
    solid = union(socket, flange, spigot)
    tube = cyl(10.2, -1, 29)
    cable = cyl(4, 28, 57)
    recess = box(-13, 13, -13, 13, 54.5, 57)
    setscrew = hole_x(1.65, 0, 15, 0, 15)
    return diff(solid, tube, cable, recess, setscrew), ((-20, 20), (-20, 20), (0, 56))

@part("P04", "Magnet holder for vane shaft", 1, "PETG",
      ["Press onto the bottom end of the 8 mm 316 shaft below the lower bearing.",
       "Glue a 6 x 2.5 mm diametric magnet (AS5600 type) into the bottom pocket.",
       "Also acts as the retaining collar that stops the shaft lifting out."],
      {"OD": 14, "Height": 10, "Magnet pocket": "D6.2 x 2.7", "Shaft bore": "D8.05 x 6.5"})
def p04():
    return diff(cyl(7, 0, 10), cyl(3.1, -1, 2.7), cyl(4.025, 3.5, 11)), ((-7, 7), (-7, 7), (0, 10))

# ------------------------------------------------------------ stern stub
@part("P05", "Antenna platform clamp", 1, "ASA",
      ["Clamps to the 20 mm stub tube at 560 mm above the hull bottom.",
       "Rev D: carries the main GPS + compass (Holybro Micro M10, potted in soft silicone, patch up), not the Iridium patch (the RockBLOCK Plus has its own). Bond it in the D42 pocket; no steel washer near the compass.",
       "Squeeze slot closed with an M4 bolt (D4.3 hole) through the ears."],
      {"Platform": "80 x 64 x 5", "Collar": "OD32, ID20.3 x 25"})
def p05():
    collar = cyl(16, 0, 25)
    plate = box(10, 90, -32, 32, 0, 5)
    rib = prism(np.array([[16, 5], [86, 5], [16, 25]]), -3, 3, axis='y') if False else \
          prism(np.array([[5, 14], [5, 86], [25, 14]]), -3, 3, axis='y')   # (z, x)
    ears = box(-30, -14, -7, 7, 0, 25)
    solid = union(collar, plate, rib, ears)
    bore = cyl(10.15, -1, 26)
    slit = box(-31, -9, -1, 1, -1, 26)
    pocket = cyl(21, -1, 1.5, c1=50, c2=0)
    bolt = hole_y(2.15, -8, 8, -23, 12.5)
    return diff(solid, bore, slit, pocket, bolt), ((-31, 91), (-33, 33), (0, 25))

@part("P06", "Transom bracket for 20 mm stub tube", 1, "ASA, 6 walls",
      ["Plate bolts to the transom with 4 x M5 316 bolts, bedded in sealant over a glass-reinforced pad.",
       "Tube bores are teardrop-shaped so they print without support.",
       "M4 set screws (D3.3 tap holes) lock the tube in both blocks."],
      {"Plate": "60 x 100 x 6", "Tube offset from transom": 32, "Blocks": "32 x 20 x 44 (x2)"})
def p06():
    plate = box(-30, 30, 0, 100, 0, 6)
    b1 = box(-16, 16, 0, 20, 0, 44)
    b2 = box(-16, 16, 80, 100, 0, 44)
    web = box(-4, 4, 0, 100, 0, 22)
    solid = union(plate, b1, b2, web)
    tube = hole_y(10.2, -1, 101, 0, 32)
    ss1 = cyl(1.65, 36, 45, c1=0, c2=10)
    ss2 = cyl(1.65, 36, 45, c1=0, c2=90)
    holes = [cyl(2.75, -1, 7, c1=sx*23, c2=yy) for sx in (-1, 1) for yy in (35, 65)]
    return diff(solid, tube, ss1, ss2, *holes), ((-31, 31), (-1, 101), (0, 44))

# ------------------------------------------------------------------- rig
@part("P07", "Mast bearing housing with catcher lands", 1, "PETG or ASA, 100% infill",
      ["Bonds into the top of the 2 in. sch 40 PVC mast tube (ID 52.5); flange rests on the tube end. Printed flange-down as modelled.",
       "Rev C4: two 6806 acetal ball bearings with glass balls (30x42x7), 130 mm apart. They cannot rust or seize, but carry only about 170 N each.",
       "Each bearing floats 0.3 mm in its seat on a 42 x 1.5 O-ring (groove in the seat). Beside each is a plain land, D30.6 x 20:",
       "above about 150 N the spar moves 0.3 mm and bears on the lands, which take wave loads of several kN. Wax or grease the lands.",
       "If you can bore Delrin, open the lands to D36 and bond in Delrin sleeves 36 x 30.6 x 20 (lower friction than the print)."],
      {"OD": 52.3, "Flange": "D66 x 5", "Length": 137, "Bearing seats": "2 x D42.6 x 7, O-ring groove D45.4 x 2.6", "Catcher lands": "2 x D30.6 x 20", "Clearance bore": "D34"})
def p07():
    solid = union(cyl(33, 0, 5), cyl(26.15, 5, 137))
    cut = [cyl(15.3, -1, 138),                 # catcher land bore D30.6 right through
           cyl(17.0, 27, 110),                 # clearance between the lands
           cyl(21.3, -1, 7), cyl(21.3, 130, 138),          # floating bearing seats D42.6
           cyl(22.7, 2.2, 4.8), cyl(22.7, 132.2, 134.8)]   # O-ring grooves D45.4
    return diff(solid, *cut), ((-33, 33), (-33, 33), (0, 137))

@part("P08", "Spar clamp with tail-boom and counterweight-arm sockets", 1, "ASA or PETG, 100% infill",
      ["Rev C: clamps the 30 mm spar just below the wing root (2 x M5 bolts through the side ears). Rev B was 25 mm.",
       "Aft socket (+x): 12 mm carbon tail boom, 40 deep. Forward socket (-x): counterweight arm, 40 deep (Rev C3: 12 mm solid fibreglass rod).",
       "Pin each tube with an M4 bolt through the D4.3 vertical holes. Both tube axes are 11 mm above the bottom face.",
       "Line the forward socket up with the wing chord: the arm must point straight at the wing's leading edge."],
      {"Collar": "OD46, ID30.2 x 40", "Boom socket (aft)": "D12.2 x 37", "Arm socket (fwd)": "D12.2 x 37",
       "Ears (side)": "24 x 22", "Overall": "126 x 62 x 40"})
def p08():
    collar = cyl(23, 0, 40)
    boss = box(16, 63, -11, 11, 0, 22)
    fboss = box(-63, -16, -11, 11, 0, 22)
    ears = box(-12, 12, 16, 39, 0, 40)
    solid = union(collar, boss, fboss, ears)
    bore = cyl(15.1, -1, 41)
    boom = hole_x(6.1, 26, 64, 0, 11)
    arm = hole_x(6.1, -64, -26, 0, 11)
    slit = box(-1, 1, 12, 40, -1, 41)
    b1 = hole_x(2.75, -13, 13, 30, 10); b2 = hole_x(2.75, -13, 13, 30, 30)
    pin = cyl(2.15, -1, 23, c1=50, c2=0)
    fpin = cyl(2.15, -1, 23, c1=-50, c2=0)
    return diff(solid, bore, boom, arm, slit, b1, b2, pin, fpin), ((-64, 64), (-24, 40), (0, 40))

def servo_cradle(x0, base_z=0):
    """Pocket for a Savox SW-1210SG (40.6 x 20.7 x 42 body) standing output-up, with tab ledge
    and slotted screw holes covering 47.5-51.5 mm tab spacing."""
    cx = x0 + 30
    blk = box(x0, x0 + 60, -15, 15, base_z, base_z + 48)
    pocket = box(cx - 20.6, cx + 20.6, -10.6, 10.6, base_z + 6, base_z + 49)
    ledge = box(cx - 28, cx + 28, -10.6, 10.6, base_z + 45, base_z + 49)
    slots = [prism(capsule_pts(4, 1.25, cx + sx * 24.75, sy * 5), base_z + 28, base_z + 46) for sx in (-1, 1) for sy in (-1, 1)]
    drain = cyl(2, base_z - 1, base_z + 7, c1=cx, c2=0)
    cable = box(x0 - 1, cx - 18, -5, 5, base_z + 6, base_z + 14)
    return blk, [pocket, ledge, drain, cable] + slots

@part("P09", "Tail servo housing (boom end)", 1, "ASA or PETG",
      ["Slides on the aft end of the 12 mm boom; pin with M4 (D4.3 hole).",
       "Rev E: holds a DFRobot magnetic-encoder servo (25 kg) output-up, potted:",
       "urethane over the case seams and cable entry, silicone round the output.",
       "The tail fin P10 bonds to the servo horn; detent P25 bonds on top, aft.",
       "Tab screw slots allow 47.5-51.5 mm tab spacing: check your servo before printing.",
       "Pocket has a D4 drain hole; cable exits through the slot toward the boom."],
      {"Overall": "92 x 30 x 48", "Servo pocket": "41.2 x 21.2 x 42", "Boom socket": "D12.2 x 28"})
def p09():
    sock = box(0, 34, -12, 12, 0, 24)
    blk, cuts = servo_cradle(32)
    solid = union(sock, blk)
    boom = hole_x(6.1, -1, 28, 0, 12)
    pin = cyl(2.15, -1, 25, c1=14, c2=0)
    return diff(solid, boom, pin, *cuts), ((-1, 93), (-16, 16), (0, 48))

def foil_prism(chord, t, z0, z1, n=70):
    xs, ys = D.naca(t, chord, n)
    return prism(np.c_[xs, ys], z0, z1, axis='z')

@part("P10", "Tail fin, lower and upper halves", 1, "PETG or ASA, 0.2 mm layers",
      ["NACA 0012, 120 mm chord, 200 mm span in two 100 mm halves printed standing up.",
       "D6.2 bore at 24 mm from the leading edge takes a 6 mm carbon pivot rod through both halves.",
       "D3.2 bore at 60 mm takes a 3 mm carbon rod to align and stiffen the joint.",
       "Lower half: 32 x 8 x 4 recess on the bottom face to bond an aluminium 25T servo horn."],
      {"Chord": 120, "Span": "2 x 100", "Thickness": 14.4, "Pivot": "D6.2 at 24 from LE"})
def p10(half="lower"):
    solid = foil_prism(120, 0.12, 0, 100)
    cuts = [cyl(3.1, -1, 101, c1=24, c2=0), cyl(1.6, -1, 101, c1=60, c2=0)]
    if half == "lower":
        cuts.append(box(24 - 10, 24 + 22, -4, 4, -1, 4))
    return diff(solid, *cuts), ((0, 120), (-8, 8), (0, 100))

# ---------------------------------------------------------------- rudder
@part("P11", "Rudder tiller arm", 2, "PETG, 100% infill",
      ["Rev C: one per rudder (two rudders). Clamps the 12 mm 316 rudder stock (M4 bolt through the ears).",
       "Cross-drill the stock 3 mm through the D3.2 hole and fit a 316 pin.",
       "Pushrod holes (D2.2) at 35, 45 and 55 mm from the stock give three throw settings."],
      {"Hub": "D26 x 16", "Arm": "65 x 12 x 6", "Stock bore": "D12.1"})
def p11():
    hub = cyl(13, 0, 16)
    arm = box(0, 65, -6, 6, 0, 6)
    ears = box(-24, -10, -8, 8, 0, 16)
    solid = union(hub, arm, ears)
    cuts = [cyl(6.05, -1, 17), box(-25, -5, -1, 1, -1, 17), hole_y(2.15, -9, 9, -18, 8),
            hole_y(1.6, -14, 14, 0, 11)] + [cyl(1.1, -1, 7, c1=r, c2=0) for r in (35, 45, 55)]
    return diff(solid, *cuts), ((-25, 66), (-14, 14), (0, 16))

@part("P12", "Rudder servo cradle (Blue Trail SER-2000)", 2, "PETG or ASA, 5 walls",
      ["Rev E: one per rudder. Holds a Blue Trail SER-2000 sealed enclosure (with a",
       "DFRobot magnetic-encoder servo inside) output-up, level with the tiller arm.",
       "Two 316 hose clamps or 20 mm straps through the slots hold the enclosure;",
       "no fixed hole pattern, so it fits whatever the unit measures.",
       "The envelope (66 x 34 x 72) is an ESTIMATE: measure your unit, set SER in",
       "design.py and rebuild before printing. Base bonds to the pocket pad."],
      {"Base": "110 x 64 x 5", "Cradle": "inside 34.8 wide x 67 long, walls 4, 40 high", "Strap slots": "2 x 22 x 3"})
def p12():
    S = D.SER; w = S['w'] + 0.8; l = S['l'] + 1.0
    base = box(-55, 55, -32, 32, 0, 5)
    walls = diff(box(-l/2 - 4, l/2 + 4, -w/2 - 4, w/2 + 4, 0, 40), box(-l/2, l/2, -w/2, w/2, 5, 41))
    slots = [box(xs - 1.5, xs + 1.5, -11, 11, -1, 41) for xs in (-l/2 - 2, l/2 + 2)]
    drain = cyl(2, -1, 6)
    cable = box(-l/2 - 5, -l/2 + 1, -6, 6, 5, 18)
    holes = [cyl(2.15, -1, 6, c1=x, c2=y) for x in (-48, 48) for y in (-25, 25)]
    return diff(union(base, walls), *slots, drain, cable, *holes), ((-56, 56), (-33, 33), (0, 40))

@part("P26", "Rudder servo arm for the 6 mm D-shaft", 2, "PETG, 100% infill",
      ["Rev E: the SER-2000 output is a 6 mm titanium D-shaft, not a 25T spline,",
       "so the C3 spline servo-saver is replaced by a spring overload link in the",
       "pushrod (D05). Clamp with an M3 316 bolt across the slit.",
       "Pushrod holes D2.2 at 20, 25 and 30 mm to match the tiller's throw."],
      {"Hub": "D20 x 12", "Bore": "D6.1 with flat at 5.5", "Arm": "36 x 10 x 5"})
def p26():
    hub = cyl(10, 0, 12)
    arm = box(0, 36, -5, 5, 0, 5)
    ears = box(-18, -7, -6, 6, 0, 12)
    solid = union(hub, arm, ears)
    bore = diff(cyl(3.05, -1, 13), box(2.5, 4, -4, 4, -2, 14))
    cuts = [bore, box(-19, -2.5, -0.75, 0.75, -1, 13), hole_y(1.65, -7, 7, -13, 6)] + [cyl(1.1, -1, 6, c1=r, c2=0) for r in (20, 25, 30)]
    return diff(solid, *cuts), ((-19, 37), (-11, 11), (0, 12))

@part("P13", "Rudder blade core, upper and lower halves", 2, "PETG, 15% gyroid",
      ["Rev C: two blades (print two of each half). NACA 0012, 120 mm chord; each half 115 mm, printed standing up.",
       "Slide both halves on the 12 mm 316 stock, pin each with a 4 mm 316 pin (D4.2 holes), fill the joint with epoxy.",
       "Sand, then laminate 2 layers of 6 oz glass over the whole blade.",
       "Stock sits 22 mm behind the leading edge (about 15% balance area)."],
      {"Chord": 120, "Span": "2 x 115", "Stock bore": "D12.2 at 22 from LE"})
def p13(half="upper"):
    solid = foil_prism(120, 0.12, 0, 115)
    cuts = [cyl(6.1, -1, 116, c1=22, c2=0), hole_y(2.1, -10, 10, 22, 57, tear=False)]
    return diff(solid, *cuts), ((0, 120), (-8, 8), (0, 115))

# ---------------------------------------------------------------- keel bulb pattern
@part("P14", "Keel bulb casting pattern, forward and aft halves", 1, "PLA or PETG, 3 walls",
      ["Pattern for a plaster or sand mould: do NOT pour lead into the print.",
       "Halves split at 160 mm; join with two 4 mm dowels (D4.2 holes) and fill/sand smooth.",
       "Slot on top matches the fin tip (NACA 0012, 150 mm chord), 15 mm deep.",
       "Rev C: 72 mm diameter (was 68). Finished lead bulb about 9.2 kg; allow 1-2% for shrinkage when sizing the mould."],
      {"Length": 320, "Max diameter": 72, "Fin slot": "150 x 18 x 15"})
def p14(half="fwd"):
    Lb = D.BULB['length']; R = D.bulb_radius
    split = 160.0
    slot_le = D.FIN['tip_le_x'] - D.BULB['nose_x']   # 91 mm from nose
    xs, ys = D.naca(0.12, 150, 120)
    def slot_half(xl):
        u = np.clip(xl - slot_le, 0, 150)
        return np.interp(u, xs[:len(xs)//2+1][::-1], ys[:len(xs)//2+1][::-1]) * ((xl >= slot_le) & (xl <= slot_le + 150))
    def f(X, Y, Z):
        xl = (split - Z) if half == "fwd" else (split + Z)   # bulb station
        xlc = np.clip(xl, 0, Lb)
        r = R(xlc)
        rr = np.sqrt(X**2 + Y**2)
        d = rr - r
        d = np.maximum(d, -Z)                               # cut face at z=0
        d = np.maximum(d, Z - (split if half == "fwd" else Lb - split))
        hs = slot_half(xlc)
        slot = np.maximum(np.abs(Y) - hs, (r - 15) - X)     # region near +X top
        slot = np.where(hs > 0.2, slot, 1.0)
        d = np.maximum(d, -slot)
        for dy in (-12, 12):
            dw = np.maximum(np.sqrt((X + 10)**2 + (Y - dy)**2) - 2.1, Z - 12)
            d = np.maximum(d, -dw)
        return d
    h = split if half == "fwd" else Lb - split
    return f, ((-37, 37), (-37, 37), (0, h))

# ---------------------------------------------------------------- interior
@part("P15", "Electronics tray", 1, "PETG",
      ["Sits inside the IP68 enclosure; trim the outline to your enclosure's inside size.",
       "Mount boards with 3M Dual Lock and zip ties through the 4 x 2.5 mm slot pairs (no hole patterns are assumed).",
       "Corner slots take M3 screws into the enclosure's mounting bosses."],
      {"Plate": "200 x 130 x 3", "Rim": "3 high", "Zip slots": "4 x 2.5 on a 25 mm grid"})
def p15():
    plate = box(-100, 100, -65, 65, 0, 3)
    rim = diff(box(-100, 100, -65, 65, 0, 6), box(-97, 97, -62, 62, 2.9, 7))
    cuts = []
    for x in np.arange(-75, 76, 25):
        for y in np.arange(-37.5, 38, 25):
            for dy in (-4, 4):
                cuts.append(box(x - 2, x + 2, y + dy - 1.25, y + dy + 1.25, -1, 4))
    for sx in (-1, 1):
        for sy in (-1, 1):
            cuts.append(prism(capsule_pts(6, 1.7, sx * 90, sy * 55), -1, 7))
    return diff(union(plate, rim), *cuts), ((-101, 101), (-66, 66), (0, 6))

@part("P16", "Battery strap anchor", 4, "PETG",
      ["Rev C: bond to the hull floor around the sealed battery box; the straps hold the box (the battery is wedged inside it).",
       "Use two straps with cam buckles; strap tension holds the battery against capsize loads."],
      {"Base": "60 x 24 x 3", "Webbing slot": "28 x 4"})
def p16():
    base = box(-30, 30, -12, 12, 0, 3)
    block = box(-18, 18, -12, 12, 0, 11)
    slot = box(-14, 14, -13, 13, 3, 7)
    return diff(union(base, block), slot), ((-31, 31), (-13, 13), (0, 11))

@part("P17", "Penetrator boss pad", 4, "ASA or PETG, 100% infill",
      ["Gives each Blue Robotics WetLink M10 penetrator a flat, thick seat on the curved deck or hull.",
       "Bond with thickened epoxy, drill through the hull using the D10.5 hole as a guide."],
      {"OD": 40, "Height": 10, "Hole": "D10.5"})
def p17():
    return diff(cyl(20, 0, 10), cyl(5.25, -1, 11)), ((-20, 20), (-20, 20), (0, 10))

@part("P18", "Wing counterweight pod", 1, "PETG or ASA, 4 walls, 40% infill",
      ["Balances the rotating wing, tail and boom on the spar axis (Rev B; unchanged in Rev C).",
       "Sits on the forward end of the 12 mm arm (Rev C3: solid fibreglass rod); pod axis 300 mm forward of the spar axis. Pin with M4 (D4.3 hole).",
       "Fill the open top with lead shot + epoxy (about 0.8 kg, roughly 115 cm3) a little at a time,",
       "until the assembled rig balances level on the spar with the tail at 0 deg. Cap the top with epoxy.",
       "Capacity about 175 cm3 (about 1.2 kg) leaves room if the tail parts come out heavier."],
      {"Body": "OD64 x 74", "Cavity": "D56 x 71 open top", "Arm socket": "D12.2 x 28 blind", "Socket axis": "12 above base"})
def p18():
    body = cyl(32, 0, 74)
    boss = box(26, 60, -11, 11, 0, 28)
    solid = union(body, boss)
    cav = cyl(28, 3, 75)
    sock = hole_x(6.1, 32, 61, 0, 12)
    pin = cyl(2.15, -1, 29, c1=46, c2=0)
    return diff(solid, cav, sock, pin), ((-33, 61), (-33, 33), (0, 74))

# ---------------------------------------------------------------- Rev C stub fittings
@part("P19", "Backup tracker (YB3) deck cradle", 1, "ASA, 5 walls, 40% infill",
      ["Rev C3: the YB3 sits in a 38 mm deep well in the foredeck, centred at x 180, not on the stern post, so a bent post cannot take the backup tracker with it.",
       "Bond the plate to the floor of the well with thickened epoxy and add two M5 316 bolts (D5.3 holes, countersink by hand) with sealant and backing washers.",
       "Strap the YB3 down with two 316 hose clamps or 20 mm webbing through the four slots; the end lips stop it sliding.",
       "The YB3 size here is approximate: check your unit before printing."],
      {"Plate": "170 x 100 x 5", "End lips": "2 x 86 x 4 x 8 high", "Strap slots": "4 x 24 x 5", "Bolt holes": "2 x D5.3"})
def p19():
    plate = box(-85, 85, -50, 50, 0, 5)
    lips = union(box(-81, -77, -43, 43, 5, 13), box(77, 81, -43, 43, 5, 13))
    solid = union(plate, lips)
    slots = [box(xc - 12, xc + 12, sy * 46 - 2.5, sy * 46 + 2.5, -1, 6) for xc in (-45, 45) for sy in (-1, 1)]
    bolts = [cyl(2.65, -1, 6, c1=xc, c2=0) for xc in (-55, 55)]
    return diff(solid, *slots, *bolts), ((-86, 86), (-51, 51), (0, 13))

@part("P20", "Navigation light clamp", 1, "ASA",
      ["Rev C: clamps the stub at z 600, below the vane; holds a 30 mm all-round white LED puck 45 mm aft of the stub.",
       "Cable runs down the D5 hole and along the groove into the stub through a 6 mm hole drilled in the tube.",
       "The controller switches the light on at night (about 0.3 W). Squeeze slot closed with an M4 bolt."],
      {"Collar": "OD32, ID20.3 x 20", "Puck seat": "D30.5 x 5 deep", "Reach": 45})
def p20():
    collar = cyl(16, 0, 20)
    arm = box(10, 50, -9, 9, 0, 9)
    seat = cyl(18, 0, 10, c1=45, c2=0)
    ears = box(-30, -14, -7, 7, 0, 20)
    solid = union(collar, arm, seat, ears)
    bore = cyl(10.15, -1, 21)
    pocket = cyl(15.25, 5, 11, c1=45, c2=0)
    cable = cyl(2.5, -1, 6, c1=45, c2=0)
    groove = box(12, 45, -2, 2, -1, 3)
    slit = box(-31, -9, -1, 1, -1, 21)
    bolt = hole_y(2.15, -8, 8, -23, 10)
    return diff(solid, bore, pocket, cable, groove, slit, bolt), ((-31, 64), (-19, 19), (0, 20))

# ---------------------------------------------------------------- Rev D electronics
@part("P21", "Limp-home controller case (potting shell)", 1, "PETG, 4 walls, 100% infill on the back",
      ["Rev D (docs/Limp_Home_Spec.md). Bond the back to the aft face of",
       "bulkhead x 300, top edge 10 mm under the deck, clear of the hatch opening.",
       "Print back-down. ESP32, 6 V regulator, opto-isolators and supervisor",
       "on the floor; GPS and BNO085 face-up on the shelf under the top wall.",
       "Pot in two pours: soft silicone round the GPS and BNO085, then",
       "urethane to the rim. Cables out through the D8 holes (drip loop).",
       "Pot only after Bench Test N. Updates over Wi-Fi: no connector inside."],
      {"Case": "96 x 66 x 30", "Walls": "2.5 (top 2.0)", "GPS shelf": "38 wide, 12 under the top", "Cable holes": "2 x D8", "Ears": "2 x D5.3"})
def p21():
    shell = box(-48, 48, -33, 33, 0, 30)
    cav = box(-45.5, 45.5, -30.5, 31, 3, 31)
    shelf = box(-19, 19, 17, 19, 3, 27)
    ears = box(-62, 62, -8, 8, 0, 3)
    solid = union(diff(shell, cav), shelf, ears)
    cables = [hole_y(4, -34, -29, xc, 15) for xc in (-20, 20)]
    bolts = [cyl(2.65, -1, 4, c1=xc, c2=0) for xc in (-55, 55)]
    return diff(solid, *cables, *bolts), ((-63, 63), (-34, 34), (0, 30))

@part("P22", "Servo switchover pod (potting shell)", 1, "PETG",
      ["Rev D: holds the 4-channel servo multiplexer and two ideal-diode",
       "boards for the starboard rudder and tail servos. Bond to the forward",
       "face of bulkhead x 1260, high, beside the servo WetLink.",
       "Pot to the rim with urethane after Bench Test N.",
       "Cable holes: main box, limp-home controller, servos."],
      {"Case": "50 x 40 x 22", "Walls": "2.5", "Cable holes": "3 x D7", "Ears": "2 x D4.3"})
def p22():
    shell = box(-25, 25, -20, 20, 0, 22)
    cav = box(-22.5, 22.5, -17.5, 17.5, 3, 23)
    ears = box(-34, 34, -7, 7, 0, 3)
    solid = union(diff(shell, cav), ears)
    cables = [hole_y(3.5, -21, -16, xc, 12) for xc in (-12, 0, 12)]
    bolts = [cyl(2.15, -1, 4, c1=xc, c2=0) for xc in (-29, 29)]
    return diff(solid, *cables, *bolts), ((-35, 35), (-21, 21), (0, 22))

@part("P23", "RockBLOCK Plus bowl (hatch lid)", 1, "ASA, 5 walls, 40% infill",
      ["Rev D: seats the RockBLOCK Plus (137 x 40) in the hatch lid, its",
       "top 2 mm proud of the flange and below z 255 (counterweight pod sweep).",
       "Cut D146 in the lid (T16); bed the flange in thickened epoxy, then one",
       "6 oz tape over the flange onto the lid. Print floor-down: the flange",
       "is chamfered underneath, so no supports.",
       "Bolt the puck through the four slots into its M5 inserts (check the",
       "pattern on your unit). M20 IP68 cable gland in the centre hole.",
       "Soft sealant fillet round the top of the puck: no standing water."],
      {"Flange": "OD166 x 3, 45 deg chamfer under", "Bowl": "ID141 x 38 deep, wall 2.5", "Floor": "5 thick, D20.5 gland hole", "Bolt slots": "4 x 5.5 wide, r 40-62"})
def p23():
    rf = lambda w: np.where(w < 30, 73.0, np.where(w < 40, 73.0 + (w - 30), 83.0))
    outer = revolve(rf, 0, 43, axis='z')
    solid = diff(outer, cyl(70.5, 5, 44))
    gland = cyl(10.25, -1, 6)
    slots = []
    for a in np.radians([45, 135, 225, 315]):
        c, sn = np.cos(a), np.sin(a)
        pts = capsule_pts(22, 2.75)
        R = np.c_[pts[:, 0] * c - pts[:, 1] * sn, pts[:, 0] * sn + pts[:, 1] * c] + [51 * c, 51 * sn]
        slots.append(prism(R, -1, 6))
    return diff(solid, gland, *slots), ((-84, 84), (-84, 84), (0, 43))

# ---------------------------------------------------------------- Rev E leaks, servos, weed
@part("P24", "Bilge pump spacer (mast tube)", 1, "PETG, 5 walls, 40% infill",
      ["Rev E: holds the 12 V diaphragm pump (D28 motor) upright against the port",
       "side of the 2 in. PVC mast tube, above the sump. Bond with thickened epoxy",
       "(scuff the PVC), then a 316 band clamp round tube, spacer and pump at the",
       "top and bottom of the spacer (grooves). Pump head down, inlet at the bottom.",
       "Pick-up hose to a strainer at the sump's low point (x 600, centreline);",
       "outlet up to a loop under the deck, check valve, deck fitting (D03, D08).",
       "Print standing on end as modelled: no supports."],
      {"Faces": "R30.4 (tube OD 60.3) and R14.3 (pump D28)", "Size": "32 x 26 x 50", "Clamp grooves": "2 x 13 wide x 1.5 deep"})
def p24():
    body = box(-16, 16, 24, 50, 0, 50)
    tube = cyl(30.4, -1, 51)
    pump = cyl(14.3, -1, 51, c1=0, c2=52)
    grooves = [diff(box(-17, 17, 23, 51, zg, zg + 13), box(-14.5, 14.5, 22, 52, zg - 1, zg + 14)) for zg in (4, 33)]
    return diff(body, tube, pump, *grooves), ((-17, 17), (23, 51), (0, 50))

@part("P25", "Tail detent magnet carrier", 1, "PETG, 100% infill",
      ["Rev E: a tail servo that fails free kills the boat; this makes it fail at",
       "+/-8 deg. Bond on top of P09, aft of the servo output, centred on it.",
       "Two 6 x 3 N52 magnets (epoxied, same pole up) in the pockets at r 30, +/-8 deg.",
       "A 6 x 1 steel disc in the underside of the fin P10, at r 30 on the fin's",
       "chord line, is pulled to the nearer magnet when the servo lets go.",
       "Check a 1.5 mm gap to the fin; the powered servo overcomes the pull easily."],
      {"Sector": "r 18-38, +/-14 deg, 5 thick", "Magnet pockets": "2 x D6.2 x 3.2 at r 30, +/-8 deg"})
def p25():
    a = np.radians(np.linspace(-14, 14, 29))
    P = np.r_[np.c_[18 * np.cos(a), 18 * np.sin(a)], np.c_[38 * np.cos(a[::-1]), 38 * np.sin(a[::-1])]]
    solid = prism(P, 0, 5)
    pk = [cyl(3.1, 1.8, 6, c1=30 * np.cos(np.radians(t)), c2=30 * np.sin(np.radians(t))) for t in (-8, 8)]
    return diff(solid, *pk), ((17, 39), (-10, 10), (0, 5))

# build list: (file stem, part id, builder kwargs)
BUILD = [("P01_vane_housing", "P01", {}), ("P02_vane_arm", "P02", {}), ("P03_sensor_cap", "P03", {}),
         ("P04_magnet_holder", "P04", {}), ("P05_antenna_platform", "P05", {}), ("P06_transom_bracket", "P06", {}),
         ("P07_mast_bearing_housing", "P07", {}), ("P08_spar_clamp_two_sockets", "P08", {}),
         ("P09_tail_servo_housing", "P09", {}), ("P10a_tail_fin_lower", "P10", {"half": "lower"}),
         ("P10b_tail_fin_upper", "P10", {"half": "upper"}), ("P11_tiller_arm", "P11", {}),
         ("P12_rudder_servo_cradle", "P12", {}), ("P13a_rudder_core_upper", "P13", {"half": "upper"}),
         ("P13b_rudder_core_lower", "P13", {"half": "lower"}), ("P14a_bulb_pattern_fwd", "P14", {"half": "fwd"}),
         ("P14b_bulb_pattern_aft", "P14", {"half": "aft"}), ("P15_electronics_tray", "P15", {}),
         ("P16_battery_strap_anchor_x4", "P16", {}), ("P17_penetrator_pad_x4", "P17", {}), ("P18_counterweight_pod", "P18", {}),
         ("P19_yb3_platform", "P19", {}), ("P20_nav_light_clamp", "P20", {}),
         ("P21_limp_home_case", "P21", {}), ("P22_switchover_pod", "P22", {}), ("P23_rockblock_plus_bowl", "P23", {}),
         ("P24_bilge_pump_spacer", "P24", {}), ("P25_tail_detent", "P25", {}), ("P26_rudder_servo_arm", "P26", {})]
