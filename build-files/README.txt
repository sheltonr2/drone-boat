SOLAR-SAIL OCEAN DRONE 1.5 m  -  BUILD FILES (Rev F, 2026-11-27)

Drawings.pdf                 29 tabloid sheets (11 x 17 in): general arrangement, hull lines + offsets,
                             interior, keel + bulb, twin rudders, wing + tail, mast/stub, hatch,
                             subdivision + foam fill + labels (D09), one sheet per pair of printed parts (D10-D24),
                             wiring (D30), laminates + build sequence (D31), hardware + linkage (D32), print guide (D33).
BOM.csv                      Full bill of materials: every part, material, fastener and consumable, with quantities,
                             prices (web = seen on the linked page in Nov 2026, est = estimate) and purchase links.
Print_Guide.csv              Every STL: quantity, material, walls/infill, orientation, supports, grams, hours.
Templates_1to1_Letter.pdf    Full-size cutting templates tiled on US Letter. Print at 100% / Actual size
                             and check the 100 mm bar on each page. Overlap 12 mm; align red dashed lines.
                             T01-T09 hull frames, T10 transom, T11 stem, T12/T13 fin root/tip,
                             T14 rudder (make 2), T15 wing rib/hot-wire template, T16 hatch,
                             T17 bulkhead x 300, T18 bulkhead x 1260, T19/T20 keel-box floors,
                             T21 weed fairing (Rev E).
dxf/                         The same templates as DXF (R12, millimetres) for CNC, laser or a vinyl cutter,
                             plus body_plan_all_stations.dxf.
stl/                         36 STL files: parts P01-P29, the P02A/B split option and fit coupons P00a/b,
                             already in print orientation.
                             Files ending _x4 are needed four times; print P11, P12, P13a/b and P26 twice (two rudders).
viewer/                      Interactive 3D model for a web browser (three.js): the whole boat with sea, cut-away,
                             X-ray, explode and moving wing/tail/rudders/vane, plus every STL on a print bed with
                             its print settings. index.html + model.json (built by source/viewer3d.py). Serve the
                             folder (e.g. python -m http.server) and open it; opening the file directly will not load.
source/                      Python that generates everything (design.py holds every master dimension).
                             Change a number there and rerun build_stl.py, drawings.py, templates.py.

Print settings: 0.4 mm nozzle, 0.2 mm layers, 4+ walls. ASA for parts outside in the sun, PETG below deck.
Print the fit coupons P00a and P00b FIRST and try the real tubes, rods, bearings and bolts in them (D33).
Bulb pattern P14 is a pattern for a plaster/sand mould: never pour lead into a print.

Check before printing: the SER-2000 enclosure size for cradle P12 (66 x 34 x 72 is an ESTIMATE: measure,
set SER in source/design.py, rebuild P12), the tail servo's tab spacing (slots cover 47.5-51.5 mm), AS5600 board size (26 mm recess),
patch antenna footprint, and enclosure inside size for the tray P15.

Rev B (2026-11-08)
  The wing counterweight moved from the wing's nose pocket to a printed pod (P18) on a 12 mm carbon arm
  reaching 300 mm forward of the spar axis. P08 (spar clamp) gained a forward socket for the arm and was
  renamed P08_spar_clamp_two_sockets.stl. Fill P18 with about 0.8 kg of lead shot + epoxy until the rig
  balances. The nose pocket alone would have needed about 7.6 kg. Sheets changed: D00, D01, D06, D12, D17.
  Extra supplies: 12 mm carbon tube (246 mm more), about 1 kg lead shot, 1 more M4 bolt.

Rev C (2026-11-10)  -  reasons and numbers: docs/Design_RevC.md
  1. Hull foam-filled behind two glassed-in bulkheads (x 300, x 1260; templates T17, T18). Bow and stern solid;
     removable XPS blocks fill the dry bay to leave 3 L or less of open space. Battery in its own sealed box.
  2. Twin rudders 100 mm either side of the centreline, each with its own trunk, servo (P12), tiller (P11) and blade
     (P13). Trunk tops get a lip seal and boot. Servo cables pass the aft bulkhead in two WetLinks.
  3. Wing spar 30 x 26 carbon on 6806-2RS bearings: P07 (bearing seats D42.05) and P08 (bore D30.2) changed;
     T15 spar bore now D30.4 (and the old nose-weight pocket is gone from T15).
  4. Bulb D72 (was D68), about 9.2 kg: P14a/b changed.
  5. New P19 (YB3 platform, z 480 on the stub) and P20 (all-round light clamp, z 600). Label areas on D09.
  Removed: thruster provision, backup D-cell. Mass about 25 kg, DWL z 98.
  Sheets changed: all (title blocks), with real changes on D00, D01, D02 (DWL), D03, D04, D05, D06, D07, D09 (new),
  and the parts sheets for P07, P08, P11-P14, P19, P20. Printed-part sheets are now D10-D19.

