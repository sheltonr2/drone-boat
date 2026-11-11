SOLAR-SAIL OCEAN DRONE 1.5 m  -  BUILD FILES (Rev C4, 2026-11-11)

Drawings.pdf                 20 tabloid sheets (11 x 17 in): general arrangement, hull lines + offsets,
                             interior, keel + bulb, twin rudders, wing + tail, mast/stub, hatch,
                             subdivision + foam fill + labels (D09), and one sheet per pair of printed parts.
Templates_1to1_Letter.pdf    Full-size cutting templates tiled on US Letter. Print at 100% / Actual size
                             and check the 100 mm bar on each page. Overlap 12 mm; align red dashed lines.
                             T01-T09 hull frames, T10 transom, T11 stem, T12/T13 fin root/tip,
                             T14 rudder (make 2), T15 wing rib/hot-wire template, T16 hatch,
                             T17 bulkhead x 300, T18 bulkhead x 1260, T19/T20 keel-box floors.
dxf/                         The same templates as DXF (R12, millimetres) for CNC, laser or a vinyl cutter,
                             plus body_plan_all_stations.dxf.
stl/                         23 STL files for the 20 printed parts (P01-P20), already in print orientation.
                             Files ending _x4 are needed four times; print P11, P12 and P13a/b twice (two rudders).
source/                      Python that generates everything (design.py holds every master dimension).
                             Change a number there and rerun build_stl.py, drawings.py, templates.py.

Print settings: 0.4 mm nozzle, 0.2 mm layers, 4+ walls. ASA for parts outside in the sun, PETG below deck.
Bulb pattern P14 is a pattern for a plaster/sand mould: never pour lead into a print.

Check before printing: servo tab spacing (slots cover 47.5-51.5 mm), AS5600 board size (26 mm recess),
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
