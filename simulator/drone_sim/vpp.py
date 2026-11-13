"""Velocity prediction (force/moment equilibrium) for the hybrid simulator.

Solves, for arrays of conditions at once, the steady state of the boat:
    surge force = 0, sway force = 0  -> boat speed u and leeway velocity v
    yaw moment  = 0                  -> rudder angle
    heel moment = righting moment    -> heel angle
Boat frame: x forward, y to port, z up, origin at the CG. Wind arrives from starboard
(true wind angle twa in 0..pi). Results are tabulated into a polar the simulator interpolates.
"""
import math
import bisect
import os

import numpy as np

RHO_W, RHO_A, G, NU = 1025.0, 1.225, 9.81, 1.19e-6


# ----------------------------------------------------------------- foil model
# Speed-model version: part of the polar cache key, so cached speed tables are rebuilt when the model changes.
MODEL_VERSION = "2"     # 2 (12 Nov 2026): the wing stalls where its straight-line lift reaches WING_CL_STALL
WING_CL_STALL = 1.03    # NACA 0015 at the wing's Reynolds number (about 1-2 x 10^5); same value as boat-sim PR #325


def foil_coeffs(alpha, ar, cd0=0.009, e=0.85, stall_deg=None, cl_stall=None):
    """Lift/drag coefficients over the full +-180 deg range (finite wing, smooth stall).

    Stall angle: if cl_stall is given (> 0), the foil stalls where its straight-line lift reaches cl_stall, so a
    stubbier foil (lower lift slope) stalls at a higher angle, as real low-aspect-ratio wings do. Used for the wing.
    Otherwise the older rule 10 + 4*min(ar, 6)/6 degrees, kept for the keel and rudders (water, higher Reynolds number).
    The older rule made a stubbier foil stall sooner, which is backwards (found by John's team, boat-sim #326)."""
    a = np.arctan2(np.sin(alpha), np.cos(alpha))
    slope = 2*np.pi*ar / (2 + np.sqrt(ar**2 + 4))
    old = np.radians(10 + 4*np.minimum(ar, 6)/6)
    if stall_deg:
        s = np.radians(stall_deg)
    elif cl_stall is not None:
        cs = np.asarray(cl_stall, dtype=float)
        s = np.where(cs > 0, cs/np.maximum(slope, 1e-6), old)
    else:
        s = old
    cdmax = 1.11 + 0.018*np.minimum(ar, 20)
    cl_lin = slope*a; cd_lin = cd0 + cl_lin**2/(np.pi*e*ar)
    cl_fp = 0.5*cdmax*np.sin(2*a); cd_fp = cd0 + cdmax*np.sin(a)**2
    w = 1/(1 + np.exp((np.abs(a) - s)/math.radians(2.5)))
    return w*cl_lin + (1 - w)*cl_fp, w*cd_lin + (1 - w)*cd_fp


def foil_force(wx, wy, area, ar, rho, cd0=0.009):
    """Force on a symmetric foil with chord along x, in a flow (wx, wy) = velocity of the fluid
    relative to the foil. Returns (Fx, Fy)."""
    V2 = wx*wx + wy*wy
    V = np.sqrt(V2) + 1e-9
    alpha = np.arctan2(wy, -wx)                      # 0 when flow comes from ahead (wx<0)
    cl, cd = foil_coeffs(alpha, ar, cd0)
    q = 0.5*rho*V2*area
    ex, ey = wx/V, wy/V
    # lift perpendicular to flow, positive cl -> +y for flow from ahead
    lx, ly = ey, -ex
    sgn = np.where(-wx >= 0, 1.0, -1.0)
    return q*(cd*ex + cl*lx*sgn*np.sign(np.cos(alpha) + 1e-12)*np.sign(np.cos(alpha) + 1e-12)), \
           q*(cd*ey + cl*ly*sgn*np.sign(np.cos(alpha) + 1e-12)*np.sign(np.cos(alpha) + 1e-12))


