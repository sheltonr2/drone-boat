# Solar-Sail Ocean Drone: Executive Summary

Nov 8, 2026 · @Randolph

## Bottom line

The plan is a 1.5 m, self-righting autonomous sailboat with a rigid wing sail. It reports by Iridium satellite and takes commands from shore, and it is meant to cross the North Atlantic from Nova Scotia or Newfoundland to Europe, then keep roaming.

- **Hardware cost:** about $2,280 sail-only, or about $1,990 after the trims in the budget section. The optional thruster adds $270. Satellite airtime adds $40–$60 a month.
- **Build time:** 9–13 months through five test gates. The realistic first ocean launch is June–July 2028; 2027 is possible only if every gate passes first time.
- **Odds:** about 10–20% that the first boat reaches Europe still sailing and reporting. Building a second boat and passing every gate raises that to about 30–40%. These are estimates, not calculations.
- **Biggest risks:** water getting in, steering failure, and fouling by weed or fishing line. Navigation and weather matter less.

## Boat at a glance

| Item | Value |
| --- | --- |
| Length overall | 1,500 mm |
| Beam / hull depth | 400 mm / 230 mm |
| Draft (waterline to bottom of bulb) | 558 mm |
| Height above waterline (top of wing) | 1,210 mm |
| All-up mass | about 21 kg |
| Ballast | 8.2 kg lead bulb, 320 mm long × 68 mm diameter |
| Keel fin | NACA 0012, 430 mm deep, 170 mm chord at the root and 150 mm at the tip |
| Rudder | NACA 0012 spade, 120 mm chord × 230 mm span, 12 mm 316 stock |
| Wing sail | NACA 0015, 1,000 × 300 mm (0.30 m²), free-rotating on a 25 mm carbon spar |
| Tail flap | NACA 0012, 120 × 200 mm, on a 600 mm boom |
| Solar | 2 panels of about 42 × 28 cm, about 40 W in total |
| Battery | 12.8 V 15 Ah LiFePO4 (192 Wh) |
| Average power draw | under 1.5 W |
| Comms | Iridium SBD, two-way; reports every 1–12 h |
| Access | 200 × 220 mm bolted, gasketed hatch (12 × M5) |

## Supplies

Everything below is needed for one boat. Prices are approximate US prices from November 2026; check them before ordering.

**Electronics and power**

