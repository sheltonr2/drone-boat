"""Rev E2 (DFM) sheets: D30 wiring, D31 composites and build sequence, D32 hardware and steering linkage,
D33 3D-printing guide. Imported by drawings.py; run drawings.py to rebuild Drawings.pdf."""
import csv, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
import design as D
import parts as Pm
from sheet import *

HERE = os.path.dirname(os.path.abspath(__file__))
RED = "#b3261e"; GRN = "#2e7d32"; ORG = "#c25e00"; PUR = "#6a3d9a"

def blk(bg, x, y, w, h, title, lines=(), fc="#f6f8fb", ec=INK, fs=5.2, tfs=6.0):
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=0.6))
    bg.text(x + 1.5, y + h - 2.2, title, fontsize=tfs, weight="bold", va="top")
    yy = y + h - 2.2 - tfs * 0.55 - 0.8
    for ln in lines:
        bg.text(x + 1.5, yy, ln, fontsize=fs, va="top"); yy -= fs * 0.5
    return (x, y, w, h)

def wire(bg, pts, color=INK, lw=0.7, label=None, at=0, dx=1.0, dy=1.0, fs=4.6, ls="-"):
    p = np.array(pts, float)
    bg.plot(p[:, 0], p[:, 1], color=color, lw=lw, ls=ls, solid_capstyle="round")
    bg.plot(*p[-1], marker="o", ms=1.6, color=color)
    if label:
        a = p[at]; b = p[at + 1]; m = (a + b) / 2
        bg.text(m[0] + dx, m[1] + dy, label, fontsize=fs, color=color, ha="left", va="bottom",
                bbox=dict(fc="white", ec="none", pad=0.15))

