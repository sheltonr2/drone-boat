"""Motions, steering workload and cyclic loads of Rev E in steady sea states, from the 6-DOF model
(docs/Fatigue_Review.md, docs/Naval_Review.md items 4, 6 and 8).

For each sea state (Hs, Tp, a wind to match, waves on the quarter or on the beam) the 6-DOF model is run for
DUR seconds with the rudder either steering continuously (the model's PD autopilot) or under the Rev E rules
(2 deg deadband, a new rudder command at most every 10 s). From the recorded motion it works out, per hour:
  * rudder movements (half-cycles of at least 0.5 deg, by rainflow), rudder travel, heading error, speed
  * bending at the root of each part from gravity, the part's own acceleration (lumped masses) and the lift and
    drag on its foil strips: fin root, wing spar at its upper bearing, stern post, counterweight arm, tail boom,
    rudder stock at its lower bushing (per rudder), and the rudder's hinge torque on the servo
  * fatigue damage per hour (Miner) for each part from rainflow ranges, Goodman mean-stress correction and an S-N
    rule for its material (see SN below)
Not included: added mass of the fin and bulb, wave slap on the rig, knockdowns and breaking-wave strikes (those are
in docs/Structural_Review.md). Grade D. Run from the repo root: python docs/data/motions_loads.py  (about 15 min)
"""
import sys, math, json, time, inspect, textwrap
import numpy as np
sys.path.insert(0, 'simulator')
from drone_sim import design as D
from drone_sim import sixdof as SX
from drone_sim.sim import prepare_design

DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 1200.0       # seconds per case after a 120 s settling period
OUT = sys.argv[2] if len(sys.argv) > 2 else 'docs/data/motions_loads.json'
DT = 0.05; G = 9.81

# ---- instrumented 6-DOF: the same model, with the strip forces kept after each force evaluation
src = textwrap.dedent(inspect.getsource(SX.SixDOF.derivs))
anchor = "F += Fs.sum(0); M += cross(pos, Fs).sum(0)"
assert anchor in src
src = src.replace(anchor, anchor + "\n    self._cap = (Fs, pos)")
ns = dict(vars(SX)); exec(src, ns)
class Rec(SX.SixDOF):
    derivs = ns["derivs"]

def build(design):
    pr = prepare_design(design, cache_dir='/tmp/cache', log=lambda *a: None)
    return pr

# ---- rainflow (ASTM E1049 three-point) on a series: returns list of (range, mean, count 0.5/1)
def turning_points(x):
    x = np.asarray(x); d = np.diff(x); keep = [0]
    s_prev = 0
    for i, v in enumerate(d):
        s = np.sign(v)
        if s == 0: continue
        if s_prev != 0 and s != s_prev: keep.append(i)
        s_prev = s
    keep.append(len(x) - 1)
    return x[keep]
def rainflow(x):
    out = []; st = []
    for p in turning_points(x):
        st.append(p)
        while len(st) >= 3:
            X = abs(st[-1] - st[-2]); Y = abs(st[-2] - st[-3])
            if X < Y: break
            if len(st) == 3:
                out.append((Y, (st[-2] + st[-3])/2, 0.5)); st.pop(0)
            else:
                out.append((Y, (st[-2] + st[-3])/2, 1.0)); last = st.pop(); st.pop(); st.pop(); st.append(last)
    for a, b in zip(st[:-1], st[1:]): out.append((abs(b - a), (a + b)/2, 0.5))
    return out

# ---- S-N rules: N cycles to failure at amplitude Sa (mean-corrected) for a part with static strength Su (same units)
def n_fail(kind, Sa, Su):
    if Sa <= 0: return math.inf
    r = Sa/Su
    if kind == 'gfrp':  b = 0.10      # glass/epoxy and hardwood/glass: about 10% of static strength lost per decade
    elif kind == 'cfrp': b = 0.07     # carbon/epoxy tube
    elif kind == 'steel_sw':          # 316 in seawater, free corrosion: Sa 150 MPa at 1e6 cycles, slope 5, no endurance limit
        return 1e6*(150.0/(r*STOCK_YIELD_MPA))**5          # Su is the elastic-limit moment, so r*260 MPa is the stress
    return 10**((1 - r)/b) if r < 1 else 1.0
