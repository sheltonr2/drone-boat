@jcolter11374, thanks to you, Ravi and Priya. That was quick work on all three of your items, plus #69–#72. The dead-boat match is reassuring. Both simulators carry the boat north and then into the Chesapeake within about 9 days (your Hampton Roads at 9.6 days, our York River at 8.9). The drifter skill of 0.23 in the eddy field fits our grid result too. We'll trust averages over many launches rather than single tracks out there.

**Our half of the split is done** (sheltonr2/drone-boat@f321cd9):

- [docs/Failure_Rates.md](https://github.com/sheltonr2/drone-boat/blob/main/docs/Failure_Rates.md) is a shared hazard table. For each failure it gives the per-day rate, the multipliers, a plausible range, a quality grade (A–D) and the evidence. Sources include glider reliability data (Brito et al. 2014), Global Drifter Program death statistics, Argo, Saildrone, Lightfish and Oshen.
- [docs/Crossing_History.md](https://github.com/sheltonr2/drone-boat/blob/main/docs/Crossing_History.md) covers all 37 Microtransat attempts from 2010 to 2023, plus other autonomous crossings. The data is in [docs/data/crossing_attempts.csv](https://github.com/sheltonr2/drone-boat/blob/main/docs/data/crossing_attempts.csv), and [hazard_analysis.py](https://github.com/sheltonr2/drone-boat/blob/main/docs/data/hazard_analysis.py) reproduces every number.

What the record says (837 boat-days, exact Poisson 95% CIs):

| Phase | Mission-ending events per day | Main causes |
|---|---|---|
| Within ~150 km of land | 0.116 (0.075–0.172) | going silent, groundings, fishermen taking the boat |
| Open ocean | 0.013 (0.006–0.025) | rig/weather damage, going silent (sometimes after erratic steering), an antenna fault |

West-to-east survival in the record: 76% at day 7, 47% at day 30, 29% at day 60, 9% at day 90. Our old rates gave 57% at day 90, so we refitted. The simulator now has a `comms_silent` failure (the boat sails on but can't report), early-life failures that a shakedown reduces, and capture by fishermen out to about 150 km. Under the rates fitted to the record, our simulator matches the record's survival curve through day 60, but it's still too kind after that because it has no wear-out yet. On our route, arriving still reporting is now 37% under our planning rates and 22% under the historical ones; it was 48% before.

For boat-sim, two suggestions so our numbers stay comparable:
1. Split exposure into near-land and open-ocean phases.
2. Count a silent arrival as a failure. That's 12–13% of our runs now.

The table should drop straight into your failure model, and corrections are welcome. The cause coding in the CSV especially is a judgment call: several "went silent" entries could be flooding or a pickup.

**Real-weather drift tests for our launch.** Dead boat, 15 May of 2022–2025, 30 days of drift. From 25 km off Ocean City, 3 of 4 went ashore within 2–5 days. From 100 km off, all 4 were carried east toward the Gulf Stream. From the shelf edge (150 km), 3 of 4 were, and one went ashore at Cape May. We've moved our drop to 100 km ([table](https://github.com/sheltonr2/drone-boat/blob/main/docs/Route_MidAtlantic.md)).

**Hurricanes.** Yes, we'll take the second half: how often a storm passes within a given radius of the boat, by launch month, from HURDAT2/IBTrACS along both routes. Your ERA5 numbers matter to us as well, since our real-weather runs use ERA5 winds. At roughly half the real wind in Cat 3–5 storms, we'd like to pair the frequency model with your wind correction rather than build our own.

**Pace.** We'd like to speed things up on both sides from here. John has authorized additional resources if needed to speed up progress, so tell us where more hands or compute would help most.

Randolph (drafted with Claude)
