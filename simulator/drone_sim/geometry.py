"""Geometry: component meshes, hydrostatics by exact plane clipping, mass properties,
righting-arm (GZ) curve, cost estimate, STL/OBJ import.

Design frame: x aft from bow, y to port, z up from hull bottom at midships (metres).
"""
import math, struct, os
import numpy as np

RHO_W = 1025.0
G = 9.81

# ----------------------------------------------------------------- shape functions
def naca(t, c=1.0, n=40):
    beta = np.linspace(0, np.pi, n)
    xc = (1 - np.cos(beta)) / 2
    yt = 5 * t * (0.2969*np.sqrt(xc) - 0.1260*xc - 0.3516*xc**2 + 0.2843*xc**3 - 0.1036*xc**4)
    xs = np.concatenate([xc[::-1], xc[1:-1]]) * c
    ys = np.concatenate([yt[::-1], -yt[1:-1]]) * c
    return np.c_[xs, ys]          # closed loop without repeated point, LE at 0


class HullShape:
    def __init__(self, h):
        self.L = h["length"]; self.B = h["beam"]; self.D = h["depth"]
        self.m = h["max_beam_at"]; self.bt = h["transom_beam"] / 2
        self.br = h["bow_rocker"]; self.sr = h["stern_rocker"]; self.bs = h["bow_sheer"]
        self.n = h["section_exponent"]

    def half_beam(self, x):
        s = np.clip(np.asarray(x, float) / self.L, 0, 1); bm = self.B / 2
        fwd = bm * np.clip(1 - (1 - s / self.m)**2, 0, 1)**0.6
        aft = bm - (bm - self.bt) * ((s - self.m) / (1 - self.m))**2
        return np.where(s <= self.m, fwd, aft)

    def keel_z(self, x):
        s = np.clip(np.asarray(x, float) / self.L, 0, 1)
        return np.where(s < 0.5, self.br * np.clip(1 - s/0.5, 0, 1)**2.2, self.sr * (np.clip(s - 0.5, 0, None)/0.5)**2)

    def deck_z(self, x):
        s = np.clip(np.asarray(x, float) / self.L, 0, 1)
        return self.D + self.bs * np.clip(1 - s/0.4, 0, 1)**2

    def section(self, x, n=14):
        zk, zd, b = float(self.keel_z(x)), float(self.deck_z(x)), max(float(self.half_beam(x)), 1e-3)
        t = np.linspace(0, 1, n)**2
        y = b * (1 - (1 - t)**self.n)**(1/self.n)
        z = zk + t * (zd - zk)
        return y, z


# ----------------------------------------------------------------- mesh building
def _loft(rings, cap_start=True, cap_end=True):
    """rings: list of (R,3) closed loops with equal R. Returns V, F (outward if rings CCW
    seen from the start cap looking along increasing ring index... orientation fixed later)."""
    R = len(rings[0]); N = len(rings)
    V = np.vstack(rings); F = []
    for i in range(N - 1):
        a = i * R; b = (i + 1) * R
        for j in range(R):
            j2 = (j + 1) % R
            F.append([a + j, a + j2, b + j2]); F.append([a + j, b + j2, b + j])
    extra = []
    for k, cap in ((0, cap_start), (N - 1, cap_end)):
        if not cap:
            continue
        c = rings[k].mean(0); ci = len(V) + len(extra); extra.append(c)
        base = k * R
        for j in range(R):
            j2 = (j + 1) % R
            F.append([ci, base + j2, base + j] if k == 0 else [ci, base + j, base + j2])
    if extra:
        V = np.vstack([V, np.array(extra)])
    V = np.asarray(V, float); F = np.asarray(F, int)
    if signed_volume(V, F) < 0:
        F = F[:, ::-1]
    return V, F


def signed_volume(V, F):
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    return float(np.einsum('ij,ij->i', a, np.cross(b, c)).sum() / 6)


def mesh_area(V, F):
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    cr = np.cross(b - a, c - a)
    ar = 0.5 * np.linalg.norm(cr, axis=1)
    cen = (a + b + c) / 3
    return ar.sum(), (cen * ar[:, None]).sum(0) / max(ar.sum(), 1e-12)


def mesh_volume_centroid(V, F):
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    vol = np.einsum('ij,ij->i', a, np.cross(b, c)) / 6
    cen = (a + b + c) / 4
    tv = vol.sum()
    return tv, (cen * vol[:, None]).sum(0) / (tv if abs(tv) > 1e-15 else 1e-15)


