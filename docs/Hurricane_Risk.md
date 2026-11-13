# Hurricane and tropical-storm risk on the Mid-Atlantic route

*9 November 2026. Our half of the joint hurricane hazard with boat-sim: how often a tropical cyclone passes close to the boat, by launch month. boat-sim supplied the other half, the ERA5 wind correction (boat-sim #117). Code: `simulator/drone_sim/storms.py` (`python -m drone_sim.cli stormcheck --mc <result.json>`). Data: [`docs/data/hurdat2_atlantic_1981-2025_box.csv`](data/hurdat2_atlantic_1981-2025_box.csv) (NOAA NHC HURDAT2, public domain).*

## Bottom line

| Launch (from 100 km off Ocean City) | Tropical storm or worse within 200 km | … of which hurricane | Within 100 km |
|---|---|---|---|
| April | **0.1%** (0.0–0.4) | 0.1% | 0.0% |
| May | **5%** (1.5–9) | 1.1% | 2.6% |
| June | **17%** (10–24) | 5.1% | 8.7% |
| July | **20%** (15–26) | 7.5% | 11% |

*200 simulated voyages (planning failure rates, synthetic weather, launches April–July) × 35 analog seasons (1991–2025). The ranges in brackets are 95% intervals, resampled over whole seasons.*

- **Launch date matters more than anything else.** Each month of delay after early May adds roughly 5–12 points of storm exposure. Encounters cluster around day 30 of the voyage (10–90% range: day 5 to day 60), near 52°W (70–41°W), and in July and August. A boat launched in early May is usually east of 45°W by July, ahead of the season.
- **This is a risk the simulator can't otherwise see.** Synthetic weather has no tropical cyclones. ERA5 has them, but at roughly 0.70 of the true wind for tropical storms and 0.42 for Category 4 (boat-sim #117). So real-weather runs understate the storms, too.
- **Plan on a 1 May launch with a hard stop around 20 May.** Past late May, the storm exposure on its own costs a few points of success. A rough loss model makes this concrete: assume a 30% chance of losing the boat for a tropical storm passing within 100 km and 70% for a hurricane (both grade D; *Bearly Assailable* was lost to TS Kyle, and Saildrone's 7 m boats survive hurricanes). On those assumptions the storm risk adds about **1% loss for a May launch, ~4% for June and ~5% for July**, on top of the other failure modes.

## Update, 13 November: real-weather tracks from 12 launch points

The table above used fast synthetic-weather voyages. The launch-point study ([Launch_Point_Study.md](Launch_Point_Study.md)) now gives real-weather (ERA5 2023) tracks from 12 launch points, 150 voyages each, launched 1 May–15 June. Same method: each voyage moved onto the same dates in every season 1991–2025, and the share of seasons with a tropical or subtropical cyclone of at least 34 kt passing within the radius.

| Launch | Storm (≥34 kt) within 200 km | … hurricane | Storm within 100 km | … hurricane | Launched in May | Launched 1–15 June | Success → with the storm loss model |
|---|---|---|---|---|---|---|---|
| Hatteras, 45 km (charter) | 17.6% | 4.8% | 9.0% | 2.0% | 16.3% | 20.2% | 54.0% → 52.9% |
| Ocean City, 100 km (charter) | 18.0% | 4.6% | 8.3% | 2.0% | 14.8% | 24.5% | 50.0% → 49.1% |
| Hatteras Inlet, 10 km | 17.2% | 4.0% | 9.0% | 1.8% | 15.7% | 20.1% | 49.3% → 48.4% |
| Virginia Beach | 17.6% | 4.6% | 8.7% | 1.9% | 14.7% | 23.2% | 48.7% → 47.6% |
| **Ocean City, 10 km (current plan)** | 18.2% | 4.6% | 7.8% | 1.8% | 15.1% | 24.5% | 46.7% → 45.8% |
| Cape Cod | 18.3% | 4.5% | 8.1% | 1.5% | 16.9% | 21.0% | 46.7% → 45.7% |
| Montauk | 17.4% | 3.6% | 8.2% | 1.3% | 17.6% | 17.1% | 46.0% → 44.9% |
| Maine | 10.7% | 3.7% | 4.3% | 1.6% | 9.9% | 12.5% | 44.0% → 43.3% |
| Charleston | 22.9% | 5.4% | 13.0% | 2.6% | 22.4% | 23.9% | 43.3% → 41.8% |
| Palm Beach | 24.8% | 6.4% | 13.5% | 2.5% | 24.9% | 24.7% | 42.7% → 41.2% |
| New Jersey (Barnegat) | 19.5% | 5.4% | 9.7% | 2.5% | 19.1% | 20.2% | 34.7% → 33.9% |
| Cape Canaveral (flawed route) | 21.8% | 5.5% | 11.6% | 2.0% | 20.9% | 23.6% | 31.3% → 30.2% |

*"Launched in May" and "1–15 June" are the 200 km column split by launch date. The loss model is the grade-D one above (30% for a tropical storm within 100 km, 70% for a hurricane), applied to each successful voyage. ERA5 2023 already contains 2023's real storms, smoothed, so there is a small double count.*

- **Exposure is about three times what the synthetic table said** for a May launch (15% within 200 km from Ocean City, not 5%). Real-weather crossings are slow: median about 120 days, and 82% of boats are still at sea after 90 days. So boats are still in the western and central Atlantic in the peak of the season. From Ocean City, half the encounters come after day 60 of the voyage; by calendar month they fall in June (25%), July (34%), August (14%), September (16%) and October–November (11%); median longitude 51°W.
- **Storms don't change the launch ranking.** With the loss model, every launch point loses 0.7 to 1.5 points of success. The southern launches (Palm Beach, Charleston, Canaveral) are the most exposed, at 22–25% within 200 km, and lose the most, about 1.5 points; Maine the least. The top of the table (Hatteras charter 52.9%, Ocean City charter 49.1%, Hatteras Inlet 48.4%) keeps its order.
- **Launch date still matters more than launch point.** From Ocean City, a 1–15 June launch meets storms 24.5% of the time, against 15.1% for May. From Hatteras the gap is smaller (16% to 20%), because those boats are faster.
- **What would change this:** the loss model. 30% and 70% are guesses (grade D). If a tropical storm within 100 km usually kills this boat, storms would cost 4–6 points and push the launch earlier, not further north or south. Field Test C (self-righting) and a storm-sea knockdown test are the evidence that would firm this up. The ERA5 wind correction from boat-sim #117 is still not applied inside the voyage loop.

Script: `docs/data/launch_storms.py` (output `docs/data/launch_storms.json`), applying `storms.StormClimatology` to `results/2026-11-13_launch_2023_<launch>__ireland_sw.json`.

## Method

- **Analog seasons.** For each simulated voyage (hourly positions), and for each season from 1991 to 2025, we move the voyage onto the same calendar dates in that year. Then we check whether any tropical or subtropical cyclone with ≥34 kt winds passed within the radius at the same hour. Best tracks are interpolated from 6-hourly to hourly. Extratropical stages are excluded because ERA5 handles them well.
- **Why 200 km:** it matches boat-sim's wind-ratio definition, and gale-force winds in Atlantic storms commonly reach 150–300 km from the centre. The 100 km column is closer to "inside the damaging core".
- **Intervals:** voyages in the same season share its storms, so we resample whole seasons rather than counting voyage-seasons separately. The second approach gave intervals several times too narrow.
- **Tracks:** these are synthetic-weather voyages. Re-run on the real-weather (bulk ERA5) Monte Carlo once it finishes. Real tracks will meander differently, but the launch-month pattern should hold.

## How it plugs into the odds

1. `stormcheck` reports encounter probabilities for any Monte Carlo result that has time-stamped tracks (every run made from today on).
2. The **survival effect** needs a damage model, and that's a judgment call (grade D) until there are knockdown tests at storm sea states. The numbers above use 30% loss for a tropical storm within 100 km and 70% for a hurricane. Field Test C (self-righting) and a mast-in-water load test are the evidence that would firm these up.
3. **Wind correction (boat-sim #117)** for real-weather runs: scale ERA5's wind near a best-track centre by 1/ratio for that storm's class (median ratios: TS 0.70, C1 0.66, C2 0.59, C3 0.53, C4 0.42). The ratios are in `storms.ERA5_RATIO` but not yet applied inside the voyage loop. That's the next step if launch dates past mid-May stay on the table.

## Sources

- NOAA National Hurricane Center, HURDAT2 Atlantic best tracks (`hurdat2-1851-2025-092326.txt`): <https://www.nhc.noaa.gov/data/hurdat/>
- boat-sim #117: ERA5 / best-track wind ratio by storm class (Actions artifact `era5-storm-wind-ratio`, PR #119)
- Crossing history (TS Kyle and *Bearly Assailable*; Oshen PC13 and TS Dolly): [Crossing_History.md](Crossing_History.md)
