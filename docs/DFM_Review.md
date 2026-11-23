# Design-for-manufacture review (Rev E2)

19 Nov 2026. Randolph asked for every design plan to be checked from a hobbyist builder's point of view: detailed drawings for everything, 3D-printed parts designed for printing with files available, and a complete bill of materials with purchase links.

The shape, mass and performance of the boat are unchanged. Rev E2 is a set of part fixes and new drawings, so it takes a numbered sub-revision (docs/Revisions.md).

## 1. What was checked

- **Drawings.pdf, all 23 sheets.** For each part I asked whether a builder could make it from the sheets alone.
- **All 29 STL files.** Each was checked for size against common printer beds. Every downward-facing surface was found from the mesh normals, to spot unsupported overhangs and bridges. I also checked how each part goes together with its bearings, shafts and fasteners.
- **Every bought-in item named anywhere.** I searched the notes, design.py, the parts list in the Build Plan, and the Rev D, Rev E, limp-home and potting specs. I then looked for a real product page for each.
- **The wiring.** The specs describe it in words only, and I traced it end to end.

## 2. Problems found and fixed

| # | Problem | Fix (E2) |
|---|---|---|
| 1 | **P01 vane housing: the lower bearing could not be fitted.** Its 22 mm seat was closed in, with a 12 mm hole above and a 2 mm web below. The notes said "press in from the top", but a 22 mm bearing cannot pass a 12 mm hole. | Now one D22.1 bore from the top, z 36–60. Fit the lower bearing, then the **new spacer P27**, then the upper bearing. The bearings sit where they did before. |
| 2 | **P07 mast bearing housing.** Printed flange-down, the shoulder over the bottom bearing seat was a 6 mm ledge with nothing under it. The bearing seats against that ledge. | The shoulder is now 2.5 mm flat, then a 45° cone up to the catcher land. The lower land moves to z 10.5–30.5 and stays 20 mm long. No supports are needed. |
| 3 | **P03 sensor cap.** The D40 flange stuck out 6 mm over the D28 socket. | A 45° chamfer under the flange. The mating face is on top and is unchanged. |
| 4 | **P12 rudder servo cradle.** Its base was 110 × 64, but the foam pocket it bonds into is 100 × 56. | The base is now 96 × 52. The cradle walls are unchanged. |
| 5 | **P10 tail fin.** The detent needs a 6 × 1 steel disc in the fin root, but the part had nowhere to put it. | A D6.2 × 1.2 pocket on the root face of P10a, 54 mm from the leading edge (r 30 from the pivot). |
| 6 | **P02 vane arm is 275 mm long.** It fits a 230 × 230 bed only diagonally, so it will not fit the common 220 × 220 bed. | P02 is kept. A split version, **P02A + P02B**, fits any 220 bed: the arm slides into a 50 mm sleeve and is held with epoxy and an M3 bolt. |
| 7 | **Hole fits depend on the printer.** A bore that is 0.2 mm tight on one printer is loose on another. | New **fit coupons**: P00a has all 14 vertical bore sizes and P00b the three horizontal teardrop sockets. Print them first (D33). |
| 8 | **P05 antenna platform.** The D42 GPS pocket is on the bed side, so its roof is a 42 mm bridge 1.5 mm off the bed. | Kept as is. Print it with supports touching the build plate only (Print_Guide.csv). |
| 9 | **No wiring drawing.** Nothing said how anything was connected, fused or brought through the hull. | New **D30**: block diagram, fuse table, wire sizes, and the eight penetrations W1–W8. |
| 10 | **Neither ESP32 had a stated 5 V supply.** The limp-home spec lists only a 6 V servo regulator, which is too high for the Feather. | Two Pololu D36V6F5 5 V regulators. |
| 11 | **No way for the companion to power-cycle the Pixhawk,** although the limp-home logic relies on it. | A MOSFET load switch ahead of the PM02 power module. |
| 12 | **The battery box had no lid fastening and no cable exits.** | D32: 8 × M5 into bonded inserts on 4 mm EPDM cord, like the hatch. Two more WetLinks (W7, W8), so 8 in all, not 6. |
| 13 | **No laminate schedule, material quantities or build order.** | New **D31**: laminate table worked out from design.py (about 9.5 m² of 6 oz cloth, about 3.5 L of epoxy), a strongback and frame setup, and a 14-step build sequence. |
| 14 | **No fastener list and no steering-linkage geometry.** The "spring overload link" was named but not drawn. | New **D32**: hardware schedule; linkage plan with a servo-travel table for each pair of holes; a spring-link section with its preload. |
| 15 | **No print settings per part.** | New **D33** and Print_Guide.csv give material, walls, infill, orientation, supports, grams and hours for every file. |
| 16 | **D03 labels overlapped.** | Labels rearranged into rows above the profile. |
| 17 | **README had no E1 section.** | Sections for E1 and E2 added. |

