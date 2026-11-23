"""Builds the data for the browser 3D viewer (build-files/viewer/): model.json (metadata + base64 mesh buffer).

Every mesh is in design coordinates (mm; x aft from the bow, y to port, z up from the hull bottom
at midships). Printed parts come from the STL files in ../stl, placed by a 4x4 matrix; the hull,
deck, foils, bulb, tubes and bought-in items are generated here from design.py.
Positions are stored as int16 (per-mesh scale), crease normals as int8, indices as uint16/uint32.
Run: python3 viewer3d.py
"""
import json, os, struct, csv
import numpy as np
import design as D
import parts as Pm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "viewer")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ mesh helpers
def read_stl(path):
    b = open(path, "rb").read()
    n = struct.unpack("<I", b[80:84])[0]
    a = np.frombuffer(b[84:84 + n * 50], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    tri = a["v"].reshape(-1, 3, 3).astype(np.float64)
    v, inv = np.unique(np.round(tri.reshape(-1, 3), 4), axis=0, return_inverse=True)
    return v, inv.reshape(-1, 3)

def crease(v, f, angle_deg=32.0):
    """Split vertices across edges sharper than angle_deg; returns (v2, n2, f2) indexed."""
    v = np.asarray(v, float); f = np.asarray(f, np.int64)
    fn = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
    area = np.linalg.norm(fn, axis=1)
    good = area > 1e-12
    f = f[good]; fn = fn[good]; area = area[good]
    fu = fn / area[:, None]
    nf = len(f)
    corner_v = f.reshape(-1)
    corner_f = np.repeat(np.arange(nf), 3)
    order = np.argsort(corner_v, kind="stable")
    cv = corner_v[order]; cf = corner_f[order]
    starts = np.r_[0, np.flatnonzero(np.diff(cv)) + 1]
    counts = np.diff(np.r_[starts, len(cv)])
    deg = counts.max()
    G = -np.ones((len(v), deg), np.int64)
    pos = np.arange(len(cv)) - np.repeat(starts, counts)
    G[cv, pos] = cf
    cosT = np.cos(np.radians(angle_deg))
    Nout = np.zeros((nf * 3, 3))
    CH = 200000
    for s in range(0, nf * 3, CH):
        idx = np.arange(s, min(s + CH, nf * 3))
        vv = corner_v[idx]; ff = corner_f[idx]
        nb = G[vv]                                   # (c, deg)
        valid = nb >= 0
        nbs = np.where(valid, nb, 0)
        dots = np.einsum("cdk,ck->cd", fu[nbs], fu[ff])
        w = np.where(valid & (dots > cosT), area[nbs], 0.0)
        Nout[idx] = np.einsum("cd,cdk->ck", w, fu[nbs])
    Nout /= np.maximum(np.linalg.norm(Nout, axis=1, keepdims=True), 1e-12)
    q = np.round(Nout * 60).astype(np.int64)
    key = np.c_[corner_v, q]
    uk, inv = np.unique(key, axis=0, return_inverse=True)
    v2 = v[uk[:, 0]]
    n2 = np.zeros((len(uk), 3))
    np.add.at(n2, inv.ravel(), Nout)
    n2 /= np.maximum(np.linalg.norm(n2, axis=1, keepdims=True), 1e-12)
    return v2, n2, inv.reshape(-1, 3)

def grid_faces(nu, nv, wrap_v=False):
    f = []
    vmax = nv if wrap_v else nv - 1
    for i in range(nu - 1):
        for j in range(vmax):
            a = i * nv + j; b = i * nv + (j + 1) % nv
            c = (i + 1) * nv + j; d = (i + 1) * nv + (j + 1) % nv
            f += [[a, c, b], [b, c, d]]
    return np.array(f, np.int64)

def orient_out(v, f, inside_pt=None):
    """Flip faces so normals point away from inside_pt (or the centroid) on average."""
    c = v.mean(0) if inside_pt is None else np.asarray(inside_pt, float)
    n = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
    m = v[f].mean(1)
    if np.sum(np.einsum("ij,ij->i", n, m - c)) < 0:
        f = f[:, ::-1]
    return f

def merge(*ms):
    V, F, o = [], [], 0
    for v, f in ms:
        V.append(v); F.append(f + o); o += len(v)
    return np.vstack(V), np.vstack(F)

def cylinder(r, z0, z1, n=48, cap=True, r1=None):
    r1 = r if r1 is None else r1
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ring0 = np.c_[r * np.cos(a), r * np.sin(a), np.full(n, z0)]
    ring1 = np.c_[r1 * np.cos(a), r1 * np.sin(a), np.full(n, z1)]
    v = np.vstack([ring0, ring1]); f = []
    for j in range(n):
        k = (j + 1) % n
        f += [[j, k, n + j], [k, n + k, n + j]]
    if cap:
        c0 = len(v); v = np.vstack([v, [0, 0, z0], [0, 0, z1]])
        for j in range(n):
            k = (j + 1) % n
            f += [[c0, k, j], [c0 + 1, n + j, n + k]]
    return v, np.array(f)

def tube(ro, ri, z0, z1, n=48):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rings = [np.c_[r * np.cos(a), r * np.sin(a), np.full(n, z)] for r, z in ((ro, z0), (ro, z1), (ri, z1), (ri, z0))]
    v = np.vstack(rings); f = []
    for s in range(4):
        A = s * n; B = ((s + 1) % 4) * n
        for j in range(n):
            k = (j + 1) % n
            f += [[A + j, A + k, B + j], [A + k, B + k, B + j]]
    return v, np.array(f)

def box(x0, x1, y0, y1, z0, z1):
    v = np.array([[x, y, z] for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)], float)
    f = np.array([[0, 2, 1], [1, 2, 3], [4, 5, 6], [5, 7, 6], [0, 1, 4], [1, 5, 4],
                  [2, 6, 3], [3, 6, 7], [0, 4, 2], [2, 4, 6], [1, 3, 5], [3, 7, 5]])
    return v, f

