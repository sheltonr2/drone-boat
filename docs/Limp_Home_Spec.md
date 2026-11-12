# Limp-home controller (Rev C6)

12 Nov 2026. Drawn on D03 (P21, P22), D00; parts P21 and P22 on the printed-parts sheets.

## Why

When the main electronics box dies today, the boat drifts. In the corrected-simulator runs (2023 weather, 250 paired voyages, `docs/Electronics_Review.md`), a backup that takes over steering raised arrivals from 48.0% to 59.6% (+11.6 points, 95% range +7.6 to +15.6). Together with coating and potting it reached 61.2%. Those gains rest on two guesses that the bench and water tests below must check: the backup sails at 85% of normal speed, and it fails at half the main box's rate.

## What it is

A small, separately powered and potted controller that does one thing: if the main box stops saying "I'm alive", it steers the boat toward the next waypoint with the starboard rudder and the wing tail.

| Item | Part | Note | USD |
|---|---|---|---|
| Processor | Adafruit Feather ESP32-S3 | Same board as the main box's companion, so one firmware toolchain | ~18 |
| Position | Holybro Micro M10 GPS | Same part as the main GPS. Off in standby; on after takeover | 37 |
| Heading and heel | Adafruit BNO085 9-axis sensor breakout | Tilt-compensated heading. A plain compass reads wrong when the boat heels | ~25 |
| Servo power | Pololu 6 V, 5.5 A step-down regulator (D36V50F6 or similar) | Set to about 5.8 V so the main 6.0 V supply carries the servos normally | ~25 |
| Isolation | 2 × optocoupler (6N137 class) | The heartbeat line in, the "takeover" flag out. A short in either box can't reach the other | ~4 |
| Supervisor | Voltage supervisor / external watchdog IC | Resets the ESP32 if it hangs or browns out | ~3 |
| Switchover | Pololu 4-channel RC servo multiplexer, assembled (item 2806), in pod P22 | See below | 10 |
| Power OR-ing | 2 × ideal-diode boards, in pod P22 | Either supply can run the starboard rudder and tail servos | ~10 |
| Feed | 2 A fuse at the battery terminal, its own cable and gland out of the battery box | Not through the main box's power switching | ~8 |
| Cases | P21 (controller), P22 (switchover pod), potting compound | `docs/Potting_Spec.md` | ~35 |
| Cable | 4-core signal cable from P21 to the main box and P22; 2-core feed | Starboard side of the dry bay | ~15 |
| **Total** | | | **~190** |

Mass about 0.37 kg with wiring (simulator: 0.22 kg at P21, 0.15 kg for the pod, feed and cable).

### Where it goes

- **P21** is bonded to the aft face of bulkhead x 300, its top edge about 10 mm under the deck, beside the hatch opening and clear of it (the battery box comes out through the opening). Its GPS and orientation sensor lie face-up on the shelf under the 2 mm top wall. They see the sky through the deck and the forward strip of the hatch lid. Nothing above them is carbon, metal or solar panel. It is 450 mm from the battery and 900 mm from the servos, which keeps the compass clean.
- **P22** is bonded to the forward face of bulkhead x 1260, starboard, beside the servo WetLink.
- The two muxed servos are the **starboard rudder** (y = −100) and the **wing-tail servo** (through the slip ring). The port rudder stays wired straight to the Pixhawk, so a failed pod can never take both rudders.

## How the switchover works

