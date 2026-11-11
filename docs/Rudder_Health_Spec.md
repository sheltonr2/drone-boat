# Autopilot specification: detecting a sticking or failed rudder

11 November 2026, Rev C4. A specification for the companion computer (ESP32) code. Not yet written or tested.

## Why

Rudder trouble is the most common killer of small ocean boats in the published record. On the first boat to finish the autonomous Atlantic challenge, the rudder began responding erratically mid-ocean and the software detected and compensated for it. Rev C has two independent rudders, so the boat can lose one and carry on, but only if it notices.

## What it must do

1. **Estimate how well the boat is answering the helm.** Every 10 minutes while sailing, compare the turn the autopilot commanded with the turn the compass and GPS show.
2. **Decide which rudder is at fault.** Briefly steer on one rudder with the other centred, then swap.
3. **Act.** Stop using a bad rudder, centre it if it will move, steer on the good one, and report.

## Signals

| Signal | Source | Meaning |
|---|---|---|
| Heading response | Commanded rudder angle against yaw rate from the Pixhawk gyro, averaged over 10 minutes at boat speed above 0.3 knots | Response below 40% of the value learned in the shakedown test means the steering is degraded |
| Servo current | A current sensor (INA260 or similar) on each rudder servo's supply | Current above 1.5 A for more than 3 s without the boat turning means a jam or a stalled servo. Near-zero current when commanded means a dead servo or a broken wire |
| Course error | GPS course against the route | A steady error above 30° for 30 minutes with enough wind means the boat is not steering |

## Test sequence (run when any signal trips, and once a day)

1. Centre both rudders for 30 s. Record yaw rate.
2. Port rudder to +15° for 20 s, starboard centred. Record yaw-rate change and servo current.
3. Port rudder to −15° for 20 s. Record.
4. Repeat steps 2 and 3 with the starboard rudder.
5. A rudder passes if both directions turn the boat the right way by at least 40% of the shakedown value and its current stays under 1.5 A.

## Actions

| Result | Action |
|---|---|
| Both pass | Carry on. Log the response values |
| One fails, moves freely | Centre it and leave it centred. Steer on the other with the gain raised by 1.6. Report "RUD P" or "RUD S" in the next message |
| One fails, jammed off-centre | Stop driving it (cut its servo power to save the battery). Steer on the other with an offset to hold course. Report. If course cannot be held within 30°, feather the wing in winds above 12 m/s and report "RUD JAM" |
| Both fail | Feather the wing, report "NO STEER" every 6 hours, retest every 12 hours |

Retest a failed rudder every 24 hours: weed and line often clear themselves.

## Rules

- Never run the test in winds above 15 m/s or within 20 km of land.
- The test costs about 3 minutes of sailing and about 0.1 Wh.
- All thresholds are starting values. Set the 40% reference and the current limits from the lake and shakedown tests (Field Test I), and record them in the design file.
- A servo-saver (Rev C3) lets a blade be forced over without the servo moving. That looks like a failed response for a few seconds, so require two failed tests an hour apart before acting.

## Hardware this needs

- One current sensor per rudder servo (two INA260 boards, about $20). Not in the Rev C parts list yet.
- A power switch (MOSFET) on each rudder servo supply.

## In the simulator

Not modelled as a separate feature. The simulator already assumes the boat keeps steering on one rudder when the other fails, which is what this code has to make true.