STOCK_YIELD_MPA = 260.0
# part: (strength in N*m at the root, S-N kind, note)  -- strengths from docs/Structural_Review.md and Design_RevC.md
PARTS = {"fin_root":       (1103.0, 'gfrp', "hardwood core, glass, carbon strip, Rev C2"),
         "spar_bearing":   (1130.0, 'cfrp', "30 x 22 carbon tube, Rev C3"),
         "stern_post":     (200.0,  'gfrp', "20 x 2 fibreglass tube, Rev C3 (estimate: 430 MPa flexural)"),
         "cw_arm":         (119.0,  'gfrp', "12 mm solid glass rod, Rev C3"),
         "tail_boom":      (53.0,   'cfrp', "12 x 10 carbon tube"),
         "rudder_stock":   (44.0,   'steel_sw', "12 mm 316 bar, elastic limit 44 N*m (260 MPa)")}

def damage(series, part):
    Su, kind, _ = PARTS[part]
    D_ = 0.0; amax = 0.0
    for rng, mean, c in rainflow(series):
        Sa = rng/2
        Sa_eq = Sa/max(1 - abs(mean)/Su, 0.05) if kind != 'steel_sw' else Sa/max(1 - abs(mean)/(Su*520/260), 0.05)
        amax = max(amax, Sa); D_ += c/n_fail(kind, Sa_eq, Su)
    return D_, amax

