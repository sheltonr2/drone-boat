# Collaboration log

Newest first. Each check of boat-sim records what was new and what we did.

## 2026-11-08, 22:00

- New on #50 since our last post: boat-sim finished all three of their items. Priya compared GLORYS with SMOC (the means agree, the eddies don't line up). Ravi ran the drifter check (skill 0.23 in the eddy field, 0.78–0.86 in the Hatteras jet) and the dead-boat run (Hampton Roads after 9.6 days, about 15 km from our grounding point on day 5). They also found ERA5 storm winds are about 0.5–0.7 of best track, and they fixed #69–#72.
- Posted our update ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6731239476), text in [comment_50_failure_rates.md](comment_50_failure_rates.md)). It covers the failure rates, the crossing history and the drift tests. It also says we'll take the storm-frequency half of the joint hurricane hazard and pair it with their ERA5 wind correction, and asks to speed up on both sides, noting that John has authorized more resources if needed.
- Next: hurricane frequency model (HURDAT2/IBTrACS by launch month along both routes); Randolph runs `run_real_mc.bat`.

## 2026-11-08, late

- Randolph ran `run_next_checks.bat` ([log](run_log_next_2026-11-08.txt)). **Drift tests** (dead boat, 30 days, real weather, four 15 May dates): from 25 km off Ocean City, 3 of 4 went ashore within 2–5 days. From 100 km off, 4 of 4 stayed at sea and moved east toward the Gulf Stream. From 150 km off, 3 of 4 did, with one ashore at Cape May on day 13.5. The default launch is now 100 km off Ocean City (38.02N 74.01W).
- **Real-weather Monte Carlo failed**: Open-Meteo's rate limit stopped it about a fifth of the way through the download. The job needed about 64,000 calls, because Open-Meteo counts every location in a request and the 0.25° grid adds about 2,000 blocks. Our earlier estimate of 7,500 counted requests, which was wrong.
- Fixes: the downloader now counts calls per location in a ledger, paces itself under the hourly limit, and stops cleanly at the daily limit. `--wait-for-limits` sleeps until the next UTC day and carries on, keeping Windows awake. The Monte Carlo prints its download size before it starts. New `simulator/run_real_mc.bat`: 60 voyages from the 100 km drop, 1 May – 15 June launches in 2023–2024, about 23,000 calls, so 2–3 days unattended.
- The #50 comment about failure rates is still waiting for Randolph's approval. The drift results are worth adding to it.

## 2026-11-08, night

- Finished our half of the split: [docs/Failure_Rates.md](../docs/Failure_Rates.md) and [docs/Crossing_History.md](../docs/Crossing_History.md). The data is [docs/data/crossing_attempts.csv](../docs/data/crossing_attempts.csv) (all 37 Microtransat attempts 2010–2023) and [hazard_analysis.py](../docs/data/hazard_analysis.py).
- Finding: open-ocean hazard 0.013/day, near-land 0.116/day; only 1 of 37 finished. Our old rates were too optimistic: 57% still reporting at day 90 against the record's 9%.
- Simulator: three rate sets (`planning` default, `historical`, `original`), a new `comms_silent` failure, early-life failures that a shakedown reduces, and capture out to ~150 km. The rate set can be picked in the web UI. Mid-Atlantic Monte Carlo: 37% (planning), 22% (historical), 48% (original).
- Added Field Test F, the pass criteria for the 3-week coastal trial.
- `run_next_checks.bat` now uses the planning rates.
- Next: draft a #50 comment for Randolph's approval; wait for boat-sim's dead-boat run and drifter check; HURDAT2 hurricane hazard and a wear-out term.

## 2026-11-08, evening

- Ran `simulator/run_collab_checks.bat` on Randolph's Windows PC ([log](run_log_2026-11-08.txt)). Self-test passed on live Open-Meteo data.
- Dead boat (36.85N 75.70W, 2023-05-15): drifted north, then into the Chesapeake Bay mouth; aground near the York River after 8.9 days, 344 km.
- Grid check (Ocean City to SW Ireland, 2024-05-15): 86.3 days at 1 deg, 101.8 days at 0.25 deg. Added a 0.25 deg grid for 30-50N, 80-38W.
- Shared both results on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6730249929)). No new boat-sim comments since ours at that point.
- Added `simulator/run_next_checks.bat`: drift tests from three drop points off Ocean City (four May dates) and an 80-run real-weather Monte Carlo.
- Next: Randolph runs it; we write docs/Failure_Rates.md and docs/Crossing_History.md; wait for boat-sim's dead-boat run and drifter check.

## 2026-11-08

- Their side: issue #50 opened with three notes on our simulator (Stokes double count, 1° grid, Europe box), then a follow-up proposing the collaboration protocol (#53) and a split of work. Last boat-sim commit seen: 28add65.
- Our side: applied all three notes (8107f25), moved our launch to the Mid-Atlantic, and replied on #50 accepting the split ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6727663938)). Added the dead-boat scenario and this folder.
- Next: start `docs/Failure_Rates.md` and `docs/Crossing_History.md`; Randolph to run the dead-boat scenario and `gridcheck` on real data.
