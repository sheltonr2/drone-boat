"""Stochastic failure (hazard) model. Rates are events per day; every one can be edited or
switched off in the scenario. Defaults are engineering guesses informed by the history of
small autonomous sailboats (leaks, steering, fouling and collisions end most attempts)."""
import math

DEFAULT_RATES = {
    "leak":            {"enabled": True, "per_day": 0.0025, "note": "x(1+(Hs/3)^2); severity random"},
    "rudder_servo":    {"enabled": True, "per_day": 0.0020, "note": "x(1+Hs/4); stuck or limp"},
    "tail_servo":      {"enabled": True, "per_day": 0.0020, "note": "x(1+Hs/4); stuck or feathered"},
    "fouling_growth":  {"enabled": True, "per_day": 0.004, "note": "drag factor added per day at 20 C SST"},
    "entanglement":    {"enabled": True, "per_day": 0.003, "note": "x3 within 100 km of land; x2 in the Sargasso"},
    "collision":       {"enabled": True, "per_day": 0.0004, "note": "x8 within 100 km of land; 60% fatal"},
    "capture":         {"enabled": True, "per_day": 0.002, "note": "only within 50 km of land"},
    "electronics":     {"enabled": True, "per_day": 0.0012, "note": "x6 once water is inside"},
    "software_hang":   {"enabled": True, "per_day": 0.02, "note": "watchdog recovers 95%"},
    "wave_capsize":    {"enabled": True, "per_day": 1.0, "note": "multiplier on breaking-wave knockdown physics"},
    "knockdown_damage": {"enabled": True, "per_day": 0.002, "note": "probability per knockdown of rig damage"},
}


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
