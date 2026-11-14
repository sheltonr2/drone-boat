"""Which steering rule saves the rudder servos without losing the course? (docs/Fatigue_Review.md, steering)
6-DOF runs of Rev E, 300 s each after 120 s settling, waves and wind from the quarter or the beam.
Rules: (heading deadband deg, minimum seconds between commands, servo deadband deg)
  continuous      the 6-DOF model's PD autopilot, moving the rudder whenever the command changes
  (2, 10, 0)      the Rev E rule as written in Design_RevE.md: hold inside 2 deg, a new command at most every 10 s
  (2, 0, 0)       heading deadband only;  (0, 2, 0) a command every 2 s only
  (0, 0, x)       servo deadband: move only when the new command differs from the rudder by more than x deg
Run from the repo root: python docs/data/steering_rules_sweep.py   (about 15 minutes)"""
import sys, runpy, json
sys.argv = ['x', '300', '/tmp/unused.json']
g = runpy.run_path('docs/data/motions_loads.py', run_name='notmain')
sys.path.insert(0, 'simulator')
from drone_sim import design as D
d = D.load('designs/revE_design.json')
rows = []
for hs, tp, U, rel in ((1.5, 8.0, 7.8, 150), (2.5, 9.0, 10.0, 150), (2.5, 9.0, 10.0, 90), (3.5, 10.0, 11.9, 150)):
    for rules in (False, (2.0, 10.0, 0.0), (2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 0.5), (0.0, 0.0, 1.0), (0.0, 0.0, 2.0)):
        r = g['run_case'](d, hs, tp, U, rel, rules)
        row = dict(hs=hs, rel=rel, rules=str(rules), u=r['u_mean'], hdg_err_rms=r['hdg_err_rms'], moves_per_h=r['rudder_moves_per_h'],
                   travel_deg_per_h=r['rudder_travel_deg_per_h'], hinge_p99=r['hinge_torque_nm']['p99'])
        rows.append(row)
        print(f"Hs {hs} waves {rel:3d} rules {str(rules):16s} u {r['u_mean']:.2f} m/s  hdg err {r['hdg_err_rms']:5.1f}  "
              f"moves/h {r['rudder_moves_per_h']:6.0f}  travel {r['rudder_travel_deg_per_h']:7.0f} deg/h", flush=True)
json.dump(rows, open('docs/data/steering_rules_sweep.json', 'w'), indent=1)
