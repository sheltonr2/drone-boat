"""Wave-filter steering rules (docs/Fatigue_Review.md): 6-DOF, Rev E, 300 s per case. rules = (heading deadband deg,
update interval s, servo deadband deg, wave-filter time constant s). Run from the repo root."""
import sys, runpy, json
sys.argv=['x','300','/tmp/unused.json']
g = runpy.run_path('docs/data/motions_loads.py', run_name='notmain')
from drone_sim import design as D
d = D.load('designs/revE_design.json')
rows=[]
for hs, tp, U, rel in ((1.5, 8.0, 7.8, 150), (2.5, 9.0, 10.0, 150), (2.5, 9.0, 10.0, 90), (3.5, 10.0, 11.9, 150)):
    for rules in ((0,0,0,3.0), (0,0,0,6.0), (0,0,0,12.0), (0,0,1.0,6.0)):
        r = g['run_case'](d, hs, tp, U, rel, rules)
        rows.append(dict(hs=hs, rel=rel, rules=str(rules), u=r['u_mean'], hdg_err_rms=r['hdg_err_rms'], moves_per_h=r['rudder_moves_per_h'], travel_deg_per_h=r['rudder_travel_deg_per_h']))
        print(f"Hs {hs} waves {rel:3d} rules {str(rules):18s} u {r['u_mean']:.2f} m/s  hdg err {r['hdg_err_rms']:5.1f}  moves/h {r['rudder_moves_per_h']:6.0f}  travel {r['rudder_travel_deg_per_h']:7.0f} deg/h", flush=True)
json.dump(rows, open('docs/data/steering_filter_sweep.json','w'), indent=1)