def hull_mesh(hs, nst=41, nsec=14):
    s = (1 - np.cos(np.linspace(0, np.pi, nst))) / 2
    xs = s * hs.L
    rings = []
    for x in xs:
        y, z = hs.section(x, nsec)
        # ring: port deck edge -> port keel ... starboard keel -> starboard deck edge, closed by deck
        port = np.c_[np.full(nsec, x), y[::-1], z[::-1]]
        stbd = np.c_[np.full(nsec - 1, x), -y[1:], z[1:]]
        ring = np.vstack([port, stbd])
        # keel point appears once (y=0) at index nsec-1; collapse tiny-beam bow
        rings.append(ring)
    return _loft(rings)


def _foil_ring(t, chord, le, z, n=24, angle=0.0, about=None):
    P = naca(t, chord, n)                       # (x along chord, y thickness)
    pts = np.c_[le[0] + P[:, 0], le[1] + P[:, 1], np.full(len(P), z)]
    return pts


def keel_geometry(d):
    k, hs = d["keel"], HullShape(d["hull"])
    xr = k["x_le_root"]
    zr = float(hs.keel_z(xr + k["root_chord"] / 2)) + 0.01      # embed 1 cm in the hull
    span = k["span"]
    rake, cant = math.radians(k["rake_deg"]), math.radians(k["cant_deg"])
    sweep = math.radians(k["sweep_deg"])
    # tip LE before rake/cant
    tip = np.array([xr + span * math.tan(sweep), 0.0, zr - span])
    def tf(p):                                   # rake about y through root LE, then cant about x
        p = np.asarray(p, float) - [xr, 0, zr]
        cr, sr = math.cos(rake), math.sin(rake)
        x = p[..., 0] * cr - p[..., 2] * sr; z = p[..., 0] * sr + p[..., 2] * cr
        p = np.stack([x, p[..., 1], z], -1)
        cc, sc = math.cos(cant), math.sin(cant)
        y = p[..., 1] * cc - p[..., 2] * sc; z = p[..., 1] * sc + p[..., 2] * cc
        p = np.stack([p[..., 0], y, z], -1)
        return p + [xr, 0, zr]
    return dict(xr=xr, zr=zr, tip=tip, tf=tf)


def fin_mesh(d, n=24, nspan=6):
    k = d["keel"]; g = keel_geometry(d)
    rings = []
    for f in np.linspace(0, 1, nspan):
        c = k["root_chord"] + f * (k["tip_chord"] - k["root_chord"])
        le = np.array([g["xr"], 0, g["zr"]]) + f * (g["tip"] - np.array([g["xr"], 0, g["zr"]]))
        P = naca(k["thickness"], c, n)
        ring = np.c_[le[0] + P[:, 0], P[:, 1], np.full(len(P), le[2])]
        rings.append(g["tf"](ring))
    return _loft(rings)


def bulb_radius(b, xl):
    Lb, R, m = b["length"], b["diameter"] / 2, b["max_at"]
    u = np.clip(np.asarray(xl, float) / Lb, 0, 1)
    fwd = R * np.sqrt(np.clip(1 - ((m - u) / m)**2, 0, 1))
    aft = R * np.clip(1 - ((u - m) / (1 - m))**2, 0, 1)**0.75
    return np.where(u <= m, fwd, aft)


def bulb_mesh(d, nax=30, nrad=20):
    b = d["bulb"]; g = keel_geometry(d)
    tip = g["tf"](g["tip"])
    xn = tip[0] + b["nose_from_tip_le"]
    zc = tip[2] - 0.004; yc = tip[1]
    u = (1 - np.cos(np.linspace(0, np.pi, nax))) / 2
    xl = u * b["length"]
    r = np.maximum(bulb_radius(b, xl), 1e-4)
    a = np.linspace(0, 2*np.pi, nrad, endpoint=False)
    rings = [np.c_[np.full(nrad, xn + x), yc + rr*np.cos(a), zc + rr*np.sin(a)] for x, rr in zip(xl, r)]
    return _loft(rings)


def rudder_mesh(d, n=20):
    r = d["rudder"]; le = r["stock_x"] - r["stock_from_le"]
    rings = []
    for z in (r["top_z"], r["top_z"] - r["span"]):
        P = naca(r["thickness"], r["chord"], n)
        rings.append(np.c_[le + P[:, 0], P[:, 1], np.full(len(P), z)])
    return _loft(rings)


