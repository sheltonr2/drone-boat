(posted by Claude at Randolph's request)

@jcolter11374 Sorry, our first post today crossed with your two comments. Thank you for putting Rev E1 into Bluewater. The glTF answers your 23 Nov request: it's a single `.glb` with every part named separately, and the bow is at +Z (noted in the file's README and in its root node).

Here is the **Rev E1 righting-arm curve and inertia** you asked for, from our simulator and in the same format as the Rev C files:
- [`docs/data/revE1_gz_curve.csv`](https://github.com/sheltonr2/drone-boat/blob/main/docs/data/revE1_gz_curve.csv): heel 0–180° in 5° steps, with GZ, trim and sink. GM is 0.180 m, the largest GZ is 0.354 m at 105°, and it's positive all the way to 180°.
- [`designs/revE1_geometry.json`](https://github.com/sheltonr2/drone-boat/blob/main/designs/revE1_geometry.json): 28.52 kg, the CG, the waterline at 106 mm and the inertia tensor about the CG: Ixx 2.93, Iyy 5.35, Izz 2.47 kg·m², with Ixz −0.43. The frame is our design frame: x aft from the bow, y to port, z up from the hull bottom.
- The Rev E3 files are the same to the figures given, because the lighter panels change the mass by grams. `docs/data/stability_export.py` makes both.

The other points in your note look right to us. One small thing: the Boatyard's test sails Rev E1 to Portugal. Our runs put Hatteras to Cornwall at about 87% for this boat, so a Portugal score won't compare one-for-one with ours. That's fine as long as the label says where it's going, which yours does.
