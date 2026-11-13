# Rev D design changes and rationale

12 Nov 2026. Rev D is Rev C5 plus a backup steering system, protected electronics and an encapsulated modem. It was drawn first as "C6" and renamed the same morning: it adds a system, so it takes a new letter ([Revisions.md](Revisions.md)). Rev C history: [Design_RevC.md](Design_RevC.md).

## What changed from Rev C5

Randolph approved drawing the backup controller, with potting and the RockBLOCK Plus, after the electronics study ([Electronics_Review.md](Electronics_Review.md)).

- **Limp-home controller P21:** a small potted ESP32 board with its own GPS, tilt-compensated compass and fused 12 V feed, on the aft face of bulkhead x 300. If the main box's heartbeat stops for 10 minutes, it takes the starboard rudder and the wing tail and steers for the next waypoint. Full spec and logic: [Limp_Home_Spec.md](Limp_Home_Spec.md).
- **Switchover pod P22** on bulkhead x 1260: a 4-channel servo multiplexer and two ideal diodes. A dead backup hands the servos straight back to the Pixhawk. The port rudder stays wired to the Pixhawk alone, so the pod can never take both rudders.
- **RockBLOCK Plus in the hatch lid (bowl P23)** replaces the RockBLOCK 9603, its antenna on the stern post and the coax. It is factory-encapsulated and sits outside the box.
- **Main GPS moves to P05 on the stern post**, where the Iridium patch was. In the box it sat under the aft solar panel, which blocks satellite signals.
- **Coating and potting:** every board coated; sensors, power boards and wire joints potted; Pixhawk coated only ([Potting_Spec.md](Potting_Spec.md)).
- **Effect on the boat:** 27.8 kg (was 26.9), waterline z 104 mm, GM 0.182 m (was 0.188), maximum righting arm 0.36 m, still self-righting. Trim about 0.3° more bow-down.
- **Cost:** about +$365 (limp-home parts about $190, RockBLOCK Plus about $450 budgeted against $315 for the 9603, tails and patch antenna, compounds about $40). The RockBLOCK Plus price is not confirmed.
- **Changed:** sheets D00, D01, D03, D07, D08; new printed parts P21, P22, P23 (sheets D20, D21); P05 notes; template T16 (lid cut-out). Field Test N added ([Field_Tests.md](Field_Tests.md)). Not updated: `designs/revC_geometry.json` and the whole-boat STL.
- **In the simulator:** Rev D is the default. `limp_home.fitted` is on; `electronics_protection` multiplies the electronics failure rate by 0.6 and the modem-silence rate by 0.5; `hull.wet_electronics_factor` is 1.3. All three are **guesses** until Test J, Test N and the takeover trial at sea. Files saved before Rev D keep their old behaviour. The C5 study with both changes gave 61.2% arrivals (+13.2 points over C5, 95% range +8.7 to +17.7). `simulator/run_revD_2023.bat` checks Rev D as drawn, with its extra 0.9 kg.

## First run of Rev D as drawn (12 Nov 2026)

250 voyages, 2023 weather, launched 10 km off Ocean City, 1 May–15 June, same launch dates and seeds as the Rev C5 runs, so the differences are paired. Includes Rev D's extra 0.9 kg.

| | Rev C5 | C5 + limp-home + better electronics (study) | **Rev D as drawn** |
|---|---|---|---|
| Verified arrivals | 48.0% (41.9–54.2) | 61.2% (55.0–67.0) | **62.0% (55.8–67.8)** |
| Gain over C5 (paired) | — | +13.2 (+8.7 to +17.7) | **+14.0 (+6.5 to +21.5)** |
| Arrived still reporting | 33.6% | | 44.0% |
| Arrived, tracked by the YB3 | | | 18.0% |
| Lost | 15.2% | 12.8% | 11.2% |
| Aground | 11.2% | 7.2% | 7.2% |
| Still at sea on 30 Nov | 18.8% | | 18.4% |
| Median crossing | 119 days | 120 days | 120 days |

- **Rev D matches the study.** 62.0% against 61.2%, so the extra 0.9 kg costs nothing measurable, as the stability numbers suggested.
- **The backup took over on 47 voyages** (the main box died); 30 of those boats sailed in, tracked by the YB3, and only 3 went aground.
- **Electronics is no longer a leading first failure** (18 voyages, sixth). The top causes are now the rudder servos (65 jams or limp failures), the tail servo (34), fouling (32) and leaks (22). Those are the next things to work on.
- **The gains rest on guesses**: the electronics ×0.6 and modem ×0.5 rates, the wet factor of 1.3, the backup's 85% speed and half failure rate, and no rudder or tail failures blamed on the switchover. Bench Test N and the takeover trial at sea replace them.

Result: `results/2026-11-12_bulk_mc_2023_revD_10km.json`. Log: `collab/run_log_revD_2023_2026-11-12.txt`. The study's row is from the rescored run (see [Electronics_Review.md](Electronics_Review.md)); the blank cells were not recorded for it.