| Item | Qty | Approx. size | Approx. USD |
| --- | --- | --- | --- |
| [RockBLOCK 9603 Iridium modem](https://www.sparkfun.com/rockblock-9603n-iridium-satcomm-module.html) + tails cable | 1 | small module | 285 |
| [Ground Control external Iridium patch antenna](https://store.groundcontrol.com/products/external-iridium-patch-antenna) | 1 | 1.8 m cable | 30 |
| [Holybro Pixhawk 6C Mini](https://pyrodrone.com/collections/everything-excluding-dji/products/holybro-pixhawk-6c-mini-model-a-flight-controller-only) (or a cheaper clone) | 1 | — | 80–177 |
| [Holybro Micro M10 GPS + compass](https://rcdrone.top/products/holybro-micro-m10-gps-module) | 1 | — | 37 |
| Adafruit Feather ESP32-S3 | 1 | — | 18 |
| AS5600 angle-sensor board + 6 × 2.5 mm diametric magnet | 1 | 26 mm recess | 10 |
| BME280 humidity sensor | 1 | — | 10 |
| [Blue Robotics SOS leak sensor](https://www.robotshop.com/products/sos-leak-sensor) | 1 | 4 probes | 35 |
| [Genasun GV-5-Li-14.2V MPPT charge controller](https://reach.dog/shop/build-the-power/products/genasun-gv-5-lithium-14-2-volt-mppt) | 1 | — | 104 |
| [Bioenno BLF-1215A LiFePO4 battery](https://www.bioennopower.com/collections/all/ebike-batteries?page=1), 12 V 15 Ah | 1 | about 180 × 77 × 167 mm | 150 |
| Saft LS33600 lithium D-cell + 5 V boost converter (backup power) | 1 | D-cell | 35 |
| ETFE semi-flexible solar panels, \~20 W | 2 | about 420 × 280 mm | 80 |
| [Savöx SW-1210SG waterproof servo](https://hillsborohobbyshop.com/products/savox-sw-1210sg) | 2 | 40.6 × 20.7 × 42 mm | 186 |
| 6-wire capsule slip ring | 1 | 12.5 mm diameter | 15 |
| [Blue Robotics T200 thruster + ESC](https://www.robotshop.com/products/bluerobotics-t200-thruster-w-basic-esc) (optional) | 1 | — | 270 |

**Hardware and fittings**

| Item | Qty | Approx. size | Approx. USD |
| --- | --- | --- | --- |
| Hammond 1554-series IP68 enclosure | 1 | \~240 × 160 × 90 mm | 40 |
| [Blue Robotics WetLink LC penetrators](https://www.robotshop.com/products/bluerobotics-wetlink-penetrator-lc-1-pack-m10-65-mm) (cable seals) | 4 | M10 | 52 |
| [Davis 151 emergency radar reflector](https://davisinstruments.com/products/emergency-radar-reflector) | 1 | 290 mm | 38 |
| 6805-2RS stainless bearings (mast) | 2 | 25 × 37 × 7 mm | 25 |
| S608-2RS stainless bearings (wind vane) | 2 | 8 × 22 × 7 mm | 12 |
| [igus iglide](https://www.igus.com/info/industries-marine) J flange bushings (rudder) | 2 | 12 mm ID × 14 mm OD | 20 |
| 316 rod: rudder stock | 1 | 12 mm × 420 mm | 20 |
| 316 rod: vane shaft | 1 | 8 mm × 75 mm | 5 |
| 316 threaded rod for keel bolts, with nuts | 2 | M10 × \~530 mm | 25 |
| G10 keel backing plate | 1 | 190 × 60 × 10 mm | 20 |
| 2 in. sch 40 PVC pipe (mast tube) | 1 | 60.3 OD × \~250 mm | 8 |
| Carbon tube: wing spar | 1 | 25 mm OD × 1,150 mm | 45 |
| Carbon tube: tail boom | 1 | 12 mm OD × \~650 mm | 15 |
| Carbon rods: tail pivot and alignment | 1 each | 6 mm and 3 mm | 10 |
| Aluminium or carbon tube: stern post | 1 | 20 mm OD × 500 mm | 15 |
| 316 fasteners (M3, M4, M5), 4 mm pins, set screws | kit | — | 30 |
| EPDM O-ring cord for the hatch | 1 | 4 mm × 1 m | 8 |
| 25 mm webbing + cam buckles (battery straps) | 2 | — | 12 |
| Marine tinned wire, inline fuses, connectors | kit | — | 40 |

**Build materials**

| Item | Qty | Use | Approx. USD |
| --- | --- | --- | --- |
| Divinycell H80 foam, 10 mm | \~1.5 m² | hull and deck strips | 120 |
| 6 oz E-glass cloth | \~6 m² | hull, deck, fin, rudder, wing skins | 70 |
| West System 105/205 epoxy + fillers (colloidal silica, microballoons) | \~1.5 kg kit | lamination, fillets, fairing | 130 |
| XPS foam blocks | \~0.05 m³ | wing and fin cores (hot-wire cut) | 25 |
| Lead (scrap or ingot) | \~8.5 kg | ballast bulb | 60 |
| Plaster of Paris or casting sand | \~10 kg | bulb mould | 15 |
| MDF or ply sheet for frames + strongback | 1 sheet | 9 frames, stem, strongback | 40 |
| Epoxy primer, barrier coat, hi-vis paint, antifouling | — | finishing | 60 |
| 3D-printer filament: ASA (\~0.8 kg) + PETG (\~0.8 kg) | 2 spools | 17 printed parts | 50 |

**Printed parts (files in the drawing set)**

These are the wind-vane housing, arm, cap and magnet holder; the antenna platform and transom bracket; the mast bearing housing and spar clamp; the tail servo housing and tail fin; the tiller arm, rudder servo mount and rudder blade core; the bulb casting pattern; the electronics tray; 4 battery strap anchors; and 4 penetrator pads.

**Tools and consumables you'll need**

Hot-wire foam cutter, oscillating or jig saw, random-orbit sander, drill and bits (to 12 mm), M3–M5 taps, soldering station, multimeter, a bench power supply with current readout, 3D printer (220 × 220 mm bed or larger), mixing cups, rollers, peel ply, release film, respirator with organic-vapour cartridges, nitrile gloves, and outdoor lead-casting gear (steel pot, burner, face shield, leather gloves).

## Budget and running costs

Itemised in full, the boat comes to about $2,280 sail-only, which is over the $2,000 target. Three trims, listed below the table, bring it to about $1,990. Tools you don't already own are extra.

| Category | Approx. USD |
| --- | --- |
| Electronics and power (sail-only) | 1,172 |
| Hardware and fittings | 440 |
| Build materials | 570 |
| Lake-test prototype (foam, scrap glass) | 100 |
| **Total, sail-only** | **\~2,280** |
| Optional T200 thruster | +270 |

**Getting under $2,000 (saves about $290)**

- Use a Pixhawk 6C clone: saves about $95.
- Drop the backup D-cell for version 1: saves $35. It still gets tracked through the main battery.
- Use one 1,000-credit airtime bundle at a time and buy epoxy and glass as a kit: about $40.
- Reuse the lake prototype's electronics and wing in the ocean boat: about $120 less in duplicate materials.

**Running costs**

| Item | Cost |
| --- | --- |
| [RockBLOCK line rental](https://groundcontrol.com/?p=1671) | $17/month |
| Message credits, at 4-hourly reports | about $22/month |
| Message credits, at hourly reports near coasts or in storms | about $86/month |
| Typical crossing (3–4 months) | about $120–$240 in total |

## Build and test timeline

There are five phases, and each ends at a gate. Don't move on until the boat passes, and don't skip a gate to make a launch window, because a missed June window costs a year.

1. **Bench rig (1–2 months).** Get the RockBLOCK, ESP32 and shore dashboard working on the desk, and the ArduPilot sailboat simulator running.
   - *Gate:* 7-day desk soak test, every command round-trips, average draw under 1.5 W.
2. **Lake prototype (2–3 months).** Build a cheap hull with the real electronics and wing, then tune tacking, wing trim and waypoint following.
   - *Gate:* 20 km autonomous course and 48 h unattended, with no manual takeover.
3. **Final ocean boat (3–4 months).** Build the composite hull, cast the bulb, pot the electronics and fit the final wing.
   - *Gate:* self-rights from 180° every time, and stays dry inside after 24 h fully submerged.
4. **Coastal trial (1–2 months).** Spend weeks offshore within recovery range, then recover and inspect it.
   - *Gate:* 3 weeks at sea unattended, with every fail-safe triggered and recovered.
5. **Ocean launch (June–July).** Launch from Nova Scotia or Newfoundland on a settled forecast. After landfall it switches to roaming mode.

## Things to watch out for

The top three entries in this table account for most lost ocean robots. That's where to spend build time.

| Risk | What to do |
| --- | --- |
| **Water getting in** through seals, the hatch or the enclosure | Keep penetrations to a minimum (4 WetLink seals). Bolt and O-ring the hatch, foam-fill the compartments, use leak sensors that trigger safe mode, and do the 24 h submerged test. |
| **Steering failure** (rudder or tail servo) | Run the rudder tube up above the waterline so it needs no seal. Use a balanced rudder and oversized bushings. Make sure the wing feathers safely if the tail fails. |
| **Fouling** by weed, fishing line or barnacles | Sweep back the keel and rudder leading edges, use antifouling paint, and don't fit an exposed propeller. |
| **Humidity killing the electronics** | Use desiccant and a humidity sensor, conformal-coat the boards, and pot the connectors. |
| **Running out of power** in long grey spells | Deep-sleep the electronics. Go to safe mode below 25% (heave-to, report every 12 h), and only run the thruster above 70%. |
| **Cold** further north | LiFePO4 must not be charged below 0 °C. Have the ESP32 cut charging below 2 °C, and mount the battery low, against the hull below the waterline. |
| **Ship strike, or capture by fishing boats** | Use hi-vis paint and a radar reflector, avoid shipping lanes with geofences, and fit an ID plate with your contact details. |
| **Software hang** | Use a hardware watchdog and boot into safe mode. The autopilot should keep sailing even if the ESP32 dies. |
| **Supplier parts not matching the drawings** | Measure servo tab spacing, the AS5600 board, the antenna footprint and the enclosure before printing the mounts. |
| **Lead casting** | Cast outdoors with a face shield and gloves, and keep the mould bone-dry: steam in a damp mould can make molten lead explode. Never pour lead into a 3D print. |
| **Legal liability** | An uncrewed roaming vessel is your responsibility. Check Transport Canada and Canadian Coast Guard rules for the launch and Irish/UK rules for the arrival, talk to a marine insurer, and publish the boat's live position. |

**Design numbers not yet verified by testing:** self-righting from 180°, the waterline at 21 kg, the wing's balance on the spar, and real-world solar output on a 40 cm deck.

## Odds of success

A first attempt has roughly a 10–20% chance of reaching Europe still sailing and reporting. These are judgment calls, anchored on the record of comparable boats.

| Scenario | Estimated odds |
| --- | --- |
| First boat reaches Europe, sailing and reporting | 10–20% |
| First boat reaches European waters at all, including as a tracked drifter | 20–30% |
| With a second hull and every gate passed | 30–40% |

**The reference point.** More than 30 teams tried the Microtransat crossing over 16 years ([Science Times](https://www.sciencetimes.com/articles/62633/20260922/robotic-sailboat-crosses-atlantic-after-traveling-5400-kilometers-without-human-intervention.htm)). Only two have finished. One sailed from Newfoundland to Ireland in 79 days in 2018 ([Slashdot / AP](https://hardware.slashdot.org/story/18/09/06/1719243/robot-boat-sails-into-history-by-finishing-atlantic-crossing)). The other was Oshen's 1.2 m C-Star, which crossed east to west in 127 days in 2026 ([Interesting Engineering](https://interestingengineering.com/transportation/tiny-autonomous-boat-crosses-atlantic-microtransat)). That's a base rate of about 5–7%.

**Why this boat should beat the base rate:** westerlies and the Gulf Stream push east even when the boat is drifting; you can command it from shore, which Microtransat rules forbid; and keeping the satellite link alive means a crippled boat still gets tracked.

**What raises the odds most**

1. Pass every gate, especially the 3-week unattended coastal trial.
2. Build two hulls: learn from the first loss, then launch the second.
3. Make leaks impossible rather than unlikely.
4. Launch in June so the crossing ends before the autumn gales.

## Open decisions

- [ ] Thruster in version 1, or sail-only? Sail-only saves $270 and removes a leak path.
- [ ] Accept going over budget (about $2,280), or take the trims to get to about $1,990?
- [ ] Lower the battery onto a hull-bonded cooling plate below the waterline? (Recommended.)
- [ ] Launch from Nova Scotia or Newfoundland. Newfoundland is about 1,000 km closer to Ireland.
- [ ] Who recovers the boat after the coastal trial, and how?

## Related documents and sources

- [Solar-Sail Ocean Drone: Build Plan](https://claude.ai/artifact/WmBHp596XyjBUHexcbbfRM): full architecture, comms protocol, software plan and parts rationale.
- Drawing set (Drawings.pdf), full-size templates and 3D-print files (Drone\_build\_files\_RevA.zip) were sent in the chat.
- [RockBLOCK 9603, SparkFun](https://www.sparkfun.com/rockblock-9603n-iridium-satcomm-module.html) · [Ground Control SBD pricing](https://groundcontrol.com/?p=1671)
- [Microtransat 2026 crossing, Science Times](https://www.sciencetimes.com/articles/62633/20260922/robotic-sailboat-crosses-atlantic-after-traveling-5400-kilometers-without-human-intervention.htm) · [Interesting Engineering](https://interestingengineering.com/transportation/tiny-autonomous-boat-crosses-atlantic-microtransat) · [2018 crossing, Slashdot / AP](https://hardware.slashdot.org/story/18/09/06/1719243/robot-boat-sails-into-history-by-finishing-atlantic-crossing)
