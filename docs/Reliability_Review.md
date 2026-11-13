# Reliability review: steering servos, weed and leaks

12 November 2026. Randolph asked, after the first Rev D run, for fixes to the three things that now end most voyages: the rudder and tail servos, weed fouling, and leaks. He suggested more sweep on the keel and rudders, a bulb that does not stick out ahead of the fin, a pressurised hull, and a small bilge pump. This note works through each, says what the run data shows, and sets up three simulator runs to price the fixes. Nothing here is drawn yet; what gets adopted becomes Rev D1 (parts changes) once the runs are in.

## What ends voyages in the Rev D run

250 voyages, 2023 weather, 10 km off Ocean City. 155 arrived (62.0%); 95 did not. Reading the event logs of the 95:

| Failure | Voyages it appeared in (of the 95 losses) | If it was the first thing to go wrong, how many still arrived |
|---|---|---|
| Leak | 41 | 18% (22 voyages) |
| One rudder servo jammed or went limp | 49 (both rudders lost in 32 voyages overall) | 60–77% |
| Tail servo failed free (wing feathers) | 21 | **0%** (15 voyages) |
| Tail servo jammed at an angle | 17 | 58% (19 voyages) |
| Fouled by weed or line | 22 | 81% (32 voyages) |
| Picked up by a fishing boat | 18 | 0% |
| Electronics (main box) | 17 | 89% (the limp-home controller sailed them in) |

Three things stand out.

1. **Leaks don't sink the boat; our response does.** Not one boat was swamped: since Rev C1 the foam-filled hull can only hold about 3 kg of water. What happens is that the leak sensor puts the boat into safe mode (wing feathered, no steering) and, as written, it never comes out. It drifts until it grounds (11 of the 22) or the season ends. The leaks themselves are 0.05 to 2.5 kg a day.
2. **A tail servo that fails free is a certain loss.** The wing weathervanes, and the boat drifts. A tail jammed at an angle is survivable more than half the time.
3. **Weed costs little in the model**, because the model lets a fouled boat clear itself in about a week. That assumption deserves scrutiny (below): a vertical fin with a bulb nose sticking out ahead of it is the shape that holds weed.

## 1. Leaks

### A bilge pump, and a different response (Randolph's suggestion: yes)

A small brushless diaphragm pump in the sump, on the same probe that raises the leak alarm. A 12 V pump of about 0.5 L/min clears the worst day's leak (2.5 kg) in five minutes, for about 1 Wh. The outlet loops up inside the hull and leaves through the transom above the waterline, with a check valve, so the sea cannot siphon back in. About 100 g, about $25, plus a strainer on the pickup.

With the pump, the response becomes: **keep sailing, pump, report the leak rate.** Safe mode only if the water keeps rising with the pump running (over 1.5 kg), and back to sailing once it is pumped down. The pump's run time becomes the leak meter in the daily report.

What it does not fix: water standing in the sump still raises the humidity around the electronics (the model charges for that above 0.3 kg; the pump keeps it below), and the pump is one more part. It needs a strainer and a bench life test (72 hours of cycling in salt water).

My estimate: +6 to 8 points of arrivals. The run below will say.

### Pressurised hull (Randolph's idea: the test, not the pressure)

The idea is to keep the dry bay at a slight overpressure so that air leaks out rather than water leaking in. The physics is right at the waterline, where the outside pressure is only 0.01 bar per 10 cm of depth. The difficulties:

- **It needs a gas supply.** Any path that lets water in also lets air out, so the overpressure bleeds away through the same leak it is holding off. A CO2 cartridge and regulator would last until the first real leak, then the boat is back where it started, with a regulator and valve as new failure points.
- **Temperature does the opposite job for free, and badly.** A sealed air space breathes with every warm day and cold night. Gore's engineering note says that in unvented housings, pressure differentials as low as 70 mbar (1 psi) can cause seals to leak after repeated temperature cycles, and after a seal fails, further pressure imbalances draw liquids into the housing. That is the mechanism by which "sealed" boxes get wet. The cure in outdoor electronics is a membrane vent, which serves as a pressure relief valve to protect seals from stress while blocking water.

