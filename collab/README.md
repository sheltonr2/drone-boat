# Collaboration with boat-sim

We share work with John's team ([jcolter11374/boat-sim](https://github.com/jcolter11374/boat-sim), MIT). The conversation lives on their repo in [issue #50](https://github.com/jcolter11374/boat-sim/issues/50), under their [collaboration protocol (#53)](https://github.com/jcolter11374/boat-sim/pull/53). Each team runs its own plan, and nothing secret or personal is shared.

## Agreed split (Nov 8, 2026)

| Item | Who | Status |
| --- | --- | --- |
| Shared failure-rate table with sources ([`docs/Failure_Rates.md`](../docs/Failure_Rates.md)) | us | done Nov 8 |
| History of Microtransat-style crossings ([`docs/Crossing_History.md`](../docs/Crossing_History.md), data in [`docs/data/`](../docs/data/)) | us | done Nov 8 |
| NOAA drifter check along the shared Gulf Stream stretch (36–42°N, 75–50°W) | boat-sim | done Nov 8 (skill 0.23 in the eddy field; [boat-sim #85](https://github.com/jcolter11374/boat-sim/issues/85)) |
| GLORYS vs Open-Meteo/SMOC currents along that stretch | boat-sim | done Nov 8 (means agree; eddies differ, RMS 0.43 m/s) |
| Dead-boat drift comparison (below) | both | done Nov 8: both into the Chesapeake in about 9 days (ours York River 8.9 d, theirs Hampton Roads 9.6 d) |
| Hurricane hazard | both | boat-sim: ERA5 wind correction (ERA5 gives ~0.5 of best-track wind in Cat 3–5). Us: storm-passage frequency by launch month from HURDAT2/IBTrACS (agreed Nov 8) |

## Dead-boat drift run (our side)

Same start in both simulators: 36.85°N, 75.70°W on 15 May 2023 at 12:00 UTC, drifting for 30 days with no steering. This needs real Open-Meteo data, so run it on your own computer from the `simulator` folder:

```
python -m drone_sim.cli voyage --scenario ../collab/dead_boat_2023-05-15.json --out ../results/dead_boat_2023-05-15.json
```

It uses a 0.25° weather grid to resolve the Gulf Stream. Commit the result file and we'll compare tracks with boat-sim's.

Run `python -m drone_sim.cli gridcheck` too. It tells us whether the default 1° grid blurs the Gulf Stream.

`LOG.md` records each check of their repo and what we did about it.