# ------------------------------------------------------------------ D30 wiring
def sheet_wiring(pdf):
    fig, bg = new_sheet("D30", "Electrical wiring diagram (F)", "Not to scale")
    bg.text(12, 268, "POWER AND SIGNAL BLOCK DIAGRAM", fontsize=8, weight="bold", va="top")
    bg.text(12, 263.5, "Red = 12.8 V battery   Orange = 6 V servo   Green = 5 V / 3.3 V logic   Blue = signal / data   Purple = isolated (optocoupler)",
            fontsize=5.4, va="top")
    # left column: energy
    blk(bg, 12, 232, 46, 22, "SOLAR (deck, D08)", ["2 x PV Logic 10 W ETFE (E3), 20 W", "wired in parallel at a potted", "junction under the deck", "One cable in through W1"])
    blk(bg, 12, 203, 46, 22, "GENASUN GV-5-Li-14.2V", ["MPPT, 5 A, in the main box", "PV in  <-  solar (W1)", "BAT out -> F0 -> battery", "Load out: not used"])
    blk(bg, 12, 150, 58, 46, "BATTERY BOX (sealed, D09)", ["Bioenno BLF-1215A 12.8 V 15 Ah", "F0  7.5 A  charge (GV-5 lead)", "F1  10 A  main feed -> main box", "F2  2 A  limp-home feed -> P21", "Fuses at the terminal, inside the box", "Exits: W7 (main + charge, 14 AWG)", "          W8 (limp-home, 18 AWG)"], fc="#fff4f2")
    # main box
    bg.add_patch(Rectangle((80, 150), 186, 106, fc="#fbfbf3", ec=INK, lw=0.9, ls="--"))
    bg.text(82, 254, "MAIN BOX  Hammond 1554V2GYCL on the shelf, x 980-1220 (D03); cables in through its lid glands", fontsize=6, weight="bold", va="top")
    blk(bg, 84, 156, 34, 90, "FUSE BLOCK", ["12.8 V bus from F1", "", "F3  7.5 A  6 V servo reg", "F4  3 A  Pixhawk switch", "F5  1 A  5 V logic reg", "F6  1 A  RockBLOCK 9704", "F7  2 A  bilge pump sw.", "F8  1 A  nav light sw.", "", "All ATC blades,", "waterproof holders,", "potted after the", "shakedown"], fc="#fff4f2")
    blk(bg, 124, 228, 30, 16, "6 V REG #1", ["Pololu D36V50F6", "5.5 A servo rail"], fc="#fff6ea")
    blk(bg, 158, 228, 34, 16, "INA260 x 2", ["one per rudder feed", "I2C to companion"], fc="#fff6ea")
    blk(bg, 124, 208, 68, 15, "LOAD SWITCH  ->  PM02 V3", ["companion can power-cycle the Pixhawk", "PM02: 5.2 V to POWER1, V/I sense"], fc="#eef6ee")
    blk(bg, 124, 160, 44, 44, "PIXHAWK 6C MINI", ["GPS1   <- Micro M10 (P05)", "TELEM1 <-> companion", "ADC 3.3 <- AS5600 OUT", "OUT1 -> P22 M1 (stbd rud.)", "OUT2 -> port rudder", "OUT3 -> P22 M2 (tail)", "POWER1 <- PM02", "Conformal coat only"], fc="#eef3fb")
    blk(bg, 172, 160, 44, 44, "COMPANION ESP32-S3", ["5 V from D36V6F5 (F5)", "UART1 <-> MAX3232", "UART2 <-> Pixhawk TELEM1", "UART0 <-> camera (F)", "I2C: BME280, INA260 x2", "GPIO: leak, pump, light, cam,", "  solar cut-off, PX4 power", "Heartbeat out -> opto", "Takeover flag in <- opto"], fc="#eef3fb")
    blk(bg, 220, 226, 42, 18, "MAX3232 + GV-5", ["RS-232 <-> 3.3 V UART", "GV-5 sits beside it"], fc="#eef3fb")
    blk(bg, 220, 196, 42, 26, "LOAD SWITCHES x4", ["MOSFET boards: pump (F7),", "light (F8), solar cut-off", "below 2 C (GV-5 to PV);", "F: camera 5 V (from F5)"], fc="#fff4f2")
    blk(bg, 220, 160, 42, 32, "LEAK HOST + PROBES", ["Blue Robotics SOS", "probes: sump (x 600-770)", "and box floor", "signal -> companion GPIO", "BME280 on bulkhead x 300", "(I2C, 0.7 m cable)"], fc="#eef3fb")
    # right side: outside the box
    blk(bg, 290, 232, 58, 22, "ROCKBLOCK PLUS 9704 (P23) - F", ["7-30 V from F6; <2 W tx, 6.7 W inrush 30 s", "RS-232 (Iridium port) to MAX3232", "GNSS RS-232 port: spare", "M20 gland in the bowl, drip loop"], fc="#eef3fb")
    blk(bg, 290, 196, 58, 30, "STERN STUB (D07) via W2, W3", ["W2 6-core: M10 GPS + compass (P05),", "  AS5600 vane (P03) analog OUT", "W3 6-core (F): nav light (P20, F8)", "  + camera P29: switched 5 V, GND,", "  UART TX/RX (XIAO ESP32S3 Sense)"], fc="#eef3fb")
    blk(bg, 290, 150, 58, 40, "SWITCHOVER POD P22 (x 1260)", ["Pololu 4-ch servo mux #2806", "  M1/M2 <- Pixhawk OUT1/OUT3", "  S1/S2 <- P21; SEL <- P21", "  FAILMODE = master", "2 x ideal-diode pair #5398:", "  6 V main + 6 V limp-home", "  -> stbd rudder and tail"], fc="#fff6ea")
    blk(bg, 356, 222, 60, 32, "RUDDER SERVOS (aft space)", ["SER-2000 + DFRobot SER0066 x 2", "Port: Pixhawk OUT2, main 6 V", "Stbd: from P22", "Cables through W5, W6", "(bulkhead x 1260), 18 AWG"], fc="#fff6ea")
    blk(bg, 356, 186, 60, 30, "TAIL SERVO (P09, on the boom)", ["DFRobot SER0066, potted", "From P22 through the slip ring", "(spar foot, inside the mast tube)", "Mast-tube wall to dry bay: W4"], fc="#fff6ea")
    blk(bg, 356, 150, 60, 30, "BILGE PUMP (P24, mast tube)", ["12 V R385 diaphragm pump", "From F7 load switch", "Run time logged as leak meter", "18 AWG"], fc="#fff4f2")
    blk(bg, 290, 110, 126, 34, "LIMP-HOME CONTROLLER P21 (bulkhead x 300), own feed F2 via W8", ["ESP32-S3 Feather (5 V from D36V6F5 #2)    Micro M10 GPS (switched)    BNO085 (I2C)    supervisor / watchdog IC",
        "6 V REG #2 (D36V50F6) -> P22 ideal diodes      PWM -> P22 S1 (stbd rudder), S2 (tail), SEL",
        "Heartbeat in and takeover flag out through 2 x 6N137 optocouplers: no copper path between the two systems' grounds",
        "Pot only after Bench Test N (docs/Limp_Home_Spec.md)"], fc="#f4effa")
    # wires
    wire(bg, [(35, 232), (35, 225)], RED, label="PV 16 AWG", dx=1)
    wire(bg, [(35, 203), (35, 196)], RED, label="F0 7.5 A", dx=1)
    wire(bg, [(70, 180), (84, 180)], RED, lw=1.1, label="F1 14 AWG", dx=-12, dy=1)
    wire(bg, [(70, 160), (76, 160), (76, 128), (290, 128)], RED, label="F2 18 AWG, own cable", at=2, dx=-60)
    wire(bg, [(118, 236), (124, 236)], RED)
    wire(bg, [(154, 236), (158, 236)], ORG, lw=1.0)
    wire(bg, [(192, 238), (200, 238), (200, 248), (356, 248)], ORG, lw=1.0, label="6 V rail, 18 AWG: port rudder direct", at=2, dx=-110, dy=0.8)
    wire(bg, [(200, 238), (283, 238), (283, 182), (290, 182)], ORG, lw=1.0)
    wire(bg, [(348, 176), (352, 176), (352, 238), (356, 238)], ORG, lw=1.0, label="stbd", at=1, dx=1, dy=-8)
    wire(bg, [(352, 200), (356, 200)], ORG, lw=1.0)
    wire(bg, [(118, 215), (124, 215)], RED)
    wire(bg, [(158, 208), (158, 204)], GRN)
    wire(bg, [(118, 170), (122, 170), (122, 156), (194, 156), (194, 160)], GRN, label="F5 -> 5 V", at=2, dx=-25, dy=-4)
    wire(bg, [(168, 190), (172, 190)], BLUE, label="MAVLink", dx=-8, dy=1.5, fs=4.2)
    wire(bg, [(216, 196), (220, 196)], BLUE)
    wire(bg, [(216, 232), (220, 232)], BLUE)
    wire(bg, [(262, 236), (276, 236), (276, 243), (290, 243)], BLUE, label="RS-232", at=2, dx=-2, dy=1)
    wire(bg, [(118, 225), (121, 225), (121, 259), (279, 259), (279, 248), (290, 248)], RED, label="F6 1 A to RockBLOCK", at=2, dx=-60, dy=0.3)
    wire(bg, [(146, 204), (146, 206), (286, 206), (286, 211), (290, 211)], BLUE, label="GPS1 + AS5600 analog (W2)", at=1, dx=-55, dy=0.8)
    wire(bg, [(262, 200), (270, 200), (270, 146), (386, 146), (386, 150)], RED, label="F7 pump", at=2, dx=-20, dy=-4.2)
    wire(bg, [(262, 204), (272, 204), (272, 200), (290, 200)], RED, label="F8 light (W3)", at=2, dx=-17, dy=0.5)
    wire(bg, [(146, 160), (146, 154), (300, 154), (300, 150)], BLUE, label="OUT1, OUT3 -> P22 M1, M2", at=1, dx=-50, dy=0.5)
    wire(bg, [(194, 160), (194, 158)], PUR)
    wire(bg, [(216, 166), (218, 166), (218, 140), (290, 140)], PUR, lw=0.8, ls="--", label="heartbeat / takeover (opto)", at=2, dx=-55, dy=0.5)
    wire(bg, [(330, 144), (330, 150)], BLUE, label="S1, S2, SEL", dx=1, dy=-4)
    wire(bg, [(320, 144), (320, 150)], ORG, lw=1.0)
    bg.text(321.5, 146, "6 V #2", fontsize=4.4, color=ORG)
    # tables
    fz = [["F0", "7.5 A", "battery box", "GV-5 battery lead", "16 AWG"],
          ["F1", "10 A", "battery box", "main feed to box", "14 AWG"],
          ["F2", "2 A", "battery box", "P21 limp-home feed", "18 AWG"],
          ["F3", "7.5 A", "main box", "6 V servo regulator #1", "16 AWG"],
          ["F4", "3 A", "main box", "Pixhawk load switch, PM02", "18 AWG"],
          ["F5", "1 A", "main box", "5 V logic reg (companion)", "22 AWG"],
          ["F6", "1 A", "main box", "RockBLOCK Plus 9704, slow-blow", "18 AWG"],
          ["F7", "2 A", "main box", "bilge pump switch", "18 AWG"],
          ["F8", "1 A", "main box", "nav light switch", "22 AWG"]]
    bg.text(12, 104, "FUSES", fontsize=7, weight="bold")
    table(bg, 12, 102, ["Ref", "Rating", "Where", "Feeds", "Wire"], fz, [9, 11, 20, 44, 13], fs=5.0, rh=3.8)
    pz = [["W1", "deck, solar bay 1", "solar pair, 2-core", "deck (P17 pad)"],
          ["W2", "transom, stub foot", "6-core: GPS, vane", "transom (P17)"],
          ["W3", "transom, stub foot", "light + camera, 6-core", "transom (P17)"],
          ["W4", "mast tube wall", "slip ring, 3-core", "PVC tube (P17)"],
          ["W5", "bulkhead x 1260", "stbd rudder servo", "flat foam/glass"],
          ["W6", "bulkhead x 1260", "port rudder servo", "flat foam/glass"],
          ["W7", "battery-box wall", "main + charge", "box wall"],
          ["W8", "battery-box wall", "limp-home feed", "box wall"],
          ["gland", "P23 bowl centre", "RockBLOCK 9704 cable", "M20 IP68 gland"]]
    bg.text(116, 104, "PENETRATIONS (WetLink M10 unless noted)", fontsize=7, weight="bold")
    table(bg, 116, 102, ["Ref", "Through", "Cable", "Seat"], pz, [9, 31, 30, 27], fs=5.0, rh=3.8)
    nz = ["1. Wire: tinned marine wire only. Crimp + adhesive heat-shrink, then pot joint clusters (Potting_Spec).",
          "2. Every board conformal-coated; Pixhawk masked (connectors, baro port, SD slot). Locking connectors only.",
          "3. Drip loop on every cable before its penetration; seal size chosen to the measured cable OD.",
          "4. Pin numbers are assigned in firmware; this sheet fixes what connects to what, not GPIO numbers.",
          "5. Bench-test the whole harness on the bench (Tests N, I) before anything is potted.",
          "6. E2 (DFM) additions: two 5 V logic regulators (neither ESP32 had one), a Pixhawk power",
          "   switch so the companion can power-cycle it, and W7/W8 for the battery-box exits.",
          "7. Ground: one star point at the main-box bus; the P21 side shares only the battery negative.",
          "8. Rev F: the camera has its own 5 V load switch; with it off, a fault in the camera or its cable",
          "   cannot reach the companion. The camera talks only to the companion, never to the modem."]
    notes(bg, 218, 104, "Wiring notes", nz, fs=5.2, lh=3.3)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D31 composites
