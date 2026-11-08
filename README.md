# Drone Boat: Solar-Sail Autonomous Ocean Drone

This is a 1.5 m self-righting sailboat with a rigid wing sail, solar power and two-way Iridium satellite commanding. It is designed to cross the North Atlantic from west to east (Newfoundland or Nova Scotia to Ireland) and then keep roaming, for under about $2,000 in hardware.

## What's here

| Folder | Contents |
| --- | --- |
| [`docs/`](docs/) | [Build Plan](docs/Build_Plan.md) (architecture, comms and command protocol, software plan, recommended parts, budget, risks) and [Executive Summary](docs/Executive_Summary.md) (supplies, dimensions, watch-outs, odds). |
| [`build-files/`](build-files/) | Rev A drawing set (`Drawings.pdf`, 18 tabloid sheets), full-size cutting templates (`Templates_1to1_Letter.pdf`), DXF templates for CNC/laser, 20 STL files for the 17 printed parts, and the Python that generates them all. See [`build-files/README.txt`](build-files/README.txt). |
| [`simulator/`](simulator/) | Voyage simulator: historic ERA5 wind, waves, currents (incl. Gulf Stream), tides and solar from Open-Meteo (2022 on), hybrid or full 6-DOF physics, editable design (keel, wing, rudder, ballast) or your own STL/OBJ hull, power and satellite budget, autopilot and command testing, failures and Monte Carlo odds. See [`simulator/README.md`](simulator/README.md). |
| [`results-viewer/`](results-viewer/) | Standalone results page (`index.html`, open in any browser) with demo runs; drop in a results `.json` exported from the simulator. |

## Quick start (simulator on Windows)

1. Install Python 3.10 or newer.
2. In `simulator/`, double-click `setup_windows.bat` once, then `run_simulator.bat`. The app opens at http://localhost:8765.
3. Check everything works: `python -m drone_sim.cli selftest`.

## Key numbers (Rev A)

- Length 1,500 mm, beam 400 mm, about 21 kg all-up, 8.2 kg lead bulb, self-righting from 180°.
- Wing sail 1,000 × 300 mm (0.30 m²), NACA 0015, free-rotating with a tail flap.
- 40 W solar, 192 Wh LiFePO4, under 1.5 W average draw, RockBLOCK 9603 two-way Iridium.

## Open findings

- **Wing counterweight:** the simulator shows the wing needs about 0.9 kg on an arm about 0.30 m forward of the mast to balance. Putting the counterweight in the nose pocket as drawn would take about 6 kg. The drawings have not been updated for this yet.
- **Simulated odds:** demo runs on synthetic (invented) weather gave about 48% reaching Europe still reporting, with crossings around 80 days. Historic-weather Monte Carlo runs have not been done yet. The failure rates are editable estimates.
- **Historic data download:** the Open-Meteo code was tested against mocked data only. Run the self-test to confirm live access.

## Live documents

The docs in `docs/` are snapshots of living Claude Docs:
[Build Plan](https://claude.ai/artifact/WmBHp596XyjBUHexcbbfRM) ·
[Executive Summary](https://claude.ai/artifact/MVREF7YQSp9tC5zgpuKYWa) ·
[Results Viewer](https://claude.ai/artifact/BDfnejrUSTCdFox6G9CGwe)
