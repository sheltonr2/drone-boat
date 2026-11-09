# Drone Boat: Solar-Sail Autonomous Ocean Drone

This is a 1.5 m self-righting sailboat with a rigid wing sail, solar power and two-way Iridium satellite commanding. It is designed to cross the North Atlantic from the US Mid-Atlantic coast to Europe (default: off Ocean City, Maryland, aiming for south-west Ireland; any European landfall counts) and then keep roaming, for under about $2,000 in hardware.

## What's here

| Folder | Contents |
| --- | --- |
| [`docs/`](docs/) | [Build Plan](docs/Build_Plan.md) (architecture, comms and command protocol, software plan, recommended parts, budget, risks), [Executive Summary](docs/Executive_Summary.md) (supplies, dimensions, watch-outs, odds), [Rev B simulation results](docs/Simulation_RevB.md), [Mid-Atlantic route study](docs/Route_MidAtlantic.md), [Field tests](docs/Field_Tests.md) (tow, inclining, self-righting, wing balance, solar day, shakedown), [Failure rates](docs/Failure_Rates.md) (shared hazard table with sources, fitted to the Microtransat record) and [Crossing history](docs/Crossing_History.md) (every Microtransat attempt, plus other autonomous crossings). Data and analysis are in `docs/data/`. |
| [`build-files/`](build-files/) | Rev B drawing set (`Drawings.pdf`, 18 tabloid sheets), full-size cutting templates (`Templates_1to1_Letter.pdf`), DXF templates for CNC/laser, 21 STL files for the 18 printed parts, and the Python that generates them all. See [`build-files/README.txt`](build-files/README.txt). |
| [`simulator/`](simulator/) | Voyage simulator: historic ERA5 wind, waves, currents (incl. Gulf Stream), tides and solar from Open-Meteo (2022 on), hybrid or full 6-DOF physics, editable design (keel, wing, rudder, ballast) or your own STL/OBJ hull, power and satellite budget, autopilot and command testing, failures and Monte Carlo odds. See [`simulator/README.md`](simulator/README.md). |
| [`results/`](results/) | Saved simulator runs (open them in the results viewer). |
| [`results-viewer/`](results-viewer/) | Standalone results page (`index.html`, open in any browser) with demo runs; drop in a results `.json` exported from the simulator. |

## Quick start (simulator on Windows)

1. Install Python 3.10 or newer.
2. In `simulator/`, double-click `setup_windows.bat` once, then `run_simulator.bat`. The app opens at http://localhost:8765.
3. Check everything works: `python -m drone_sim.cli selftest`.

## Key numbers (Rev B)

- Length 1,500 mm, beam 400 mm, about 21 kg all-up, 8.2 kg lead bulb, self-righting from 180°.
- Wing sail 1,000 × 300 mm (0.30 m²), NACA 0015, free-rotating with a tail flap, balanced by about 0.8 kg of lead in a pod 300 mm forward of the spar.
- 40 W solar, 192 Wh LiFePO4, under 1.5 W average draw, RockBLOCK 9603 two-way Iridium.

## Open findings

- **Wing counterweight (fixed in Rev B):** the lead moved from the wing's nose pocket (which needed about 7.6 kg) to a printed pod on a 300 mm forward arm (about 0.8 kg). See [Simulation_RevB.md](docs/Simulation_RevB.md): the boat stays at 20.8 kg, GM goes from 0.11 to 0.20 m, and crossings run about 4 days faster.
- **Simulated odds (Mid-Atlantic route):** 100 Monte Carlo runs on synthetic (invented) weather, April–July launches, median crossing 102 days. With failure rates refitted to the Microtransat record (Nov 8, 2026), **37%** reach Europe still reporting under the `planning` set (95% range 28–47%; this assumes the 3-week coastal trial is passed), and **22%** under the record's own `historical` rates. The earlier 51% used the old guesses. Real-weather drift tests moved the drop point to about 100 km off Ocean City, because dead boats dropped 25 km out drifted ashore. A real-weather Monte Carlo is set up in `simulator/run_real_mc.bat` (2–3 days, because of Open-Meteo's free limits). Hurricanes are not modelled. See [Failure_Rates.md](docs/Failure_Rates.md) and [Route_MidAtlantic.md](docs/Route_MidAtlantic.md). Historic-weather runs have not been done yet.
- **Historic data works.** The self-test downloaded real Open-Meteo data on Windows (Nov 8, 2026). A grid check showed the 1° weather grid makes crossings look about 15 days faster than a 0.25° grid, so the Gulf Stream region now uses 0.25° (see [Route_MidAtlantic.md](docs/Route_MidAtlantic.md)).

## Ideas borrowed from other projects

From John's [boat-sim](https://github.com/jcolter11374/boat-sim) (MIT): the tow-test idea behind [Field tests](docs/Field_Tests.md), the panel-loss model for solar, arrival odds by launch month, and (from their notes in [boat-sim #50](https://github.com/jcolter11374/boat-sim/issues/50)) three fixes: no double-counted Stokes drift with Open-Meteo currents, Europe judged by Natural Earth country borders, and a 0.25° grid check (`python -m drone_sim.cli gridcheck`).

## Live documents

The docs in `docs/` are snapshots of living Claude Docs:
[Build Plan](https://claude.ai/artifact/WmBHp596XyjBUHexcbbfRM) ·
[Executive Summary](https://claude.ai/artifact/MVREF7YQSp9tC5zgpuKYWa) ·
[Results Viewer](https://claude.ai/artifact/BDfnejrUSTCdFox6G9CGwe)
