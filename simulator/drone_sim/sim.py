"""Voyage simulator: environment + physics backend (hybrid or 6-DOF) + autopilot + power +
satellite comms + failures. One call to run_voyage() simulates one crossing."""
import math, time, json, copy, os
import numpy as np

from .env import make_provider, LandMask, destination, haversine_km, bearing_deg, to_epoch, from_epoch
from .autopilot import Autopilot, wrap180
from .bulk import BulkDataMissing
from .failures import DEFAULT_RATE_SET, rates_for, early_life_factor, wear_out_factor, p_event, breaking_knockdown_rate
from . import geometry, vpp as vppmod

DEFAULT_SCENARIO = {
    "name": "Ocean City, MD to south-west Ireland",
    "start_time": "2024-05-15T12:00:00",
    "start": {"lat": 38.02, "lon": -74.01},      # ~100 km off Ocean City, MD (drift tests, Nov 2026: 25 km drops drifted ashore)
    "target": {"lat": 51.35, "lon": -9.7},       # off Mizen Head; any landfall in Europe also counts
    "waypoints": [[42.0, -48.0]],                # stay south of the Grand Banks (fishing fleets, fog, icebergs)
    "arrival_radius_km": 40.0,
    "waypoint_rule": "radius",         # radius: within 25 km (original) | abeam: also once passed (launch study)
    "europe_landfall_counts": True,
    "atlantic_islands_count": False,   # Azores, Madeira, Canaries: count a landfall there as reaching Europe?
    "africa_landfall_counts": False,   # North-west Africa's Atlantic coast counts as across (destination study)
    "max_days": 240,
    "mode": "hybrid",              # hybrid | 6dof
    "dt_s": 300.0,                 # hybrid step
    "dt_6dof_s": 0.05,
    "log_interval_min": 30.0,
    "provider": "openmeteo",       # openmeteo | bulk (downloaded months, see bulk.py) | synthetic
    "grid_deg": 1.0,
    # 0.25-degree weather where the Gulf Stream and North Atlantic Current run (see TwoGridProvider)
    "fine_grid": {"deg": 0.25, "lat": [30.0, 50.0], "lon": [-80.0, -38.0]},
    "seed": 1,
    "commands": [],                # [{"t_hours": 240, "cmd": "SET_REPORT", "args": {"hours": 1}}]
    "operator": {"auto_reboot_after_silence_h": 24},
    "failure_rate_set": DEFAULT_RATE_SET,   # planning | historical | original (see failures.py)
    "failures": {},                         # per-entry overrides of the rate set
    "failures_enabled": True,
    "initial_mode": "sail",
}



# --------------------------------------------------------------------- design cache
_CACHE = {}


def prepare_design(design, cache_dir="cache", log=print):
    """Geometry, stability and the polar table for a design (cached in memory and on disk)."""
    from .design import design_hash
    h = design_hash(design)
    if h in _CACHE: return _CACHE[h]
    boat = geometry.Boat(design)
    stab = boat.stability_summary()
    vp = vppmod.VPP(boat, stab)
    p = os.path.join(cache_dir, "polars", f"{h}_v{vppmod.MODEL_VERSION}.npz")
    if os.path.exists(p):
        z = np.load(p, allow_pickle=True); pol = {k: z[k] for k in z.files if k != "grid"}
        pol["grid"] = z["grid"].item()
    else:
        log("Building the speed polar for this design (about 10-30 s) ...")
        pol = vppmod.build_polar(vp)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        np.savez_compressed(p, **{k: v for k, v in pol.items() if k != "grid"}, grid=np.array(pol["grid"], dtype=object))
    out = dict(boat=boat, stab=stab, vpp=vp, polar=vppmod.Polar(pol), polar_raw=pol, hash=h)
    _CACHE[h] = out
    return out


