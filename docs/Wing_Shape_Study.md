# Wing shape study: the same sail area, shorter and wider

11 November 2026. Grade D. Script `docs/data/wing_shape_study.py`, output `docs/data/wing_shape_study_output.txt`.

## Correction (12 November 2026)

The first version of this study averaged the speed wrongly: its script passed wind angles in degrees to a speed table that expects radians, so every point was really dead downwind. Separately, the speed model's stall rule made a stubbier wing stall sooner, which is backwards (found by John's team). Both are fixed ([Simulator_Angle_Bug.md](Simulator_Angle_Bug.md)). With the old stall rule and correct angles, the 0.8 m wing would have cost about 22%; with both fixes it costs about 2%. The table below is the corrected one. The decision to adopt 0.8 × 0.375 m stands.

## Result

**A wing 0.8 m tall and 0.375 m wide halves the worst wing-slap load and cuts the chance of breaking the spar in a knockdown by four to eight times, for about 2% less average speed and 3% less upwind progress.** Going shorter than 0.7 m buys little more.

| Wing (height × width) | Average speed against today's wing | Upwind progress in 7 m/s of wind | Worst slap load, 1 in 1,000 | Chance of breaking the spar in one knockdown, seas of 3 m / 6 m |
|---|---|---|---|---|
| 1.0 × 0.300 m (Rev C4) | — | 0.37 knots | 1,640 N·m | 0.0016 / 0.0099 |
| 0.9 × 0.333 m | −0.5% | 0.37 | 1,100 (67%) | 0.0004 / 0.0051 |
| **0.8 × 0.375 m (Rev C5)** | **−1.7%** | 0.36 (−3%) | 850 (52%) | 0.0002 / 0.0026 |
| 0.7 × 0.429 m | −2.6% | 0.36 (−3%) | 610 (37%) | 0.0001 / 0.0019 |
| 0.6 × 0.500 m | −2.0% | 0.35 (−5%) | 430 (26%) | 0.0002 / 0.0015 |

All five have 0.30 m² of area and the Rev C3 spar (30 × 22 mm, about 1,130 N·m). Average speed is over wind angles 50–150° at 4, 7, 10 and 14 m/s. John's team, with the same stall fix in their own model, get −3.6% averaged over 3–15 m/s and 50–165°, and about 0% downwind.

## What it means for the voyage

- **Cost:** about 2% slower on average, roughly 2–3 more days on a 130-day crossing.
- **Gain:** wing damage was the largest single failure in the real-weather runs (about 1 voyage in 6 before the stronger spar). The stronger spar already cuts that to roughly 1 in 20; the shorter wing would take it to roughly 1 in 100.
- **So the net gain is a few voyages in a hundred.** It is worth having, but it is no longer the large win it would have been before the spar change.
- **Side effects, all small and favourable:** the centre of effort is 0.1 m lower, so the boat heels less; stability improves slightly (GM 0.185 m against 0.182); the wing weighs about 0.1 kg more.

## How it was done

- **Speed:** the voyage simulator's own speed model, rebuilt for each wing shape, averaged over five wind angles (50° to 150°) at four wind speeds. A shorter, wider wing has more induced drag, which is where the loss comes from.
- **Loads:** the strike simulation with breakers matched to measured buoy data. The slap load depends on how fast the tip is moving when it meets the water and how far out it is, so it falls quickly as the wing gets shorter.

## Limits

- The chances per knockdown are model figures and are several times higher than the rate the voyage simulator is calibrated to. Trust the ratios between shapes, not the absolute values.
- Below about 0.7 m the remaining risk is the breaker's own water hitting the wing, which a shorter wing does not avoid.
- Not checked: whether the tail still has enough leverage on a wider wing in very light wind, and the fit of the solar-panel shadow. Both look fine on the drawing but need a look if the wing is redrawn.

## Outcome

Adopted as Rev C5 the same day (0.8 × 0.375 m): new wing template T15, sheets D01 and D06, simulator wing dimensions. The spar is shorter (995 mm); bearings, tail and printed parts are unchanged.
