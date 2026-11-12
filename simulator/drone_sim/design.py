"""Boat design parameters (SI units: metres, kilograms, seconds, degrees where noted).

A design is a nested dict that round-trips to JSON. `default_design()` returns the Rev C
1.5 m drone from the drawing set (10 Nov 2026); `default_design("revB")` returns Rev B. Coordinates follow the drawings: x aft from the bow,
y to port, z up from the hull bottom at midships.
"""
import copy, json, hashlib

DEFAULT = {
    "name": "Rev C 1.5 m solar-sail drone",
    "revision": "C", "revision_note": "C5: wing 0.80 x 0.375 m (same area), 11 Nov 2026; C4: acetal mast bearings; C3: structural review changes (YB3 to the foredeck, fibreglass post and counterweight arm, servo-savers, 30 x 22 spar), 11 Nov 2026; C2: hardwood keel fin; C1: electronics box above the flood level",
    # Structural failures in knockdowns, from the strike simulation (docs/Structural_Review.md, drone_sim/structure_tables.json).
    # parts: which set of parts (C2 = before the review, C3 = with its changes). breakers: "measured" (strikes matched to
    # drifting-buoy accelerations, docs/Research_Review.md; the default), or the older "gentle" / "central" slam-model sets. None = off.
    "structure": {"parts": "C3", "breakers": "measured", "tracker_on_post": False, "wing_shape_factor": 0.25},
    "hull": {
        "length": 1.50, "beam": 0.40, "depth": 0.23,
        "max_beam_at": 0.55,            # fraction of length
        "transom_beam": 0.30,
        "bow_rocker": 0.12, "stern_rocker": 0.06, "bow_sheer": 0.03,
        "section_exponent": 2.2,        # 2 = round bilge, larger = boxier
        "laminate_kg_m2": 1.6,          # foam core + glass + resin, hull and deck
        "stl": None,                    # optional uploaded mesh: {"path":..., "role": "hull"|"full", "units": "mm"|"m"}
        # Rev C: hull foam-filled (XPS blocks) behind two glassed-in bulkheads (x 0.30, 1.26), battery in its own sealed
        # box. A leak can only fill the free space left in the dry bay, so it can no longer swamp the boat.
        "flood_limit_kg": 3.0,
        # Rev C1 (11 Nov 2026): electronics box on a shelf 70 mm above the sump, glands on top. Water in the bay multiplies
        # the electronics hazard by this (Rev B and Rev C: 6). 2 is a GUESS until Field Test J (wet-bay soak) is done.
        "wet_electronics_factor": 2.0,
    },
    "keel": {
        "x_le_root": 0.657, "span": 0.43, "root_chord": 0.17, "tip_chord": 0.15,
        "sweep_deg": 1.7,               # leading-edge sweep back
        "rake_deg": 0.0,                # whole fin rotated aft (positive) about the root LE
        "cant_deg": 0.0,                # fixed cant to port (positive), for experiments
        "thickness": 0.12,              # t/c
        # Rev C2 (11 Nov 2026): hardwood core (680 kg/m3), 6 x 6 oz glass and a 60 x 1.5 mm carbon strip each side
        # (was XPS core 35 kg/m3 and 3 x 6 oz, 1.2 kg/m2). docs/Keel_Structure_Loads.md
        "kg_per_m2_skin": 3.2, "core_density": 680.0, "rod_kg": 0.65,
    },
    "bulb": {
        "length": 0.32, "diameter": 0.072, "max_at": 0.40,   # Rev C: D72 (was D68), ~9.2 kg
        "nose_from_tip_le": -0.091,     # bulb nose position relative to fin tip LE (m, + aft)
        "density": 11340.0,             # lead
    },
    "rudder": {
        "stock_x": 1.40, "chord": 0.12, "span": 0.23, "stock_from_le": 0.022,
        "y_offsets": [-0.10, 0.10],     # Rev C: twin rudders, each with its own servo and trunk ([0.0] = one, Rev B)
        "top_z": 0.072, "thickness": 0.12, "max_angle_deg": 35.0, "rate_deg_s": 60.0,   # top at the hull surface at y 100
        "kg_per_m2_skin": 1.0, "stock_kg": 0.37,
    },
    "wing": {
        "mast_x": 0.60, "span": 0.80, "chord": 0.375, "thickness": 0.15,   # Rev C5: shorter, wider wing, same 0.30 m2 (was 1.00 x 0.30): docs/Wing_Shape_Study.md
        "pivot_from_le": 0.082, "root_z": 0.30,
        "skin_kg_m2": 0.45, "core_density": 30.0, "spar_kg": 0.67,    # Rev C5: 30 x 22 carbon spar, 995 long (C3: 1195 long, 0.80; Rev C: 30 x 26, 0.43; Rev B: 25 x 22, 0.32)
        "buoyant": True,                # sealed foam core (True) or free-flooding (False)
        "balanced": True,               # counterweight puts the rig CG on the pivot axis
        "counterweight_arm": 0.30,      # m forward of the pivot (0.036 = nose pocket only)
        "bearing_friction_nm": 0.02,
    },
    "tail": {
        "chord": 0.12, "span": 0.20, "boom_length": 0.60, "boom_z": 0.276, "bot_z": 0.30,
        "pivot_from_le": 0.024, "thickness": 0.12, "max_angle_deg": 20.0, "kg": 0.25,
    },
    "equipment": {   # point masses: [kg, x, y, z]
        "battery": [2.0, 0.87, 0.0, 0.10],
        "electronics_box": [1.1, 1.10, 0.0, 0.163],         # Rev C: no backup D-cell. C1: raised onto a shelf (was z 0.10)
        "electronics_shelf": [0.08, 1.10, 0.0, 0.115],      # Rev C1: glassed foam shelf
        "solar_panels": [1.0, 1.06, 0.0, 0.235],
        "mast_tube_and_housing": [0.52, 0.60, 0.0, 0.13],       # Rev C3: longer bearing housing (was 0.45)
        "rudder_servos_and_trunks": [0.53, 1.36, 0.0, 0.14],   # Rev C: two of each
        "foam_fill_xps": [1.65, 0.80, 0.0, 0.13],           # Rev C: ~59 L of XPS at 28 kg/m3
        "bulkheads": [0.20, 0.78, 0.0, 0.12],               # Rev C: x 0.30 and 1.26, 10 mm foam + glass
        "battery_box": [0.35, 0.87, 0.0, 0.10],             # Rev C: sealed box with O-ring lid
        "yb3_tracker_and_platform": [0.45, 0.18, 0.0, 0.225],  # Rev C3: in a well in the foredeck (was on the stern post, x 1.53, z 0.48); +0.05 for the well's glass  # Rev C: P19 on the stern stub
        "nav_light": [0.06, 1.53, 0.0, 0.60],               # Rev C: all-round white LED on P20
        "stern_stub_vane_antenna_reflector": [0.9, 1.53, 0.0, 0.42],
        "keel_box_and_backing": [0.75, 0.745, 0.0, 0.02],      # Rev C2: + fin tenon, two floors and a hull doubler (was 0.5)
        "misc_fittings": [0.6, 0.80, 0.0, 0.12],
    },
    "power": {
        "solar_peak_w": 40.0, "panel_area_m2": 0.235, "panel_eff": 0.17,
        "battery_wh": 192.0, "battery_min_soc": 0.05,
        "sleep_w": 0.25, "autopilot_w": 1.1,        # autopilot active (Pixhawk + GPS + ESP32 awake)
        "servo_j_per_deg": 0.04, "modem_session_j": 6.0, "modem_failed_session_j": 10.0,
        "thruster_w": 35.0, "thruster_n": 6.0,
        "cold_charge_cutoff_c": 2.0,
        # Solar losses (idea from jcolter11374/boat-sim vessel/power.py). GUESS = not yet measured.
        "soiling_salt": 0.93,          # GUESS: salt film between rain showers
        "mppt_eff": 0.95,              # GUESS: Genasun GV-5 at part load
        "wiring_eff": 0.98,            # GUESS
        "temp_coeff_per_c": -0.0037,   # GUESS: typical monocrystalline cell
        "noct_c": 55.0,                # GUESS: semi-flexible panel bonded flat to the deck runs hot
    },
    "comms": {"report_interval_h": 4.0, "report_bytes": 45, "credit_usd": 0.12,
              "line_rental_usd_month": 17.0},
    "drift": {                          # a dead boat (no steering, wing feathered or lost, or upside down)
        "leeway_downwind": 0.033,       # x U10. Windage balance: Cd*A air ~0.20 m2 vs water ~0.22 m2 -> 3.3%.
                                        # Measured: Sunfish without sail 2.1%, 4.15 m skiff 4.0% (Breivik et al. 2010)
        "leeway_crosswind": 0.008,      # x U10, side picked at random per voyage (~14 deg divergence)
    },
    # Limp-home controller (proposed, not drawn; docs/Electronics_Review.md). A separate potted board (ESP32 class) with
    # its own GPS and compass that takes over steering and the tail when the main box dies. Off unless a design sets it.
    "limp_home": {"fitted": False, "speed_factor": 0.85, "rate_factor": 0.5},
    "backup_tracker": {                 # independent YB3 (Iridium SBD), docs/Backup_Tracker.md. Own battery, GPS, modem, antenna.
        "fitted": True,
        "report_interval_h": 12.0,      # every 12 h after the first week
        "first_week_interval_h": 3.0,
        "transmissions": 2500,          # rated per charge
        "cold_derate": 0.6,             # plan on 60% of the rating
        "p_report_ok": 0.95,            # per scheduled fix (sky view, sea state); none while inverted
    },
    "autopilot": {
        "heel_limit_deg": 25.0, "storm_tws_ms": 20.0, "reef_tws_ms": 13.0,
        "tack_hysteresis_deg": 20.0, "decision_interval_min": 10.0,
        "min_upwind_twa_deg": 50.0, "min_downwind_twa_deg": 165.0,
        "land_clearance_km": 15.0,
        "thruster_policy": {"enabled": False, "min_soc": 0.70, "max_speed_ms": 0.25, "max_hours_per_day": 2.0},
        "safe_soc": 0.25,
    },
    "hydro": {"form_factor": 1.15, "wave_resistance_scale": 1.0, "added_resistance_scale": 1.0,
              "hull_lateral_cd": 0.8},
    "cost": {
        "electronics_and_power_usd": 1172.0, "hardware_usd": 440.0,
        "hull_materials_usd_per_m2": 105.0, "foil_materials_usd_per_m2": 60.0,
        "lead_usd_per_kg": 7.0, "wing_materials_usd_per_m2": 55.0,
        "printing_and_misc_usd": 150.0, "thruster_usd": 270.0,
    },
}


