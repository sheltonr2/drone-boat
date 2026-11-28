"""Run 043c (28 Nov 2026): idle-CPU runs while run 041 downloads the 2025 weather. Randolph: "Do both" (this batch,
and the Rev F software). Rev F (adopted 27 Nov), v2 coastlines, four years of weather already on the PC. No decision
changes; better numbers for the three open recommendations from run 043b.

1. Rev F baseline: plan B, and B with the 90 km approach (B90), same 1,000 launches and seeds as 043a B / 043b B90.
2. BVI holds, fine-tuned: Norman offing 30 km E, 30 and 40 km ESE, 20 and 40 km SE; Anegada W 45 km N and 30 km NE;
   and Norman ESE20 again on Rev F (paired with 043b's Rev E3 run, a check that the design change is neutral).
3. Mindelo 15 Nov-10 Dec on Rev F, to the best upwind points from 043b: Norman offing ESE20 and Anegada W N30.
4. B90 checks: April launch, 21 May-15 June launch, the 70 km drop.
About 6 hours. One queue job (run_043c.bat calls both parts). Run from the repo root: python collab/runs_043c/make_runs.py
"""
import json, math, os, sys, copy
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "collab", "east_west"))
import make_ew as EW
OUT = "collab/runs_043c"
def jload(p): return json.load(open(os.path.join(ROOT, p)))
def jsave(obj, p):
    json.dump(obj, open(os.path.join(ROOT, p), "w"), indent=1); return p
def offset(lat, lon, km_e, km_n):
    return round(lat + km_n / 110.54, 4), round(lon + km_e / (111.32 * math.cos(math.radians(lat))), 4)
def dirkm(d, b):  # km east, km north for distance d at compass bearing b
    return d * math.sin(math.radians(b)), d * math.cos(math.radians(b))

# 1 and 4: eastbound
B = "collab/runs_043a/plan_B.json"; B90 = "collab/runs_043b/plan_B90.json"
s = copy.deepcopy(jload(B90)); d70 = jload("collab/runs_043a/plan_B_drop70.json")
s["start"] = d70["start"]; s["name"] = s["name"].replace("Hatteras 45 km", "Hatteras 70 km").replace("run 043b", "run 043c")
B90_70 = jsave(s, f"{OUT}/plan_B90_drop70.json")

# 2: holds
NO, AW = (18.17, -64.58), (18.72, -64.49)
def hold_at(base, tag, lat, lon, label):
    s = copy.deepcopy(jload(base)); s.update(start={"lat": lat, "lon": lon}, target={"lat": lat, "lon": lon}, station=[lat, lon])
    s["name"] = f"{label}: station-keeping within 1 km, 14 days (Rev F, v2 coasts), run 043c"
    return jsave(s, f"{OUT}/hold_station_{tag}.json")
HN, HA = "collab/runs_043a/hold_station_norman_offing.json", "collab/runs_043a/hold_station_anegada_west.json"
pts = {}
for tag, base, ref, d, b, lab in [
        ("norman_offing_E30", HN, NO, 30, 90, "BVI, 30 km east of the Norman offing"),
        ("norman_offing_ESE30", HN, NO, 30, 112, "BVI, 30 km ESE of the Norman offing"),
        ("norman_offing_ESE40", HN, NO, 40, 112, "BVI, 40 km ESE of the Norman offing"),
        ("norman_offing_SE20", HN, NO, 20, 135, "BVI, 20 km SE of the Norman offing"),
        ("norman_offing_SE40", HN, NO, 40, 135, "BVI, 40 km SE of the Norman offing"),
        ("anegada_west_N45", HA, AW, 45, 0, "BVI, 45 km north of Anegada W"),
        ("anegada_west_NE30", HA, AW, 30, 45, "BVI, 30 km NE of Anegada W")]:
    la, lo = offset(*ref, *dirkm(d, b)); pts[tag] = [la, lo]; pts[tag + "_file"] = hold_at(base, tag, la, lo, lab)
up = jload("collab/runs_043b/upwind_points.json")
pts["norman_offing_ESE20_file"] = "collab/runs_043b/hold_station_norman_offing_ESE20.json"

