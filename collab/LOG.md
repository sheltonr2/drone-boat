# Collaboration log

Newest first. Each check of boat-sim records what was new and what we did.

## 2026-11-11, 04:40

- Posted tonight's comparison on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6786560712)). John had posted a round-up: Rev C and Rev B are in his Boatyard and replays (his yaml load test passed); his Rev C replays grounded twice from the 10 km drop. Accepted his offer to rerun Rev C from ~85 km; gave him our inertias (Ixx 2.90, Iyy 5.00, Izz 2.15, Ixz −0.70).
- **Rev C1 (approved by Randolph):** electronics box raised onto a shelf (bottom z 118), open space reduced to one 3 L sump at the low point, glands on top. Simulator: `hull.wet_electronics_factor` 2 for C1 (GUESS; 6 for B and C), Field Test J added. GM 0.184, self-righting. Drawings D00/D03/D09 regenerated as C1.
- `run_revC1_compare_2023.bat` on Randolph's PC (sim.py + design files only; his default design stays Rev C so tonight's 500-voyage run is unchanged).

## 2026-11-11, 04:00

- **Rev C comparison on 2023 real weather (250 each, refit rates):** Rev C near-coast 38.8% verified (33–45), Rev B near-coast 41.2%, Rev C 100 km 44.8%. Rev C: 0 swamped (Rev B 31), steering losses 19 (62), lost 18.8% (25.6%). But arrivals are level: saved boats die of wet electronics (82 vs 64) or a broken wing (95 vs 76), and Rev C is slower. Next levers: electronics above the flood level, and the wing.
- **Near-coast launch costs more than I said:** 11 US-coast groundings vs 2 from 100 km; ~6 points of verified arrivals (edge of noise). My "about 1%" came from the 100 km run. Docs corrected. Launch rule, escort and recovery aren't modelled.
- Knockdowns by Hs: mean (Hs/3)² = 3.6 at a knockdown → 0.0009 flat ≈ 0.00025 at Hs 3 m.
- 3D viewer added (`viewer-3d/`), noted on #50.

## 2026-11-10, 22:30

- **Rev C approved by Randolph and built** ([Design_RevC.md](../docs/Design_RevC.md)): foam-filled hull behind two bulkheads + sealed battery box (flooding capped at ~3 kg), twin rudders with separate servos, 30 × 26 mm spar on 6806 bearings, bulb D72, YB3 platform P19 and light P20 on the stub; thruster provision and backup D-cell removed. Outer pontoons considered and rejected (stable inverted).
- Simulator: Rev C default (`default_design()`), Rev B preset kept; new keys `rudder.y_offsets`, `hull.flood_limit_kg`; per-rudder servo failures. Rev C 25.2 kg, DWL 98 mm, GM 0.187, max GZ 0.378, self-righting; ~7% slower in the VPP (weight 5%, second rudder 2%).
- Build files regenerated: 20 sheets (new D09), templates T17/T18, 23 STL for 20 parts. Geometry for both sims in `designs/` (boat-sim YAML checked against its Rev B schema and `HazardParams`; not run here).
- Budget correction: Rev C adds ~$260 of parts; my proposal's "~$300 cheaper" was wrong (the thruster was never in the sail-only budget). The YB3 (~$630) also wasn't budgeted.
- John (#50): (Hs/3)² scaling averages ~2.9 at a knockdown on real seas (mean Hs 3.6–5.6 m), so 0.0009 flat ≈ 0.0003 at Hs 3 m in his form. Rev C boat-sim YAML now uses sail 0.0003. He's testing a forecast go/no-go launch rule (#163).
- Posted the full Rev C update on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6779530067)). Live Build Plan and Executive Summary docs updated; replied in the Build Plan's thruster thread (decided: sail-only).
- `run_revC_compare_2023.bat` copied to Randolph's PC: Rev C near-coast, Rev B near-coast, Rev C 100 km (250 each, 2023). Tonight's 500-voyage run (`run_bulk.bat`) now uses Rev C and the near-coast launch (scenario file updated; the old 100 km scenario is `collab/bulk_mc_100km.json`).

## 2026-11-10, 20:30