# --------------------------------------------------------------------- simulation
class Voyage:
    def __init__(self, design, scenario, cache_dir="cache", log=print, progress=None, land=None, provider=None,
                 prepared=None):
        self.d = design; self.sc = sc = {**copy.deepcopy(DEFAULT_SCENARIO), **scenario}
        self.log = log; self.progress = progress; self.cache_dir = cache_dir; self.backend = None
        self.prep = prepared or prepare_design(design, cache_dir, log)
        self.boat = self.prep["boat"]; self.polar = self.prep["polar"]; self.stab = self.prep["stab"]
        self.env = provider or make_provider(sc["provider"], cache_dir, log, sc["grid_deg"], sc["seed"], sc.get("fine_grid"))
        self.land = land or LandMask(cache_dir, allow_download=(sc["provider"] != "synthetic"), log=log)
        self.rng = np.random.default_rng(sc["seed"])
        self.events = []
        self.ap = Autopilot(design, sc, self.polar, self.land, self.event)
        self.fr = rates_for(sc)
        from .structure import load_tables
        self.struct = load_tables(design)     # structural failures in knockdowns (None = off)
        self.fail_on = sc.get("failures_enabled", True)
        self.cmds = sorted(sc.get("commands", []), key=lambda c: c["t_hours"])
        # Watch lines (scenario key "watch_lines": {name: [[lat, lon], ...]}): hazards the coastline file does not hold,
        # such as shoals. The voyage is not changed; the result reports the closest approach to each line in km.
        self.watch = {k: [tuple(q) for q in v] for k, v in (sc.get("watch_lines") or {}).items()}
        self.watch_min = {k: 1e9 for k in self.watch}

    def event(self, t, kind, msg):
        self.events.append(dict(t=float(t), day=round((t - self.t0)/86400, 3), kind=kind, msg=msg))

    def rate(self, name):
        f = self.fr[name]
        if not (self.fail_on and f.get("enabled", True)):
            return 0.0
        m = (self.d.get("electronics_protection") or {}).get(name, 1.0)   # Rev D coating/potting credit
        return f["per_day"] * m

    # -------------------------------------------------------------- run
    def run(self):
        sc, d = self.sc, self.d
        self.t0 = t = to_epoch(sc["start_time"])
        t_end = t + sc["max_days"]*86400
        if sc["provider"] == "openmeteo" and t_end > time.time() - 3*86400:
            t_end = time.time() - 3*86400
            self.log("Historic data ends a few days before today; the voyage is cut off there.")
        mode6 = sc["mode"] == "6dof"
        dt = float(sc["dt_s"]) if not mode6 else 60.0          # outer step (6-DOF integrates inside)
        P = d["power"]
        st = dict(lat=sc["start"]["lat"], lon=sc["start"]["lon"], heading=bearing_deg(sc["start"]["lat"], sc["start"]["lon"],
                  sc["target"]["lat"], sc["target"]["lon"]), soc=0.9, stw=0.0, sog=0.0, heel=0.0, df=1.0,
                  water_kg=0.0, inverted=False, knocked=False, rudder="ok", rudder_stuck=0.0, tail="ok",
                  rudders_ok=len(d["rudder"].get("y_offsets") or [0.0]),
                  tail_stuck_alpha=0.0, wing_lost=False, entangled=False, hung=False, comms_dead=False,
                  brownout=False, leak_rate=0.0, leak_alarm=False, thrust_h_today=0.0, alive=True, credits=0,
                  sessions_ok=0, sessions_fail=0, last_report=t, last_report_ok=t, energy_in_wh=0.0,
                  energy_out_wh=0.0, distance_km=0.0, knockdowns=0, capsizes=0, box_dead=False, kd_hs=[0]*10, post_bent=False,
                  limp_ok=bool((d.get("limp_home") or {}).get("fitted")), limp_on=False)
        BT = d.get("backup_tracker") or {}
        st.update(trk_ok=bool(BT.get("fitted")), trk_next=t, trk_sent=0, trk_fixes=0, trk_last_ok=None,
                  trk_budget=int(BT.get("transmissions", 2500)*BT.get("cold_derate", 1.0)))
        self.st = st
        self.event(t, "start", f"Launch at {st['lat']:.2f}, {st['lon']:.2f}")
        backend = None
        if mode6:
            from .sixdof import SixDOF
            backend = SixDOF(self.boat, self.prep["vpp"], self.d, self.sc, self.rng, self.log,
                             cache_dir=self.cache_dir)
            self.backend = backend
        log_every = sc["log_interval_min"]*60
        next_log = t; series = []
        next_decision = t; cmd_i = 0; pending = []
        decision = dict(heading=st["heading"], alpha_mode="best", thruster=False, steering=True)
        day_mark = math.floor(t/86400)
        outcome = None; wall0 = time.time()
        total_steps = (t_end - t)/dt
        k = 0
        L = self.boat.hs.L; Bm = self.boat.hs.B
        while t < t_end:
            k += 1
            try:
                e = self.env.sample(st["lat"], st["lon"], t)
            except BulkDataMissing as ex:
                if k == 1: raise
                outcome = "at_sea_timeout"; self.event(t, "end", f"Weather data ends here: {ex}")
                break
            # water-relative wind
            wu, wv = e["wind_u"] - e["cur_u"], e["wind_v"] - e["cur_v"]
            tws = math.hypot(wu, wv); twd = (math.degrees(math.atan2(-wu, -wv))) % 360   # FROM direction
            envd = dict(tws=tws, twd=twd, hs=e["hs"], df=st["df"])
            # commands queued by the operator become available at their time; delivered at next good session
            while cmd_i < len(self.cmds) and self.cmds[cmd_i]["t_hours"]*3600 + self.t0 <= t:
                pending.append(self.cmds[cmd_i]); cmd_i += 1
            # daily reset
            if math.floor(t/86400) != day_mark:
                day_mark = math.floor(t/86400); st["thrust_h_today"] = 0.0
            # ---- autopilot decisions
            controllable = st["alive"] and not st["brownout"] and not st["inverted"] and (not st["box_dead"] or st["limp_on"])
            if controllable and t >= next_decision:
                decision = self.ap.decide(t, st, envd)
                next_decision = t + d["autopilot"]["decision_interval_min"]*60
            # ---- physics step
            if mode6 and not st["box_dead"]:
                twa_s = wrap180(twd - st["heading"])
                pr = self.polar(tws, math.radians(abs(twa_s)), e["hs"], st["df"], ("alpha",))   # the polar's angle axis is radians
                decision["alpha_deg"] = math.degrees(pr["alpha"])
                st["thruster_on"] = bool(decision.get("thruster")) and not st["brownout"]
                if st["thruster_on"]: st["thrust_h_today"] += dt/3600
                res = backend.advance(st, e, decision, dt, t)
            else:
                res = self.hybrid_step(st, e, envd, decision, dt, t)
            # ---- kinematics: water-relative velocity + current + Stokes drift
            hdg = math.radians(st["heading"])
            fe, fn = math.sin(hdg), math.cos(hdg); pe, pn = -math.cos(hdg), math.sin(hdg)
            if res.get("ground_included"):
                ve, vn = res["ve"], res["vn"]
            else:
                ve = res["u"]*fe + res["v"]*pe; vn = res["u"]*fn + res["v"]*pn
            if not res.get("ground_included"):
                ve += e["cur_u"]; vn += e["cur_v"]
                if e["hs"] > 0.05 and not e.get("current_includes_stokes"):   # Open-Meteo/SMOC currents already include it
                    w = 2*math.pi/max(e["tp"], 1.0)
                    us = 2*w**3*(e["hs"]/2)**2/(8*9.81)
                    wd = math.radians(e["wave_dir"] + 180)
                    ve += us*math.sin(wd); vn += us*math.cos(wd)
            sog = math.hypot(ve, vn)
            dist = sog*dt
            if dist > 0:
                nlat, nlon = destination(st["lat"], st["lon"], math.degrees(math.atan2(ve, vn)), dist)
            else:
                nlat, nlon = st["lat"], st["lon"]
            st.update(stw=res["u"], sog=sog, heel=res["heel"])
            st["distance_km"] += dist/1000
            for wk, wl in self.watch.items():
                if abs(nlat - wl[0][0]) < 1.0 and abs(nlon - wl[0][1]) < 1.5:
                    kx = 111.2*math.cos(math.radians(nlat)); px, py = nlon*kx, nlat*111.2
                    for (a0, o0), (a1, o1) in zip(wl[:-1], wl[1:]):
                        x0, y0, x1, y1 = o0*kx, a0*111.2, o1*kx, a1*111.2
                        tt = max(0.0, min(1.0, ((px - x0)*(x1 - x0) + (py - y0)*(y1 - y0))/max((x1 - x0)**2 + (y1 - y0)**2, 1e-9)))
                        dd = math.hypot(px - x0 - tt*(x1 - x0), py - y0 - tt*(y1 - y0))
                        if dd < self.watch_min[wk]: self.watch_min[wk] = dd
            # land / arrival
            if self.land.is_land(nlat, nlon):
                isle = self.land.atlantic_island(nlat, nlon)
                if self.land.far_side(nlat, nlon, sc.get("atlantic_islands_count", False), sc.get("africa_landfall_counts", False),
                                      sc.get("far_side", "europe")) \
                        and sc.get("europe_landfall_counts", True):
                    st["lat"], st["lon"] = nlat, nlon
                    outcome = self._arrival_outcome(st)
                    st["landfall"] = [round(nlat, 2), round(nlon, 2)]
                    self.event(t, "arrival", f"Landfall across the Atlantic at {nlat:.2f}, {nlon:.2f}")
                else:
                    outcome = "aground"
                    self.event(t, "end", f"Landed on the {isle} (not counted as Europe in this scenario)" if isle
                               else f"Ran aground at {nlat:.2f}, {nlon:.2f}")
                    st["lat"], st["lon"] = nlat, nlon
                break
            st["lat"], st["lon"] = nlat, nlon
            if haversine_km(nlat, nlon, sc["target"]["lat"], sc["target"]["lon"]) < sc["arrival_radius_km"]:
                outcome = self._arrival_outcome(st)
                self.event(t, "arrival", f"Reached the target area at {nlat:.2f}, {nlon:.2f}"); break
            # ---- power
            if not st["box_dead"]:
                self.power_step(st, e, decision, res, dt, t)
            # ---- comms
            interval = 12.0 if self.ap.mode == "safe" else self.ap.report_h
            if t - st["last_report"] >= interval*3600:
                self.comms_session(st, e, t, pending)
            self.tracker_step(st, e, t)
            # ---- failures
            self.failure_step(st, e, envd, dt, t, L, Bm)
            if not st["alive"]:
                outcome = "lost"; break
            # ---- logging
            if t >= next_log:
                series.append(self.snapshot(t, st, e, envd, decision, res))
                next_log = t + log_every
            t += dt
            if self.progress and k % 200 == 0:
                self.progress(min((t - self.t0)/(t_end - self.t0), 1.0), st)
        if outcome is None:
            outcome = "at_sea_timeout"
            self.event(t, "end", f"Still at sea after {sc['max_days']} days" + (
                (" (adrift, backup tracker reporting)" if st["trk_ok"] else " (adrift, silent)") if st["box_dead"] else ""))
        try:
            e_last = self.env.sample(st["lat"], st["lon"], t)
        except BulkDataMissing:
            e_last = e
        series.append(self.snapshot(t, st, e_last, envd, decision, dict(u=st["stw"], v=0, heel=st["heel"], alpha=0, delta=0)))
        days = (t - self.t0)/86400
        months = max(days/30.44, 0.5)
        cost = st["credits"]*d["comms"]["credit_usd"] + months*d["comms"]["line_rental_usd_month"]
        return dict(
            outcome=outcome, days=round(days, 2), end=dict(lat=st["lat"], lon=st["lon"]),
            distance_km=round(st["distance_km"], 1), credits=st["credits"], airtime_usd=round(cost, 2),
            sessions_ok=st["sessions_ok"], sessions_failed=st["sessions_fail"],
            last_report_day=round((st["last_report_ok"] - self.t0)/86400, 2),
            last_fix_day=round((max(st["last_report_ok"], st["trk_last_ok"] or 0) - self.t0)/86400, 2),
            position_known_at_end=self._position_known(st, outcome),
            box_dead=st["box_dead"], tracker_fitted=bool((d.get("backup_tracker") or {}).get("fitted")),
            tracker_ok=st["trk_ok"], tracker_fixes=st["trk_fixes"],
            knockdowns=st["knockdowns"], capsizes=st["capsizes"], knockdowns_by_hs_m=st["kd_hs"],
            energy_in_wh=round(st["energy_in_wh"], 1), energy_out_wh=round(st["energy_out_wh"], 1),
            final_soc=round(st["soc"], 3), final_drag_factor=round(st["df"], 2), pumped_kg=round(st.get("pumped_kg", 0.0), 2),
            failures=[ev for ev in self.events if ev["kind"] == "failure"],
            events=self.events, series=series, wall_s=round(time.time() - wall0, 1),
            mode=sc["mode"], scenario=sc, design_name=d.get("name"),
            stats=self._stats(series),
            **({"watch_min_km": {k: (round(v, 2) if v < 1e8 else None) for k, v in self.watch_min.items()}} if self.watch else {}))

    # -------------------------------------------------------------- hybrid physics
    def hybrid_step(self, st, e, envd, dec, dt, t):
        P = self.polar
        twa_s = wrap180(envd["twd"] - st["heading"])            # + = wind on starboard side
        side = 1 if twa_s >= 0 else -1
        wing_ok = not st["wing_lost"]
        feather = dec["alpha_mode"] == "feather" or not wing_ok or st["brownout"] or st["tail"] == "feathered"
        df = st["df"] + (3.0 if st["entangled"] else 0) + st["water_kg"]/max(self.boat.mass, 1)*2
        df = min(df, 4.0)
        steer_possible = dec["steering"] and not st["brownout"] and st["rudder"] == "ok"
        if st["inverted"] or (st["box_dead"] and not st["limp_on"]) or (feather and not steer_possible):
            # Dead boat: leeway, i.e. drift through the water at a fixed share of the 10 m wind, close to downwind
            # (USCG/SAR leeway model; coefficients in design["drift"]). The VPP's feathered state assumes the
            # keel holds the boat on its heading, which made a dead boat reach across the wind at 4-6%.
            Dd = self.d.get("drift", {})
            if "cw_sign" not in st:
                st["cw_sign"] = 1 if self.rng.random() < 0.5 else -1
            dw = Dd.get("leeway_downwind", 0.033)*envd["tws"]
            cw = Dd.get("leeway_crosswind", 0.008)*envd["tws"]*st["cw_sign"]
            downwind = (envd["twd"] + 180) % 360
            st["heading"] = (downwind + math.degrees(math.atan2(cw, max(dw, 1e-6)))) % 360
            return dict(u=math.hypot(dw, cw), v=0.0, heel=180.0 if st["inverted"] else 0.0, alpha=0.0, delta=0.0,
                        ground_included=False)
        keys = ("u_f", "v_f", "phi_f", "delta_f") if feather else ("u", "v", "phi", "delta", "alpha")
        # The polar's wind-angle axis is RADIANS. Until 12 Nov 2026 this passed degrees, which the polar clipped to 180 deg:
        # every heading sailed at the dead-downwind speed (docs/Simulator_Angle_Bug.md).
        r = P(envd["tws"], math.radians(abs(twa_s)), envd["hs"], df, keys)
        if feather:
            u, v, phi, dl, al = r["u_f"], r["v_f"], r["phi_f"], r["delta_f"], 0.0
        else:
            u, v, phi, dl, al = r["u"], r["v"], r["phi"], r["delta"], r["alpha"]
        pf = (self.d.get("performance") or {}).get("speed_factor", 1.0)   # study key: the whole polar faster or slower (the VPP is unvalidated until Field Test A)
        if pf != 1.0:
            u *= pf
        if st["limp_on"] and not feather:
            u *= (self.d.get("limp_home") or {}).get("speed_factor", 0.85)   # limp-home: fixed wing angle, simple steering
        if st["tail"] == "stuck" and wing_ok:
            al = st["tail_stuck_alpha"]
            u *= max(0.2, 1 - abs(al - r.get("alpha", al))/0.3)
        v *= side; dl *= side
        # heading dynamics
        steer_ok = dec["steering"] and not st["brownout"] and st["rudder"] == "ok" and not st["hung_steer"] if "hung_steer" in st else \
            dec["steering"] and not st["brownout"] and st["rudder"] == "ok"
        dmax = math.radians(self.d["rudder"]["max_angle_deg"])
        if steer_ok and abs(dl) <= dmax*1.05:
            # tack/gybe through the wind takes time; heading converges at up to 3 deg/s
            err = wrap180(dec["heading"] - st["heading"])
            st["heading"] = (st["heading"] + max(-180*dt/60, min(180*dt/60, err))) % 360
        else:
            # no steering: weathervane toward a natural drift angle (~110 deg TWA), or follow a stuck rudder
            target_twa = 110.0 if st["rudder"] != "stuck" else 60.0 + 70.0*(st["rudder_stuck"] + 1)/2
            want = (envd["twd"] - side*target_twa) % 360
            err = wrap180(want - st["heading"])
            st["heading"] = (st["heading"] + err*(1 - math.exp(-dt/900))) % 360
        # thruster
        if dec.get("thruster") and not st["brownout"]:
            ut = (self.d["power"]["thruster_n"]/(0.5*1025*self.prep["vpp"].s_hull*0.006))**0.5
            u = max(u, min(ut, 1.2)); st["thrust_h_today"] += dt/3600; st["thruster_on"] = True
        else:
            st["thruster_on"] = False
        return dict(u=u, v=v, heel=math.degrees(phi), alpha=math.degrees(al), delta=math.degrees(dl),
                    ground_included=False)

    # -------------------------------------------------------------- power
    def solar_derate(self, e):
        """Panel-to-battery losses: salt and soiling, MPPT, wiring, and hot cells.
        Cell temperature from the NOCT model, T_cell = T_air + (NOCT - 20) x G / 800."""
        P = self.d["power"]
        t_cell = e["air_t"] + (P.get("noct_c", 45.0) - 20.0)*max(e["sw_rad"], 0.0)/800.0
        temp = max(0.0, 1.0 + P.get("temp_coeff_per_c", 0.0)*(t_cell - 25.0))
        return P.get("soiling_salt", 0.9)*P.get("mppt_eff", 1.0)*P.get("wiring_eff", 1.0)*temp

    def power_step(self, st, e, dec, res, dt, t):
        P = self.d["power"]
        cap = P["battery_wh"]
        heel = math.radians(min(abs(res["heel"]), 90))
        sun = 0.0 if (st["inverted"] or st["knocked"]) else e["sw_rad"]*P["panel_area_m2"]*P["panel_eff"]*math.cos(heel)
        sun = min(sun, P["solar_peak_w"])*self.solar_derate(e)
        if e["sst"] + 1.0 < P["cold_charge_cutoff_c"]:
            sun = 0.0
        load = P["sleep_w"]
        if not st["brownout"]:
            if dec["steering"] and self.ap.mode not in ("safe", "drift"):
                load += P["autopilot_w"]
                load += P["servo_j_per_deg"]*(150 + 120*e["hs"])/3600           # rudder corrections (deg per hour)
            load += P["servo_j_per_deg"]*(30 + 30*e["hs"])/3600                  # tail
            if st.get("thruster_on"): load += P["thruster_w"]
        if st.get("pump_wh", 0.0) > 0:                                             # bilge pump energy since the last step
            load += st["pump_wh"]*3600/dt; st["pump_wh"] = 0.0
        dE = (sun - load)*dt/3600
        st["energy_in_wh"] += sun*dt/3600; st["energy_out_wh"] += load*dt/3600
        st["soc"] = min(1.0, max(0.0, st["soc"] + dE/cap))
        st["solar_w"], st["load_w"] = sun, load
        if st["soc"] <= P["battery_min_soc"] and not st["brownout"]:
            st["brownout"] = True; self.event(t, "power", "Battery flat: brown-out, drifting")
        elif st["brownout"] and st["soc"] > 0.15:
            st["brownout"] = False; self.event(t, "power", "Recovered from brown-out")

    # -------------------------------------------------------------- comms
    def comms_session(self, st, e, t, pending):
        P = self.d["power"]; C = self.d["comms"]
        st["last_report"] = t
        if st["brownout"] or st["comms_dead"] or st["box_dead"]:
            return
        if st["hung"]:
            st["sessions_fail"] += 1; return
        p_ok = 0.97 - 0.03*min(e["hs"], 8)
        if st["inverted"] or st["knocked"]: p_ok = 0.0
        tries = 0; ok = False
        while tries < 3 and not ok:
            tries += 1
            ok = self.rng.random() < p_ok
            st["soc"] -= (P["modem_session_j"] if ok else P["modem_failed_session_j"])/3600/P["battery_wh"]
        if not ok:
            st["sessions_fail"] += 1; return
        st["sessions_ok"] += 1; st["last_report_ok"] = t
        credits = math.ceil(C["report_bytes"]/50)
        if self.ap.diag_requested:
            credits += 4; self.ap.diag_requested = False
        while pending:
            c = pending.pop(0)
            credits += max(1, math.ceil(len(json.dumps(c.get("args", {})))/50))
            if c["cmd"].upper() == "REBOOT":
                st["hung"] = False
            self.ap.apply_command(c["cmd"], c.get("args", {}), t, st)
        st["credits"] += credits

    # -------------------------------------------------------------- backup tracker
    def tracker_step(self, st, e, t):
        """Independent YB3: own battery, GPS and Iridium modem. Fixes every 3 h for the first week, then every 12 h."""
        if not st["trk_ok"] or t < st["trk_next"]:
            return
        BT = self.d.get("backup_tracker") or {}
        week1 = (t - self.t0) < 7*86400
        st["trk_next"] = t + 3600*(BT.get("first_week_interval_h", 3.0) if week1 else BT.get("report_interval_h", 12.0))
        st["trk_sent"] += 1
        if not st["inverted"] and self.rng.random() < BT.get("p_report_ok", 0.95):
            st["trk_fixes"] += 1; st["trk_last_ok"] = t
        if st["trk_sent"] >= st["trk_budget"]:
            st["trk_ok"] = False; self.event(t, "failure", "Backup tracker battery flat")

    @staticmethod
    def _arrival_outcome(st):
        if st["box_dead"] and not st.get("limp_on"):
            return "arrived_adrift"                       # washed up with the main box dead: not a sailed crossing
        if st["box_dead"]:                                # sailed in under the limp-home controller (12 Nov 2026 fix)
            return "arrived_tracked" if st["trk_ok"] else "arrived_silent"
        if not (st["comms_dead"] or st["hung"]):
            return "arrived_reporting"
        return "arrived_tracked" if st["trk_ok"] else "arrived_silent"

    @staticmethod
    def _position_known(st, outcome):
        if outcome == "lost":
            return False
        main = not (st["comms_dead"] or st["hung"] or st["box_dead"])
        return bool(main or st["trk_ok"])

    # -------------------------------------------------------------- failures
    def failure_step(self, st, e, envd, dt, t, L, B):
        rnd = self.rng.random
        hs = e["hs"]
        dland = None
        def near(km):
            nonlocal dland
            if dland is None:
                dland = self.land.dist_to_land_km(st["lat"], st["lon"], max_km=220) if (self.rng.random() < 0.05 or not hasattr(self, "_dl")) else self._dl
                self._dl = dland
            return dland < km
        # fouling (continuous)
        if self.rate("fouling_growth") > 0:
            st["df"] = min(st["df"] + self.rate("fouling_growth")*max(e["sst"], 0)/20*dt/86400, 3.0)
        el = (early_life_factor(self.fr, (t - self.t0)/86400)*wear_out_factor(self.fr, (t - self.t0)/86400)) if self.fail_on else 1.0
        # leak
        if st["leak_rate"] == 0 and rnd() < p_event(self.rate("leak")*el*(1 + (hs/3)**2), dt):
            sev = rnd(); st["leak_rate"] = 0.05 + 2.5*sev**2
            self.event(t, "failure", f"Leak started ({st['leak_rate']:.2f} kg/day of water)")
        if st["leak_rate"] > 0:
            st["water_kg"] += st["leak_rate"]*dt/86400
            lim = self.d["hull"].get("flood_limit_kg")          # Rev C: foam-filled hull, only the free space can flood
            if lim is not None:
                st["water_kg"] = min(st["water_kg"], lim)
            pump = self.d.get("bilge_pump") or {}
            if pump.get("fitted") and not st.get("pump_dead"):
                if rnd() < p_event(pump.get("fail_per_day", 0.0)*el, dt):
                    st["pump_dead"] = True; self.event(t, "failure", "Bilge pump failed")
                elif st["water_kg"] > 0.02:                    # pumps the sump down to the pickup level
                    out = min(st["water_kg"] - 0.02, pump["kg_per_day"]*dt/86400)
                    if not st.get("pumped_kg"):
                        self.event(t, "alarm", "Leak: bilge pump running, sailing on")
                    st["water_kg"] -= out; st["pumped_kg"] = st.get("pumped_kg", 0.0) + out
                    st["pump_wh"] = st.get("pump_wh", 0.0) + pump.get("power_w", 4.0)*(out/pump["kg_per_day"]*24)
            policy = self.d["autopilot"].get("leak_policy", "safe")
            if st["water_kg"] > 0.1 and not st["leak_alarm"]:
                st["leak_alarm"] = True
                if policy == "safe":                            # Rev B-D: stop and wait (the boat never leaves SAFE)
                    self.ap.mode = "safe"; self.event(t, "alarm", "Leak sensor wet -> SAFE mode")
                else:
                    self.event(t, "alarm", "Leak sensor wet: pumping, sailing on")
            if policy != "safe":                                # pump_and_sail: stop only if the pump is losing
                thr = self.d["autopilot"].get("leak_safe_kg", 1.5)
                if st["water_kg"] > thr and not st.get("flooding"):
                    st["flooding"] = True; self.ap.mode = "safe"; self.event(t, "alarm", f"Water over {thr:.1f} kg -> SAFE mode")
                elif st.get("flooding") and st["water_kg"] < 0.5*thr:
                    st["flooding"] = False; self.event(t, "recovery", "Water pumped down: sailing on")
            if st["water_kg"] > 0.35*self.boat.mass:
                st["alive"] = False; self.event(t, "failure", "Swamped by leaking water: boat lost"); return
        # backup tracker (independent box)
        if st["trk_ok"] and rnd() < p_event(self.rate("backup_tracker"), dt):
            st["trk_ok"] = False; self.event(t, "failure", "Backup tracker failed")
        # limp-home controller (Rev D study, docs/Electronics_Review.md): its own sealed, potted board, used only
        # after the main box dies. It fails at its own rate, scaled by the same early-life and wetness factors.
        if st["limp_on"]:
            LH = self.d.get("limp_home") or {}
            wet = 1 + (self.d["hull"].get("wet_electronics_factor", 6.0) - 1)*(st["water_kg"] > 0.3)
            if rnd() < p_event(self.rate("electronics")*LH.get("rate_factor", 0.5)*el*wet, dt):
                st["limp_on"] = False; st["limp_ok"] = False
                self.event(t, "failure", "Limp-home controller failed: boat drifting")
        # once the main box is dead only the hull, the rig and the outside world can still change things
        active = not st["box_dead"]
        # electronics
        if active and rnd() < p_event(self.rate("electronics")*el*(1 + (self.d["hull"].get("wet_electronics_factor", 6.0) - 1)*(st["water_kg"] > 0.3)), dt):
            if st["limp_ok"]:
                st["box_dead"] = True; st["brownout"] = False; st["limp_on"] = True
                self.event(t, "failure", "Electronics failure (corrosion/humidity): main box dead; limp-home controller sailing on"
                           + ("; backup tracker reporting" if st["trk_ok"] else ", silent"))
                return
            if st["trk_ok"]:
                st["box_dead"] = True; st["brownout"] = False
                self.event(t, "failure", "Electronics failure (corrosion/humidity): main box dead, boat drifting; backup tracker still reporting")
            else:
                st["alive"] = False; self.event(t, "failure", "Electronics failure (corrosion/humidity): boat silent and uncontrolled")
            return
        # satellite modem, antenna or comms power path: the boat keeps sailing but goes quiet for good
        if active and not st["comms_dead"] and rnd() < p_event(self.rate("comms_silent")*el*(1 + hs/4), dt):
            st["comms_dead"] = True; self.event(t, "failure", "Satellite modem or antenna failed: boat sails on but is silent")
        # steering
        # steering. Each rudder has its own servo (Rev C has two): the boat keeps steering until the last one fails.
        # Design-level factors (docs/Reliability_Review.md): servo_rate_factor scales the scenario's servo rates for a
        # better actuator (GUESS until a bench life test); tail_fail_free_share is the share of tail failures that
        # leave the tail free (wing feathers, boat drifts) rather than jammed at an angle (0.5 as drawn).
        rsf = self.d["rudder"].get("servo_rate_factor", 1.0); tsf = self.d["wing"].get("tail_servo_rate_factor", 1.0)
        free_share = self.d["wing"].get("tail_fail_free_share", 0.5)
        if active and st["rudder"] == "ok" and st["rudders_ok"] > 1:
            if rnd() < p_event(self.rate("rudder_servo")*rsf*el*(1 + hs/4)*st["rudders_ok"], dt):
                st["rudders_ok"] -= 1
                how = "jammed" if rnd() < 0.6 else "failed limp"
                self.event(t, "failure", f"One rudder servo {how}: the other rudder still steers")
        elif active and st["rudder"] == "ok" and rnd() < p_event(self.rate("rudder_servo")*rsf*el*(1 + hs/4), dt):
            if rnd() < 0.6:
                st["rudder"] = "stuck"; st["rudder_stuck"] = rnd()*2 - 1
                self.event(t, "failure", f"Rudder servo jammed at {st['rudder_stuck']*self.d['rudder']['max_angle_deg']:.0f} deg")
            else:
                st["rudder"] = "limp"; self.event(t, "failure", "Rudder servo failed limp: no steering")
        if active and st["tail"] == "ok" and rnd() < p_event(self.rate("tail_servo")*tsf*el*(1 + hs/4), dt):
            if rnd() < 1.0 - free_share:              # same draw as before when free_share is 0.5
                st["tail"] = "stuck"; st["tail_stuck_alpha"] = math.radians(rnd()*15)
                self.event(t, "failure", "Tail servo jammed: wing stuck at a fixed angle of attack")
            else:
                st["tail"] = "feathered"; self.event(t, "failure", "Tail servo failed: wing feathers, boat drifts")
        # entanglement
        # Geometry factors (docs/Reliability_Review.md): weed_catch_factor scales the catch rate, weed_clear_per_day
        # is how fast a fouled boat sheds it (0.15 as drawn, which assumes a vertical fin with a protruding bulb nose
        # clears in a week: a GUESS, probably kind).
        wk = self.d["keel"].get("weed_catch_factor", 1.0); wc = self.d["keel"].get("weed_clear_per_day", 0.15)
        if not st["entangled"]:
            m = 3 if near(100) else 1
            zones = self.sc.get("weed_zones")
            if zones is None:                                   # default: the Sargasso Sea doubles the rate
                if 20 <= st["lat"] <= 35 and -70 <= st["lon"] <= -40: m *= 2
            else:                                               # scenario zones (east-west study: the Sargassum belt)
                for z in zones:
                    if z["lat"][0] <= st["lat"] <= z["lat"][1] and z["lon"][0] <= st["lon"] <= z["lon"][1]:
                        f = z.get("factor", 1.0)
                        if "factor_by_month" in z:
                            f = z["factor_by_month"].get(str(from_epoch(t).month), f)
                        m *= f
            if rnd() < p_event(self.rate("entanglement")*wk*m, dt):
                st["entangled"] = True; self.event(t, "failure", "Fouled by weed or fishing line (drag x4)")
        elif rnd() < p_event(wc, dt):
            st["entangled"] = False; self.event(t, "recovery", "Fouling cleared")
        # collision / capture
        if rnd() < p_event(self.rate("collision")*(8 if near(100) else 1), dt):
            if rnd() < 0.6:
                st["alive"] = False; self.event(t, "failure", "Struck by a vessel: boat lost"); return
            st["leak_rate"] = max(st["leak_rate"], 0.5); self.event(t, "failure", "Collision damage: hull leaking")
        if near(self.fr["capture"].get("capture_km", 50)) and rnd() < p_event(self.rate("capture"), dt):
            st["alive"] = False; self.event(t, "failure", "Picked up by a fishing boat or passer-by"); return
        # software hang
        if active and not st["hung"] and rnd() < p_event(self.rate("software_hang"), dt):
            if rnd() < 0.95:
                self.event(t, "recovery", "Software hang cleared by watchdog")
            else:
                st["hung"] = True; self.event(t, "failure", "Companion computer hung: no reports (autopilot keeps sailing)")
        if st["hung"]:
            sil = self.sc.get("operator", {}).get("auto_reboot_after_silence_h")
            # a hung ESP32 cannot receive a REBOOT command (it drives the modem); only a power cycle clears it
            if st["brownout"]:
                st["hung"] = False; self.event(t, "recovery", "Power cycle cleared the software hang")
        # waves: knockdowns and capsize
        if self.rate("wave_capsize") > 0 and not st["inverted"]:
            u10 = envd["tws"]
            lam = breaking_knockdown_rate(hs, e["tp"], u10, L, B)*self.rate("wave_capsize")
            if rnd() < p_event(lam, dt):
                st["knockdowns"] += 1; st["kd_hs"][min(int(hs), 9)] += 1   # knockdowns by Hs, 1 m bins (9 = 9 m+)
                S = self.struct if self.fail_on else None
                kb = min(int(hs), 9)
                if S:                                              # what the strike breaks (docs/Structural_Review.md)
                    if rnd() < S["keel"][kb]:
                        st["alive"] = False
                        self.event(t, "failure", f"Keel fin or its joint broke in a knockdown (Hs {hs:.1f} m): capsized, boat lost"); return
                    if not st["post_bent"] and rnd() < S["post"][kb]:
                        st["post_bent"] = True; st["comms_dead"] = True
                        if S["tracker_on_post"] and st["trk_ok"]:
                            st["trk_ok"] = False
                            self.event(t, "failure", "Stern post bent in a knockdown: main antenna and backup tracker both lost")
                        else:
                            self.event(t, "failure", "Stern post bent in a knockdown: main antenna lost, boat sails on silent")
                    if not st["wing_lost"] and rnd() < S["arm"][kb]:
                        st["wing_lost"] = True; self.event(t, "failure", "Counterweight arm broke in a knockdown: wing unbalanced, drifting")
                    if st["tail"] == "ok" and rnd() < S["boom"][kb]:
                        st["tail"] = "feathered"; self.event(t, "failure", "Tail boom broke in a knockdown: wing feathers, boat drifts")
                    for _ in range(max(int(st["rudders_ok"]), 1)):
                        if st["rudder"] == "ok" and rnd() < S["rudder"][kb]:
                            if st["rudders_ok"] > 1:
                                st["rudders_ok"] -= 1
                                self.event(t, "failure", "One rudder servo stripped by a wave strike: the other rudder still steers")
                            else:
                                st["rudder"] = "limp"; self.event(t, "failure", "Rudder servo stripped by a wave strike: no steering")
                if self.backend is not None and not st["box_dead"]:   # 6-DOF: hit the boat with a breaking crest, physics decides
                    self.backend.kick(side=1.0 if rnd() < 0.5 else -1.0, mag=3.0 + 2.0*rnd())
                    self.event(t, "knockdown", f"Breaking wave strike (Hs {hs:.1f} m)")
                    return
                pinv = self.stab["p_stay_inverted"]
                if rnd() < pinv:
                    st["inverted"] = True; st["capsizes"] += 1
                    self.event(t, "failure", f"Capsized by a breaking wave (Hs {hs:.1f} m): boat inverted")
                else:
                    self.event(t, "knockdown", f"Knocked down by a breaking wave (Hs {hs:.1f} m); self-righted")
                if rnd() < self.rate("knockdown_damage")*(S["wing_factor"][kb] if S else 1.0):
                    st["wing_lost"] = True; self.event(t, "failure", "Wing damaged in a knockdown: drifting")
        elif st["inverted"] and (self.backend is None or st["box_dead"]):
            lam = breaking_knockdown_rate(hs, e["tp"], envd["tws"], L, B)*max(self.rate("wave_capsize"), 1) + 0.2
            pr = 1 - self.stab["p_stay_inverted"]
            if rnd() < p_event(lam*pr, dt):
                st["inverted"] = False; self.event(t, "recovery", "Righted by a wave")

    # -------------------------------------------------------------- logging
    def snapshot(self, t, st, e, envd, dec, res):
        return dict(t=round((t - self.t0)/3600, 3), lat=round(st["lat"], 5), lon=round(st["lon"], 5),
                    hdg=round(float(st["heading"]), 1), sog=round(float(st["sog"]), 3), stw=round(float(st["stw"]), 3),
                    tws=round(envd["tws"], 2), twd=round(envd["twd"], 1),
                    twa=round(wrap180(envd["twd"] - st["heading"]), 1), hs=round(e["hs"], 2), tp=round(e["tp"], 1),
                    cur=round(math.hypot(e["cur_u"], e["cur_v"]), 3), sst=round(e["sst"], 1),
                    heel=round(float(res.get("heel", 0)), 1), alpha=round(float(res.get("alpha", 0)), 1), rudder=round(float(res.get("delta", 0)), 1),
                    soc=round(st["soc"], 3), solar_w=round(st.get("solar_w", 0), 2), load_w=round(st.get("load_w", 0), 2),
                    mode=self.ap.mode, df=round(st["df"], 2), water=round(st["water_kg"], 2), credits=st["credits"],
                    sea_level=round(e.get("sea_level", 0), 2), inverted=st["inverted"])

    @staticmethod
    def _stats(series):
        if not series: return {}
        a = lambda k: np.array([s[k] for s in series], float)
        sog, tws, hs, soc = a("sog"), a("tws"), a("hs"), a("soc")
        return dict(mean_sog_kn=round(float(sog.mean())*1.944, 2), max_tws_ms=round(float(tws.max()), 1),
                    max_hs_m=round(float(hs.max()), 1), min_soc=round(float(soc.min()), 3),
                    mean_tws_ms=round(float(tws.mean()), 1))


def run_voyage(design, scenario, **kw):
    return Voyage(design, scenario, **kw).run()