def run_case(design, hs, tp, U, rel_deg, rules, seed=3, alpha=10.0):
    d = json.loads(json.dumps(design))
    if rules:                                 # True = the Rev E rules as written; or (deadband_deg, update_s)
        rr = (2.0, 10.0) if rules is True else tuple(rules)
        d["rudder"]["deadband_deg"] = rr[0]; d["rudder"]["update_s"] = rr[1]
        if len(rr) > 2: d["rudder"]["cmd_deadband_deg"] = rr[2]      # (heading deadband, update interval, servo deadband,
        if len(rr) > 3: d["rudder"]["wave_filter_s"] = rr[3]         #  wave-filter time constant)
    pr = build(d); boat = pr["boat"]; cg = boat.cg; Sm = SX.S
    sd = Rec(boat, pr["vpp"], d, {"dt_6dof_s": DT}, np.random.default_rng(seed), log=lambda *a: None, cache_dir='/tmp/cache')
    course = 60.0; frm = (course + rel_deg) % 360                         # rel_deg: direction the waves come from, off the bow (starboard); 150 = on the quarter, 90 = on the beam
    tow = math.radians(frm + 180)
    env = dict(hs=hs, tp=tp, wave_dir=frm, wind_u=U*math.sin(tow), wind_v=U*math.cos(tow), cur_u=0.0, cur_v=0.0)
    st = dict(heading=course, lat=36.0, lon=-70.0, rudder='ok', brownout=False, wing_lost=False, tail='ok', inverted=False,
              capsizes=0, entangled=False, df=1.0)
    dec = dict(heading=course, steering=True, alpha_mode='sail', alpha_deg=alpha)
    n_settle = int(120/DT); n = int(DUR/DT)
    rec = {k: [] for k in ("v", "w", "q", "rud", "gam", "Fs", "pos", "u", "hdg")}
    for i in range(n_settle + n):
        r = sd.advance(st, env, dec, DT, i*DT)
        if i < n_settle: continue
        s = sd.state
        rec["v"].append(s["v"].copy()); rec["w"].append(s["w"].copy()); rec["q"].append(s["q"].copy())
        rec["rud"].append(s["rud"]); rec["gam"].append(s["gam"]); rec["u"].append(r["u"])
        Fs, pos = sd._cap; rec["Fs"].append(Fs.copy()); rec["pos"].append(pos.copy())
        rec["hdg"].append(((st["heading"] - course + 180) % 360) - 180)
    v = np.array(rec["v"]); w = np.array(rec["w"]); q = np.array(rec["q"])
    dv = np.gradient(v, DT, axis=0); al = np.gradient(w, DT, axis=0)
    a_cg = dv + np.cross(w, v)
    Rs = np.array([SX.quat_to_R(qq) for qq in q]); gb = np.einsum('nij,i->nj', Rs, np.array([0, 0, -G]))   # R^T g
    def body(p): return Sm @ (np.asarray(p, float) - cg)
    def inertial(m, r):                       # force on a lumped mass at body point r (array n x 3 or 3)
        r = np.broadcast_to(r, a_cg.shape)
        ap = a_cg + np.cross(al, r) + np.cross(w, np.cross(w, r))
        return m*(gb - ap)
    out = dict(hs=hs, tp=tp, U=U, rel_deg=rel_deg, rules=rules, dur_s=DUR, alpha=alpha,
               u_mean=float(np.mean(rec["u"])), hdg_err_rms=float(np.sqrt(np.mean(np.square(rec["hdg"])))),
               roll_rms=float(np.degrees(np.std([math.atan2(R[2, 1], R[2, 2]) for R in Rs]))),
               pitch_rms=float(np.degrees(np.std([-math.asin(max(-1, min(1, R[2, 0]))) for R in Rs]))),
               acc_lat_rms=float(np.std(a_cg[:, 1] - gb[:, 1])), acc_vert_rms=float(np.std(a_cg[:, 2])))
    # rudder workload
    rud = np.degrees(np.array(rec["rud"]))
    cyc = rainflow(rud)
    out["rudder_moves_per_h"] = sum(2*c for rg, _, c in cyc if rg >= 0.5)*3600/DUR
    out["rudder_travel_deg_per_h"] = float(np.abs(np.diff(rud)).sum()*3600/DUR)
    out["rudder_rms_deg"] = float(np.std(rud))
    Fs = np.array(rec["Fs"]); pos = np.array(rec["pos"])
    k = d["keel"]; nr = len(d["rudder"].get("y_offsets") or [0.0])
    # --- fin root (body x moment about the root point): bulb + fin weight/inertia, keel strip forces
    root = body([0.657 + 0.085, 0, 0.010])
    items = [m_ for m_ in boat.mass_items if m_[0] in ("lead bulb", "keel fin")]
    Mfin = np.zeros((len(v), 3))
    for nm, m_, p in items:
        rb = body(p); vol = (m_/11340.0 if nm == "lead bulb" else 0.0)
        F = inertial(m_, rb) - 1025*vol*gb                       # bulb's own buoyancy (submerged weight)
        Mfin += np.cross(rb - root, F)
    ki = slice(0, 5)
    Mfin += np.cross(pos[:, ki] - root, Fs[:, ki]).sum(1)
    # --- rudder stock at the lower bushing, per rudder, and hinge torque
    ri = sd.rudder_idx
    bush = body([d["rudder"]["stock_x"], 0, float(boat.hs.keel_z(d["rudder"]["stock_x"]))])
    Mstk = np.cross(pos[:, ri] - bush, Fs[:, ri]).sum(1)/nr
    rdn = np.stack([-np.sin(np.array(rec["rud"])), np.cos(np.array(rec["rud"])), np.zeros(len(v))], 1)
    Fn = np.einsum('nij,nj->n', Fs[:, ri], rdn)/nr
    hinge = Fn*(0.25*d["rudder"]["chord"] - d["rudder"]["stock_from_le"])
    # --- rig: spar at the upper bearing (55 mm below the wing root), on the mast axis
    wg = d["wing"]; tl = d["tail"]
    bear = body([wg["mast_x"], 0, wg["root_z"] - 0.055])
    rigcg = body([wg["mast_x"], 0, wg["root_z"] + boat.rig_cg_local[2]])
    rig_slice = slice(len(sd.fs_pos), None)
    Mspar = np.cross(rigcg - bear, inertial(boat.rig_mass, rigcg)) + np.cross(pos[:, rig_slice] - bear, Fs[:, rig_slice]).sum(1)
    # --- counterweight arm and tail boom: lumped masses on arms that turn with the wing (gamma)
    gam = np.array(rec["gam"]); cgm, sgm = np.cos(gam), np.sin(gam)
    def wingpt(xw, zdesign):
        z = zdesign - cg[2]
        return np.stack([cgm*xw, sgm*xw, np.full(len(gam), z)], 1) + np.array([sd.pivot_b[0], sd.pivot_b[1], 0])
    arm = wg["counterweight_arm"]
    pod = wingpt(arm, tl["boom_z"] + 0.01); proot = wingpt(0.0, tl["boom_z"] + 0.01)
    m_pod = boat.counterweight_kg + wg.get("pod_shell_kg", 0.11)
    Mcw = np.cross(pod - proot, inertial(m_pod, pod))
    tailp = wingpt(-tl["boom_length"], tl["bot_z"] + 0.05); troot = wingpt(0.0, tl["boom_z"])
    Mtb = np.cross(tailp - troot, inertial(tl["kg"] + 0.12, tailp)) + np.cross(pos[:, -1] - troot, Fs[:, -1])
    # --- stern post: lumped equipment at the top, root at the deck
    sp_root = body([1.53, 0, float(boat.hs.deck_z(1.5))])
    Msp = np.cross(body([1.53, 0, 0.42]) - sp_root, inertial(0.85, body([1.53, 0, 0.42]))) + \
          np.cross(body([1.53, 0, 0.60]) - sp_root, inertial(0.06, body([1.53, 0, 0.60])))
    def bend_series(M, axis=None):
        if axis is None: return M[:, 0], M[:, 1]                    # vertical members: the two horizontal axes
        u = axis/np.linalg.norm(axis, axis=1)[:, None]               # members along u: bending perpendicular to it
        Mp = M - (np.einsum('ij,ij->i', M, u))[:, None]*u
        zz = np.array([0, 0, 1.0]); h = np.cross(u, zz); h /= np.maximum(np.linalg.norm(h, axis=1), 1e-9)[:, None]
        return np.einsum('ij,ij->i', Mp, h), Mp[:, 2]
    loads = {"fin_root": bend_series(Mfin), "spar_bearing": bend_series(Mspar), "stern_post": bend_series(Msp),
             "cw_arm": bend_series(Mcw, pod - proot), "tail_boom": bend_series(Mtb, tailp - troot),
             "rudder_stock": bend_series(Mstk)}
    out["loads"] = {}
    for kpart, (a1, a2) in loads.items():
        d1, m1 = damage(a1, kpart); d2, m2 = damage(a2, kpart)
        nc = sum(c for rg, _, c in rainflow(a1) if rg > 0.02*PARTS[kpart][0]) + sum(c for rg, _, c in rainflow(a2) if rg > 0.02*PARTS[kpart][0])
        out["loads"][kpart] = dict(damage_per_h=(d1 + d2)*3600/DUR, max_amp=max(m1, m2), mean_abs=float(max(abs(np.mean(a1)), abs(np.mean(a2)))),
                                   p99_abs=float(max(np.percentile(np.abs(a1), 99), np.percentile(np.abs(a2), 99))),
                                   cycles_over_2pct_per_h=nc*3600/DUR, strength=PARTS[kpart][0])
    out["hinge_torque_nm"] = dict(rms=float(np.std(hinge)), p99=float(np.percentile(np.abs(hinge), 99)), max=float(np.abs(hinge).max()))
    out["roll_cycles_per_h"] = sum(c for rg, _, c in rainflow(np.degrees([math.atan2(R[2, 1], R[2, 2]) for R in Rs])) if rg > 2)*3600/DUR
    return out