def _foil(wx, wy, area, ar, rho, cd0=0.009):
    V2 = wx*wx + wy*wy; V = np.sqrt(V2) + 1e-9
    alpha = np.arctan2(wy, -wx)
    cl, cd = foil_coeffs(alpha, ar, cd0)
    q = 0.5*rho*V2*area
    ex, ey = wx/V, wy/V
    # unit vector perpendicular to the flow such that positive alpha (wy>0, flow from ahead) gives +y
    px, py = -ey, ex
    flip = np.where(px*0 + py*np.sign(-wx + 1e-12) < 0, -1.0, 1.0)
    px, py = px*flip, py*flip
    return q*(cd*ex + cl*px), q*(cd*ey + cl*py)


# ----------------------------------------------------------------- resistance
def friction_cf(u, lwl):
    re = np.maximum(np.abs(u)*lwl/NU, 1e4)
    return 0.075/(np.log10(re) - 2)**2


def wave_resistance(u, lwl, weight, scale):
    fn = np.abs(u)/math.sqrt(G*lwl)
    base = 0.012*(fn/0.4)**4
    wall = 0.25*np.clip(fn - 0.42, 0, None)**2*20
    return weight*scale*(base + wall)


def added_resistance(hs, tp, rel, lwl, bwl, scale):
    lam = G*np.maximum(tp, 1.0)**2/(2*np.pi)
    c = 2.0*np.clip(lwl/lam, 0, 1)**1.5
    f = 0.55 + 0.45*np.cos(rel)
    return scale*0.5*RHO_W*G*(hs/4)**2*bwl*c*f


