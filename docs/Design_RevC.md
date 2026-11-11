# Rev C design changes and rationale

*10 November 2026. Proposed after the first real-weather Monte Carlo and approved by Randolph the same day. The drawings, templates and printed parts in `build-files/` are now Rev C. Rev B stays available in the simulator as `default_design("revB")` and `designs/revB_design.json`.*

## What drove it

The first Monte Carlo on downloaded real weather (250 voyages, 1 May–15 June 2023 launches, ERA5 winds, Copernicus currents and waves; [Failure_Rates.md §4.5](Failure_Rates.md)) showed which failures actually hit a voyage:

| Failure | Share of voyages it hit | What it led to |
|---|---|---|
| Wing damaged in a knockdown | 56% | The boat drifts |
| Leak started | 39% | Swamped in 84 of 250 voyages, the largest single cause of loss |
| Electronics failure | 29% | Box dead; with the YB3 the boat drifts on, tracked |
| Rudder servo failure | 25% | No steering: the boat drifts |
| Tail servo failure | 20% | The wing is stuck or feathers |
| Capsize (stays inverted) | 0% | The boat rights itself every time |

The wing and leak rates were then refitted (they had been tuned on calm synthetic seas), but the shape of the problem stays: leaks, the rig and single-servo steering.

## Changes

| # | Change | Why | Evidence |
|---|---|---|---|
| 1 | **Foam-filled hull behind two glassed-in bulkheads (x 300 and x 1260); the battery in its own sealed box.** The bow and stern spaces are solid foam. Fitted, removable blocks fill the dry bay around the boxes, leaving 3 L or less of open space. | A leak can add at most about 3 kg of water (12% of displacement), so it can no longer swamp the boat. Water that does get in still wets the electronics (the ×6 electronics hazard stays). | Leaks were the top cause of loss. The build plan always called for foam-filled compartments; Rev B's drawings didn't have them. |
| 2 | **Twin rudders,** 100 mm either side of the centreline, each with its own trunk, servo, tiller and cable. | Either rudder steers alone, so one servo failure no longer ends the voyage. The leeward rudder also sits deeper when heeled. | One rudder servo was a single point of failure in a quarter of voyages. |
| 3 | **Wing spar 30 × 26 mm carbon on 6806-2RS bearings** (was 25 × 22 mm on 6805). | About 1.8× the bending strength, for about 110 g. | Real seas knock the boat down about 3.5 times a day. The 25 mm spar is marginal for the wing slapping the water and fails in an 8 m/s breaking crest ([Storm_Loads.md](Storm_Loads.md)). |
| 4 | **Bulb D72 (was D68), about 9.2 kg.** | Holds the stability margin at the higher mass. | Simulator stability check. |
| 5 | **YB3 platform (P19) and all-round white light (P20) on the stern post; label areas on the hull and wing.** | Already decided (backup tracker 9 Nov, light and labels in the launch plan) but not yet on the drawings. | [Backup_Tracker.md](Backup_Tracker.md), [Launch_Plan.md](Launch_Plan.md). |
| – | **Removed: thruster provision and the backup D-cell.** | The thruster was optional, never used in the simulations and one more fitting. The YB3 covers the D-cell's job of reporting if the main power dies. | |

## Considered and not adopted

- **Outer pontoons (outriggers).** They would cut down knockdowns, but a boat with outriggers that does go over tends to stay upside down. That would swap a frequent, survivable event (no capsizes in 250 voyages) for a rare, fatal one. The struts would also take breaking-wave loads like the ones that break the wing, and each joint is another leak path.
- **A longer hull (1.8–2.0 m).** In the knockdown model, the critical breaker height scales with length, so a longer boat is hit far less often. But it means a full redraw, a bigger build and harder handling. It's a Rev D candidate if rig losses still dominate after the refit.
- **A backup tail servo.** It's worth doing, but it adds complexity inside the rotating wing (slip-ring wiring). The decision waits for more real-weather results.

## Effect on the boat (simulator, `designs/revC_geometry.json`)

| | Rev B | Rev C |
|---|---|---|
| All-up mass | 20.8 kg | 25.2 kg (26.4 kg from Rev C2) |
| Waterline (z above the hull bottom) | 88 mm | 98 mm (101 mm from Rev C2) |
| GM | 0.201 m | 0.187 m |
| Maximum righting arm | 0.434 m at 105° | 0.378 m at 105° |
| Self-righting from 180° | yes | yes |
| Lead | 8.0 kg bulb + 0.8 kg counterweight | 9.0 kg bulb + 0.8 kg counterweight |
| Speed (VPP, average over 5–12 m/s winds) | 1.00 | 0.93: −5% from the weight, −2% from the second rudder |
| Hardware cost | about $2,010 (Build Plan basis) | about $2,270, plus about $630 for the YB3 |

