# Design files for simulators

| File | For | What it is |
|---|---|---|
| `revC_design.json` | Our simulator (`simulator/drone_sim`) | Rev C, the current design (10 Nov 2026). Also what `default_design()` returns. Load with `--design ..\designs\revC_design.json`. |
| `revC1_design.json` | Our simulator | The same as `revC_design.json` today (Rev C1, 11 Nov 2026), under a fixed name for comparison runs. `revC0_design.json` is Rev C as first drawn (box low, wet-electronics factor 6). |
| `revB_design.json` | Our simulator | Rev B (8 Nov 2026), for comparisons. Files without a `"revision"` key load as Rev B. |
| `boat-sim/randolph_rev_c.yaml` | John's [boat-sim](https://github.com/jcolter11374/boat-sim) | Rev C in boat-sim's config schema (same keys as its own `configs/randolph_rev_b.yaml`, plus `hazards.leak_per_day`). Drop it into `configs/`. |
| `revC_boat_wing_feathered.stl` | Any tool | Whole boat (hull, fin, bulb, both rudders, wing feathered fore and aft), binary STL in **metres**. x aft from the bow, y to port, z up from the hull bottom at midships. |
| `revC_geometry.json` | Any tool | Mass items, CG, inertia, waterline, stability (GM, GZ max, AVS), reference areas, rudder and spar data. |

The master dimensions in millimetres are in `build-files/source/design.py`; the drawings are generated from it. The stability curve is in `docs/data/revC_gz_curve.csv`. The reasons for each Rev C change are in `docs/Design_RevC.md`.
