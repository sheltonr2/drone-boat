# Structural review of the whole boat (Rev C2)

11 November 2026. Grade D: a physics model with published coefficients and handbook material values. Nothing here has been tested on the boat yet.

Scripts and their output are in `docs/data/`: `strike_sim.py` (breaking-wave strike simulation), `structural_checks.py` (hand checks), `keel_reliability.py` (the earlier fin study).

## Verdict

The hull, deck, hatch, keel bolts and battery mounts have comfortable margins. **Four parts above the deck do not: the stern post, the counterweight arm, the rudder servos and the wing spar.** The first three have cheap fixes. The wing spar is the one large risk that this review cannot settle either way.

| Part | Worst load in a 1-in-1,000 strike | Strength | Chance of breaking per voyage (gentle / central / hard) | With the change below |
|---|---|---|---|---|
| **Stern post** (carries the main antenna, wind vane, light and the backup tracker) | 199 N·m | 115 N·m | 95% / 100% / 100% | 0% / 2% / 14% |
| **Counterweight arm** (12 mm carbon tube, 1 kg pod) | 63 N·m | 53 N·m | 31% / 96% / 100% | 0% / 0% / 1% |
| **Rudder servos** (forced backwards by the blade) | 9 N·m | 2 N·m stall | 98% / 100% / 100% | 0% / 1% / 4% |
| **Wing spar** | 1,400 N·m | 690 N·m | 44% / 100% / 100% | 2% / 93% / 100% |
| Keel-box joint (tenon) | 313 N·m | about 700 N·m | 0% / 4% / 16% | unchanged; proof test K |
| Rudder stocks | 28 N·m | 75 N·m | 0% / 2% / 7% | unchanged |
| Tail boom | 24 N·m | 53 N·m | 0% / 1% / 2% | unchanged |
| Keel fin (Rev C2) | 313 N·m | 1,100 N·m | 0% / 0% / 0% | — |

A voyage sees about 660 knockdowns on real 2023–2024 weather, so a part needs a chance of breaking below about 1 in 10,000 per knockdown to be safe. "Gentle / central / hard" are three sets of assumptions about the breakers, described below. Per-voyage figures between 5% and 95% are not to be trusted; the ranking is.

## What the simulation replaced

Three inputs to the earlier load work were guesses. The strike simulation now derives them from the boat's mass, inertia and shape and a published model of breaking-wave impact.

| Quantity | Was (guess) | Now (simulated, seas of 5 m) |
|---|---|---|
| Share of the water's speed the hull picks up | 25–85% | 75% (median) |
| Time for the hull to reach half that speed | 0.05–0.4 s | 0.014 s in a plunging breaker; 0.2 s in a spilling one |
| Roll rate in a knockdown | 1.6 rad/s | median 0.9–1.5 rad/s; 1 in 20 above 3 rad/s; 1 in 1,000 about 4.5 rad/s |
| Peak sideways acceleration of the hull | not estimated | plunging: 16 g typical, 68 g 1 in 20, for a few thousandths of a second. Spilling: under 2 g |

The 1.6 rad/s guess was a fair typical value, but the loads that break things come from the 3 rad/s tail. The fast pick-up in a plunging breaker is what matters most: the hull is light (26 kg), so the water takes it up to speed in about a hundredth of a second, and everything attached on a stalk gets a sharp sideways jolt of 2–5 m/s.

## How the strike model works

- **The boat** is a rigid body free to move sideways and roll, with the fin and bulb dragging in the slower water below.
- **The breaker** is water moving at 60–110% of the breaker's own speed, hitting the hull side. A plunging breaker hits as a wall: slamming coefficient up to 2π, falling to ordinary drag once the hull is about 0.4 radii into the water (Wienke and Oumeraci's model for breaking waves on cylinders). A spilling breaker builds up over 0.2–0.6 s with ordinary drag only.
- **Breaker heights** follow the rule the voyage simulator already uses for knockdowns: the tail above 0.825 m, which is the 55%-of-length figure from the Southampton capsize tests.
- **Stalk-mounted parts** (bulb on fin, wing on spar, pod on arm, tail on boom, gear on the stern post) are spring-mass systems driven by the hull's motion where they attach. The wing and the post also take water directly when the moving water reaches them.
- **The wing slapping the water** as the boat goes over is added from the roll rate, assuming the free wing swings edge-on within 0.08 s of touching.

## The four fail points

**1. Stern post.** The 20 × 1.5 mm aluminium tube carries about 0.9 kg of gear up to 0.39 m above its bracket. A sideways jolt of 3 m/s bends it. The main Iridium antenna and the backup tracker are both on it, so one bent post silences both: the backup is not independent of the failure it is there to cover.
- *Change:* move the YB3 to the aft deck (it has its own antenna and battery), and make the post a 20 × 2 mm pultruded fibreglass tube, which bends instead of kinking. The clamps P05, P19 and P20 keep their 20 mm bore.

**2. Counterweight arm.** A 1 kg pod on a 12 × 10 mm carbon tube. A carbon tube is stiff and strong but stores little energy, and a jolt is an energy problem. A drop of 20 cm onto the water (2 m/s) takes it to 93% of its strength; 46 cm breaks it (`structural_checks.py`).
- *Change:* a 12 mm solid pultruded fibreglass rod in the same sockets. It stores about six times the energy. About +40 g.

