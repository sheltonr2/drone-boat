"""Stochastic failure (hazard) model. Rates are events per day of open-ocean sailing; the code
adds multipliers for sea state, nearness to land and early life. Every rate can be edited or
switched off in the scenario.

Three rate sets (scenario key "failure_rate_set"; individual "failures" entries still override):
  planning   - default. Microtransat-class rates with credit taken only for mitigations that are
               in the build plan (potted IP68 box, backup comms power, watchdog, buoyant wing,
               antifouling), and a 14-day shakedown before launch.
  historical - fitted to the Microtransat record 2010-2023 (amateur and student boats, no shakedown).
               Use it as the pessimistic bracket.
  original   - the guesses used before 2026-11-08, kept so older results can be reproduced.
Sources, derivations and quality grades: docs/Failure_Rates.md and docs/data/hazard_analysis.py."""
import copy, math

_ORIGINAL = {
    "leak":            {"enabled": True, "per_day": 0.0025, "note": "x(1+(Hs/3)^2); severity random"},
    "rudder_servo":    {"enabled": True, "per_day": 0.0020, "note": "x(1+Hs/4); stuck or limp"},
    "tail_servo":      {"enabled": True, "per_day": 0.0020, "note": "x(1+Hs/4); stuck or feathered"},
    "fouling_growth":  {"enabled": True, "per_day": 0.004, "note": "drag factor added per day at 20 C SST"},
    "entanglement":    {"enabled": True, "per_day": 0.003, "note": "x3 within 100 km of land; x2 in the Sargasso"},
    "collision":       {"enabled": True, "per_day": 0.0004, "note": "x8 within 100 km of land; 60% fatal"},
    "capture":         {"enabled": True, "per_day": 0.002, "note": "only within capture_km of land", "capture_km": 50},
    "electronics":     {"enabled": True, "per_day": 0.0012, "note": "x6 once water is inside"},
    "comms_silent":    {"enabled": False, "per_day": 0.0, "note": "modem/antenna/power-path failure: boat sails on, silent"},
    "software_hang":   {"enabled": True, "per_day": 0.02, "note": "watchdog recovers 95%"},
    "backup_tracker":  {"enabled": True, "per_day": 0.0007,
                        "note": "the independent YB3 dies (only matters when design backup_tracker.fitted). Flat rate, no "
                                "early-life or sea-state factor: off-the-shelf unit, proven in the shakedown. boat-sim #153 GUESS"},
    "wave_capsize":    {"enabled": True, "per_day": 1.0, "note": "multiplier on breaking-wave knockdown physics"},
    "knockdown_damage": {"enabled": True, "per_day": 0.002, "note": "probability per knockdown of rig damage"},
    "early_life":      {"enabled": False, "per_day": 0.0, "note": "extra multiplier k*exp(-(day+burn_in)/tau) on hardware hazards",
                        "tau_days": 7.0, "burn_in_days": 0.0},
    "wear_out":        {"enabled": False, "per_day": 1.41, "t_ref_days": 34.9,
                        "note": "sensitivity only: hardware hazards x (day/t_ref)^(k-1), k in per_day. Weibull fit to the "
                                "Microtransat open-ocean record by boat-sim #118 (central k 1.41, t_ref 34.9 d; low 0.75/22.7; "
                                "high 2.24/48.6). The record can't tell it from a steady rate (p = 0.25), so it is off by default."},
}


def _derive(base, changes):
    out = copy.deepcopy(base)
    for k, v in changes.items():
        out[k].update(v)
    return out


RATE_SETS = {
    "original": _ORIGINAL,
    "historical": _derive(_ORIGINAL, {
        "electronics":  {"per_day": 0.0035, "note": "x6 once water is inside; Microtransat open-ocean silent/erratic losses"},
        "comms_silent": {"enabled": True, "per_day": 0.0022},
        "capture":      {"per_day": 0.02, "capture_km": 160, "note": "within ~150 km of land (rings at 100 and 150 km); Microtransat near-land rate 0.019/day"},
        "knockdown_damage": {"per_day": 0.006, "note": "fitted to Microtransat open-ocean rig/weather losses 0.0048/day"},
        "early_life":   {"enabled": True, "per_day": 3.0, "tau_days": 7.0, "burn_in_days": 0.0},
    }),
    "planning": _derive(_ORIGINAL, {
        "electronics":  {"per_day": 0.0025, "note": "x6 once water is inside; historical 0.0035 x0.7 for the potted IP68 box + desiccant"},
        "comms_silent": {"enabled": True, "per_day": 0.0011, "note": "historical 0.0022 x0.5 for the backup D-cell and watchdog"},
        "capture":      {"per_day": 0.01, "capture_km": 160, "note": "within ~150 km of land; historical 0.02 x0.5: labels, notices to fishermen, offshore drop"},
        "knockdown_damage": {"per_day": 0.003, "note": "historical 0.006 x0.5: buoyant, balanced wing on a self-righting hull"},
        "early_life":   {"enabled": True, "per_day": 3.0, "tau_days": 7.0, "burn_in_days": 14.0},
    }),
}
DEFAULT_RATE_SET = "planning"
DEFAULT_RATES = RATE_SETS[DEFAULT_RATE_SET]


def rates_for(scenario):
    """Rate table for a scenario: the named set, then any per-entry overrides."""
    fr = copy.deepcopy(RATE_SETS.get((scenario or {}).get("failure_rate_set") or DEFAULT_RATE_SET, DEFAULT_RATES))
    for k, v in ((scenario or {}).get("failures") or {}).items():
        if k in fr: fr[k].update(v)
    return fr


def wear_out_factor(fr, day):
    """(day / t_ref)^(k - 1), boat-sim's wearout_multiplier (MIT, boat-sim #118). 1.0 when switched off."""
    w = fr.get("wear_out") or {}
    if not w.get("enabled"):
        return 1.0
    return (max(day, 0.5)/max(w.get("t_ref_days", 34.9), 0.1))**(w.get("per_day", 1.0) - 1.0)


def early_life_factor(fr, day):
    """1 + k*exp(-(day + burn_in)/tau): infant-mortality bump for hardware that has not been shaken down."""
    e = fr.get("early_life") or {}
    if not e.get("enabled") or e.get("per_day", 0) <= 0:
        return 1.0
    return 1.0 + e["per_day"]*math.exp(-(day + e.get("burn_in_days", 0.0))/max(e.get("tau_days", 7.0), 0.1))


def p_event(rate_per_day, dt_s):
    return 1 - math.exp(-max(rate_per_day, 0)*dt_s/86400)


def breaking_knockdown_rate(hs, tp, u10, boat_len, beam):
    """Knockdowns per day from breaking waves.
    Whitecap coverage W ~ 3.84e-6 U^3.41 is the fraction of time a point on the sea sits in a
    breaker; each breaking event lasts about half a wave period. Only breakers whose height
    exceeds ~0.55 x boat length (or 1.2 x beam) can roll the boat, and only beam-on hits count.
    Breaker heights are taken as Rayleigh-distributed with scale 0.25 x Hs."""
    if hs <= 0.05 or tp <= 0: return 0.0
    W = min(3.84e-6*max(u10, 0)**3.41, 0.3)
    events_per_day = W*86400/(0.5*max(tp, 1.0))
    h_crit = max(0.55*boat_len, 1.2*beam, 0.3)
    p_big = math.exp(-2*(h_crit/(0.25*hs))**2)
    return events_per_day*p_big*0.25
