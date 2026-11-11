# Field tests: replacing the simulator's guesses with measurements

The simulator's speed and stability rest on a few numbers nobody has measured yet: how hard the water drags on the hull, how stiff the boat is, and how much the solar panels really deliver. About half a day of tests on the finished boat replaces those guesses. Do them during build gate 3, before the coastal trial.

This page is adapted from John's tow test for his kayak drone ([jcolter11374/boat-sim](https://github.com/jcolter11374/boat-sim), `docs/tow-test.md`).

**People:** two. **Water:** at least 1.5 m deep (the keel reaches about 0.56 m down), flat and with little wind.

## What you need

- The boat **fully built at sailing weight** (about 20.8 kg), wing fitted and balanced.
- A **digital hanging scale reading to 1 g** with at least a 1 kg range (a pocket "fishing" or jewellery hanging scale). The pulls are small: about 60 g at 1 knot and 750 g at 3 knots.
- 15 m of **floating line**, a **phone GPS speed app**, and a phone **inclinometer** app.
- A **1 kg weight** (a bag of lead shot or a water bottle) and a tape measure.
- A **bathroom or luggage scale** to weigh the whole boat.
- For test E, an inline **DC watt-hour meter** between the charge controller and the battery.

## Test A: tow drag (2 hours)

1. Tie the hanging scale between the tow line and the bow. Tow from the side of the towing boat, out of its wake.
2. Centre the rudder and tape the wing's tail at 0°, so the wing points into the wind and makes no push.
3. Tow at a steady **1.0 knot** by GPS for one minute and film the scale. Then turn and repeat the other way.
4. Repeat at **1.5, 2.0, 2.5 and 3.0 knots**. Average each pair of runs, which cancels any current.

What the model expects today:

| Speed (knots) | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 |
| --- | --- | --- | --- | --- | --- |
| Pull (kg) | 0.062 | 0.142 | 0.269 | 0.462 | 0.746 |

Fit the hull's drag factor from your readings:

```
python -m drone_sim.calibrate tow 1,1.5,2,2.5,3 <your five pulls in kg, comma separated>
```

It prints the new `form_factor` and how well the fit matches. Put it in your design file under `"hydro"`.

## Test B: inclining (30 minutes)

This measures GM, the boat's stiffness against heeling. It is the number the self-righting and knockdown results depend on.

1. Weigh the whole boat.
2. Float it in still water, sheltered from wind, with the wing removed or tied fore and aft. Zero the inclinometer on the deck.
3. Put the 1 kg weight on the centreline, then move it **30 cm to one side** and read the heel angle. Move it 30 cm to the other side and read again.

The Rev C model expects about **3.6°** for 1 kg moved 30 cm (Rev B: 4.1°). Work out the real GM:

```
python -m drone_sim.calibrate incline 1.0 0.30 <heel angles in degrees, comma separated> --mass <weighed kg>
```

If the measured GM is more than about 15% below the model's 0.19 m (Rev C; Rev B 0.20 m), find out why (a heavy deck fitting, or a light bulb) before going to sea.

## Test C: self-righting (15 minutes)

Roll the boat fully upside down by hand and let go. It must come back upright on its own every time, from both sides. Then try 90° with the wing flat on the water. This is build gate 3. Film it.

## Test D: wing balance (at assembly)

With the wing, tail, boom, arm and pod assembled on the spar, add lead shot to pod P18 until the rig sits level at any heading with the tail at 0°. Write down the lead you used. The model expects about **0.8 kg**. More than 1.0 kg means the tail end came out heavy, so update `"tail": {"kg": ...}` in the design file.

## Test E: solar day (one sunny day, on the bench)

Leave the finished boat in full sun from dawn to dusk with the electronics running, and read the watt-hours the meter logged going into the battery. Compare with the simulator's solar output for that date and place. If the measured value is lower, adjust `"soiling_salt"` under `"power"` until it matches.

## Test F: shakedown at sea (14–30 days, before launch)

This test sets the pass criteria for the 3-week unattended coastal trial, the build plan's last gate before an ocean launch. It is about reliability, not about measuring the hull. In the Microtransat record, half of all boats were lost within a week, mostly to faults that a few weeks on the water would have exposed. The simulator's default "planning" failure rates **assume this test has been passed**. Skip it, and the honest numbers are the "historical" ones (see [Failure_Rates.md](Failure_Rates.md)).

Put the finished boat, at sailing weight, on a swivel mooring or a short coastal loop in protected water for at least 14 days, with the full electronics running and reporting through Iridium at the crossing interval. It passes when all of these hold for 14 days in a row:

- No unexplained reboot or watchdog reset. Log the reason for every reset.
- The leak sensors stay dry, and the internal humidity stays flat (no rising trend).
- No reporting gap longer than two report intervals.
- The battery state of charge at dawn does not fall from week to week.
- Servos and the wing still move freely afterwards, with no salt binding at the bearings or the tail pivot.

Any failure resets the 14-day count after the fix. Record the start date and the results in `results/`, and set `"burn_in_days"` under `"early_life"` in your scenario to the days actually completed.

