"""Full six-degree-of-freedom time-domain model (plus the free-rotating wing as a 7th DOF).

Body frame: x forward, y to port, z up, origin at the CG. World frame: x east, y north, z up.

Forces
  * Hydrostatics + Froude-Krylov: exact submerged volume/centroid of the hull, keel, bulb and
    rudder meshes below the local water plane, from a precomputed table over
    (heel-like angle, trim-like angle, plane offset). The local water plane is fitted to an
    irregular directional JONSWAP sea (24 components) built from the hourly Hs/Tp/direction.
    Buoyancy acts along (g z - a_orbital).
  * Lifting surfaces: keel (5 strips), rudder (3), wing (6), tail (1) with the full-range foil
    model, local flow from wind/current/wave orbital velocity and body rotation, and smooth
    air/water transition by local submergence (the wing works as a hydrofoil when knocked
    down).
  * Hull: ITTC friction + wave resistance in surge, quadratic cross-flow drag, linear radiation
    damping in heave/pitch/roll, diagonal added mass, hull windage.
  * Rig: wing+tail rotate freely about the mast (bearing friction); tail angle is servo driven.
Integration: semi-implicit Euler at dt (default 0.05 s) with automatic sub-stepping when
water-loaded surfaces make the equations stiff.
"""
import math, os
import numpy as np
from . import geometry as geo
from .vpp import foil_coeffs, friction_cf, wave_resistance, RHO_W, RHO_A, G

S = np.diag([-1.0, 1.0, 1.0])     # design frame -> body frame (x flipped)


def cross(a, b):
    """Fast cross product for (3,) or (N,3) arrays (numpy's generic version is slow for tiny arrays)."""
    if a.ndim == 1 and b.ndim == 1:
        return np.array([a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]])
    a = np.broadcast_to(a, np.broadcast_shapes(a.shape, b.shape)); b = np.broadcast_to(b, a.shape)
    out = np.empty(a.shape)
    out[..., 0] = a[..., 1]*b[..., 2] - a[..., 2]*b[..., 1]
    out[..., 1] = a[..., 2]*b[..., 0] - a[..., 0]*b[..., 2]
    out[..., 2] = a[..., 0]*b[..., 1] - a[..., 1]*b[..., 0]
    return out


def quat_mul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2 - x1*x2 - y1*y2 - z1*z2, w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2])


def quat_to_R(q):
    w, x, y, z = q
    return np.array([[1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)],
                     [2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)],
                     [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)]])


def euler_from_R(R):
    roll = math.atan2(R[2, 1], R[2, 2])
    pitch = -math.asin(max(-1, min(1, R[2, 0])))
    yaw = math.atan2(R[1, 0], R[0, 0])
    return roll, pitch, yaw


class WaveField:
    def __init__(self, rng, n=24):
        self.rng = rng; self.n = n
        self.phase = rng.uniform(0, 2*np.pi, n)
        self.dir_off = rng.uniform(-1, 1, n)
        self.u = rng.uniform(0, 1, n)
        self.set(0.0, 6.0, 0.0)

    def set(self, hs, tp, dir_from_deg):
        tp = max(tp, 1.5); wp = 2*np.pi/tp
        w = wp*(0.7 + 2.3*(np.arange(self.n) + self.u)/self.n)
        dw = wp*2.3/self.n
        g = 3.3; sig = np.where(w <= wp, 0.07, 0.09)
        r = np.exp(-(w - wp)**2/(2*sig**2*wp**2))
        Spm = (5/16)*hs**2*wp**4/w**5*np.exp(-1.25*(wp/w)**4)
        Sj = Spm*g**r*(1 - 0.287*math.log(g))
        self.a = np.sqrt(2*Sj*dw)
        self.w = w; self.k = w**2/G
        prop = math.radians(dir_from_deg + 180.0)                       # propagation, clockwise from north
        th = prop + self.dir_off*math.radians(40)
        self.cx, self.cy = np.sin(th), np.cos(th)                       # east, north components
        self.hs, self.tp, self.dir = hs, tp, dir_from_deg

    def eta(self, x, y, t):
        T = self.k*(x*self.cx + y*self.cy) - self.w*t + self.phase
        c, s = np.cos(T), np.sin(T)
        eta = float(np.dot(self.a, c))
        ex = float(-np.dot(self.a*self.k*self.cx, s)); ey = float(-np.dot(self.a*self.k*self.cy, s))
        return eta, ex, ey

    def kinematics(self, X, Y, Z, t):
        """Orbital velocity and acceleration at points (arrays) with Z = depth below mean surface (<=0)."""
        T = np.outer(X, self.k*self.cx) + np.outer(Y, self.k*self.cy) - self.w*t + self.phase
        dec = np.exp(np.outer(np.minimum(Z, 0), self.k))
        aw = self.a*self.w*dec; aw2 = self.a*self.w**2*dec
        c, s = np.cos(T), np.sin(T)
        uh = (aw*c); w = (aw*s).sum(1)
        u_e = (uh*self.cx).sum(1); u_n = (uh*self.cy).sum(1)
        ah = aw2*s
        a_e = (ah*self.cx).sum(1); a_n = (ah*self.cy).sum(1); a_z = -(aw2*c).sum(1)
        return np.stack([u_e, u_n, w], 1), np.stack([a_e, a_n, a_z], 1)


