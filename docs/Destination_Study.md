# Destination study: is there a better target than Ireland?

12 November 2026. Plan and reasoning; results to follow when the runs finish. Run files `simulator/run_destinations_2023.bat` and `run_destinations2_2023.bat`, scenarios in `collab/destinations/`.

## How the question is set up

- **The simulator already counts any landfall in Europe as a crossing.** Ireland is where the autopilot aims, not the only place that counts. So the question is which aim point gets the most boats across.
- **What counts as "across" in this study:** mainland Europe and the British Isles, Madeira, the Canary Islands, and north-west Africa's Atlantic coast (Morocco, Western Sahara). **The Azores do not count:** they sit about two-thirds of the way across, roughly 4,000 km from the launch point against 5,200–5,700 km for the others.
- **Same everything else:** Rev C5, corrected simulator, 10 km launch off Ocean City, launches 1 May–15 June 2023, real 2023 weather, 150 voyages per destination. A 150-voyage result is good to about ±8 points, so this is a first screen; the best two or three get a 2023 + 2024 confirmation run.
- **An artefact to keep in mind:** a boat that leaves the weather data's area (north of 60°N or east of 0°) gets no wind there. That penalises boats that overshoot the Hebrides to the north.
- **Weather data limits:** the downloaded weather covers 26–60°N and 82°W–0°. That rules out Norway, Iceland and West Africa south of the Canaries without new downloads. A boat pushed south of 26°N near the Canaries sails on neutral weather there.

## Candidates

### How they were chosen

The first six were a quick north-to-south sweep of well-known headlands on the European side that fit inside the weather data, each with an obvious route. They were a sensible first screen but not an optimised list, and they left three gaps: nothing north of Mizen Head, nothing between Brittany and Galicia, and nothing between Lisbon and the Canaries. They also tested only one route to each place. A second batch of seven fills those gaps.

The choice is driven by two things more than by the name on the map:
- **The latitude at which the boat approaches the far side.** That sets how much it uses the westerlies and the North Atlantic Current, how rough the seas are, and how long it takes.
- **How good a net the coast behind the aim point is.** Any far-side landfall counts, and many boats arrive damaged. A coast that wraps round the aim point, with the wind blowing onto it, catches boats that can no longer steer well. An isolated island or a coast the current runs along, not onto, does not.

### Batch 1 (`run_destinations_2023.bat`)

| Destination | Aim point | Route distance | Route |
|---|---|---|---|
| South-west Ireland (current plan) | Mizen Head, 51.35°N 9.7°W | 5,380 km | via 42°N 48°W, south of the Grand Banks |
| Cornwall and the Isles of Scilly | 49.95°N 6.3°W | 5,610 km | same waypoint |
| Brittany | Pointe du Raz, 48.04°N 4.85°W | 5,730 km | same waypoint |
| Galicia, Spain | Cape Finisterre, 42.9°N 9.35°W | 5,530 km | via 40°N 48°W |
| Portugal | Cabo da Roca, 38.75°N 9.6°W | 5,560 km | direct (the direct course arcs north to about 43°N in mid-ocean) |
| Canary Islands | Lanzarote, 29.0°N 13.4°W | 5,690 km | direct |

### Batch 2 (`run_destinations2_2023.bat`)

| Destination | Aim point | Why it was added |
|---|---|---|
| Bay of Biscay | Vendée coast, 46.45°N 1.85°W | The middle of the widest net: Brittany to the north, Spain to the south, wind onshore. The best test of the "net" idea |
| West of Ireland | Connemara, 53.4°N 10.25°W | Further into the current's path; a boat that drifts north still has Donegal and Scotland beyond it |
| Outer Hebrides, Scotland | South Uist, 57.2°N 7.5°W | The northern end of what the weather data allows; most current, roughest seas |
| Gulf of Cádiz | 36.55°N 6.4°W | A funnel between the Algarve and Morocco, both of which count |
| Morocco | Casablanca, 33.6°N 7.7°W | A long, straight coast to aim at south of the stormy latitudes |
| Canary Islands by the northern arc | via 42°N 48°W and 40°N 20°W | The traditional sailing route: stay in the westerlies, then turn south with the northerly winds off Portugal. Tests route against destination |
| Azores | Faial, 38.55°N 28.75°W | Only about 4,000 km, but two-thirds of the way across. Reported separately: it counts only if the Azores are accepted as "across" |

### Not tested, and why

- **Iceland, the Faroes and Norway:** outside the downloaded weather (which stops at 60°N and at 0° longitude). Iceland's south coast is about 4,600 km from the launch point, shorter than Ireland, but colder and rougher, with ice near the route. Worth a weather download only if the northern targets do well here.
- **West Africa south of the Canaries, Cape Verde:** outside the weather data (south of 26°N), and reaching them means crossing the light-wind belt.
- **The Caribbean and South America:** not across from North America in the sense asked. (The trade-wind route runs the other way, Europe to the Caribbean.)
- **Madeira:** a single small island, bracketed by the Portugal and Canaries runs.
- **Different routes to the northern targets:** the waypoint at 42°N 48°W is held fixed. Tuning it is the next step for whichever targets win.
- **A different launch point:** was out of scope here. Added on 12 Nov as its own study, which also tests launch and destination pairs: [Launch_Point_Study.md](Launch_Point_Study.md).