Rev C2 (2026-11-11)
  Keel fin rebuilt after a strength check (docs/Keel_Structure_Loads.md). Outside shape unchanged.
  Core: two hardwood planks glued round the 2 x M10 rods (was foam). Skin: 6 x 6 oz each side (was 3) over a
  60 x 1.5 mm unidirectional carbon strip let into each face. The top 60 mm of the core is a tenon standing in a
  keel-box socket cast round it; G10 plate 122 x 60 x 10 on top (was 190 x 60). Two 9 mm marine-ply floors at
  x 650 and x 800 (new templates T19, T20) and 3 extra plies inside the hull bottom between them.
  T12 and T13 are now planing gauges for the wood core. Rods are about 580 long. No printed part changed.
  Mass about 26.4 kg, DWL z 101. Proof-load the keel before paint: Field Test K (60 kg hung from the bulb).
  Sheets changed: all (title blocks), with real changes on D00, D03, D04.

Rev C3 (2026-11-11)
  Changes from the whole-boat structural review (docs/Structural_Review.md):
  1. YB3 backup tracker moved from the stern post to a glassed well in the foredeck (176 x 106 x 38 deep, centred
     x 180, scupper slots to the deck edges). P19 is now a flat deck cradle: reprint it.
  2. Stern post: 20 x 2 mm pultruded fibreglass tube (was aluminium). Clamps P05, P06, P20 unchanged.
  3. Counterweight arm: 12 mm solid pultruded fibreglass rod (was carbon tube). P08 and P18 unchanged.
  4. Rudders: a spring servo-saver on each servo and two G10 stop blocks per tiller (+/-40 deg).
  5. Spar 30 x 22 carbon, 1195 long, bottom at z 105. Bearings 130 apart: P07 is now 137 long: reprint it.
     Slip ring moves down with the spar end.
  6. Second inner ply of 6 oz over the sump (hull bottom, x 560-770).
  Mass about 26.9 kg, DWL z 102. Sheets with real changes: D00, D01, D03, D05, D06, D07, and the P07 and P19 sheets.

Rev C4 (2026-11-11)
  From the research review (docs/Research_Review.md):
  1. Mast bearings: two 6806 acetal (Delrin-type) ball bearings with glass balls, each floating 0.3 mm on a
     42 x 1.5 O-ring, with plain catcher lands (D30.6 x 20) in P07 that take wave loads. V-ring VA-30 on the spar
     above the housing; a Delrin thrust collar on the spar. REPRINT P07 (same outside size, new inside).
  2. Notes: fin glue-up and rod bedding (D04); grease the rudder trunks and inspect the stocks (D05);
     epoxy and paint every exposed printed part; three coats of ablative copper antifouling (D00).
  3. docs/Rudder_Health_Spec.md: autopilot detection of a sticking rudder; needs a current sensor per rudder servo.
  Sheets with real changes: D00, D04, D05, D07 and the P07 sheet. No change to mass or templates.

Rev C5 (2026-11-11)
  Wing 800 x 375 (was 1000 x 300), same 0.30 m2, after docs/Wing_Shape_Study.md: about half the load when a knockdown
  slaps the wing on the water, about 4% slower. Spar 82 from the leading edge; spar tube 995 long (was 1195).
  New template T15 (print it again). Wing core: two 400 mm blocks. Counterweight about 0.85 kg.
  Sheets with real changes: D00, D01, D06. No printed part changed.

Rev D (2026-11-12)   [drafted as C6; a new letter because it adds a system: see docs/Revisions.md]
  After docs/Electronics_Review.md: a limp-home controller, coating and potting, and the encapsulated modem.
  1. Limp-home controller in potted case P21 on the aft face of bulkhead x 300 (own ESP32, GPS, BNO085 heading,
     fused 12 V feed). Takes the starboard rudder and the tail through switchover pod P22 (bulkhead x 1260) if the
     main box's heartbeat stops. docs/Limp_Home_Spec.md. Bench Test N before and after potting.
  2. RockBLOCK Plus in bowl P23 bonded into a D146 hole in the hatch lid (template T16 shows the cut).
     The Iridium patch on the stern post and its cable are deleted.
  3. Main GPS + compass moves to P05 on the stern post (it was in the box, under the aft solar panel).
  4. Every board coated; sensors, power boards and joints potted after the shakedown. docs/Potting_Spec.md.
  About 27.8 kg, DWL z 104. Sheets with real changes: D00, D01, D03, D07, D08, and new parts sheets D20, D21.
  New STL: P21_limp_home_case, P22_switchover_pod, P23_rockblock_plus_bowl. P05 notes changed (same part).

Revision convention (docs/Revisions.md): a new letter when a system is added or removed, the way parts connect
changes, or a set is frozen for building; numbered sub-revisions (D1, D2...) for part fixes within a letter.

