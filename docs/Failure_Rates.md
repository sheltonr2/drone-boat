# Failure rates for small autonomous ocean sailboats

*Shared hazard table for drone-boat and boat-sim (our half of the agreed work split). Compiled 8 November 2026. Rates are **events per day at sea** unless stated. The code lives in `simulator/drone_sim/failures.py`, the data in `docs/data/crossing_attempts.csv`, and the analysis in `docs/data/hazard_analysis.py` (output saved in `docs/data/hazard_analysis_output.txt`).*

## Summary

1. **Our simulator was too optimistic.** The rates we used up to now ("original") gave a 57% chance that the boat is still reporting at day 90. The best real-world record for our size class, the Microtransat, gives 9% (95% CI 1–30%) for west-to-east boats. The gap comes from four failure modes: the boat going **silent** while still sailing, **fishermen** taking or snagging boats near the coast, **rig damage** in heavy weather, and **failures in the first week** of untested hardware.
2. **We fitted a new rate set to the record and added three mechanisms to the simulator.** The new mechanisms are a *comms-silent* failure (the boat sails on but cannot report), an *early-life* (infant-mortality) multiplier that a shakedown period reduces, and a capture band that reaches the edge of the shelf (~150 km). The scenario now selects one of three rate sets: `historical` (the fit to the record), `planning` (the new default, with credit only for mitigations that are in our build plan), and `original` (kept so that old results can be reproduced).
3. **Effect on the Mid-Atlantic → SW Ireland plan** (100-run Monte Carlo, April–July launches 2022–2025, synthetic weather): the chance of arriving **and still reporting** falls from 48–51% under the original rates to **37% (95% CI 28–47%) under planning** and **22% (15–31%) under historical**. Under the historical set, the simulator matches the record's survival curve through day 60. It stays too kind after that, so even the historical number is an upper bound (§6). The changes that move the odds most are passing the 3-week coastal trial, fitting a second independent tracker, and keeping time on the fishing shelf short (§5).

## 1. How the numbers were built

**Exposure-based hazards.** For each failure mode, rate = (number of mission-ending events) ÷ (boat-days at risk). The 95% intervals are exact Poisson intervals. This is the standard method for fleets that cannot be lab-tested, as used for gliders by Brito, Smeed & Griffiths (2014). It lets records of very different lengths be combined fairly.

**Two phases.** Every attempt's days are split into *near land* (within ~150 km of a coast: the shelf, the channels and the fishing grounds) and *open ocean*. The record shows the two phases behave very differently, so a single average rate would mislead.

**Competing risks.** Each mode is treated as an independent clock, which is also how the simulator draws them. Only the first fatal event ends a run.

**Quality grades** (the last column of the table in §2):

| Grade | Meaning |
|---|---|
| A | Large fleet statistic (thousands of vehicle-days), peer-reviewed |
| B | Smaller fleet or analogous vehicle, peer-reviewed or official |
| C | Our own analysis of the small Microtransat record (tens of events, wide intervals) |
| D | Engineering judgement or a back-of-envelope model. Replace it as soon as a test or better data exists |

## 2. The shared table

These are the planning values (the default set). "Historical" is the fit to the Microtransat record, and "Range" is what we would defend as plausible for a careful amateur build in our size class. Multipliers are applied in the code.

