# Flooded stability (Rev E)

13 November 2026. Item 5 of [Naval_Review.md](Naval_Review.md). Grade D: computed from the hull geometry and mass model, not measured. Script: `docs/data/flooded_stability.py` (results in `flooded_stability.json`). Water levels: the same script's geometry, worked through for the table below.

## Question

Rev E keeps sailing with water aboard, pumping it out, and goes to SAFE only above 1.5 kg ([Design_RevE.md](Design_RevE.md)). The simulator lets up to 3 kg in, the 3 L of open space the dry bay was meant to leave. Does free water slopping about in the boat spoil its stability or its self-righting?

## How

The righting arm (GZ) curve from 0° to 180° is computed with the boat's trim found at every angle, as for the intact curves. Water is added in three ways:

- **Solid:** frozen at the bottom of the sump. This is the optimistic case.
- **Sump:** free water that stays in the sump, with its surface level with the sea's at every angle. The sump is the space below z 45 mm between x 560 and 770, less the keel box. Water beyond the sump's capacity spills into the bay.
- **Bay:** free water that can run anywhere in the dry bay between the bulkheads, as if the foam blocks didn't fit at all. This is the pessimistic bound.

## Results

| Water | Treated as | GM (m) | GZ at 20° (mm) | Max GZ (mm) | Righting at 180°? |
|---|---|---|---|---|---|
| none (intact Rev E) | | 0.177 | 62 | 350 at 110° | yes, positive to 180° |
| 0.5 kg | sump / bay | 0.173 | 61 | 347 | yes |
| 1.5 kg | solid | 0.176 | 62 | 339 | yes |
| 1.5 kg | free (overflows the sump) | 0.166 | 58 | 333 | yes |
| 3.0 kg | solid | 0.175 | 61 | 329 at 100° | yes |
| 3.0 kg | free | **0.158** | 55 | 318 | yes |

- **Stability is fine.** The worst case, 3 kg sloshing freely through the whole bay, takes 11% off GM and 9% off the maximum righting arm. The boat still rights itself from any angle, and the area under the curve falls only from 0.50 to 0.46 m·rad. Free water near the deck even helps a little when the boat is almost upside down, because it runs to the low side.
- **One problem: the sump holds only 1.2 L, not 3 L.** The drawn sump is 210 mm long and only 45 mm deep where the hull bottom is narrow, less the keel box. Rev E's SAFE limit is 1.5 kg, so water passes the sump before the boat stops to wait:

| Water | Where it lies | Highest wetted point (above the hull bottom), upright / 20° / 40° / 90° heel |
|---|---|---|
| 1.2 kg | sump, full | 43 / 45 / 45 / 45 mm |
| 1.5 kg | spills into the bay | 23 / 64 / 115 / 231 mm |
| 3.0 kg | bay | 34 / 78 / 136 / 234 mm |

  The electronics box sits on a shelf with its bottom at z 118 mm. With 1.5 kg aboard and the foam blocks not sealing, a 40° roll puts water at the bottom of the box. In a knockdown it reaches the deck. The box is sealed and its glands are on top, so this is a margin problem, not a failure. But the pump-and-sail policy was set without knowing the sump's real size.

## Recommendation

- **Adopted 14 Nov (Rev E1): lower Rev E's SAFE limit from 1.5 kg to 1.0 kg**, inside the sump's 1.2 L. This is a firmware setting (`autopilot.leak_safe_kg`). The pump keeps up with every simulated leak (worst 2.5 kg/day against 500 kg/day), so the boat should reach 1.0 kg only if the pump has failed. The change should cost the simulator nothing measurable; a run will confirm it if adopted.
- **Or deepen the sump** to hold 3 L (z 45 → about 95 mm over the same footprint). That is a mould and foam-block change, not worth it on these numbers.
- **Change the simulator's flood limit** to the volume the boat really leaves (`hull.flood_limit_kg`: 1.2 if the blocks seal, more if they don't). Measure it on the real boat: fill the sump from a jug until the probe sees water above the rim, at the same time as the 3 L check in Test G.

Not modelled: the dynamics of sloshing (the static free-surface effect is what's computed), water in the foam itself, and the battery box filling (it is sealed; if it filled, 0.35 kg of box plus water low in the boat would barely change GM).