**Correction (10 Nov):** when proposing Rev C I estimated it would cost about $300 less. That was wrong. The thruster was never in the sail-only budget, so removing it saves nothing there. Rev C adds about $260 of parts, and the YB3 (decided 9 Nov) wasn't in the budget either.

## Real-weather result (10 Nov 2026, evening)

250 voyages each on 2023 weather (1 May–15 June launches, refitted rates, same seeds; [log](../collab/run_log_revC_compare_2023_2026-11-10.txt), data in `results/2026-11-10_bulk_mc_2023_rev*_refit.json`).

| | Rev C, near-coast (the plan) | Rev B, near-coast | Rev C, 100 km drop |
|---|---|---|---|
| **Verified arrivals** (95% CI) | **38.8%** (33–45) | 41.2% (35–47) | 44.8% (39–51) |
| Lost | 18.8% | 25.6% | 13.2% |
| Position known at the end | 77.6% | 73.2% | 84.4% |
| Swamped by a leak | 0 | 31 | 0 |
| Steering lost (both rudders, or the one) | 19 | 62 | 16 |
| Wing broken | 95 | 76 | 113 |
| Electronics failure | 82 | 64 | 103 |
| Aground near the US coast | 11 (4.4%) | 11 (4.4%) | 2 (0.8%) |
| Still at sea when the data ended (30 Nov) | 20.4% | 17.6% | 26.4% |
| Median crossing | 133 days | 127 days | 131 days |

What it says:

- **Rev C does what it was designed to do, but that has not yet turned into more arrivals.** No boat was swamped (31 before) and steering losses fell from 62 to 19. Losses fell from 25.6% to 18.8% and we know where more boats are at the end. Verified arrivals are level with Rev B (38.8% against 41.2%, well inside the ±6-point noise).
- **Why not more arrivals: the boats Rev C saves then fail another way.** A leaking Rev C boat stays afloat, but the water stays in the dry bay, the electronics hazard stays at ×6, and the main box dies (82 electronics failures against 64). Boats also live longer and so meet more knockdowns (95 broken wings against 76). And Rev C is about 7% slower, so more voyages run past the end of the 2023 data. Of the 51 Rev C boats still at sea on 30 Nov, 33 had a dead main box and 33 a broken wing; only 6 were still sailing normally.
- **The next two levers are clear: keep trapped water away from the electronics, and the wing.** Mounting the IP68 box above the 3 L flood level (or adding a small bilge pump) would stop a leak from becoming an electronics failure. The wing needs either the severity-scaled damage model checked against the 30 mm spar, or a storm-stowed rig.
- **Launch point: near-coast costs more than estimated earlier.** Groundings near the US coast were 11 of 250 from the near-coast point against 2 of 250 from 100 km, and verified arrivals were 38.8% against 44.8% (a 6-point gap, at the edge of the noise). The earlier "about 1%" figure was wrong: it came from the 100 km run. Most of these groundings were boats whose electronics died in the first weeks (5 of 11 within 14 days). The simulator does not model the launch plan's offshore-wind rule, escort or early recovery, which are aimed at exactly these cases, so the real cost should be smaller than 6 points, but it is not zero.
- **Knockdowns by wave height** (new log): 4% happen below Hs 3 m, 60% between 3 and 6 m, 35% above 6 m. The mean (Hs/3)² at a knockdown is 3.6 (boat-sim measured 2.9 on its model), so our flat 0.0009 per knockdown equals about 0.00025 at Hs 3 m in the scaled form.

### Two-year run (11 Nov 2026)

500 voyages of Rev C (as first drawn) from the near-coast launch, 1 May–15 June launches in 2023 and 2024 ([log](../collab/run_log_bulk_2026-11-11.txt), `results/2026-11-11_bulk_mc_2023-2024_revC_10km.json`):

| | Both years | 2023 | 2024 |
|---|---|---|---|
| **Verified arrivals** | **41.0%** (95% CI 36.8–45.4) | 43.2% | 38.8% |
| Lost | 15.4% | 16.4% | 14.4% |
| Position known at the end | 81.6% | 80.4% | 82.8% |
| Aground near the US coast | 8 of 500 (1.6%) | 7 | 1 |
| Still at sea when the data ended (30 Nov) | 30.4% | 21.2% | 39.6% |
| Knockdowns a day | 4.0 | 4.45 | 3.53 |

