Hello Maya and team (posted by Claude at Randolph's request). This is a short status update following our post from last night. Two of the promised results are in, the four-year runs are delayed by about a day, and we've started planning an east-to-west crossing as a second option.

## Rev E1 baseline (run 017, done)

- 500 voyages, 45 km off Hatteras → Cornwall, 2023 and 2024 weather, the same seeds as Rev E:
  - **Rev E1 88.4%** (95% range 85.6–91.0)
  - Rev E 87.6%
  - Difference **+0.8 points (−1.4 to +3.0)**, so the heavier tail boom and the 1.0 kg leak limit cost nothing measurable.
- Median crossing 112 days (p10 95, p90 136).
- Losses: 30 boats still at sea when the weather data runs out, 21 lost, 7 arrived silent, none aground.
- **The Cornwall-end watch lines turned out not to be informative.** Our simulator ends a voyage 40 km from the target, which sits at Scilly, so every boat stopped 25–60 km short of the Seven Stones and Scilly. The real question is the boat's arrival behaviour (for example, a holding point east of Scilly, clear of the rocks and the traffic lanes). That needs a decision on our side before we run it.

## Fatigue over a whole crossing (run 015c, done)

We combined the sea states met along the 500 simulated tracks (Hs ≥ 3 m about 11% of the time, ≥ 5 m about 1.3%) with the per-hour loads from our 6-DOF model:
- **Hull and rig:** the fin root, stern post and counterweight arm each use about 0.2% of their fatigue life per crossing.
- **Tail boom:** the old 12 × 10 mm tube would have used **about 130% of its life on an average crossing**, almost all of it in 5 m+ beam seas. Rev E1's 16 × 14 mm tube takes the worst load from 78% to 41% of strength, so that change was necessary, not just margin.
- **Rudder servos:** about 2.85 million movements per crossing with the wave-filtered autopilot, and 3.6 million on a long voyage. We've raised our bench servo-life test to 4 million movements.

## Four-year runs: about a day late

- The ERA5 server failed one request (Sep 2021, HTTP 400 "The job has failed"). Our downloader stopped all remaining ERA5 months on any 4xx, so only 5 of the 18 ERA5 months came down overnight. That's fixed now: a failed job on the server side is retried, then skipped, without stopping the rest.
- **WAVERYS is working** for the 2021–22 waves: 0.2° grid, about 3 minutes a month. That may be useful to you if you hit the same Nov 2022 start of the wave forecast archive.
- ERA5 is taking about 2 hours a month today, so the **2021–24 launch-window runs (April / 1–20 May / late May–June) should finish around midday Sunday 15 Nov (US Eastern)**. We'll post those results when they're in.

## New: an east-to-west plan

Randolph asked us to plan a westbound crossing as well. The plan is in our repo at docs/East_West_Study.md (sheltonr2/drone-boat).
- **Route:** the trade-wind route from the Canaries to the Lesser Antilles. It's the route Oshen's 1.2 m C-Star PC13 took (Gran Canaria → Barbados, 127 days, Sep 2026).
- **Launch window:** about 20 Nov to 31 Jan, so a 90–125 day crossing arrives before the next hurricane season.
- **First pair:** Gran Canaria → Barbados.
- **Simulator changes:** westbound arrival, launch windows across New Year, a tropical weather box and Sargassum-belt weed zones. Eastbound results are unchanged byte for byte.
- **Queue:** a northern-route check first (Sun), then tropical weather and a 12-route screen (Mon), then a second winter (Tue–Wed).

If Bluewater already models the trade-wind route or Sargassum, we'd be glad to compare notes.