def wing_mesh(d, n=24, local=False):
    w = d["wing"]
    P = naca(w["thickness"], w["chord"], n)
    if local:   # wing frame: origin on pivot axis at root, x aft along chord
        x0 = -w["pivot_from_le"]; z0 = 0.0
    else:
        x0 = w["mast_x"] - w["pivot_from_le"]; z0 = w["root_z"]
    rings = [np.c_[x0 + P[:, 0], P[:, 1], np.full(len(P), z0 + zz)] for zz in (0.0, w["span"])]
    return _loft(rings)


def tail_mesh(d, n=16, local=False):
    t, w = d["tail"], d["wing"]
    P = naca(t["thickness"], t["chord"], n)
    if local:
        x0 = t["boom_length"] - t["pivot_from_le"]; z0 = t["bot_z"] - w["root_z"]
    else:
        x0 = w["mast_x"] + t["boom_length"] - t["pivot_from_le"]; z0 = t["bot_z"]
    rings = [np.c_[x0 + P[:, 0], P[:, 1], np.full(len(P), z0 + zz)] for zz in (0.0, t["span"])]
    return _loft(rings)


# ----------------------------------------------------------------- STL / OBJ import
def read_mesh_file(path):
    ext = os.path.splitext(path)[1].lower()
    data = open(path, "rb").read()
    if ext == ".obj":
        V, F = [], []
        for line in data.decode("utf-8", "ignore").splitlines():
            p = line.split()
            if not p: continue
            if p[0] == "v": V.append([float(x) for x in p[1:4]])
            elif p[0] == "f":
                idx = [int(q.split("/")[0]) for q in p[1:]]
                idx = [i - 1 if i > 0 else len(V) + i for i in idx]
                for k in range(1, len(idx) - 1):
                    F.append([idx[0], idx[k], idx[k + 1]])
        return np.array(V, float), np.array(F, int)
    # STL: binary or ascii
    if data[:5].lower() == b"solid" and b"facet" in data[:400]:
        tris = []
        for line in data.decode("utf-8", "ignore").splitlines():
            p = line.split()
            if p and p[0] == "vertex":
                tris.append([float(x) for x in p[1:4]])
        T = np.array(tris, float).reshape(-1, 3, 3)
    else:
        n = struct.unpack("<I", data[80:84])[0]
        arr = np.frombuffer(data[84:84 + n*50], dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
        T = arr["v"].astype(float)
    # weld vertices
    flat = T.reshape(-1, 3)
    key = np.round(flat / 1e-6).astype(np.int64)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    V = np.zeros((len(uniq), 3)); V[inv.ravel()] = flat
    F = inv.reshape(-1, 3)
    F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
    return V, F


def mesh_check(V, F):
    e = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1)
    _, cnt = np.unique(e, axis=0, return_counts=True)
    return dict(triangles=int(len(F)), open_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()),
                watertight=bool(np.all(cnt == 2)))


def import_mesh(spec):
    """spec: {"path", "role": "hull"|"full", "units": "mm"|"cm"|"m"|"in", "axes": "x_aft_z_up"|"x_fwd_z_up"|"x_aft_y_up"|"x_fwd_y_up",
    "auto_place": bool}"""
    V, F = read_mesh_file(spec["path"])
    scale = {"mm": 1e-3, "cm": 1e-2, "m": 1.0, "in": 0.0254}[spec.get("units", "mm")]
    V = V * scale
    axes = spec.get("axes", "x_aft_z_up")
    if axes.endswith("y_up"):
        V = np.c_[V[:, 0], -V[:, 2], V[:, 1]]
    if axes.startswith("x_fwd"):
        V = np.c_[-V[:, 0], -V[:, 1], V[:, 2]]
    if spec.get("auto_place", True):
        V[:, 0] -= V[:, 0].min()
        if spec.get("role", "hull") == "hull":
            V[:, 2] -= V[:, 2].min()
    if signed_volume(V, F) < 0:
        F = F[:, ::-1]
    return V, F, mesh_check(V, F)