| Hazard (sim key) | Planning | Historical | Range | Multipliers in the sim | What happens | Grade | Main evidence |
|---|---|---|---|---|---|---|---|
| Leak starts (`leak`) | 0.0025 | 0.0025 | 0.0015–0.0045 | ×(1+(Hs/3)²); ×early-life | Water comes in at 0.05–2.55 kg/day. Leak sensor → SAFE mode. Swamped at 35% of displacement | B | Gliders: 15 leak aborts in 5,753 days = 0.0026/day (95% CI 0.0015–0.0043) |
| Electronics die (`electronics`) | 0.0025 | 0.0035 | 0.0012–0.006 | ×6 once water is inside; ×early-life | Boat silent **and** uncontrolled: lost | C | Microtransat open ocean: 2 silent + 2 erratic-then-silent + 1 antenna fault in 622 days = 0.008/day of silent-type endings, minus the leak-driven share the sim already produces (~0.0023/day). Gliders: power or battery 0.0016/day |
| Comms go silent (`comms_silent`) **new** | 0.0011 | 0.0022 | 0.0005–0.004 | ×(1+Hs/4); ×early-life | Modem, antenna or comms power path fails. **The boat sails on, unheard.** If it arrives, it counts as "arrived silent", not a success | C | SB Wave 2017: antenna fault at day 69. In the Global Drifter Program, 68% of drifters that die simply stop transmitting |
| Rudder servo (`rudder_servo`) | 0.002 | 0.002 | 0.001–0.004 | ×(1+Hs/4); ×early-life | Jams (60%) or goes limp (40%) | D | Microtransat: 1 actuator failure, plus 2 offshore boats that steered erratically before going silent. SeaCharger's steering failed after ~155 days. PC13 had to work round rudder faults |
| Tail servo (`tail_servo`) | 0.002 | 0.002 | 0.001–0.004 | as above | Wing stuck at a fixed angle, or feathered | D | As above. Gortobot v4: sail motor failure |
| Rig damage per knockdown (`knockdown_damage`) | 0.003 per knockdown | 0.006 | 0.002–0.01 | Knockdown rate comes from breaking-wave physics | Wing lost: the boat drifts | C | Microtransat open ocean: 3 rig or weather losses in 622 days = 0.0048/day. SD 1021's wing broke when it was rolled in the Gulf Stream |
| Taken or snagged by fishermen near land (`capture`) | 0.01 within ~150 km | 0.02 | 0.005–0.03 | Only within `capture_km` (160) of land | Boat removed: lost | C | Microtransat near land: 4 taken in 215 days = 0.019/day (95% CI 0.005–0.048). USNA lost 3 of 6 Cape Cod starts to fishermen |
| Entanglement (`entanglement`) | 0.003 | 0.003 | 0.001–0.01 | ×3 within 100 km of land; ×2 in the Sargasso | Drag ×4 until it clears (mean ~7 days) | D | ABoat Time 2014 (scallop net). Solar Voyager 2016, offshore. NMFS warned fixed-gear fishermen about Saildrone's casts |
| Ship strike (`collision`) | 0.0004 | 0.0004 | 0.0002–0.002 | ×8 within 100 km of land; 60% fatal | Boat lost, or a leak | D | No confirmed strikes in 837 Microtransat boat-days (95% upper bound 0.0044/day). Kinematic model in §4.3 |
| Software hang (`software_hang`) | 0.02 | 0.02 | 0.005–0.05 | Watchdog clears 95% | Hung computer: no reports until a power cycle | D | ABoat Time 2015 grounded after a software bug. Our build has a hardware watchdog and boots into safe mode |
| Fouling growth (`fouling_growth`) | +0.004 drag factor per day at 20 °C | same | 0.002–0.008 | Scales with sea-surface temperature | Slows the boat; does not kill it | D | Lightfish arrived after 62 days with "dozens" of barnacles. PacX Wave Gliders grew barnacles wherever there was no antifouling. On ships, 10% barnacle cover costs about 36% more power |
| Early life (`early_life`) **new** | k = 3, τ = 7 d, 14-day shakedown | k = 3, τ = 7 d, no shakedown | k 1–5 | Multiplies the hardware hazards by 1 + k·e^(−(day+shakedown)/τ) | Infant mortality | D | Microtransat: 46% of boats had stopped by day 7; the near-land silent rate (0.033/day) is ~5× the open-ocean rate. Every successful team had long sea time first (Oshen succeeded on its third boat) |
| Groundings | modelled physically | | | Land mask + autopilot clearance | Aground | n/a | 7 of the 25 near-land Microtransat losses were groundings, almost all from English Channel launches in strong tides |
| Hurricanes and tropical storms | separate climatology | | | `stormcheck` (HURDAT2 analog seasons) | Knockdowns, rig damage | C | TS+ within 200 km: April 0.1%, May 5%, June 17%, July 20% of voyages ([Hurricane_Risk.md](Hurricane_Risk.md)). TS Kyle ended *Bearly Assailable* (2020) |

**Design credits behind the planning set.** Each credit is a factor applied to the historical rate. It is earned by a specific feature in `Build_Plan.md` and **confirmed by a test**. Until the test passes, the honest number is the historical one.

