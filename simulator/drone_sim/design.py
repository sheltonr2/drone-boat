"""Boat design parameters (SI units: metres, kilograms, seconds, degrees where noted).

A design is a nested dict that round-trips to JSON. `default_design()` returns the Rev B
1.5 m drone from the drawing set. Coordinates follow the drawings: x aft from the bow,
y to port, z up from the hull bottom at midships.
"""
import copy, json, hashlib

DEFAULT = {
    "name": "Rev B 1.5 m solar-sail drone",
    "hull": {
        "length": 1.50, "beam": 0.40, "depth": 0.23,
        "max_beam_at": 0.55,            # fraction of length
        "transom_beam": 0.30,
        "bow_rocker": 0.12, "stern_rocker": 0.06, "bow_sheer": 0.03,
        "section_exponent": 2.2,        # 2 = round bilge, larger = boxier
        "laminate_kg_m2": 1.6,          # foam core + glass + resin, hull and deck
        "stl": None,                    # optional uploaded mesh: {"path":..., "role": "hull"|"full", "units": "mm"|"m"}
    },
    "keel": {
        "x_le_root": 0.657, "span": 0.43, "root_chord": 0.17, "tip_chord": 0.15,
        "sweep_deg": 1.7,               # leading-edge sweep back
        "rake_deg": 0.0,                # whole fin rotated aft (positive) about the root LE
        "cant_deg": 0.0,                # fixed cant to port (positive), for experiments
        "thickness": 0.12,              # t/c
        "kg_per_m2_skin": 1.2, "core_density": 35.0, "rod_kg": 0.65,
    },
    "bulb": {
        "length": 0.32, "diameter": 0.068, "max_at": 0.40,
        "nose_from_tip_le": -0.091,     # bulb nose position relative to fin tip LE (m, + aft)
        "density": 11340.0,             # lead
    },
    "rudder": {
        "stock_x": 1.40, "chord": 0.12, "span": 0.23, "stock_from_le": 0.022,
        "top_z": 0.04, "thickness": 0.12, "max_angle_deg": 35.0, "rate_deg_s": 60.0,
        "kg_per_m2_skin": 1.0, "stock_kg": 0.37,
    },
    "wing": {
        "mast_x": 0.60, "span": 1.00, "chord": 0.30, "thickness": 0.15,
        "pivot_from_le": 0.066, "root_z": 0.30,
        "skin_kg_m2": 0.45, "core_density": 30.0, "spar_kg": 0.32,
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
        "electronics_box": [1.2, 1.10, 0.0, 0.10],
        "solar_panels": [1.0, 1.06, 0.0, 0.235],
        "mast_tube_and_housing": [0.45, 0.60, 0.0, 0.13],
        "rudder_servo_and_tube": [0.25, 1.36, 0.0, 0.14],
        "stern_stub_vane_antenna_reflector": [0.9, 1.53, 0.0, 0.42],
        "keel_box_and_backing": [0.5, 0.745, 0.0, 0.02],
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


def default_design():
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
    with open(path, "r", encoding="utf-8") as fh:
        return merge(DEFAULT, json.load(fh))


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