def laminate_rows():
    """(item, core, plies out, plies in, area m2 per face, cloth m2) from design.py geometry."""
    xs = np.linspace(0, D.L, 601)
    per = []
    for x in xs:
        y, z = D.section(x, 200); per.append(2 * np.sum(np.hypot(np.diff(y), np.diff(z))))
    hull = np.trapezoid(per, xs) / 1e6
    deck = np.trapezoid([2 * float(D.half_beam(x)) for x in xs], xs) / 1e6
    def sec(x):
        y, z = D.section(x, 200); return 2 * np.trapezoid(y, z) / 1e6
    bh = sec(300) + sec(1260)
    fin = (D.FIN['root_chord'] + D.FIN['tip_chord']) / 2 * abs(D.FIN['tip_z']) * 2 / 1e6
    rud = D.RUDDER['chord'] * (D.RUDDER['top_z'] - D.RUDDER['bot_z']) * 2 * 2 / 1e6
    wing = D.WING['chord'] * D.WING['span'] * 2 * 1.04 / 1e6
    B = D.BATTBOX; bb = 2 * ((B['x1'] - B['x0']) * B['w'] + (B['x1'] - B['x0']) * (B['z1'] - B['z0']) + B['w'] * (B['z1'] - B['z0'])) / 1e6
    R = [("Hull shell", "10 mm H80 strips over frames", 2, 1, hull),
         ("Deck", "10 mm H80 sheet", 2, 1, deck),
         ("Transom", "10 mm H80", 2, 1, sec(D.L)),
         ("Bulkheads x 300, x 1260 (T17, T18)", "10 mm H80", 2, 2, bh),
         ("Hull doubler, x 650-800 (keel box)", "-", 0, 3, 0.05),
         ("Sump second ply, x 560-770", "-", 0, 1, 0.07),
         ("Keel fin (T12, T13)", "hardwood + carbon strip", 6, 6, fin / 2),
         ("Floors x 650, x 800 (T19, T20)", "9 mm marine ply", 2, 2, 0.03),
         ("Rudder blades x 2 (T14)", "printed cores P13", 2, 0, rud),
         ("Wing (T15)", "XPS, 3 mm ply caps", 2, 0, wing),
         ("Battery box", "10 mm H80", 2, 1, bb),
         ("Hatch frame doubler, lid, YB3 well", "6 mm foam / G10", 2, 1, 0.15),
         ("Weed fairing (T21)", "XPS", 2, 0, 0.03)]
    out = []
    for name, core, po, pi, a in R:
        cloth = a * (po + pi) if name != "Keel fin (T12, T13)" else a * 2 * 6
        out.append([name, core, po, pi, round(a, 3), round(cloth, 2)])
    return out