Rev E (2026-11-13)  docs/Design_RevE.md
  After the reliability runs (docs/Reliability_Review.md). A new letter: it adds a system (bilge pump) and a sensor.
  Leaks: bilge pump upright on spacer P24 against the mast tube, strainer port of the keel box, outlet loop to a
  check valve and a deck fitting aft of the hatch; the autopilot keeps sailing and pumps. Membrane vents in the hatch
  lid and the electronics-box lid, a capped Schrader valve in the lid for the pressure-decay test, a humidity and
  pressure sensor on bulkhead x 300. Servos: sealed Blue Trail SER-2000 rudder servos in cradles P12 (replaces the
  servo mount) with arms P26 for the 6 mm D-shaft and spring overload links in the pushrods; tail servo is a potted
  magnetic-encoder servo with detent P25 so it fails at +/-8 deg, not free. Weed: fairing fin-to-bulb (T21).
  Not adopted: flush bulb nose (W2) and raked rudders (W3). 28.5 kg, DWL z 106.
  Sheets changed: D00, D03, D04, D05, D06, D08, parts sheets. New: P24, P25, P26, T21. Changed: P09 (notes), P12.

Rev E1 (2026-11-14)  docs/Design_RevE.md, docs/Fatigue_Review.md
  Tail boom 16 x 14 carbon, 600 long (was 12 x 10): in 5 m beam seas the old tube saw stress cycles near its strength.
  P08 aft socket D16.2 x 37 (wider, taller boss) and P09 socket D16.2: REPRINT both. About 25 g more lead in P18
  (about 0.91 kg). Steering wave filter; leak SAFE limit 1.0 kg. Sheets: D00, D06, P08 and P09 sheets.

Rev E2 (2026-11-19)  docs/DFM_Review.md  -  design for manufacture; no change to shape, mass or performance
  Printed parts:
  1. P01: the lower vane bearing seat was closed in, so the bearing could not be fitted. Now one D22.1 bore from
     the top: lower bearing, new spacer P27, upper bearing. REPRINT P01; print P27.
  2. P03: 45 deg chamfer under the flange; P07: shoulder + 45 deg cone above the bottom bearing seat (lower land
     now z 10.5-30.5). Both print without supports. REPRINT if not printed yet.
  3. P10a: D6.2 x 1.2 pocket for the detent's steel disc. P12: base cut to 96 x 52 so it fits the 100 x 56 foam pocket.
  4. P02 is 275 long: print it diagonally on a 230 x 230 bed, or print P02A + P02B and join them.
  5. New fit coupons P00a (vertical bores) and P00b (horizontal teardrop sockets).
  Drawings: new D30-D33; D03 labels rearranged; all title blocks E2.
  Gaps filled: 5 V logic supplies for both ESP32s, a Pixhawk power switch, battery-box lid closure and its two
  cable exits (W7, W8: 8 WetLinks, not 6), wire gauges and fuse ratings, linkage geometry, laminate quantities.
  Open items for the builder (DFM_Review section 4): solar panels to fit the deck bays, the 30 x 22 spar, metric
  12 mm rod and bar in the US, the SER-2000 size, the GV-5 sealing.

Rev E3 (2026-11-23)  docs/DFM_Review.md sections 4 and 6  -  DFM open items 1 and 2 settled
  1. Solar: 2 x stock PV Logic / Solar Technology STPVF010 10 W ETFE flexi panels, 380 x 250 x 4, one centred in each
     deck bay (20 W in all, was about 40 W of custom-size panels). Run 027: no measurable change in success; about
     1 voyage in 20 dips to SAFE (25%) once and recovers. Custom-size 17-20 W panels stay an optional upgrade.
  2. Wing spar: 30 x 26 stock carbon tube with an R&G 26 x 22 tube bonded full length inside (sand to a sliding fit,
     thickened epoxy, cure vertical): the same section as the 30 x 22 spec. A one-piece special-order 30 x 22 is also
     fine. Run 027: the plain 30 x 26 tube alone would cost about 2 points (4x the wing breakages), so don't skip the sleeve.
  Sheets: D00 (revision history), D01 (plan, key data), D06 and D07 (spar notes), D30 (solar block); title blocks E3.
  BOM: solar and spar lines replaced (two spar lines now). Simulator design: designs/revE3_design.json (20 W).
  Still open (DFM_Review section 4): metric 12 mm rod and bar in the US, the SER-2000 size, the GV-5 sealing.


Rev F (2026-11-27)  docs/Design_RevF.md  -  daily photo by satellite
  The RockBLOCK Plus (Iridium SBD, 340-byte messages) becomes a RockBLOCK Plus 9704 (Iridium IMT, messages up to 100 KB) in the
  same bowl P23: the same 137 x 40 puck; check its bolt pattern against P23's slots. A camera pod goes on the stern post at z 472-522:
  clamp P28 and housing P29 (new STLs), a 40 x 3 mm glass window, a XIAO ESP32S3 Sense camera (OV3660, microSD) on a 10 deg wedge.
  The nav-light cable W3 becomes a 6-core carrying the light and the camera; the camera gets its own 5 V load switch.
  Sheets changed: D00, D01, D07, D30; new parts sheet D24 (P29; P28 shares D23 with P27). BOM about +$127. Mass about +0.18 kg.
  Hull, rig, foils and templates unchanged (the template PDF still carries the Rev E3 title block).
