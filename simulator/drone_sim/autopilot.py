"""Mission logic: routing, tacking/gybing, wing control policy, land/geofence avoidance,
modes and the command set from the build plan (SET_ROUTE, GOTO, MODE, SET_REPORT,
THRUSTER_POLICY, GEOFENCE, DIAG, REBOOT)."""
import math
from .env import bearing_deg, haversine_km, destination


def wrap180(a):
    return (a + 180.0) % 360.0 - 180.0


class Autopilot:
    MODES = ("sail", "sail+thrust", "station", "drift", "safe")

    def __init__(self, design, scenario, polar, land, log_event):
        self.d = design; ap = design["autopilot"]; self.ap = ap
        self.polar = polar; self.land = land; self.event = log_event
        tgt = scenario["target"]
        self.route = [tuple(w) for w in scenario.get("waypoints", [])] + [(tgt["lat"], tgt["lon"])]
        self.wp = 0
        self.mode = scenario.get("initial_mode", "sail")
        self.tack = None                 # +1 = wind over starboard side, -1 = port
        self.heading = None
        self.alpha_mode = "best"         # best | feather
        self.report_h = design["comms"]["report_interval_h"]
        tp = dict(ap["thruster_policy"]); self.thruster = tp
        self.geofences = []              # (lat, lon, radius_km)
        self.station = None
        self.last_decision = -1e18
        self._vmg_cache = {}
        self.diag_requested = False

    # ---------------- commands
    def apply_command(self, cmd, args, t, state):
        c = cmd.upper()
        if c == "SET_ROUTE":
            self.route = [tuple(p) for p in args.get("waypoints", [])] or self.route; self.wp = 0
        elif c == "GOTO":
            self.route = [(args["lat"], args["lon"])]; self.wp = 0; self.station = (args["lat"], args["lon"])
        elif c == "MODE":
            m = args.get("mode", "sail")
            if m in self.MODES:
                self.mode = m
                if m == "station" and self.station is None:
                    self.station = (state["lat"], state["lon"])
        elif c == "SET_REPORT":
            self.report_h = float(min(max(args.get("hours", 4), 0.5), 24))
        elif c == "THRUSTER_POLICY":
            self.thruster.update({k: v for k, v in args.items() if k in ("enabled", "min_soc", "max_hours_per_day", "max_speed_ms")})
        elif c == "GEOFENCE":
            if args.get("clear"): self.geofences = []
            else: self.geofences.append((args["lat"], args["lon"], args.get("radius_km", 50)))
        elif c == "DIAG":
            self.diag_requested = True
        elif c == "REBOOT":
            pass                          # handled by the simulator (clears a software hang)
        self.event(t, "command", f"Executed {c} {args}")
        self.last_decision = -1e18

    # ---------------- helpers
    def vmg_angles(self, tws, hs, df):
        key = (round(tws), round(hs), round(df, 1))
        if key not in self._vmg_cache:
            up, dn = self.polar.best_vmg_angles(max(tws, 1.0), hs, df)
            up = max(math.degrees(up), self.ap["min_upwind_twa_deg"])
            dn = min(math.degrees(dn), self.ap["min_downwind_twa_deg"])
            self._vmg_cache[key] = (up, dn)
        return self._vmg_cache[key]

    def blocked(self, lat, lon, hdg, km):
        if self.land.land_ahead(lat, lon, hdg, km, steps=4):
            return True
        for la, lo, r in self.geofences:
            for f in (0.25, 0.5, 0.75, 1.0):
                p = destination(lat, lon, hdg, km*1000*f)
                if haversine_km(p[0], p[1], la, lo) < r: return True
        return False

    # ---------------- main decision
    def decide(self, t, s, env):
        """s: state dict (lat, lon, heading, soc, ...); env: dict with tws, twd (from, deg), hs, df.
        Returns dict(heading, alpha_mode, thruster, steering)."""
        tws, twd = env["tws"], env["twd"]
        out = dict(heading=s["heading"], alpha_mode="best", thruster=False, steering=True)
        # power & safety overrides
        if s["soc"] < self.ap["safe_soc"] and self.mode != "safe":
            self.event(t, "mode", f"Battery {s['soc']*100:.0f}% -> SAFE mode (heave-to, 12 h reports)")
            self.prev_mode = self.mode; self.mode = "safe"
        if self.mode == "safe" and s["soc"] > self.ap["safe_soc"] + 0.2 and not s.get("leak_alarm"):
            self.mode = getattr(self, "prev_mode", "sail"); self.event(t, "mode", f"Battery recovered -> {self.mode}")
        if self.mode in ("safe", "drift"):
            out.update(alpha_mode="feather", steering=False, heading=s["heading"])
            return out
        # waypoint management
        while self.wp < len(self.route) - 1 and haversine_km(s["lat"], s["lon"], *self.route[self.wp]) < 25:
            self.event(t, "nav", f"Reached waypoint {self.wp + 1}"); self.wp += 1
        tgt = self.route[self.wp]
        if self.mode == "station" and self.station and haversine_km(s["lat"], s["lon"], *self.station) < 5:
            out.update(alpha_mode="feather", steering=True); return out
        if tws > self.ap["storm_tws_ms"]:
            # storm: feather and run off at ~140 deg TWA on the more favourable gybe
            hdg_a, hdg_b = (twd + 180 - 40) % 360, (twd + 180 + 40) % 360
            b = bearing_deg(s["lat"], s["lon"], *tgt)
            hdg = hdg_a if abs(wrap180(hdg_a - b)) < abs(wrap180(hdg_b - b)) else hdg_b
            out.update(heading=hdg, alpha_mode="feather")
            return out
        b = bearing_deg(s["lat"], s["lon"], *tgt)
        twa_direct = wrap180(twd - b)                # angle wind comes from relative to desired course
        up, dn = self.vmg_angles(tws, env["hs"], env["df"])
        hyst = self.ap["tack_hysteresis_deg"]
        def pick(angle):
            h_cur = None if self.tack is None else (twd - self.tack*angle) % 360
            h_p, h_s = (twd - angle) % 360, (twd + angle) % 360      # starboard tack, port tack
            g_p, g_s = math.cos(math.radians(wrap180(h_p - b))), math.cos(math.radians(wrap180(h_s - b)))
            best = 1 if g_p >= g_s else -1
            if self.tack is None:
                self.tack = best
            elif best != self.tack and abs(g_p - g_s) > math.sin(math.radians(hyst)):
                self.event(t, "nav", "Tack" if angle < 90 else "Gybe"); self.tack = best
            return (twd - self.tack*angle) % 360
        if abs(twa_direct) < up:
            hdg = pick(up)
        elif abs(twa_direct) > dn:
            hdg = pick(dn)
        else:
            hdg = b; self.tack = 1 if twa_direct > 0 else -1
        # land / geofence avoidance
        clear_km = self.ap["land_clearance_km"]
        if self.blocked(s["lat"], s["lon"], hdg, clear_km):
            found = False
            for off in range(15, 181, 15):
                for sgn in (1, -1):
                    h2 = (hdg + sgn*off) % 360
                    if abs(wrap180(twd - h2)) < up*0.9: continue
                    if not self.blocked(s["lat"], s["lon"], h2, clear_km):
                        hdg = h2; found = True; break
                if found: break
            if not found:
                out.update(alpha_mode="feather")
        out["heading"] = hdg
        # thruster
        tp = self.thruster
        if (tp.get("enabled") or self.mode == "sail+thrust") and s["soc"] > tp.get("min_soc", 0.7) \
                and s.get("stw", 0) < tp.get("max_speed_ms", 0.25) and s.get("thrust_h_today", 0) < tp.get("max_hours_per_day", 2):
            out["thruster"] = True
        return out
