# Mid-Atlantic route study

Nov 8, 2026

The launch moves from Newfoundland to the US Mid-Atlantic coast. The best target is **south-west Ireland**, with any European landfall counting. It is the quickest target in the simulator (about 100 days from Ocean City, Maryland), and it avoids the heavy shipping around Brittany and Cornwall. The crossing is about 5,400 km instead of 3,000 and takes about 20 days longer than from Newfoundland. The simulated odds are about the same (51% vs 47.5%), but hurricane season is now a real risk, and the simulator doesn't model it.

All numbers come from the simulator's **synthetic (invented) weather**, because historic data couldn't be downloaded from the build environment. Use them to compare routes, not as forecasts. The invented weather includes a Gulf Stream, travelling lows and seasonal westerlies, but **no hurricanes**.

## Route

- **Launch:** about 25 km off Ocean City, Maryland (38.25°N, 74.65°W), dropped from a charter boat clear of the Delaware Bay and Chesapeake shipping lanes. Virginia Beach and Cape May are the alternatives.
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

100 voyages, launches April to July in 2022–2025, default failure rates.

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
- **Same main killers.** Leaks (21 of 100) and electronics failures (12) still end most failed voyages. Sealing and electronics reliability remain the biggest levers on the odds.

## Before trusting these numbers

1. Run `python -m drone_sim.cli gridcheck` on your computer. It shows whether the 1° weather grid blurs the Gulf Stream; if crossing times move more than about 3 days, use a 0.25° grid.
2. Run the Monte Carlo on historic weather (2022 onward) for April–July launches.
3. Add hurricane tracks (NOAA's HURDAT2 best-track record) to the hazard model. That's the biggest gap for this route.

## Files

- `results/2026-11-08_midatlantic_ocmd_ireland_montecarlo.json`: the 100-run Monte Carlo (open it in the results viewer).
- `results/2026-11-08_midatlantic_route_comparison.json`: the 24 failure-free voyages behind the targets table.
