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

## The gaps, in the order I would close them

| # | Analysis | Why it matters | Cost | State |
|---|---|---|---|---|
| 1 | **Hazards the map doesn't hold**: Diamond Shoals now; the Cornwall landfall next | Half the inlet tracks crossed a shoal | PC, 1.5 h | **Running (014)** |
| 2 | **New baseline: Rev E on the new route** | Every earlier number is Rev D or the old route | PC, 30 min | **Running (013)** |
| 3 | **Slower boat than predicted**: every sailing speed ×0.9 and ×0.8 | The speed prediction has never been checked against water (Test A). Arriving boats average only about 1.4 kn over the ground and take a median 114 days, with currents doing part of the work. If the boat is 20% slower through the water, does it still arrive before the autumn gales? | PC, 1 h | **Running (013)** |
| 4 | **Fatigue and creep** of every load path over a voyage: fin root, spar at the bearings, rudder stocks, tail boom, mast bearings, and the printed parts (P07 bearing housing, P12 cradles, P24) | A crossing is about 6 million roll cycles. Both structural notes list fatigue as "not modelled". Printed PETG also creeps under steady load in the sun | Sandbox, half a day | Proposed |
| 5 | **Flooded stability**: GZ curve with 1.5 kg and 3 L in the sump (free surface), pump dead, at Rev E weights | The new leak response keeps sailing with water aboard. Check it still self-rights and what heel it sails at | Sandbox, 1–2 h | Proposed |
| 6 | **Steering workload**: rudder movements per day in a seaway, with and without the 2° deadband | Servos are the top hardware loss. This says whether Test P's 1 million movements is one voyage or five | Sandbox, half a day | Proposed |
| 7 | **Dead-boat drift from the new drop point** | The Ocean City launch rules came from drift tests. From the Stream a dead boat should be carried out to sea; check, and find the wind rule for Hatteras | PC, 30 min | Proposed |
| 8 | **Roll and pitch periods against the waves it will meet** | Resonance drives wing slap, servo work and knockdowns; the knockdown count (660 a voyage) is itself a model | Sandbox, half a day | Proposed |
| 9 | **More weather years** (2021, 2022) and **April launches** | Two years is a thin sample for a go/no-go | PC download, about a day per year; needs Randolph's OK | Proposed |
| 10 | **Ship-strike risk from real traffic density**, mostly at the Cornwall end | The model's ship-strike rate is one number for the whole ocean | Needs a traffic-density dataset; needs Randolph's OK to download | Proposed |

## What no simulation will settle

- **The wing spar in breakers** (Tests L and M).
- **Servo life** (Test P) and **the tail detent** (Test Q).
- **Boat speed** (Test A, tow drag) and **real fouling** (Test F).
- **Fishing-boat pick-ups**, now the largest single loss in the model. The rate is a guess from other people's boats.

A simulation can rank designs and find blind spots, as it did today. It can't replace those five tests.

## Sources

- Diamond Shoals: <https://en.wikipedia.org/wiki/Diamond_Shoals>, <https://www.dncr.nc.gov/blog/2023/12/05/diamond-shoals-b-41>, <https://www.lighthousefriends.com/light.asp?ID=1690>
