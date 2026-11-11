# Research review: comparable boats, ocean loads and materials

11 November 2026. What the published record and measurements say, checked against Rev C3, with the changes they suggest. Sources are linked at the end. Where a figure comes from my memory and not from a page I opened today, it says so.

## The three findings that matter most

1. **Measured data says my breaking-wave shock loads were too high, by about ten times in acceleration.** A drifting buoy in real 1–2 m breakers recorded sideways accelerations of about 1 g, not the tens of g my "wall of water" model gave. Rerun with strikes matched to that data, the stern post and the counterweight arm pass with margin. The wing spar and the rudder servos are unchanged, because they depend on speed and roll rate, not on shock. Details below; the Structural Review now carries a correction.
2. **A boat this size has now done it.** In September 2026 a 1.2 m boat finished the fully autonomous Microtransat class for the first time, after 127 days. Its builder's previous attempt ended when a storm destroyed the sail after 277 days. Sails and rudders, not hulls, are what the record shows failing.
3. **Stainless steel in stagnant seawater is a known trap,** and Rev C3 uses it in three such places: the mast bearings, the rudder stocks in their trunks, and the keel rods.

## 1. Comparable boats

| Boat | Size | Result | What failed or nearly did |
|---|---|---|---|
| Oshen C-Star PC13 (2026) | 1.2 m; reported 56 kg | Gran Canaria to Barbados, 2,926 nm in 127 days (0.96 knots average), fully autonomous; rode out a tropical storm with 9 m waves | Rudder began sticking mid-voyage; the software noticed and compensated. Its 2025 predecessor lost its sail in a storm after 277 days. Its 2023 attempt lasted 20 days |
| Offshore Sensing Sailbuoy Met (2018) | 2 m (about 60 kg, from memory) | Newfoundland to Ireland, 5,100 km in about 2.5 months, operator could re-route | — |
| Damon McMillan's solar boat (2025) | 2.6 m, 28 kg | California across the Pacific, 13,322 km in about 4 months at 1.5 m/s | Picked up by a fisherman near land; propeller chewed; one deck corner bent by an impact |
| SeaCharger (2016) | 2.3 m, 23 kg | California to Hawaii, then toward New Zealand | Rudder failed 482 km short after 155 days |
| Saildrone (7 m, professional) | 7 m | Many ocean crossings | Rolled by a breaking wave in 58-knot winds and 12 m seas; the wing broke in half |
| Educational Passages miniboats | 1.5 m, unpowered, fixed sail | Described by the organisers as usually crossing oceans and surviving hurricanes | Simple and heavy: keel filled with resin and sand |

What this says about our design:
- **Our predicted speed is realistic.** The simulator's median crossing is 130 days over about 5,700 km, which is 1.0 knot. C-Star averaged 0.96 knots.
- **Our weight is not excessive.** 27 kg at 1.5 m sits between McMillan's 28 kg at 2.6 m and C-Star's reported 56 kg at 1.2 m. The successful small boat is the heavy one.
- **Rudders and sails are the record's killers,** which matches the simulator's top causes (wing damage, steering, electronics). A Microtransat review names rudder servo failure and rudder loss as main causes of failure for small ocean craft, and recommends two steering actuators, actuators that hold position without power, watertight compartments with foam, and self-righting. Rev C already has all but the second.
- **Pickup near land is real.** Two of these voyages ended in a fisherman's hands.

## 2. Loads from the sea

### Breaking-wave strikes: model against measurement

A 40 cm, 18 kg spherical buoy with a motion sensor was put through real spilling and plunging breakers 1–2 m high (Brown and others, 2021). Mean peak values:

| | Spilling | Plunging |
|---|---|---|
| Sideways acceleration | 0.80 g | 1.18 g |
| Vertical acceleration | 1.3 g | 1.9 g |
| Rotation rate | 4.2 rad/s | 8.7 rad/s |

My strike simulation, for our boat in similar breakers:

| | Spilling | Plunging, "wall of water" model | Plunging, matched to the buoy data |
|---|---|---|---|
| Sideways acceleration | 1.1 g | 37 g | 2.5 g |
| Time to half the water's speed | 0.17 s | 0.010 s | 0.08 s |
| Roll rate | 2.6 rad/s | 3.5 rad/s | 3.3 rad/s |

