# Solar-Sail Ocean Drone: Build Plan

Nov 1, 2026 · @Randolph

## Mission and design targets

The plan is a 1.5 m sealed, self-righting sailboat. It sails west to east across the North Atlantic, then keeps roaming for as long as it survives. It reports by Iridium satellite and accepts commands from shore, and the hardware budget is under $2,000.

| Target | Value |
| --- | --- |
| Length overall | \~1.5 m (under the 2.4 m Microtransat small class) |
| Displacement | 15–25 kg, at least 40% of it in a ballast bulb |
| Primary propulsion | Rigid wing sail (no cloth to tear) |
| Backup propulsion | Small brushless thruster, used in calms only |
| Solar | 40–60 W of flexible panels on deck |
| Battery | \~200 Wh LiFePO4 (12.8 V, 15–20 Ah) |
| Average power draw | Under 1.5 W while sailing |
| Comms | Iridium SBD, two-way, a report every 1–6 h |
| Endurance goal | 6+ months, no maintenance |
| Route | Mid-Atlantic coast (Maryland, Virginia or New Jersey) to Europe, aiming for south-west Ireland; launch in May |

The launch date is open, so the plan is built around testing gates, not deadlines. A realistic first ocean attempt is May 2028, after a full year of lake and coastal trials. May 2027 is possible only if every trial passes on the first try.

## System architecture

The boat is designed so nothing needs to open at sea: every penetration is either a sealed shaft or a cable gland. Robustness matters more than performance. Every past failure has come from leaks, broken steering, or fouling.

**Hull and keel.** Build a narrow monohull in fiberglass over a foam core. A deep fin keel with a lead bulb makes it self-righting from 180°. Split the hull into two or three sealed compartments filled with closed-cell foam, so one leak can't sink it. Use a weed-shedding swept-back keel and rudder leading edges, because Sargassum and fishing line are common killers.

**Wing sail.** Use a free-rotating rigid wing with a small tail flap (the Saildrone approach). The wing weathervanes on its own, and a tiny servo on the tail sets the angle of attack. That takes a fraction of the power of winching a sail. Because the wing can always swing to point into the wind, the boat sheds load in a storm.

**Rudder.** Fit a single spade rudder on a stainless or carbon shaft through a lip-sealed bearing tube. Drive it with a sealed linear actuator or a worm-gear servo that holds position with no power. Rudder friction nearly ended the Oshen crossing, so oversize the bearings.

**Thruster.** Mount a sealed rim-drive or magnetically coupled thruster that needs no shaft seal. It runs only when the batteries are above 70% and the boat speed is under 0.5 knots.

**Power.** Laminate flexible 12 V panels into the deck and wing faces. Route them through an MPPT charge controller (Victron 75/10 or a Genasun GV-5) into a LiFePO4 pack with a cold-charge cutoff. Add a separate small primary lithium cell as a last-resort beacon supply.

**Electronics.** Mount everything in a sealed IP68 box potted to the hull, with desiccant packs and a humidity sensor. The parts are a Pixhawk-class autopilot, a GPS with a compass, a wind vane with an angle encoder, an ESP32 companion computer, and the RockBLOCK 9603 with an external antenna on the mast.

## Satellite comms and commanding

One RockBLOCK 9603 handles both directions, so commanding adds no hardware. Each time the boat wakes to send a report, the same Iridium session downloads any commands you've queued for it. Your commands reach the boat at its next report: within 1–6 hours, depending on the interval you set.

**How a command gets to the boat**

1. You type a command into your shore dashboard.
2. The dashboard encodes it, signs it, and posts it to Ground Control's RockBLOCK web API. The API queues it at the Iridium gateway (up to 270 bytes per message).
3. At its next scheduled report, the boat sends its status (up to 340 bytes) and receives the queued message in the same session.
4. The boat checks the signature and sequence number, applies the command, and confirms it in the next report.
5. Ground Control forwards every report to your server by webhook (an HTTP POST). The dashboard decodes it and plots the position.

