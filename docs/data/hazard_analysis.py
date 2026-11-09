"""Exposure-based failure rates from the Microtransat record, and a check of the simulator
against it. Run from the repo root:  python docs/data/hazard_analysis.py
Inputs : docs/data/crossing_attempts.csv, results/*midatlantic*montecarlo.json
Output : printed tables (saved as docs/data/hazard_analysis_output.txt)"""
import csv, json, math, os, glob, collections
from scipy.stats import chi2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
NEAR_KM = 150.0      # "near land" band: within ~150 km of a coast (shelf, channels, fishing grounds)
TORTUOSITY = 1.5     # track km per km made good when leaving the coast

def poisson_ci(k, t, conf=0.95):
    a = 1 - conf
    lo = 0.0 if k == 0 else chi2.ppf(a/2, 2*k)/(2*t)
    hi = chi2.ppf(1-a/2, 2*k+2)/(2*t)
    return lo, hi

rows = list(csv.DictReader(open(os.path.join(HERE, "crossing_attempts.csv"))))
for r in rows:
    r["days"] = float(r["days"]) if r["days"] else None
    r["track_km"] = float(r["track_km"]) if r["track_km"] else None

def split_exposure(r):
    """Days spent near land (N) and in open ocean (O)."""
    d, km, z = r["days"], r["track_km"], r["end_zone"]
    if d is None or z == "U": return None
    if z == "N" and r["crossed"] != "yes":
        return d, 0.0
    v = km/d if km else 50.0
    dep = min(d, TORTUOSITY*NEAR_KM/v)
    arr = dep if r["crossed"] == "yes" else 0.0
    n = min(d, dep+arr)
    return n, d-n

exp = {"N": 0.0, "O": 0.0}; ev = collections.defaultdict(lambda: collections.Counter())
used = 0
for r in rows:
    s = split_exposure(r)
    if s is None: continue
    used += 1
    exp["N"] += s[0]; exp["O"] += s[1]
    if r["root_cause"] != "none":
        ev[r["end_zone"]][r["root_cause"]] += 1

out = []
P = out.append
P(f"Microtransat attempts in file: {len(rows)}; with usable exposure: {used}")
P(f"Exposure: near land {exp['N']:.1f} boat-days, open ocean {exp['O']:.1f} boat-days, total {exp['N']+exp['O']:.1f}")
for z, name in (("N", "NEAR LAND (<~150 km)"), ("O", "OPEN OCEAN")):
    tot = sum(ev[z].values()); lo, hi = poisson_ci(tot, exp[z])
    P(f"\n{name}: {tot} mission-ending events / {exp[z]:.1f} days = {tot/exp[z]:.4f} per day (95% CI {lo:.4f}-{hi:.4f})")
    for c, k in ev[z].most_common():
        lo, hi = poisson_ci(k, exp[z])
        P(f"   {c:22s} {k:2d}  {k/exp[z]:.4f}/day  (95% CI {lo:.4f}-{hi:.4f})")

# Kaplan-Meier of "still sailing and reporting"
def km(times):  # times: list of (t, event)
    times = sorted(times); n = len(times); S = 1.0; curve = [(0.0, 1.0)]
    i = 0
    while i < len(times):
        t = times[i][0]; d = sum(1 for x in times if x[0] == t and x[1]); c = sum(1 for x in times if x[0] == t)
        if d: S *= (1 - d/n); curve.append((t, S))
        n -= c; i += c
    return curve
def S_at(curve, t):
    s = 1.0
    for ti, si in curve:
        if ti <= t: s = si
    return s
mt = [(r["days"], r["root_cause"] != "none") for r in rows if r["days"] is not None]
c_mt = km(mt)
P("\nKaplan-Meier, Microtransat (all 35 attempts with a published duration):")
P("   " + "  ".join(f"S({t}d)={S_at(c_mt,t):.2f}" for t in (1, 3, 7, 14, 30, 60, 90)))
mt_ww = [(r["days"], r["root_cause"] != "none") for r in rows if r["days"] is not None and r["direction"] == "W-E"]
c_ww = km(mt_ww)
P(f"Kaplan-Meier, Microtransat west-to-east only ({len(mt_ww)} attempts, the direction we will sail):")
P("   " + "  ".join(f"S({t}d)={S_at(c_ww,t):.2f}" for t in (1, 3, 7, 14, 30, 60, 90)))

def greenwood(times, t):
    """95% interval on S(t) (Greenwood variance, log-log transform)."""
    times = sorted(times); n = len(times); S = 1.0; v = 0.0; i = 0
    while i < len(times) and times[i][0] <= t:
        tt = times[i][0]; d = sum(1 for x in times if x[0] == tt and x[1]); c = sum(1 for x in times if x[0] == tt)
        if d:
            S *= (1 - d/n)
            if n > d: v += d/(n*(n - d))
        n -= c; i += c
    if S <= 0 or S >= 1 or v == 0: return S, S, S
    se = math.sqrt(v)/abs(math.log(S)); z = 1.96
    return S, S**math.exp(z*se), S**math.exp(-z*se)
P("   95% intervals (west-to-east): " + "  ".join(
    "S({}d) {:.2f}-{:.2f}".format(t, *greenwood(mt_ww, t)[1:]) for t in (7, 14, 30, 60, 90)))

# Simulator check
for f in sorted(glob.glob(os.path.join(ROOT, "results", "*midatlantic*montecarlo*.json"))):
    d = json.load(open(f)); runs = d["result"]["runs"]
    sim = []
    for r in runs:
        ev_ = r["outcome"] in ("lost", "aground")
        sim.append((r["days"], ev_))
    c_s = km(sim)
    P(f"\nSimulator Monte Carlo ({os.path.basename(f)}, {len(runs)} runs; loss or grounding = event, arrival = censored):")
    P("   " + "  ".join(f"S({t}d)={S_at(c_s,t):.2f}" for t in (1, 3, 7, 14, 30, 60, 90)))
    lost = [r for r in runs if r["outcome"] in ("lost", "aground")]
    T = sum(r["days"] for r in runs)
    P(f"   Mean hazard over the whole voyage: {len(lost)}/{T:.0f} boat-days = {len(lost)/T:.4f} per day")
    silent = sum(1 for r in runs if r["outcome"] == "arrived_silent")
    P(f"   Plus {silent} runs that arrived with comms already dead (silent failures not counted above)")
    if all(r.get("last_report_day") is not None for r in runs):
        # Same yardstick as the Microtransat table: days until the last report; only a reporting arrival is a success
        rep = [(r["last_report_day"] if r["outcome"] != "arrived_reporting" else r["days"],
                r["outcome"] != "arrived_reporting") for r in runs]
        c_r = km(rep)
        P("   Still reporting (Microtransat yardstick: last report; silent arrival = failure):")
        P("   " + "  ".join(f"S({t}d)={S_at(c_r,t):.2f}" for t in (1, 3, 7, 14, 30, 60, 90)))
    s_ = d["result"]["summary"]
    P(f"   Success (arrived and reporting): {s_['success_percent']}% (95% CI {s_['success_ci95'][0]}-{s_['success_ci95'][1]})")
txt = "\n".join(out); print(txt)
open(os.path.join(HERE, "hazard_analysis_output.txt"), "w").write(txt + "\n")