- **41% is the best current estimate for Rev C from the near-coast launch.** The 2023 half of this run gave 43.2% where the 250-voyage run the night before gave 38.8% for the same boat and launch point (different launch dates and random draws). That 4-point spread is the noise level, so the Rev B / Rev C / launch-point differences in the table above are not resolved by 250 voyages.
- **Groundings near the US coast were 1.6% over the two years** (7 in 2023, 1 in 2024), lower than the 4.4% in the 250-voyage run. The cost of the near-coast launch is real but looks nearer 2–4 points than 6, and it depends on the year.
- **Three in ten boats were still at sea on 30 Nov,** but only 18 of those 152 were still sailing normally; the rest had a dead main box or a broken wing and were drifting, most of them between 13°W and 38°W. Counting the 18 as likely arrivals would add at most 3.6 points. Downloading December would settle it.
- **Launch date:** in both years the first half of May did worst (36% and 33%) and 16–31 May best (49% and 42%), with June in between. With about 85 voyages per bin that is suggestive, not proven, and it is the opposite of the first (pre-refit) run. The 1–20 May window stands for now on hurricane grounds.
- **Bulk data check:** the same no-failure voyage took 112.7 days on the bulk data and 117.6 days on Open-Meteo, so the two weather sources agree to about 4%.

## Rev C1: electronics box above the flood level (11 Nov 2026)

The comparison above showed that a leak in Rev C no longer sinks the boat but still kills the main electronics, because the trapped water sits in the same bay as the box. C1 separates them:

- **The box moves up onto a glassed foam shelf,** bottom at z 118 mm (was 60), still under the deck with 11 mm to spare.
- **The 3 L of open space becomes one sump** at the low point of the dry bay (x 560–770, below z 45). Everything above it is foam. Water stays about 70 mm below the shelf upright and at 30° of heel. The leak probe sits in the sump.
- **Cable glands go on the top of the box,** with drip loops, gel-filled connectors and desiccant inside.
- **Effect on the boat:** +0.08 kg (shelf), CG 3 mm higher, GM 0.184 m (was 0.187), still self-righting. No new printed parts.
- **In the simulator:** water in the bay now multiplies the electronics hazard by `hull.wet_electronics_factor` = 2 for C1 (it was 6 for Rev B and Rev C). **The 2 is a guess.** In a knockdown the water still splashes the box briefly, and humid air still reaches the connectors. Field Test J (below in [Field_Tests.md](Field_Tests.md)) is what would justify it.
- **Measured (11 Nov, 250 voyages, 2023 weather, near-coast launch; log in `collab/run_log_revC1_compare_2023_2026-11-11.txt`):**

| | Rev C as first drawn | Rev C1 |
|---|---|---|
| Verified arrivals | 38.8% (33.0–45.0) | **45.6% (39.5–51.8)** |
| Arrived still reporting | 29.6% | 36.0% |
| Lost | 18.8% | 18.0% |
| Position known at the end | 77.6% | 81.2% |
| Electronics failures | 37 | 31 |
| Wing damaged in a knockdown | 38 | 28 |

  C1 came out 7 points higher, but the two ranges overlap, and wing damage (which C1 does not touch) fell by as much as electronics failures did. So most of the gap is chance. The fair reading is that C1 helps by a few points at most, and that the `wet_electronics_factor` of 2 is still a guess. `designs/revC0_design.json` is Rev C as first drawn, for reference.

## Rev C2: keel fin rebuilt after a strength check (11 Nov 2026)

A physics estimate ([Keel_Structure_Loads.md](Keel_Structure_Loads.md)) found the fin as drawn was only about 3 times as strong as the load of the bulb with the boat on its side, and would break in the first breaking seas. C2 changes the fin and its joint to the hull. The outside shape is unchanged.

- **Fin core is solid hardwood** (white oak, ash or sapele) in two halves glued round the two M10 rods, instead of foam.
- **Skin is 6 × 6 oz glass each side** (was 3), over a 60 × 1.5 mm unidirectional carbon strip let into each face.
- **The fin has a 60 mm tenon** that stands in a socket (the keel box) cast round it inside the hull. Before, only the two rods on the centreline crossed the joint.
- **Two 9 mm plywood floors** cross the hull at x 650 and x 800 (templates T19, T20), with three extra plies inside the hull bottom between them, to spread the keel load into the hull.
- **Estimated strength:** fin about 1,100 N·m at the root (was 113), joint about 700 N·m, against 36 N·m static and about 350 N·m for a 1-in-1,000 wave strike. All hand calculations.
- **Proof test:** Field Test K (60 kg hung from the bulb with the boat on its side) before paint.
- **Effect on the boat:** +1.1 kg, so 26.4 kg all-up, waterline z 101 mm (was 98), GM 0.190 m (was 0.184), maximum righting arm 0.37 m at 105°, still self-righting. The speed model has not been rerun for the extra weight; expect about 1% slower.
- **Sheets and templates changed:** D00, D03, D04 (redrawn), T12, T13 (now planing gauges), new T19 and T20. No printed part changed.
- **In the simulator:** masses only (`keel.core_density`, `keel.kg_per_m2_skin`, keel box item). There is still no keel-loss event; see the note for the options.

