# Mid-Atlantic route study

Nov 8, 2026

The launch moves from Newfoundland to the US Mid-Atlantic coast. The best target is **south-west Ireland**, with any European landfall counting. It is the quickest target in the simulator (about 100 days from Ocean City, Maryland), and it avoids the heavy shipping around Brittany and Cornwall. The crossing is about 5,400 km instead of 3,000 and takes about 20 days longer than from Newfoundland. The simulated odds are about the same (51% vs 47.5%), but hurricane season is now a real risk, and the simulator doesn't model it.

All numbers come from the simulator's **synthetic (invented) weather**, because historic data couldn't be downloaded from the build environment. Use them to compare routes, not as forecasts. The invented weather includes a Gulf Stream, travelling lows and seasonal westerlies, but **no hurricanes**.

## Route

- **Launch:** about **100 km (54 nm) off Ocean City, Maryland (38.02°N, 74.01°W)**, dropped from a charter boat. This changed on 8 Nov 2026 after the drift tests below: 3 of 4 boats dropped 25 km out drifted ashore within 2–5 days. Ocean City's offshore canyon-fishing charters already run this far. Virginia Beach and Cape May are the alternatives.
- **Waypoint:** 42°N, 48°W. This keeps the boat south of the Grand Banks and its fishing fleets, fog and spring icebergs.
- **Target:** off Mizen Head, south-west Ireland (51.35°N, 9.7°W). Any landfall in Europe counts, judged against Natural Earth country borders. Iceland and the Faroes count. The Azores, Madeira and the Canaries count only if you switch that option on.
- **Launch month:** May. That gets most of the crossing done before hurricane season peaks (mid-August to mid-October).

## Targets compared (no failures, May and June starts)

| Target | Ocean City, MD | Virginia Beach, VA | Cape May, NJ | Notes |
| --- | --- | --- | --- | --- |
| South-west Ireland | 99–100 days | 113–116 days | 114–119 days | Quickest; light shipping |
| Brittany or Cornwall | 98–99 days | 112–115 days | 112–118 days | As quick, but beside Europe's busiest shipping lanes |
| Galicia, Spain | 125–126 days | 141 days | 140–141 days | Weaker westerlies further south |
| Portugal | 139–144 days | 154–160 days | 142–151 days | Slowest |

The northern targets win clearly. The differences between launch sites come from where the invented weather puts the Gulf Stream near the coast, so don't choose a site on them. Rerun on historic weather first.

## Monte Carlo, Ocean City to south-west Ireland, failures on

100 voyages, launches April to July in 2022–2025, with the failure rates in use before 8 Nov 2026 (now called `original`).

> **Update, 8 Nov 2026:** the failure rates have been refitted to the Microtransat record ([Failure_Rates.md](Failure_Rates.md)). On the same route and launch window, the new default (`planning`) gives **37%** reaching Europe still reporting (95% range 28–47%), and the record's own rates (`historical`) give **22%** (15–31%). The two new main killers are electronics and comms failures (12% of boats now arrive silent) and fishermen on the shelf. The table below is kept for comparison between routes.

| | Mid-Atlantic route | Newfoundland route (for comparison) |
| --- | --- | --- |
| Reaches Europe, still reporting | 51% (95% range 41–61%) | 47.5% (33–63%) |
| Reaches Europe at all | 57% | 50% |
| Lost at sea | 36% | 37.5% |
| Ran aground outside Europe | 6% | 2.5% |
| Median crossing | 102 days (10–90%: 97–124) | 82 days |
| Knockdowns per voyage (mean) | 86 | 17 |
| Satellite airtime per voyage (mean) | $112 | $95 |

By launch month: April 41%, May 48%, June 52%, July 60%. With 22–30 runs a month, those ranges overlap heavily. July looks best only because the invented weather has no hurricanes.

**What the route changes**

- **More knockdowns.** The boat spends weeks in the storm track off the US coast, where lows form and run up the Gulf Stream. It self-rights every time in the simulator, but each knockdown risks damage.
- **More groundings.** About 6% of boats were disabled early (usually a jammed rudder) and drifted north-east onto Nova Scotia, New England or Newfoundland.
- **Same main killers.** Leaks (21 of 100) and electronics failures (12) still end most failed voyages. Sealing and electronics reliability remain the biggest levers on the odds. Under the refitted rates, being picked up on the shelf joins them (see [Failure_Rates.md](Failure_Rates.md)).

## First checks on real weather (run on Randolph's computer, Nov 8, 2026)

