# Fatigue, steering workload and motions (Rev E)

13 November 2026. Items 4, 6 and 8 of [Naval_Review.md](Naval_Review.md). Grade D: the 6-DOF model and handbook S-N rules, nothing measured.

**Scripts:**
- `docs/data/motions_loads.py` (results in `motions_loads.json` and `motions_loads_output.txt`)
- `docs/data/steering_rules_sweep.py` (output `steering_rules_sweep_output.txt`)
- `docs/data/steering_filter_sweep.py` (output `steering_filter_sweep_output.txt`)

## Short answer

- **Fatigue is not a problem for the hull, fin, spar, stern post, counterweight arm or rudder stocks.** Even if a whole voyage were spent in 5 m beam seas, Miner's sum stays below 1% for every one of them. Their wave-by-wave loads are 1–10% of their strength.
- **The tail boom is the exception.** In 5 m beam seas the tail dips into the water as the boat rolls, and the 12 × 10 mm carbon tube sees load cycles up to three-quarters of its strength. Each hour in such seas uses about 5% of its fatigue life. A 16 × 14 mm tube (+30 g) would end this.
- **The servo count is the real fatigue issue, and the Rev E steering rule as written doesn't work.**
  - The 6-DOF autopilot, steering continuously, moves each rudder 1,600 to 41,000 times an hour, depending on the sea. Over a 112-day voyage that is roughly 10 to 100 million movements, against the 1 million that Test P planned.
  - The Rev E rule ("2° deadband, at most one correction per 10 s") loses the course in a quartering sea: heading error 78–83° RMS, speed down by two-thirds.
  - **A wave filter** (steer on a 3–6 s low-passed heading error and yaw rate) cuts movements to about 1,000 an hour, travel by 2–8×, and holds the course.

## How

The 6-DOF model (`simulator/drone_sim/sixdof.py`: irregular directional seas, foil strips, exact hydrostatics) was run for Rev E in steady sea states:
- Hs 0.75, 1.5, 2.5, 3.5 and 5 m, with Tp = 6.5 s + Hs and the wind of a developed sea.
- Waves on the starboard quarter (150° off the bow, the usual case on this route) or on the beam.
- 20 minutes each after 2 minutes to settle.

From the recorded motion:
- **Bending at each part's root** from gravity, the part's own acceleration (lumped masses at their real positions) and the lift and drag on its foil strips.
- **Rainflow cycle counting** with Goodman mean-stress correction.
- **S-N rules:**
  - glass/epoxy and the hardwood/glass fin lose 10% of their static strength per decade of cycles;
  - carbon/epoxy loses 7% per decade;
  - the 316 rudder stock in seawater: 150 MPa at 10⁶ cycles, slope 5, no endurance limit.
- **Static strengths** from [Structural_Review.md](Structural_Review.md) and Rev C3.
- **Steering workload:**
  - movements are rudder half-cycles of at least 0.5° (rainflow);
  - travel is the total degrees moved;
  - heading error is the RMS over the run.

**Not included:**
- the fin's and bulb's added mass;
- wave slap on the rig;
- knockdowns and breaking-wave strikes, which [Structural_Review.md](Structural_Review.md) covers as one-off strength;
- weed or a jammed blade loading the servo.

**The hours in each sea state** come next: a run on the PC is sampling the wave data along the 500 Hatteras → Cornwall tracks (request 015c; the first attempt stopped at a voyage that ran into December, now fixed). Until then the conclusions rest on bounds: the worst sea state for the whole voyage.

## Loads, part by part

