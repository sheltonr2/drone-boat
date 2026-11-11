# Mid-Atlantic route study

Nov 8, 2026

The launch moves from Newfoundland to the US Mid-Atlantic coast. The best target is **south-west Ireland**, with any European landfall counting. It is the quickest target in the simulator (about 100 days from Ocean City, Maryland), and it avoids the heavy shipping around Brittany and Cornwall. The crossing is about 5,400 km instead of 3,000 and takes about 20 days longer than from Newfoundland. The simulated odds are about the same (51% vs 47.5%), but hurricane season is now a real risk, and the simulator doesn't model it.

All numbers come from the simulator's **synthetic (invented) weather**, because historic data couldn't be downloaded from the build environment. Use them to compare routes, not as forecasts. The invented weather includes a Gulf Stream, travelling lows and seasonal westerlies, but **no hurricanes**.

## Route

- **Launch:** **near the coast, about 10 km (5.5 nm) east of Ocean City Inlet (38.32°N, 74.97°W)**, from a small boat. Decided 10 Nov 2026 to keep the boat trip as short as practicable. The risk is a boat that dies in its first days drifting ashore; the launch plan handles it with an offshore-wind rule, an escort for the first hours and early recovery ([Launch_Plan.md](Launch_Plan.md)). The simulator results below were run from 100 km (8–10 Nov); the near-coast run is next. Virginia Beach and Cape May are the alternatives.
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

## Drift tests on ERA5 + Copernicus data, leeway model (Nov 10, 2026)

The same worst case (a boat dead from the moment it is dropped: no steering, wing feathered, 30 days adrift), re-run with the corrected leeway model on the downloaded bulk data: ERA5 winds, Copernicus SMOC currents (which include wave-driven Stokes drift) and MFWAM waves. One drop every 3 days from 1 May to 15 June 2023 (16 dates) at each of four points, at three leeway factors for sensitivity ([log](../results/2026-11-10_drift_tests_ocean_city_bulk_2023.txt), [data](../results/2026-11-10_drift_tests_ocean_city_bulk_2023.json)).

| Drop point | Aground within 30 days, at 2% / **3.3%** / 5% of wind | Median days to grounding (3.3%) | Where they went ashore (3.3%) | Median eastward progress of the rest (3.3%) |
|---|---|---|---|---|
| 25 km off (old plan) | 14 / **16** / 15 of 16 | 12 | Delmarva 11, New Jersey 2, Virginia Beach 2 | none left at sea |
| 50 km off | 13 / **13** / 13 | 9 | Delmarva 8, Virginia Beach 4, Outer Banks 1 | +0.5° |
| **100 km off (current plan)** | 8 / **8** / 12 | 9 | Outer Banks 7, Virginia Beach 1 | +5.2° |
| 150 km off (shelf edge) | 5 / **5** / 6 | 13 | Outer Banks 4, Cape Cod area 1 | +11.8° |

What this says:
- **The 100 km drop is not the safe point the Nov 8 tests suggested.** With the corrected model, half the dead boats dropped there in May–June 2023 went ashore, nearly all on the North Carolina Outer Banks after 5–23 days. The shelf currents carried them south-west along the coast instead of east into the Gulf Stream. The Nov 8 result (4 of 4 at sea) came from the old model, which let a dead boat reach across the wind.
- **The shelf edge (150 km) is better: 5 of 16 aground against 8**, and the boats that stayed at sea got more than twice as far east. This reverses the Nov 8 finding, which was based on one 2022 date that went ashore near Cape May.
- **In 2023, timing mattered more than distance.** From 100 km, every drop between 7 and 28 May went ashore, and every drop from 31 May to 15 June stayed at sea. From 150 km, only 13–22 May and 9 June went ashore. That is one year's weather pattern, not a rule. The 2024 results are in the table below.
- **The leeway factor barely matters** between 2% and 3.3%. At 5% (a boat with more windage than we estimate), groundings from 100 km rise from 8 to 12. The windage estimate for Rev B is about right to within that range, so this is a second-order risk.
- **A grounding is now often recoverable.** With the backup tracker fitted, a boat that dies early and washes up on the Outer Banks is a boat we can collect and relaunch, not a loss. That softens this result but doesn't remove it: a beached boat is a public nuisance and costs the launch season.
- **Keep in mind what this test is.** It is the worst case. The boat only drifts like this if it fails at or soon after launch. The real-weather Monte Carlo (running now) puts this together with the actual chance of an early failure.

