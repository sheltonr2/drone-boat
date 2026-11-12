# Electronics: why they fail in the simulator, and potting

> **12 Nov 2026: adopted as Rev D.** The limp-home controller, coating and potting, and the RockBLOCK Plus are now in the drawings and the default simulator design ([Design_RevD.md](Design_RevD.md)).

12 November 2026. Grade D: the failure rates are fitted to other people's boats, and the improvement factors in the study run are guesses.

## Short answer on potting

**Potting individual boards has not been considered in this project until now.** Three earlier mentions are easy to misread:
- **"Potted IP68 box"** in the build plan and failure rates means the box is bonded into the hull, not that anything inside it is potted.
- **The Executive Summary's risk table** says "conformal-coat the boards, and pot the connectors". That never made it into the build plan, the drawings or the parts list.
- **The simulator** gives the electronics a ×0.7 credit for the sealed box and desiccant. It gives nothing for coating or potting.

## Where the losses come from

In the first Rev C5 run (250 voyages, 2023 weather):
- **83 voyages had an electronics failure.** In 47 it was the first thing to go, which is the figure reported earlier.
- **About 20 came after a leak** had put water in the hull.
- **About 60 came from the base "dry" rate** of 0.25% per day. That rate is the Microtransat record of boats going silent or erratic (0.35% per day) less 30% for the sealed box.

A flat 0.25% per day over the average 139-day voyage predicts about 72 failures, so the dry rate does most of the damage. Keeping water out of the box (Rev C1) was worth doing but cannot fix this on its own. The dry rate lumps together everything that kills small autonomous boats' electronics: humidity and salt creeping into connectors, corrosion on boards, power faults and software hangs.

## What can be potted

| Item | Pot? | Notes |
|---|---|---|
| Wind vane sensor (magnetic angle encoder) | **Yes** | Pot the board completely; the magnet sits outside on the vane shaft. Soft silicone or urethane |
| Solar charge controller (Genasun) | **Buy it potted** | Genasun's waterproof models come factory-potted. Check that the GV-5 variant we buy is one of them; if not, change to one that is |
| DC-DC converters, fuse and power-distribution board | **Yes** | Small heat (well under 1 W each); a thin, thermally conductive urethane |
| Wire-to-wire joints and the inside ends of the cable penetrators | **Yes** | Probably the single biggest win. Heat-shrink with adhesive lining, then pot the joint cluster in a small mould |
| GPS and compass module | **Yes, with care** | Soft silicone only: a rigid compound stresses the compass and shifts its calibration. Keep the GPS patch antenna's top covered by no more than a few millimetres. Recalibrate the compass after potting |
| Watchdog board (ESP32) | **Coat, then pot after shakedown** | Potting ends firmware updates by cable. Pot it only once the software is final, and keep a programmed spare |
| Pixhawk autopilot | **No** | Barometer port, SD card log, USB for updates, vibration-isolated motion sensors. Conformal coat the board with the connectors, barometer and SD slot masked |
| Satellite modem, RockBLOCK 9603 | **Replace instead** | Its data sheet allows no more than 75% relative humidity, and it is not waterproof. The RockBLOCK Plus is the same service in a fully encapsulated, waterproof case, mounted outside the box. That also takes the antenna cable out of the box |
| Servos | **No (buy sealed)** | Already specified as waterproof servos |
| Battery management board | **No** | Leave in the sealed battery box; potting traps heat and blocks inspection |

### How to pot

- **Compound:** two-part polyurethane for power boards and joints; soft silicone for anything with a sensor on it. Avoid rigid epoxy on sensors.
- **When:** only after the 14-day shakedown, so faults are found while boards can still be reworked. A potted board cannot be repaired; keep one spare of each.
- **Coating:** everything in the box gets a conformal coat (acrylic or urethane spray) whether or not it is potted.
- **Heat:** the whole box dissipates about 1–2 W, so potting adds no meaningful temperature rise.

## Other changes worth more than potting alone