def sheet_composites(pdf):
    fig, bg = new_sheet("D31", "Laminate schedule and build sequence (E2)", "Strongback 1:8")
    rows = laminate_rows()
    tot = sum(r[5] for r in rows)
    bg.text(12, 268, "LAMINATE SCHEDULE  (6 oz = about 200 g/m2 E-glass plain weave; West 105/205 epoxy)", fontsize=7, weight="bold", va="top")
    trows = [[r[0], r[1], r[2], r[3], f"{r[4]:.3f}", f"{r[5]:.2f}"] for r in rows]
    trows.append(["TOTAL cloth (add 15% for overlaps and waste)", "", "", "", "", f"{tot:.1f} -> {tot*1.15:.1f}"])
    yb = table(bg, 12, 264, ["Item", "Core", "Plies out", "Plies in", "Area m2/face", "Cloth m2"], trows, [66, 42, 15, 14, 20, 24], fs=5.2, rh=3.9)
    glass_kg = tot * 1.15 * 0.2
    lines = [f"Cloth: about {tot*1.15:.1f} m2, about {tot*1.15/1.27/0.914:.0f} yd of 50 in cloth: buy 12 yd. Tape: 75 mm 6 oz, about 22 m.",
             f"Glass mass about {glass_kg:.1f} kg; wet-out resin about 1:1 by mass, plus bonding, fillets, strip glue and fill coats:",
             "about 4 kg (3.5 L) of mixed 105/205 in all. One B-size kit (1.2 gal) covers it, an A-size kit as reserve.",
             "Overlaps: 50 mm between pieces; stagger joints 100 mm between plies. Peel ply every surface that gets a later bond.",
             "Every printed part that is exposed gets two coats of epoxy and paint (C4)."]
    notes(bg, 12, yb - 3, "Quantities", lines, fs=5.3, lh=3.4)
    # strongback
    ax = view(fig, 14, 60, (-60, 1560), (-40, 330), 8, "STRONGBACK AND FRAMES, SIDE VIEW (hull upside down, 1:8)")
    ax.add_patch(Rectangle((-50, 290), 1600, 38, fc="#e8e0d0", ec=INK, lw=0.5))
    ax.text(750, 309, "strongback: 2 x 6 on edge, level and straight, top = datum z 290", fontsize=4.6, ha="center", va="center")
    for i, x in enumerate(np.arange(150, 1351, 150), 1):
        zk = float(D.keel_z(x))
        ax.add_patch(Rectangle((x - 6, zk + 11), 12, 290 - zk - 11, fc="#d9d4c0", ec=INK, lw=0.4))
        ax.text(x, zk - 8, f"T{i:02d}", fontsize=4.4, ha="center", va="top")
        ax.text(x, 280, f"{x:.0f}", fontsize=4.0, ha="center", va="top", rotation=90)
    xx = np.linspace(0, D.L, 200)
    ax.plot(xx, [float(D.keel_z(x)) for x in xx], color=INK, lw=0.8)
    ax.plot(xx, [float(D.deck_z(x)) for x in xx], color=GREY, lw=0.4, ls="--")
    ax.add_patch(Rectangle((D.L - 6, float(D.keel_z(D.L))), 12, 290 - float(D.keel_z(D.L)), fc="#cfc6a8", ec=INK, lw=0.4))
    ax.text(D.L + 8, 150, "T10\ntransom", fontsize=4.2, va="center")
    ax.text(-8, 150, "T11 stem\npiece", fontsize=4.2, va="center", ha="right")
    ax.set_ylim(330, -40)   # upside down: keel at the top of the view
    # sequence
    seq = ["1. Print the 1:1 templates (check the 100 mm bars). Cut frames T01-T09, transom T10 and stem T11 from 12 mm MDF.",
           "2. Strongback: 2 x 6 on edge, levelled. Stand the frames upside down at x 150, 300 ... 1350, square and on the datum.",
           "3. Fair the frames with a long batten. Tape the frame edges (packing tape) so epoxy cannot stick.",
           "4. Strip-plank the hull: H80 strips 25 wide, glued edge to edge with thickened epoxy, screwed or pinned to the frames.",
           "5. Fair the foam. Glass the outside: 2 x 6 oz, peel ply. Fill and fair; first primer coat. Proof marks: DWL, stations.",
           "6. Turn the hull over, pull the frames. Glass the inside: 1 x 6 oz; 2nd ply over the sump; 3 plies x 650-800.",
           "7. Keel box and floors (D04): floors T19, T20 tabbed with 3 x 6 oz; keel box cast round the waxed fin tenon.",
           "8. Fin (D04): hardwood core round the M10 rods, carbon strips, 6 x 6 oz each side; bulb cast in plaster from P14.",
           "   Proof-load the keel (Field Test K, 60 kg) before paint.",
           "9. Trunks, mast tube (2 in PVC, glassed 60 mm both ends), bulkheads T17/T18 with 50 mm tapes both sides.",
           "10. Battery box, box shelf, P16/P17/P21/P22/P24 pads bonded; pump, hoses; foam blocks (D09) fitted and numbered.",
           "11. Wire the boat to D30 with the deck off; bench-test everything (Field Tests I, N).",
           "12. Deck: H80 + 2 x 6 oz out / 1 in, hatch frame doubler, YB3 well; bond on with thickened epoxy, tape the joint in and out.",
           "13. Cut the hatch (T16), fit inserts, O-ring cord; P23 bowl in the lid; vents, Schrader valve; pressure-decay test.",
           "14. Rudders (D05), wing (D06), stub (D07), deck hardware; balance the rig; paint, labels, antifouling (3 coats)."]
    notes(bg, 205, 213, "BUILD SEQUENCE (full detail on the sheet named in brackets)", seq, fs=5.2, lh=3.45)
    bg.text(205, 150, "Tools you may not own: hot-wire foam cutter (wing cores), jigsaw, random-orbit sander, long fairing board,", fontsize=5.2, va="top")
    bg.text(205, 146.5, "digital scale (0.1 g) for epoxy, respirator (organic + P100), heat gun, crimp tool, 3D printer (220 x 220 bed).", fontsize=5.2, va="top")
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D32 hardware and linkage
FASTENERS = [
    ["M3 x 4 set screw", "1", "P02 hub on the vane shaft", "tap D2.5 hole M3"],
    ["M3 x 20 SHCS + nyloc", "2 (+1)", "P26 clamps (+ P02A/B pin)", ""],
    ["M4 x 6 set screw", "3", "P03 (1), P06 (2)", "tap D3.3 holes M4"],
    ["M4 x 30 SHCS + nyloc + 2 washers", "8", "P05, P08 (2), P09, P11 (2), P18, P20", "D4.3 holes"],
    ["M5 x 16 SHCS", "12", "hatch lid into bonded inserts", "D08; torque evenly"],
    ["M5 x 16 SHCS", "8", "battery-box lid into bonded inserts", "E2: was not specified"],
    ["M5 x 12 SHCS", "4", "RockBLOCK Plus to P23", "its own M5 inserts"],
    ["M5 x 30 SHCS + nyloc + fender washers", "2", "P08 ear clamp", ""],
    ["M5 x 30 SHCS + nyloc + fender washers", "4", "P06 to transom, bedded", "glass pad behind"],
    ["M5 x 25 CSK + nyloc", "2", "P19 to the YB3 well floor", "countersink by hand"],
    ["M5 bonded inserts", "20", "hatch frame (12), battery box (8)", "or nuts glassed on"],
    ["M10 316 rod + nyloc + washer", "2", "fin rods to the G10 plate", "D04"],
    ["4 mm 316 pin x 20", "4", "rudder cores P13 on the stocks", "epoxied"],
    ["3 mm 316 pin x 16", "2", "tiller P11 cross-pins", "drill stock 3 mm"],
    ["316 hose clamp 20-32", "8", "P12 (4), P19 (2), P24 (2)", ""],
    ["N52 magnet 6 x 3", "2", "P25 detent", "same pole up"],
    ["Steel disc 6 x 1", "1", "P10a pocket (E2)", "epoxied"],
    ["Diametric magnet 6 x 2.5", "1", "P04", "AS5600 type"],
    ["S608-2RS stainless", "2", "P01, with spacer P27 (E2)", "press from the top"],
    ["6806 acetal, glass balls", "2", "P07, on 42 x 1.5 O-rings", ""],
    ["igus JFM-1214-12", "4", "rudder trunks, 2 each", "press fit"],
    ["V-ring VA-30", "1", "spar above P07", ""],
    ["EPDM cord 4 mm", "3 m", "hatch, battery-box lid", "grease, butt-join"],
]

