SOLAR-SAIL OCEAN DRONE 1.5 m  -  BUILD FILES (Rev C, 2026-11-10)

Drawings.pdf                 20 tabloid sheets (11 x 17 in): general arrangement, hull lines + offsets,
                             interior, keel + bulb, twin rudders, wing + tail, mast/stub, hatch,
                             subdivision + foam fill + labels (D09), and one sheet per pair of printed parts.
Templates_1to1_Letter.pdf    Full-size cutting templates tiled on US Letter. Print at 100% / Actual size
                             and check the 100 mm bar on each page. Overlap 12 mm; align red dashed lines.
                             T01-T09 hull frames, T10 transom, T11 stem, T12/T13 fin root/tip,
                             T14 rudder (make 2), T15 wing rib/hot-wire template, T16 hatch,
                             T17 bulkhead x 300, T18 bulkhead x 1260.
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