Mesh check after the fixes: all 34 STLs are watertight. P01 is left with one 32 mm circular bridge, the roof of the sensor cavity, which nothing bears on. P02B has a 3 mm fin that needs a brim. Every other downward face is a teardrop hole, a chamfer, or a short bridge.

## 3. Bill of materials

**build-files/BOM.csv** (generated by `source/bom.py`) lists 111 lines across 10 sections: electronics, power, actuators, enclosure and cable, tracker and safety, rig and steering, fasteners, composites and consumables, filament, and spares.

- **Links:** 40 lines carry a purchase link that I found by search this week.
- **Prices:** 25 prices were read from the linked page ("web"). The rest are estimates ("est"). Check them before ordering.
- **Total: about $4,870,** including the YB3 (about $600). Budget about $4,400 if the YB3 is already in hand.

| Section | USD |
|---|---|
| Autopilot, comms, sensors | 832 |
| Power (battery, MPPT, solar, regulators, fuses) | 503 |
| Actuators and pump (2 × SER-2000, 3 servos) | 571 |
| Box, cable, penetrations, potting | 456 |
| Backup tracker and radar reflector | 640 |
| Rig, steering, mechanical | 452 |
| Fasteners | 64 |
| Composites, foam, wood, lead, paint, consumables | 1,209 |
| Filament | 105 |
| Spares | 39 |

The Build Plan budget (Rev E, about $2,995 plus about $630 for the YB3) left out most consumables and fasteners. It also put the whole hull at about $350 and had no paint, antifouling, building frames or spares. This BOM is the full shopping list. Its composites line alone is about $1,200.

Two prices changed when checked:

- **RockBLOCK Plus:** $419 with a 3 m cable (budgeted at about $450).
- **YB3:** £449 plus tax.

## 4. Open items for Randolph

**Update 23 Nov (Rev E3): items 1 and 2 are settled.** Randolph chose the stock options after run 027 (section 6):
- **Item 1, solar:** two stock PV Logic STPVF010 10 W ETFE panels, 380 × 250 × 4 mm, one centred in each bay: 20 W in all. I'd first suggested 30 W of stock panels, but no stock 15 W panel I could find fits a 280 mm bay (they're 300–350 mm wide), so the stock answer is 2 × 10 W. Run 027's 20 W case gives the same success as 40 W, with about 1 voyage in 20 dipping to SAFE once. Custom-size 17–20 W panels stay an optional upgrade.
- **Item 2, spar:** a 30 × 26 stock tube with a 26 × 22 R&G tube bonded full length inside, which gives the same section as 30 × 22. A one-piece special-order 30 × 22 is also fine. Don't use the plain 30 × 26: run 027 puts it at about 2 points lower, with 4× the wing breakages.

Items 3–6 below are still open.

These need a decision. I did not change the design for them.

1. **Solar panels do not fit as specified.** The deck bays are 420 × 280 and 400 × 280 mm. Every stock 20 W semi-flexible ETFE panel I found is about 450 × 350, and 450 × 350 × 4 is common. That is too wide by 70 mm. The options:
   - Order panels to size. Several makers build ETFE panels to custom dimensions.
   - Fit smaller stock panels, with less power, and re-run the power budget.
   - Rework the deck bays.

   The BOM carries a placeholder at $45 each.
2. **The spar, 30 × 22 carbon (4 mm wall), is not a stock size.** Stock 30 mm tubes are 30 × 26, 30 × 27 and 30 × 28. The options:
   - Order it specially. Roll-wrapped tube makers will do it.
   - Bond a 26 × 22 inner tube inside a 30 × 26. R&G sells 26/22. The inner tube may need sanding to slide in. A full-length bond gives about the same section.

   30 × 26 on its own is the Rev C spar, with about 1/1.6 of the bending strength the structural review called for.
