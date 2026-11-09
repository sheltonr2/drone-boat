# Collaboration log

Newest first. Each check of boat-sim records what was new and what we did.

## 2026-11-08, evening

- Ran `simulator/run_collab_checks.bat` on Randolph's Windows PC ([log](run_log_2026-11-08.txt)). Self-test passed on live Open-Meteo data.
- Dead boat (36.85N 75.70W, 2023-05-15): drifted north, then into the Chesapeake Bay mouth; aground near the York River after 8.9 days, 344 km.
- Grid check (Ocean City to SW Ireland, 2024-05-15): 86.3 days at 1 deg, 101.8 days at 0.25 deg. Added a 0.25 deg grid for 30-50N, 80-38W.
- Next: share both results on #50 (draft for Randolph), wait for boat-sim's dead-boat run and drifter check.

## 2026-11-08

- Their side: issue #50 opened with three notes on our simulator (Stokes double count, 1° grid, Europe box), then a follow-up proposing the collaboration protocol (#53) and a split of work. Last boat-sim commit seen: 28add65.
- Our side: applied all three notes (8107f25), moved our launch to the Mid-Atlantic, and replied on #50 accepting the split ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6727663938)). Added the dead-boat scenario and this folder.
- Next: start `docs/Failure_Rates.md` and `docs/Crossing_History.md`; Randolph to run the dead-boat scenario and `gridcheck` on real data.
