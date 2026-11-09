# Collaboration with boat-sim

We share work with John's team ([jcolter11374/boat-sim](https://github.com/jcolter11374/boat-sim), MIT). The conversation lives on their repo in [issue #50](https://github.com/jcolter11374/boat-sim/issues/50), under their [collaboration protocol (#53)](https://github.com/jcolter11374/boat-sim/pull/53). Each team runs its own plan, and nothing secret or personal is shared.

## Agreed split (Nov 8, 2026)

| Item | Who | Status |
| --- | --- | --- |
| Shared failure-rate table with sources (`docs/Failure_Rates.md`) | us | to do |
| History of Microtransat-style crossings (`docs/Crossing_History.md`) | us | to do |
| NOAA drifter check along the shared Gulf Stream stretch (36–42°N, 75–50°W) | boat-sim | asked |
| GLORYS vs Open-Meteo/SMOC currents along that stretch | boat-sim | asked |
| Dead-boat drift comparison (below) | both | our run done Nov 8 ([track](../results/2026-11-08_dead_boat_2023-05-15_track.txt)); waiting for boat-sim's |
| Hurricane hazard from NOAA HURDAT2 | both | proposed |

## Dead-boat drift run (our side)

Same start in both simulators: 36.85°N, 75.70°W on 15 May 2023 at 12:00 UTC, drifting for 30 days with no steering. This needs real Open-Meteo data, so run it on your own computer from the `simulator` folder:

```
python -m drone_sim.cli voyage --scenario ../collab/dead_boat_2023-05-15.json --out ../results/dead_boat_2023-05-15.json
```

It uses a 0.25° weather grid to resolve the Gulf Stream. Commit the result file and we'll compare tracks with boat-sim's.

Run `python -m drone_sim.cli gridcheck` too. It tells us whether the default 1° grid blurs the Gulf Stream.

`LOG.md` records each check of their repo and what we did about it.