| Mode | Factor | Earned by | Confirmed by |
|---|---|---|---|
| Electronics | ×0.7 | IP68 box potted to the hull, desiccant, humidity sensor | 72-hour submersion of the sealed box; humidity log flat for 14 days of shakedown |
| Comms silent | ×0.5 | Backup Saft D-cell on the comms rail, hardware watchdog | Pull the main battery on the bench: the RockBLOCK keeps reporting for the cell's rated life |
| Rig damage | ×0.5 | Buoyant, balanced wing on a self-righting hull | Test C (self-righting), plus a mast-in-water knockdown load test |
| Capture | ×0.5 | Large "research vessel – do not remove" labels with a contact number, notice through the fishery council, offshore drop point | No direct test. Only experience will confirm it |
| Early life | 14-day shakedown | The 3-week unattended coastal trial in the build plan | Field Test F's pass criteria: 14 days in a row with no unexplained reboot, leak or comms gap |

## 3. Reference fleets: what professional vehicles achieve

| Fleet | Exposure | Rate | What it tells us |
|---|---|---|---|
| European underwater gliders (Seaglider, Slocum), 12 labs, 205 missions (Brito et al. 2014) | ~5,750 glider-days | Mission aborts 0.011/day (0.0076 Seaglider to 0.0168 Slocum shallow). Leaks 0.0026/day. Power 0.0016/day. Vehicle losses 0.0017/day. A 90-day deep mission had about a 50% chance of running to the end | Professional vehicles still end missions early at about 1% a day. Our planning hazard (0.0063/day for losses over the whole voyage in the Monte Carlo) is in the same range, so it is not optimistic |
| Argo profiling floats | Millions of float-days | Modern SOLO-II floats: ~98–99% of cycles completed. Older batches: 80–90% still working after 5 years | Shows what sealed, simple electronics can reach after many build iterations: a lower bound we cannot claim yet |
| Global Drifter Program (Lumpkin et al. 2012) | 13,127 dead drifters | 68% stopped transmitting, 23% ran aground, 7% were picked up | Silence is the main way small floating electronics die, and being picked up is a real hazard even for drifters |
| Wave Glider PacX (2011–13) | 4 vehicles, ~1 year each | 2 of 4 completed (one after servicing), 1 rescued, 1 left drifting | Even well-funded fleets lose about half on very long legs |
| Saildrone hurricane missions (2021–24) | 5–12 vehicles a season | We found no published losses; SD 1045 survived Cat 4 Sam and was redeployed | Purpose-built 7 m rigs can survive extreme weather. This is *not* evidence for our 1.5 m wing |
| Microtransat (2010–2023) | 837 boat-days, 33 endings | Near land 0.116/day; open ocean 0.013/day | Our size class and build culture. The pessimistic bracket |

Iridium SBD links are not a big source of silence on their own. A polar buoy study captured about 95% of its data, and fixed NOAA stations exceed 99.9%. Missed sessions are already in the sim (p_ok falls with sea state, and is zero when inverted), so the `comms_silent` hazard covers hardware death, not individual dropped messages.

## 4. Derivations for the less obvious rates

### 4.1 Silent failures (electronics + comms_silent)
In the open ocean the record shows 8 mission-ending events in 622 boat-days. Of these, 5 are silent-type: 2 went silent with no warning, 2 steered erratically and then went silent, and 1 antenna fault led to the boat being picked up. That is 0.008/day. The simulator already turns about 0.0023/day of leaks into losses, so we split the remaining ~0.0057/day between electronics that kill the boat (0.0035) and comms failures that leave it sailing (0.0022). The split is judgement (grade C). The total is not. With planning credits these become 0.0025 and 0.0011.

### 4.2 Capture near land
Near land, the record shows 4 boats taken by fishermen plus 1 caught in a net, in 215 boat-days, so 0.019/day for capture alone. Our Ocean City launch crosses the Mid-Atlantic Bight shelf, a scallop, trawl and longline area about 100–130 km wide. At 1–1.5 kn that takes the boat 2–4 days, and the approach to SW Ireland adds about the same again. The old model applied capture only within 50 km of land, so the boat was exposed for a few hours. The new one applies it to ~150 km, so the boat is exposed for 5–8 days in all. Under the planning rate (0.01/day) that is a 5–8% chance of loss. The Monte Carlo gave 4 of 100 runs under planning and 14 of 100 under historical, where early-life failures also stretch the time spent near land.

