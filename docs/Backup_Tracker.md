# Backup tracker

*9 November 2026. Why: in the Microtransat record, going silent is the most common way a boat is lost, and 12–13% of our simulated voyages now arrive with their main radio dead ([Failure_Rates.md](Failure_Rates.md)). A second tracker with its own battery, antenna and satellite modem turns most of those from "lost" into "found". The simulator now models it directly (Nov 10, below): from the 100 km drop, verified arrivals rise from 40.5% to 54.5%, and we still know where the boat is at the end of 65.5% of voyages, against 40.5% without it.*

## Requirements

- **Fully independent of the main system:** its own battery, GPS, modem and antenna, and no wiring to the autopilot. One flooded box or one broken mast shouldn't take out both.
- **Coverage over the whole route.** Iridium covers everywhere. Globalstar's simplex network covers the North Atlantic but has historically had gaps in some mid-ocean areas, so it's a second choice for us.
- **Endurance:** at least 150 days at 2 positions a day, with margin for cold and for the cases where it can't see the sky.
- **Waterproof** (IP67 or better) and able to report from under a clear hatch, or from a sealed pocket with an external patch antenna.

## Options

| Option | Network | Power | Endurance at 2 fixes/day | Notes | Rough cost |
|---|---|---|---|---|---|
| **YB3 (Yellowbrick)** | Iridium SBD (9602) | Internal 5.3 Ah LiPo, USB charge | Rated over 2,500 transmissions per charge (~3.4 years at 2/day on paper; plan on less in the cold) | Off the shelf, IP67, used by ocean-race fleets. Pay-as-you-go airtime: month-by-month line rental plus credits (1 credit per position). 305 g | Hardware about $630 at launch (2012 price; **check current**) + line rental for ~5 months + ~300 credits (£0.05–0.12 each) |
| **Second RockBLOCK 9603 + small MCU + primary lithium cells** | Iridium SBD | 2× Saft LS33600 D-cells (17 Ah, 3.6 V) | Months to years with a duty-cycled MCU | Cheapest at scale, but it's another custom board to test. It shares a failure mode with the main build if the same code or the same flaw is reused | ~$300 hardware + Rock7 line rental and credits |
| **SmartOne Solar (Globalstar)** | Globalstar simplex | Solar + NiMH | Effectively unlimited | Rugged and fit-and-forget; boat-sim carries one. One-way only, with possible mid-ocean gaps | ~$200–300 + service plan **(check)** |

**Where it goes (Rev C3):** in a 38 mm well in the foredeck, centred 180 mm from the bow, top flush with the deck, on cradle P19. It was on the stern post in Rev C; the structural review found that one bent post would take the main antenna and the tracker together.

**Recommendation: YB3.** It's independent by design, needs no custom electronics, has global Iridium coverage, and has a long ocean-racing track record. Set it to report every 12 hours, and every 3 hours for the first week.

## Fitting

- Mount it in its own small sealed compartment under a clear polycarbonate window on the aft deck, well away from the main electronics box and the solar panel wiring. Bed the window in sealant and pressure-test it with the hull (see the leak test in [Field_Tests.md](Field_Tests.md)).
- Add foam padding and a strap, and keep it away from the bilge.
- Mass is about 0.3 kg. Rerun the stability check (`selftest` step 1) with it added at its real position.

## Tests (add to Field Test F)

1. **Bench:** 7 days reporting every hour from a window, to confirm the battery drain matches the data sheet.
2. **Wet:** 1 hour submerged at 0.5 m inside its compartment, then report.
3. **On the boat:** reports arrive during all 14 days of the coastal trial, with the main system **switched off** for 48 hours. That proves it really is independent.
4. **Inverted:** with the boat upside down for 10 minutes, note whether reports still go out. They probably won't; record it.

## In the simulator (Nov 10, 2026)

The tracker is now part of the default Rev B design (`design["backup_tracker"]`, `fitted: true`):

- It sends a fix every 3 h for the first week, then every 12 h. 95% of fixes get through, and none do while the boat is upside down. Its battery budget is 60% of the rated 2,500 transmissions, which is never the limit on a 240-day voyage.
- It dies at 0.0007/day, a flat rate with no sea-state or early-life factor (`failures["backup_tracker"]`, boat-sim #153's figure).
- **A dead main box no longer ends the voyage.** If the tracker still works, the boat drifts on at leeway (3.3% of the wind plus current), still reporting, until it washes up, gets swamped, is picked up or the run ends. Without a tracker, an electronics failure is still counted as lost.
- **New outcomes.** `arrived_tracked`: the boat sailed in with its main modem dead or hung, and the tracker logged the arrival. It counts as a success, because the crossing can be shown. `arrived_adrift`: the main box was dead and the boat washed up in Europe. That is not a sailed crossing, but the boat can be recovered.

200 voyages from the 100 km drop, planning failure rates, synthetic weather, April–July launches in 2022–2025, same seeds for both:

| | No tracker | YB3 fitted |
|---|---|---|
| **Arrived, verified** (main system reporting, or main modem dead and the tracker logged the arrival) | **40.5%** (95% CI 33.9–47.4) | **54.5%** (47.6–61.3) |
| of which: main system still reporting | 40.5% | 42.5% |
| of which: main modem dead, logged by the tracker | — | 12.0% |
| Arrived silent (nobody knows) | 8.5% | 0.5% |
| Main box dead, washed up in Europe | (counted as lost) | 8.5% |
| Lost | 49.0% | 32.5% |
| Position known at the end of the run | 40.5% | 65.5% |
| Position known at day 30 / 60 / 90 / 150 | 0.81 / 0.69 / 0.54 / 0.43 | 0.94 / 0.88 / 0.81 / 0.70 |

The no-tracker batch reproduces the earlier 100 km result exactly, which confirms the new code leaves the rest of the model unchanged. The main reporting share moves by 2 points only because the random draws diverge once the tracker is fitted; that is noise.

Of the 39 boats whose main box died with the tracker working, 17 washed up in Europe, 1 went aground elsewhere and 21 were later lost, mostly to slow leaks over months of drifting. Leaks are now the largest single cause of loss (50 of 200 runs), so the leak test in [Field_Tests.md](Field_Tests.md) is the next thing that moves the odds.

Results: `results/2026-11-10_midatlantic_montecarlo_drop100km_tracker.json` and `..._no-tracker.json`. To run without the tracker, set `backup_tracker.fitted` to false in the design.