if __name__ == "__main__":
    design = D.load('designs/revE_design.json')
    # sea states: Tp and wind to match a typical North Atlantic wind sea / swell mix (Tp = 6.5 + Hs s; U10 from a
    # developed sea, Hs = 0.0248 U10^2, at least 5 m/s); waves on the quarter (150 deg off the bow) or the beam (90)
    cases = []
    for hs in (0.75, 1.5, 2.5, 3.5, 5.0):
        tp = 6.5 + hs; U = max(5.0, math.sqrt(hs/0.0248))
        for rel in (150, 90):
            cases.append((hs, tp, U, rel, False, 10.0 if U < 13 else 6.0))     # steering rules: docs/data/steering_rules_sweep.py
    res = []
    for c in cases:
        t = time.time(); r = run_case(design, *c[:5], alpha=c[5]); res.append(r)
        L = r["loads"]
        print(f"Hs {c[0]:4.2f} Tp {c[1]:4.1f} U {c[2]:4.1f} waves {c[3]:3d} {'RevE rules' if c[4] else 'continuous'}: "
              f"u {r['u_mean']:.2f} m/s, hdg err {r['hdg_err_rms']:4.1f} deg, roll rms {r['roll_rms']:4.1f}, "
              f"rudder {r['rudder_moves_per_h']:6.0f} moves/h {r['rudder_travel_deg_per_h']:7.0f} deg/h, hinge p99 {r['hinge_torque_nm']['p99']:.2f} N*m | "
              + " ".join(f"{k} {v['p99_abs']:.1f}/{v['strength']:.0f}" for k, v in L.items()) + f"  ({time.time()-t:.0f} s)", flush=True)
    json.dump(res, open(OUT, 'w'), indent=1)
    print("Saved", OUT)