# ----------------------------------------------------------------- the model
class VPP:
    def __init__(self, boat, stab=None):
        self.boat = boat
        d = boat.d; ref = boat.reference(); self.ref = ref
        self.W = boat.mass*G
        cg = boat.cg
        st = stab or boat.stability_summary()
        self.gz_ang = np.radians(st["gz_curve"]["angle"]); self.gz = np.array(st["gz_curve"]["gz"])
        i_max = int(np.argmax(self.gz)); self.phi_max = self.gz_ang[i_max]; self.rm_max = self.W*self.gz[i_max]
        self._gz_inc_a = self.gz_ang[:i_max + 1]; self._gz_inc = np.maximum.accumulate(self.gz[:i_max + 1])
        # geometry in boat frame (x forward from CG)
        self.x_keel = cg[0] - ref["x_keel"]; self.z_keel = ref["z_keel"] - cg[2]
        self.x_rud = cg[0] - ref["x_rudder"]; self.z_rud = ref["z_rudder"] - cg[2]
        self.x_piv = cg[0] - d["wing"]["mast_x"]; self.z_ce = ref["z_wing_ce"] - cg[2]
        self.z_hull = (ref["z_wl"] - 0.04) - cg[2]; self.x_hull = 0.15*ref["lwl"]
        self.z_wind = ref["z_wl"] + 0.08 - cg[2]
        self.ce_height = ref["z_wing_ce"] - ref["z_wl"]
        self.a_keel, self.ar_keel = ref["keel_area"], min(ref["keel_ar"], 8)
        self.a_rud, self.ar_rud = ref["rudder_area"], min(ref["rudder_ar"], 8)
        self.a_wing, self.ar_wing = ref["wing_area"], ref["wing_ar"]
        self.s_hull = ref["s_hull"] + boat.bulb_area_wet
        self.lwl, self.bwl = max(ref["lwl"], 0.3), max(ref["bwl"], 0.05)
        self.a_lat = ref["hull_lat_area"]; self.a_wind = ref["hull_windage_area"] + 0.08
        self.bulb_frontal = ref["bulb_frontal"]
        h = d["hydro"]; self.k = h["form_factor"]; self.ws = h["wave_resistance_scale"]
        self.aws = h["added_resistance_scale"]; self.cd_lat = h["hull_lateral_cd"]
        self.dmax = math.radians(d["rudder"]["max_angle_deg"])
        self.heel_limit = math.radians(d["autopilot"]["heel_limit_deg"])

    def wind_at(self, tws, hs):
        z0 = 2e-4 + 0.002*hs
        f = np.log(np.maximum(self.ce_height, 0.2)/z0)/np.log(10/z0)
        shelter = 1 - 0.25*np.clip(hs/(2*np.maximum(self.ce_height, 0.2)), 0, 1)
        return tws*f*shelter

    def forces(self, u, v, phi, delta, U, twa, alpha, hs, tp, df, thrust=0.0):
        cphi = np.cos(phi)
        # ---- air: apparent wind = air velocity relative to the boat
        ax = -U*np.cos(twa) - u; ay = U*np.sin(twa) - v
        ayh = ay*cphi
        V = np.sqrt(ax**2 + ayh**2) + 1e-9
        ex, ey = ax/V, ayh/V
        cl, cd = foil_coeffs(alpha, self.ar_wing, cd0=0.012, cl_stall=WING_CL_STALL)
        q = 0.5*RHO_A*V**2*self.a_wing
        # lift perpendicular to flow, side chosen to drive forward
        p1x, p1y = ey, -ex
        s = np.where(p1x >= 0, 1.0, -1.0)
        Fwx = q*(cd*ex + cl*s*p1x); Fwy = q*(cd*ey + cl*s*p1y)
        # tail drag (small) and hull windage
        Fwx += 0.5*RHO_A*V**2*0.012*0.03*ex; Fwy += 0.5*RHO_A*V**2*0.012*0.03*ey
        Uh = U*0.75
        hx = -Uh*np.cos(twa) - u; hy = (Uh*np.sin(twa) - v)*cphi
        Vh = np.sqrt(hx**2 + hy**2) + 1e-9
        qh = 0.5*RHO_A*Vh*self.a_wind*0.9
        Fhx = qh*hx*0.35; Fhy = qh*hy                     # streamlined fore-aft, bluff side-on
        # ---- water
        wx, wy = -u, -v*cphi
        Fkx, Fky = _foil(wx, wy, self.a_keel, self.ar_keel, RHO_W)
        cd_, sd_ = np.cos(delta), np.sin(delta)
        rwx, rwy = -u, -v*cphi*0.75 + 0*self.x_rud
        # rudder chord rotated by delta (positive delta = trailing edge to port -> bow turns starboard)
        lx = rwx*cd_ + rwy*sd_; ly = -rwx*sd_ + rwy*cd_
        frx, fry = _foil(lx, ly, self.a_rud, self.ar_rud, RHO_W)
        Frx = frx*cd_ - fry*sd_; Fry = frx*sd_ + fry*cd_
        Vw2 = u*u + v*v
        beta = np.arctan2(v, np.abs(u) + 1e-6)
        Fhy_lift = -0.5*RHO_W*Vw2*self.a_lat*0.35*np.sin(2*beta)
        Fhy_cross = -0.5*RHO_W*self.a_lat*self.cd_lat*v*np.abs(v)
        cf = friction_cf(u, self.lwl)
        Rf = 0.5*RHO_W*u*np.abs(u)*self.s_hull*cf*self.k*df
        Rb = 0.5*RHO_W*u*np.abs(u)*self.bulb_frontal*0.1
        sgn = u/np.sqrt(u*u + 0.02**2)
        Rw = wave_resistance(u, self.lwl, self.W, self.ws)*sgn
        Raw = added_resistance(hs, tp, twa, self.lwl, self.bwl, self.aws)*sgn*np.clip(np.abs(u)/0.6, 0, 1)
        Fx = Fwx + Fhx + Fkx + Frx - Rf - Rb - Rw - Raw + thrust
        Fy = (Fwy + Fhy)*cphi + (Fky + Fry)*cphi + Fhy_lift + Fhy_cross
        N = Fwy*cphi*self.x_piv + Fky*cphi*self.x_keel + Fry*cphi*self.x_rud + (Fhy_lift + Fhy_cross)*self.x_hull \
            + Fhy*cphi*0.0
        Mx = Fwy*self.z_ce + Fhy*self.z_wind + Fky*self.z_keel + Fry*self.z_rud + (Fhy_lift + Fhy_cross)*self.z_hull
        return Fx, Fy, N, Mx

    def heel_from_moment(self, Mx):
        m = np.abs(Mx)/self.W
        knock = m > self._gz_inc[-1]
        phi = np.interp(m, self._gz_inc, self._gz_inc_a)
        return np.where(knock, math.pi/2, phi)*np.sign(Mx + 1e-12), knock

    def solve(self, tws, twa, hs, tp, alpha, df, thrust=0.0, iters=80, u0=None):
        shp = np.broadcast(tws, twa, hs, tp, alpha, df).shape
        tws, twa, hs, tp, alpha, df = [np.broadcast_to(np.asarray(a, float), shp).ravel().copy() for a in (tws, twa, hs, tp, alpha, df)]
        U = self.wind_at(tws, hs)
        u = np.full(tws.shape, 0.3) if u0 is None else np.asarray(u0, float).ravel().copy()
        v = np.zeros_like(u); phi = np.zeros_like(u); delta = np.zeros_like(u)
        eps = 1e-4
        for it in range(iters):
            Fx, Fy, N, Mx = self.forces(u, v, phi, delta, U, twa, alpha, hs, tp, df, thrust)
            Fx_u, Fy_u, _, _ = self.forces(u + eps, v, phi, delta, U, twa, alpha, hs, tp, df, thrust)
            Fx_v, Fy_v, _, _ = self.forces(u, v + eps, phi, delta, U, twa, alpha, hs, tp, df, thrust)
            a11 = (Fx_u - Fx)/eps; a12 = (Fx_v - Fx)/eps; a21 = (Fy_u - Fy)/eps; a22 = (Fy_v - Fy)/eps
            det = a11*a22 - a12*a21
            det = np.where(np.abs(det) < 1e-9, -1e-9, det)
            du = (-Fx*a22 + Fy*a12)/det; dv = (-a11*Fy + a21*Fx)/det
            lim = 0.3
            du = np.clip(du, -lim, lim); dv = np.clip(dv, -lim, lim)
            damp = 0.7 if it < 10 else 1.0
            u = u + damp*du; v = v + damp*dv
            # rudder for yaw balance
            _, _, N1, _ = self.forces(u, v, phi, delta + 0.01, U, twa, alpha, hs, tp, df, thrust)
            _, _, N0, Mx0 = self.forces(u, v, phi, delta, U, twa, alpha, hs, tp, df, thrust)
            dN = (N1 - N0)/0.01
            dN = np.where(np.abs(dN) < 1e-6, -1e-6, dN)
            step = np.clip(-0.6*N0/dN, -0.08, 0.08)
            delta = np.clip(delta + step, -1.2*self.dmax, 1.2*self.dmax)
            new_phi, knock = self.heel_from_moment(Mx0)
            phi = 0.6*phi + 0.4*new_phi
        Fx, Fy, N, Mx = self.forces(u, v, phi, delta, U, twa, alpha, hs, tp, df, thrust)
        res = np.abs(Fx) + np.abs(Fy)
        ok = (res < 0.05 + 0.0002*self.W) & np.isfinite(u)
        balanced = np.abs(N) < 0.05
        _, knock = self.heel_from_moment(Mx)
        out = dict(u=u, v=v, phi=np.abs(phi), delta=delta, ok=ok, knock=knock,
                   rudder_ok=(np.abs(delta) <= self.dmax) & balanced)
        return {k: val.reshape(shp) for k, val in out.items()}


