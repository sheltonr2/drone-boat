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
| All-up mass | 20.8 kg | 25.2 kg |
| Waterline (z above the hull bottom) | 88 mm | 98 mm |
| GM | 0.201 m | 0.187 m |
| Maximum righting arm | 0.434 m at 105° | 0.378 m at 105° |
| Self-righting from 180° | yes | yes |
| Lead | 8.0 kg bulb + 0.8 kg counterweight | 9.0 kg bulb + 0.8 kg counterweight |
| Speed (VPP, average over 5–12 m/s winds) | 1.00 | 0.93: −5% from the weight, −2% from the second rudder |
| Hardware cost | about $2,010 (Build Plan basis) | about $2,270, plus about $630 for the YB3 |

**Correction (10 Nov):** when proposing Rev C I estimated it would cost about $300 less. That was wrong. The thruster was never in the sail-only budget, so removing it saves nothing there. Rev C adds about $260 of parts, and the YB3 (decided 9 Nov) wasn't in the budget either.

## Files

- **Drawings and build files:** `build-files/Drawings.pdf` (20 sheets; new D09 for subdivision, foam fill, battery box and labels), `Templates_1to1_Letter.pdf` (new T17 and T18 bulkheads; T15 spar bore 30.4 mm), 19 DXF files, and 23 STL files for 20 printed parts (P07 and P08 for the 30 mm spar, P14 for the D72 bulb, new P19 and P20; print two each of P11, P12 and P13).
- **Our simulator:** Rev C is the default (`default_design()`); `designs/revC_design.json` and `designs/revB_design.json`. New design keys: `rudder.y_offsets` (twin rudders) and `hull.flood_limit_kg` (bounded flooding).
- **John's boat-sim:** `designs/boat-sim/randolph_rev_c.yaml`, in the same schema as boat-sim's own `randolph_rev_b.yaml`; the keys were checked against that file and against `HazardParams`.
- **Neutral geometry:** `designs/revC_boat_wing_feathered.stl` (whole boat, metres) and `designs/revC_geometry.json` (mass items, CG, inertia, stability, reference areas). The GZ curve is in `docs/data/revC_gz_curve.csv`.
- **Real-weather comparison:** `simulator/run_revC_compare_2023.bat` (Rev C near-coast, Rev B near-coast, Rev C at 100 km; 250 voyages each, same seeds).