# Rev B (8 Nov 2026), kept so older results can be reproduced and compared.
REV_B_CHANGES = {
    "name": "Rev B 1.5 m solar-sail drone", "revision": "B",
    "hull": {"flood_limit_kg": None, "wet_electronics_factor": 6.0},
    "structure": None,
    "keel": {"kg_per_m2_skin": 1.2, "core_density": 35.0},
    "bulb": {"diameter": 0.068},
    "rudder": {"y_offsets": [0.0], "top_z": 0.04},
    "wing": {"spar_kg": 0.32, "span": 1.00, "chord": 0.30, "pivot_from_le": 0.066},
}
REV_B_DROP_EQUIPMENT = ("electronics_shelf", "rudder_servos_and_trunks", "foam_fill_xps", "bulkheads", "battery_box",
                        "yb3_tracker_and_platform", "nav_light")


def _rev_b():
    d = merge(DEFAULT, REV_B_CHANGES)
    for k in REV_B_DROP_EQUIPMENT:
        d["equipment"].pop(k, None)
    d["equipment"]["electronics_box"] = [1.2, 1.10, 0.0, 0.10]
    d["equipment"]["keel_box_and_backing"] = [0.5, 0.745, 0.0, 0.02]
    d["equipment"]["mast_tube_and_housing"] = [0.45, 0.60, 0.0, 0.13]
    d["structure"] = None
    d["equipment"]["rudder_servo_and_tube"] = [0.25, 1.36, 0.0, 0.14]
    return d


