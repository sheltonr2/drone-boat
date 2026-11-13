"""Storm encounters for the 12 launch-point runs (docs/Hurricane_Risk.md, 13 Nov update). Run from the repo root."""
import json, sys, numpy as np
sys.path.insert(0, 'simulator')
from drone_sim.storms import StormClimatology
clim = StormClimatology()
L = ['hatteras_stream','ocean_city_canyon','hatteras','virginia_beach','ocean_city','cape_cod','montauk','maine','charleston','palm_beach','barnegat','canaveral']
ok = lambda r: r['outcome'] in ('arrived_reporting','arrived_tracked')
LOSS = {'TS': 0.30, 'HU': 0.70}          # grade-D loss model from docs/Hurricane_Risk.md, storm within 100 km
out = {}
for nm in L:
    d = json.load(open(f'results/2026-11-13_launch_2023_{nm}__ireland_sw.json'))['result']; R = d['runs']; n = len(R)
    acc = {'any200': [], 'hu200': [], 'any100': [], 'hu100': []}; bymon = {}; adj = 0.0; succ = 0
    for r in R:
        tr = r.get('track')
        if not tr or len(tr[0]) < 3: continue
        v200 = clim.voyage(tr, r['start_time'], 200.0); v100 = clim.voyage(tr, r['start_time'], 100.0)
        a200 = np.mean([w >= 34 for _, w, _ in v200]); h200 = np.mean([w >= 64 for _, w, _ in v200])
        a100 = np.mean([w >= 34 for _, w, _ in v100]); h100 = np.mean([w >= 64 for _, w, _ in v100])
        for k, v in (('any200', a200), ('hu200', h200), ('any100', a100), ('hu100', h100)): acc[k].append(v)
        mon = r['start_time'][5:7]; bymon.setdefault(mon, []).append(a200)
        if ok(r):
            succ += 1
            loss = np.mean([LOSS['HU'] if w >= 64 else LOSS['TS'] if w >= 34 else 0.0 for _, w, _ in v100])
            adj += 1 - loss
    out[nm] = dict(n=n, succ=100*succ/n, adj=100*adj/n, **{k: 100*float(np.mean(v)) for k, v in acc.items()},
                   may=100*float(np.mean(bymon.get('05', [0]))), june=100*float(np.mean(bymon.get('06', [0]))))
    o = out[nm]
    print(f"{nm:18s} TS+ 200km {o['any200']:5.1f}%  HU 200km {o['hu200']:4.1f}%  TS+ 100km {o['any100']:4.1f}%  HU 100km {o['hu100']:4.1f}%  | May {o['may']:4.1f} Jun1-15 {o['june']:4.1f} | success {o['succ']:.1f} -> {o['adj']:.1f}", flush=True)
json.dump(out, open('docs/data/launch_storms.json', 'w'), indent=1)
