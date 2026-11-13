# Rev E design changes and rationale

13 Nov 2026. Rev E is Rev D plus the leak, servo and weed measures from the reliability review ([Reliability_Review.md](Reliability_Review.md)). Randolph approved them on 13 Nov. The review called the package "Rev D1". It takes a new letter because it adds a system (the bilge pump) and a sensor ([Revisions.md](Revisions.md)). Rev D: [Design_RevD.md](Design_RevD.md).

## What changed from Rev D

**Leaks: keep sailing and pump**
- **Bilge pump.** A 12 V self-priming diaphragm pump (D28 motor, about 0.5 L/min) stands upright against the port side of the mast tube, above the sump, on spacer **P24**. The strainer sits at the sump's low point, port of the keel box. The centreline there is the keel box itself. The outlet hose loops up to z 226 under the deck, through a check valve, to a 1/4 in. through-deck fitting just aft of the hatch on the starboard side. Above the waterline at any heel the boat sails at, the fitting can't siphon.
- **New leak response.** The leak probe starts the pump and the boat keeps sailing. It reports the pump's run time as a leak meter. It goes to SAFE only if the water passes 1.5 kg with the pump running, and comes back out below half that. Rev D went to SAFE at the first alarm and never came back out.
- **Finding leaks before launch.** The hatch lid gets a membrane vent and a capped Schrader valve, both in lid corners clear of the RockBLOCK bowl. The electronics-box lid gets a second vent, and bulkhead x 300 gets a humidity and pressure sensor (BME280). The pressure-decay test (0.1 bar, no measurable drop in 30 minutes) becomes the routine check before every launch.

**Servos: sealed, worked less, failing safe**
- **Rudders:** each servo is a DFRobot magnetic-encoder servo (no potentiometer to wear) inside a Blue Trail **SER-2000** sealed enclosure, rated to 200 m, with a titanium 6 mm D-shaft.
  - Each sits in cradle **P12**, which replaces the servo mount, held by two 316 clamps. The cradle has no fixed hole pattern, because we don't have the enclosure's drawing. Its 66 × 34 × 72 mm envelope is an **estimate**: measure the unit and rebuild P12 before printing.
  - The D-shaft takes arm **P26**. The C3 spline servo-saver doesn't fit a D-shaft, so a spring overload link in each pushrod replaces it. The G10 stops at ±40° stay.
  - The aft-foam pockets grow to 100 × 56 mm.
- **Steering:** a 2° deadband, at most one correction every 10 seconds outside a gybe, and servo power off between corrections.
- **Tail:** a DFRobot magnetic-encoder servo, potted in P09, with magnetic detent **P25**: two magnets at ±8° and a steel disc in the fin root. If the servo lets go, the tail snaps to ±8° and the wing keeps driving instead of feathering. In Rev D, a tail that failed free was the one certain-loss failure (15 voyages in 250).

**Weed**
- **Fin-to-bulb fairing (W1):** a glassed foam ramp from the fin's leading edge at z −250 to the top of the bulb nose, about 22° from vertical (template **T21**, sheet D04). Weed sliding down the fin runs off the nose instead of hooking in the step. About 0.1 kg and $20.
- **Weed-shedding manoeuvre (W4), software:** if speed falls 40% below the polar for an hour with steady wind, feather, round up for ten minutes, then bear away.
- **Not adopted:**
  - **Raked rudders (W3).** The review called them a template change, and that was wrong. A 35° rake moves the blade tip 160 mm aft, which puts it past the transom and takes the lower blade off the stock. A smaller rake with a tapered blade would need a shorter stock or a skeg. It is a redesign, and the model says weed is worth about a point.
  - **Flush bulb nose (W2):** deferred. It moves the fin and changes the helm balance.

## Effect on the boat

- **Mass:** 28.5 kg (Rev D 27.8). The two sealed enclosures weigh about 0.17 kg each more than the Savöx servos. The pump, hoses, vents and sensor add 0.2 kg, and the fairing 0.1 kg.
- **Waterline and stability:** waterline z 106 mm (was 104); GM 0.180 m (was 0.182), still self-righting.
- **Cost:** about +$360, which brings the itemised total to about $3,280.
  - Pump, strainer, hose, check valve and deck fitting: about $50.
  - Two vents, the BME280 and the Schrader valve: about $40.
  - Two SER-2000 kits with DFRobot servos instead of two Savöx: +$288.
  - DFRobot tail servo instead of a Savöx: −$71.
  - Magnets, fairing and spring links: about $50.
- **Drawings:** sheets D00, D03, D04, D05, D06 and D08 changed. New printed parts P24, P25 and P26; P12 replaced; P09 notes changed. New template T21. Build files: `build-files/README.txt`.

## In the simulator

`designs/revE_design.json` (revision "E") holds:
- the pump (500 kg/day, 4 W, fails 0.0005/day) and `leak_policy: pump_and_sail`;
- servo rates ×0.5 for the rudders and the tail, and a tail free-failure share of 10% (detent);
- weed catch ×0.75 and clearing 0.3/day. The reliability package gave ×0.5 and 0.5/day for all four weed measures; Rev E has two of them.
- the extra mass.

The servo and weed numbers are **guesses** until the bench life test and the tow test. The default design is still Rev D, so older result files keep their meaning.

**First run:** `simulator/run_revE_2023.bat`, queued on Randolph's PC after the launch study (request 012): 250 voyages, 2023 weather, same seeds as Rev D. Expect a little under the package study's 80.8%.

## Tests added ([Field_Tests.md](Field_Tests.md))

- **Test G:** the pressure-decay test becomes the routine check before every launch.
- **Test O, pump:**
  - 72 hours of cycling in salt water through the strainer.
  - Check that the check valve holds with the outlet 30 cm under water.
  - Check that the pump empties a 2.5 kg flood in under 10 minutes on the boat.
- **Test P, servo life:** two SER-2000 rudder servos cycling ±10° every 3 seconds, loaded through a spring, in salt fog, for 1 million movements. Log position error, current and any water inside. This turns the ×0.5 guess into a number.
- **Test Q, tail detent:** with the servo unpowered, turn the fin by hand. It must stop at ±8° and hold against a 2 kn flow on the lake. Powered, the servo must move it through the detents without stalling.