- **The weather grid matters.** The default voyage (Ocean City to south-west Ireland, launched 15 May 2024) took **86 days on the 1° grid and 102 days on the 0.25° grid**. That's 6,432 km sailed against 5,682 km. The gap built up west of 40°W, where the Gulf Stream and North Atlantic Current are narrow; east of there both runs moved alike. The simulator now uses a 0.25° grid inside 30–50°N, 80–38°W and 1° elsewhere (`fine_grid` in the scenario).
- **Real weather comes out close to the invented weather** for this one voyage: 102 days on real 2024 weather against about 100 on synthetic.
- **A dead boat near the coast can drift back in.** With no steering, a boat dropped at John's point (36.85°N, 75.70°W) on 15 May 2023 was carried north and then into the Chesapeake Bay mouth. It went aground near the York River after 8.9 days, never reaching the Gulf Stream. Our own drop point, 25 km off Ocean City, is also on the shelf, so the same thing could happen to a boat that fails early. Worth testing a drop further offshore.

## Drift tests: how far out to drop the boat (real weather, Nov 8, 2026)

> **Correction, 9 Nov:** these tests used the simulator's old dead-boat model. That model held the boat on a heading about 110° off the wind, so a dead boat reached across the wind at 4–6% of wind speed. Real drifting objects go roughly downwind: a Sunfish with no sail drifts at about 2.1% of the wind, a 4.15 m skiff at about 4.0% (Breivik et al. 2010), and both stay within about 15° of downwind. The simulator now uses a leeway model: 3.3% of the wind, ±14°, from a windage balance for Rev B. The tests need re-running before the 100 km decision is final (`collab/drift_tests.py`, on real weather).

This checks the worst case for the launch: a boat that is dead from the start, with no steering and the wing feathered, left to drift for 30 days. The tests used real Open-Meteo weather and currents from three drop points off Ocean City on 15 May of four years ([log](../collab/run_log_next_2026-11-08.txt), [table](../results/2026-11-08_drift_tests_ocean_city.txt)).

| Drop point | 2022 | 2023 | 2024 | 2025 | Still at sea after 30 days |
|---|---|---|---|---|---|
| 25 km off (old plan), 38.25°N 74.65°W | aground day 5.1 (NJ) | aground day 3.9 (Ocean City) | aground day 2.2 (VA Eastern Shore) | at sea, 62°W | **1 of 4** |
| **100 km off, 38.02°N 74.01°W** | at sea, 58°W | at sea, 67°W | at sea, 66°W | at sea, 67°W | **4 of 4** |
| 150 km off (shelf edge), 37.86°N 73.47°W | aground day 13.5 (Cape May) | at sea, 65°W | at sea, 55°W | at sea, 65°W | 3 of 4 |

- **Drop at least 100 km out.** On the inner shelf, the winds and currents in May push a dead boat back onto the beach within days. From 100 km out, every dead boat was carried east toward the Gulf Stream, ending 7–16° of longitude further east after a month.
- **Further out isn't automatically better.** In 2022, the boat dropped at the shelf edge was carried back west and went ashore near Cape May after 13.5 days. With four dates per point, the samples are small. The pattern (25 km bad, 100 km good) matches the physics, but the 100 vs 150 km difference could be chance.
- **The 100 km point is fishing ground.** It sits just inshore of the canyons along the shelf edge (Baltimore Canyon is about 20 km to the north-east), which are popular with offshore anglers and longliners. Labels, a radar reflector and a notice to the fishery council matter here (see [Failure_Rates.md](Failure_Rates.md) §5).
- **On invented weather the drop point makes little difference to the odds.** On synthetic weather with the planning failure rates, the 100 km drop cut groundings from 4 to 1 and captures from 4 to 1 per 100 runs. Overall it gave 30% (95% range 22–40%) against 37% (28–47%) from 25 km. That gap is within the noise of 100 runs, because more leak and electronics losses happened to be drawn. The real-weather Monte Carlo uses the 100 km drop.

## Before trusting these numbers

1. Done: the grid check (above) showed the 1° grid flatters crossings by about 15 days, so the Gulf Stream region now uses 0.25°.
2. Run the Monte Carlo on historic weather. The first attempt (Nov 8) hit Open-Meteo's free rate limit about a fifth of the way through its download. That job needed about 64,000 calls, against a free limit of 10,000 a day; the earlier estimate counted requests, not locations. The downloader now paces itself and waits overnight when the daily limit is hit. `simulator/run_real_mc.bat` runs 60 voyages from the 100 km drop (1 May – 15 June launches, 2023–2024). That is about 23,000 calls, or 2–3 days unattended.
3. Add hurricane tracks (NOAA's HURDAT2 best-track record) to the hazard model. That's the biggest gap for this route.

## Files

- `results/2026-11-08_midatlantic_ocmd_ireland_montecarlo.json`: the 100-run Monte Carlo (open it in the results viewer).
- `results/2026-11-08_midatlantic_route_comparison.json`: the 24 failure-free voyages behind the targets table.