- **Decision (Randolph): launch near the coast, keeping the boat trip as short as practicable.** Planned point about 10 km (5.5 nm) east of Ocean City Inlet, 38.32°N 74.97°W, from a small boat. Closer is not practicable (inlet currents and traffic, surf). Launch_Plan, Route_MidAtlantic and Executive_Summary updated.
- Mitigations written into the launch plan: launch only on a forecast with ≥72 h of westerly-component wind and no easterly spell; escort for the first 2–3 h; recover and relaunch on early failure during the first week (cheap close to shore, and the backup tracker finds a beached boat).
- Posted the real-weather results, the refit and the launch decision on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6778201353)). Live Executive Summary doc updated to the near-coast launch.
- `run_launch_compare_2023.bat`: 250 voyages from the near-coast point and 250 from 100 km on 2023 bulk data with the refitted rates, same seeds, to put a number on the trade-off.

## 2026-11-10, 20:10

- First real-weather Monte Carlo done (250 voyages, 2023, 100 km drop, YB3 fitted, all cores, 54 min): **34% verified arrivals (28–40)**: 26% reporting plus 8% logged by the tracker. May launches 40%, June 21%. Median crossing 123 days. 10.8% still at sea when the 2023 data ran out.
- Real seas: 3.5 knockdowns/day (522 per voyage). Wing broke in 140 of 250 voyages (hazard 0.0084/day vs target 0.0024). Leaks started at 0.0048/day vs glider 0.0026 (Hs factor ~1.9). **Refit**: knockdown_damage planning 0.003 → 0.0009, historical 0.006 → 0.0017; leak base 0.0025 → 0.00135 (planning and historical). Original set unchanged. Knockdowns now logged by Hs for a severity fit (boat-sim's (Hs/3)² form).
- Only 2 of 250 went aground near the US coast, so the drop point is worth ~1%; launch date matters far more.
- Updated code copied to Randolph's PC before tonight's 500-voyage 2023–2024 run, which will test the refit.

## 2026-11-10, 16:40

- Dead-boat drift tests re-run on the bulk data (ERA5 + SMOC + MFWAM) with the leeway model: 16 drop dates (1 May–15 June 2023) × 4 points × leeway 2/3.3/5%. Aground within 30 days at 3.3%: 25 km 16/16, 50 km 13/16, 100 km 8/16 (7 on the NC Outer Banks), 150 km 5/16. This overturns the Nov 8 "100 km is safe" result, which came from the old cross-wind drift model. Proposed: move the drop to the shelf edge (150 km), pending a 2024 run (`run_drift_bulk_2024.bat`, after tonight's download) and the 2023 bulk Monte Carlo (running).
- In 2023 the drop date mattered more than the distance: from 100 km, every drop 7–28 May grounded and every drop 31 May–15 June stayed at sea. One year only.
- Posted the drift results on #50 at Randolph's request ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6773239793)), including a note that John's Chesapeake test point is on the inner shelf.
- `drift_tests.py` now refuses to run if May–July of a requested year isn't downloaded, names its output by year, and no longer prints "nan".

## 2026-11-10, 15:50

- Bulk download log (sanitized: `run_log_bulk_2026-11-10.txt`): ERA5 for all of May–Nov 2023 plus May–Jul 2024 is stored, at about 2.5–3.3 h per month. 2024-08 was in progress at 10:43 local. The last four months should finish around 10 pm tonight (Nov 10, local); `run_bulk.bat` then runs bulkcheck and the 500-run Monte Carlo on its own.
- The 2023 runs (`run_drift_bulk.bat`, `run_bulk_mc_2023.bat`) can start now, alongside the download.

## 2026-11-10, 15:30

- Backup tracker now modelled in our simulator and fitted by default (`design["backup_tracker"]`, `failures["backup_tracker"]` at boat-sim's 0.0007/day). A dead main box with a working tracker means the boat drifts on at leeway, still tracked. New outcomes `arrived_tracked` (counts as success) and `arrived_adrift` (doesn't).
- 200 runs from the 100 km drop, synthetic weather: verified arrivals 40.5% → 54.5%; position known at the end 40.5% → 65.5%. The no-tracker batch reproduces the earlier 40.5% exactly. Leaks are now the largest cause of loss (50 of 200). Details in docs/Backup_Tracker.md.
- Still waiting on the ERA5 2023 download before the drift and bulk Monte Carlo runs.
- Posted the update on #50 with Randolph's approval ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6770219785)).

## 2026-11-10, 13:44 (scheduled check)

- New on #50: boat-sim confirmed their Rev B replays already used our 14-day shakedown (`burn_in_days`; early-life multiplier 1.41 at launch, never 4×). The early box losses were bad luck (about 1 in 180), not a missing burn-in. My suggestion on Nov 9 was wrong.
- They added the YB3 backup tracker to their Rev B model (#153, #154) and re-ran the replays (#155): still 0 of 6 arrivals, but four boats are afloat and reporting at day 150 instead of lost. The wing breaks within 18 days in 4 of 6 runs.
- Their GUESS values: YB3 failure 0.0007/day, a report every 6 h, rudderless reach behaviour, heeling arm 0.9 m, lateral drag area 0.19 m², and knockdown damage scaled by (Hs/3)².
- Our side: we accept the 0.0007/day tracker rate. A backup-tracker option in our simulator (a dead main box means "drifting, tracked", not lost) is next. Severity-scaled knockdown damage waits for the 2023 bulk Monte Carlo knockdown counts. Posted with Randolph's approval ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6769047482)): corrected the burn-in claim, accepted the 0.0007/day tracker rate, said the knockdown re-tune follows the 2023 bulk run (ERA5 download still running).

## 2026-11-09, 21:40

- New on #50: boat-sim modelled Rev B themselves for their voyage replays (#141, configs/randolph_rev_b.yaml). On ERA5, April–June 2020, it made 0 of 6 crossings. Speed matched ours (~0.9 kn made good). Losses came from the single electronics box (4 of 6, days 4–17) and from knockdowns: real ERA5 seas give hundreds per voyage, against 17–86 on our synthetic weather, so 0.003 per knockdown loses the wing in half the runs.
- Posted ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6757352322)): the backup tracker and 14-day shakedown in our plan (asked them to check `burn_in_days`); we will re-tune `knockdown_damage` on the bulk real-weather Monte Carlo so daily rig loss matches the record, probably scaled by breaking severity; spar going to 30–32 mm; status; and Randolph's new build rule (no union labor; ours only).
- To do: re-tune knockdown damage against real-sea knockdown counts (bulk MC, 2023).

## 2026-11-09, 17:45 (scheduled check)

- New on #50: Theo has put Rev B's GZ curve and inertia into boat-sim's 3D view (#136, credited). Rev B's calm-water roll period comes out at 1.66 s, and it rolls about 4° RMS (13° worst) in a beam gale; these are display-only figures. Live pages: jcolter11374.github.io/boat-sim. boat-sim also moved its default drop to 100 km out (#128).
- #90: boat-sim checked its dead-boat drift against our 3.3%: theirs is 3.86% of U10, straight downwind (beam-on kayak with a dome). They suggest a 3%/5% windage sensitivity before choosing a drop. We adopted the same idea: drift_tests.py `--leeway 0.02,0.033,0.05`, and run_drift_bulk.bat now runs all three.
- No questions for us; no reply needed until our drift re-run results are in.

## 2026-11-09, 17:00

- Posted our reply on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6751168056)): wear-out k = 1 by default, SMOC/Stokes noted, wind ratios credited, hurricane frequency results, Rev B GZ curve for Theo.
- Wear-out is now an off-by-default option in failures.py (`wear_out`, boat-sim #118 parameters).
- **Dead-boat drift fixed.** The VPP's feathered state held the boat on its heading, so a dead boat reached across the wind at 4–6% of wind speed, 70° off downwind. The new leeway model drifts at 3.3% of U10, ±14° of downwind (windage balance; Sunfish 2.1% and skiff 4.0% in Breivik et al. 2010). Synthetic Monte Carlo odds barely change (40.5% vs 40.0%, 200 runs), but the drop-point drift tests need re-running: `run_next_checks.bat` (Open-Meteo) and the new `run_drift_bulk.bat` (2023 bulk data, a drop every 3 days at 25/50/100/150 km).
- New docs: Launch_Plan.md (1–20 May window, charter, Coast Guard, fishery and Irish notices with drafts, labels, light), Backup_Tracker.md (YB3 recommended), Storm_Loads.md (the 25 mm spar is marginal in a knockdown and fails under an 8 m/s breaking crest; upgrade to 30–32 mm and add a proof test).

## 2026-11-09, 16:30

- New on #50: boat-sim delivered #116 (SMOC vs GLORYS on real drifters: neither is measurably better in the eddy field; don't add Stokes drift on top of SMOC's total current), #117 (ERA5/best-track wind ratios: TS 0.70, C1 0.66, C2 0.59, C3 0.53, C4 0.42) and #118 (wear-out: the record can't tell it apart from a steady rate; Weibull k = 1.41, 95% 0.75–2.24, p = 0.25; use k = 1 by default). Theo asked for Rev B's GZ curve and roll inertia for their 3D view.
- Done: `docs/data/revB_gz_curve.csv` (5° steps, inertia in the header). Hurricane storm-frequency model `storms.py` + `stormcheck`, using HURDAT2 1991–2025 analog seasons with a season-bootstrap interval ([Hurricane_Risk.md](../docs/Hurricane_Risk.md)): TS-or-worse within 200 km is 0.1% for April, 5% May, 17% June, 20% July launches. Monte Carlo tracks now carry the time. The default design label now says Rev B (the geometry already was).
- Synthetic Monte Carlo, 200 runs from the 100 km drop, planning rates: 40% (95% CI 33.5–46.9). The earlier 100-run 30% was noise.

## 2026-11-09, 15:30

- The CDS token fix worked: ERA5 2023-05 and 2023-06 are stored. Each month takes about 3 hours, mostly CDS queue time, so the 12 remaining months take about 35 hours more (done around Wednesday morning). 2023 should be complete around 3–4 am Tuesday.
- New `run_bulk_mc_2023.bat`: a 250-voyage Monte Carlo on 2023 alone, which can run while 2024 keeps downloading. A bulk Monte Carlo now refuses to start unless the launch months plus the next five are all on disk, so voyages aren't cut short by the end of the data.

## 2026-11-09, 07:20

- New on #50 overnight: boat-sim is adopting our failure table (#89) and testing drop distance from their own launch point (#90). Their project owner confirmed extra people and free GitHub computing, nothing paid. They offered three jobs: SMOC scored on their 20 drifters, the hurricane wind-ratio CSV, and a wear-out term. They also pointed out ERA5 waves (swh, pp1d, mwd) for years before Nov 2022.
- Posted ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6739897871)): we accepted all three offers and kept storm frequency, the #89 review and the bulk Monte Carlo for ourselves, plus a status update on the bulk data.