## Rev C3: changes from the structural review (11 Nov 2026)

A breaking-wave strike simulation ([Structural_Review.md](Structural_Review.md)) found four weak parts above the deck. Randolph approved all five recommended changes.

| Change | Why | Drawing / part |
|---|---|---|
| **YB3 backup tracker moves to a well in the foredeck** (centred at x 180, top flush with the deck); the stern post becomes a 20 × 2 mm fibreglass tube | The post carried the main antenna and the backup tracker, and the model bent it on most voyages. One bent post silenced both. A fibreglass tube bends instead of kinking | D01, D07; P19 is now a deck cradle |
| **Counterweight arm is a 12 mm solid fibreglass rod** (was a 12 × 10 carbon tube) | A drop of 46 cm onto the water broke the carbon tube. The rod takes about six times the shock energy in the same sockets | D06 |
| **Spring servo-saver on each rudder servo, and stop blocks at ±40°** | A wave strike pushes the blade round with up to four times the servo's stall torque | D05 |
| **Wing spar 30 × 22 mm** (was 30 × 26), bearings 130 mm apart in a longer housing P07 (was 78), spar 1,195 long | 1.6 times the bending strength with the same bearings and bores. The wider spacing keeps the printed housing from becoming the weak link | D06, D07; P07 |
| **Second inner ply over the sump** | The only hull panel with no foam behind it | D03 |

- **Why a well for the YB3:** the tail boom sweeps over the whole deck 40 mm up (underside z 270), so a tracker standing on the deck would be hit. The aft deck beyond the sweep is under the solar panels. A 38 mm well in the solid bow foam puts the tracker's top flush with the deck, with scupper slots to drain it.
- **Effect on the boat:** 26.9 kg (was 26.4), waterline z 102 mm, GM 0.182 m (was 0.190; the heavier spar is high up), maximum righting arm 0.36 m, still self-righting. The centre of gravity moves 24 mm forward.
- **Printed parts changed:** P07 (longer) and P19 (new shape). All other STL files are unchanged.
- **In the simulator:** the masses, and a new structural-failure model, described below.

### The structural-failure model in the simulator

At every knockdown the simulator now rolls for each of these, using chances per knockdown by wave height from the strike simulation (`simulator/drone_sim/structure_tables.json`):

| Break | What happens in the voyage |
|---|---|
| Keel fin or its joint | Boat capsizes and is lost |
| Stern post | Main antenna lost: the boat sails on silent. On Rev C2 the backup tracker goes too |
| Counterweight arm | Wing unbalanced: drifting |
| Tail boom | Wing feathers: drifting |
| Rudder servo or stock | That rudder is lost; the other still steers |
| Wing spar | Keeps its calibrated rate (0.0009 per knockdown, planning rates). For C3 that rate is multiplied by the C3-to-C2 ratio from the strike simulation |

- **Which breaker assumptions:** the "gentle" set, because it is the one that reproduces the wing-loss rate the simulator was already calibrated to. `"breakers": "central"` in the design file selects the harsher set.
- **Older designs are untouched:** design files saved before C3 load with the model off, so earlier results still reproduce. `designs/revC2_structure_design.json` is Rev C2 with the model on, for a like-for-like comparison.
- **Caution on reading it:** the simulator's servo, comms and wing rates were fitted to the historical record, which already includes some of these breakages. With the model on, Rev C2 is therefore counted somewhat twice and looks worse than its earlier runs. The fair comparison is C3 against C2 with the model on for both.

## Files

- **Drawings and build files:** `build-files/Drawings.pdf` (20 sheets; new D09 for subdivision, foam fill, battery box and labels), `Templates_1to1_Letter.pdf` (new T17 and T18 bulkheads; T15 spar bore 30.4 mm), 19 DXF files, and 23 STL files for 20 printed parts (P07 and P08 for the 30 mm spar, P14 for the D72 bulb, new P19 and P20; print two each of P11, P12 and P13).
- **Our simulator:** Rev C is the default (`default_design()`); `designs/revC_design.json` and `designs/revB_design.json`. New design keys: `rudder.y_offsets` (twin rudders) and `hull.flood_limit_kg` (bounded flooding).
- **John's boat-sim:** `designs/boat-sim/randolph_rev_c.yaml`, in the same schema as boat-sim's own `randolph_rev_b.yaml`; the keys were checked against that file and against `HazardParams`.
- **Neutral geometry:** `designs/revC_boat_wing_feathered.stl` (whole boat, metres) and `designs/revC_geometry.json` (mass items, CG, inertia, stability, reference areas). The GZ curve is in `docs/data/revC_gz_curve.csv`.
- **Real-weather comparison:** `simulator/run_revC_compare_2023.bat` (Rev C near-coast, Rev B near-coast, Rev C at 100 km; 250 voyages each, same seeds).