## Additions (9 Nov 2026)

- **Test C, spar proof load:** with the hull clamped, hang 32 kg from the wing spar 0.8 m above the lower bearing for one minute (≈250 N·m, the knockdown case in [Storm_Loads.md](Storm_Loads.md)). There must be no cracks or permanent set. With the recommended 30–32 mm spar, repeat at 38 kg.
- **Test F, backup tracker:** during the coastal trial, switch the main system off for 48 hours and confirm that the backup tracker's reports keep arriving ([Backup_Tracker.md](Backup_Tracker.md)).


## Additions for Rev C (10 Nov 2026)

- **Test G, compartment leak test (before the deck goes on, and again on the finished hull):** pressurise each space to about 0.1 bar through a temporary fitting and brush soapy water over every joint, bulkhead tape and penetration. No bubbles anywhere. Then submerge the finished hull for 72 hours and weigh any water you can sponge out of each space: it must be zero.
- **Test H, free-flood volume:** with the dry-bay foam blocks and both boxes in place, fill the dry bay with water from a measuring jug through the hatch until it reaches the deck. It must take **3 L or less** (the simulator's `flood_limit_kg`). If it takes more, cut more blocks. Sponge it dry and leave the hatch open to dry for a day.
- **Test I, one-rudder steering:** on the lake, disconnect one rudder servo (leave the blade free) and sail the 20 km gate course on the other alone; then repeat with the first one clamped at 10° to the side. The boat must hold course within ±15° in both cases. Then swap sides.
- **Test C, spar proof load (Rev C):** with the 30 × 26 mm spar fitted, hang 38 kg (1.2× the knockdown case) 0.8 m above the lower bearing for one minute; no cracks, no permanent set.
- **Test B (Rev C):** the expected heel and GM above are for the Rev C mass of about 25 kg. Weigh the boat first: the model expects about 25.2 kg. More than 26 kg means the foam fill or a laminate came out heavy; update the design file.
- **Test J, wet-bay soak (Rev C1):** with the boat complete and powered, pour 3 L of salt water into the sump through the hatch and close up. Rock the hull through ±40° every few seconds for an hour (or leave it on a mooring in chop for a day), lay it on each side for a minute as a knockdown, then leave it wet for 72 hours with the electronics running. Pass: the box is dry inside, the desiccant card has not changed colour, every connector is dry, and insulation resistance from each supply rail to seawater is still above 1 MΩ. This is the evidence for the simulator's `wet_electronics_factor` of 2; if it fails, set it back to 6.
- **Test K, keel proof load (Rev C2), before paint and again after Test F:** lay the finished hull on its side on padded trestles under the hull sides at x 300 and x 1260, fin horizontal, deck hatch open so you can see the keel box. Hang weight from the middle of the bulb in steps of 10 kg up to **60 kg** (260 N·m at the fin root, about 7 times the load of a knockdown in flat water), hold for one minute, then unload. Measure the bulb's height above the floor before, at each step and after. Pass: no cracking sounds, no cracks or whitening in the glass at the fin root, the keel box, the floors or the hull bottom, and the bulb returns to within 1 mm of where it started. Expect the bulb to drop about 7 mm at 60 kg from the fin bending alone; more than 15 mm means the fin or the joint is much less stiff than drawn. Repeat with the boat on its other side. Wear boots and keep feet clear of the weights.
- **Test B (Rev C2):** the model now expects about 26.4 kg and GM 0.19 m.
- **Test C, spar proof load (Rev C3):** with the 30 × 22 mm spar, hang 60 kg 0.8 m above the upper bearing for one minute (about 470 N·m, the 1-in-20 wave-strike load); no cracks, no permanent set, and the bearing housing P07 must not have moved or cracked in the mast tube.
- **Test B (Rev C3):** the model now expects about 26.9 kg and GM 0.18 m.
- **Test L, breaker test (Rev C3):** hull complete with a dummy rig of the right mass and no electronics you care about except the autopilot, in 0.8–1.2 m shore break, beam-on, on a 20 m tether from the beach. Set the Pixhawk to log raw accelerometer and gyro data at 400 Hz or more. Collect at least twenty strikes and film them. From the log read, for each strike: the jump in sideways speed, the time it took, the peak roll rate and the peak acceleration. Compare with `docs/Structural_Review.md` (expected: 2–4 m/s, 0.01–0.3 s, 1–3 rad/s). These three numbers set every load in the structural review; send the log and the loads can be recalculated from it.
- **Test M, wing slap (Rev C3):** boat on its side on a lake, held by two people. Bond a strain gauge (or a cheap clip-on dial gauge reading spar deflection) at the upper bearing. Lift the wing tip and let the boat roll it into the water so the tip arrives at about 1, 2 and 3 m/s (drop heights 5, 20 and 46 cm). Record the peak reading and film from above to time how fast the wing swings edge-on. Stop if the reading passes half the Test C value.
- **Rudder servo-savers (Rev C3):** with the boat ashore, push each blade hard over by hand: the saver must give before the servo is forced, and the tiller must meet its stop block at about 40°.
