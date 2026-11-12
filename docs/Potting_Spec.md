# Coating and potting (Rev D)

12 Nov 2026. Why: `docs/Electronics_Review.md`. In the simulator this is worth about 5 points of arrivals, but only if the guessed factors hold (electronics failures ×0.6, modem ×0.5, wet-bay factor 1.3 instead of 2.0). Rev D now carries those factors in the design (`electronics_protection`, `wet_electronics_factor`).

## What gets what

| Item | Treatment | Compound |
|---|---|---|
| Every board in the main box (Pixhawk, companion ESP32, sensor boards) | Conformal coat, 2 coats | Acrylic or urethane spray. On the Pixhawk, mask the connectors, barometer port and SD slot |
| Wind-vane angle sensor (AS5600) | Pot completely | Soft silicone. The magnet stays outside on the vane shaft |
| Main GPS + compass on P05 | Pot, with care | Soft silicone, no more than about 3 mm over the antenna. Recalibrate the compass afterwards |
| DC-DC converters, fuses, power distribution | Pot | Thin, heat-conducting urethane |
| Wire joints and the inside ends of the cable penetrators | Pot | Adhesive-lined heat-shrink, then urethane in a small mould |
| Solar charge controller (Genasun) | Buy factory-potted | Confirm the GV-5 variant ordered is a potted one |
| Satellite modem | **Replaced** by the RockBLOCK Plus, outside the box in the hatch lid (P23) | Factory-encapsulated |
| Limp-home controller P21 and switchover pod P22 | Pot completely | Silicone round the GPS and orientation sensor, urethane to the rim (`docs/Limp_Home_Spec.md`) |
| Pixhawk | Coat only, never pot | Needs its barometer port, SD card, USB and soft-mounted motion sensors |
| Battery management board | Neither | Stays in the sealed battery box; potting traps heat |
| Servos | Neither | Bought sealed (IP67) |

## The RockBLOCK Plus

The [data sheet](https://www.groundcontrol.com/wp-content/uploads/2026/08/RockBLOCK-Plus-Data-Sheet.pdf) gives 137 mm diameter × 40 mm high, 450 g with the 3 m cable, a 9-30 V DC supply, 225 mA maximum input current, and RS-232 serial at 19200 baud. It has four M5 threaded mounting inserts, an integrated 1621 MHz patch antenna, and an operating range of -40°C to +85°C. The data sheet is inconsistent on sealing: the spec table lists IP67, but the features section says IP68 with submersion to 3 m for 30 minutes. Plan on IP67.

- It runs straight off the 12.8 V battery. It needs an RS-232 level shifter (a MAX3232-class board) at the companion ESP32 in place of the 9603's logic-level link.
- It replaces the RockBLOCK 9603, its tails cable, the external patch antenna on the stern post and that antenna's cable. One fewer coax run, and the modem is no longer in the box's humid air.
- Price: not confirmed (Ground Control's store didn't list it when checked). Budgeted at about $450 until a quote is in hand.

## Process

1. **Only after the 14-day shakedown**, so faults are found while the boards can still be reworked. A potted board can't be repaired: keep one programmed spare of each.
2. Clean the boards (isopropyl alcohol), bake at 50 °C for 2 hours to drive off moisture, coat, then cure for the full time on the label.
3. Pot in a dry room. Degas or pour slowly from one corner to avoid trapped air over the parts.
4. Run every potted item for 24 hours, then soak it 1 m under water for 24 hours and run it again before installing.
5. Recalibrate both compasses with the boat fully rigged.

Heat is not a concern: the whole main box dissipates about 1–2 W.

## Mass and cost

About 0.15 kg of compound and coating in all. About $40 in compounds and spray. The RockBLOCK Plus swap adds about 0.4 kg (450 g in, about 90 g of modem, antenna and cable out).