Our hull has about 1.8 times the buoy's side area per kilogram, so 1.4 g and 2.1 g would be the like-for-like targets. The spilling model already matched. The plunging model did not: it treated the breaker as a solid wall hitting the whole hull side at once, which is right for a fixed pile and wrong for a 27 kg floating body.

Worst load in a 1-in-1,000 strike in 5 m seas, in N·m:

| Part | Strength (C2 / C3) | "Wall of water" | Matched to buoy data |
|---|---|---|---|
| Stern post | 115 / 185 | 194 / 108 | 40 / 22 |
| Counterweight arm | 53 / 119 | 61 | 20 |
| Keel-box joint | about 700 | 300 | 235 |
| Wing spar | 690 / 1,130 | 1,375 | 1,460 |
| Rudder servo | 2 stall | 9 | 9 |

- **Stern post and counterweight arm:** not fail points on this evidence. I told you and John that the post bent on most voyages; that was the model, not the sea.
- **Wing spar and rudder servos:** unchanged, and still the real risks.
- **Two cautions on the data.** The buoy's accelerations were filtered at 10 Hz, so a spike shorter than about a twentieth of a second would not show, and the stern post responds in about that time. And the buoy rolled two to three times faster than our simulated boat; a sphere has no keel, but if our roll rates are low the wing-slap load is too. Test L (shore break, logging at 400 Hz) answers both.
- **The C3 changes stay.** Fibreglass for the post and arm costs nothing and is more forgiving, and moving the YB3 off the post still removes a shared point of failure for collision and entanglement. But they were not the rescue the first numbers suggested.

### Other load checks

- **Small-craft standard (ISO 12215-5).** From memory of the standard, not checked against its text today: for a 27 kg sailing craft the bottom design pressure comes out near 24 kPa and the deck near 13 kPa. My hull checks used 37–52 kPa on the bottom and 33 kPa on the deck, so they are on the safe side of the standard.
- **How often waves break.** An open-sea study that matched whitecap sightings to buoy records found 10–16% of waves breaking, depending on wind. Our simulator's 3.5–4.5 knockdowns a day is a small fraction of those, which is the right order for breakers big enough to roll the boat.
- **Capsize threshold.** Unchanged: a breaking wave of about 55% of boat length (Southampton tests).

## 3. Materials

| Item in Rev C3 | What the record says | Proposed |
|---|---|---|
| **Mast bearings:** stainless 6806-2RS, at deck level in a tube that will hold salt water | Stainless bearings resist seawater only while fresh, oxygenated water flows over them; in a bearing-maker's immersion test a metal bearing rusted within hours, where a polymer one did not. Polymer ball bearings are immune but carry far less load | Keep ball bearings for low friction, but specify full 316 (not the usual 440 grade), packed with waterproof grease, a V-ring seal above the upper bearing and a drain hole at the foot of the mast tube. Add a free-rotation check to the shakedown test. A seized wing bearing removes the wing's only defence |
| **Rudder stocks:** 12 mm 316 in bushed trunks | Rudder shafts and keel bolts are the classic sites for crevice corrosion: 316 starved of oxygen in trapped water. One surveyor reports 25 mm 316 keel bolts eaten through in under ten years | Acceptable for one season. Grease the trunks, and inspect the stocks after the shakedown. For a boat meant to last years, titanium |
| **Keel rods:** M10 316 glued into the wooden fin and the lead | Same mechanism if water reaches them | Bed them fully in epoxy with no voids, and seal the wood end grain at the tip and tenon |
| **Fin core:** "white oak, ash or sapele" | West System's own tests found white oak bonds well given preparation: every shear sample broke in the wood, not the glue line. Their G/flex epoxy did best | Add to the drawing: sand to 80 grit and wipe twice with alcohol before gluing; use G/flex for the core glue line |
| **Hull core:** Divinycell H80 | Data sheet: shear strength 1.15 MPa nominal, 0.95 minimum | My sump-panel check used the nominal figure. On the minimum the safety factor is 1.8, not 2.2. The second inner ply already drawn in C3 covers it |
| **Foam fill and wing core:** XPS | Lower shear strength than PVC foam; fine as fill, poor as a structural core (the fin lesson) | No change: XPS carries no structure in C3 |
| **Printed parts** (ASA and PETG, some load-bearing) | Printed parts are weakest between layers; ASA chalks after six to eight months outdoors. This is maker-level evidence, not a study | Coat every exposed printed part with epoxy and paint. Check that the transom bracket (P06) is printed so the post's bending does not pull its layers apart |
| **Antifouling** | McMillan's boat used an ablative copper paint and came back nearly clean after four months at 1.5 m/s. Barnacles grow about 0.1 mm a day, faster in warm water and on idle hulls | We sail at a third of that speed, so fouling will be worse. Three coats of ablative copper paint on hull, fin, bulb and rudders; none on the bearings' running surfaces |
| **Glass laminate in seawater** | From general knowledge, not a page opened today: wet strength 10–20% below dry, and fatigue strength over a million cycles about a quarter of static | Already inside the 20–25% strength scatter the models use. No change |

