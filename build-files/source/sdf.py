"""Tiny axis-aligned SDF CSG kit evaluated on regular grids, meshed with marching cubes.
A shape is a function f(X, Y, Z) -> distance (negative inside), where X, Y, Z are
broadcastable arrays. 2D profiles are evaluated with polygon distance."""
import numpy as np
from skimage.measure import marching_cubes
import struct

# ---------- 2D --------------------------------------------------------------
def poly_sdf2(px, py, P):
    """Signed distance from points (px, py) to closed polygon P (N,2). Negative inside."""
    px = np.asarray(px, float); py = np.asarray(py, float)
    shp = np.broadcast(px, py).shape
    px = np.broadcast_to(px, shp).ravel(); py = np.broadcast_to(py, shp).ravel()
    d = np.full(px.shape, np.inf); s = np.ones(px.shape)
    A = P; B = np.roll(P, -1, axis=0)
    for (ax, ay), (bx, by) in zip(A, B):
        ex, ey = bx - ax, by - ay
        wx, wy = px - ax, py - ay
        h = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey + 1e-12), 0, 1)
        dx, dy = wx - ex * h, wy - ey * h
        d = np.minimum(d, dx * dx + dy * dy)
        c1 = py >= ay; c2 = py < by; c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        s = np.where(flip, -s, s)
    return (s * np.sqrt(d)).reshape(shp)

def circle_pts(r, n=96, cx=0, cy=0):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[cx + r * np.cos(a), cy + r * np.sin(a)]

def rect_pts(w, h, cx=0, cy=0):
    return np.array([[cx - w/2, cy - h/2], [cx + w/2, cy - h/2], [cx + w/2, cy + h/2], [cx - w/2, cy + h/2]])

def rounded_rect_pts(w, h, r, cx=0, cy=0, n=12):
    pts = []
    for (sx, sy, a0) in [(1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)]:
        ccx, ccy = cx + sx * (w/2 - r), cy + sy * (h/2 - r)
        for a in np.radians(np.linspace(a0, a0 + 90, n)):
            pts.append([ccx + r*np.cos(a), ccy + r*np.sin(a)])
    return np.array(pts)

# ---------- 3D primitives (all axis aligned) --------------------------------
def _extrude(d2, w, h):
    q = np.stack(np.broadcast_arrays(d2, w), 0)
    outside = np.sqrt(np.maximum(q[0], 0)**2 + np.maximum(q[1], 0)**2)
    return outside + np.minimum(np.maximum(q[0], q[1]), 0)

def prism(P, z0, z1, axis='z'):
    """Extrude 2D polygon P between z0..z1 along axis. P coords are the other two axes
    in cyclic order: z->(x,y), x->(y,z), y->(z,x)."""
    P = np.asarray(P, float); zc, hz = (z0 + z1) / 2, (z1 - z0) / 2
    def f(X, Y, Z):
        if axis == 'z': a, b, c = X, Y, Z
        elif axis == 'x': a, b, c = Y, Z, X
        else: a, b, c = Z, X, Y
        return _extrude(poly_sdf2(a, b, P), np.abs(c - zc) - hz, None)
    return f

def box(x0, x1, y0, y1, z0, z1):
    c = np.array([(x0+x1)/2, (y0+y1)/2, (z0+z1)/2]); h = np.array([(x1-x0)/2, (y1-y0)/2, (z1-z0)/2])
    def f(X, Y, Z):
        qx, qy, qz = np.abs(X-c[0])-h[0], np.abs(Y-c[1])-h[1], np.abs(Z-c[2])-h[2]
        o = np.sqrt(np.maximum(qx,0)**2 + np.maximum(qy,0)**2 + np.maximum(qz,0)**2)
        return o + np.minimum(np.maximum(qx, np.maximum(qy, qz)), 0)
    return f

def cyl(r, a0, a1, axis='z', c1=0.0, c2=0.0):
    """Cylinder radius r along axis from a0..a1, centred at (c1, c2) in the other axes (cyclic)."""
    def f(X, Y, Z):
        if axis == 'z': u, v, w = X, Y, Z
        elif axis == 'x': u, v, w = Y, Z, X
        else: u, v, w = Z, X, Y
        d2 = np.sqrt((u - c1)**2 + (v - c2)**2) - r
        return _extrude(d2, np.abs(w - (a0+a1)/2) - (a1-a0)/2, None)
    return f

def revolve(rfunc, a0, a1, axis='x', c1=0.0, c2=0.0):
    """Body of revolution along axis, radius rfunc(a - a0) for a in a0..a1 (approximate SDF)."""
    def f(X, Y, Z):
        if axis == 'x': w, u, v = X, Y, Z
        elif axis == 'y': w, u, v = Y, Z, X
        else: w, u, v = Z, X, Y
        rr = np.sqrt((u - c1)**2 + (v - c2)**2)
        d = rr - rfunc(np.clip(w - a0, 0, a1 - a0))
        return np.maximum(d, np.maximum(a0 - w, w - a1))
    return f

def union(*fs):
    return lambda X, Y, Z: np.minimum.reduce([f(X, Y, Z) for f in fs])

def diff(a, *bs):
    return lambda X, Y, Z: np.maximum.reduce([a(X, Y, Z)] + [-b(X, Y, Z) for b in bs])

def inter(*fs):
    return lambda X, Y, Z: np.maximum.reduce([f(X, Y, Z) for f in fs])

def shift(f, dx=0, dy=0, dz=0):
    return lambda X, Y, Z: f(X - dx, Y - dy, Z - dz)

# ---------- meshing ---------------------------------------------------------
def mesh(f, bounds, res=0.4, chunk=48):
    (x0, x1), (y0, y1), (z0, z1) = bounds
    pad = 3 * res
    xs = np.arange(x0 - pad, x1 + pad + res, res)
    ys = np.arange(y0 - pad, y1 + pad + res, res)
    zs = np.arange(z0 - pad, z1 + pad + res, res)
    vol = np.empty((len(xs), len(ys), len(zs)), np.float32)
    for i in range(0, len(zs), chunk):
        zz = zs[i:i+chunk]
        vol[:, :, i:i+chunk] = f(xs[:, None, None], ys[None, :, None], zz[None, None, :])
    vol[0], vol[-1], vol[:, 0], vol[:, -1], vol[:, :, 0], vol[:, :, -1] = [1.0] * 6
    v, faces, _, _ = marching_cubes(vol, 0.0, spacing=(res, res, res))
    v += np.array([xs[0], ys[0], zs[0]])
    return v, faces, (xs, ys, zs, vol)

def write_stl(path, v, faces, name="part"):
    tri = v[faces]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    with open(path, "wb") as fh:
        fh.write(name.encode()[:80].ljust(80, b" "))
        fh.write(struct.pack("<I", len(faces)))
        data = np.zeros(len(faces), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
        data["n"] = n; data["v"] = tri
        fh.write(data.tobytes())

def check_watertight(faces):
    e = np.sort(np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1)
    _, cnt = np.unique(e, axis=0, return_counts=True)
    return bool(np.all(cnt == 2)), int(np.sum(cnt != 2))

def volume(v, faces):
    tri = v[faces]
    return float(np.sum(np.einsum('ij,ij->i', tri[:, 0], np.cross(tri[:, 1], tri[:, 2]))) / 6)
