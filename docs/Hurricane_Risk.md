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