# 3: Mindelo to the upwind points
def cross_to(base, tag, lat, lon, wps):
    s = copy.deepcopy(jload(base)); s["target"] = {"lat": lat, "lon": lon}; s["waypoints"] = wps
    s["name"] = s["name"].split(" - ")[0] + f" -> holding point {tag} (Rev F, v2 coasts), run 043c"
    return jsave(s, f"{OUT}/ew_mindelo__{tag}.json")
cx = {"norman_offing_ESE20": cross_to("collab/runs_043a/ew_mindelo__norman_offing.json", "norman_offing_ESE20", *up["norman_offing_ESE20"], [[18.15, -63.9]]),
      "anegada_west_N30": cross_to("collab/runs_043a/ew_mindelo__anegada_west.json", "anegada_west_N30", *up["anegada_west_N30"], [[19.05, -63.9]])}

Y4, Y4W, TR = "2021,2022,2023,2024", "2022,2023,2024,2025", EW.TROPICS_CSV
P = "043c_2021-2024_revF"
east = [("Rev F: plan B", B, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_B_v2", ""),
        ("Rev F: B90", B90, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_B90_v2", ""),
        ("Rev F: B90 launched in April", B90, 1000, "2023-04-01", "2023-04-30", Y4, f"plan{P}_B90_april_v2", ""),
        ("Rev F: B90 launched 21 May-15 Jun", B90, 1000, "2023-05-21", "2023-06-15", Y4, f"plan{P}_B90_latemay_v2", ""),
        ("Rev F: B90 from the 70 km drop", B90_70, 1000, "2023-05-01", "2023-05-20", Y4, f"plan{P}_B90_drop70_v2", "")]
htags = ["norman_offing_ESE20", "norman_offing_E30", "norman_offing_ESE30", "norman_offing_ESE40", "norman_offing_SE20",
         "norman_offing_SE40", "anegada_west_N45", "anegada_west_NE30"]
ew = [(f"BVI hold {t}", pts[t + "_file"], 500, "2022-02-01", "2022-04-30", Y4W, f"hold043c_2022-2025_revF_station_{t}_v2", None) for t in htags]
ew += [(f"Mindelo 15 Nov-10 Dec -> {t}", sc, 1000, "2021-11-15", "2021-12-10", Y4, f"ew{P}_mindelo_nov__{t}_v2", TR) for t, sc in cx.items()]

# write the .bat files with run 043a's writer (same format), with the Rev F design
src = open(os.path.join(ROOT, "collab", "runs_043a", "make_runs.py")).read()
ns = {"os": os, "SIM": os.path.join(ROOT, "simulator"), "E3": "designs/revF_design.json", "chr": chr}
exec(src[src.index("PY = r"):src.index("Y4, Y4W, TR")], ns)
ns["part"]("043c1_east", "Run 043c part 1: Rev F baseline and B90 checks", east, False)
ns["part"]("043c2_ew", "Run 043c part 2: BVI holds fine-tuned, Mindelo to the upwind points", ew, True)
W = ["@echo off", "REM Run 043c: Rev F baseline, BVI holds fine-tuned, Mindelo to the upwind points, B90 checks.",
     "REM About 6 hours: part 1 eastbound (5 runs, about 3 h), part 2 east-west (10 runs, about 3 h).", 'cd /d "%~dp0"',
     "echo ============================================================",
     "echo  Run 043c: Rev F baseline, BVI holds, Mindelo, B90 checks - 15 runs, about 6 hours",
     "echo  Part 1 eastbound (about 3 h), then part 2 east-west (about 3 h). Started %date% %time%",
     "echo  Logs: collab\\run_log_043c1_east.txt and collab\\run_log_043c2_ew.txt",
     "echo ============================================================",
     "call run_043c1_east.bat", "call run_043c2_ew.bat",
     "echo.", "echo ============================================================", "echo  ALL DONE %date% %time%",
     "echo ============================================================"]
open(os.path.join(ROOT, "simulator", "run_043c.bat"), "w", newline="\r\n").write("\n".join(W) + "\n")
json.dump({k: v for k, v in pts.items() if not k.endswith("_file")}, open(os.path.join(ROOT, OUT, "points.json"), "w"), indent=1)
print(len(east), "east;", len(ew), "east-west"); print(json.dumps({k: v for k, v in pts.items() if not k.endswith("_file")}))
