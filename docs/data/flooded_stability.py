"""Flooded stability of Rev E (docs/Naval_Review.md, item 5; docs/Flooded_Stability.md).

Rev E keeps sailing with water aboard and the pump running, and goes to SAFE only above 1.5 kg. This checks what
water in the boat does to the righting-arm (GZ) curve, at 0, 0.5, 1.5 and 3.0 kg (3.0 kg is the model's flood
limit, the 3 L of open space left in the dry bay).

Water is treated three ways:
  solid  - frozen at the bottom of the sump (no free surface): the optimistic case
  sump   - free liquid that stays in the sump (x 0.56-0.77 m, below z 0.045 m, keel box excluded): the fitted foam
           blocks hold it there. When the sump is full it overflows into the rest of the bay
  bay    - free liquid that can run anywhere in the dry bay between the bulkheads (x 0.30-1.26 m), as if the foam
           blocks did not fit at all: the pessimistic bound
At every heel angle the water's surface is level with the sea's (body frame plane normal from the heel and trim),
the water fills the lowest part of the space it is allowed, and the boat's trim is solved with the water's
centroid recomputed. Hull inner surface = outer surface (shell thickness ignored, a few % optimistic on volume).
Run from the repo root: python docs/data/flooded_stability.py   (about 5-10 minutes)
"""
import sys, math, json, time
import numpy as np
sys.path.insert(0, 'simulator')
from drone_sim import design as D
from drone_sim.geometry import Boat, _equilibrium, _rot, _plane_normal, RHO_W, _hb_at

RHO_SEA = 1025.0
d = D.load('designs/revE_design.json')
boat = Boat(d); hs = boat.hs
H = 0.006                                    # voxel size, m

def voxels(x0, x1, ztop=None):
    xs = np.arange(x0 + H/2, x1, H); pts = []
    for x in xs:
        zk, zd = float(hs.keel_z(x)), float(hs.deck_z(x))
        zt = min(zd, ztop) if ztop is not None else zd
        for z in np.arange(zk + H/2, zt, H):
            b = _hb_at(hs, x, z)
            ys = np.arange(-b + H/2, b, H)
            if len(ys): pts.append(np.c_[np.full(len(ys), x), ys, np.full(len(ys), z)])
    P = np.vstack(pts)
    keelbox = (P[:, 0] > 0.650) & (P[:, 0] < 0.772) & (np.abs(P[:, 1]) < 0.030) & (P[:, 2] < 0.080)
    return P[~keelbox]

SUMP = voxels(0.56, 0.77, ztop=0.045)
BAY = voxels(0.30, 1.26)
VOX = H**3
sump_cap = len(SUMP)*VOX
print(f"Sump capacity {1000*sump_cap:.2f} L ({len(SUMP)} voxels); dry-bay envelope {1000*len(BAY)*VOX:.1f} L")

def water_centroid(mode, mw, phi, theta):
    vol = mw/RHO_SEA
    if mode == 'solid':
        n = np.array([0, 0, 1.0])          # fixed: the lowest part of the sump, upright
        space = SUMP
    else:
        n = _plane_normal(phi, theta)
        space = SUMP if (mode == 'sump' and vol <= sump_cap) else BAY
    k = min(int(round(vol/VOX)), len(space))
    h = space @ n
    idx = np.argpartition(h, k - 1)[:k] if k < len(space) else np.arange(len(space))
    return space[idx].mean(axis=0)

V, F = boat.combined()

def gz_curve(mode, mw, angles):
    M = boat.mass + mw; disp = M/RHO_W
    out = []; th = 0.0
    for phi in angles:
        ph = math.radians(phi)
        def fx(theta):
            cg = boat.cg if mw == 0 else (boat.mass*boat.cg + mw*water_centroid(mode, mw, ph, theta))/M
            vol, cb, h = _equilibrium(V - cg, F, ph, theta, disp)
            return float((_rot(ph, theta) @ cb)[0]), cb
        t0 = th; f0, cb = fx(t0); t1 = t0 + 0.05; f1, cb1 = fx(t1)
        for _ in range(10):
            if abs(f1) < 2e-4 or abs(f1 - f0) < 1e-9: break
            t2 = float(np.clip(t1 - f1*(t1 - t0)/(f1 - f0), t1 - 0.2, t1 + 0.2)); t2 = float(np.clip(t2, -1.3, 1.3))
            t0, f0 = t1, f1; t1 = t2; f1, cb1 = fx(t1)
        th = t1
        out.append((phi, float(-(_rot(ph, th) @ cb1)[1]), math.degrees(th)))
    return np.array(out)

ANG = np.r_[0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 175, 180]
cases = [('intact', 'solid', 0.0)] + [(f'{m} {w} kg', m, w) for w in (0.5, 1.5, 3.0) for m in ('solid', 'sump', 'bay')]
res = {}
for name, mode, mw in cases:
    t = time.time(); a = gz_curve(mode, mw, ANG); ang, gz, trim = a[:, 0], a[:, 1], a[:, 2]
    gm = gz[1]/math.radians(5)
    avs = 180.0
    for i in range(1, len(ang)):
        if gz[i] < 0 <= gz[i-1]: avs = ang[i-1] + (ang[i] - ang[i-1])*gz[i-1]/(gz[i-1] - gz[i]); break
    pos = np.trapezoid(np.clip(gz, 0, None), np.radians(ang)); neg = -np.trapezoid(np.clip(gz, None, 0), np.radians(ang))
    M = boat.mass + mw
    res[name] = dict(water_kg=mw, mode=mode, gm_m=gm, gz20_m=float(gz[4]), max_gz_m=float(gz.max()), angle_max=float(ang[np.argmax(gz)]),
                     avs_deg=float(avs), rm20_nm=float(gz[4]*M*9.81), pos_area=float(pos), neg_area=float(neg),
                     trim0_deg=float(trim[0]), gz=gz.round(4).tolist())
    print(f"{name:16s} GM {gm:.3f} m  GZ(20) {gz[4]*1000:5.1f} mm  max GZ {gz.max()*1000:5.0f} mm at {ang[np.argmax(gz)]:.0f}  "
          f"vanishing angle {avs:5.1f}  righting moment at 20 deg {gz[4]*M*9.81:5.1f} N.m  trim {trim[0]:+.2f} deg  ({time.time()-t:.0f} s)", flush=True)
res['_angles'] = ANG.tolist(); res['_sump_capacity_l'] = 1000*sump_cap
json.dump(res, open('docs/data/flooded_stability.json', 'w'), indent=1)