# ----------------------------------------------------------------- the assembled boat
class Boat:
    """All geometry + mass properties for one design."""

    def __init__(self, design):
        self.d = d = design
        self.hs = HullShape(d["hull"])
        stl = d["hull"].get("stl")
        self.mesh_info = None
        comps = {}
        if stl and stl.get("path") and os.path.exists(stl["path"]):
            V, F, info = import_mesh(stl)
            self.mesh_info = info
            if stl.get("role", "hull") == "full":
                comps["hull"] = (V, F)            # whole boat volume from the mesh
            else:
                comps["hull"] = (V, F)
        else:
            comps["hull"] = hull_mesh(self.hs)
        full = bool(stl and stl.get("role") == "full" and "path" in stl and os.path.exists(stl["path"]))
        if not full:
            comps["fin"] = fin_mesh(d); comps["bulb"] = bulb_mesh(d); comps["rudder"] = rudder_mesh(d)
        self.fixed = comps                                    # meshes that move with the hull
        self.wing_local = wing_mesh(d, local=True)
        self.tail_local = tail_mesh(d, local=True)
        self.full_mesh_mode = full
        self._mass_properties()

    # ---------------- mass
    def _mass_properties(self):
        d = self.d; items = []                                # (name, kg, (x,y,z))
        Vh, Fh = self.fixed["hull"]
        area, ac = mesh_area(Vh, Fh)
        if self.full_mesh_mode:
            ov = d["hull"]["stl"]
            if ov.get("mass_kg") and ov.get("cg"):
                items.append(("mesh (user mass)", float(ov["mass_kg"]), np.array(ov["cg"], float)))
            else:
                items.append(("hull shell (from mesh area)", area * d["hull"]["laminate_kg_m2"] * 0.6, ac))
        else:
            items.append(("hull + deck shell", area * d["hull"]["laminate_kg_m2"], ac))
        self.hull_area = area
        if not self.full_mesh_mode or not d["hull"]["stl"].get("mass_kg"):
            Vf, Ff = fin_mesh(d); fa, fc = mesh_area(Vf, Ff); fv, fvc = mesh_volume_centroid(Vf, Ff)
            k = d["keel"]
            items.append(("keel fin", fa * k["kg_per_m2_skin"] + fv * k["core_density"] + k["rod_kg"], fvc))
            Vb, Fb = bulb_mesh(d); bv, bc = mesh_volume_centroid(Vb, Fb)
            items.append(("lead bulb", bv * d["bulb"]["density"], bc)); self.bulb_volume = bv
            Vr, Fr = rudder_mesh(d); ra, rc = mesh_area(Vr, Fr); rv, rvc = mesh_volume_centroid(Vr, Fr)
            items.append(("rudder", ra * d["rudder"]["kg_per_m2_skin"] + rv * 250 + d["rudder"]["stock_kg"], rvc))
            self.fin_area_wet = fa; self.rudder_area_wet = ra
            self.bulb_area_wet = mesh_area(Vb, Fb)[0]
        else:
            self.bulb_volume = 0.0; self.fin_area_wet = 0.0; self.rudder_area_wet = 0.0; self.bulb_area_wet = 0.0
        # rotating rig (wing + tail + boom + counterweight)
        w, t = d["wing"], d["tail"]
        Vw, Fw = self.wing_local; wa, wac = mesh_area(Vw, Fw); wv, wvc = mesh_volume_centroid(Vw, Fw)
        rig = [("wing", wa * w["skin_kg_m2"] + wv * w["core_density"], wvc),
               ("wing spar", w["spar_kg"], np.array([0, 0, w["span"]/2 - 0.05])),
               ("tail + servo housing", t["kg"] + 0.12, np.array([t["boom_length"], 0, t["bot_z"] - w["root_z"] + 0.05])),
               ("tail boom", 0.11 * t["boom_length"], np.array([t["boom_length"]/2, 0, t["boom_z"] - w["root_z"]]))]
        cw = 0.0
        if w["balanced"]:
            arm = max(w["counterweight_arm"], 1e-3)
            zc = t["boom_z"] - w["root_z"] + 0.01          # pod hangs at boom height, under the wing root
            if arm > 0.08:                                  # separate arm + pod (Rev B), not the nose pocket
                rig += [("counterweight arm tube", w.get("arm_kg_per_m", 0.06) * arm, np.array([-arm / 2, 0, zc])),
                        ("counterweight pod shell", w.get("pod_shell_kg", 0.11), np.array([-arm, 0, zc]))]
            else:
                zc = 0.04
            mx = sum(m * p[0] for _, m, p in rig)
            cw = max(mx / arm, 0.0)
            rig.append(("rig counterweight (lead)", cw, np.array([-arm, 0, zc])))
        self.counterweight_kg = cw
        self.rig_items = rig
        self.rig_mass = sum(m for _, m, _ in rig)
        self.rig_cg_local = sum(m * p for _, m, p in rig) / self.rig_mass
        self.wing_area_wet = wa; self.wing_volume = wv
        pivot = np.array([w["mast_x"], 0, w["root_z"]])
        for n, m, p in rig:
            items.append((n, m, pivot + p))
        for n, (m, x, y, z) in d["equipment"].items():
            items.append((n.replace("_", " "), m, np.array([x, y, z], float)))
        self.mass_items = items
        self.mass = sum(m for _, m, _ in items)
        self.cg = sum(m * p for _, m, p in items) / self.mass
        # inertia (point masses + shell/solid spread approximations)
        I = np.zeros((3, 3))
        for n, m, p in items:
            r = p - self.cg
            I += m * (np.dot(r, r) * np.eye(3) - np.outer(r, r))
        # add self-inertia of the hull shell and wing as distributed bodies
        L, B, Dh = self.hs.L, self.hs.B, self.hs.D
        mh = items[0][1]
        I += np.diag([mh*(B**2 + Dh**2)/12, mh*(L**2 + Dh**2)/12, mh*(L**2 + B**2)/12]) * 0.8
        mw = rig[0][1]
        I += np.diag([mw*w["span"]**2/12, mw*(w["span"]**2 + w["chord"]**2)/12, mw*w["chord"]**2/12])
        self.inertia = I
        self.rig_inertia_z = sum(m * (p[0]**2 + p[1]**2) for _, m, p in rig) + mw * w["chord"]**2 / 12

    # ---------------- hydrostatics
    def world_meshes(self, wing_angle=0.0, include_rig=True):
        out = [m for m in self.fixed.values()]
        if include_rig and self.d["wing"]["buoyant"]:
            out.append(self._rig_mesh(self.wing_local, wing_angle))
        return out

    def _rig_mesh(self, mesh, ang):
        w = self.d["wing"]; V, F = mesh
        c, s = math.cos(ang), math.sin(ang)
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        return (V @ R.T + [w["mast_x"], 0, w["root_z"]], F)

    def combined(self, wing_angle=0.0, include_rig=True):
        Vs, Fs, off = [], [], 0
        for V, F in self.world_meshes(wing_angle, include_rig):
            Vs.append(V); Fs.append(F + off); off += len(V)
        return np.vstack(Vs), np.vstack(Fs)

    def gz_curve(self, angles_deg=None, free_trim=True):
        if angles_deg is None:
            angles_deg = np.arange(0, 181, 5)
        V, F = self.combined()
        P = V - self.cg
        disp = self.mass / RHO_W
        out = []
        th = 0.0
        for phi in angles_deg:
            ph = math.radians(phi)
            def fx(theta):
                vol, cb, h = _equilibrium(P, F, ph, theta, disp)
                return float((_rot(ph, theta) @ cb)[0]), cb, h
            if free_trim:
                t0 = th; f0, cb, h = fx(t0)
                t1 = t0 + 0.05; f1, cb1, h1 = fx(t1)
                for _ in range(10):
                    if abs(f1) < 2e-4 or abs(f1 - f0) < 1e-9:
                        break
                    t2 = t1 - f1 * (t1 - t0) / (f1 - f0)
                    t2 = float(np.clip(t2, t1 - 0.2, t1 + 0.2)); t2 = float(np.clip(t2, -1.3, 1.3))
                    t0, f0 = t1, f1
                    t1 = t2; f1, cb1, h1 = fx(t1)
                th, cb, h = t1, cb1, h1
            else:
                _, cb, h = fx(0.0); th = 0.0
            cbw = _rot(ph, th) @ cb
            out.append((float(phi), float(-cbw[1]), float(math.degrees(th)), float(h)))
        a = np.array(out)
        return dict(angle=a[:, 0], gz=a[:, 1], trim_deg=a[:, 2], sink=a[:, 3])

    def stability_summary(self):
        g = self.gz_curve()
        ang, gz = g["angle"], g["gz"]
        avs = 180.0
        for i in range(1, len(ang)):
            if gz[i] < 0 <= gz[i-1]:
                avs = ang[i-1] + (ang[i]-ang[i-1]) * gz[i-1] / (gz[i-1] - gz[i]); break
        pos = np.trapezoid(np.clip(gz, 0, None), np.radians(ang))
        neg = -np.trapezoid(np.clip(gz, None, 0), np.radians(ang))
        gm = (gz[1] - gz[0]) / math.radians(ang[1] - ang[0])
        return dict(gz_curve=g, avs_deg=float(avs), gm_m=float(gm), max_gz_m=float(gz.max()),
                    angle_max_gz=float(ang[np.argmax(gz)]), positive_area=float(pos), negative_area=float(neg),
                    self_righting=bool(avs >= 179.0), p_stay_inverted=float(neg / max(pos + neg, 1e-9)))

    def waterline(self):
        V, F = self.combined()
        disp = self.mass / RHO_W
        vol, cb, h = _equilibrium(V - self.cg, F, 0.0, 0.0, disp)
        return dict(z_waterline=float(self.cg[2] - h), cb=(cb + self.cg).tolist())

    # ---------------- derived reference values for the hydrodynamic models
    def reference(self):
        d = self.d; k, r, w, t = d["keel"], d["rudder"], d["wing"], d["tail"]
        wl = self.waterline()["z_waterline"]
        xs = np.linspace(0, self.hs.L, 200)
        submerged = self.hs.keel_z(xs) < wl
        lwl = float(np.ptp(xs[submerged])) if submerged.any() else self.hs.L
        bwl = float(2*max(_hb_at(self.hs, x, wl) for x in xs))
        # wetted hull area: integrate section girth below waterline
        girth = []
        for x in xs:
            y, z = self.hs.section(x, 40)
            m = z <= wl
            if m.sum() < 2: girth.append(0.0); continue
            yy, zz = y[m], z[m]
            girth.append(2*np.sum(np.hypot(np.diff(yy), np.diff(zz))))
        s_hull = float(np.trapezoid(girth, xs))
        keel_area = 0.5 * (k["root_chord"] + k["tip_chord"]) * k["span"]
        g = keel_geometry(d)
        x_keel_qc = g["xr"] + 0.25*k["root_chord"] + 0.45*k["span"]*math.tan(math.radians(k["sweep_deg"]))
        z_keel_ce = g["zr"] - 0.45*k["span"]*math.cos(math.radians(k["rake_deg"]))
        return dict(
            lwl=lwl, bwl=bwl, z_wl=wl, s_hull=s_hull,
            s_total=s_hull + self.fin_area_wet + self.rudder_area_wet + self.bulb_area_wet,
            keel_area=keel_area, keel_ar=2*k["span"]/(0.5*(k["root_chord"]+k["tip_chord"])),
            x_keel=x_keel_qc, z_keel=z_keel_ce,
            rudder_area=r["chord"]*r["span"], rudder_ar=2*r["span"]/r["chord"],
            x_rudder=r["stock_x"] - r["stock_from_le"] + 0.25*r["chord"], z_rudder=r["top_z"] - r["span"]/2,
            wing_area=w["chord"]*w["span"], wing_ar=1.6*w["span"]/w["chord"],
            z_wing_ce=w["root_z"] + 0.45*w["span"],
            tail_area=t["chord"]*t["span"], tail_ar=t["span"]/t["chord"],
            hull_lat_area=lwl*max(wl - float(self.hs.keel_z(lwl/2)), 0.02),
            hull_windage_area=self.hs.L*(self.hs.D - wl + 0.05),
            bulb_frontal=math.pi*(d["bulb"]["diameter"]/2)**2,
            mass=self.mass, cg=self.cg.tolist(),
        )

    # ---------------- cost
    def cost(self):
        d = self.d; c = d["cost"]; k, r, w, t = d["keel"], d["rudder"], d["wing"], d["tail"]
        items = {
            "Electronics and power": c["electronics_and_power_usd"],
            "Hardware and fittings": c["hardware_usd"],
            "Hull materials": self.hull_area * c["hull_materials_usd_per_m2"],
            "Keel + rudder materials": (self.fin_area_wet + self.rudder_area_wet) * c["foil_materials_usd_per_m2"],
            "Lead": (self.bulb_volume * d["bulb"]["density"] + self.counterweight_kg) * c["lead_usd_per_kg"],
            "Wing + tail materials": (self.wing_area_wet + 2*t["chord"]*t["span"]) * c["wing_materials_usd_per_m2"],
            "Printing and misc": c["printing_and_misc_usd"],
        }
        if d["autopilot"]["thruster_policy"]["enabled"]:
            items["Thruster"] = c["thruster_usd"]
        return dict(items={k: round(v, 0) for k, v in items.items()}, total=round(sum(items.values()), 0))

    def summary(self):
        st = self.stability_summary()
        ref = self.reference()
        return dict(
            mass_kg=round(self.mass, 2), cg=[round(v, 3) for v in self.cg],
            mass_items=[(n, round(m, 3), [round(float(v), 3) for v in p]) for n, m, p in self.mass_items],
            counterweight_kg=round(self.counterweight_kg, 2), rig_mass_kg=round(self.rig_mass, 2),
            ballast_kg=round(self.bulb_volume * self.d["bulb"]["density"], 2),
            ballast_ratio=round(self.bulb_volume * self.d["bulb"]["density"] / self.mass, 3),
            waterline_z=round(ref["z_wl"], 3), lwl=round(ref["lwl"], 3), wetted_area_m2=round(ref["s_total"], 3),
            wing_area_m2=round(ref["wing_area"], 3), keel_area_m2=round(ref["keel_area"], 4),
            wing_buoyancy_kg=round(self.wing_volume * RHO_W if self.d["wing"]["buoyant"] else 0.0, 2),
            stability={k: v for k, v in st.items() if k != "gz_curve"},
            gz_curve={k: [round(float(x), 4) for x in v] for k, v in st["gz_curve"].items()},
            cost=self.cost(), mesh_info=self.mesh_info,
            warnings=self.warnings(st),
        )

    def warnings(self, st=None):
        st = st or self.stability_summary(); out = []
        if not st["self_righting"]:
            out.append(f"Not self-righting: the boat has a stable upside-down position (vanishing stability at {st['avs_deg']:.0f} deg). "
                       f"About {100*st['p_stay_inverted']:.0f}% of capsizes would leave it inverted.")
        if self.counterweight_kg > 0.25 * self.rig_mass + 0.5:
            out.append(f"Rig counterweight is {self.counterweight_kg:.1f} kg: lengthen the counterweight arm or lighten the tail.")
        if self.mesh_info and not self.mesh_info["watertight"]:
            out.append(f"Uploaded mesh is not watertight ({self.mesh_info['open_edges']} open edges): buoyancy will be wrong.")
        wl = self.waterline()["z_waterline"]
        if wl > self.hs.D * 0.8:
            out.append("Waterline is above 80% of hull depth: the boat is overloaded for this hull.")
        return out


