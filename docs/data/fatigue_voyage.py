"""Fatigue damage and servo movements over a whole crossing (docs/Fatigue_Review.md).

Inputs (run from the repo root):
  results/2026-11-14_seastates_hatteras__cornwall.json  hours at each wave height along the 500 Rev E tracks
                                                         (45 km off Hatteras -> Cornwall, 2023+2024 weather)
  docs/data/motions_loads.json      damage per hour for each part at Hs 0.75-5 m, quartering (150) and beam (90) seas
  docs/data/steering_filter_sweep.json   rudder movements per hour with the wave filter
Damage per hour is interpolated in Hs (held at the end values outside 0.75-5 m) and mixed 70% quartering / 30% beam.
Miner's sum: 1.0 = the part's fatigue life used up. Grade D (the loads model's own limits apply)."""
import json, statistics as st
import numpy as np
SS = json.load(open('results/2026-11-14_seastates_hatteras__cornwall.json'))
ML = json.load(open('docs/data/motions_loads.json'))
SW = json.load(open('docs/data/steering_filter_sweep.json'))
edges = SS['hs_edges']; mids = [(a + b)/2 for a, b in zip(edges[:-1], edges[1:])]
hours = np.zeros(len(mids))
for k, h in SS['hours_by_hs_tp'].items():
    i = min(int(k.split(",")[0]), len(mids) - 1); hours[i] += h   # bin 40 = Hs >= 10 m
nv = len(SS['voyages']); per_voy = hours/nv
vh = sorted(v['hours_sampled'] for v in SS['voyages'])
mean_h, p90_h = st.mean(vh), vh[int(.9*len(vh))]
def curve(get, rels=(150, 90), w=(0.7, 0.3)):
    hs = sorted({r['hs'] for r in ML})
    vals = []
    for h in hs:
        v = [get(next(r for r in ML if r['hs'] == h and r['rel_deg'] == rel)) for rel in rels]
        vals.append(sum(a*b for a, b in zip(w, v)))
    return lambda x: float(np.interp(x, hs, vals))
parts = list(ML[0]['loads'])
out = dict(voyages=nv, mean_hours=mean_h, p90_hours=p90_h, hours_per_voyage_by_hs={f"{a:.2f}-{b:.2f}": round(float(h), 1) for a, b, h in zip(edges[:-1], edges[1:], per_voy) if h > 0.05})
print(f"{nv} voyages; mean {mean_h/24:.0f} days sampled per voyage (p90 {p90_h/24:.0f})")
print("Hours per average voyage by Hs:", ", ".join(f"{a:.1f}-{b:.1f} m: {h:.0f} h" for a, b, h in zip(edges[:-1:2], edges[2::2], per_voy[0::2] + per_voy[1::2]) if h >= 0.5))
print(f"Share of time with Hs >= 3 m: {100*per_voy[np.array(mids) >= 3].sum()/per_voy.sum():.1f}%, >= 5 m: {100*per_voy[np.array(mids) >= 5].sum()/per_voy.sum():.2f}%")
print("\nMiner's damage per voyage (1.0 = life used up); average voyage, and a long (p90) voyage scaled by hours:")
out['damage_per_voyage'] = {}
for p in parts:
    f = curve(lambda r: r['loads'][p]['damage_per_h'])
    d = float(sum(h*f(m) for h, m in zip(per_voy, mids)))
    out['damage_per_voyage'][p] = d
    print(f"  {p:13s} {d:9.2e}   p90 voyage {d*p90_h/mean_h:9.2e}   ({1/d if d > 0 else float('inf'):,.0f} crossings to use the life)")
# Tail boom: the 5 m beam case was run on the old 12 x 10 tube (53 N*m). Rev E1 fits 16 x 14 (section modulus x1.89,
# about 100 N*m). With the cfrp S-N rule (10% per decade -> b 0.07) the worst cycle seen goes from:
tb = next(r for r in ML if r['hs'] == 5.0 and r['rel_deg'] == 90)['loads']['tail_boom']
for su, lab in ((53.0, '12 x 10 (Rev E)'), (53.0*1.894, '16 x 14 (Rev E1)')):
    r = (tb['max_amp'] + tb['mean_abs'])/su
    print(f"  tail boom {lab}: worst load {100*r:.0f}% of strength -> about {10**((1 - r)/0.07):,.0f} cycles to failure at that load")
# Servo movements
def sw(rules, hs, rel):
    c = [r for r in SW if r['rules'] == rules and r['rel'] == rel]
    return float(np.interp(hs, [r['hs'] for r in c], [r['moves_per_h'] for r in c]))
filt = lambda x: 0.7*sw("(0, 0, 0, 6.0)", x, 150) + 0.3*(sw("(0, 0, 0, 6.0)", x, 90) if 1.5 < x < 3.5 else sw("(0, 0, 0, 6.0)", x, 150))
unf = curve(lambda r: r['rudder_moves_per_h'])
mf = float(sum(h*filt(m) for h, m in zip(per_voy, mids))); mu = float(sum(h*unf(m) for h, m in zip(per_voy, mids)))
out['servo_moves_per_voyage'] = dict(filter_6s=mf, unfiltered=mu, filter_6s_p90=mf*p90_h/mean_h)
print(f"\nRudder servo movements per voyage: with the 6 s wave filter {mf/1e6:.2f} million (p90 voyage {mf*p90_h/mean_h/1e6:.2f} M); "
      f"unfiltered {mu/1e6:.1f} million")
json.dump(out, open('docs/data/fatigue_voyage.json', 'w'), indent=1)