What the subsea world does instead is instructive. Ocean instrument housings are purged with dry air and then left with a small partial vacuum: the small amount of residual vacuum, under 1/3 bar, beneficially pre-loads the housing seals prior to deployment, and sensors can alert the user to a seal leak. The pressure trend before launch is the leak test: if there is a slow loss of the vacuum, there is a leak somewhere.

So the useful half of the idea is **a pressure-decay test and a vent**, not a pressurised hull:

- **Pressure-decay test** of the dry bay and of the electronics box, at the build and before every launch: a Schrader valve in the hatch lid, a bicycle pump to 0.1 bar, a U-tube or digital manometer, and no measurable drop in 30 minutes. A leak found on the dock is free; the same leak at sea is a lost voyage. This replaces the "72-hour submersion" in Field Test G as the routine check, and keeps the submersion as the acceptance test.
- **A membrane vent** (Gore PolyVent or equal, rated for immersion) in the hatch lid, so the dry bay breathes through a membrane instead of past the hatch O-ring and the cable glands. The same on the electronics box lid. About $15 each.
- **A humidity and pressure sensor** (BME280, $5) in the dry bay, reported daily. With the pump's run time, that gives three independent leak signals.

### Where our leaks will come from

The rate in the model is borrowed from ocean gliders. On this boat the likely paths, in order: the rudder trunk tops (they sit 71 mm above the waterline inside the hull, and a wave fills a trunk to the top; the boots and lip seals in the build plan are not optional), the mast bearing tube, the hatch O-ring, the six cable penetrators, the keel rod nuts, and the YB3 well. Every one of these is testable with the pressure-decay test.

## 2. Rudder and tail servos

Both rudders failed in 32 voyages out of 250 (13%). The tail servo failed in 59 (24%), half of them free. Together they are in about half the losses.

### Why servos die

Hobby servos fail in three ways: the position potentiometer wears (a carbon track rubbed by a wiper on every movement), the gears strip or corrode, and water gets past the case seals. On duty: coreless-motor servos are rated for approximately 400,000 cycles, four times a standard brushed motor, and a long-running forum estimate for a servo in continuous use is that the potentiometer will have the shortest life, one month, maybe more, maybe less. Our rudder servos make a correction every few seconds for four months: on the order of a million movements. The tail servo moves far less.

The fix is a different class of actuator, not a better hobby servo: a **brushless motor and a magnetic position encoder** (no brushes to wear, non-contact sensing that eliminates the wear associated with traditional potentiometers), in a **sealed housing**.

### Options

| | What | Cost for two rudders | Note |
|---|---|---|---|
| S0 | Savöx SW-1210SG as specified (IP67 hobby servo, potentiometer, brushed) | $186 | What the 0.002/day rate assumes |
| S1 | Blue Trail Engineering SER-2020: 34 kgf-cm, brushless motor and magnetic encoder, depth-rated to 200 metres, $495 | $990 | The right part; the price hurts |
| S2 | Blue Trail SER-2000 enclosure kit $215, takes a standard-size servo of your choice, with a WetLink penetrator) with a DFRobot magnetic-encoder servo inside 25 kg, magnetic encoder, steel gears, $21.90) | $475 | Sealed, no potentiometer, but a brushed motor |
| S3 | DFRobot magnetic-encoder servo in our own potted housing | $60 | Cheapest; our seal, our risk |

Recommendation: **S2 for the rudders**, with S1 if the budget allows. For the **tail**, which lives up the mast and moves little, a DFRobot magnetic-encoder servo potted in its own case (S3), plus the detent below.

### Make the tail fail jammed, not free

A tail that fails free kills the boat; a tail stuck at an angle usually does not. Fit a **magnetic detent**: a pair of small magnets that hold the tail at about ±8° when the servo stops holding it. The servo overcomes them easily when powered. If the gears strip or the servo loses power, the tail snaps to one detent and the wing keeps driving. In a gale a wing stuck at 8° is not what we want, but the boat is self-righting and the alternative is certain loss. About $10.