## 4. Proposed design iterations

For your approval; nothing here is drawn.

1. **Mast bearings:** 316 bearings, grease, V-ring seal, mast-tube drain, and a rotation check in the shakedown test.
2. **Drawing notes:** oak preparation and G/flex for the fin; full epoxy bedding of the keel rods; epoxy and paint on printed parts; antifouling specification.
3. **Autopilot:** detect a sticking rudder from the mismatch between commanded turn and actual turn, and shift to the other rudder. C-Star's software did the equivalent and it saved the voyage.
4. **A shorter, wider wing:** the wing-slap load grows with about the fourth power of how far the tip is from the hull. A wing 0.8 m tall and 0.375 m wide has the same area and about 40% of the slap load. It would sail a little worse to windward. I have not run the speed model on it; say if you want that study.
5. **Simulator:** make the buoy-matched strike model the default. This is done in the repository, not on your PC, so the run you have going is not disturbed.

## Sources

- [Yacht: C-Star PC13 first autonomous boat across the Atlantic](https://www.yacht.de/en/yachts/small-cruiser/microtransat-challenge-c-star-pc13-became-the-first-autonomous-robotic-boat-to-cross-the-atlantic/)
- [Interesting Engineering: C-Star crossing](https://interestingengineering.com/transportation/tiny-autonomous-boat-crosses-atlantic-microtransat) and [video summary](https://interestingengineering.com/videos/how-this-4-foot-boat-crossed-the-atlantic-alone)
- [Yachting Monthly: Sailbuoy Met crossing](https://www.ybw.com/tag/unmanned-boats)
- [Blue Robotics forum: Pacific crossing by autonomous boat (McMillan, 2025)](https://discuss.bluerobotics.com/t/pacific-crossing-by-autonomous-boat/21369)
- [NZ Herald: SeaCharger rudder failure](https://nzherald.co.nz/nz/liberian-freighter-rescues-solar-powered-boat-on-historic-pacific-adventure-to-nz/K2NEF6EYZMJZHIROHKFUXTOME4)
- [Saildrone: Atlantic crossing and wing loss](https://saildrone.com/news/saildrone-completes-fastest-atlantic-crossing-unmanned-vehicle)
- [Educational Passages: miniboat building](https://educationalpassages.org/?p=116)
- [Microtransat fault-tree paper (CEUR Vol-2331)](https://ceur-ws.org/Vol-2331/paper2.pdf)
- [Brown and others, buoy accelerations in breaking waves, J. Mar. Sci. Eng. 9(2) 214](https://mdpi.com/2077-1312/9/2/214)
- [Statistics of breaking waves observed as whitecaps in the open sea](https://scilit.com/publications/47495ba3a03f0e97bb85c0d50096889e)
- [Boating NZ: crevice corrosion](https://www.pressreader.com/new-zealand/boating-nz/20160201/283145722734981); [Cruising World: stainless-steel corrosion](https://www.cruisingworld.com/how/beware-stainless-steel-corrosion)
- [SMB Bearings: are corrosion-resistant bearings waterproof](https://www.smbbearings.com/are-corrosion-resistant-bearings-waterproof); [igus: polymer against metal bearings under water](https://blog.igus.eu/?p=15033)
- [Epoxyworks: testing epoxy's adhesion to white oak](https://www.epoxyworks.com/?p=16340)
- [Diab Divinycell H data sheet](https://www.boatbuildercentral.com/MSDS/Diab-Divinycell-H-June-2020-rev19-SI.pdf)
- [I-Tech barnacle fouling study, via Benzinga](https://benzinga.com/z/23505279)
- [QIDI: outdoor lifespan of printed parts](https://qidi3d.com/blogs/print-lab/outdoor-lifespan-3d-printed-garden-mounts-guide)
