# Solar-Sail Ocean Drone: Executive Summary

Nov 8, 2026 (updated Nov 10 for Rev C) · @Randolph

## Bottom line

The plan is a 1.5 m, self-righting autonomous sailboat with a rigid wing sail (design Rev C, 10 Nov 2026: foam-filled hull, twin rudders, 30 mm spar). It reports by Iridium satellite and takes commands from shore, and it is meant to cross the North Atlantic from the Mid-Atlantic coast (Maryland, Virginia or New Jersey) to Europe, aiming for south-west Ireland, then keep roaming.

- **Hardware cost:** about $2,550 for Rev C, or about $2,290 after the trims in the budget section, plus about $630 for the backup tracker (YB3). Rev C adds about $260 over Rev B; there is no thruster. Satellite airtime adds $40–$60 a month, plus the tracker's own airtime.
- **Build time:** 9–13 months through five test gates. The realistic first ocean launch is May 2028; 2027 is possible only if every gate passes first time.
- **Odds:** about 10–20% that the first boat reaches Europe still sailing and reporting. Building a second boat and passing every gate raises that to about 30–40%. These are estimates, not calculations.
- **Biggest risks:** water getting in, steering failure, and fouling by weed or fishing line. Navigation and weather matter less.

## Boat at a glance

| Item | Value |
| --- | --- |
| Length overall | 1,500 mm |
| Beam / hull depth | 400 mm / 230 mm |
| Draft (waterline to bottom of bulb) | 570 mm |
| Height above waterline (top of wing) | 1,202 mm |
| All-up mass | about 25 kg (Rev C; Rev B was 21 kg) |
| Ballast | about 9.2 kg lead bulb, 320 mm long × 72 mm diameter |
| Keel fin | NACA 0012, 430 mm deep, 170 mm chord at the root and 150 mm at the tip. Rev C2: hardwood core, 6 × 6 oz glass and a carbon strip each side, 60 mm tenon into the keel box |
| Rudders | Two NACA 0012 spades, 100 mm either side of the centreline, each 120 mm chord × 230 mm span on a 12 mm 316 stock, with its own trunk and servo |
| Wing sail | NACA 0015, 1,000 × 300 mm (0.30 m²), free-rotating on a 30 × 22 mm carbon spar (Rev C3) on 6806 bearings 130 mm apart, balanced by about 0.8 kg of lead in a pod on a fibreglass rod 300 mm forward of the spar |
| Tail flap | NACA 0012, 120 × 200 mm, on a 600 mm boom |
| Solar | 2 panels of about 42 × 28 cm, about 40 W in total |
| Battery | 12.8 V 15 Ah LiFePO4 (192 Wh) |
| Average power draw | under 1.5 W |
| Comms | Iridium SBD, two-way; reports every 1–12 h |
| Access | 200 × 220 mm bolted, gasketed hatch (12 × M5) |
| Hull subdivision | Two glassed-in bulkheads; ends foam-filled, dry bay filled with removable foam blocks to leave 3 L or less of open space; battery in its own sealed box |
| Stern post | Radar reflector, YB3 backup tracker (P19), Iridium antenna, all-round white light (P20), wind vane |

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
| ETFE semi-flexible solar panels, \~20 W | 2 | about 420 × 280 mm | 80 |
| [Savöx SW-1210SG waterproof servo](https://hillsborohobbyshop.com/products/savox-sw-1210sg) | 3 | 40.6 × 20.7 × 42 mm | 279 |
| All-round white LED navigation light (12 V, about 0.3 W, 30 mm puck) | 1 | 30 mm | 25 |
| 6-wire capsule slip ring | 1 | 12.5 mm diameter | 15 |

**Hardware and fittings**

| Item | Qty | Approx. size | Approx. USD |
| --- | --- | --- | --- |
| Hammond 1554-series IP68 enclosure | 1 | \~240 × 160 × 90 mm | 40 |
| [Blue Robotics WetLink LC penetrators](https://www.robotshop.com/products/bluerobotics-wetlink-penetrator-lc-1-pack-m10-65-mm) (cable seals; 2 of them in the aft bulkhead) | 6 | M10 | 78 |
| [Davis 151 emergency radar reflector](https://davisinstruments.com/products/emergency-radar-reflector) | 1 | 290 mm | 38 |
| 6806 acetal ball bearings with glass balls (mast, Rev C4) | 2 | 30 × 42 × 7 mm | 30 |
| O-rings 42 × 1.5, V-ring VA-30, Delrin collar 30 mm bore (mast, Rev C4) | 1 set | — | 15 |
| Current sensor and MOSFET switch per rudder servo (Rev C4) | 2 | INA260 or similar | 25 |
| S608-2RS stainless bearings (wind vane) | 2 | 8 × 22 × 7 mm | 12 |
| [igus iglide](https://www.igus.com/info/industries-marine) J flange bushings (rudders) | 4 | 12 mm ID × 14 mm OD | 40 |
| 316 rod: rudder stocks | 2 | 12 mm × 360 mm | 30 |
| Rudder lip seals + rubber boots (trunk tops) | 2 | 12 mm shaft | 15 |
| 316 rod: vane shaft | 1 | 8 mm × 75 mm | 5 |
| 316 threaded rod for keel bolts, with nuts | 2 | M10 × \~580 mm | 25 |
| G10 keel backing plate | 1 | 122 × 60 × 10 mm | 20 |
| 2 in. sch 40 PVC pipe (mast tube) | 1 | 60.3 OD × \~250 mm | 8 |
| Carbon tube: wing spar (Rev C3) | 1 | 30 × 22 mm × 1,195 mm | 95 |
| Carbon tube: tail boom | 1 | 12 mm OD × 600 mm | 10 |
| Solid pultruded fibreglass rod: counterweight arm (Rev C3) | 1 | 12 mm × 246 mm | 8 |
| Spring servo-savers for the rudder servos (Rev C3) | 2 | 25T spline, 1/8-scale RC car type | 20 |
| Carbon rods: tail pivot and alignment | 1 each | 6 mm and 3 mm | 10 |
| Pultruded fibreglass tube: stern post (Rev C3) | 1 | 20 mm OD × 2 mm wall × 500 mm | 15 |
| 316 fasteners (M3, M4, M5), 4 mm pins, set screws | kit | — | 30 |
| EPDM O-ring cord for the hatch and battery box | 1 | 4 mm × 2 m | 12 |
| 25 mm webbing + cam buckles (battery straps) | 2 | — | 12 |
| Marine tinned wire, inline fuses, connectors | kit | — | 40 |

**Build materials**

| Item | Qty | Use | Approx. USD |
| --- | --- | --- | --- |
| Divinycell H80 foam, 10 mm | \~1.5 m² | hull and deck strips | 120 |
| 6 oz E-glass cloth | \~6 m² | hull, deck, fin, rudder, wing skins | 70 |
| West System 105/205 epoxy + fillers (colloidal silica, microballoons) | \~1.5 kg kit | lamination, fillets, fairing | 130 |
| XPS foam blocks | \~0.05 m³ | wing core (hot-wire cut) | 25 |
| Hardwood planks (white oak, ash or sapele), straight-grained | 2 | 12 × 180 × 500 mm, for the keel fin core (Rev C2) | 30 |
| Unidirectional carbon strip or tape | \~1.1 m | 60 mm wide, 1.5 mm thick built up; keel fin faces (Rev C2) | 35 |
| Marine plywood, 9 mm | 1 | 400 × 200 mm, keel-box floors (Rev C2) | 10 |
| XPS foam board, 25–50 mm | \~0.06 m³ (60 L) | hull fill: forward and aft spaces, removable dry-bay blocks | 40 |
| Battery box: foam, glass, M5 inserts | — | sealed box with O-ring lid | 15 |
| Lead (scrap or ingot) | \~9.5 kg | ballast bulb (Rev C, D72) | 67 |
| Lead shot | \~1 kg | wing counterweight pod (P18), set in epoxy | 10 |
| Plaster of Paris or casting sand | \~10 kg | bulb mould | 15 |
| MDF or ply sheet for frames + strongback | 1 sheet | 9 frames, stem, strongback | 40 |
| Epoxy primer, barrier coat, hi-vis paint, antifouling | — | finishing | 60 |
| 3D-printer filament: ASA (\~0.8 kg) + PETG (\~0.8 kg) | 2 spools | 20 printed parts | 50 |

**Printed parts (files in the drawing set)**

These are the wind-vane housing, arm, cap and magnet holder; the antenna platform and transom bracket; the mast bearing housing and spar clamp; the tail servo housing and tail fin; two each of the tiller arm, rudder servo mount and rudder blade core; the bulb casting pattern; the electronics tray; 4 battery strap anchors; 4 penetrator pads; the wing counterweight pod; and (Rev C) the YB3 platform and the navigation-light clamp.

**Tools and consumables you'll need**

Hot-wire foam cutter, oscillating or jig saw, random-orbit sander, drill and bits (to 12 mm), M3–M5 taps, soldering station, multimeter, a bench power supply with current readout, 3D printer (220 × 220 mm bed or larger), mixing cups, rollers, peel ply, release film, respirator with organic-vapour cartridges, nitrile gloves, and outdoor lead-casting gear (steel pot, burner, face shield, leather gloves).

## Budget and running costs

Itemised in full, Rev C comes to about $2,550, plus about $630 for the YB3 backup tracker. That is over the $2,000 target. The trims below the table bring the boat to about $2,290 (about $2,920 with the tracker). Tools you don't already own are extra.

| Category | Approx. USD |
| --- | --- |
| Electronics and power (Rev C: second rudder servo, nav light; no backup D-cell) | 1,255 |
| Hardware and fittings (Rev C: twin rudder bushings and stocks, 6806 bearings, 30 mm spar, 2 more WetLinks, trunk seals) | 550 |
| Build materials (Rev C: XPS hull fill, battery box, 1 kg more lead) | 642 |
| Lake-test prototype (foam, scrap glass) | 100 |
| **Total, Rev C** | **\~2,550** |
| YB3 backup tracker (decided 9 Nov; hardware, check current price) | +630 |

**Getting to about $2,290 (saves about $255)**

- Use a Pixhawk 6C clone: saves about $95.
- (The backup D-cell is gone in Rev C: the YB3 backup tracker does its job.)
- Use one 1,000-credit airtime bundle at a time and buy epoxy and glass as a kit: about $40.
- Reuse the lake prototype's electronics and wing in the ocean boat: about $120 less in duplicate materials.

**Running costs**

| Item | Cost |
| --- | --- |
| [RockBLOCK line rental](https://groundcontrol.com/?p=1671) | $17/month |
| Message credits, at 4-hourly reports | about $22/month |
| Message credits, at hourly reports near coasts or in storms | about $86/month |
| Typical crossing (about 100–125 days) | about $130–$260 in total |

## Build and test timeline

There are five phases, and each ends at a gate. Don't move on until the boat passes, and don't skip a gate to make a launch window, because a missed May window costs a year.

1. **Bench rig (1–2 months).** Get the RockBLOCK, ESP32 and shore dashboard working on the desk, and the ArduPilot sailboat simulator running.
   - *Gate:* 7-day desk soak test, every command round-trips, average draw under 1.5 W.
2. **Lake prototype (2–3 months).** Build a cheap hull with the real electronics and wing, then tune tacking, wing trim and waypoint following.
   - *Gate:* 20 km autonomous course and 48 h unattended, with no manual takeover.
3. **Final ocean boat (3–4 months).** Build the composite hull, cast the bulb, pot the electronics and fit the final wing.
   - *Gate:* self-rights from 180° every time, and stays dry inside after 24 h fully submerged.
4. **Coastal trial (1–2 months).** Spend weeks offshore within recovery range, then recover and inspect it.
   - *Gate:* 3 weeks at sea unattended, with every fail-safe triggered and recovered.
5. **Ocean launch (May).** Launch it about 10 km (5.5 nm) off Ocean City Inlet, Maryland, from a small boat, on a forecast with at least three days of offshore (westerly) wind. Escort it for the first few hours and recover it if it fails in the first week. After landfall it switches to roaming mode.

## Things to watch out for

The top three entries in this table account for most lost ocean robots. That's where to spend build time.

| Risk | What to do |
| --- | --- |
| **Water getting in** through seals, the hatch or the enclosure | Rev C makes a leak survivable: two bulkheads, the hull foam-filled so 3 L or less can flood, the battery in its own sealed box. Still keep penetrations few, bolt and O-ring the hatch, use leak sensors that trigger safe mode, pressure-test each space and do the 72 h submerged test. |
| **Steering failure** (rudder or tail servo) | Rev C has two rudders, each with its own servo: either one steers alone. Seal the trunk tops (they go under in a knockdown). Use balanced rudders and oversized bushings. Make sure the wing feathers safely if the tail fails. |
| **Fouling** by weed, fishing line or barnacles | Sweep back the keel and rudder leading edges and use antifouling paint. (There is no propeller in Rev C.) |
| **Humidity killing the electronics** | Use desiccant and a humidity sensor, conformal-coat the boards, and pot the connectors. |
| **Running out of power** in long grey spells | Deep-sleep the electronics. Go to safe mode below 25% (heave-to, report every 12 h). |
| **Hurricanes** and Gulf Stream storms | Hurricane season runs June to November and peaks mid-August to mid-October. Launch in May so the boat is well east before the peak, watch the National Hurricane Center outlook, and send a new route to steer it away from forecast tracks. Wind against the Gulf Stream builds steep, breaking seas: the simulator gives about 5 times as many knockdowns on this route as from Newfoundland. Keep the ESP32 cutting charging below 2 °C. |
| **Ship strike, or capture by fishing boats** | Use hi-vis paint and a radar reflector, avoid shipping lanes with geofences, and fit an ID plate with your contact details. |
| **Software hang** | Use a hardware watchdog and boot into safe mode. The autopilot should keep sailing even if the ESP32 dies. |
| **Supplier parts not matching the drawings** | Measure servo tab spacing, the AS5600 board, the antenna footprint and the enclosure before printing the mounts. |
| **Lead casting** | Cast outdoors with a face shield and gloves, and keep the mould bone-dry: steam in a damp mould can make molten lead explode. Never pour lead into a 3D print. |
| **Legal liability** | An uncrewed roaming vessel is your responsibility. Check US Coast Guard rules for the launch and the rules wherever it lands (Ireland, the UK or France), talk to a marine insurer, and publish the boat's live position. |

**Design numbers not yet verified by testing:** self-righting from 180°, the waterline at about 26.9 kg (z 102 mm), the wave-strike loads (breaker test L), the keel fin and its joint (proof test K), the 3 L free-flood volume, the wing's balance on the spar, and real-world solar output on a 40 cm deck.

## Odds of success

A first attempt has roughly a 10–20% chance of reaching Europe still sailing and reporting. These are judgment calls, anchored on the record of comparable boats. The longer route (about 5,400 km instead of 3,000) and hurricane season put it toward the lower end.

| Scenario | Estimated odds |
| --- | --- |
| First boat reaches Europe, sailing and reporting | 10–20% |
| First boat reaches European waters at all, including as a tracked drifter | 20–30% |
| With a second hull and every gate passed | 30–40% |

**The reference point.** More than 30 teams tried the Microtransat crossing over 16 years ([Science Times](https://www.sciencetimes.com/articles/62633/20260922/robotic-sailboat-crosses-atlantic-after-traveling-5400-kilometers-without-human-intervention.htm)). Only two have finished. One sailed from Newfoundland to Ireland in 79 days in 2018 ([Slashdot / AP](https://hardware.slashdot.org/story/18/09/06/1719243/robot-boat-sails-into-history-by-finishing-atlantic-crossing)). The other was Oshen's 1.2 m C-Star, which crossed east to west in 127 days in 2026 ([Interesting Engineering](https://interestingengineering.com/transportation/tiny-autonomous-boat-crosses-atlantic-microtransat)). That's a base rate of about 5–7%.

**Why this boat should beat the base rate:** westerlies and the Gulf Stream push east even when the boat is drifting; you can command it from shore, which Microtransat rules forbid; and keeping the satellite link alive means a crippled boat still gets tracked. The simulator, on invented weather without hurricanes, first gave 51% (95% range 41–61%) on the Mid-Atlantic route against 47.5% from Newfoundland. With failure rates refitted to the Microtransat record (Nov 8, 2026; see docs/Failure_Rates.md in the repo), it gives 37% (28–47%) if the coastal trial is passed and the build's safeguards work, and 22% (15–31%) at the record's own rates. Even the second figure is an upper bound, because the simulator is still too kind after day 60. Crossings take about 102 days instead of 82, and about 6% of boats were disabled early and drifted ashore in Nova Scotia, New England or Newfoundland. Read those as a comparison between routes, not as real odds.

**What raises the odds most**

1. Pass every gate, especially the 3-week unattended coastal trial.
2. Build two hulls: learn from the first loss, then launch the second.
3. Make leaks impossible rather than unlikely.
4. Launch in May, so most of the crossing is done before the peak of hurricane season and the autumn gales.

## Open decisions

- [x] Thruster in version 1, or sail-only? Decided 10 Nov 2026 (Rev C): sail-only, no thruster provision.
- [ ] Accept going over budget (Rev C about $2,550 plus the YB3), or take the trims to get to about $2,290 plus the YB3?
- [ ] Lower the battery onto a hull-bonded cooling plate below the waterline? (Recommended.)
- [ ] Launch site: Ocean City, Maryland (the default), Virginia Beach or Cape May. In the simulator they came out within about two weeks of each other, so choose on access, ship traffic and distance to the Gulf Stream. Decided 10 Nov 2026: launch near the coast (about 10 km off the inlet) to keep the boat trip short, and manage the risk of an early failure drifting ashore with an offshore-wind launch rule, an escort and early recovery ([Launch_Plan.md](Launch_Plan.md)).
- [ ] Target: south-west Ireland (the default; any European landfall also counts). Brittany or Cornwall take about as long but sit beside the busiest shipping lanes in Europe. Galicia or Portugal take 3–6 weeks longer. Decide too whether a landfall in the Azores counts.
- [ ] Who recovers the boat after the coastal trial, and how?

## Related documents and sources

- [Solar-Sail Ocean Drone: Build Plan](https://claude.ai/artifact/WmBHp596XyjBUHexcbbfRM): full architecture, comms protocol, software plan and parts rationale.
- Drawing set (Drawings.pdf), full-size templates and 3D-print files (Rev B, with the wing counterweight pod) are in the private drone-boat repository on GitHub, in the build-files folder.
- [RockBLOCK 9603, SparkFun](https://www.sparkfun.com/rockblock-9603n-iridium-satcomm-module.html) · [Ground Control SBD pricing](https://groundcontrol.com/?p=1671)
- [Microtransat 2026 crossing, Science Times](https://www.sciencetimes.com/articles/62633/20260922/robotic-sailboat-crosses-atlantic-after-traveling-5400-kilometers-without-human-intervention.htm) · [Interesting Engineering](https://interestingengineering.com/transportation/tiny-autonomous-boat-crosses-atlantic-microtransat) · [2018 crossing, Slashdot / AP](https://hardware.slashdot.org/story/18/09/06/1719243/robot-boat-sails-into-history-by-finishing-atlantic-crossing)
