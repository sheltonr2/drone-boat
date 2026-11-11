# Design files for simulators

| File | For | What it is |
|---|---|---|
| `revC_design.json` | Our simulator (`simulator/drone_sim`) | The current design (Rev C3 since 11 Nov 2026). Also what `default_design()` returns. Load with `--design ..\designs\revC_design.json`. |
| `revC1_design.json` | Our simulator | The same as `revC_design.json` today (Rev C1, 11 Nov 2026), under a fixed name for comparison runs. `revC0_design.json` is Rev C as first drawn (box low, wet-electronics factor 6). |
| `revC3_design.json` | Our simulator | **Rev C3, the current design** (11 Nov 2026): the structural-review changes, 26.9 kg, with the structural-failure model on (`"structure"` key). `revC_design.json` and `default_design()` are the same. |
| `revC2_design.json`, `revC2_structure_design.json` | Our simulator | Rev C2 (hardwood keel fin, 26.4 kg). The first loads with the structural-failure model off, as it was run; the second has it on with the pre-review parts, for comparison with C3. `revC1_design.json` keeps the C1 masses (25.3 kg). |
| `revB_design.json` | Our simulator | Rev B (8 Nov 2026), for comparisons. Files without a `"revision"` key load as Rev B. |
| `boat-sim/randolph_rev_c.yaml` | John's [boat-sim](https://github.com/jcolter11374/boat-sim) | Rev C in boat-sim's config schema (same keys as its own `configs/randolph_rev_b.yaml`, plus `hazards.leak_per_day`). Drop it into `configs/`. |
| `revC_boat_wing_feathered.stl` | Any tool | Whole boat (hull, fin, bulb, both rudders, wing feathered fore and aft), binary STL in **metres**. x aft from the bow, y to port, z up from the hull bottom at midships. |
| `revC_geometry.json` | Any tool | Mass items, CG, inertia, waterline, stability (GM, GZ max, AVS), reference areas, rudder and spar data. |

The master dimensions in millimetres are in `build-files/source/design.py`; the drawings are generated from it. The stability curve is in `docs/data/revC_gz_curve.csv`. The reasons for each Rev C change are in `docs/Design_RevC.md`.