def rbox(x0, x1, y0, y1, z0, z1, r=3.0, n=4):
    """Box with rounded vertical edges and chamfered top/bottom rims."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; hx, hy = (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
    pts = []
    for (sx, sy, a0) in ((1, 1, 0), (-1, 1, 90), (-1, -1, 180), (1, -1, 270)):
        for a in np.radians(np.linspace(a0, a0 + 90, n + 1)):
            pts.append([cx + sx * hx + r * np.cos(a), cy + sy * hy + r * np.sin(a)])
    P = np.array(pts); m = len(P)
    ch = min(r * 0.6, (z1 - z0) * 0.2)
    cen = P.mean(0)
    def shrink(d):
        return cen + (P - cen) * (1 - d / max(np.linalg.norm(P - cen, axis=1).min(), 1e-6))
    layers = [(shrink(ch), z0), (P, z0 + ch), (P, z1 - ch), (shrink(ch), z1)]
    v = np.vstack([np.c_[L, np.full(m, z)] for L, z in layers]); f = []
    for s in range(3):
        A, B = s * m, (s + 1) * m
        for j in range(m):
            k = (j + 1) % m
            f += [[A + j, A + k, B + j], [A + k, B + k, B + j]]
    c0 = len(v); v = np.vstack([v, [*cen, z0], [*cen, z1]])
    for j in range(m):
        k = (j + 1) % m
        f += [[c0, k, j], [c0 + 1, 3 * m + j, 3 * m + k]]
    return v, np.array(f)

def poly_prism(P, z0, z1):
    """Extrude a convex-ish closed polygon (fan from its centroid)."""
    P = np.asarray(P, float); m = len(P); c = P.mean(0)
    v = np.vstack([np.c_[P, np.full(m, z0)], np.c_[P, np.full(m, z1)], [[*c, z0], [*c, z1]]])
    f = []
    for j in range(m):
        k = (j + 1) % m
        f += [[j, k, m + j], [k, m + k, m + j], [2 * m, k, j], [2 * m + 1, m + j, m + k]]
    return v, np.array(f)

def xf(v, M):
    return (np.c_[v, np.ones(len(v))] @ np.asarray(M).T)[:, :3]

def T(R=np.eye(3), t=(0, 0, 0)):
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = t; return M

def Rz(deg):
    a = np.radians(deg); c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
RX180 = np.diag([1., -1., -1.])
CYC = np.array([[0., 0., 1.], [1., 0., 0.], [0., 1., 0.]])     # local x->y, y->z, z->x
def axis_x():   # local z axis along world +x
    return np.array([[0., 0., 1.], [0., 1., 0.], [-1., 0., 0.]])
def axis_y():   # local z axis along world +y
    return np.array([[1., 0., 0.], [0., 0., 1.], [0., -1., 0.]])

# ------------------------------------------------------------------ generated vessel geometry
def hull_mesh():
    u = np.linspace(0, 1, 181)
    xs = D.L * (1 - np.cos(np.pi * u / 2) ** 1.0) ** 1.0
    xs = np.unique(np.r_[np.linspace(0, 40, 12), D.L * (u ** 1.15)])
    nt = 64; cols = []
    for x in xs:
        y, z = D.section(max(x, 0.05), nt)
        cols.append(np.c_[np.full(2 * nt - 1, x), np.r_[y[::-1], -y[1:]], np.r_[z[::-1], z[1:]]])
    V = np.vstack(cols)
    F = grid_faces(len(xs), 2 * nt - 1)
    F = orient_out(V, F, inside_pt=(750, 0, 140))
    # transom
    y, z = D.section(D.L, nt)
    P = np.c_[np.r_[y[::-1], -y[1:]], np.r_[z[::-1], z[1:]]]
    c = P.mean(0); m = len(P)
    tv = np.vstack([np.c_[np.full(m, D.L), P], [D.L, *c]])
    tf = np.array([[m, j, (j + 1) % m] for j in range(m)])
    tf = orient_out(tv, tf, inside_pt=(D.L - 100, 0, 140))
    return V, F, tv, tf, xs

def deck_mesh():
    W = D.YB3['well']; xw0, xw1 = D.YB3['x'] - W[0] / 2, D.YB3['x'] + W[0] / 2; yw = W[1] / 2
    pts = []
    for x in np.r_[np.linspace(0.5, 120, 40), np.linspace(121, D.L, 230)]:
        b = float(D.half_beam(x))
        for v in np.linspace(-1, 1, 41):
            pts.append([x, v * b * 0.999])
    for x in np.linspace(0.5, D.L, 400):
        b = float(D.half_beam(x)); pts += [[x, b], [x, -b]]
    for t in np.linspace(0, 1, 40):     # well edges
        pts += [[xw0 + t * (xw1 - xw0), yw], [xw0 + t * (xw1 - xw0), -yw]]
    for t in np.linspace(0, 1, 28):
        pts += [[xw0, -yw + t * 2 * yw], [xw1, -yw + t * 2 * yw]]
    P = np.array(pts)
    inw = (P[:, 0] > xw0 + 0.1) & (P[:, 0] < xw1 - 0.1) & (np.abs(P[:, 1]) < yw - 0.1)
    P = P[~inw]
    from scipy.spatial import Delaunay
    tri = Delaunay(P)
    S = tri.simplices; cen = P[S].mean(1)
    keep = ~((cen[:, 0] > xw0) & (cen[:, 0] < xw1) & (np.abs(cen[:, 1]) < yw))
    keep &= np.abs(cen[:, 1]) <= D.half_beam(cen[:, 0])
    S = S[keep]
    V = np.c_[P, D.deck_z(P[:, 0])]
    S = orient_out(V, S, inside_pt=(750, 0, 0))
    return V, S

def foil_loft(sections, n=90):
    """sections: list of (le_x, chord, t, z, y0). Returns closed loft with flat end caps."""
    rings = []
    for le, c, t, z, y0 in sections:
        xs, ys = D.naca(t, 1.0, n)
        xs, ys = xs[:-1], ys[:-1]
        rings.append(np.c_[le + xs * c, y0 + ys * c, np.full(len(xs), z)])
    m = len(rings[0]); V = np.vstack(rings)
    F = grid_faces(len(rings), m, wrap_v=True)
    for k, ring in ((0, rings[0]), (len(rings) - 1, rings[-1])):
        c0 = len(V); V = np.vstack([V, ring.mean(0)])
        cap = [[c0, k * m + j, k * m + (j + 1) % m] for j in range(m)]
        F = np.vstack([F, cap if k == 0 else [c[::-1] for c in cap]])
    return V, orient_out(V, F)

def fin_mesh():
    Fd = D.FIN; secs = []
    for z in np.linspace(40, Fd['tip_z'], 24):
        s = (z - 0) / Fd['tip_z'] if z < 0 else 0.0
        le = Fd['root_le_x'] + s * (Fd['tip_le_x'] - Fd['root_le_x'])
        c = Fd['root_chord'] + s * (Fd['tip_chord'] - Fd['root_chord'])
        secs.append((le, c, Fd['t'], z, 0.0))
    return foil_loft(secs)

def bulb_mesh():
    B = D.BULB; xl = np.r_[np.linspace(0, 12, 14), np.linspace(13, B['length'] - 10, 90), np.linspace(B['length'] - 9, B['length'], 10)]
    r = D.bulb_radius(xl)
    a = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    rings = [np.c_[np.full(len(a), B['nose_x'] + x), rr * np.cos(a), B['axis_z'] + rr * np.sin(a)] for x, rr in zip(xl, r)]
    V = np.vstack(rings); F = grid_faces(len(xl), len(a), wrap_v=True)
    return V, orient_out(V, F)

def fairing_mesh():
    Fa = D.FAIRING; Fd = D.FIN; secs = []
    for z in np.linspace(Fa['fin_le_z'], Fa['nose_z'], 16):
        s = (z - Fa['fin_le_z']) / (Fa['nose_z'] - Fa['fin_le_z'])
        fin_le = Fd['root_le_x'] + (z / Fd['tip_z']) * (Fd['tip_le_x'] - Fd['root_le_x'])
        le = fin_le + s * (Fa['nose_x'] - fin_le)
        c = (fin_le + 50) - le
        secs.append((le, max(c, 20), 0.12 * (1 - 0.3 * s) * 170 / max(c, 20) * 0.6 + 0.08, z, 0.0))
    return foil_loft(secs, 60)

def wing_mesh():
    Wd = D.WING; le = D.MAST_X - Wd['pivot_from_le']
    secs = [(le, Wd['chord'], Wd['t'], z, 0.0) for z in np.linspace(Wd['root_z'], D.WING_TOP_Z, 12)]
    return foil_loft(secs, 140)

def inner_loft(x0, x1, skin=11.0, nx=40, nt=40):
    rings = []
    for x in np.linspace(x0, x1, nx):
        zk, zd = float(D.keel_z(x)) + skin, float(D.deck_z(x)) - skin
        zz = np.linspace(zk, zd, nt)
        yy = np.array([max(D.half_beam_at(x, z) - skin, 0.5) for z in zz])
        rings.append(np.c_[np.full(2 * nt, x), np.r_[yy, -yy[::-1]], np.r_[zz, zz[::-1]]])
    m = 2 * nt; V = np.vstack(rings); F = grid_faces(nx, m, wrap_v=True)
    for k, ring in ((0, rings[0]), (nx - 1, rings[-1])):
        c0 = len(V); V = np.vstack([V, ring.mean(0)])
        cap = [[c0, k * m + j, k * m + (j + 1) % m] for j in range(m)]
        F = np.vstack([F, cap if k == 0 else [c[::-1] for c in cap]])
    return V, orient_out(V, F)

def section_plate(x, thick, top=None, skin=0.0, nt=50):
    zk, zd = float(D.keel_z(x)) + skin, float(D.deck_z(x)) - skin
    if top is not None:
        zd = min(zd, top)
    zz = np.linspace(zk, zd, nt)
    yy = np.array([max(D.half_beam_at(x, z) - skin, 0.0) for z in zz])
    P = np.c_[np.r_[yy, -yy[::-1]], np.r_[zz, zz[::-1]]]
    v, f = poly_prism(P, -thick / 2, thick / 2)       # in (y, z, x) order
    v = np.c_[v[:, 2] + x, v[:, 0], v[:, 1]]
    return v, orient_out(v, f)


def draped_box(x0, x1, hw, z0, z1, nx=60, ny=12):
    """Thin plate following the deck camber in x: z offsets z0..z1 above deck_z(x)."""
    xs = np.linspace(x0, x1, nx); ys = np.linspace(-hw, hw, ny)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    top = np.c_[X.ravel(), Y.ravel(), D.deck_z(X.ravel()) + z1]
    bot = np.c_[X.ravel(), Y.ravel(), D.deck_z(X.ravel()) + z0]
    ft = grid_faces(nx, ny); fb = ft[:, ::-1] + nx * ny
    V = np.vstack([top, bot]); F = [ft, fb]
    ring = [(i, 0) for i in range(nx)] + [(nx - 1, j) for j in range(1, ny)] + [(i, ny - 1) for i in range(nx - 2, -1, -1)] + [(0, j) for j in range(ny - 2, 0, -1)]
    r = [i * ny + j for i, j in ring]; m = len(r); side = []
    for k in range(m):
        a, b = r[k], r[(k + 1) % m]
        side += [[a, b, a + nx * ny], [b, b + nx * ny, a + nx * ny]]
    F.append(np.array(side))
    F = np.vstack(F)
    return V, orient_out(V, F)

def hatch_lid(x0, x1, hw, hx, hr, t, n=96, nr=10):
    """Rectangular lid with rounded corners and a round hole, draped on the deck camber."""
    cx = (x0 + x1) / 2; hx_ = (x1 - x0) / 2; rc = 14.0
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    def outline(a):
        d = np.array([np.cos(a), np.sin(a)])
        # ray from (hx, 0) to the rounded rectangle centred at (cx, 0)
        lo, hi = 0.0, 1000.0
        for _ in range(40):
            mid = (lo + hi) / 2; p = np.array([hx, 0.0]) + mid * d
            qx = max(abs(p[0] - cx) - (hx_ - rc), 0); qy = max(abs(p[1]) - (hw - rc), 0)
            inside = abs(p[0] - cx) <= hx_ and abs(p[1]) <= hw and np.hypot(qx, qy) <= rc
            lo, hi = (mid, hi) if inside else (lo, mid)
        return np.array([hx, 0.0]) + lo * d
    O = np.array([outline(a) for a in ang]); Hh = np.c_[hx + hr * np.cos(ang), hr * np.sin(ang)]
    rings = [Hh + (O - Hh) * s for s in np.linspace(0, 1, nr)]
    P = np.vstack(rings)
    zt = D.deck_z(P[:, 0]) + t; zb = D.deck_z(P[:, 0])
    top = np.c_[P, zt]; bot = np.c_[P, zb]; N = len(P)
    ft = grid_faces(nr, n, wrap_v=True); fb = ft[:, ::-1] + N
    side = []
    for base in (0, (nr - 1) * n):
        for j in range(n):
            a, b = base + j, base + (j + 1) % n
            side += [[a, b, a + N], [b, b + N, a + N]]
    V = np.vstack([top, bot]); F = np.vstack([ft, fb, side])
    # make winding consistent: top faces up, bottom down, walls by face normals vs local centre
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    m = V[F].mean(1)
    out = np.zeros(len(F))
    k1 = len(ft); k2 = 2 * len(ft)
    out[:k1] = fn[:k1, 2]; out[k1:k2] = -fn[k1:k2, 2]
    for i in range(k2, len(F)):
        rr = m[i, :2] - [hx, 0]
        inner = np.hypot(*rr) < hr + 1
        out[i] = np.dot(fn[i, :2], rr) * (-1 if inner else 1)
    F[out < 0] = F[out < 0][:, ::-1]
    return V, F

# ------------------------------------------------------------------ data assembly
GEOMS = {}; ORDER = []
def add_geom(key, v, f, crease_deg=32.0):
    v2, n2, f2 = crease(v, f, crease_deg)
    GEOMS[key] = (v2, n2, f2); ORDER.append(key)

ASM = []
FLIP_Y = np.diag([1., -1., 1., 1.])
def put(cid, name, group, mat, geom, M=None, explode=(0, 0, 0), info="", ref="", part=None, interior=False):
    # The design frame (x aft, y port, z up) is left-handed. A printed part is placed with an extra local
    # y-flip so that, after the viewer's mirror into a right-handed world, it shows its true (unmirrored) shape.
    if part is not None:
        M = np.asarray(M) @ FLIP_Y
    ASM.append(dict(id=cid, name=name, group=group, mat=mat, geom=geom,
                    m=(np.eye(4) if M is None else np.asarray(M)).T.reshape(-1).round(5).tolist(),
                    ex=list(explode), info=info, ref=ref, part=part, interior=interior))

def stl_geom(stem):
    if stem not in GEOMS:
        v, f = read_stl(os.path.join(HERE, "..", "stl", f"{stem}.stl"))
        add_geom(stem, v, f, 34.0)
    return stem

def main():
    # ---- hull and deck
    hv, hf, tv, tf, _ = hull_mesh()
    add_geom("hull", hv, hf, 50.0); add_geom("transom", tv, tf, 50.0)
    dv, df = deck_mesh(); add_geom("deck", dv, df, 50.0)
    G = "Hull and deck"
    put("hull", "Hull shell", G, "hull", "hull", info="H80 foam strip-plank, 2 x 6 oz glass outside, 1 x 6 oz inside. Hi-vis topsides, boot stripe, copper antifouling below the waterline.", ref="D01, D02, D31")
    put("transom", "Transom", G, "hull", "transom", info="10 mm H80 with 2 + 1 plies; carries the stern-post bracket P06.", ref="D02, T10")
    put("deck", "Deck", G, "deck", "deck", info="10 mm H80, 2 x 6 oz out / 1 in, non-skid. Bonded and taped to the hull.", ref="D08, D31")

    # hatch lid (annulus mesh between the lid outline and the P23 hole) and solar panels, draped on the deck
    H = D.HATCH
    lx0, lx1 = H['x0'] - H['lid_margin'], H['x1'] + H['lid_margin']; lw = H['w'] / 2 + H['lid_margin']
    add_geom("hatchlid", *hatch_lid(lx0, lx1, lw, D.RBPLUS['x'], D.RBPLUS['bowl_od'] / 2 + 0.5, 8.0), 40)
    put("hatch_lid", "Hatch lid", G, "deckpaint", "hatchlid", explode=(0, 0, 160),
        info="Bolted with 12 x M5 into bonded inserts on 4 mm EPDM cord. Carries the RockBLOCK bowl P23, a membrane vent and a Schrader test valve.", ref="D08, T16")
    for k, S in enumerate(D.SOLAR):
        SP = D.SOLAR_PANEL; cx = (S['x0'] + S['x1']) / 2          # Rev E3: stock 10 W panel centred in the bay
        add_geom(f"solar{k+1}", *draped_box(cx - SP['l'] / 2, cx + SP['l'] / 2, SP['w'] / 2, 0.4, 0.4 + SP['t']), 40)
        put(f"solar{k+1}", f"Solar panel {k+1}", "Power and electronics", "solar", f"solar{k+1}", explode=(0, 0, 120),
            info="Rev E3: PV Logic STPVF010 10 W ETFE flexi panel, 380 x 250 x 4, bonded in its deck bay; 20 W in all (run 027: no measurable cost).", ref="D01, D08, D30")
    # well walls + floor
    W = D.YB3['well']; xw0, xw1 = D.YB3['x'] - W[0] / 2, D.YB3['x'] + W[0] / 2; yw = W[1] / 2
    zt = float(D.deck_z(D.YB3['x'])); zb = zt - W[2]; zwell = zb
    wall = merge(box(xw0, xw1, yw, yw + 3, zb, zt), box(xw0, xw1, -yw - 3, -yw, zb, zt),
                 box(xw0 - 3, xw0, -yw - 3, yw + 3, zb, float(D.deck_z(xw0))), box(xw1, xw1 + 3, -yw - 3, yw + 3, zb, zt),
                 box(xw0, xw1, -yw, yw, zb - 3, zb))
    add_geom("well", *wall, 40)
    rim_v, rim_f = merge(box(xw0 - 6, xw1 + 6, yw, yw + 6, 0, 1.5), box(xw0 - 6, xw1 + 6, -yw - 6, -yw, 0, 1.5),
                         box(xw0 - 6, xw0, -yw, yw, 0, 1.5), box(xw1, xw1 + 6, -yw, yw, 0, 1.5))
    rim_v[:, 2] += D.deck_z(rim_v[:, 0])
    add_geom("wellrim", rim_v, rim_f, 40)
    put("yb3_well", "YB3 well", G, "deckpaint", "well", info="Glassed well in the foredeck, 176 x 106 x 38, drains aft.", ref="D07, D08")
    put("yb3_rim", "YB3 well rim", G, "deckpaint", "wellrim", info="", ref="D08")

    # ---- keel and ballast
    G = "Keel and ballast"
    add_geom("fin", *fin_mesh(), 40); add_geom("bulb", *bulb_mesh(), 60); add_geom("fairing", *fairing_mesh(), 40)
    put("fin", "Keel fin", G, "antifoul", "fin", explode=(0, 0, -260), info="NACA 0012, 170/150 chord, 430 deep. Hardwood core, carbon strip and 6 x 6 oz each side; 60 mm tenon into the keel box, two M10 rods.", ref="D04, T12, T13")
    put("bulb", "Lead bulb", G, "antifoul", "bulb", explode=(0, 0, -470), info=f"Cast lead, D72 x 320, about {D.bulb_mass()[1]:.1f} kg, from pattern P14 in a plaster mould. Slotted onto the fin tip.", ref="D04, P14")
    put("fairing", "Weed fairing", G, "antifoul", "fairing", explode=(0, 0, -365), info="XPS + glass ramp from the fin leading edge to the bulb nose, so weed and line slide off.", ref="D04, T21")

    # ---- rig
    G = "Wing-sail rig"; EXR = (0, 0, 520)
    add_geom("wing", *wing_mesh(), 40)
    put("wing", "Wing sail", G, "wing", "wing", explode=(0, 0, 640), info="NACA 0015, 375 chord x 800 span, XPS core with 2 x 6 oz glass and 3 mm ply end caps. Free-pivoting on the spar 82 mm from the leading edge.", ref="D06, T15")
    sp_v, sp_f = tube(D.SPAR_OD / 2, D.SPAR_ID / 2, D.SPAR_BOT_Z, D.WING_TOP_Z + 4, 48)
    add_geom("spar", sp_v + [D.MAST_X, 0, 0], sp_f, 40)
    put("spar", "Wing spar", G, "carbon", "spar", explode=EXR, info="Carbon tube 30 x 22, 995 long, on two 6806 acetal bearings in P07 (open item: special-order size).", ref="D06, D07")
    xb0 = D.MAST_X + 16; xp = D.MAST_X + D.BOOM['length']; x09 = xp - 62
    bv, bf = cylinder(D.BOOM['od'] / 2, 0, (x09 + 28) - xb0, 32)
    add_geom("boom", xf(bv, T(axis_x(), (xb0, 0, D.BOOM['z']))), bf, 40)
    put("boom", "Tail boom", G, "carbon", "boom", explode=EXR, info="Carbon tube 16 x 14 (Rev E1), spar axis to tail pivot 600.", ref="D06")
    cw0 = 300 + 32; cw1 = D.MAST_X - 26
    cv_, cf_ = cylinder(6, 0, cw1 - cw0, 24)
    add_geom("cwarm", xf(cv_, T(axis_x(), (cw0, 0, D.CWARM['z']))), cf_, 40)
    put("cwarm", "Counterweight arm", G, "frp", "cwarm", explode=EXR, info="12 mm solid pultruded fibreglass rod, 244 long (Rev C3).", ref="D06")
    lead_v, lead_f = cylinder(27, 3, 60, 40)
    add_geom("cwlead", lead_v + [300, 0, D.CWARM['pod_bot_z']], lead_f, 40)
    put("cwlead", "Counterweight lead", G, "lead", "cwlead", explode=EXR, interior=True, info="About 0.91 kg of lead shot in epoxy inside P18.", ref="D06")
    tp_v, tp_f = cylinder(3, 300, 522, 20)
    add_geom("tailpivot", tp_v + [xp, 0, 0], tp_f, 40)
    put("tailpivot", "Tail pivot rod", G, "carbon", "tailpivot", explode=EXR, info="6 mm carbon rod through both tail halves.", ref="D06")
    # printed rig parts
    put("P07", "P07 Mast bearing housing", G, "petg", stl_geom("P07_mast_bearing_housing"), T(RX180, (D.MAST_X, 0, D.MAST_TUBE['top_z'])), explode=(0, 0, 260), part="P07",
        info="Bonded into the top of the mast tube; two floating 6806 acetal bearings and plain catcher lands.", ref="D07")
    put("P08", "P08 Spar clamp", G, "asa", stl_geom("P08_spar_clamp_two_sockets"), T(np.eye(3), (D.MAST_X, 0, D.BOOM['z'] - 13)), explode=EXR, part="P08",
        info="Clamps the spar; takes the tail boom aft and the counterweight arm forward.", ref="D06")
    put("P09", "P09 Tail servo housing", G, "asa", stl_geom("P09_tail_servo_housing"), T(np.eye(3), (x09, 0, D.BOOM['z'] - 14)), explode=EXR, part="P09",
        info="On the aft end of the boom; holds the potted tail servo output-up.", ref="D06")
    ztail = D.BOOM['z'] - 14 + 48 + 6
    put("P10a", "P10 Tail fin, lower", G, "wing", stl_geom("P10a_tail_fin_lower"), T(np.eye(3), (xp - 24, 0, ztail)), explode=EXR, part="P10",
        info="NACA 0012, 120 chord, printed and glassed; bonded to the servo horn.", ref="D06")
    put("P10b", "P10 Tail fin, upper", G, "wing", stl_geom("P10b_tail_fin_upper"), T(np.eye(3), (xp - 24, 0, ztail + 100)), explode=EXR, part="P10", ref="D06",
        info="Upper half, joined with the pivot rod and a 3 mm carbon pin.")
    put("P25", "P25 Tail detent", G, "petg", stl_geom("P25_tail_detent"), T(np.eye(3), (xp, 0, ztail - 5.5)), explode=EXR, part="P25",
        info="Two magnets that hold the tail at +/-8 deg if its servo dies.", ref="D06")
    put("P18", "P18 Counterweight pod", G, "asa", stl_geom("P18_counterweight_pod"), T(np.eye(3), (300, 0, D.CWARM['pod_bot_z'])), explode=EXR, part="P18",
        info="Holds about 0.91 kg of lead; balances the wing and tail on the spar axis.", ref="D06")

    # ---- stern post
    G = "Stern post"; S = D.STUB; EXS = (260, 0, 0)
    sv, sf = tube(S['od'] / 2, S['od'] / 2 - 2, S['bot_z'], S['top_z'], 32)
    add_geom("stub", sv + [S['x'], 0, 0], sf, 40)
    put("stub", "Stern post", G, "frp", "stub", explode=EXS, info="20 x 2 pultruded fibreglass tube, 500 long (Rev C3): bends rather than kinks.", ref="D07")
    rr_v, rr_f = merge(cylinder(30, 330, 470, 8), tube(31, 10.5, 395, 405, 8))
    add_geom("radar", rr_v + [S['x'], 0, 0], rr_f, 20)
    put("radar", "Radar reflector", G, "white", "radar", explode=EXS, info="Davis Emergency Radar Reflector 151, lashed to the post at z 330-470.", ref="D07")
    put("P06", "P06 Transom bracket", G, "asa", stl_geom("P06_transom_bracket"), T(CYC, (D.L - 2, 0, 130)), explode=(120, 0, 0), part="P06",
        info="Bolted through the transom with 4 x M5; two M4 set screws grip the post.", ref="D07")
    put("P05", "P05 Antenna platform", G, "asa", stl_geom("P05_antenna_platform"), T(Rz(180), (S['x'], 0, 548)), explode=EXS, part="P05",
        info="Main GPS + compass (Holybro Micro M10) bonded under the plate.", ref="D07")
    gv, gf = cylinder(12.5, -9, 0, 32)
    add_geom("gps", xf(gv, T(np.eye(3), (S['x'] - 50, 0, 548))), gf, 40)
    put("gps", "Main GPS (Micro M10)", G, "black", "gps", explode=EXS, info="Holybro Micro M10 GPS + IST8310 compass, potted in soft silicone.", ref="D07, D30")
    put("P20", "P20 Nav light clamp", G, "asa", stl_geom("P20_nav_light_clamp"), T(np.eye(3), (S['x'], 0, 585)), explode=EXS, part="P20",
        info="All-round white light on a 45 mm arm.", ref="D07")
    lv, lf = merge(cylinder(15, 0, 6, 32), cylinder(14, 6, 16, 32, r1=8))
    add_geom("navlight", lv + [S['x'] + 45, 0, 585 + 11], lf, 30)
    put("navlight", "Navigation light", G, "lamp", "navlight", explode=EXS, info="12 V all-round white LED puck.", ref="D07, D30")
    zc = S['top_z'] - 29
    put("P03", "P03 Sensor cap", G, "asa", stl_geom("P03_sensor_cap"), T(np.eye(3), (S['x'], 0, zc)), explode=EXS, part="P03",
        info="Caps the post; carries the AS5600 board under the vane magnet.", ref="D07")
    z01 = zc + 34
    put("P01", "P01 Wind-vane housing", G, "asa", stl_geom("P01_vane_housing"), T(np.eye(3), (S['x'], 0, z01)), explode=(260, 0, 30), part="P01",
        info="Two S608 stainless bearings and spacer P27 in one D22.1 bore (E2).", ref="D07")
    put("P27", "P27 Vane bearing spacer", G, "petg", stl_geom("P27_vane_bearing_spacer"), T(np.eye(3), (S['x'], 0, z01 + 43)), explode=(260, 0, 30), part="P27", interior=True,
        info="Between the two vane bearings (E2).", ref="D07")
    for k, zbr in enumerate((z01 + 36, z01 + 53)):
        bv2, bf2 = tube(11, 4, zbr, zbr + 7, 32)
        add_geom(f"s608_{k}", bv2 + [S['x'], 0, 0], bf2, 40)
        put(f"s608_{k}", "S608-2RS bearing", G, "steel", f"s608_{k}", explode=(260, 0, 30), interior=True, info="Stainless 8 x 22 x 7.", ref="D07")
    put("P04", "P04 Magnet holder", G, "petg", stl_geom("P04_magnet_holder"), T(np.eye(3), (S['x'], 0, z01 + 23)), explode=(260, 0, 30), part="P04", interior=True,
        info="Diametric magnet on the end of the vane shaft, over the AS5600.", ref="D07")
    shv, shf = cylinder(4, z01 + 24, z01 + 69, 20)
    add_geom("vaneshaft", shv + [S['x'], 0, 0], shf, 40)
    put("vaneshaft", "Vane shaft", G, "steel", "vaneshaft", explode=(260, 0, 30), interior=True, info="8 mm 316 stainless.", ref="D07")
    put("P02", "P02 Wind-vane arm", G, "asa", stl_geom("P02_vane_arm"), T(RX180, (S['x'], 0, z01 + 70)), explode=(260, 0, 60), part="P02",
        info="Vane arm with fin and lead counterweight; hub set-screwed to the shaft.", ref="D07")

    # ---- deck fittings
    G = "Deck fittings"; EXD = (0, 0, 160)
    zlid = float(D.deck_z(D.RBPLUS['x'])) + 8
    put("P23", "P23 RockBLOCK bowl", G, "asa", stl_geom("P23_rockblock_plus_bowl"), T(np.eye(3), (D.RBPLUS['x'], 0, zlid - 40)), explode=EXD, part="P23",
        info="Bonded into a D146 hole in the hatch lid; holds the RockBLOCK Plus with 4 x M5.", ref="D08")
    rbv, rbf = merge(cylinder(D.RBPLUS['dia'] / 2, 0, 34, 64), cylinder(D.RBPLUS['dia'] / 2 - 4, 34, 37, 64, r1=D.RBPLUS['dia'] / 2 - 12))
    add_geom("rockblock", rbv + [D.RBPLUS["x"], 0, zlid - 32], rbf, 40)
    put("rockblock", "RockBLOCK Plus", G, "darkgrey", "rockblock", explode=EXD, info="Iridium SBD modem, IP67 puck; RS-232 to the main box.", ref="D08, D30")
    Y = D.YB3
    put("P19", "P19 YB3 platform", G, "asa", stl_geom("P19_yb3_platform"), T(np.eye(3), (Y['x'], 0, zwell)), explode=EXD, part="P19",
        info="In the foredeck well; straps hold the YB3.", ref="D07")
    yv, yf = rbox(-Y['box'][0] / 2, Y['box'][0] / 2, -Y['box'][1] / 2, Y['box'][1] / 2, 0, Y['box'][2], 8)
    add_geom("yb3", yv + [Y['x'], 0, zwell + 5], yf, 35)
    put("yb3", "YB3 tracker", G, "yellow", "yb3", explode=EXD, info="Independent backup tracker with its own battery and Iridium link.", ref="D07")
    for k, (vx, vy) in enumerate(D.VENTS[:1]):
        vv, vf = cylinder(8, 0, 6, 24)
        add_geom(f"vent{k}", vv + [vx, vy, float(D.deck_z(vx)) + 8], vf, 40)
        put(f"vent{k}", "Membrane vent", G, "steel", f"vent{k}", explode=EXD, info="Amphenol M12 IP68 vent: pressure equalisation without water.", ref="D08")
    tvx, tvy = D.TEST_VALVE
    sv2, sf2 = cylinder(4, 0, 9, 20)
    add_geom("schrader", sv2 + [tvx, tvy, float(D.deck_z(tvx)) + 8], sf2, 40)
    put("schrader", "Schrader test valve", G, "black", "schrader", explode=EXD, info="For the pressure-decay leak test; capped at sea.", ref="D08")
    Po = D.PUMP_OUTLET
    ov, of_ = merge(cylinder(9, 0, 2, 24), cylinder(5, 2, 8, 24))
    add_geom("deckfitting", ov + [Po['x'], Po['y'], float(D.deck_z(Po['x']))], of_, 40)
    put("deckfitting", "Pump outlet fitting", G, "white", "deckfitting", explode=EXD, info="1/4 in through-deck fitting, after a check valve and a loop to z 226.", ref="D03")
    mtv, mtf = tube(D.MAST_TUBE['od'] / 2, D.MAST_TUBE['id'] / 2, 2, D.MAST_TUBE['top_z'], 48)
    add_geom("masttube", mtv + [D.MAST_X, 0, 0], mtf, 40)
    put("masttube", "Mast tube", "Interior structure", "pvc", "masttube", info="2 in. schedule 40 PVC, glassed to hull and deck; P07 bonds into its top.", ref="D03, D07")

    # ---- steering
    G = "Steering"; EXR2 = (0, 0, -240)
    R = D.RUDDER; xle = R['stock_x'] - R['stock_from_le']
    for side, y in (("port", 100.0), ("stbd", -100.0)):
        sgn = 1 if y > 0 else -1
        put(f"P13a_{side}", f"P13 Rudder core, upper ({side})", G, "antifoul", stl_geom("P13a_rudder_core_upper"), T(np.eye(3), (xle, y, R['top_z'] - 115)), explode=EXR2, part="P13",
            info="Printed core, 2 x 6 oz glass over it, pinned to the 12 mm stock with two 4 mm pins.", ref="D05")
        put(f"P13b_{side}", f"P13 Rudder core, lower ({side})", G, "antifoul", stl_geom("P13b_rudder_core_lower"), T(np.eye(3), (xle, y, R['bot_z'])), explode=EXR2, part="P13",
            info="Lower half of the rudder blade.", ref="D05")
        stv, stf = cylinder(R['stock_d'] / 2, R['bot_z'] + 8, 200, 24)
        add_geom(f"stock_{side}", stv + [R['stock_x'], y, 0], stf, 40)
        put(f"stock_{side}", f"Rudder stock ({side})", G, "steel", f"stock_{side}", explode=EXR2, interior=True, info="12 mm 316 bar, 360 long.", ref="D05")
        zh = D.hull_z_at(R['stock_x'], y)
        trv, trf = tube(8, 7, zh - 2, R['trunk_top_z'], 24)
        add_geom(f"trunk_{side}", trv + [R['stock_x'], y, 0], trf, 40)
        put(f"trunk_{side}", f"Rudder trunk ({side})", G, "steel", f"trunk_{side}", interior=True, info="316 tube 16 x 1 (or GRP, 14 ID) with two igus JFM-1214 bushings.", ref="D05")
        put(f"P11_{side}", f"P11 Tiller arm ({side})", G, "petg", stl_geom("P11_tiller_arm"), T(Rz(-90 * sgn), (R['stock_x'], y, 182)), explode=(0, 0, 330), part="P11", interior=True,
            info="Clamped and pinned to the stock; pushrod holes at 35/45/55.", ref="D05, D32")
        zc12 = 105
        put(f"P12_{side}", f"P12 Servo cradle ({side})", G, "petg", stl_geom("P12_rudder_servo_cradle"), T(np.eye(3), (1330, y, zc12)), explode=(0, 0, 330), part="P12", interior=True,
            info="Holds the sealed SER-2000 servo output-up in the aft-foam pocket (E2 base fits the pocket).", ref="D05")
        Sx = D.SER
        sev, sef = merge(rbox(-Sx['l'] / 2, Sx['l'] / 2, -Sx['w'] / 2, Sx['w'] / 2, 0, Sx['h'], 3), cylinder(5, Sx['h'], Sx['h'] + 4, 20))
        add_geom(f"ser_{side}", sev + [1330, y, zc12 + 5], sef, 35)
        put(f"ser_{side}", f"SER-2000 sealed servo ({side})", G, "alu", f"ser_{side}", explode=(0, 0, 330), interior=True,
            info="Blue Trail SER-2000 housing around a DFRobot 25 kg magnetic-encoder servo (size is an estimate).", ref="D05")
        zarm = zc12 + 5 + Sx['h'] + 4
        put(f"P26_{side}", f"P26 Servo arm ({side})", G, "petg", stl_geom("P26_rudder_servo_arm"), T(Rz(-90 * sgn), (1330, y, zarm)), explode=(0, 0, 330), part="P26", interior=True,
            info="Clamps the SER-2000's 6 mm D-shaft; holes at 20/25/30.", ref="D05, D32")
        p0 = np.array([1330, y - sgn * 30, zarm + 3]); p1 = np.array([R['stock_x'], y - sgn * 45, 185])
        d = p1 - p0; Lr = np.linalg.norm(d); zaxis = d / Lr
        xa = np.cross([0, 0, 1], zaxis); xa /= np.linalg.norm(xa); ya = np.cross(zaxis, xa)
        Rm = np.c_[xa, ya, zaxis]
        prv, prf = merge(cylinder(1.0, 0, Lr, 12), cylinder(3.5, Lr * 0.3, Lr * 0.7, 20))
        add_geom(f"pushrod_{side}", xf(prv, T(Rm, p0)), prf, 40)
        put(f"pushrod_{side}", f"Pushrod + spring link ({side})", G, "brass", f"pushrod_{side}", explode=(0, 0, 330), interior=True, info="M2 316 rod with the spring overload link (D32).", ref="D32")

    # ---- interior structure
    G = "Interior structure"
    for x, nm in ((300.0, "Bulkhead x 300"), (1260.0, "Bulkhead x 1260")):
        k = f"bh{int(x)}"
        add_geom(k, *section_plate(x, 10, skin=10), 30)
        put(k, nm, G, "h80", k, interior=True, info="10 mm H80, glassed in with 50 mm tapes both sides (T17/T18).", ref="D03, D09")
    for x, top in D.FLOORS:
        k = f"floor{int(x)}"
        add_geom(k, *section_plate(x, 9, top=top, skin=10), 30)
        put(k, f"Floor x {int(x)}", G, "ply", k, interior=True, info="9 mm marine ply floor across the hull at the keel box.", ref="D04, T19, T20")
    K = D.KEELBOX
    kv, kf = merge(box(K['x0'], K['x1'], -K['w'] / 2 - 6, -K['w'] / 2, 2, K['h']), box(K['x0'], K['x1'], K['w'] / 2, K['w'] / 2 + 6, 2, K['h']),
                   box(K['x1'], K['x1'] + 6, -K['w'] / 2 - 6, K['w'] / 2 + 6, 2, K['h']), box(K['x0'] - 6, K['x0'], -K['w'] / 2 - 6, K['w'] / 2 + 6, 2, K['h']))
    add_geom("keelbox", kv, kf, 30)
    put("keelbox", "Keel box", G, "glass", "keelbox", interior=True, info="Glass socket cast round the waxed fin tenon, 60 deep.", ref="D04")
    pv, pf = box(K['x0'], K['x1'], -K['w'] / 2, K['w'] / 2, K['h'], K['h'] + K['plate_t'])
    add_geom("g10plate", pv, pf, 30)
    put("g10plate", "G10 plate + fin rods", G, "g10", "g10plate", interior=True, info="122 x 60 x 10 G10 taking the two M10 rod nuts.", ref="D04")
    for k, x in enumerate(D.FIN_BUILD['rods_x']):
        nv_, nf_ = merge(cylinder(5, -400, K['h'] + 22, 16), cylinder(8.5, K['h'] + 10, K['h'] + 18, 6))
        add_geom(f"rod{k}", nv_ + [D.FIN['root_le_x'] + x, 0, 0], nf_, 40)
        put(f"rod{k}", "M10 fin rod", G, "steel", f"rod{k}", interior=True, info="M10 316 threaded rod bedded in the fin.", ref="D04")
    add_geom("foam_bow", *inner_loft(14, 295), 60)
    put("foam_bow", "Bow foam fill", G, "xps", "foam_bow", interior=True, info="Sealed compartment ahead of bulkhead x 300, filled with XPS blocks.", ref="D09")
    add_geom("foam_stern", *inner_loft(1265, 1489), 60)
    put("foam_stern", "Stern foam fill", G, "xps", "foam_stern", interior=True, info="Sealed compartment aft of bulkhead x 1260, XPS with fitted pockets for the two servos.", ref="D09")
    put("P24", "P24 Bilge-pump spacer", G, "petg", stl_geom("P24_bilge_pump_spacer"), T(Rz(180), (D.MAST_X, 0, 35)), part="P24", interior=True,
        info="Holds the diaphragm pump upright against the port side of the mast tube.", ref="D03")
    pmv, pmf = merge(cylinder(14, 0, 62, 32), cylinder(5, 62, 72, 16))
    add_geom("pump", pmv + [D.PUMP['x'], D.PUMP['y'], 32], pmf, 40)
    put("pump", "Bilge pump", G, "black", "pump", interior=True, info="12 V R385 diaphragm pump, self-priming, pickup at the sump low point.", ref="D03, D30")
    for k, (x, y) in enumerate(((700, 0), (1488, 25), (1488, -25), (D.MAST_X - 31, 0))):
        if k == 0:
            M = T(RX180, (x, y, D.DECK_Z - 10))
        elif k in (1, 2):
            M = T(np.array([[0., 0., -1.], [0., 1., 0.], [1., 0., 0.]]), (x, y, 185))
        else:
            M = T(np.array([[0., 0., -1.], [0., 1., 0.], [1., 0., 0.]]), (x, 0, 180))
        put(f"P17_{k}", "P17 Penetrator pad", G, "petg", stl_geom("P17_penetrator_pad_x4"), M, part="P17", interior=True,
            info="Flat seat for a WetLink penetrator on a curved or thin wall.", ref="D30")

    # ---- power and electronics
    G = "Power and electronics"
    B = D.BATTBOX
    bbv, bbf = rbox(B['x0'], B['x1'], -B['w'] / 2, B['w'] / 2, B['z0'], B['z1'], 6)
    add_geom("battbox", bbv, bbf, 35)
    put("battbox", "Battery box", G, "glassbox", "battbox", explode=(0, 0, 420), interior=True, info="Sealed 10 mm H80 box with an O-ring lid, strapped down on P16; lifts out through the hatch.", ref="D09, D32")
    Bt = D.BATTERY
    btv, btf = rbox(Bt['x0'], Bt['x1'], -Bt['w'] / 2, Bt['w'] / 2, B['z0'] + 4, B['z0'] + 4 + Bt['h'], 5)
    add_geom("battery", btv, btf, 35)
    put("battery", "Battery 12.8 V 15 Ah", G, "battery", "battery", explode=(0, 0, 420), interior=True, info="Bioenno BLF-1215A LiFePO4, PVC pack.", ref="D09, D30")
    for k, (x, y) in enumerate(((800, 62), (800, -62), (940, 62), (940, -62))):
        put(f"P16_{k}", "P16 Battery strap anchor", G, "petg", stl_geom("P16_battery_strap_anchor_x4"), T(Rz(90), (x, y, 22)), part="P16", interior=True,
            info="Four anchors glassed to the hull floor take the battery-box straps.", ref="D09")
    E = D.EBOX
    shv2, shf2 = box(E['x0'], E['x1'], -E['w'] / 2 - 5, E['w'] / 2 + 5, 60, E['z0'])
    add_geom("shelf", shv2, shf2, 30)
    put("shelf", "Electronics shelf", G, "h80", "shelf", interior=True, info="Glassed foam shelf: box bottom at z 118, 70 mm above the sump.", ref="D03")
    ebv, ebf = rbox(E['x0'], E['x1'], -E['w'] / 2, E['w'] / 2, E['z0'], E['z0'] + E['h'] - 8, 6)
    add_geom("ebox", ebv, ebf, 35)
    put("ebox", "Electronics box", G, "hammond", "ebox", explode=(0, 0, 380), interior=True, info="Hammond 1554V2GYCL, IP68 polycarbonate.", ref="D03, D30")
    elv, elf = rbox(E['x0'], E['x1'], -E['w'] / 2, E['w'] / 2, E['z0'] + E['h'] - 8, E['z0'] + E['h'], 6)
    add_geom("eboxlid", elv, elf, 35)
    put("eboxlid", "Electronics box lid", G, "clearlid", "eboxlid", explode=(0, 0, 470), interior=True, info="Clear lid with cable glands and a membrane vent.", ref="D03")
    xc = (E['x0'] + E['x1']) / 2; zt = E['z0'] + 4
    put("P15", "P15 Electronics tray", G, "petg", stl_geom("P15_electronics_tray"), T(np.eye(3), (xc, 0, zt)), explode=(0, 0, 400), part="P15", interior=True,
        info="Slotted tray for zip ties and Dual Lock inside the box.", ref="D03")
    boards = [("pixhawk", "Pixhawk 6C Mini", (xc - 50, 20), (53, 39, 16), "alu"),
              ("esp32", "Companion ESP32-S3", (xc + 40, 35), (51, 23, 7), "pcb"),
              ("gv5", "Genasun GV-5 MPPT", (xc + 35, -30), (75, 50, 22), "black"),
              ("pm02", "PM02 power module", (xc - 55, -30), (35, 25, 10), "pcb"),
              ("regs", "6 V / 5 V regulators", (xc - 5, -40), (30, 20, 8), "pcbblue"),
              ("max3232", "MAX3232 + INA260s", (xc - 5, 45), (25, 18, 6), "pcbred")]
    for key, nm, (x, y), (l, w, h), mat in boards:
        bv3, bf3 = rbox(x - l / 2, x + l / 2, y - w / 2, y + w / 2, zt + 6, zt + 6 + h, 1.5)
        add_geom(key, bv3, bf3, 35)
        put(key, nm, G, mat, key, explode=(0, 0, 400), interior=True, info="Inside the sealed main box (D30).", ref="D30")
    put("P21", "P21 Limp-home case", G, "petg", stl_geom("P21_limp_home_case"), T(CYC, (D.LHC['x0'], 0, (D.LHC['z0'] + D.LHC['z1']) / 2)), part="P21", interior=True,
        info="Potted limp-home controller (own ESP32, GPS, BNO085, fused feed) on bulkhead x 300.", ref="D03, D30")
    Mx = D.MUXPOD
    put("P22", "P22 Switchover pod", G, "petg", stl_geom("P22_switchover_pod"),
        T(np.array([[0., 0., -1.], [1., 0., 0.], [0., -1., 0.]]), (Mx['x1'], Mx['y'], (Mx['z0'] + Mx['z1']) / 2)), part="P22", interior=True,
        info="Servo multiplexer and ideal diodes, potted, on bulkhead x 1260.", ref="D03, D30")
    fills = {"P21": "darkgrey", "P22": "darkgrey"}

    # ---- parts catalogue
    guide = {r["file"][4:-4]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "Print_Guide.csv")))}
    catalogue = []
    for stem, pid, kw in Pm.BUILD:
        P = Pm.PARTS[pid]; g = guide.get(stem, {})
        stl_geom(stem)
        catalogue.append(dict(stem=stem, pid=pid, name=P["name"], qty=g.get("qty", ""), mat=P["mat"], notes=P["notes"],
                              dims={k: str(v) for k, v in P.get("dims", {}).items()},
                              print=dict(material=g.get("material", ""), walls=g.get("walls", ""), infill=g.get("infill", ""),
                                         orientation=g.get("orientation", ""), supports=g.get("supports", ""), size=g.get("size_mm", ""),
                                         grams=g.get("grams_each", ""), hours=g.get("hours_each", ""), bed=g.get("min_bed", ""))))

    # ---- write binary
    blob = bytearray(); meta = {}
    def align():
        while len(blob) % 4: blob.append(0)
    for key in ORDER:
        v, n, f = GEOMS[key]
        lo = v.min(0); hi = v.max(0); sc = np.maximum(hi - lo, 1e-6) / 65535.0
        q = np.round((v - lo) / sc - 32768).astype(np.int16)
        nq = np.round(n * 127).astype(np.int8)
        align(); po = len(blob); blob += q.tobytes()
        align(); no = len(blob); blob += nq.tobytes()
        align(); io = len(blob)
        if len(v) < 65536:
            blob += f.astype(np.uint16).tobytes(); it = 16
        else:
            blob += f.astype(np.uint32).tobytes(); it = 32
        meta[key] = dict(nv=len(v), nf=len(f), pos=po, nrm=no, idx=io, it=it,
                         lo=lo.round(4).tolist(), sc=sc.tolist(), hi=hi.round(3).tolist())
    # The artifact host serves text formats only, so the binary buffer travels base64-encoded inside the JSON.
    import base64
    out = dict(bin=base64.b64encode(bytes(blob)).decode("ascii"), version="E3", date="2026-11-23", dwl=D.DWL, L=D.L, mass=D.MASS_KG, geoms=meta, assembly=ASM, parts=catalogue,
               deck=dict(z=D.DECK_Z), mast=dict(x=D.MAST_X), rudder=dict(x=D.RUDDER['stock_x'], y=D.RUDDER_Y))
    json.dump(out, open(os.path.join(OUT, "model.json"), "w"), separators=(",", ":"))
    tris = sum(m["nf"] for m in meta.values())
    print(f"{len(meta)} geoms, {len(ASM)} placed, {tris} tris, buffer {len(blob)/1e6:.2f} MB, model.json {os.path.getsize(os.path.join(OUT,'model.json'))/1e6:.2f} MB")

if __name__ == "__main__":
    main()