def _hb_at(hs, x, z):
    zk, zd, b = float(hs.keel_z(x)), float(hs.deck_z(x)), float(hs.half_beam(x))
    if z <= zk: return 0.0
    t = min((z - zk) / max(zd - zk, 1e-6), 1.0)
    return b * (1 - (1 - t)**hs.n)**(1/hs.n)


# ----------------------------------------------------------------- clipping hydrostatics
def _rot(phi, theta):
    """Body->world rotation for heel phi (about body x) then trim theta (about world y)."""
    cp, sp, ct, st = math.cos(phi), math.sin(phi), math.cos(theta), math.sin(theta)
    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    Ry = np.array([[ct, 0, st], [0, 1, 0], [-st, 0, ct]])
    return Ry @ Rx


def _plane_normal(phi, theta):
    return _rot(phi, theta)[2]           # world z expressed in body coords (row of R)


def clip_volume(P, F, n, hs):
    """Submerged volume and centroid of closed mesh (points P relative to CG, body frame)
    below the plane n.p + h = 0 (n: unit normal pointing up in body coords), for each h in hs.
    Returns vol (H,), centroid (H,3)."""
    hs = np.atleast_1d(np.asarray(hs, float))
    sd = P @ n                                     # (N,)
    A, B, C = F[:, 0], F[:, 1], F[:, 2]
    vol_out = np.zeros(len(hs)); mom_out = np.zeros((len(hs), 3))
    for i, h in enumerate(hs):
        s = sd + h
        sa, sb, sc = s[A], s[B], s[C]
        below = (sa < 0).astype(int) + (sb < 0) + (sc < 0)
        O = -h * n
        vol = 0.0; mom = np.zeros(3)
        # all below
        m3 = below == 3
        if m3.any():
            v, c = _tet(P[A[m3]], P[B[m3]], P[C[m3]], O); vol += v.sum(); mom += (c * v[:, None]).sum(0)
        for cnt in (1, 2):
            m = below == cnt
            if not m.any(): continue
            a, b, c = P[A[m]], P[B[m]], P[C[m]]
            s1, s2, s3 = sa[m], sb[m], sc[m]
            # rotate vertex order so the odd vertex is first
            if cnt == 1:
                odd = np.stack([s1 < 0, s2 < 0, s3 < 0], 1)
            else:
                odd = np.stack([s1 >= 0, s2 >= 0, s3 >= 0], 1)
            k = np.argmax(odd, 1)
            pts = np.stack([a, b, c], 1); ss = np.stack([s1, s2, s3], 1)
            idx = np.stack([k, (k + 1) % 3, (k + 2) % 3], 1)
            r = np.arange(len(k))[:, None]
            pts = pts[r, idx]; ss = ss[r, idx]
            p0, p1, p2 = pts[:, 0], pts[:, 1], pts[:, 2]
            t01 = (ss[:, 0] / (ss[:, 0] - ss[:, 1]))[:, None]; t02 = (ss[:, 0] / (ss[:, 0] - ss[:, 2]))[:, None]
            q1 = p0 + t01 * (p1 - p0); q2 = p0 + t02 * (p2 - p0)
            if cnt == 1:
                v, cc = _tet(p0, q1, q2, O); vol += v.sum(); mom += (cc * v[:, None]).sum(0)
            else:
                v1, c1 = _tet(q1, p1, p2, O); v2, c2 = _tet(q1, p2, q2, O)
                vol += v1.sum() + v2.sum(); mom += (c1 * v1[:, None]).sum(0) + (c2 * v2[:, None]).sum(0)
        vol_out[i] = vol; mom_out[i] = mom
    cen = mom_out / np.where(np.abs(vol_out) > 1e-12, vol_out, 1e-12)[:, None]
    return vol_out, cen


