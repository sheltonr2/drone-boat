# Backup tracker

*9 November 2026. Why: in the Microtransat record, going silent is the most common way a boat is lost, and 12–13% of our simulated voyages now arrive with their main radio dead ([Failure_Rates.md](Failure_Rates.md)). A second tracker with its own battery, antenna and satellite modem turns most of those from "lost" into "found". In the simulator it lifts "arrived, and we know where" from about 37% to 47–49%.*

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
