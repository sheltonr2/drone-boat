"""Map of every candidate pickup point with its hold radius and probabilities (runs 036-039, 26 Nov 2026).

Each point is drawn on the detailed coastline it was simulated on (docs/data/coast/detail_*.json). Around it:
  solid ring  = r50, the radius the boat stays inside half the time while station-keeping (14 days, 1 km target);
  dashed ring = r90, the radius it stays inside 90% of the time: the search radius for the recovery boat.
Label: for the BVI, arrival from Mindelo (run 038), the share of holds still afloat and with the boat after 3 days,
and their product, the chance of a pickup 3 days after arrival; for Cornwall, the share still afloat after 3 and 14 days.
Reads collab/runs_036/pickup_analysis.json. Writes docs/figures/pickup_map.png (and .svg).
Run from the repo root: python docs/data/pickup_map.py
"""
import json, math, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = json.load(open(os.path.join(ROOT, "collab/runs_036/pickup_analysis.json")))
INK, INK2, LAND, SEA, RING, PLAN = "#191919", "#666666", "#d9d6cf", "#ffffff", "#257de0", "#f47230"
CURRENT = {"bvi": "norman", "cornwall": "lizard"}
# label offsets (dx, dy in degrees) chosen by hand so labels clear each other and the land
OFF = {"norman": (-0.62, -0.36), "norman_offing": (0.12, -0.42), "ginger_se": (0.30, -0.12), "jvd_north": (-0.95, 0.20),
       "anegada_west": (-1.02, 0.40), "anegada_north": (0.22, 0.30), "stcroix_north": (0.25, -0.22),
       "lizard": (0.35, -0.05), "mounts": (-0.95, 0.20), "lizard_deep": (0.30, -0.30), "scilly_lizard": (-0.95, -0.38)}


def ring(ax, lat, lon, r_km, **kw):
    t = [2 * math.pi * k / 120 for k in range(121)]
    ax.plot([lon + r_km * math.cos(a) / (111.32 * math.cos(math.radians(lat))) for a in t],
            [lat + r_km * math.sin(a) / 110.54 for a in t], **kw)


def panel(ax, region, coast, ext, title):
    det = json.load(open(os.path.join(ROOT, "docs/data/coast", coast)))
    for p in det["polygons"]:
        ax.add_patch(Polygon(p, closed=True, fc=LAND, ec="#a8a39a", lw=0.25, zorder=1))
    for tag, e in P[region].items():
        if not isinstance(e, dict) or "lat" not in e or not e.get("hold"): continue
        la, lo, h = e["lat"], e["lon"], e["hold"]
        cur = tag == CURRENT[region]
        ring(ax, la, lo, h["r90_km"], color=RING, lw=1.0, ls=(0, (4, 3)), alpha=0.8, zorder=3)
        ring(ax, la, lo, h["r50_km"], color=RING, lw=1.6, zorder=3)
        ax.plot(lo, la, marker="o", ms=9, mfc=PLAN if cur else INK, mec="white", mew=2, zorder=5)
        a3 = (e.get("afloat_by_day") or {}).get("3") or (e.get("afloat_by_day") or {}).get(3)
        lines = [e["name"] + ("  (current plan)" if cur else "")]
        if region == "bvi":
            c = e.get("crossing")
            pk = (e.get("p_pickup") or {}).get("3") or (e.get("p_pickup") or {}).get(3)
            if c: lines.append(f"arrive {c['arrive']:.0f}%   afloat after 3 d {a3:.0f}%")
            else: lines.append(f"arrive (run 038 pending)   afloat after 3 d {a3:.0f}%")
            if pk is not None: lines.append(f"pickup 3 d after arrival: {pk:.0f}%")
        else:
            a14 = (e.get("afloat_by_day") or {}).get("14") or (e.get("afloat_by_day") or {}).get(14)
            lines.append(f"afloat after 3 d {a3:.0f}%, after 14 d {a14:.0f}%")
        lines.append(f"aground in 14 d {h['percent'].get('aground', 0):.0f}%   r50 {h['r50_km']:.0f} km, r90 {h['r90_km']:.0f} km")
        dx, dy = OFF.get(tag, (0.2, 0.2))
        ax.annotate("\n".join(lines), xy=(lo, la), xytext=(lo + dx, la + dy), fontsize=7.2, color=INK, zorder=6,
                    bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cccccc", lw=0.6, alpha=0.93),
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
    ax.set_xlim(*ext[:2]); ax.set_ylim(*ext[2:]); ax.set_aspect(1 / math.cos(math.radians(sum(ext[2:]) / 2)))
    ax.set_facecolor(SEA); ax.set_title(title, fontsize=11, color=INK, loc="left", pad=10)
    ax.tick_params(labelsize=7, colors=INK2)
    for s in ax.spines.values(): s.set_color("#cccccc")


fig, axs = plt.subplots(1, 2, figsize=(17, 8.6), gridspec_kw=dict(width_ratios=[1.05, 1]))
panel(axs[0], "bvi", "detail_carib.json", (-65.55, -63.75, 17.45, 19.30),
      "BVI pickup candidates: hold radius and odds (runs 036 and 038, Feb-Apr / Nov-Jan winters)")
panel(axs[1], "cornwall", "detail_cornwall.json", (-7.05, -4.35, 49.25, 50.35),
      "Cornwall pickup candidates: hold radius and odds (run 037, mid-Aug to mid-Oct 2021-2024)")
fig.text(0.01, 0.015, "Rings: solid = r50, the boat is inside it half the time while station-keeping; dashed = r90, inside it 90% of the time "
         "(the search radius). Orange dot = current plan. Station-keeping target 1 km, 14 days, Rev E3, failures on. "
         "Coastline: OpenStreetMap + NOAA ENC hazards (BVI), OpenStreetMap (Cornwall).", fontsize=7.5, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
os.makedirs(os.path.join(ROOT, "docs/figures"), exist_ok=True)
for ext in ("png", "svg"):
    fig.savefig(os.path.join(ROOT, f"docs/figures/pickup_map.{ext}"), dpi=150)
print("docs/figures/pickup_map.png")