## 2026-11-09, morning

- First bulk run ([log](run_log_bulk_2026-11-09.txt)): all 28 Copernicus Marine source-months downloaded and converted (SMOC ~2.2 GB and MFWAM ~0.95 GB a month, about 17 and 9 minutes each, 31 GB stored). Every ERA5 request got HTTP 400 from CDS, including plain GET calls the browser makes without trouble. The ERA5 licence shows "Accepted" on the dataset page.
- The downloader had retried those 400s about 40 times. CDS's October notice warns that repeated invalid requests can get an account disabled, so it now stops at the first 4xx and prints the server's reason. The Monte Carlo now refuses to start when bulk months are missing; the first run logged 500 empty "errors".
- cdscheck found the cause: the saved token was 1 character long. Windows' hidden-input prompt (getpass) doesn't take Ctrl+V; it stores a control character, which gave CDS a malformed header ("Invalid HTTP request received"). New `save_cds_token.bat` reads the token from the clipboard, checks its shape, saves it without showing it, then runs cdscheck.
- New `cds_check.bat` / `cli cdscheck`: versions, .cdsapirc shape (never the token), two plain GETs with the token, and one tiny request, with server responses printed.

## 2026-11-08, 22:45

- Randolph has free accounts with ECMWF (CDS) and Copernicus Marine. New `bulk` data provider: whole months of ERA5 (0.25°, hourly), SMOC currents (1/12°, hourly) and MFWAM waves (1/12°, 3-hourly) for 26–60°N, 82°W–0°, stored as memory-mapped float16 arrays. It uses the same data Open-Meteo serves, but the currents come at full resolution, with no daily quota, and runs use all cores.
- `setup_bulk_data.bat` (installs the tools, Copernicus Marine login, CDS token) and `run_bulk.bat` (download May–Nov 2023/2024, compare with the Open-Meteo cache, 500-voyage Monte Carlo).
- The CDS asks for sequential requests (Oct 2026 notice), so ERA5 months go one at a time. The MFWAM archive is rolling (now from Nov 2022), so earlier years need another wave source.
- Tested offline on synthetic netCDF files: conversion, interpolation (land corners, wave direction across north, month boundaries) and a voyage plus Monte Carlo on memory-mapped data (~0.1 ms per weather sample). Not yet run against the real services, which can't be reached from here.

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