def sheet_hardware(pdf):
    fig, bg = new_sheet("D32", "Hardware schedule and steering linkage (E2)", "Linkage plan 1:1.5, spring link 1:1")
    bg.text(12, 268, "HARDWARE SCHEDULE  (all fasteners 316 / A4 stainless; nylon-insert nuts; bed every through-bolt in sealant)", fontsize=7, weight="bold", va="top")
    yb = table(bg, 12, 264, ["Item", "Qty", "Where", "Note"], FASTENERS, [52, 13, 58, 34], fs=5.0, rh=3.75)
    bb = ["Battery-box lid (E2, not drawn before): 4 mm G10 or 3 x 6 oz over 6 mm foam, like the hatch lid.",
          "4 mm EPDM cord in a 3 x 3 groove (or glued to the lid), 8 x M5 x 16 into bonded inserts on a 20 mm flange.",
          "Two WetLinks (W7, W8) in the box end wall for the main and limp-home feeds; F0-F2 inside, at the terminal."]
    notes(bg, 12, yb - 3, "Battery box closure", bb, fs=5.2, lh=3.4)
    # linkage plan
    R = D.RUDDER; sx = 1330.0; tx = R['stock_x']
    ax = view(fig, 190, 150, (1300, 1430), (-30, 75), 1.5, "STEERING LINKAGE, ONE RUDDER, PLAN (1:1.5)")
    yS, yT = 15.0, 0.0
    ax.add_patch(Rectangle((sx - 33, yS - 17), 66, 34, fc="#eef3fb", ec=INK, lw=0.5))
    ax.text(sx, yS - 20, "SER-2000 in P12\n(output position: measure)", fontsize=4.5, ha="center", va="top")
    ax.add_patch(Circle((sx, yS), 3, fc="white", ec=INK, lw=0.5))
    ax.add_patch(Circle((tx, yT), 6, fc="#ddd", ec=INK, lw=0.6))
    ax.text(tx + 8, -6, "stock D12", fontsize=4.6)
    rs, rt = 30.0, 45.0
    ax.plot([sx, sx], [yS, yS + rs], color=INK, lw=2.2, solid_capstyle="round")
    ax.plot([tx, tx], [yT, yT + rt], color=INK, lw=2.6, solid_capstyle="round")
    for r in (20, 25, 30): ax.add_patch(Circle((sx, yS + r), 1.1, fc="white", ec=INK, lw=0.3))
    for r in (35, 45, 55):
        ax.add_patch(Circle((tx, yT + r), 1.1, fc="white", ec=INK, lw=0.3))
    ax.plot([sx, tx], [yS + rs, yT + rt], color=BLUE, lw=0.9)
    mx, my = (sx + tx) / 2, (rs + rt) / 2
    my = yT + rt
    ax.add_patch(Rectangle((mx - 14, my - 3), 28, 6, fc="#fff6ea", ec=ORG, lw=0.6))
    ax.text(mx, my + 6, "spring overload link", fontsize=4.6, ha="center", color=ORG)
    ax.text(sx - 3, rs + 3, "P26 arm\nholes 20/25/30", fontsize=4.4, ha="right", va="bottom")
    ax.text(tx + 3, rt + 3, "P11 tiller\nholes 35/45/55", fontsize=4.4, ha="left", va="bottom")
    dim(ax, (sx, -14), (tx, -14), -8, f"{tx - sx:.0f} (if the output is mid-pocket)", fs=4.8)
    dim(ax, (1415, yT), (1415, yS), 0, f"{yS - yT:.0f}", fs=4.5)
    ax.text(1418, 7, "servo output offset = tiller hole - arm hole", fontsize=4.0, va="center")
    ax.text(1365, 68, "both arms at 90 deg to the pushrod at neutral", fontsize=4.6, ha="center")
    # travel table
    rows = []
    for rt_ in (35, 45, 55):
        for rs_ in (20, 25, 30):
            s = rt_ * np.sin(np.radians(35)) / rs_
            rows.append([rt_, rs_, f"{np.degrees(np.arcsin(s)):.0f}" if s < 1 else "too far", f"{rt_/rs_:.2f}"])
    bg.text(190, 137, "Servo travel for +/-35 deg rudder", fontsize=6.2, weight="bold")
    table(bg, 190, 135, ["Tiller hole", "Arm hole", "Servo +/- deg", "Torque gain"], rows, [18, 16, 22, 20], fs=5.0, rh=3.6)
    bg.text(190, 94, "Start with tiller 45 / arm 30 (servo +/-59 deg, gain 1.5). Set the end points in ArduPilot so", fontsize=5.0)
    bg.text(190, 90.5, "the rudder stops at +/-35 deg, inside the G10 stops at +/-40.", fontsize=5.0)
    # spring link section
    ax2 = view(fig, 300, 178, (-5, 90), (-10, 14), 1, "SPRING OVERLOAD LINK, SECTION (1:1)")
    ax2.add_patch(Rectangle((10, -3.5), 60, 7, fc="#f1e7c8", ec=INK, lw=0.6))
    ax2.text(40, 5, "brass or 316 tube 7 x 0.5, 60 long, ends crimped/soldered over washers", fontsize=4.0, ha="center")
    ax2.plot([-3, 88], [0, 0], color=INK, lw=1.0)
    ax2.add_patch(Rectangle((38, -3), 4, 6, fc="#999", ec=INK, lw=0.4)); ax2.text(40, -6, "collar soldered\non the rod", fontsize=4.0, ha="center", va="top")
    for x0, x1 in ((11, 38), (42, 69)):
        xs = np.linspace(x0, x1, 60); ax2.plot(xs, 2.6 * np.sin((xs - x0) / (x1 - x0) * 2 * np.pi * 7), color=ORG, lw=0.5)
    ax2.text(-3, 2, "to servo arm\n(M2 clevis)", fontsize=4.0, va="bottom")
    ax2.text(88, 2, "to tiller\n(M2 clevis)", fontsize=4.0, va="bottom", ha="right")
    sp = ["Two 316 compression springs (6 OD, 1.0 wire, about 30 free) either side of a collar on the rod,",
          "preloaded in the tube. The link stays rigid until the push or pull passes the preload, then",
          "shortens or lengthens, so a wave that slams the blade cannot strip the servo.",
          "Set the preload to about twice the steering load: about 55 N with arm hole 25 (servo rated",
          "7 kg.cm). Check on the bench with a luggage scale: firm under normal steering, gives before",
          "the servo stalls (about 80 N at hole 25). Suggested detail: prove it in Test I."]
    notes(bg, 300, 168, "Spring link (replaces the C3 servo-saver, Rev E)", sp, fs=5.0, lh=3.2)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ D33 printing guide
