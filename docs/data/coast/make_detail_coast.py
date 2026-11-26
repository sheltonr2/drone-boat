"""Detailed coastlines and charted hazards for the simulator's scenario key "detail_coast" (26 Nov 2026).

Inputs (in this folder, fetched on 26 Nov 2026 through the browser on Randolph's PC):
  osm_coast_<region>.json   OpenStreetMap natural=coastline ways (Overpass, maps.mail.ru mirror), simplified to 12 m.
                            (c) OpenStreetMap contributors, ODbL 1.0.
  osm_reef_carib.json       OpenStreetMap natural=reef areas.
  noaa_enc_<region>.json    NOAA ENC Direct to GIS (US Office of Coast Survey; public domain; not for navigation):
                            depth areas shallower than 2 m, rocks, obstructions and wrecks, all scale bands.

Output: detail_<region>.json = {"name", "boxes": [[lat0, lat1, lon0, lon1]], "polygons": [[[lon, lat], ...], ...],
        "layers": {polygon index ranges by source}, "notes"}. Inside its boxes the simulator treats the polygons as the
        only land (anything a 0.6 m-draft boat would hit: land, drying and sub-2 m reef and shoal, charted rocks and
        obstructions within 2 m of the surface). Outside the boxes Natural Earth 1:50m is used as before.

Run from the repo root:  python docs/data/coast/make_detail_coast.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))

REGIONS = {
    # box: where the detailed data replaces Natural Earth (inside the OSM query box, so every ring that matters is whole)
    "carib": dict(name="US and British Virgin Islands (OSM coastline + reefs + NOAA ENC hazards)",
                  box=(17.62, 18.88, -65.12, -64.17), osm="osm_coast_carib.json", reef="osm_reef_carib.json",
                  enc="noaa_enc_vi.json"),
    "cornwall": dict(name="West Cornwall and the Isles of Scilly (OSM coastline)",
                     box=(49.78, 50.55, -6.55, -3.95), osm="osm_coast_cornwall.json", reef=None, enc=None),
    "hatteras": dict(name="Cape Hatteras and Diamond Shoals (OSM coastline + NOAA ENC hazards)",
                     box=(34.83, 35.92, -76.25, -75.03), osm="osm_coast_hatteras.json", reef=None,
                     enc="noaa_enc_hatteras.json"),
}
ROCK_M = 2.0           # rocks/obstructions/wrecks with a charted depth (VALSOU) below this, or awash/drying/unknown
ROCK_R_M = 40.0        # point hazards become 40 m-radius polygons


def join_ways(ways):
    """OSM coastline ways -> chains, joined end to start by node id. Coastline ways have the land on their left."""
    by_first = {}
    for w in ways:
        by_first.setdefault(w[1], []).append(w)
    used, chains = set(), []
    for w in ways:
        if w[0] in used: continue
        used.add(w[0]); pts = list(w[3]); first, last = w[1], w[2]
        while last != first:
            nxt = [x for x in by_first.get(last, []) if x[0] not in used]
            if not nxt: break
            x = nxt[0]; used.add(x[0]); pts += x[3][1:]; last = x[2]
        chains.append((pts, first == last))
    # a chain that started mid-ring is completed by another chain ending at its start: merge open chains repeatedly
    opens = [c for c, closed in chains if not closed]
    closed = [c for c, cl in chains if cl]
    changed = True
    while changed:
        changed = False
        for i in range(len(opens)):
            for j in range(len(opens)):
                if i != j and opens[i] and opens[j] and opens[i][-1] == opens[j][0]:
                    opens[i] = opens[i] + opens[j][1:]; opens[j] = None; changed = True
            if opens[i] and opens[i][0] == opens[i][-1]:
                closed.append(opens[i]); opens[i] = None; changed = True
        opens = [o for o in opens if o]
    return closed, opens


def inside_box(p, box):
    return box[0] <= p[1] <= box[1] and box[2] <= p[0] <= box[3]


def clip_chain(chain, box):
    """Pieces of an open chain inside the box, each with its entry and exit points on the box edge."""
    lat0, lat1, lon0, lon1 = box
    def cross(a, b):
        # first crossing of segment a->b with the box edge, as (t, point)
        best = None
        for (k, v) in ((0, lon0), (0, lon1), (1, lat0), (1, lat1)):
            if (a[k] - v)*(b[k] - v) <= 0 and a[k] != b[k]:
                t = (v - a[k])/(b[k] - a[k]); q = [a[0] + t*(b[0] - a[0]), a[1] + t*(b[1] - a[1])]
                if inside_box([min(max(q[0], lon0), lon1), min(max(q[1], lat0), lat1)], box):
                    q = [min(max(q[0], lon0), lon1), min(max(q[1], lat0), lat1)]
                    if best is None or t < best[0]: best = (t, q)
        return best or (0.0, [min(max(a[0], lon0), lon1), min(max(a[1], lat0), lat1)])
    pieces, cur = [], None
    for a, b in zip(chain[:-1], chain[1:]):
        ia, ib = inside_box(a, box), inside_box(b, box)
        if ia and cur is None: cur = [a]            # chain starts inside (should not happen with a big query box)
        if ia and ib: cur.append(b)
        elif ia and not ib:
            c = cross(a, b); cur.append(c[1]); pieces.append(cur); cur = None
        elif not ia and ib:
            c = cross(a, b); cur = [c[1], b]
    if cur: pieces.append(cur)
    return pieces


def perim_pos(p, box):
    """Position of a point on the box edge, increasing anticlockwise from the south-west corner."""
    lat0, lat1, lon0, lon1 = box; w, h = lon1 - lon0, lat1 - lat0; x, y = p
    e = 1e-9
    if abs(y - lat0) < e: return x - lon0                       # south edge, west to east
    if abs(x - lon1) < e: return w + (y - lat0)                 # east edge, south to north
    if abs(y - lat1) < e: return w + h + (lon1 - x)             # north edge, east to west
    return 2*w + h + (lat1 - y)                                 # west edge, north to south


def corner_path(s0, s1, box):
    """Box corners passed going anticlockwise from perimeter position s0 to s1."""
    lat0, lat1, lon0, lon1 = box; w, h = lon1 - lon0, lat1 - lat0; L = 2*(w + h)
    corners = [(w, [lon1, lat0]), (w + h, [lon1, lat1]), (2*w + h, [lon0, lat1]), (L, [lon0, lat0])]
    out, s = [], s0
    span = (s1 - s0) % L
    for k in range(8):
        for cs, cp in corners:
            d = (cs - s0) % L
            if 0 < d < span and cp not in out: out.append((d, cp))
        break
    return [cp for d, cp in sorted(out)]


def close_pieces(pieces, box):
    """Land on the left of each piece: from a piece's exit, follow the box edge anticlockwise to the next entry."""
    if not pieces: return []
    rings, left = [], list(pieces)
    while left:
        ring = list(left.pop(0)); start = perim_pos(ring[0], box)
        for _ in range(len(pieces) + 2):
            s_exit = perim_pos(ring[-1], box)
            L = 2*((box[3] - box[2]) + (box[1] - box[0]))
            cands = [(((perim_pos(p[0], box) - s_exit) % L), i) for i, p in enumerate(left)]
            d_start = (start - s_exit) % L
            if cands and min(cands)[0] < d_start:
                d, i = min(cands); nxt = left.pop(i)
                ring += corner_path(s_exit, perim_pos(nxt[0], box), box) + nxt
            else:
                ring += corner_path(s_exit, start, box) + [ring[0]]
                break
        rings.append(ring)
    return rings