1. **A limp-home controller.** If the Pixhawk dies today, the boat drifts. The ESP32 watchdog could drive the tail and one rudder directly on a simple compass course toward Ireland. That turns "box dead, drifting" into "sailing slowly". In the C5 run, of the 83 boats whose electronics died, 39 were still at sea at the end and 21 drifted to the far side without steering; a boat that keeps sailing would turn some of those into arrivals. Not yet modelled. It needs its own compass and a separate power feed. This is a design change for review, not drawn. **Update 12 Nov: drawn as Rev D with the potting and the RockBLOCK Plus ([Limp_Home_Spec.md](Limp_Home_Spec.md), [Potting_Spec.md](Potting_Spec.md)).**
2. **Report humidity and box temperature** in every satellite message, so a slow leak shows up as a trend before it kills anything.
3. **Locking connectors throughout** (the Pixhawk's are already locking). No pin headers or push-on jumper wires in the box.

## Results (12 Nov 2026, corrected simulator)

| | Rev C5 as drawn | With better-protected electronics |
|---|---|---|
| Verified arrivals | 48.0% (41.9–54.2) | 52.8% (46.6–58.9) |
| Arrived still reporting | 33.6% | 39.6% |
| Voyages with an electronics failure | 61 | 35 |
| Electronics as first failure | 31 | 16 |

**Coating, potting and the encapsulated modem add about 5 points of arrivals (paired difference +4.8, 95% range +1.5 to +8.1), and 6 points of boats still reporting on arrival** — if the guessed factors hold (dry electronics rate ×0.6, modem ×0.5, wet factor 1.3 against 2.0). The improvement is real in the model; its size rests on those guesses. The limp-home runs followed (below).

### Limp-home controller

| | Rev C5 | + better electronics | + limp-home | + both |
|---|---|---|---|---|
| Verified arrivals | 48.0% (41.9–54.2) | 52.8% (46.6–58.9) | **59.6% (53.4–65.5)** | **61.2% (55.0–67.0)** |
| Paired gain over C5 | — | +4.8 (+1.5 to +8.1) | **+11.6 (+7.6 to +15.6)** | **+13.2 (+8.7 to +17.7)** |
| Lost | 15.2% | 14.0% | 12.8% | 12.8% |
| Aground | 11.2% | 9.6% | 7.2% | 7.2% |

- **The limp-home controller is the bigger win.** In the C5 run, 61 boats lost their main electronics. Without a backup, 14 of them washed up somewhere across and 47 drifted, grounded or were lost. With limp-home, the same 61 boats took over. About 29 sailed in, most still tracked by the YB3, and groundings among them fell from 11 to 1.
- **With both, the gains overlap.** Better electronics means fewer box deaths, so the controller has less to rescue: +13.2 together, against +11.6 and +4.8 apart.
- **A scoring fix was needed.** The simulator labelled every arrival with a dead main box "arrived adrift" and did not count it as a success, even when the limp-home controller had sailed it in and the YB3 was tracking it. This is fixed in `sim.py`. The two runs were rescored from their event logs: a takeover voyage that arrived, whose controller never failed and whose tracker was working, counts as tracked. As-run, both runs showed exactly the C5 and electronics figures, because every limp-home arrival was being thrown away.
- **This flatters the controller.** It assumes 85% of normal speed, half the main box's failure rate, and no rudder or tail failures while it steers. All three are guesses. Read +12 as "large, probably 5–15 points", not as a measurement.

## What it is worth: simulator studies

The limp-home controller is now an option in the simulator (`limp_home` in the design, off by default): when the main box dies, it keeps steering toward Ireland at 85% of normal speed (fixed wing angle, simple steering), and fails at half the main box's rate because it is a small, separately potted board. Both factors are guesses. While it is in charge, rudder and tail failures are not rolled, which flatters it slightly.

Four runs, all 250 voyages on 2023 weather with the corrected simulator: Rev C5 as drawn (`run_fixed_compare_2023.bat`), with better-protected electronics (`run_electronics_2023.bat`), with the limp-home controller (`run_limp_2023.bat`), and with both (`run_limp_electronics_2023.bat`).

### Better-protected electronics

`simulator/run_electronics_2023.bat` runs Rev C5 with three changes, all **guesses** about what coating, potting and the encapsulated modem would achieve:

| | Now | Study |
|---|---|---|
| Electronics rate per day | 0.25% | 0.15% (×0.6) |
| Silent-modem rate per day | 0.11% | 0.06% (×0.5) |
| Electronics rate once water is inside | ×2.0 | ×1.3 |

Compare it with the Rev C5 step of `run_fixed_compare_2023.bat`, which uses the corrected simulator. Both are queued on Randolph's PC.

## Sources

- [RockBLOCK 9603 store page (humidity rating, not waterproof)](https://store.groundcontrol.com/products/rockblock-9603)
- [RockBLOCK Plus data sheet (fully encapsulated case)](https://www.groundcontrol.com/wp-content/uploads/2026/08/RockBLOCK-Plus-Data-Sheet.pdf)
- [Genasun waterproof controllers: potted electronics](https://www.gigaparts.com/genasun-waterproof-mppt-voltage-boosting-solar-controller-for-lead-acid-batteries.html)
- [Sensor potting: compound stress shifts calibration](https://incurelab.com/wp/?p=16596)
