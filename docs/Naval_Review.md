# A naval engineer's review: what else to simulate

13 November 2026. Randolph asked what further simulations are worth running, hull stress among them, from a naval engineer's point of view. This note says what is already covered, where the gaps are, and what is running. Grade D throughout: models and handbook numbers, nothing tested on the boat yet.

## Short answer

- **Hull stress is the least useful thing to simulate.** At 1.5 m the foam-filled hull is the strongest part of the boat: the hull girder has a factor of 13 in a bottom slam and the panels 2.2 to 4.8 ([Structural_Review.md](Structural_Review.md)). Loads grow with size faster than strength does, so small hulls are overbuilt by nature. A finite-element run would confirm a margin we already have.
- **The boat fails at its attachments and its moving parts, and at the edges of the map.** The useful work is on fatigue, flooded stability, steering workload, how far the conclusions lean on an unvalidated speed prediction, and hazards the simulator's map doesn't hold.
- **The first check found a real problem the same afternoon:** Diamond Shoals, below.

## Found today: Diamond Shoals

The launch study recommended a drop 10 km off Hatteras Inlet. The simulator's coastline (Natural Earth) has no shoals. Diamond Shoals run 13–22 km south-east from Cape Hatteras with as little as 1 m over them and breakers in any sea, and the Gulf Stream sets north-east straight across them from the inlet.

`docs/data/diamond_shoals_check.py`, on the saved stage C tracks (a point every 0.6–0.8 days, interpolated, shoal position approximate):

| Launch | Tracks passing within 2 km of the shoal line | within 5 km | within 10 km |
|---|---|---|---|
| Hatteras Inlet, 10 km (500 voyages) | **52%** | 64% | 81% |
| Hatteras charter, 45 km (150 voyages, stage B) | 0% | 0% | 0% |

So about half the "successful" inlet launches sailed over a shoal that would probably have rolled and broken the boat. The 45 km charter point tied with the inlet on success in stage B (+0.0, −7.8 to +8.0), so it is the provisional drop point ([Launch_Plan.md](Launch_Plan.md)).

**Results (13 Nov evening), Rev E, 500 voyages each, 2023 and 2024, to Cornwall** (`docs/data/plan_runs_analysis.py`). The shoal distances below are recorded by the simulator at its own 5-minute step, so they replace the rough track check above:

| Drop | Success | Within 2 / 5 / 10 km of the shoals | vs the inlet, paired |
|---|---|---|---|
| Inlet, 10 km (closest approaches from the ×0.9 run, same drop) | 83.4% | 22% / 49% / 74% | — |
| Inlet with a dog-leg south-east first | 84.8% | 7% / 12% / 36% | +1.4 (−2.6 to +5.6) |
| **45 km, on the Stream's inshore edge** | **87.6%** | **0 / 0 / 0** | **+4.2 (+0.0 to +8.4)** |
| 70 km, east of the shoals | 86.8% | 0 / 0 / 0 | +3.4 (−0.4 to +7.4) |

- **The dog-leg doesn't clear the shoals.** The Stream sets the boat north-east faster than it can sail out.
- **The inlet's 83.4% is itself too high.** In the ×0.9 run, 110 of 500 voyages passed within 2 km of the shoal line and 83% of those "arrived". Counting them as lost would take that run from 82.8% to 64.6%.
- **45 km and 70 km tie** (70 against 45: −0.8, −4.6 to +3.0). The recommended drop is 45 km: a shorter run out. 70 km is the safer choice for a boat that dies on the first day (dead-boat drift, below).

**Dead-boat drift from the new drop points** (item 7; `collab/drift_tests.py --set hatteras`, 32 drops each, 1 May–15 June 2023 and 2024, 30 days, three leeway factors):

| Drop | Aground within 30 days (2% / 3.3% / 5% leeway) | Passed within 5 km of the shoals |
|---|---|---|
| Inlet, 10 km | 15 / 14 / 17 of 32 (most within 4 days) | 13–14 of 32 |
| 45 km | 2 / 3 / 8 of 32 | 1–3 of 32 |
| 70 km | 0 / 1 / 3 of 32 | 0–2 of 32 |