def _tet(a, b, c, O):
    v = np.einsum('ij,ij->i', a - O, np.cross(b - O, c - O)) / 6
    return v, (a + b + c + O) / 4


def _equilibrium(P, F, phi, theta, disp, iters=40):
    n = _plane_normal(phi, theta)
    ext = np.abs(P @ n).max() + 0.05
    lo, hi = -ext, ext                    # h large -> fully submerged? s = n.p + h ; below if s<0 -> h small => more submerged
    # volume decreases with h
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        v, _ = clip_volume(P, F, n, [mid])
        if v[0] > disp: lo = mid
        else: hi = mid
    h = 0.5 * (lo + hi)
    v, c = clip_volume(P, F, n, [h])
    return v[0], c[0], h


def hydro_table(P, F, phis, thetas, hs):
    """Precompute submerged volume and first moments over (phi, theta, h)."""
    T = np.zeros((len(phis), len(thetas), len(hs), 4))
    for i, ph in enumerate(phis):
        for j, th in enumerate(thetas):
            n = _plane_normal(ph, th)
            v, c = clip_volume(P, F, n, hs)
            T[i, j, :, 0] = v; T[i, j, :, 1:] = c * v[:, None]
    return T


def outlines(boat):
    """Side-view and plan outlines (design frame, metres) for drawing the boat in the UI."""
    d, hs = boat.d, boat.hs
    xs = np.linspace(0, hs.L, 60)
    prof = np.r_[np.c_[xs, hs.keel_z(xs)], np.c_[xs[::-1], hs.deck_z(xs[::-1])]].tolist()
    plan = np.r_[np.c_[xs, hs.half_beam(xs)], np.c_[xs[::-1], -hs.half_beam(xs[::-1])]].tolist()
    k = d["keel"]; g = keel_geometry(d)
    root = np.array([g["xr"], 0, g["zr"]]); tip = g["tip"]
    pts = [root, root + [k["root_chord"], 0, 0], tip + [k["tip_chord"], 0, 0], tip]
    fin = [[float(p[0]), float(p[2])] for p in g["tf"](np.array(pts))]
    b = d["bulb"]; tipw = g["tf"](g["tip"])
    xl = np.linspace(0, b["length"], 40); r = bulb_radius(b, xl)
    xn = tipw[0] + b["nose_from_tip_le"]; zc = tipw[2] - 0.004
    bulb = np.r_[np.c_[xn + xl, zc + r], np.c_[(xn + xl)[::-1], (zc - r)[::-1]]].tolist()
    r_ = d["rudder"]; le = r_["stock_x"] - r_["stock_from_le"]
    rud = [[le, r_["top_z"]], [le + r_["chord"], r_["top_z"]], [le + r_["chord"], r_["top_z"] - r_["span"]], [le, r_["top_z"] - r_["span"]]]
    w = d["wing"]; wl = w["mast_x"] - w["pivot_from_le"]
    wing = [[wl, w["root_z"]], [wl + w["chord"], w["root_z"]], [wl + w["chord"], w["root_z"] + w["span"]], [wl, w["root_z"] + w["span"]]]
    t = d["tail"]; tp = w["mast_x"] + t["boom_length"]; tl = tp - t["pivot_from_le"]
    tail = [[tl, t["bot_z"]], [tl + t["chord"], t["bot_z"]], [tl + t["chord"], t["bot_z"] + t["span"]], [tl, t["bot_z"] + t["span"]]]
    boom = [[w["mast_x"], t["boom_z"]], [tp, t["boom_z"]]]
    cw = [[w["mast_x"] - w["counterweight_arm"], w["root_z"] + 0.04], [w["mast_x"], w["root_z"] + 0.04]]
    return dict(profile=prof, plan=plan, fin=fin, bulb=bulb, rudder=rud, wing=wing, tail=tail, boom=boom,
                counterweight_arm=cw, waterline=boat.waterline()["z_waterline"], cg=boat.cg.tolist(), length=hs.L)
