# Rev B simulation: wing counterweight on a forward arm

Nov 8, 2026

Moving the wing counterweight from the wing's nose pocket to a pod on a 300 mm forward arm keeps the boat at 20.8 kg instead of 27.5 kg. It also nearly doubles the stability margin and makes crossings about 4 days faster. In the Monte Carlo it reached Europe more often (47.5% vs 40%), but with 40 runs each that gap is within the noise.

All runs use the simulator's **synthetic (invented) weather**, because historic data could not be downloaded from the build environment. Treat the numbers as a comparison between the two layouts, not as forecasts. Rerun on historic weather with `python -m drone_sim.cli mc ...` on your computer.

## Design comparison

| | Rev B: pod on 300 mm arm | Rev A as drawn: nose pocket |
| --- | --- | --- |
| Lead to balance the wing | 0.80 kg | 7.64 kg |
| Rotating rig mass | 2.24 kg | 8.96 kg |
| All-up mass | 20.8 kg | 27.5 kg |
| GM (initial stability) | 0.201 m | 0.112 m |
| Maximum righting arm | 0.434 m | 0.291 m |
| Self-righting from 180° | yes | yes |

## Sailing, failures switched off (3 start dates each)

| | Rev B | Rev A |
| --- | --- | --- |
| Crossing time, Newfoundland to Ireland | 79.9–80.4 days | 83.3–84.7 days |
| Mean speed over ground | 0.85–0.86 kn | 0.80–0.82 kn |

## Monte Carlo, 40 voyages each, June starts, default failure rates

| | Rev B | Rev A |
| --- | --- | --- |
| Reaches Europe, still reporting | 47.5% (95% range 33–63%) | 40.0% (26–55%) |
| Reaches Europe at all | 50.0% | 42.5% |
| Lost at sea | 37.5% | 42.5% |
| Median crossing | 82.0 days | 86.5 days |
| Knockdowns per voyage (mean) | 17.3 | 20.3 |
| Satellite airtime per voyage (mean) | $95 | $101 |

The main causes of loss are the same for both layouts: leaks (7 runs each), electronics failure (5 vs 7) and ship strikes (3 each). The counterweight change doesn't address those. Leak-proofing and electronics reliability are still the biggest levers on the odds.

## Files

- `results/2026-11-08_revB_montecarlo.json` and `results/2026-11-08_revA_noseweight_montecarlo.json`: full Monte Carlo results. Open either in the results viewer (`results-viewer/index.html`).
- `results/2026-11-08_revB_voyage_no_failures.json`: the example Rev B voyage shown in the viewer's demo.