Four of the 45 km groundings come within two days, back on Hatteras Island. A dead boat in the model drifts downwind plus the current, so to get ashore that fast against the Stream the wind must have been onshore. A launch rule of no wind from the east or south-east for 72 hours targets them ([Launch_Plan.md](Launch_Plan.md)). The rest ground after one to four weeks, on the Outer Banks again or carried north to New Jersey and New England.

**Changes and runs:**
- The simulator now takes `watch_lines` in a scenario and reports each voyage's closest approach, at its own 5-minute step. It does not change the voyage.
- Queued on the PC (request 014, Rev E, 500 voyages each, 2023 and 2024, to Cornwall): the 45 km point; a point 70 km out and east of the shoals; and the inlet with a dog-leg south-east first, to see whether a cheap beach launch can be made to clear them.
- **Lesson:** a launch or landfall point needs a look at the chart, not only at the simulator's coastline. The same check is owed at the Cornwall end (Seven Stones, the Western Rocks, the tidal streams and the shipping lanes off Land's End).

## What is already covered

| Question | Where | State |
|---|---|---|
| Hull, deck, hatch, keel bolts, battery mounts under slam and strike loads | Structural_Review.md | Pass with margin |
| Keel fin and joint in knockdowns | Keel_Structure_Loads.md, Test K | Strengthened in C2; proof test defined |
| Wing spar, stern post, counterweight arm, rudder servos in breaking-wave strikes | Structural_Review.md (`strike_sim.py`) | Fixed in C3; **the spar can't be settled by simulation** (Tests L, M) |
| Intact stability and self-righting | GZ curves, Test C | GM 0.18 m, self-righting on paper |
| Storm exposure | Hurricane_Risk.md | Counted on real tracks; loss model is a guess |
| Biofouling, weed, leaks, electronics, servos | Failure_Rates.md, Reliability_Review.md | In the voyage model; rates are Grade D |

## Rev E on the new route, and a slower boat (items 2 and 3)

| Run (Hatteras Inlet → Cornwall, 500 voyages) | Success | Median days | Paired |
|---|---|---|---|
| Rev D | 68.4% | 114 | — |
| **Rev E** | **83.4%** | 112 | **+15.0 (+10.2 to +19.4) over Rev D** |
| Rev E, every sailing speed ×0.9 | 82.8% | 122 | −0.6 (−4.6 to +3.4) |
| Rev E, every sailing speed ×0.8 | 78.4% | 132 | −5.0 (−9.0 to −0.8) |

- **The plan barely depends on the speed prediction.** A boat 10% slower than the model loses nothing measurable. One 20% slower loses 5 points and takes three weeks longer, mostly by still being at sea when the season ends (11% against 6%).
- The current does a large share of the work on this route. Test A (tow drag) still matters for the other numbers, but not for this go/no-go.

## Further results (13 Nov evening)

- **Flooded stability** (item 5): fine, but the sump holds only 1.2 L, less than Rev E's 1.5 kg SAFE limit ([Flooded_Stability.md](Flooded_Stability.md)).
- **Fatigue, steering workload, motions** (items 4, 6 and 8): see [Fatigue_Review.md](Fatigue_Review.md).
  - No fatigue concern except the tail boom in big beam seas.
  - The Rev E steering rule as written lost the course in the 6-DOF model; it is replaced by a wave filter.
  - A crossing is about 2.7 million servo movements, so Test P becomes 3 million.
- **More weather years** (item 9): downloading on the PC since 13 Nov 19:33 (April 2021–2024 and May–November 2021–2022, 245 GB free).

## Decisions and next runs (14 Nov 2026)

Randolph decided on 14 Nov: **drop 45 km off Hatteras**, **leak SAFE limit 1.0 kg**, **16 × 14 tail boom**. Drawn as Rev E1 ([Design_RevE.md](Design_RevE.md)).

**Found while planning:** the Copernicus wave forecast archive starts in November 2022, so 2021 and 2022 waves failed in the download. The downloader now takes months before November 2022 from the WAVERYS reanalysis (same variables, 0.2° grid instead of 1/12°).

PC queue, in order. Times are estimates. The weather download's ERA5 lane has run between 20 minutes and 2 hours per month, so it holds everything behind it.

