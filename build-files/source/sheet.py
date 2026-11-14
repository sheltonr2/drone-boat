"""Drawing-sheet helpers: tabloid sheets with a title block, views at exact scales, dimensions."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

MM = 1 / 25.4
SHEET_W, SHEET_H = 431.8, 279.4            # tabloid landscape, mm
PROJECT = "SOLAR-SAIL OCEAN DRONE  1.5 m"
DATE = "2026-11-14"
INK = "#111111"; THIN = 0.35; MED = 0.6; THICK = 1.0
BLUE = "#1f5fa8"; GREY = "#888888"; WATER = "#3b8bd4"

def new_sheet(num, title, scale_note="", rev="E1"):
    fig = plt.figure(figsize=(SHEET_W * MM, SHEET_H * MM))
    bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, SHEET_W); bg.set_ylim(0, SHEET_H); bg.axis("off")
    bg.add_patch(Rectangle((8, 8), SHEET_W - 16, SHEET_H - 16, fill=False, lw=THICK, ec=INK))
    # title block bottom-right
    x0, y0, w, h = SHEET_W - 8 - 170, 8, 170, 30
    bg.add_patch(Rectangle((x0, y0), w, h, fill=False, lw=MED, ec=INK))
    bg.plot([x0, x0 + w], [y0 + 18, y0 + 18], color=INK, lw=THIN)
    bg.plot([x0 + 120, x0 + 120], [y0, y0 + 18], color=INK, lw=THIN)
    bg.plot([x0 + 145, x0 + 145], [y0, y0 + 18], color=INK, lw=THIN)
    bg.text(x0 + 3, y0 + 26, PROJECT, fontsize=7, weight="bold", va="center")
    bg.text(x0 + 3, y0 + 21, title.upper(), fontsize=8.5, weight="bold", va="center", color=BLUE)
    bg.text(x0 + 3, y0 + 13, f"Units: mm    {scale_note}", fontsize=6.5, va="center")
    bg.text(x0 + 3, y0 + 7, f"Date {DATE}    Drawn with Claude    Check all dims before cutting", fontsize=5.5, va="center")
    bg.text(x0 + 122, y0 + 13, "SHEET", fontsize=5, va="center"); bg.text(x0 + 122, y0 + 6, num, fontsize=9, weight="bold", va="center")
    bg.text(x0 + 147, y0 + 13, "REV", fontsize=5, va="center"); bg.text(x0 + 147, y0 + 6, rev, fontsize=9, weight="bold", va="center")
    return fig, bg

def view(fig, x, y, xlim, ylim, scale, label=None, frame=False):
    """Axes placed at sheet mm (x, y) lower-left, showing model xlim/ylim at 1:scale."""
    w = (xlim[1] - xlim[0]) / scale; h = (ylim[1] - ylim[0]) / scale
    ax = fig.add_axes([x / SHEET_W, y / SHEET_H, w / SHEET_W, h / SHEET_H])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.axis("on" if frame else "off")
    if label:
        ax.text(0.5, -0.02, label, transform=ax.transAxes, ha="center", va="top", fontsize=7, weight="bold")
    return ax

def dim(ax, p1, p2, off, text=None, fs=6, ext=True, color=INK, tpos=0.5):
    """Linear dimension between p1, p2 offset perpendicular by off (model units)."""
    p1, p2 = np.array(p1, float), np.array(p2, float)
    d = p2 - p1; L = np.linalg.norm(d)
    if L == 0: return
    u = d / L; n = np.array([-u[1], u[0]])
    a, b = p1 + n * off, p2 + n * off
    if ext:
        s = np.sign(off) if off else 1
        for p, q in [(p1, a), (p2, b)]:
            ax.plot([p[0] + n[0]*s*1.5*0, q[0] + n[0]*s*2], [p[1], q[1] + n[1]*s*2], color=color, lw=0.25)
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<|-|>", mutation_scale=5, lw=0.4, color=color, shrinkA=0, shrinkB=0))
    t = text if text is not None else f"{L:.0f}"
    m = a + (b - a) * tpos
    ang = np.degrees(np.arctan2(u[1], u[0]))
    if ang > 90.5: ang -= 180
    if ang < -89.5: ang += 180
    ax.text(m[0] + n[0] * 0, m[1], t, fontsize=fs, ha="center", va="bottom" if abs(ang) < 45 else "center",
            rotation=ang, rotation_mode="anchor", color=color,
            bbox=dict(fc="white", ec="none", pad=0.3))

def leader(ax, p, t, text, fs=5.8, color=INK, ha="left"):
    ax.annotate(text, xy=p, xytext=t, fontsize=fs, ha=ha, va="center", color=color,
                arrowprops=dict(arrowstyle="-|>", lw=0.35, color=color, mutation_scale=5))

def notes(bg, x, y, title, lines, fs=6.2, width=None, lh=3.6):
    bg.text(x, y, title, fontsize=fs + 1, weight="bold", va="top")
    yy = y - lh * 1.3
    for ln in lines:
        bg.text(x, yy, ln, fontsize=fs, va="top")
        yy -= lh
    return yy

def table(bg, x, y, cols, rows, widths, fs=5.8, rh=4.0, header_fill="#e8eef6"):
    xx = x
    tw = sum(widths)
    bg.add_patch(Rectangle((x, y - rh), tw, rh, fc=header_fill, ec=INK, lw=0.3))
    for c, w in zip(cols, widths):
        bg.text(xx + 1, y - rh/2, c, fontsize=fs, weight="bold", va="center"); xx += w
    for i, r in enumerate(rows):
        yy = y - rh * (i + 2)
        bg.add_patch(Rectangle((x, yy), tw, rh, fc="none", ec=INK, lw=0.2))
        xx = x
        for c, w in zip(r, widths):
            bg.text(xx + 1, yy + rh/2, str(c), fontsize=fs, va="center"); xx += w
    return y - rh * (len(rows) + 1)

def scale_bar(ax, x, y, length, scale_label, fs=5.5):
    ax.plot([x, x + length], [y, y], color=INK, lw=1.2, solid_capstyle="butt")
    for t in np.linspace(x, x + length, 6):
        ax.plot([t, t], [y - length*0.015, y + length*0.015], color=INK, lw=0.4)
    ax.text(x + length/2, y - length*0.03, scale_label, fontsize=fs, ha="center", va="top")