def circle(lon, lat, r_m, n=8):
    kx = 111320*math.cos(math.radians(lat)); ky = 110540
    return [[round(lon + r_m*math.cos(2*math.pi*k/n)/kx, 6), round(lat + r_m*math.sin(2*math.pi*k/n)/ky, 6)] for k in range(n + 1)]


HAZ_WATLEV = {1, 2, 4, 5}   # S-57 WATLEV: 1 partly submerged at high water, 2 always dry, 4 covers and uncovers, 5 awash


def enc_hazards(path, box):
    """Charted hazards a 0.6 m-draft boat could hit, from NOAA ENC (all scale bands):
    - depth areas wholly shallower than 1.8 m (DRVAL2 <= 1.8: drying and 0-1.8 m reef flats and shoals);
    - rocks that dry, cover and uncover or are awash, charted shallower than 2 m, or of unknown depth;
    - obstructions and wrecks that dry, cover and uncover or are awash, or are charted shallower than 2 m, and
      dangerous wrecks of unknown depth (CATWRK exactly "dangerous wreck": until 26 Nov 2026 a substring test also
      caught "non-dangerous wreck", adding 12 harmless wrecks off Hatteras and 3 in the Virgin Islands to the v1 files).
    Points become 40 m-radius polygons. Areas such as 0-18 m depth bands, fish havens and subsurface foul ground
    are left out."""
    d = json.load(open(os.path.join(HERE, path)))
    polys, counts = [], {}
    def add(kind, ring):
        if len(ring) >= 4 and any(inside_box(p, box) for p in ring):
            polys.append(ring); counts[kind] = counts.get(kind, 0) + 1
    def rings_of(g):
        return [g["c"][0]] if g["t"] == "Polygon" else [pp[0] for pp in g["c"]] if g["t"] == "MultiPolygon" else []
    def points_of(g):
        return [g["c"]] if g["t"] == "Point" else g["c"] if g["t"] == "MultiPoint" else []
    for band, layers in d["bands"].items():
        for lname, feats in layers.items():
            for f in feats:
                g, p = f.get("g"), f.get("p") or {}
                if not g: continue
                v, wl = p.get("VALSOU"), p.get("WATLEV")
                shallow = v is not None and v < ROCK_M
                if lname == "Depth_Area":
                    if p.get("DRVAL2") is not None and p["DRVAL2"] <= 1.8:
                        for r in rings_of(g): add("depth area under 1.8 m", r)
                elif lname == "Underwater_Awash_Rock_point":
                    if wl in HAZ_WATLEV or shallow or v is None:
                        for q in points_of(g): add("rock", circle(q[0], q[1], ROCK_R_M))
                elif lname == "Obstruction_point":
                    if wl in HAZ_WATLEV or shallow:
                        for q in points_of(g): add("obstruction", circle(q[0], q[1], ROCK_R_M))
                elif lname == "Wreck_point":
                    if wl in HAZ_WATLEV or shallow or (v is None and str(p.get("CATWRK", "")).strip().lower() == "dangerous wreck"):
                        for q in points_of(g): add("wreck", circle(q[0], q[1], ROCK_R_M))
                elif lname in ("Obstruction_area", "Wreck_area"):
                    if wl in HAZ_WATLEV or shallow:
                        for r in rings_of(g): add(lname.split("_")[0].lower() + " area", r)
    return polys, counts