TWS = np.array([0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 17, 20, 24, 28.0])
TWA = np.radians(np.arange(0, 181, 7.5))
HS = np.array([0, 0.5, 1.5, 3, 5, 8.0])
DF = np.array([1, 1.6, 2.5, 4.0])
ALPHAS = np.radians([0, 2.5, 5, 7.5, 10, 12.5, 15, 20])


def tp_for(hs):
    """Typical peak period for a wind sea of height hs (used only to build the table)."""
    return 3.5 + 2.2*np.sqrt(np.maximum(hs, 0))


def build_polar(vpp):
    """Tabulate optimal (and feathered) equilibrium over (tws, twa, hs, df)."""
    T, A, H, F, AL = np.meshgrid(TWS, TWA, HS, DF, ALPHAS, indexing="ij")
    r = vpp.solve(T, A, H, tp_for(H), AL, F)
    u = r["u"]
    feasible = r["ok"] & r["rudder_ok"] & (r["phi"] <= vpp.heel_limit + 1e-6) & ~r["knock"]
    score = np.where(feasible, u, -1e9)
    score[..., 0] = np.where(score[..., 0] < -1e8, u[..., 0] - 1e3, score[..., 0])   # feathered always allowed
    best = np.argmax(score, axis=-1)
    take = lambda X: np.take_along_axis(X, best[..., None], -1)[..., 0]
    pol = dict(u=take(u), v=take(r["v"]), phi=take(r["phi"]), delta=take(r["delta"]),
               alpha=ALPHAS[best],
               u_f=u[..., 0], v_f=r["v"][..., 0], phi_f=r["phi"][..., 0], delta_f=r["delta"][..., 0],
               knock_f=r["knock"][..., 0].astype(float),
               ok=take(r["ok"].astype(float)))
    pol["grid"] = dict(tws=TWS, twa=TWA, hs=HS, df=DF)
    return pol