**Status report (\~45 bytes, packed binary, 1 credit)**

Time, latitude/longitude, speed and heading, apparent wind angle and speed, battery voltage and state of charge, solar watts, wing and rudder angles, and internal humidity. It also carries leak sensor flags, mode, current waypoint index, last command sequence received, and fault bits.

**Command set (version 1)**

| Command | What it does |
| --- | --- |
| `SET_ROUTE` | Replace the waypoint list (up to \~20 points per message) |
| `GOTO` | Go to one point, then hold station |
| `MODE` | Switch between sail, sail+thrust, station-keep, drift/heave-to, and safe |
| `SET_REPORT` | Change the reporting interval (30 min to 24 h) |
| `THRUSTER_POLICY` | Set the battery threshold and maximum run time for the thruster |
| `GEOFENCE` | Add or clear keep-out zones (shipping lanes, coastlines) |
| `DIAG` | Request one detailed diagnostics packet |
| `REBOOT` | Restart the companion computer or the autopilot |

**Security and fail-safes**

- Each command carries an increasing sequence number and a 4-byte truncated HMAC-SHA256 signature made with a secret stored on the boat. If someone gets into your Ground Control account, they still can't steer the boat.
- The boat range-checks every value. A waypoint on land, or a report interval under 30 minutes, is rejected and flagged in the next report.
- The boat never depends on you. With no commands it keeps flying its last route. It goes to safe mode (heave-to, reports every 12 h) when the battery falls below 25% or a leak is detected.

**Airtime cost**