def default_design(name=None):
    if name and name.lower().replace(" ", "").replace("_", "") in ("revb", "b"):
        return _rev_b()
    return copy.deepcopy(DEFAULT)


def merge(base, over):
    """Deep-merge dict `over` into a copy of `base` (unknown keys are kept)."""
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load(path):
    """A saved design merged onto its own revision's defaults. Files saved before Rev C carry no
    "revision" key: they are Rev B designs, so they merge onto Rev B, not Rev C."""
    with open(path, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    base = DEFAULT if d.get("revision", "B") == "C" else _rev_b()
    if base is not DEFAULT:
        eq = d.get("equipment")
        if eq is not None:            # a full equipment list replaces the base list (no Rev C items sneak in)
            base = copy.deepcopy(base); base["equipment"] = {}
    out = merge(base, d)
    if "structure" not in d:          # files saved before Rev C3 have no structural-failure model: keep them as they were run
        out["structure"] = None
    elif isinstance(d["structure"], dict) and "wing_shape_factor" not in d["structure"]:
        out["structure"]["wing_shape_factor"] = 1.0      # files saved before Rev C5 have the 1.0 m wing
    return out


def save(design, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(design, fh, indent=2)


def design_hash(design):
    s = json.dumps(design, sort_keys=True, default=str)
    return hashlib.sha1(s.encode()).hexdigest()[:12]


# Slider metadata for the UI: path, label, min, max, step, unit
EDITABLE = [
    ("hull.length", "Hull length", 0.8, 3.0, 0.01, "m"),
    ("hull.beam", "Hull beam", 0.2, 0.9, 0.01, "m"),
    ("hull.depth", "Hull depth", 0.12, 0.5, 0.005, "m"),
    ("hull.max_beam_at", "Max beam position", 0.35, 0.75, 0.01, "of L"),
    ("hull.transom_beam", "Transom beam", 0.0, 0.8, 0.01, "m"),
    ("hull.bow_rocker", "Bow rocker", 0.0, 0.3, 0.005, "m"),
    ("hull.stern_rocker", "Stern rocker", 0.0, 0.2, 0.005, "m"),
    ("hull.section_exponent", "Section fullness", 1.6, 4.0, 0.1, ""),
    ("keel.x_le_root", "Keel position (root LE)", 0.3, 1.2, 0.005, "m"),
    ("keel.span", "Keel length (depth)", 0.15, 1.0, 0.01, "m"),
    ("keel.root_chord", "Keel root chord", 0.06, 0.4, 0.005, "m"),
    ("keel.tip_chord", "Keel tip chord", 0.04, 0.4, 0.005, "m"),
    ("keel.sweep_deg", "Keel sweep", -10, 45, 0.5, "deg"),
    ("keel.rake_deg", "Keel rake", -20, 30, 0.5, "deg"),
    ("keel.cant_deg", "Keel cant", -30, 30, 0.5, "deg"),
    ("keel.thickness", "Keel t/c", 0.06, 0.2, 0.005, ""),
    ("bulb.length", "Bulb length", 0.1, 0.6, 0.005, "m"),
    ("bulb.diameter", "Bulb diameter", 0.03, 0.15, 0.001, "m"),
    ("bulb.nose_from_tip_le", "Bulb fore/aft offset", -0.3, 0.1, 0.005, "m"),
    ("rudder.stock_x", "Rudder position", 0.9, 2.9, 0.005, "m"),
    ("rudder.chord", "Rudder chord", 0.05, 0.3, 0.005, "m"),
    ("rudder.span", "Rudder span", 0.08, 0.5, 0.005, "m"),
    ("rudder.max_angle_deg", "Rudder max angle", 10, 45, 1, "deg"),
    ("wing.mast_x", "Mast position", 0.2, 1.5, 0.005, "m"),
    ("wing.span", "Wing height", 0.3, 2.5, 0.01, "m"),
    ("wing.chord", "Wing chord", 0.1, 0.8, 0.005, "m"),
    ("wing.thickness", "Wing t/c", 0.06, 0.24, 0.005, ""),
    ("wing.pivot_from_le", "Wing pivot from LE", 0.0, 0.3, 0.002, "m"),
    ("wing.root_z", "Wing root height", 0.24, 0.6, 0.005, "m"),
    ("wing.counterweight_arm", "Counterweight arm", 0.03, 0.8, 0.005, "m"),
    ("tail.chord", "Tail chord", 0.05, 0.3, 0.005, "m"),
    ("tail.span", "Tail span", 0.08, 0.5, 0.005, "m"),
    ("tail.boom_length", "Tail boom length", 0.3, 1.2, 0.01, "m"),
    ("power.solar_peak_w", "Solar peak power", 5, 200, 1, "W"),
    ("power.panel_area_m2", "Solar panel area", 0.03, 1.2, 0.005, "m2"),
    ("power.battery_wh", "Battery capacity", 20, 1500, 5, "Wh"),
    ("power.soiling_salt", "Solar: salt and soiling factor", 0.6, 1.0, 0.01, ""),
    ("power.noct_c", "Solar: panel NOCT", 40, 70, 1, "C"),
    ("power.autopilot_w", "Autopilot power", 0.2, 5, 0.05, "W"),
    ("comms.report_interval_h", "Report interval", 0.5, 24, 0.5, "h"),
    ("autopilot.heel_limit_deg", "Heel limit", 10, 50, 1, "deg"),
    ("autopilot.storm_tws_ms", "Storm mode wind", 10, 35, 0.5, "m/s"),
]


def get_path(d, path):
    for k in path.split("."):
        d = d[k]
    return d


def set_path(d, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value