**Second year (11 Nov): the same drift tests on 2024 weather** (`collab/run_log_drift_bulk_2024_2026-11-11.txt`). Aground within 30 days, at 2% / **3.3%** / 5% of wind:

| Drop point | 2023 | 2024 |
|---|---|---|
| 25 km off | 14 / **16** / 15 of 16 | 6 / **8** / 13 of 16 |
| 50 km off | 13 / **13** / 13 | 5 / **7** / 10 |
| 100 km off | 8 / **8** / 12 | 1 / **2** / 5 |
| 150 km off (shelf edge) | 5 / **5** / 6 | 0 / **0** / 1 |

- **2024 was a much kinder year than 2023:** about half as many groundings from 25 and 50 km, a quarter as many from 100 km, and none from the shelf edge at our leeway estimate.
- **Distance still helps in both years,** and the step from 50 to 100 km is the big one.
- **The early-May drops went ashore in both years.** In 2024 every drop on 1–10 May from 25 and 50 km grounded within 13 days on Delmarva or the Outer Banks; drops from 13 May to early June stayed at sea. In 2023 the bad spell was 7–28 May. Two years is not enough to call it a rule, but it supports waiting for a spell of offshore wind over fixing a date.
- **Late drops (after about 10 June) from 25–50 km drifted north-east and went ashore around Cape Cod and Long Island** after 2–4 weeks.
- **Leeway mattered more in 2024:** at 5% of wind, groundings from 25 km rose from 8 to 13.
- This is still the worst case (a boat dead at launch). The near-coast launch at 10 km is closer in than any point tested here, so the launch-plan rules (72 hours of offshore wind, escort, early recovery) carry the weight.

**What the full Monte Carlo adds (Nov 10, 250 voyages on 2023 weather):** only 2 of 250 voyages (0.8%) went aground near the US coast, because few boats actually fail in their first days after a 14-day shakedown. So the drop point is worth about 1% on the odds, not the 50% the worst case suggests. The launch date mattered far more: launches 1–15 May succeeded 44% of the time, 16–31 May 36%, and 1–15 June 21%. June boats met more breaking seas (4.1 knockdowns a day against 3.4) and arrived into autumn storms. That supports the 1–20 May window in [Launch_Plan.md](Launch_Plan.md). In 2023, early May is also when the 100 km drop grounds dead boats; that tension is another reason to prefer the shelf edge.

**Correction (10 Nov, evening):** the near-coast launch was then run directly (Rev C, 250 voyages, 2023): 11 groundings near the US coast against 2 from 100 km, and 38.8% verified arrivals against 44.8%. So the launch point is worth up to about 6 points, not 1; see [Design_RevC.md](Design_RevC.md). The simulator does not model the offshore-wind rule, escort or early recovery.

**Decision (10 Nov 2026): launch near the coast instead** (see the Launch line at the top). The analysis below is kept for the record. The earlier recommendation was to move the drop to the shelf edge, about 150 km (81 nm) out at 37.86°N 73.47°W, unless 2024 reverses this. It is still inside the range of Ocean City's canyon charters, which fish the shelf edge. The cost is about an hour more each way on the charter.

## Drift tests: how far out to drop the boat (Open-Meteo, Nov 8, 2026; superseded)

> **Correction, 9 Nov:** these tests used the simulator's old dead-boat model. That model held the boat on a heading about 110° off the wind, so a dead boat reached across the wind at 4–6% of wind speed. Real drifting objects go roughly downwind: a Sunfish with no sail drifts at about 2.1% of the wind, a 4.15 m skiff at about 4.0% (Breivik et al. 2010), and both stay within about 15° of downwind. The simulator now uses a leeway model: 3.3% of the wind, ±14°, from a windage balance for Rev B. Re-run on Nov 10 (section above); the conclusions below no longer hold.

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
