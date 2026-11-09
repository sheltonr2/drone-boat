# Storm loads on the wing spar (hand calculation)

*9 November 2026. Purpose: put numbers behind the storm-damage assumptions in [Hurricane_Risk.md](Hurricane_Risk.md) (30% loss for a tropical storm within 100 km, 70% for a hurricane) and check whether the 25 mm carbon spar is strong enough. Grade D: textbook coefficients, no test data yet.*

## Spar strength

| Spar | Section modulus | Bending moment at failure (UD carbon ~600 MPa) | Mass per metre |
|---|---|---|---|
| **25 × 22 mm tube (current plan; wall assumed)** | 614 mm³ | **~370 N·m** | ~0.17 kg |
| 30 × 26 mm | 1,155 mm³ | ~690 N·m | ~0.27 kg |
| 32 × 28 mm | 1,330 mm³ | ~800 N·m | ~0.29 kg |

*Section modulus Z = π(D⁴ − d⁴)/(32D). Roll-wrapped carbon tube bending strength varies widely between suppliers, so get the real figure from the supplier, or from the proof test below.*

## Load cases (bending moment at the lower bearing)

The wing's area centre sits about 0.8 m above the lower bearing (wing root 0.30 m, span 1.0 m, chord 0.30 m, thickness 0.15 m).

| Case | Speed | Wing orientation | Force | Moment | vs 25 mm spar |
|---|---|---|---|---|---|
| 25 m/s gale, wing stalled by a jammed tail (Cl 1.3) | 25 m/s air | broadside to the flow | 150 N | 120 N·m | OK (3×) |
| Knockdown: wing slapped into the water by the roll (~1.6 rad/s) | 1.3 m/s water | broadside | 310 N | 250 N·m | **marginal (1.5×)** |
| Same | 1.3 m/s water | edge-on (weathervaned) | ~13 N | ~10 N·m | OK |
| Breaking crest sweeps over the boat with the wing up | 6 m/s water | edge-on (free to weathervane) | ~280 N | ~220 N·m | marginal |
| Same | 8 m/s water | edge-on | ~490 N | ~390 N·m | **fails** |
| Same | 6 m/s water | broadside (wing jammed) | ~6.6 kN | ~5 kN·m | fails |

*Water drag F = ½ρv²·Cd·A, with ρ = 1,025 kg/m³. Broadside: Cd 1.2, A = 0.30 m². Edge-on: Cd·A ≈ 0.015 m². Water speeds in a breaking crest are a fraction of the wave's phase speed (~12–15 m/s for 8–10 s storm waves).*

## What this means

1. **Gales on their own aren't the danger. Breaking waves are.** The 25 mm spar survives any wind load while the wing can weathervane. It's marginal in a knockdown, and it fails if a fast breaking crest catches it. Hurricane seas make such crests likely, and tropical-storm seas make them possible. That matches the 30%/70% loss assumptions in order of magnitude. It also matches the record: Saildrone's wing broke when the vessel was rolled in a Gulf Stream storm.
2. **A free-weathervaning wing is the main defence.** Loads drop roughly 20-fold when the wing aligns with the flow. Keep the bearing friction low (`bearing_friction_nm` 0.02) and make sure the tail can't jam the wing broadside. If the tail servo fails, it should leave the tail free to swing.
3. **Upgrade the spar to 30–32 mm.** That doubles the strength for about 100 g, and with the counterweight it barely shifts the rig's centre of gravity. Re-check the wing balance (Field Test D) after the change.
4. **Proof test (add to Field Test C):** clamp the hull, hang 32 kg from the spar 0.8 m above the lower bearing (≈250 N·m, the knockdown case) for one minute, then check for cracks and permanent set. It must also pass at 1.2× that load (38 kg) with a 30–32 mm spar.