**3. Rudder servos.** When the stern is thrown sideways, each blade is pushed broadside and tries to turn its stock with up to 9 N·m. The servo's stall torque is about 2 N·m (from memory of the Savox SW-1210SG data sheet; check). The servo gears take that load.
- *Change:* a spring servo-saver in each linkage, and hard stops for the tiller at ±40° on the hull, so the blade can be forced over without the servo seeing it.

**4. Wing spar.** Two mechanisms: the moving water of a plunging breaker hitting the wing (up to about 540 N·m), and the wing slapping the water as the boat goes over (about 460 N·m 1 time in 20, 1,400 N·m 1 in 1,000). The slap grows with the cube of the roll rate, so it is driven by the rare fast rolls.
- The model's chance of losing the wing in one knockdown runs from 0.0002–0.001 (gentle) to 0.01–0.03 (central). The voyage simulator uses 0.0009 (planning rates), which sits near the gentle end. So the simulator's largest single failure cause may be understated by up to ten times, or about right. This model cannot say which.
- *Change worth making anyway:* a 30 × 22 mm spar (same outside diameter, bearings and printed parts; strength 1,130 N·m, about +0.3 kg). It cuts the chance per knockdown by roughly five to ten times.
- *What would settle it:* Test L below.

## Parts that pass

| Part | Load case | Factor of safety |
|---|---|---|
| Hull bottom over the sump (the only shell panel with no foam behind it) | 52 kPa slam, 1-in-1,000 strike | 2.2 (inner skin and core shear) |
| Hull and deck where foam-backed | 52 kPa on the foam fill | 4.8 (a dent at worst) |
| Hatch lid, 4 mm G10 | 33 kPa from a jet landing on deck | 11 |
| Hatch lid, glass over 6 mm foam | same | 2.2 (core shear; the core must be H80, not XPS) |
| Hatch bolts | lid forced outward when inverted | 12 |
| Keel rods in a bottom slam | bulb at 50 g | 12 |
| Hull girder in a bottom slam | 850 N·m amidships | 13 |
| Battery straps and anchors | 60 g jolt | high in shear; peel of the printed anchors is unchecked |
| Rudder bushings and trunks | blade broadside at 4 m/s | 5 |
| Wing spar in wind alone | 50 m/s, wing jammed broadside | 2.3 (13 N·m when feathered) |
| Bearing housing P07 (printed PETG) | spar at its breaking load | 1.7 with the present spar; 1.0 with a 30 × 22 spar |

Two notes on the passes:
- **The printed bearing housing becomes the weak link if the spar is strengthened.** With a 30 × 22 spar, machine the housing from acetal or aluminium, or space the bearings 150 mm apart instead of 78.
- **The inner skin over the sump is one ply.** A second ply there costs about 20 g and takes the factor from 2.2 to above 4.

## What is still a guess

- **The share of knockdowns that are plunging breakers** (10%, 20% or 40% in the three cases). Deep-water breakers are mostly spilling; steep seas over the Gulf Stream are where plunging ones come from.
- **How thick the moving water is** above the boat, and how much air is in it. This sets the direct load on the wing and post.
- **How fast the free wing swings edge-on** when it touches water (0.08 s assumed).
- **The count of 660 knockdowns per voyage** comes from the voyage simulator's breaking-wave rule, which is itself a model.
- **Material strengths** are handbook values.
- **Not modelled:** being thrown end over end, fatigue, impact with debris or a vessel, grounding.
- One source I meant to use for measured buoy accelerations in breakers could not be opened today, so the acceleration figures have no measured check yet.

## Tests that would turn the guesses into data

- **Test L, breaker test:** put the finished hull (dummy rig of the right mass, no electronics you care about) in 0.8–1.2 m shore break, beam-on, on a tether. Log the Pixhawk's accelerometer and gyro at 400 Hz or more. Twenty strikes give the hull's speed jump, how fast it happens and the roll rate directly, which are the three numbers every load in this note hangs on. Film it.
- **Test M, wing slap:** with the boat on its side on a lake, drop the wing into the water from heights that give tip speeds of 1, 2 and 3 m/s, with a strain gauge on the spar at the upper bearing. This measures the slap load and how fast the wing swings edge-on.
- **Test K** (keel proof load) and **Test C** (spar proof load) already cover the two static strengths.

## Recommended changes, in order of value

1. Move the YB3 to the aft deck and change the stern post to fibreglass tube.
2. Fibreglass rod for the counterweight arm.
3. Servo-savers and tiller stops on both rudders.
4. 30 × 22 mm spar with a machined or longer bearing housing.
5. Second inner ply over the sump.

None of these is drawn yet. Items 1–3 and 5 add about 0.1 kg; item 4 about 0.3 kg.

## Sources

- [Wienke and Oumeraci, breaking wave impact force on a slender pile](https://www.scribd.com/document/355814311/icce2004-wienke-03-pdf) (slamming coefficient 2π, impact at wave speed)
- [Wang et al., slamming force contribution due to plunging breakers](https://strathprints.strath.ac.uk/71861/1/Wang_etal_OMAE2019_Slamming_force_contribution_due_to_plunging_breakers.pdf)
- [Good Old Boat, "Capsize: how it happens"](https://goodoldboat.com/capsize-how-it-happens) (Southampton tests: breaking wave of 55% of boat length)