def build(region):
    R = REGIONS[region]; box = R["box"]
    ways = json.load(open(os.path.join(HERE, R["osm"])))["ways"]
    closed, opens = join_ways(ways)
    rings = [c for c in closed if any(inside_box(p, box) for p in c)]
    pieces = [pc for ch in opens for pc in clip_chain(ch, box)]
    mainland = close_pieces(pieces, box)
    polys = rings + mainland
    layers = {"osm_coast": [0, len(polys)]}
    notes = [f"{len(rings)} closed OSM rings (islands, islets, rocks) and {len(mainland)} mainland pieces clipped to the box"]
    if R.get("reef"):
        rr = json.load(open(os.path.join(HERE, R["reef"])))["rings"]
        n0 = len(polys)
        for r in rr:
            if r.get("role", "outer") == "outer" and len(r["pts"]) >= 4 and any(inside_box(p, box) for p in r["pts"]):
                ring = r["pts"] if r["pts"][0] == r["pts"][-1] else r["pts"] + [r["pts"][0]]
                polys.append(ring)
        layers["osm_reef"] = [n0, len(polys)]; notes.append(f"{len(polys) - n0} OSM reef areas")
    if R.get("enc") and os.path.exists(os.path.join(HERE, R["enc"])):
        n0 = len(polys); hp, counts = enc_hazards(R["enc"], box); polys += hp
        layers["noaa_enc"] = [n0, len(polys)]; notes.append("NOAA ENC hazards: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    out = dict(name=R["name"], boxes=[list(box)], polygons=polys, layers=layers, notes=notes,
               sources=["OpenStreetMap contributors (ODbL 1.0)"] + (["NOAA Office of Coast Survey ENC Direct to GIS (not for navigation)"] if "noaa_enc" in layers else []))
    json.dump(out, open(os.path.join(HERE, f"detail_{region}.json"), "w"), separators=(",", ":"))
    print(region, "; ".join(notes), f"; {sum(len(p) for p in polys)} vertices")
    return out


if __name__ == "__main__":
    for r in REGIONS:
        build(r)
