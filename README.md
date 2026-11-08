# Drone Boat: Solar-Sail Autonomous Ocean Drone

This is a 1.5 m self-righting sailboat with a rigid wing sail, solar power and two-way Iridium satellite commanding. It is designed to cross the North Atlantic from west to east (Newfoundland or Nova Scotia to Ireland) and then keep roaming, for under about $2,000 in hardware.

## What's here

| Folder | Contents |
| --- | --- |
| [`docs/`](docs/) | [Build Plan](docs/Build_Plan.md) (architecture, comms and command protocol, software plan, recommended parts, budget, risks), [Executive Summary](docs/Executive_Summary.md) (supplies, dimensions, watch-outs, odds), [Rev B simulation results](docs/Simulation_RevB.md) and [Field tests](docs/Field_Tests.md) (tow, inclining, self-righting, wing balance, solar day). |
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
- **Simulated odds:** 40 Monte Carlo runs of Rev B on synthetic (invented) weather gave 47.5% reaching Europe still reporting (95% range 33–63%), median crossing 82 days. Historic-weather runs have not been done yet. The failure rates are editable estimates, and leaks and electronics failures dominate the losses.
- **Historic data download:** the Open-Meteo code was tested against mocked data only. Run the self-test to confirm live access.

## Ideas borrowed from other projects

From John's [boat-sim](https://github.com/jcolter11374/boat-sim) (MIT): the tow-test idea behind [Field tests](docs/Field_Tests.md), the panel-loss model for solar, and arrival odds by launch month.

## Live documents

The docs in `docs/` are snapshots of living Claude Docs:
[Build Plan](https://claude.ai/artifact/WmBHp596XyjBUHexcbbfRM) ·
[Executive Summary](https://claude.ai/artifact/MVREF7YQSp9tC5zgpuKYWa) ·
[Results Viewer](https://claude.ai/artifact/BDfnejrUSTCdFox6G9CGwe)
