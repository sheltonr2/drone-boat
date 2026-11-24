# 3D model export, Rev E3

The same model as the 3D viewer (build-files/viewer), exported for game engines and CAD/3D tools. Made for Bluewater in [jcolter11374/boat-sim](https://github.com/jcolter11374/boat-sim) (issue #50). MIT licence, like the rest of this repo.

| File | What it is | Size |
|---|---|---|
| `drone_boat_revE3_exterior.glb` | glTF 2.0 binary, only the parts visible from outside: 45 nodes, 18 materials. **Start here for a game.** | 8 MB |
| `drone_boat_revE3.glb` | glTF 2.0 binary, every part including the interior structure and electronics: 99 nodes, 33 materials | 13 MB |
| `drone_boat_revE3.obj` + `.mtl` | Wavefront OBJ of all 99 parts, one `o` per part, with normals and colour-only materials | 35 MB |
| `parts.csv` | Each node's id, name, group, whether it is interior, materials, triangle count and drawing reference | |

## Frame and units

- Metres. Right-handed, glTF convention: **+Y up, +Z forward (towards the bow), +X to port**.
- Origin: on the centreline, at midships (750 mm aft of the bow) and at the design waterline (106 mm above the hull bottom). So the water surface is the plane Y = 0 at the design trim, the bow is at Z = +0.75 and the transom at Z = −0.75.
- Bounds: X ±0.20, Y −0.58 (bottom of the bulb) to +1.00 (top of the wing), Z −0.98 (tail-boom tip) to +0.75.
- Each part is its own node, with its placement baked into the vertices, so every node sits at the identity. To make a part move, set its pivot first:
  - **Wing, tail and counterweight** turn together about the mast axis, the vertical line X = 0, Z = 0.15 (600 mm aft of the bow). That is every node in the "Wing-sail rig" group of `parts.csv` except `P07`, the mast bearing housing, which is fixed to the deck.
  - **Rudders** turn about vertical axes at Z = −0.65 (1400 mm aft of the bow), X = ±0.10. The nodes are the "Steering" group, ending `_port` or `_stbd`.

## What is approximate

- Colours are flat PBR base colours. The viewer's shader paints the hull's antifouling, white boot stripe and hi-vis topsides by height; here the hull triangles are split into three materials at 14 mm and 27 mm above the waterline instead, and the dark sheer stripe is left out.
- The hull is an open shell (its materials are double-sided so cut-aways look right). The solar panels are plain dark blue, without cells.
- The triangle count is high (390k all parts, about 260k exterior) because the hull and the printed parts come from the build geometry. Decimate for real-time use; the hull keeps its shape well at a tenth of the triangles.
- This is Rev E3. It differs from the Rev E1 config in boat-sim only by the solar panels (two stock 10 W panels, 380 × 250 mm) and the spar's make-up, which looks the same.

## Rebuilding

`python build-files/source/export_model.py` regenerates every file here from `build-files/viewer/model.json`, which `build-files/source/viewer3d.py` makes from the design.