### 4.3 Ship strike
Kinematic model (after Merckelbach 2013 for gliders): encounter rate = ρ × V × W. Here ρ is ships per km², V is ship speed (14 kn ≈ 620 km/day), and W is the swept width (beam ~32 m plus our 0.4 m). That gives:

| Ship density ρ | Example | Encounters per day |
|---|---|---|
| 1×10⁻⁵ per km² | Open ocean away from the lanes | 0.0002 |
| 1×10⁻⁴ per km² | Inside a transatlantic lane | 0.002 |
| 1×10⁻³ per km² | Port approaches, Traffic Separation Schemes | 0.02 |

Our 0.0004/day offshore (×8 near land) corresponds to ρ ≈ 2×10⁻⁵ offshore and ≈ 1.6×10⁻⁴ near the coast. That is plausible, and it sits inside the zero-event bound from the record. It is still grade D, because the real exposure depends on how long we sit in the lanes. **Next step:** replace the flat rate with an AIS vessel-density map (EMODnet Human Activities, or Global Fishing Watch for fishing effort) sampled along each simulated track. That would also give a location-based capture rate.

### 4.4 Early life
Half the Microtransat boats were gone by day 7. Some of that is location (tides, fishermen), but the near-land *silent* rate (0.033/day, with no grounding or capture in it) is about 5× the open-ocean silent rate. Reliability engineering models that as a falling hazard (a Weibull shape below 1). We use a multiplier 1 + k·e^(−t/τ) with k = 3 and τ = 7 days, which averages about ×2.9 over the first week. A shakedown of S days before launch shifts the curve by S. Fourteen days cuts the launch-day multiplier from 4.0 to 1.4.

## 5. What moves our odds (cheapest first)

1. **Pass the 3-week unattended coastal trial against Field Test F's criteria** (now written into `Field_Tests.md`): 14 days in a row with no unexplained reboot, leak or reporting gap. This removes most of the early-life bump. The planning numbers already assume it, so **skipping or shortening the trial puts us back on the historical curve** (see the no-shakedown row in §6).
2. **A second, independent tracker** (its own battery, antenna and modem; a commercial satellite tracker or a second RockBLOCK on a primary cell). In the simulator, "arrived and reporting" rose from 37% to 41%. More important, the 12% of boats that arrive silent become boats we can find, so "arrived, and we know where" rises to about 47–49%. Roughly $150–250 plus airtime.
3. **Keep the shelf crossing short and visible:** an offshore drop beyond the shelf edge, labels, a notice to the fishery council, and a radar reflector (already in the plan). An AIS class-B SART or transponder would help with both ships and fishermen if the power budget allows.
4. **Steering that fails safe:** a rudder that centres itself when the servo loses power, so the wing can still drive the boat downwind toward Europe.
5. **Leak testing to an engineered standard:** pressure-test every penetration and do a 72-hour submersion of the finished hull, so the leak credit is earned rather than assumed.

## 6. Simulator check against the record

Mid-Atlantic → SW Ireland, 100 runs per rate set, launches April–July 2022–2025, synthetic weather, same seeds for every set. "Still reporting" uses the Microtransat yardstick: the day of the last report, where a silent arrival counts as a failure.

| Rate set | Arrived, still reporting | Arrived silent | Lost at sea | Aground outside Europe | Still reporting at day 30 / 60 / 90 | Main causes of loss |
|---|---|---|---|---|---|---|
| original (rerun with the new code) | **48%** (95% CI 39–58) | 6% | 40% | 5% | 0.89 / 0.74 / 0.57 | Leaks 22, electronics 13, ship strikes 5 |
| **planning (new default)** | **37%** (28–47) | 12% | 47% | 4% | 0.74 / 0.61 / 0.47 | Electronics 23, leaks 19, fishermen 4 |
| planning, no shakedown | 32% (24–42) | 13% | 48% | 7% | 0.67 / 0.54 / 0.42 | Leaks 22, electronics 21, fishermen 4 |
| planning + second tracker (`comms_silent` off) | 41% (32–51) | 6% | 49% | 4% | 0.79 / 0.68 / 0.52 | Electronics 24, leaks 20, fishermen 4 |
| historical | **22%** (15–31) | 13% | 60% | 5% | 0.58 / 0.45 / 0.33 | Electronics 28, leaks 16, fishermen 14 |
| *Microtransat record, west to east (17 boats)* | *1 of 17 finished* | | | | *0.47 (0.23–0.68) / 0.29 (0.11–0.51) / 0.09 (0.01–0.30)* | *Silent, fishermen, rig damage* |