In the model this turns the "failed free" share of tail failures from 50% to perhaps 10%.

### Work the servos less

- A **deadband and a rate limit** in the steering loop: no correction under 2°, no more than one every 10 seconds except in a gybe. This alone could cut rudder movements five-fold, and wear is cycles.
- **Cut servo power between corrections** (already in the build plan). A balanced rudder needs almost no holding force.
- **Trunks packed with grease and the servos above the trunk tops** (as drawn). The servos must never sit in standing water: another reason for the pump.

### What the model can and cannot say

The simulator's servo rate (0.002 per servo per day, grade D) comes from three or four events in the Microtransat record. It cannot tell a brushless sealed servo from a hobby one. The run below halves the servo rates for S2/S3 and sets the tail's free share to 10%. **Both are guesses.** A bench life test (two servos cycling in a salt-fog box for the number of movements a crossing takes) is how the numbers become real, and it costs a few weeks of running time, not money.

## 3. Weed

### The shape we have

The fin is nearly vertical (1.7° of sweep), and the bulb nose sticks out 91 mm ahead of the fin tip. That is the classic weed trap: weed slides down a leading edge until it meets a forward-facing step, and the fin–bulb notch holds it. Experienced sailors are blunt about it: a 45 degree leading edge is a great, practical fin angle whether fixed or pivoting. Stuff slides off it. Chain doesn't wrap up on it. Against that, designers warn that a large sweep-back angle cripples the performance of high-aspect-ratio keels, by making water flow down the span instead of across the chord, though the same source notes that Delft towing-tank tests found sweeping back a keel's leading edge 45 degrees or more is beneficial in reducing the drag of a low-aspect ratio keel with long chord lengths. Our fin, at an aspect ratio near 2.7, sits between the two cases.

### Options

- **W1, the fairing (cheap, do it regardless).** Fill the notch between the fin's leading edge and the bulb nose with a swept fairing: a foam-and-glass ramp from the fin's leading edge at about 200 mm above the tip, running forward and down to the top of the bulb nose. That turns the 90° step into a slope of about 25–30° from vertical. Weed sliding down the fin continues down the ramp and off the nose. About 0.1 kg, $20, no change to the fin or the keel box.
- **W2, bulb nose flush with the fin.** Move the bulb aft so its nose sits on the fin's leading-edge line. To keep the boat's trim, the fin and keel box move forward by the same 90 mm (fin root at x 566 instead of 657). That moves the centre of lateral resistance forward by 6% of the waterline, which changes helm balance. The simulator can check it (the fin position is a parameter) before anyone cuts foam. The bulb's lead and the fin's structure do not change.
- **W3, rudders with raked leading edges.** Rake the rudder leading edge 35° by moving the tip aft 160 mm, keeping the stock vertical and the balance area at the top. The rudder's loads barely change. Weed and line slide down and off the heel. Cheap: it is a template change.
- **W4, a shedding manoeuvre in software.** When speed falls more than 40% below the polar for an hour with no change in the wind, feather the wing and let the boat round up and stop for ten minutes, then bear away. With raked edges the weed slides off while the boat sits; a vertical fin needs the boat to back down, which we cannot do.
- **Not recommended: sweeping the whole fin 45°.** With the bulb's weight fixed under the boat's centre of gravity, a 45° fin puts its root 430 mm forward, under the wing mast, and rebuilds the keel box, floors and tenon from Rev C2. The fairing (W1) and the flush nose (W2) get most of the benefit for a fraction of the work.

### What the model says, and what it assumes