REFERENCE = os.environ.get("DRONE_SIM_REFERENCE", "") == "1"   # 1: the original (slower) lookups, for checking


class Polar:
    """Fast multilinear interpolation into the tabulated polar.

    Speed-up of 13 Nov 2026: the same 16-corner sum in the same order, on plain Python floats taken from
    the same float64 tables, so results are bit-for-bit identical (DRONE_SIM_REFERENCE=1 runs the original)."""
    def __init__(self, pol):
        self.p = pol; g = pol["grid"]
        self.axes = [g["tws"], g["twa"], g["hs"], g["df"]]
        self._ax = [[float(v) for v in a] for a in self.axes]
        shp = [len(a) for a in self.axes]
        self._strides = (shp[1]*shp[2]*shp[3], shp[2]*shp[3], shp[3], 1)
        self._flat = {}

    def _flat_table(self, k):
        t = self._flat.get(k)
        if t is None:
            t = self._flat[k] = np.asarray(self.p[k], dtype=float).ravel().tolist()
        return t

    @staticmethod
    def _idx_fast(ax, x):
        x = min(max(x, ax[0]), ax[-1])
        i = bisect.bisect_left(ax, x) - 1; i = min(max(i, 0), len(ax) - 2)
        f = (x - ax[i])/(ax[i + 1] - ax[i])
        return i, f

    def _idx(self, ax, x):
        x = min(max(x, ax[0]), ax[-1])
        i = int(np.searchsorted(ax, x) - 1); i = min(max(i, 0), len(ax) - 2)
        f = (x - ax[i])/(ax[i + 1] - ax[i])
        return i, f

    def __call__(self, tws, twa, hs, df, keys=("u", "v", "phi", "delta", "alpha")):
        """twa in RADIANS (0 to pi). A value above about 3.2 is almost certainly degrees passed by mistake."""
        if abs(twa) > 3.2:
            raise ValueError(f"Polar: wind angle {twa!r} looks like degrees; pass radians")
        if not REFERENCE:
            idx = [self._idx_fast(a, x) for a, x in zip(self._ax, (tws, abs(twa), hs, df))]
            st = self._strides
            corners = []
            for c in range(16):                         # same weights, same order, same zero-skip as below
                w = 1.0; flat = 0
                for dim in range(4):
                    bit = (c >> dim) & 1
                    i, f = idx[dim]
                    w *= f if bit else (1 - f)
                    flat += (i + bit)*st[dim]
                if w:
                    corners.append((w, flat))
            out = {}
            for k in keys:
                t = self._flat_table(k); acc = 0.0
                for w, flat in corners:
                    acc += w*t[flat]
                out[k] = float(acc)
            return out
        idx = [self._idx(a, x) for a, x in zip(self.axes, (tws, abs(twa), hs, df))]
        out = {}
        for k in keys:
            arr = self.p[k]; acc = 0.0
            for c in range(16):
                w = 1.0; sl = []
                for dim in range(4):
                    bit = (c >> dim) & 1
                    i, f = idx[dim]
                    w *= f if bit else (1 - f)
                    sl.append(i + bit)
                if w:
                    acc += w*arr[sl[0], sl[1], sl[2], sl[3]]
            out[k] = float(acc)
        return out

    def best_vmg_angles(self, tws, hs=0.5, df=1.0):
        twa = self.axes[1]
        u = np.array([self(tws, a, hs, df, ("u",))["u"] for a in twa])
        u = np.maximum(u, 0.0)
        vmg = u*np.cos(twa)
        upm = twa < np.pi/2; dnm = twa > np.pi/2
        up = twa[upm][np.argmax(vmg[upm])]; dn = twa[dnm][np.argmin(vmg[dnm])]
        return float(up), float(dn)