The multiplexer passes either its "master" inputs (from the Pixhawk) or its "slave" inputs (from the limp-home controller) to the two servos. A select pulse chooses which. The data sheets say [it switches between two independent sources using a separate channel as the selector](https://shop.pimoroni.com/en-au/products/pololu-4-channel-rc-servo-multiplexer). The select input is driven only by the limp-home controller. [If the select signal is lost or invalid, a FAILMODE jumper sets what the outputs do](https://servocity.com/4-channel-rc-servo-multiplexer).

- **Fit the FAILMODE jumper so a lost select signal gives the master (Pixhawk).** A dead or unpowered limp-home controller then hands the servos straight back to the main box. The backup can never strand the main system.
- The limp-home controller drives the select line to "slave" only after it has decided to take over.

**Servo power.** The main box's 6.0 V servo supply and the limp-home controller's 5.8 V regulator both feed the two muxed servos through ideal diodes in P22. Normally the main supply carries the load. If it dies, the backup takes over with no gap. The port rudder runs on the main supply only.

## Heartbeat and takeover logic

**Heartbeat.** The main box's companion ESP32 sends a short packet every second at 9600 baud, through an optocoupler, to the limp-home controller. It sends it only while its own checks pass (the Pixhawk answers when it should be on, and the main loop runs). Every few hours the packet also carries the current waypoint list. So the backup always follows the latest route, including route changes sent from shore. The companion stops the heartbeat on purpose if it judges the Pixhawk dead after its own power-cycle attempts.

**Standby.** The ESP32 sleeps and wakes once a minute to listen for 2 seconds. The GPS and orientation sensor are off (the GPS keeps its backup memory for a fast start). Target draw: under 3 mA at 12 V, about 1 Wh a day. Bench Test N measures it.

**Takeover** after 10 consecutive missed checks (about 10 minutes):

1. Power the GPS and orientation sensor; wait for a fix.
2. Drive the select line to "slave". Set a "takeover" flag back to the main box through the second optocoupler (the companion reports it if it is still able to).
3. **Steer.** Hold a heading toward the next waypoint with the starboard rudder, using tilt-compensated heading from the BNO085 and a GPS fix every 10 minutes. Advance waypoints as the main autopilot would.
4. **Wing tail.** The controller has no wind vane, so it finds the right tail side by trial: tail +8° for 10 minutes, then −8°, keeping whichever gives the better speed toward the waypoint. It repeats the test every 2 hours and after any large heading change.
5. **Upwind.** If speed toward the waypoint stays under 0.3 kn for 30 minutes, try headings 50° either side of the bearing and keep the better. Recheck every 2 hours.
6. **Storm.** If heel stays over 45° or the BNO085 sees repeated knockdowns, set the tail to 0 so the wing feathers, and steer 150° off the last good wind side until it settles.
7. **Hand back** after 30 minutes of unbroken heartbeat: release the select line, clear the flag, power down the GPS and sensor.

**What it does not do.** It has no modem. The YB3 keeps reporting the position, so shore sees a slower boat still heading for the waypoint. It does not tack precisely, and it does not avoid weather.

**Known risk.** If the Pixhawk dies holding the port rudder off centre, the backup has to steer against it. Bench Test N checks the boat can be held on course with the port rudder fixed at ±10°. If the servo can be programmed to go limp when its signal stops, set that for the port rudder.

## Software

About 600 lines on the ESP32, written with Claude Code: heartbeat receiver, takeover state machine, heading hold, tail test, waypoint follower, storm rule, logging to flash. Updates go over Wi-Fi at the dock, so the board can be potted without a programming connector. The firmware and the shore-side test harness live in the repo alongside the main code. Keep one programmed spare P21.

## Tests

- **Bench Test N** (`docs/Field_Tests.md`): switchover on the bench before potting, repeated after potting.
- **Shakedown:** during the 14-day shakedown, stop the heartbeat from shore for 2 hours in moderate wind and watch the YB3 and main tracks. Measure the speed toward the waypoint against the main autopilot's on the same leg. That number replaces the simulator's 0.85 guess.

## Sources

- [RockBLOCK Plus data sheet](https://www.groundcontrol.com/wp-content/uploads/2026/08/RockBLOCK-Plus-Data-Sheet.pdf)
- [Pololu 4-channel RC servo multiplexer, assembled (item 2806)](https://www.pololu.com/product/2806/specs)
- [Pololu multiplexer at Pimoroni (switching between two sources)](https://shop.pimoroni.com/en-au/products/pololu-4-channel-rc-servo-multiplexer)
- [Pololu multiplexer at ServoCity (FAILMODE behaviour)](https://servocity.com/4-channel-rc-servo-multiplexer)
