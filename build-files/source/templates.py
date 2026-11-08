"""Full-size templates: tiled 1:1 Letter PDF + DXF files."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle
import design as D

OUT = "out"; os.makedirs(f"{OUT}/dxf", exist_ok=True)
MM = 1 / 25.4
PW, PH = 215.9, 279.4; MARGIN = 10.0; OVER = 12.0

def write_dxf(path, polys, circles=(), texts=()):
    L = ["0", "SECTION", "2", "HEADER", "9", "$ACADVER", "1", "AC1009", "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"]
    for P, layer, closed in polys:
        L += ["0", "POLYLINE", "8", layer, "66", "1", "70", "1" if closed else "0"]
        for x, y in P:
            L += ["0", "VERTEX", "8", layer, "10", f"{x:.3f}", "20", f"{y:.3f}"]
        L += ["0", "SEQEND"]
    for x, y, r, layer in circles:
        L += ["0", "CIRCLE", "8", layer, "10", f"{x:.3f}", "20", f"{y:.3f}", "40", f"{r:.3f}"]
    for x, y, h, t, layer in texts:
        L += ["0", "TEXT", "8", layer, "10", f"{x:.3f}", "20", f"{y:.3f}", "40", f"{h:.2f}", "1", t]
    L += ["0", "ENDSEC", "0", "EOF"]
    open(path, "w").write("\n".join(L) + "\n")

def offset_curve(P, d):
    """Offset an open polyline P (N,2) by d to its left."""
    t = np.gradient(P, axis=0); t /= np.linalg.norm(t, axis=1, keepdims=True)
    n = np.c_[-t[:, 1], t[:, 0]]
    return P + n * d

# ------------------------------------------------------------------ templates
def frame_template(i, x):
    y, z = D.section(x, 120)
    outer = np.r_[np.c_[-y[::-1], z[::-1]], np.c_[y[1:], z[1:]]]      # port deck edge -> keel -> stbd deck edge
    # offset inward 11 mm: walking from port deck down to keel and up to stbd, inside is to the left? compute both, choose inner
    a = offset_curve(outer, 11.0); b = offset_curve(outer, -11.0)
    inner = a if np.mean(a[:, 1]) > np.mean(b[:, 1]) else b
    datum = 290.0
    m = (np.abs(inner[:, 0]) < np.abs(outer[:, 0]).max()) & (inner[:, 1] < datum)
    inner = inner[m]
    frame = np.r_[inner, [[inner[-1, 0], datum], [inner[0, 0], datum]]]
    polys = [(outer, "HULL_OUTSIDE", False), (frame, "FRAME_CUT", True),
             (np.array([[0, float(D.keel_z(x)) - 15], [0, datum + 10]]), "CENTRELINE", False),
             (np.array([[-float(D.half_beam(x)) - 20, 90], [float(D.half_beam(x)) + 20, 90]]), "DWL", False)]
    xl = -0.6 * float(D.half_beam(x))
    texts = [(xl, datum - 22, 6, f"T{i:02d}  STATION {i}  (x = {x:.0f})", "TEXT"),
             (xl, datum - 32, 3.5, "Cut on the solid FRAME line (hull minus 11 mm).", "TEXT"),
             (xl, datum - 39, 3.5, "Dashed = outside of hull. Blue = DWL.", "TEXT"),
             (xl, datum - 46, 3.5, "Top edge = strongback datum (frames upside down).", "TEXT")]
    return dict(name=f"T{i:02d}_frame_station_{i}", polys=polys, circles=[], texts=texts,
                desc=f"Hull frame, station {i} (x {x:.0f})")

def transom_template():
    x = D.L; y, z = D.section(x, 120)
    outer = np.r_[np.c_[-y[::-1], z[::-1]], np.c_[y[1:], z[1:]], [[-y[-1], z[-1]]]]
    return dict(name="T10_transom", polys=[(outer, "TRANSOM_OUTSIDE", True),
                (np.array([[0, 40], [0, 240]]), "CENTRELINE", False)], circles=[],
                texts=[(-60, 200, 6, "T10  TRANSOM (outside shape)", "TEXT"),
                       (-60, 190, 4, "Cut the foam transom to this line; bracket P06 bolts at z 160-260.", "TEXT")],
                desc="Transom outline")

def stem_template():
    x = np.linspace(0, 330, 120)
    keel = np.c_[x, D.keel_z(x)]; deck = np.c_[x[::-1], D.deck_z(x[::-1])]
    P = np.r_[keel, deck]
    return dict(name="T11_stem_profile", polys=[(P, "STEM_PROFILE", True)], circles=[],
                texts=[(120, 200, 6, "T11  STEM PROFILE x 0-330", "TEXT"),
                       (120, 190, 4, "Cut a 12 mm ply stem piece; frames 1 and 2 notch into it.", "TEXT")],
                desc="Bow stem profile")

def foil_template(name, t, c, holes, label, extra=()):
    xs, ys = D.naca(t, c, 140)
    P = np.c_[xs, ys]
    circles = [(hx, 0, hr, "HOLES") for hx, hr in holes]
    polys = [(P, "FOIL", True), (np.array([[-15, 0], [c + 15, 0]]), "CHORDLINE", False)]
    for xq in (0.25 * c,):
        polys.append((np.array([[xq, -c*t*0.8], [xq, c*t*0.8]]), "QUARTER_CHORD", False))
    polys += list(extra)
    texts = [(0, -c * t * 0.5 - 18, 6, label, "TEXT"),
             (0, -c * t * 0.5 - 26, 4, "Hot-wire: screw template to the block end; lead in and out at the trailing edge.", "TEXT")]
    return dict(name=name, polys=polys, circles=circles, texts=texts, desc=label)

def hatch_template():
    H = D.HATCH; w, l, m = H['w'], H['x1'] - H['x0'], H['lid_margin']
    rect = lambda a, b: np.array([[-a/2, -b/2], [a/2, -b/2], [a/2, b/2], [-a/2, b/2]])
    from drawings import hatch_bolts
    return dict(name="T16_hatch", polys=[(rect(l + 2*m, w + 2*m), "LID_OUTLINE", True), (rect(l, w), "DECK_OPENING", True),
                                        (rect(l + 24, w + 24), "ORING_CENTRELINE", True)],
                circles=[(x, y, 2.75, "BOLT_HOLES_M5") for x, y in hatch_bolts()],
                texts=[(-l/2 + 10, 20, 6, "T16  HATCH: lid, opening, O-ring, 12 x M5", "TEXT"),
                       (-l/2 + 10, 10, 4, "x along the boat (bow to the left).", "TEXT")],
                desc="Hatch lid, opening and bolt pattern")

def all_templates():
    T = []
    for i, x in enumerate(np.arange(0, 1501, 150)):
        if 1 <= i <= 9:
            T.append(frame_template(i, x))
    T.append(transom_template()); T.append(stem_template())
    F = D.FIN
    T.append(foil_template("T12_fin_root", 0.12, F['root_chord'], [(50, 6), (105, 6)], "T12  FIN ROOT  NACA 0012  chord 170  (rod holes D12)"))
    T.append(foil_template("T13_fin_tip", 0.12, F['tip_chord'], [(37, 6), (92, 6)], "T13  FIN TIP  NACA 0012  chord 150  (rod holes D12)"))
    T.append(foil_template("T14_rudder", 0.12, D.RUDDER['chord'], [(22, 6)], "T14  RUDDER  NACA 0012  chord 120  (stock D12)"))
    nose = np.array([[4, -6], [29, -6], [29, 6], [4, 6]])
    T.append(foil_template("T15_wing", 0.15, D.WING['chord'], [(66, 12.7)], "T15  WING  NACA 0015  chord 300  (spar D25.4)",
                           extra=[(nose, "WEIGHT_POCKET", True)]))
    T.append(hatch_template())
    return T

# ------------------------------------------------------------------ tiled PDF
def draw_template(ax, T):
    for P, layer, closed in T['polys']:
        Q = np.r_[P, P[:1]] if closed else P
        style = dict(color="#111", lw=0.6)
        if layer in ("CENTRELINE", "CHORDLINE", "QUARTER_CHORD"): style = dict(color="#777", lw=0.3, ls="-.")
        if layer == "DWL": style = dict(color="#3b8bd4", lw=0.4)
        if layer == "HULL_OUTSIDE": style = dict(color="#777", lw=0.4, ls="--")
        if layer in ("FRAME_CUT",): style = dict(color="#111", lw=0.8)
        if layer == "ORING_CENTRELINE": style = dict(color="#3b8bd4", lw=0.4, ls="--")
        ax.plot(Q[:, 0], Q[:, 1], **style)
    for x, y, r, layer in T['circles']:
        ax.add_patch(Circle((x, y), r, fill=False, lw=0.5, ec="#111"))
        ax.plot([x - r - 3, x + r + 3], [y, y], color="#777", lw=0.25); ax.plot([x, x], [y - r - 3, y + r + 3], color="#777", lw=0.25)
    for x, y, h, t, layer in T['texts']:
        ax.text(x, y, t, fontsize=h * 2.2, va="bottom")

def bounds(T):
    pts = np.vstack([P for P, _, _ in T['polys']] + [np.array([[x - r, y - r], [x + r, y + r]]) for x, y, r, _ in T['circles']])
    tx = np.array([[x, y] for x, y, h, t, _ in T['texts']] + [[x + len(t) * h * 0.55, y + h] for x, y, h, t, _ in T['texts']])
    pts = np.vstack([pts, tx])
    return pts.min(0) - 8, pts.max(0) + 8

def tiled_pages(pdf, T):
    lo, hi = bounds(T)
    W, H = hi - lo
    land = W > H
    pw, ph = (PH, PW) if land else (PW, PH)
    uw, uh = pw - 2 * MARGIN, ph - 2 * MARGIN
    step_w, step_h = uw - OVER, uh - OVER
    nc = max(1, int(np.ceil((W - OVER) / step_w))) if W > uw else 1
    nr = max(1, int(np.ceil((H - OVER) / step_h))) if H > uh else 1
    total = nc * nr; k = 0
    for r in range(nr):
        for c in range(nc):
            k += 1
            x0 = lo[0] + c * step_w; y1 = hi[1] - r * step_h; y0 = y1 - uh
            if nc == 1: x0 = lo[0] - (uw - W) / 2
            if nr == 1: y0 = lo[1] - (uh - H) / 2
            fig = plt.figure(figsize=(pw * MM, ph * MM))
            ax = fig.add_axes([MARGIN / pw, MARGIN / ph, uw / pw, uh / ph])
            ax.set_xlim(x0, x0 + uw); ax.set_ylim(y0, y0 + uh); ax.set_aspect("equal"); ax.axis("off")
            draw_template(ax, T)
            ax.add_patch(plt.Rectangle((x0, y0), uw, uh, fill=False, lw=0.3, ec="#bbb", ls=":"))
            if nc > 1 or nr > 1:
                for xx in (x0 + OVER, x0 + uw - OVER):
                    ax.plot([xx, xx], [y0, y0 + uh], color="#d55", lw=0.25, ls="--")
                for yy in (y0 + OVER, y0 + uh - OVER):
                    ax.plot([x0, x0 + uw], [yy, yy], color="#d55", lw=0.25, ls="--")
            bx, by = x0 + 6, y0 + 6
            ax.plot([bx, bx + 100], [by, by], color="#111", lw=1.2, solid_capstyle="butt")
            for t in range(0, 101, 10):
                ax.plot([bx + t, bx + t], [by, by + (3 if t % 50 else 5)], color="#111", lw=0.3)
            ax.text(bx + 104, by, "100 mm check: print at 100% / Actual size", fontsize=6, va="center")
            fig.text(0.5, 1 - 6 / ph, f"{T['desc']}   |   page {k} of {total} (row {r+1}, col {c+1})   |   1:1, mm"
                     + ("   |   overlap 12 mm: align the red dashed lines" if total > 1 else ""), ha="center", fontsize=7)
            pdf.savefig(fig); plt.close(fig)
    return total

def main():
    Ts = all_templates()
    pages = {}
    with PdfPages(f"{OUT}/Templates_1to1_Letter.pdf") as pdf:
        for T in Ts:
            pages[T['name']] = tiled_pages(pdf, T)
            write_dxf(f"{OUT}/dxf/{T['name']}.dxf", T['polys'], T['circles'], T['texts'])
    # combined hull offsets DXF (body plan)
    polys = []
    for i, x in enumerate(np.arange(0, 1501, 150)):
        y, z = D.section(x, 80)
        polys.append((np.c_[y, z], f"STATION_{i}", False)); polys.append((np.c_[-y, z], f"STATION_{i}", False))
    write_dxf(f"{OUT}/dxf/body_plan_all_stations.dxf", polys)
    print(pages, sum(pages.values()))

if __name__ == "__main__":
    main()