## What the physics suggests before the runs

These are expectations from general North Atlantic oceanography, not results. The runs will confirm or overturn them.

- **The ocean's conveyor favours the north.** The Gulf Stream feeds the North Atlantic Current, which runs north-east toward Ireland and Britain. A boat sailing for the British Isles has current and the prevailing westerlies behind it for most of the way, and a dead boat drifts the same way. That is why drift bottles and small unpowered boats from North America so often land in Ireland, Britain and France.
- **The southern routes cross the Azores High.** In summer a large area of high pressure sits around 30–40°N in the mid-Atlantic, with light, shifting winds. Routes to Portugal and the Canaries go through or around it, so they are likely to be slower, and time at sea is what drives failures.
- **The north is rougher.** Gales and breaking seas are more frequent the further north and the later in the season. That costs knockdowns, wing and keel damage. It is the main argument for a more southerly target.
- **Coast width matters.** Aiming at Cornwall or Brittany puts the boat in the mouth of a funnel: if it drifts north it hits Ireland or Wales, if south it hits France or Spain. Aiming at south-west Ireland, a boat that overshoots north passes Ireland and continues into the open sea towards Scotland and Norway.
- **Traffic and fishing near the coast.** The approaches to the English Channel (off Ushant) and Cape Finisterre are among the busiest shipping lanes in the world, and the Iberian and Moroccan coasts are heavily fished. The simulator's collision and pick-up risks do not vary by region, so it will understate this for Brittany, Galicia and Portugal.
- **Hurricanes.** The Canaries route stays in the subtropics into August to October. The simulator's weather resolves hurricanes poorly, so it will understate that risk.
- **The Azores** would be the easiest target by distance alone, but they are not across the Atlantic and are excluded.

## When results are in

For each destination: share of voyages reaching any far-side coast with a verified position, where they landed, median crossing time, and the main causes of loss. Then a recommendation, with the confirmation run for the best candidates.

## Interim results: batch 1 (12 Nov 2026, 14:20)

**Interim.** Batch 2 (seven more aim points) is still running; no recommendation until it is in. Rev C5 on the corrected simulator, 150 voyages per aim point, 2023 weather, launched 10 km off Ocean City, 1 May–15 June. Every aim point used the same launch dates and seeds, so the paired column is the fairer comparison. A 150-voyage share is good to about ±8 points.

| Aim point | Success (95% range) | vs SW Ireland, paired | Any landfall | Median days | Lost | Aground | At sea | Where successes landed |
|---|---|---|---|---|---|---|---|---|
| SW Ireland (Mizen Head) | 44.7% (37–53) | — | 51.3% | 121 | 14.7% | 12.0% | 22.0% | Ireland 58, France 4, Great Britain 4, Portugal 1 |
| Cornwall | 44.7% (37–53) | +0.0 (-7.3 to +8.0) | 50.7% | 127 | 16.0% | 12.7% | 20.7% | Great Britain 57, France 9, Portugal 1 |
| Brittany | 41.3% (34–49) | -3.3 (-10.7 to +4.0) | 48.6% | 132 | 13.3% | 12.7% | 25.3% | France 58, Ireland 3, Great Britain 1 |
| Galicia | 38.0% (31–46) | -6.7 (-15.3 to +2.0) | 43.4% | 140 | 20.7% | 5.3% | 30.7% | Spain 51, Portugal 5, France 1 |
| Portugal (Lisbon) | 33.4% (26–41) | -11.3 (-21.3 to -1.3) | 36.1% | 148 | 16.7% | 12.7% | 34.7% | Portugal 50 |
| Canaries | 10.7% (7–17) | -34.0 (-42.7 to -25.3) | 13.4% | 170 | 19.3% | 6.0% | 61.3% | Canaries 15, Madeira 1 |

Success = arrived still reporting or tracked by the YB3. "Any landfall" also counts silent and adrift arrivals. Boats that reach the 40 km arrival circle but are still offshore count for the aim point's country. Lost, aground and at sea are shares of all 150.

What it shows so far:

- **SW Ireland and Cornwall are tied** (44.7% each, paired difference 0, range −7 to +8). Brittany is within noise (−3).
- **The further south, the worse.** Galicia −7 (not yet certain), Portugal −11 (range −21 to −1), the Canaries −34. The southern routes are slower (median 140–170 days against 121), so more boats are still at sea at the end of the season (31–61% against 22%) and every per-day failure has longer to strike. That matches the physics note above: the Azores High costs more than the rougher north.
- **Groundings** are about the same everywhere (5–13%) except Galicia, where boats that overshoot the coast keep sailing south instead of hitting land.
- **First failures** are the same mix on every route (rudder servos, electronics, fouling, leaks); no route avoids them. Rev D (backup steering and protected electronics) addresses electronics on every route.
- Caveats as before: collision and pick-up risk don't vary by region, so busy approaches (Channel, Ushant, Finisterre) are flattered; one weather year.

Script: `docs/data/dest_analysis.py`. Results: `results/2026-11-12_dest_2023_<name>.json`. Log: `collab/run_log_destinations_2023_2026-11-12.txt`.