3. **Metric stock in the US.** The counterweight arm (12 mm fibreglass rod) and the rudder stocks (12 mm 316 bar) are metric. US 1/2 in (12.7 mm) will not go into the 12.2 sockets or the 12 mm igus bushings. Buy metric, or change `CWARM` and the socket sizes in design.py and parts.py and rebuild P08 and P18. The bushings would also change.
4. **The SER-2000 size is still an estimate.** This was already open, and it now matters twice:
   - P12 has to be rebuilt to the real enclosure.
   - The output-shaft position sets the linkage on D32. With tiller hole 45 and arm hole 30, the output sits 15 mm off the stock line and about 70 mm forward of it.
5. **Genasun GV-5.** The data sheet gives IP40, so it is not potted. Potting_Spec asked for a factory-potted unit. It lives in the sealed box, so conformal-coating it is probably enough, but this is your call.
6. **The spring overload link on D32 is a suggested detail.** The design is two 316 springs preloaded to about 55 N in a brass tube. Prove it in Test I before trusting it.
7. **The battery-box lid on D32 is a proposal.** It copies the hatch. Confirm it.

## 6. Simulated effect of open items 1 and 2 (21 Nov 2026, run 027)

Rev E1 on run 025's set-up (45 km off Hatteras to the Lizard offing, 500 voyages, 1 May–15 June 2023+2024), with the same launches and seeds, so the differences are paired. Run 025 itself: 83.0% success, 76.4% reach the hold.

| Change | Success | Paired change (95% range) | Reached the hold | Boats whose battery reached SAFE (25%) | Voyages with the wing broken in a knockdown |
|---|---|---|---|---|---|
| Run 025 (40 W solar, 30 × 22 spar) | 83.0% | — | 76.4% | 0 | 10 |
| **30 W solar** | 83.0% | +0.0 (-0.6 to +0.6) | 76.2% | 9 | 10 |
| **20 W solar** | 83.0% | +0.0 (-0.8 to +0.8) | 75.8% | 26 | 9 |
| **Stock 30 × 26 spar** | 80.8% | **-2.2** (-3.6 to -1.0) | 72.0% (-4.4) | 0 | **40** |

**What it shows:**
- **Solar (item 1): smaller stock panels are acceptable.** 30 W or even 20 W in total changes nothing measurable in success. The battery margin does shrink: the lowest charge on a typical voyage falls from 88% (40 W) to 87% (30 W) and 85% (20 W). More to the point, with 20 W about 1 boat in 20 (26 of 500) runs the battery down to the 25% SAFE threshold at some point and waits there until the sun brings it back, against none with 40 W. With 30 W it's 9 of 500. **30 W of smaller stock panels is a reasonable choice; 20 W works but leaves little margin** for a cloudy spell, a dirty panel or a weaker battery.
- **Spar (item 2): the stock 30 × 26 tube costs about 2 points.** Wing breakages in knockdowns go from 10 to 40 voyages in 500, which takes success down 2.2 points and reaching the hold down 4.4. So the 30 × 22 spec, or the bonded 26 × 22 sleeve inside a 30 × 26 (option 2 in item 2), is worth having. This uses the strike model's table for the 30 × 26 tube (the Rev C spar), which depends only on the tube and the wing height; it's the same grade as the rest of the structural model.
- No decision is changed here; both items stay open for Randolph.

## 5. What a builder needs

**Printing:**
- **Printer:** a 220 × 220 bed or larger.
- **Filament:** about 2.5 kg in all: 1.3 kg PETG, 0.7 kg ASA and 0.6 kg PLA (the PLA is for the bulb pattern only).
- **Time:** about 220 hours at 12 g/h. A fast CoreXY printer takes about half that.

**Tools that are probably not in a hobby shop already:**
- a hot-wire foam cutter;
- a long fairing board;
- a 0.1 g scale for epoxy;
- a respirator rated for organic vapour and P100;
- a crimp tool;
- an outdoor setup for casting lead.

**The full file set is in build-files/:**
- Drawings.pdf, 28 sheets;
- Templates_1to1_Letter.pdf and the DXF files;
- 34 STLs;
- BOM.csv and Print_Guide.csv;
- the Python source that regenerates all of them.