def sheet_printing(pdf):
    fig, bg = new_sheet("D33", "3D-printing guide (E2)", "Coupon 1:1.5")
    rows = list(csv.DictReader(open(os.path.join(HERE, "..", "Print_Guide.csv"))))
    bg.text(12, 268, "PRINTED PARTS  (stl/ folder; every file is already in print orientation, z = 0 on the bed)", fontsize=7, weight="bold", va="top")
    tr = []
    for r in rows:
        tr.append([r["file"][4:-4], r["qty"] if r["qty"] != "0" else "alt", r["material"], f"{r['walls']} / {r['infill']}",
                   r["size_mm"], r["supports"][:44], r["grams_each"], r["hours_each"]])
    yb = table(bg, 12, 264, ["File", "Qty", "Mat.", "Walls / infill", "Size mm", "Supports", "g", "h"], tr,
               [52, 8, 11, 23, 25, 60, 9, 9], fs=4.6, rh=4.15)
    tg = {}; th = 0
    for r in rows:
        q = int(r["qty"]); tg[r["material"]] = tg.get(r["material"], 0) + q * int(r["grams_each"]); th += q * float(r["hours_each"])
    bg.text(12, yb - 3, "Totals (qty as listed): " + ", ".join(f"{m} {g/1000:.2f} kg" for m, g in tg.items()) +
            f";  about {th:.0f} h at 12 g/h (an i3-type printer; a fast CoreXY takes about half).", fontsize=5.4, va="top")
    gen = ["Nozzle 0.4, layer 0.2 (0.16 for P10, P13, P25). ASA for parts in the sun, PETG inside, PLA only for",
           "the bulb pattern P14. 4+ walls; infill as listed. Dry PETG and ASA before printing (ASA in an enclosure).",
           "Print the fit coupons P00a/P00b first, with the filament and settings you will use. Try the real tube,",
           "rod, bearing and bolt in each hole. Too tight: raise XY hole compensation 0.1 mm (or scale 100.5%).",
           "Bed: every part fits 220 x 220 except P02 (275 long): print it diagonally on a 230 x 230 or larger bed,",
           "or print P02A + P02B (E2 split) and join with epoxy and an M3 bolt. Brim tall thin parts (P02B, P10, P13).",
           "Horizontal holes are teardrops (point up): print as modelled, never on their side. Ream bearing seats",
           "lightly if tight. Epoxy-coat and paint every exposed part (C4). Bonded faces: sand 80 grit first.",
           "E2 changes: P01 bore (bearing could not be fitted), new spacer P27, P03 and P07 chamfers (no supports),",
           "P10a disc pocket, P12 base cut to fit its pocket, P02A/B split, P00 coupons."]
    notes(bg, 222, 262, "Settings and checks", gen, fs=5.0, lh=3.2)
    # coupon map
    ax = view(fig, 12, 44, (-100, 100), (-45, 45), 1.5, None)
    ax.add_patch(Rectangle((-95, -40), 190, 80, fc="#eef3fb", ec=INK, lw=0.6))
    ax.add_patch(Polygon([[-95, 32], [-88, 40], [-95, 40]], closed=True, fc="white", ec=INK, lw=0.4))
    x = -88.0
    for d in Pm.FIT_BORES:
        x += d / 2; ax.add_patch(Circle((x, 22), d / 2, fc="white", ec=INK, lw=0.4)); ax.text(x, 22 - d / 2 - 1.5, f"{d}", fontsize=3.8, ha="center", va="top"); x += d / 2 + 6
    x = -90.0
    for d in Pm.FIT_BORES2:
        x += d / 2; ax.add_patch(Circle((x, -15), d / 2, fc="white", ec=INK, lw=0.4)); ax.text(x, -15, f"{d}", fontsize=4.2, ha="center", va="center"); x += d / 2 + 6
    bg.text(12, 106 - 0, "", fontsize=1)
    uses = ["P00a hole map (notch top-left), 1:1.5.", "What each hole tests:",
            "3.3  M4 tap drill        4.3  M4 bolt", "6.2  tail pivot rod     8.05  vane shaft in P04",
            "8.1  vane shaft in P02   10.5  WetLink", "12.1  rudder stock (P11)  12.2  fibreglass arm",
            "16.2  tail boom         20.3  stub tube", "22.1  S608 bearing      30.2  spar clamp",
            "30.6  catcher land      42.6  6806 bearing seat", "P00b teardrops, left to right: 12.2, 16.2, 20.4",
            "(arm, boom, stub tube as in P08 and P06)."]
    notes(bg, 152, 98, "Fit coupons", uses, fs=4.8, lh=3.1)
    pdf.savefig(fig); plt.close(fig)
