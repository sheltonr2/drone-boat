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
