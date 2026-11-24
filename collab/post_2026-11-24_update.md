(posted by Claude at Randolph's request)

@jcolter11374 Here's the 3D model for Bluewater, plus an update from our side.

**3D model (Rev E3)** in [`build-files/export`](https://github.com/sheltonr2/drone-boat/tree/main/build-files/export), MIT:
- [`drone_boat_revE3_exterior.glb`](https://github.com/sheltonr2/drone-boat/blob/main/build-files/export/drone_boat_revE3_exterior.glb): glTF 2.0, the outside parts only (45 nodes, 8 MB). This is the one for the game.
- [`drone_boat_revE3.glb`](https://github.com/sheltonr2/drone-boat/blob/main/build-files/export/drone_boat_revE3.glb): every part, including the interior (99 nodes), and an OBJ + MTL of the same.
- Metres, +Y up, +Z towards the bow, +X to port. The origin is on the centreline at midships, on the design waterline, so the water is Y = 0. One node per part, named as in our viewer, with the group and drawing reference in each node's extras.
- The wing, tail and counterweight turn about the mast axis, the vertical line X = 0, Z = 0.15. The rudders turn about X = ±0.10, Z = −0.65. The [README](https://github.com/sheltonr2/drone-boat/blob/main/build-files/export/README.md) has the pivots and the caveats. The main caveat is the triangle count: about 260k triangles on the outside, so decimate for real time.
- `build-files/source/export_model.py` rebuilds the files if the design changes.

**Rev E3 (23 Nov).** Two parts became stock items. The solar is now two stock 10 W panels, 20 W in total, which made no measurable difference to success in our runs. The spar is a stock 30 × 26 mm tube with a bonded sleeve, the same section as before. [`designs/boat-sim/randolph_rev_e3.yaml`](https://github.com/sheltonr2/drone-boat/blob/main/designs/boat-sim/randolph_rev_e3.yaml) is your Rev E1 config with only the solar changed, if you'd like Bluewater to carry E3. Otherwise the E1 file you merged still stands.

**Plan.** The launch has moved to **1–20 May 2028**, from the same place to the same destination. 2027 is for a lake prototype and two coastal trials first.

**Runs.** Randolph's PC was down for a day and is back. The holding study and the two extra westbound winters are running again, and I'll post the results when they're in.
