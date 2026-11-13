# Simulator speed-up (13 Nov 2026)

Randolph asked whether his GPU could speed up the runs. It can't usefully: a voyage is about 300,000 small sequential steps, and the time goes on Python overhead in a few lookups, not on arithmetic a GPU could parallelise. So instead, two hot spots were rewritten to do **exactly the same arithmetic with less overhead**. The rule: the faster code must give results identical to the old code, bit for bit, or it is not used.

## Where the time went (one 40-day voyage, profiled)

| | Share of run time |
|---|---|
| Polar lookup (boat speed for the current wind) | 33% |
| Land test (point in coastline polygons) | 25% |
| Small array shuffles inside those two | 16% |
| Weather lookup | 12% |
| Everything else | 14% |

## What changed

- **Polar lookup** (`vpp.Polar.__call__`): the same 16-corner interpolation, the same weights in the same order, the same zero-weight skip, on plain Python floats taken from the same float64 tables. The corner weights are now computed once per call instead of once per output.
- **Land test** (`env.LandMask.is_land`, and the Europe test): the same ray-casting test, but only over polygons whose bounding box covers the point (a 1° grid of boxes) and only over the coastline edges that can cross the point's latitude (edges binned into 0.25° bands). Every edge the old test counted is still counted, with the same arithmetic.
- **Not changed:** the weather lookup. It interpolates with a matrix routine whose rounding could change in the last digit, so it was left alone.
- The old code is still there: `DRONE_SIM_REFERENCE=1` runs it.

## Proof that nothing changed

| Test | Result |
|---|---|
| Polar lookup, 100,000 random inputs (including exact grid points), all 11 outputs | 0 mismatches |
| Land test, Natural Earth 50 m coastline (1,421 polygons): 49,081 points (random, near coasts, on vertices, on cell corners) | 0 mismatches; 13× faster |
| Europe test, same points | 0 mismatches; 10× faster |
| 36 full voyages (Rev D, the reliability package and C5; six launch points), synthetic weather, real coastline | identical in every field apart from run time; about 6× faster |
| 48 voyages with heavy failures so boats drift ashore (4 grounded) | identical apart from run time |
| **On Randolph's PC (13 Nov):** 80 voyages, real 2023 weather, Canaveral (land-heavy) and Ocean City → Cornwall, old code vs new | **PASS**: identical in every field apart from run time. 40 voyages: Canaveral 10 min 31 s → 2 min 25 s (4.3×), Ocean City → Cornwall 11 min 48 s → 2 min 39 s (4.4×). New code installed at 1:20 pm (`collab/run_log_speed_check_2026-11-13.txt`) |

On real weather the weather lookup becomes the largest remaining cost, which is why the PC gains 4.4× rather than 6×. A 150-voyage run now takes about 9 minutes instead of 40 (`collab/launch_points/make_batch.py` uses the new figure).

`simulator/tools/compare_results.py` compares two result files field by field, ignoring only run time.
