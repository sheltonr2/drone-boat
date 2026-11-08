SOLAR-SAIL OCEAN DRONE 1.5 m  -  BUILD FILES (Rev B, 2026-11-08)

Drawings.pdf                 18 tabloid sheets (11 x 17 in): general arrangement, hull lines + offsets,
                             interior, keel + bulb, rudder, wing + tail, mast/stub, hatch, and one
                             sheet per pair of 3D-printed parts.
Templates_1to1_Letter.pdf    Full-size cutting templates tiled on US Letter. Print at 100% / Actual size
                             and check the 100 mm bar on each page. Overlap 12 mm; align red dashed lines.
                             T01-T09 hull frames, T10 transom, T11 stem, T12/T13 fin root/tip,
                             T14 rudder, T15 wing rib/hot-wire template, T16 hatch.
dxf/                         The same templates as DXF (R12, millimetres) for CNC, laser or a vinyl cutter,
                             plus body_plan_all_stations.dxf.
stl/                         21 STL files for the 18 printed parts (P01-P18), already in print orientation.
                             Files ending _x4 are needed four times.
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