| # | What | Why | Expected |
|---|---|---|---|
| 016 | Weather download: April 2021–24, May–Nov 2021–22 (running since 13 Nov 19:33) | More years and April launches | ERA5 done Saturday afternoon to Sunday morning |
| 015c | Sea states along the Rev E 45 km tracks | Hours per voyage by wave height: turns the fatigue bounds into voyage totals | +15 min |
| 017 | Rev E1 from 45 km to Cornwall, 2023–24, 500 voyages, same seeds | New baseline, and the first record of approaches to the Seven Stones and Scilly | +30 min |
| 018 | Download 2021–22 waves from WAVERYS | Waves for the older years | +about 1 h |
| 019a–c | Rev E1 from 45 km, 2021–24 weather, 500 voyages each: launches 1–20 May, April, 21 May–15 June | Four weather years, and the launch window | +1.5 h |

All results: Saturday evening to Sunday midday.

## The gaps, in the order I would close them

| # | Analysis | Why it matters | Cost | State |
|---|---|---|---|---|
| 1 | **Hazards the map doesn't hold**: Diamond Shoals now; the Cornwall landfall next | Half the inlet tracks crossed a shoal | PC, 1.5 h | **Done** for Hatteras (above); Cornwall end still to check |
| 2 | **New baseline: Rev E on the new route** | Every earlier number is Rev D or the old route | PC, 30 min | **Done**: 83.4% (inlet), 87.6% (45 km) |
| 3 | **Slower boat than predicted**: every sailing speed ×0.9 and ×0.8 | The speed prediction has never been checked against water (Test A). Arriving boats average only about 1.4 kn over the ground and take a median 114 days, with currents doing part of the work. If the boat is 20% slower through the water, does it still arrive before the autumn gales? | PC, 1 h | **Done**: ×0.9 no change, ×0.8 −5 points |
| 4 | **Fatigue and creep** of every load path over a voyage | 1.5–3.4 million roll cycles a crossing (6 million was my first guess, too high) | Sandbox | **Done** ([Fatigue_Review.md](Fatigue_Review.md)); sea-state hours from the PC to follow |
| 5 | **Flooded stability**: GZ curve with 1.5 kg and 3 L in the sump (free surface), pump dead, at Rev E weights | The new leak response keeps sailing with water aboard. Check it still self-rights and what heel it sails at | Sandbox | **Done** ([Flooded_Stability.md](Flooded_Stability.md)) |
| 6 | **Steering workload**: rudder movements per day in a seaway, with and without the 2° deadband | Servos are the top hardware loss. This says whether Test P's 1 million movements is one voyage or five | Sandbox | **Done** ([Fatigue_Review.md](Fatigue_Review.md)) |
| 7 | **Dead-boat drift from the new drop point** | The Ocean City launch rules came from drift tests. From the Stream a dead boat should be carried out to sea; check, and find the wind rule for Hatteras | PC, 12 min | **Done** (above) |
| 8 | **Roll and pitch periods against the waves it will meet** | Resonance drives wing slap, servo work and knockdowns; the knockdown count (660 a voyage) is itself a model | Sandbox | **Done** with item 4 |
| 9 | **More weather years** (2021, 2022) and **April launches** | Two years is a thin sample for a go/no-go | PC download, about a day per year | **Downloading** (approved 13 Nov) |
| 10 | **Ship-strike risk from real traffic density**, mostly at the Cornwall end | The model's ship-strike rate is one number for the whole ocean | Needs a traffic-density dataset; needs Randolph's OK to download | Proposed |

## What no simulation will settle

- **The wing spar in breakers** (Tests L and M).
- **Servo life** (Test P) and **the tail detent** (Test Q).
- **Boat speed** (Test A, tow drag) and **real fouling** (Test F).
- **Fishing-boat pick-ups**, now the largest single loss in the model. The rate is a guess from other people's boats.

A simulation can rank designs and find blind spots, as it did today. It can't replace those five tests.

## Sources

- Diamond Shoals: <https://en.wikipedia.org/wiki/Diamond_Shoals>, <https://www.dncr.nc.gov/blog/2023/12/05/diamond-shoals-b-41>, <https://www.lighthousefriends.com/light.asp?ID=1690>