**How to read this.**
- **The historical set reproduces the record up to day 60.** Its survival curve sits inside the record's 95% interval at 7, 14, 30 and 60 days. By day 90 it is above the interval (0.33 against 0.01–0.30). After two months the simulator is still too kind, because it has **no wear-out** (bearings, servos and seals that get worse with age), synthetic weather with no hurricanes, and no late-season gales. A wear-out term (a Weibull hazard rising after ~60 days) is the next model change.
- **Planning is better than the record by design.** That improvement is only valid once the credits in §2 have been earned by tests.
- **Differences of about 5 points sit inside the noise of 100 runs** (each 95% CI spans ±9–10 points). The no-shakedown and second-tracker rows show the direction of each effect, but not its exact size. A 400-run batch per row would halve the noise. The real-weather batch in `run_next_checks.bat` will use the planning set.
- **A second tracker is worth more than its row shows.** With one, the 12% of runs that arrive silent become arrivals we can find and recover. So "arrived, and we know where" goes from 37% to about 47–49%.
- **Silent arrival is now a real outcome** (12–13% of runs). The old rate set seldom produced it (6%).
- These runs launch 25 km off Ocean City. The default launch has since moved 100 km out, after the real-weather drift tests ([Route_MidAtlantic.md](Route_MidAtlantic.md)). Under the planning set, that drop gave 30% (95% CI 22–40%), with groundings down from 4 to 1 and captures from 4 to 1. The difference from 37% is noise: more leak and electronics losses happened to be drawn.
- For reference, the 51% in earlier documents came from the original set before this change. The rerun gives 48%. The code now draws random numbers in a different order, so individual runs differ, but the result is statistically the same.

## 7. Notes for boat-sim

The table in §2 uses plain per-day rates with explicit multipliers, so it can be lifted into boat-sim directly. The CSV and analysis script are standalone (Python + SciPy). Two things are worth matching so our numbers can be compared: (1) the split of every voyage into near-land and open-ocean phases, and (2) treating a silent arrival as a failure, not a success.

## References

- Brito, M., Smeed, D. & Griffiths, G. (2014). Underwater glider reliability and implications for survey design. *J. Atmos. Oceanic Technol.* 31(12), 2858–2870. doi:10.1175/JTECH-D-13-00138.1
- Lumpkin, R., Grodsky, S. A., Centurioni, L., Rio, M.-H., Carton, J. A. & Lee, D. (2012). Evaluating where and why drifters die. *J. Atmos. Oceanic Technol.* 29(2), 300–308.
- Merckelbach, L. (2013). On the probability of underwater glider loss due to collision with a ship. *J. Mar. Sci. Technol.* 18, 75–86. doi:10.1007/s00773-012-0189-7
- Microtransat Challenge, history of attempts: <https://www.microtransat.org/history.php>
- Scripps (SIO) Argo float failure-rate tables: <https://sio-argo.ucsd.edu/fail_web_enter.html>; Argo survival by deployment year: *Oceanography* 34(4), 2021
- NOAA–Saildrone Atlantic hurricane missions: <https://www.pmel.noaa.gov/usv-hurricane/2024/index.html>
- NMFS / Saildrone notice to fixed-gear fishermen: <https://www.workboat.com/coastal-inland-waterways/noaa-says-keep-lookout-for-saildrones-cruising-gulf-of-maine>
- Seasats *Lightfish* crossing and arrival condition: <https://www.dvidshub.net/news/printable/551741>
- Saildrone SD 1021 storm damage and crossings: <https://www.saildrone.com/news/saildrone-completes-fastest-atlantic-crossing-unmanned-vehicle>
- Oshen *C-Star PC13*: <https://www.sciencetimes.com/articles/62633/20260922/robotic-sailboat-crosses-atlantic-after-traveling-5400-kilometers-without-human-intervention.htm>
- Iridium data-capture rates: polar buoy study, arXiv:2309.13714
- Biofouling power penalty (10% barnacle cover → ~36% more power): I-Tech / Selektope industry data
- Full list of crossings: [`Crossing_History.md`](Crossing_History.md)