In the Rev D run, fouling appeared in 65 voyages and those boats still arrived 66% of the time, because the model lets a fouled boat clear in about a week (0.15 a day). If the true clearing rate for a vertical fin with a protruding nose is a month (0.03 a day), fouling becomes a leading cause of loss. The third run below tests that downside on the boat as drawn. The package run gives W1–W4 together credit for half the catch rate and a clearing rate of 0.5 a day. **All three numbers are guesses.** The tow test (Field Test A) can measure one of them: drag a bundle of kelp or rope across the fin at 1 kn and see whether it stays.

## The runs

Queued on the PC behind the launch-point study (`simulator/run_reliability_2023.bat`, about four hours). 250 voyages each, 2023 weather, the same launch dates and seeds as the Rev D run, so each is a paired comparison with Rev D as drawn (62.0%).

| Run | Design file | What it tests |
|---|---|---|
| 1 | `designs/revD_pump_study_design.json` | Bilge pump (500 kg/day, 4 W, fails 0.0005/day) and the pump-and-sail response |
| 2 | `designs/revD_reliability_study_design.json` | Run 1 plus servo rates ×0.5 (S2/S3), tail free share 10% (detent), weed catch ×0.5 and clearing 0.5/day (W1–W4) |
| 3 | `designs/revD_weed_pessimistic_study_design.json` | Rev D as drawn, but weed clears at 0.03/day: the downside if the model is kind to the current fin |

New design keys: `autopilot.leak_policy` ("safe" or "pump_and_sail"), `autopilot.leak_safe_kg`, `bilge_pump`, `rudder.servo_rate_factor`, `wing.tail_servo_rate_factor`, `wing.tail_fail_free_share`, `keel.weed_catch_factor`, `keel.weed_clear_per_day`. Rev D as drawn keeps every old value, so earlier results stand.

## Recommendation so far

In order of confidence:

1. **Bilge pump and the pump-and-sail response.** Certain to help, cheap, and the model's leak losses are mostly self-inflicted. Adopt for Rev D1 whatever the run says about the size of the gain.
2. **Pressure-decay test, membrane vents, humidity sensor.** Cheap, and they catch leaks before launch. Adopt.
3. **Sealed magnetic-encoder rudder servos (S2), a potted tail servo with a magnetic detent, deadband steering.** The biggest remaining cause of loss. Adopt S2 and the detent; buy S1 if the budget allows. Run the bench life test either way.
4. **Weed: the fairing (W1), raked rudders (W3) and the shedding manoeuvre (W4).** Cheap insurance against a risk the model may understate. Check the flush nose (W2) in the simulator before deciding.

Costs, if all adopted with S2: about $600 and 0.4 kg over Rev D.

## Sources

- [Gore: protective vents and seal stress from temperature cycling](https://www.gore.com/node/21661); [Gore: pressure relief for outdoor housings](https://www.gore.com/solutions-enclosure-pressure-relief)
- [Ocean News: moisture control in subsea housings (purge and vacuum pre-load)](https://oceannews.com/?p=39765); [Marine Technology, March 2023: vacuum leak tests and purge ports](https://magazines.marinelink.com/Magazines/MarineTechnology/202303/page/44)
- [Blue Trail Engineering SER-20XX underwater servos (Blue Robotics forum)](https://discuss.bluerobotics.com/t/new-underwater-servos-from-blue-trail-engineering/13749)
- [DFRobot 25 kg magnetic-encoder waterproof servo](https://www.dfrobot.com/product-2789.html); [DFRobot brushless magnetic-encoder servos (Mouser)](https://www.mouser.fi/new/dfrobot/dfrobot-pwm-magnetic-encoder-brushless-servos/)
- [Robotdigg: servo types and rated cycles](https://www.robotdigg.com/news/242); [comp.robotics.misc: servo life in continuous use](https://groups.google.com/g/comp.robotics.misc/c/akeO1iCaOx8/m/tFrqwn4ke2IJ)
- [Boat Design forum: swing keels and the 45° leading edge](https://www.boatdesign.net/threads/swing-keel-not-vertical.67603/); [Vacanti, keel design (TU Delft repository)](https://repository.tudelft.nl/file/File_f6d76529-9032-4dd8-9e47-a723e41e08c6)