class SixDOF:
    PHIS = np.radians(np.arange(-180, 181, 7.5))
    THETAS = np.radians(np.arange(-45, 46, 7.5))
    HS = np.arange(-1.2, 1.2001, 0.03)

    def __init__(self, boat, vpp, design, scenario, rng, log=print, cache_dir="cache"):
        self.boat, self.vpp, self.d, self.sc, self.rng, self.log = boat, vpp, design, scenario, rng, log
        self.dt = float(scenario.get("dt_6dof_s", 0.05))
        d = design; cg = boat.cg
        self.m = boat.mass
        self.I = S @ boat.inertia @ S
        # ---- hydrostatic table for the fixed parts
        from .design import design_hash
        p = os.path.join(cache_dir, "hydro6", design_hash(design) + ".npz")
        if os.path.exists(p):
            self.T = np.load(p)["T"]
        else:
            log("Precomputing the 6-DOF hydrostatic table (about 1 minute, cached) ...")
            Vs, Fs, off = [], [], 0
            for V, F in boat.fixed.values():
                Vs.append((V - cg) @ S.T); Fs.append(F[:, ::-1] + off); off += len(V)
            P, F = np.vstack(Vs), np.vstack(Fs)
            self.T = geo.hydro_table(P, F, self.PHIS, self.THETAS, self.HS)
            os.makedirs(os.path.dirname(p), exist_ok=True); np.savez_compressed(p, T=self.T)
        self.vol_design = self.m/RHO_W
        # ---- lifting-surface strips (body frame, relative to CG)
        self._build_strips()
        # ---- rig buoyancy points (wing frame)
        self._build_rig_points()
        # ---- added mass and damping
        md = self.vol_design*RHO_W
        k = d["keel"]
        lat_am = RHO_W*math.pi/4*(0.5*(k["root_chord"] + k["tip_chord"]))**2*k["span"]
        self.A_tr = np.array([0.05*md, 0.5*md + lat_am, 1.0*md])
        self.A_rot = np.array([0.25*self.I[0, 0] + lat_am*0.25**2, 1.0*self.I[1, 1], 0.4*self.I[2, 2]])
        self.Minv = 1/(self.m + self.A_tr)
        self.Ifull = self.I + np.diag(self.A_rot); self.Iinv = np.linalg.inv(self.Ifull)
        ref = vpp.ref
        self.awp = 0.7*ref["lwl"]*ref["bwl"]
        kz = RHO_W*G*self.awp
        self.b_heave = 2*0.15*math.sqrt(kz*(self.m + self.A_tr[2]))
        self.b_pitch = 2*0.15*math.sqrt(kz*ref["lwl"]**2/12*(self.I[1, 1] + self.A_rot[1]))
        self.b_roll = 2*0.03*math.sqrt(max(self.m*G*0.2, 1)*(self.I[0, 0] + self.A_rot[0]))
        self.lat_area = ref["hull_lat_area"]; self.lwl = ref["lwl"]
        self.rig_I = boat.rig_inertia_z
        self.fric = d["wing"]["bearing_friction_nm"]
        self.waves = WaveField(rng)
        self.state = None
        self.gust = 0.0
        t = d["tail"]; w = d["wing"]
        a_t = 2*np.pi*max(vpp.ref["tail_ar"]*1.4, 0.5)/(2 + math.sqrt((vpp.ref["tail_ar"]*1.4)**2 + 4))
        a_w = 2*np.pi*vpp.ar_wing/(2 + math.sqrt(vpp.ar_wing**2 + 4))
        e = max(0.25*w["chord"] - w["pivot_from_le"], 0.0)
        lt = t["boom_length"]
        At, Aw = t["chord"]*t["span"], w["chord"]*w["span"]
        self.kappa = (a_t*At*lt)/(a_w*Aw*e + a_t*At*lt)                   # alpha = -kappa * tail angle
        self.tmax = math.radians(t["max_angle_deg"]); self.dmax = math.radians(d["rudder"]["max_angle_deg"])
        self.drate = math.radians(d["rudder"]["rate_deg_s"])

    # ---------------------------------------------------------------- geometry
    def _build_strips(self):
        d, cg = self.d, self.boat.cg
        k = d["keel"]; g = geo.keel_geometry(d)
        strips = []
        root = np.array([g["xr"], 0, g["zr"]]); tip = g["tip"]
        n = 5
        cant = math.radians(k["cant_deg"])
        for i in range(n):
            f0, f1 = i/n, (i + 1)/n; fm = (f0 + f1)/2
            c = k["root_chord"] + fm*(k["tip_chord"] - k["root_chord"])
            le = g["tf"](root + fm*(tip - root))
            ctr = np.array([le[0] + 0.25*c, le[1], le[2]])
            span = k["span"]*(f1 - f0)
            strips.append(("keel", S @ (ctr - cg), c*span, min(2*k["span"]/c, 8), np.array([0, math.cos(cant), math.sin(cant)]), c))
        bl = d["bulb"]
        r = d["rudder"]; le = r["stock_x"] - r["stock_from_le"]
        self.rudder_idx = []
        for i in range(3):
            z = r["top_z"] - r["span"]*(i + 0.5)/3
            ctr = np.array([le + 0.25*r["chord"], 0, z])
            self.rudder_idx.append(len(strips))
            strips.append(("rudder", S @ (ctr - cg), r["chord"]*r["span"]/3*len(r.get("y_offsets") or [0.0]), min(2*r["span"]/r["chord"], 8),
                           np.array([0, 1.0, 0]), r["chord"]))
        self.rudder_stock_b = S @ (np.array([r["stock_x"], 0, 0]) - cg)
        self.fixed_strips = strips
        P = np.array([s[1] for s in strips]); self.fs_pos = P
        self.fs_area = np.array([s[2] for s in strips]); self.fs_ar = np.array([s[3] for s in strips])
        self.fs_norm = np.array([s[4] for s in strips]); self.fs_chord = np.array([s[5] for s in strips])
        # rig strips in wing frame (x forward along chord at gamma=0, origin on the pivot axis at the CG height)
        w, t = d["wing"], d["tail"]
        self.pivot_b = S @ (np.array([w["mast_x"], 0, 0]) - cg); self.pivot_b[2] = 0.0
        zr = w["root_z"] - cg[2]
        rig = []
        for i in range(6):
            z = zr + w["span"]*(i + 0.5)/6
            rig.append(("wing", np.array([w["pivot_from_le"] - 0.25*w["chord"], 0, z]), w["chord"]*w["span"]/6,
                        1.6*w["span"]/w["chord"], 0.0, w["chord"]))
        zt = t["bot_z"] - cg[2] + t["span"]/2
        rig.append(("tail", np.array([-t["boom_length"] + t["pivot_from_le"] - 0.25*t["chord"], 0, zt]),
                    t["chord"]*t["span"], max(1.4*t["span"]/t["chord"], 0.8), 1.0, t["chord"]))
        self.rig_strips = rig
        self.rs_pos = np.array([s[1] for s in rig]); self.rs_area = np.array([s[2] for s in rig])
        self.rs_ar = np.array([s[3] for s in rig]); self.rs_tail = np.array([s[4] for s in rig])
        self.rs_chord = np.array([s[5] for s in rig])
        self.tail_pivot_w = np.array([-t["boom_length"], 0, zt])
        nf, nr = len(self.fs_pos), len(self.rs_pos)
        self._cx0 = np.tile([1.0, 0, 0], (nf + nr, 1))
        self._ny0 = np.vstack([self.fs_norm, np.tile([0, 1.0, 0], (nr, 1))])
        self._cd0 = np.r_[np.full(nf, 0.009), np.full(nr, 0.012)]
        self._area = np.r_[self.fs_area, self.rs_area]; self._ar = np.r_[self.fs_ar, self.rs_ar]
        self._subscale = np.maximum(0.6*np.r_[self.fs_chord, self.rs_chord], 0.03)

    def _build_rig_points(self):
        w = self.d["wing"]; cg = self.boat.cg
        if not w["buoyant"]:
            self.rp_pos = np.zeros((0, 3)); self.rp_vol = np.zeros(0); return
        P = geo.naca(w["thickness"], w["chord"], 40)
        xs = np.linspace(0, w["chord"], 7)
        xc = (xs[:-1] + xs[1:])/2
        thick = np.interp(xc, P[:len(P)//2 + 1, 0][::-1], 2*P[:len(P)//2 + 1, 1][::-1])
        zs = (np.arange(10) + 0.5)/10*w["span"]
        pts, vol = [], []
        for z in zs:
            for x, th in zip(xc, thick):
                pts.append([w["pivot_from_le"] - x, 0, w["root_z"] - cg[2] + z]); vol.append(th*(xs[1] - xs[0])*w["span"]/10)
        self.rp_pos = np.array(pts); self.rp_vol = np.array(vol)
        self.rp_vol *= self.boat.wing_volume/max(self.rp_vol.sum(), 1e-9)

    # ---------------------------------------------------------------- table lookup
    def hydro(self, n_b, h):
        phi = math.atan2(n_b[1], n_b[2]); th = math.asin(max(-1.0, min(1.0, -n_b[0])))
        ph_ax, th_ax, h_ax = self.PHIS, self.THETAS, self.HS
        th = max(th_ax[0], min(th_ax[-1], th)); hh = max(h_ax[0], min(h_ax[-1] - 1e-9, h))
        def ix(ax, v):
            i = int(np.searchsorted(ax, v) - 1); i = max(0, min(i, len(ax) - 2))
            return i, (v - ax[i])/(ax[i + 1] - ax[i])
        i, fi = ix(ph_ax, phi); j, fj = ix(th_ax, th); k, fk = ix(h_ax, hh)
        T = self.T
        c = (T[i, j, k]*(1-fi)*(1-fj)*(1-fk) + T[i+1, j, k]*fi*(1-fj)*(1-fk) + T[i, j+1, k]*(1-fi)*fj*(1-fk)
             + T[i, j, k+1]*(1-fi)*(1-fj)*fk + T[i+1, j+1, k]*fi*fj*(1-fk) + T[i+1, j, k+1]*fi*(1-fj)*fk
             + T[i, j+1, k+1]*(1-fi)*fj*fk + T[i+1, j+1, k+1]*fi*fj*fk)
        V = max(c[0], 0.0)
        cen = c[1:]/V if V > 1e-9 else np.zeros(3)
        if h < h_ax[0]:            # deeper than the table: fully submerged
            V = T[i, j, 0, 0]; cen = T[i, j, 0, 1:]/max(V, 1e-9)
        return V, cen

    # ---------------------------------------------------------------- init / control
    def init_state(self, st):
        hdg = math.radians(st["heading"])
        yaw = math.pi/2 - hdg
        q = np.array([math.cos(yaw/2), 0, 0, math.sin(yaw/2)])
        V, cen = self.hydro(np.array([0, 0, 1.0]), 0.0)
        # find equilibrium sinkage roughly
        lo, hi = -0.6, 0.6
        for _ in range(30):
            mid = (lo + hi)/2; V, _ = self.hydro(np.array([0, 0, 1.0]), mid)
            if V > self.vol_design: lo = mid
            else: hi = mid
        eta0 = self.waves.eta(0.0, 0.0, 0.0)[0]
        self.state = dict(r=np.array([0.0, 0.0, eta0 - lo]), v=np.array([0.3, 0.0, 0.0]), q=q, w=np.zeros(3),
                          gam=0.0, gamd=0.0, tail=0.0, rud=0.0, t=0.0)
        self.origin = (st["lat"], st["lon"])
        self.local_xy = np.zeros(2)

    def kick(self, side=1.0, mag=3.5):
        if self.state is not None:
            self.state["w"][0] += side*mag

    # ---------------------------------------------------------------- forces
    def derivs(self, s, env, ctrl, t):
        R = quat_to_R(s["q"]); Rt = R.T
        v, w = s["v"], s["w"]
        x, y, z = s["r"]
        eta, ex, ey = self.waves.eta(x, y, t)
        nw = np.array([-ex, -ey, 1.0]); nw /= np.linalg.norm(nw)
        n_b = Rt @ nw
        h = (z - eta)*nw[2]
        F = np.zeros(3); M = np.zeros(3)
        # gravity
        F += Rt @ np.array([0, 0, -self.m*G])
        # buoyancy (hull + appendages)
        V, cen = self.hydro(n_b, h)
        cur = np.array([env["cur_u"], env["cur_v"], 0.0])
        if V > 0:
            cw = s["r"] + R @ cen
            _, acc = self.waves.kinematics(np.array([cw[0]]), np.array([cw[1]]), np.array([min(cw[2] - eta, 0)]), t)
            Fb = Rt @ (RHO_W*V*(np.array([0, 0, G]) + acc[0]))
            F += Fb; M += cross(cen, Fb)
        frac = min(V/self.vol_design, 1.5)
        # ---- strips: fixed + rig, built as one batch
        g = s["gam"]; cgm, sgm = math.cos(g), math.sin(g)
        Rg = np.array([[cgm, -sgm, 0], [sgm, cgm, 0], [0, 0, 1]])
        rig_pos = (self.rs_pos @ Rg.T) + self.pivot_b
        pos = np.vstack([self.fs_pos, rig_pos])
        nfix = len(self.fs_pos)
        # foil axes in body frame
        rud = s["rud"]
        cx = self._cx0.copy(); ny = self._ny0.copy()
        ri = self.rudder_idx
        cx[ri] = [math.cos(rud), math.sin(rud), 0.0]; ny[ri] = [-math.sin(rud), math.cos(rud), 0.0]
        ang = g + s["tail"]*self.rs_tail
        ca, sa = np.cos(ang), np.sin(ang)
        cx[nfix:, 0] = ca; cx[nfix:, 1] = sa; ny[nfix:, 0] = -sa; ny[nfix:, 1] = ca
        pw = s["r"] + pos @ R.T                                     # world positions
        surf = eta + ex*(pw[:, 0] - x) + ey*(pw[:, 1] - y)
        depth = pw[:, 2] - surf                                      # >0 above water
        sub = np.clip(0.5 - depth/self._subscale, 0, 1)
        orb, _ = self.waves.kinematics(pw[:, 0], pw[:, 1], np.minimum(depth, 0), t)
        vel_pts_w = (R @ (v + cross(w, pos).T).T.T).T if False else (cross(w, pos) + v) @ R.T
        U10 = math.hypot(env["wind_u"], env["wind_v"])
        hgt = np.maximum(depth, 0.05)
        z0 = 2e-4 + 0.002*self.waves.hs
        prof = np.log(np.maximum(hgt, 0.2)/z0)/np.log(10/z0)*(1 - 0.25*np.clip(self.waves.hs/(2*np.maximum(hgt, 0.2)), 0, 1))
        wind = np.outer(prof*(1 + self.gust), [env["wind_u"], env["wind_v"], 0.0])
        rig_rel = pos[nfix:] - self.pivot_b
        rel_w = sub[:, None]*(cur + orb - vel_pts_w) + (1 - sub[:, None])*(wind - vel_pts_w)
        rel_b = rel_w @ R
        wx = np.einsum("ij,ij->i", rel_b, cx); wy = np.einsum("ij,ij->i", rel_b, ny)
        area = self._area; ar = self._ar
        rho = sub*RHO_W + (1 - sub)*RHO_A
        V2 = wx*wx + wy*wy; Vm = np.sqrt(V2) + 1e-9
        alpha = np.arctan2(wy, -wx)
        cl, cd = foil_coeffs(alpha, ar, self._cd0)
        q = 0.5*rho*V2*area
        ex_, ey_ = wx/Vm, wy/Vm
        px, py = -ey_, ex_
        flip = np.where(py*np.sign(-wx + 1e-12) < 0, -1.0, 1.0)
        fx = q*(cd*ex_ + cl*px*flip); fy = q*(cd*ey_ + cl*py*flip)
        Fs = fx[:, None]*cx + fy[:, None]*ny
        F += Fs.sum(0); M += cross(pos, Fs).sum(0)
        # rig torque about the pivot axis: it spins the free wing, not the hull
        tau_rig = float(cross(rig_rel, Fs[nfix:])[:, 2].sum())
        M[2] -= tau_rig
        # rig buoyancy
        if len(self.rp_pos):
            rp = (self.rp_pos @ Rg.T) + self.pivot_b
            rpw = s["r"] + rp @ R.T
            sd = rpw[:, 2] - (eta + ex*(rpw[:, 0] - x) + ey*(rpw[:, 1] - y))
            fsub = np.clip(0.5 - sd/0.04, 0, 1)
            if fsub.any():
                Fbw = np.outer(fsub*self.rp_vol*RHO_W*G, nw)
                Fbb = Fbw @ R
                F += Fbb.sum(0); M += cross(rp, Fbb).sum(0)
                tb = float(cross(rp - self.pivot_b, Fbb)[:, 2].sum())
                tau_rig += tb; M[2] -= tb
        # stiffness estimate for sub-stepping
        lever2 = (pos**2).sum(1)
        damp_rate = float(((0.5*rho*Vm*area*4.0)*sub).sum())
        rot_rate = float(((0.5*rho*Vm*area*4.0*lever2)).sum()/min(np.diag(self.Ifull)))
        rig_rate = float(((0.5*rho[nfix:]*Vm[nfix:]*area[nfix:]*4.0*(rig_rel**2).sum(1))).sum()/max(self.rig_I, 1e-3))
        # hull resistance / damping (relative to water)
        vrel_w = R @ v - cur
        vr = Rt @ vrel_w
        u = vr[0]
        if frac > 0.02:
            Rf = 0.5*RHO_W*u*abs(u)*self.vpp.s_hull*friction_cf(abs(u), self.lwl)*self.vpp.k*env.get("df", 1.0)
            Rw = wave_resistance(u, self.lwl, self.m*G, self.vpp.ws)*np.sign(u)
            F[0] -= (Rf + Rw)*min(frac, 1.0)
            F[1] -= 0.5*RHO_W*self.lat_area*0.8*vr[1]*abs(vr[1])*min(frac, 1.0)
            F[2] -= (self.b_heave*vr[2] + 0.5*RHO_W*self.awp*1.0*vr[2]*abs(vr[2]))*min(frac, 1.0)
            M[0] -= self.b_roll*w[0]*min(frac, 1.0)
            M[1] -= self.b_pitch*w[1]*min(frac, 1.0)
            M[2] -= 0.5*RHO_W*self.lat_area*0.8*(self.lwl/2)**3/4*w[2]*abs(w[2])*min(frac, 1.0)
        # hull windage
        aw_b = Rt @ (np.array([env["wind_u"], env["wind_v"], 0])*0.75 - R @ v)
        F += 0.5*RHO_A*np.linalg.norm(aw_b)*aw_b*np.array([0.15, 0.4, 0.0])*self.vpp.a_wind
        # thruster
        if ctrl.get("thrust", 0) > 0 and frac > 0.3:
            F[0] += ctrl["thrust"]
        return F, M, tau_rig, dict(eta=eta, frac=frac, n_sub=max(damp_rate*self.Minv.min(), rot_rate)*self.dt,
                                   rig_rate=rig_rate, depth_rig=depth[nfix:], alpha=alpha, nfix=nfix)

    # ---------------------------------------------------------------- integrate one outer step
    def advance(self, st, env, decision, dt_outer, t_abs):
        if self.state is None:
            self.init_state(st)
        s = self.state
        # sea state for this minute
        if abs(env["hs"] - self.waves.hs) > 0.05 or abs(env["tp"] - self.waves.tp) > 0.2 or abs(env["wave_dir"] - self.waves.dir) > 5:
            self.waves.set(env["hs"], env["tp"], env["wave_dir"])
        env = dict(env); env["df"] = st["df"] + (3.0 if st["entangled"] else 0)
        n = int(round(dt_outer/self.dt))
        acc = dict(u=0.0, v=0.0, heel=0.0, heel_max=0.0, alpha=0.0, delta=0.0, ve=0.0, vn=0.0)
        r0 = s["r"].copy()
        # control targets
        hdg_cmd = decision["heading"]; steer = decision["steering"] and st["rudder"] == "ok" and not st["brownout"]
        feather = decision["alpha_mode"] == "feather" or st["wing_lost"] or st["tail"] == "feathered" or st["brownout"]
        alpha_cmd = 0.0
        if not feather:
            alpha_cmd = math.radians(decision.get("alpha_deg", 10.0))
        thrust = self.d["power"]["thruster_n"] if st.get("thruster_on") else 0.0
        inv_time = 0.0
        for i in range(n):
            t = s["t"]
            self.gust += (-self.gust/20.0)*self.dt + 0.10*math.sqrt(2*self.dt/20.0)*self.rng.standard_normal()
            R = quat_to_R(s["q"])
            roll, pitch, yaw = euler_from_R(R)
            hdg_now = (90 - math.degrees(yaw)) % 360
            # rudder: heading PD
            if steer:
                err = math.radians(((hdg_cmd - hdg_now + 180) % 360) - 180)
                if abs(err) < 0.5:
                    self.hint = max(-0.3, min(0.3, getattr(self, "hint", 0.0) + 0.02*err*self.dt))
                want = max(-self.dmax, min(self.dmax, 1.2*err + 1.5*s["w"][2] + self.hint if hasattr(self, "hint") else 1.2*err + 1.5*s["w"][2]))
            elif st["rudder"] == "stuck":
                want = st["rudder_stuck"]*self.dmax
            else:
                want = 0.0 if st["rudder"] == "ok" else s["rud"]
            s["rud"] += max(-self.drate*self.dt, min(self.drate*self.dt, want - s["rud"]))
            # tail: hold the wing at +-alpha to the apparent wind, on the side that drives forward
            if not st["brownout"] and st["tail"] == "ok":
                aw_b = R.T @ (np.array([env["wind_u"], env["wind_v"], 0]) - R @ s["v"])
                flow = math.atan2(aw_b[1], aw_b[0])           # direction the air moves toward (body)
                best = None
                for sg in (1, -1):
                    cl_, cd_ = foil_coeffs(sg*alpha_cmd, self.vpp.ar_wing, 0.012)
                    # force in flow axes: drag along flow, lift perpendicular (sign follows the foil model)
                    ex_, ey_ = math.cos(flow), math.sin(flow)
                    gam_t = flow + math.pi + sg*alpha_cmd
                    wxw = math.cos(flow - gam_t); wyw = math.sin(flow - gam_t)
                    px, py = -wyw, wxw
                    fl = -1.0 if py*math.copysign(1, -wxw) < 0 else 1.0
                    fxw = cd_*wxw + cl_*px*fl; fyw = cd_*wyw + cl_*py*fl
                    fxb = fxw*math.cos(gam_t) - fyw*math.sin(gam_t)
                    if best is None or fxb > best[0]: best = (fxb, gam_t, sg)
                gerr = math.atan2(math.sin(best[1] - s["gam"]), math.cos(best[1] - s["gam"]))
                tail_cmd = -best[2]*alpha_cmd/max(self.kappa, 0.2) - 0.5*gerr
                tail_cmd = max(-self.tmax, min(self.tmax, tail_cmd))
            elif st["tail"] == "stuck":
                tail_cmd = -st["tail_stuck_alpha"]/max(self.kappa, 0.2)
            else:
                tail_cmd = 0.0
            s["tail"] += max(-1.0*self.dt, min(1.0*self.dt, tail_cmd - s["tail"]))
            ctrl = dict(thrust=thrust)
            F, M, tau, info = self.derivs(s, env, ctrl, t)
            nsub = int(min(max(math.ceil(info["n_sub"]/0.8), 1), 40))
            h = self.dt/nsub
            for kk in range(nsub):
                if kk:
                    F, M, tau, info = self.derivs(s, env, ctrl, t + kk*h)
                v, w = s["v"], s["w"]
                M = M.copy(); M[2] += self.fric*math.tanh(s["gamd"]/0.05)     # bearing friction reaction
                a = (F - self.m*cross(w, v))*self.Minv
                alp = self.Iinv @ (M - cross(w, self.I @ w))
                s["v"] = v + a*h
                s["w"] = w + alp*h
                R = quat_to_R(s["q"])
                s["r"] = s["r"] + (R @ s["v"])*h
                dq = 0.5*quat_mul(s["q"], np.r_[0.0, s["w"]])
                s["q"] = s["q"] + dq*h; s["q"] /= np.linalg.norm(s["q"])
                # wing DOF (implicit damping)
                c = info["rig_rate"]*self.rig_I
                torque = tau - self.fric*math.tanh(s["gamd"]/0.05)
                s["gamd"] = (s["gamd"] + h*torque/self.rig_I)/(1 + h*c/self.rig_I) - alp[2]*h
                s["gam"] = math.atan2(math.sin(s["gam"] + s["gamd"]*h), math.cos(s["gam"] + s["gamd"]*h))
            s["t"] = t + self.dt
            R = quat_to_R(s["q"]); roll, pitch, yaw = euler_from_R(R)
            vr = R.T @ (R @ s["v"] - np.array([env["cur_u"], env["cur_v"], 0]))
            acc["u"] += vr[0]; acc["v"] += vr[1]
            acc["heel"] += abs(math.degrees(roll)); acc["heel_max"] = max(acc["heel_max"], abs(math.degrees(roll)))
            acc["delta"] += math.degrees(s["rud"])
            if abs(roll) > math.radians(120): inv_time += self.dt
        r1 = s["r"]
        dr = r1 - r0
        R = quat_to_R(s["q"]); roll, pitch, yaw = euler_from_R(R)
        st["heading"] = (90 - math.degrees(yaw)) % 360
        if inv_time > 0.8*dt_outer and not st["inverted"]:
            st["inverted"] = True; st["capsizes"] += 1
        elif inv_time < 0.2*dt_outer and st["inverted"]:
            st["inverted"] = False
        st["knocked"] = acc["heel_max"] > 75
        st["roll_deg"], st["pitch_deg"] = math.degrees(roll), math.degrees(pitch)
        out = dict(u=acc["u"]/n, v=acc["v"]/n, heel=acc["heel"]/n, heel_max=acc["heel_max"], alpha=math.degrees(alpha_cmd),
                   delta=acc["delta"]/n, ve=dr[0]/dt_outer, vn=dr[1]/dt_outer, ground_included=True,
                   z=float(s["r"][2]))
        return out