RockBLOCK line rental is [$17/month](https://groundcontrol.com/?p=1671). Credits cost $0.12–$0.20 each, and [one credit covers 50 bytes](https://core-electronics.com.au/rockblock-9603-with-usb-cable-iridium-satellite-modem-bundle.html). Checking for commands when none are waiting [also uses a credit](https://adafruit.com/product/4521). Piggyback every check on a report so you never pay for an empty mailbox check.

| Report interval | Credits/month | Approx. total/month |
| --- | --- | --- |
| Every 1 h | \~720 | \~$105 |
| Every 2 h | \~360 | \~$60 |
| Every 4 h | \~180 | \~$40 |
| Every 12 h (safe mode) | \~60 | \~$25 |

The totals assume 1,000-credit bundles and include line rental. Use 4-hour reports while crossing open ocean, then switch to hourly near coasts or in bad weather.

## Software plan

Use ArduPilot Rover's built-in sailboat mode for steering and sail trim. Your custom code, written with Claude Code, covers only the mission logic, power management and satellite link. That keeps the custom code small and testable.

| Layer | Runs on | Source | What it does |
| --- | --- | --- | --- |
| Autopilot | Pixhawk | ArduPilot Rover (stock, sailboat mode) | Steering, tacking, wing trim, waypoint following |
| Mission manager | ESP32 (MAVLink to the Pixhawk) | Custom, built with Claude Code | Route, weather avoidance, thruster policy, safe mode, watchdog |
| Comms | ESP32 + RockBLOCK | Custom | Packing reports, unpacking and verifying commands, scheduling |
| Power manager | ESP32 | Custom | Switches the Pixhawk, sensors and modem off between tasks; deep-sleep budget |
| Shore server | Small cloud service | Custom | Webhook receiver, decoder, command signer, database |
| Dashboard | Web page | Custom | Map track, charts, command form, alerts by email or text |

**Build order with Claude Code**

1. Define the report and command packet formats in one shared file, used by both the boat code and the shore server.
2. Write the shore server and dashboard first, and test them with a RockBLOCK on your desk.
3. Write the ESP32 comms and power manager. Measure real current draw at each step.
4. Run ArduPilot SITL (its software simulator) in sailboat mode. Drive it from the mission manager and replay real North Atlantic wind data.
5. Add the watchdogs: a hardware watchdog timer, a brown-out reset, and an automatic safe mode after any reboot.

## Recommended parts

Every part below runs on 12.8 V or 5 V and works with stock ArduPilot. The picks favour well-documented hobby and marine-robotics parts over the cheapest option. Prices are US street prices checked in November 2026 where linked. The rest are estimates and are marked with \~.

| Subsystem | Recommended part | Why this one | Price (USD) |
| --- | --- | --- | --- |
| Satellite modem | [RockBLOCK 9603](https://www.sparkfun.com/rockblock-9603n-iridium-satcomm-module.html) | Two-way Iridium SBD; huge example-code base; has an SMA port for an external antenna | 268 |
| Satellite antenna | [Ground Control External Iridium Patch Antenna](https://store.groundcontrol.com/products/external-iridium-patch-antenna) (2J7426MPz) | Passive, outdoor-rated, comes with a 1.8 m SMA cable; mount on the mast stub above the deck | 30 |
| Modem cable | [RockBLOCK 9603 Tails Cable](https://store.groundcontrol.com/collections/accessories) | Pre-stripped leads to wire straight to the ESP32 | 17 |
| Autopilot | [Holybro Pixhawk 6C Mini (Model A)](https://pyrodrone.com/collections/everything-excluding-dji/products/holybro-pixhawk-6c-mini-model-a-flight-controller-only) | H7 processor, IMU redundancy, supported by ArduPilot, rated −40 to 85 °C | 177 |
| GPS + compass | [Holybro Micro M10 GPS](https://rcdrone.top/products/holybro-micro-m10-gps-module) | u-blox M10, 4 constellations, IST8310 compass, small enough to fit in the enclosure lid | 37 |
| Companion computer | Adafruit Feather ESP32-S3 | Low deep-sleep current, two spare UARTs (Pixhawk + RockBLOCK), and good Arduino/PlatformIO support for Claude Code | \~18 |
| Wind vane sensor | AS5600 magnetic angle encoder + 3D-printed vane on a ceramic bearing | Contactless, so nothing wears out; reads the vane through a sealed cap | \~20 |
| Humidity/temperature sensor | Bosch BME280 breakout | Detects slow leaks and condensation before water pools | \~10 |
| Leak sensor | [Blue Robotics SOS Leak Sensor](https://www.robotshop.com/products/sos-leak-sensor) | Four probes for the bilge and enclosure; outputs a 3.3/5 V logic signal | 35 |
| Charge controller | [Genasun GV-5-Li-14.2V](https://reach.dog/shop/build-the-power/products/genasun-gv-5-lithium-14-2-volt-mppt) | 4S LiFePO4 profile, up to 65 W panels, 0.125 mA at night, rated −40 to 85 °C, 10-year warranty | 104 |
| Battery | [Bioenno BLF-1215A, 12 V 15 Ah LiFePO4](https://www.bioennopower.com/collections/all/ebike-batteries?page=1) | 192 Wh, which matches the 200 Wh target; compact and well known in ham-radio field use | 150 |
| Backup power | Saft LS33600 lithium D-cell + small 5 V boost converter, diode-ORed onto the comms rail | 17 Ah primary cell that can't be drained by charging faults; keeps the RockBLOCK reporting if the main pack dies | \~35 |
| Solar | Two \~20 W ETFE semi-flexible panels, about 42 × 28 cm each, wired in parallel | Must fit the deck: a [Renogy 50 W flexible](https://offgridstores.com/products/renogy-50-watt-12-volt-flexible-monocrystalline-solar-panel) is 67 × 51 cm, wider than the hull. ETFE resists salt and UV better than PET | \~80 |
| Thruster (optional) | [Blue Robotics T200 + Basic ESC](https://www.robotshop.com/products/bluerobotics-t200-thruster-w-basic-esc) | Flooded-motor design, so no shaft seal to leak; 316 stainless and polycarbonate | 270 |
| Rudder actuator | [Savöx SW-1210SG](https://hillsborohobbyshop.com/products/savox-sw-1210sg) waterproof servo | 20 kg·cm at 6 V, steel gears, IP67, 12-bit resolution | \~93 |
| Wing-tail actuator | Second Savöx SW-1210SG | Same part as the rudder, so one spare covers both | \~93 |
| Rudder bearings | [igus iglide](https://www.igus.com/info/industries-marine) J or T500 flanged bushings on a 316 stainless rudder stock | Self-lubricating, saltwater-proof, no grease to wash out | \~20 |
| Cable penetrations | [Blue Robotics WetLink Penetrator LC (M10)](https://www.robotshop.com/products/bluerobotics-wetlink-penetrator-lc-1-pack-m10-65-mm) × 4 | Rated to 95 m; no glue or potting; one each for solar, servos, antenna and sensors | 52 |
| Electronics box | Hammond 1554-series IP68 polycarbonate enclosure | NEMA 6P rated; UV-stabilized; screw-down gasket lid | \~40 |
| Radar reflector | [Davis Emergency Radar Reflector 151](https://davisinstruments.com/products/emergency-radar-reflector) | 11.5 in across and about 1 lb, which suits a 1.5 m boat | 38 |
| Hull | Divinycell H80 foam core (10 mm), 6 oz E-glass, West System 105/205 epoxy | Standard cored-composite layup; forgiving for a first-time builder | \~350 |
| Ballast | \~8 kg lead, cast into the keel bulb | Gives self-righting stability; scrap lead works | \~60 |
| Wing sail | XPS foam ribs + glass skin on a 25 mm carbon tube spar, two sealed 316 stainless bearings | Light, rigid, and weathervanes freely | \~120 |
| Wiring and safety | Marine tinned wire, inline fuses, hi-vis paint, ID plate | Bare copper corrodes within weeks at sea | \~60 |
| Testing | Lake-prototype hull (foam and fiberglass, rough finish) | Breaks first so the ocean boat doesn't | \~100 |

**Three changes to the architecture above, prompted by the parts**

- **Rudder seal:** run the rudder tube up above the waterline inside the hull. Then you don't need a lip seal at all, which removes one leak path.
- **Rudder actuator:** the Savöx is a hobby servo, so it holds position only while powered. Use a balanced rudder, with about 15% of its area ahead of the stock, so it needs little holding force. Cut its power between course corrections. A worm-gear drive is a version-2 upgrade.
- **Cold charging:** I couldn't confirm that the Bioenno pack has a low-temperature charge cutoff. North Atlantic surface water stays above freezing in summer, but have the ESP32 switch off solar input below 2 °C as a backstop.

**Added by the drawing set (Rev A)**

- **Slip ring:** the wing turns freely through 360°, so the tail servo's wires pass through a 6-wire, 12.5 mm capsule slip ring in the bottom of the spar (about $15).
- **Hull:** 400 mm beam, 230 mm deep, built from foam strips over 9 frames. The waterline sits at about 21 kg all-up.
- **Stern stub:** the antenna, wind vane and radar reflector go on a 20 mm tube on the transom. That keeps them clear of the tail as it sweeps round.

**Changed in Rev B (Nov 8, 2026)**

- **Wing counterweight:** the lead now sits in a printed pod (P18) on a 12 mm carbon arm, 300 mm forward of the spar axis, instead of in the wing's nose pocket. It needs about 0.8 kg of lead shot; the nose pocket would have needed about 7.6 kg, taking the boat to 27.5 kg.
- **Effect in the simulator:** the boat stays at about 21 kg with a stronger righting curve (GM 0.20 m vs 0.11 m). Crossings run about 4 days faster in identical weather (about 80 vs 84 days).
- **Parts:** spar clamp P08 gains a forward socket; new pod P18. Supplies add about 1 kg of lead shot and 246 mm more 12 mm carbon tube (about $10 extra).

**Changed: launch from the Mid-Atlantic (Nov 8, 2026)**

The boat now launches about 25 km off the Mid-Atlantic coast (Ocean City, Maryland by default) and aims for south-west Ireland; any landfall in Europe counts. The route rides the Gulf Stream and the North Atlantic Current and passes south of the Grand Banks at 42°N, 48°W. It is about 5,400 km instead of 3,000, and a May launch keeps most of it ahead of peak hurricane season.

| From Ocean City, MD to | Crossing time, no failures (May and June starts) |
| --- | --- |
| South-west Ireland | 99–100 days |
| Brittany or Cornwall | 98–99 days |
| Galicia, Spain | 125–126 days |
| Portugal | 139–144 days |

These come from the simulator on invented weather, without hurricanes. Virginia Beach and Cape May took 113–119 days to Ireland, but that gap comes from where the invented weather puts the Gulf Stream, so don't choose a launch site on it. With failures switched on, 51% of 100 voyages (April–July starts) reached Europe still reporting, against 47.5% from Newfoundland.

## Budget

The recommended parts total about $2,280 with the thruster and $2,010 without it. Both are over the $2,000 limit, so the boat needs to be sail-only plus one or two savings. Airtime is a separate running cost of $40–$60 a month.

| Configuration | Hardware total (USD) |
| --- | --- |
| All parts, including the T200 thruster | \~2,280 |
| Sail-only (no thruster) | \~2,010 |
| Sail-only + Pixhawk 6C clone + skip the backup D-cell | \~1,880 |

Other ways to save:

- Build the lake prototype from scrap foam instead of glass (save about $60).
- Use the RockBLOCK's built-in patch antenna for lake tests and buy the external antenna only for the ocean boat.
- Watch for sales: the Pixhawk and Genasun prices above swing by $20–$80 between sellers.

## Phased build and test plan

The work runs in five phases, and you should take about 9–13 months of build time before an ocean launch. Each phase ends at a gate, and you shouldn't move on until the boat passes it. If it fails, fix it and repeat the phase rather than launching early.

&#91;embedded content: build and test roadmap · 5 phases, 4 gates\]

The lake prototype is cheap on purpose. Its job is to break first, so the ocean boat doesn't. Ocean launches only make sense in May, ahead of hurricane season, so a missed gate costs a year. Plan the build to finish by early spring.

## Risks, failure modes, legal and safety

The boat is most likely to be lost to water getting in, steering failure, or fouling. Weather and navigation are less likely causes. Most of the build effort should go toward the first three rows below.

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| Water ingress through seals or the enclosure | High | No hatches; potted cable glands; foam-filled compartments; leak sensors trigger safe mode |
| Rudder or wing-tail actuator failure | High | Oversized bearings; worm-gear actuators that hold position with no power; wing designed to weathervane safely if the tail fails |
| Fouling by weed, fishing line or barnacles | High | Swept-back leading edges; antifouling paint; no exposed propeller (use a rim drive or ducted thruster) |
| Knockdown or rollover in a gale | Medium | Self-righting from 180°; rigid wing with no sheets; everything strapped down |
| Hurricane, or a gale against the Gulf Stream | Medium | Launch in May; follow the National Hurricane Center outlook and send a new route away from forecast tracks; self-righting with no sheets |
| Power starvation in a long overcast spell | Medium | Deep-sleep budget under 1.5 W; safe mode below 25%; thruster disabled below 70% |
| Collision with a ship | Low–medium | Hi-vis paint and radar reflector; avoid shipping lanes with geofences; consider an AIS transponder later |
| Software hang | Medium | Hardware watchdog; boots into safe mode; autopilot keeps sailing if the ESP32 dies |
| Theft or capture by fishers | Low | ID plate with contact details and a "research vessel" notice |

**Legal and responsibility**

- A roaming uncrewed vessel is your responsibility, including any harm it causes. Talk to a marine insurer before launch.
- Check the rules with the US Coast Guard for the launch, and with Irish, UK or French authorities for the arrival. Rules for small autonomous surface vessels are still evolving.
- Iridium modems are type-approved, so you don't need a radio licence for the RockBLOCK.
- Post the boat's live position publicly, as Microtransat teams do, so other mariners and authorities can see it.