| Part | Strength (N·m) | Largest cycle amplitude, worst sea state | Fatigue damage per hour, worst sea state | Whole voyage at that rate |
|---|---|---|---|---|
| Fin root | 1,103 | 69 (Hs 5, beam) | 3×10⁻⁶ | under 1% |
| Wing spar at upper bearing | 1,130 | 98 (Hs 5, beam) | 1×10⁻¹⁰ | negligible |
| Stern post | 200 | 5 | 3×10⁻⁶ | under 1% |
| Counterweight arm (glass rod) | 119 | 6 (on a steady 3 N·m from the pod's weight) | 2×10⁻⁶ | under 1% |
| **Tail boom (12 × 10 carbon)** | **53** | **39 (Hs 5, beam)** | **0.05 at Hs 5 beam; 2×10⁻⁸ at Hs 3.5** | **depends on hours in 5 m beam seas** |
| Rudder stock (12 mm 316) | 44 (elastic) | 8.5 | 2×10⁻⁸ | negligible |

- **Cycles:** the boat rolls 540–1,240 times an hour by more than 2°. That is 1.5 to 3.4 million roll cycles in a 112-day crossing; the naval review's earlier estimate of 6 million was high.
- **Rudder hinge torque is tiny:** at most 0.1 N·m in any sea state, because the stock sits 8 mm ahead of the blade's centre of pressure. The servo works against seal and bushing friction, not the water. The printed servo arm P26 sees almost nothing in normal sailing. Its only real loads are a jammed blade or a strike, which the spring link limits. **Set the spring link to give at well under the servo's 2.5 N·m stall**, and have the firmware limit servo current if the rudder stops moving.
- **The printed bearing housing P07 and the cradles P12 and P24:** the spar's working loads (under 18 N·m at p99) put a few MPa on P07's seat, far below PETG's creep threshold of about 15 MPa. Creep isn't a concern for them. P07 and anything else above deck must still be ASA, not PETG, for the heat.
- **Tail boom:** with Hs 5 m on the beam the boat rolls 14° RMS, and the tail, 0.6 m aft at boom height, catches the water on the big rolls. That is the one place the model finds load cycles near a part's strength. How many hours a voyage spends in 5 m beam seas will set the risk; the PC run will say.
  - **Adopted 14 Nov as Rev E1:** a 16 × 14 mm carbon tube. Its section modulus is about 1.9×, so strength about 100 N·m, and the worst cycle drops to under 40% of strength, which gives effectively unlimited life. The tube adds about 12 g; the pod needs about 24 g more lead to balance (simulator mass model), so 36 g in all.
  - Field Test D (wing balance) rebalances it.

## Steering workload

**Continuous PD autopilot** (the 6-DOF model's own, rudder rate 60°/s):

| Sea | Quarter: moves/h | Quarter: travel °/h | Beam: moves/h | Beam: travel °/h |
|---|---|---|---|---|
| Hs 0.75 | 1,662 | 5,032 | 1,809 | 8,244 |
| Hs 1.5 | 1,641 | 6,338 | 4,023 | 16,137 |
| Hs 2.5 | 7,059 | 20,589 | 34,092 | 95,261 |
| Hs 3.5 | 27,297 | 82,192 | 41,307 | 122,238 |
| Hs 5 | 28,272 | 93,741 | 24,102 | 89,290 |

The rudders chase every wave. Rev E's reliability credit (servo failure rate ×0.5) assumed a steering rule that cuts this.

**Steering rules compared** (300 s each):

| Rule | Hs 1.5 quarter: moves/h, heading error | Hs 2.5 quarter | Hs 2.5 beam |
|---|---|---|---|
| Continuous | 1,608, 0.8° | 4,836, 1.4° | 26,724, 3.6° |
| **Rev E as written**: 2° deadband, a command at most every 10 s | 228, **83°**, speed 0.23 m/s | 348, **78°** | 288, **97°** |
| Heading deadband 2° only | 1,716, 1.7° | 4,560, 2.1° | 15,768, 4.1° |
| A command every 2 s only | 1,788, 10°, travel ×17 | 1,704, 14° | 1,428, 53° |
| Servo deadband 0.5–2° (move only when the command differs by more) | 3,576–9,900 | 17,832–22,728 | 36,972 |
| **Wave filter 3 s** | 1,296, 2.1° | 1,176, 3.0° | 1,116, 9.9° |
| **Wave filter 6 s** | 1,068, 2.3° | 1,032, 3.9° | 912, 14.7° (speed 0.78 against 0.95) |
| Wave filter 12 s | 864, 2.3° | 864, 4.2° | 624, **54°** |

- **Holding the rudder between commands is what breaks the course:** the yaw-rate damping goes, and the boat swings through tens of degrees between corrections. The heading deadband barely changes the count, and a servo deadband makes it worse: each held step becomes a bigger jump.
- **A low-pass filter on the inputs works.** The autopilot ignores the wave-by-wave yaw it can't correct anyway and steers the mean course.
  - 3–6 s is the useful range. 12 s is too slow on the beam.
  - At Hs 3.5 m on the quarter, 6 s held the course better than continuous steering (7.7° against 40°) at 948 moves/h.
- **Per voyage:** at about 1,000 moves/h, a 112-day crossing is about 2.7 million movements per rudder servo.

**Recommendations:**
1. **Replace the Rev E steering rule** with a wave filter on heading error and yaw rate, time constant about 4 s, to be tuned on the lake (Test I). Keep the servo powered; don't add a deadband or an update interval.
2. **Test P: run 3 million movements, not 1 million**, at one every second (about 5 weeks), to cover one crossing with margin.
3. **The simulator's servo credit:** Rev E's ×0.5 on the servo failure rate stands as a guess. The failure rates were fitted per day to boats with real autopilots, so they already include those boats' duty. Test P is what turns it into a number.

## Motions

- **Roll:** 1–3° RMS up to Hs 2.5 m on the quarter. On the beam it rises to 6° at 2.5 m, 10° at 3.5 m and 14° at 5 m.
- **Course-keeping in big quartering seas:** at Hs 3.5–5 m with the waves on the quarter the model yaws hard (heading error about 40° RMS with continuous steering). This is the classic small-boat problem running before big seas. The 6 s wave filter did better there (7.7°), which suggests some of it is the autopilot fighting the waves. Whether the real boat broaches is for the lake tests and Test F.
- **Accelerations at the CG:** under 1 m/s² RMS up to Hs 2.5 m. The electronics and battery mounts (factor 20 at 60 g) are nowhere near their limits in normal sailing.
