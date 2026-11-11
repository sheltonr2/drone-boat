# Keel fin strength in knockdowns: a physics estimate

11 November 2026. Grade D (hand-calculation level, no test data yet). Script: `docs/data/keel_reliability.py`, output: `docs/data/keel_reliability_output.txt`.

## Why

John's boat-sim rolls a dice at every knockdown for "keel or structure lost" (4e-5 × (Hs/3)², capped at 5%). Our simulator has no such event. This note estimates the chance from our own structure and the loads it would see, instead of a placeholder.

## Result

**The fin as drawn in Rev C is too weak. The model says it would break in the first days of breaking seas, under every load assumption tried.** A solid hardwood core with a thicker skin and two carbon strips fixes it for about 0.75 kg.

| Fin construction | Strength at the root | Times the static load | Chance of breaking per voyage: gentle / central / hard strikes | Added mass |
|---|---|---|---|---|
| As drawn: XPS foam core, 3 × 6 oz glass each side, two M10 rods | 113 N·m | 3.2 | 100% / 100% / 100% | 0 |
| H80 PVC foam core, same skins | 234 N·m | 6.5 | 4% / 100% / 100% | 0.05 kg |
| Hardwood core, 6 × 6 oz each side | 661 N·m | 18.5 | 0% / 3.5% / 97% | 0.60 kg |
| Hardwood core, 6 × 6 oz, plus a 60 × 1.5 mm carbon strip each side | 1,103 N·m | 31 | 0% / 0% / 10% | 0.75 kg |

"Static load" is 36 N·m: the weight of the 9.2 kg bulb in water on its 0.436 m arm with the boat lying on its side. A voyage sees about 660 knockdowns (mean of the 500 real-weather voyages of 11 November).

Per knockdown, the hardwood fin comes out at 3e-6 at Hs 3 m and 6e-5 at Hs 6 m in the central case. John's placeholder gives 4e-5 and 1.6e-4 at the same wave heights, so his number is about right for a solid-cored fin and far too kind to ours as drawn.

## How the model works

1. **Strength.** Bending strength of the fin root section (170 mm chord, 20.4 mm thick). With a foam core the thin glass skin on the compressed side buckles into the foam (face wrinkling) long before the glass itself fails: at about 65 MPa on XPS against 200 MPa for the glass. That is why the as-drawn fin is weak. The two M10 rods sit on the centreline, where they add little bending strength (48 N·m at yield). Strength is given 20% scatter for hand lay-up.
2. **Load in one strike.** A breaking crest throws the hull sideways. The bulb, 0.44 m below, has to be dragged along through the fin. The fin is treated as a spring between the hull and the bulb (plus the water the fin carries with it), which gives the peak root moment from the hull's change of speed and how quickly it happens. Drag on the fin swept sideways and the static bulb weight are added.
3. **Sea state.** Breaker heights follow the same rule the voyage simulator uses to count knockdowns (tail of a Rayleigh distribution above 0.825 m), and crest speed follows from breaker height.
4. **Per voyage.** The per-knockdown chance at each wave height is combined with the knockdown counts by wave height logged on real 2023 and 2024 weather.

Typical strike at Hs 5 m: median root moment 65 N·m, 1 in 20 above 190 N·m, 1 in 1,000 above 350 N·m.

## What is uncertain

- **The load side, by about a factor of 2 either way.** The two inputs that matter most are guesses: how much of the crest's speed the hull picks up (central 25 to 85%) and how fast (0.05 to 0.4 s). The three columns in the table span that. Per-voyage numbers between 1% and 99% are not to be trusted; the ranking of the four constructions is.
- Material values are handbook figures, not coupons.
- **Not modelled: the joint between fin and hull.** Both rods are on the centreline, so the sideways moment goes into the hull through the 40 mm deep keel box and the 60 mm wide G10 plate. At 600 N·m that is about 10 kN on each edge of the plate, into a hull bottom of 10 mm foam with two plies outside and one inside. This is probably the next weak point once the fin is strengthened. Floors tying the keel box to the hull sides and the x 300 bulkhead would deal with it.
- Not modelled: fatigue beyond a simple check (everyday rolling puts about 27 N·m on the root, a quarter of the as-drawn strength, which is at the limit for glass over millions of cycles), groundings, and collisions.
- After the shell fails the rods fold at about 82 N·m rather than snap, so the bulb would probably stay attached but hang off to one side. For the voyage that is the same as losing the keel.

## Recommended

1. Change the fin to a hardwood core with 6 × 6 oz each side and a carbon strip each side, and add floors at the keel box. This needs a drawing change (D04, templates) and is not done yet.
2. Add a proof test to Field_Tests.md: boat on its side, 60 kg hung from the bulb (260 N·m, 7 times static), no cracking sounds, no permanent set. It tests the fin and the hull joint together, which the calculation cannot.
3. Until the test is done, use John's placeholder (4e-5 × (Hs/3)²) in both simulators for the strengthened fin. On our knockdown counts it costs about 8% of voyages.
