# Collaboration log

Newest first. Each check of boat-sim records what was new and what we did.

## 2026-11-27, 19:15 UTC (14:15 local): Rev F drawn (proposed)

- Randolph asked what a daily photo would take, then "Draw up the revision". Rev F = Rev E3 + RockBLOCK Plus 9704 (Iridium IMT) in the same bowl + a camera pod on the stern post (P28, P29). docs/Design_RevF.md, docs/Revisions.md.
- Drawings (D00, D01, D07, D23, D24, D30), BOM (+$127, $5,041), print guide, 3D viewer (Pages now shows Rev F), exports. Mass 28.7 kg.
- Simulator: optional IMT billing and daily-photo energy (`comms.imt`, `comms.photo_per_day`, `photo_bytes`, `power.photo_session_j`), off by default; regression bit-identical. designs/revF_design.json. 60-day check: same track and battery, airtime $83 vs $77.
- Not adopted: the plan and the build stay on Rev E3 until Randolph decides.

## 2026-11-27, 13:50 UTC (08:50 local): run 043b running

- Randolph: "Go". Run 043b (collab/runs_043b) started at 08:43, alongside 041; about 9 h, 15 runs, v2 coasts, Rev E3, 4 years:
  - Approaches about 60 and 90 km south of Scilly, with the hold 30 km S of the Lizard (paired with 043a B).
  - Holding upwind of the pickup points, 14-day station-keeping: Norman offing E20, E40 and ESE20; Anegada W N15 and N30; Cornwall hold SW20 and W20.
  - Mindelo launch windows (15 Nov-10 Dec, 11 Dec-10 Jan, 11 Jan-5 Feb) to the Norman offing and Anegada W.
- Bug avoided: `--years` names the year a window starts, so the January window uses 2022-2025.

## 2026-11-27, 13:35 UTC (08:35 local): run 043a analysed

- Nothing new on #50 or by email.
- Queue: 043a ran 21:18-06:42, all 17 runs completed. 041: 3 of 15 ERA5 months done in about 15 h (May 2025 13 min, Jun 4.6 h, Jul 5.7 h; CDS connection errors, retried). Marine May-Nov 2025 is complete. About 2.5 days to go at this rate.
- **043a results** (collab/runs_043a/analysis.py and .json), v2 against the v1 twins:
  - Eastbound: B 81.1% (+0.3), A 79.5% (+0.1), the old plan 74.3% (-1.5). B vs the old plan +6.8 (+3.8 to +9.7); B vs A +1.6 (-0.4 to +3.6).
  - B launch window: April 79.6% (storm 1.8%); 21 May-15 June 82.8% (storm 12.7%, vs 4.4% for 1-20 May); 70 km drop 81.9% (+0.8).
  - Cornwall holds unchanged: 30 km S of the Lizard 0.4% aground; Lizard offing 14.2% (12.8%).
  - Mindelo -> Norman offing 88.3% (+0.3); pickup 3 days after arrival 84%. Mindelo -> Anegada W 82.3%; pickup 7 days after arrival 75%. El Hierro -> Norman offing 81.7% (123 days median).
  - BVI holds unchanged.
- **Conclusion:** the depth data confirms every decision. Docs updated (Launch_Plan and East_West_Study) and copied to the PC.

## 2026-11-27, 02:25 UTC (21:25 local): run 043a queued and running

- Randolph: "Are there any sims running? Can we put sims in to run for the next 10+ hours?" Only 041 (the download, network-bound) was running.
- **043a** (collab/runs_043a): the decided plans on the v2 coasts with the four years already on the PC, 17 runs, about 11 hours, one queue job (run_043a_v2_4yr.bat calls both parts so the queue hands over only once). It started at 21:18 local, alongside 041.
  - Part 1, eastbound (1,000 voyages each): B, A and the old plan; B in April; B from 21 May to 15 June; B from the 70 km drop. Then Cornwall holds at both points (station-keeping and drift, 500 each).
  - Part 2, east-west: Mindelo to the Norman offing and to Anegada W; El Hierro via 20N 28W to the Norman offing (1,000 each, with a storm check). Then BVI holds at both points.
  - Every run pairs with its v1 twin (036-042), so it measures the depth data's effect.

## 2026-11-27, 02:20 UTC (21:15 local): Cornwall arrival decided: option B

- Randolph: "B". The approach moves 40-45 km south of Scilly (49.35N 7.20W, 49.50N 6.40W) and the hold moves to 30 km south of the Lizard (49.70N 5.20W); scenario collab/runs_042/plan_south_deep.json. Option A (the same approach to the Lizard offing) is the fallback if the recovery boat can't go 50 km out. Launch_Plan updated (decision table and the accurate-coastline section) and copied to the PC.

## 2026-11-27, 02:20 UTC (21:20 local): #50 results posted; BVI pickup point decided

- Randolph: "Make the #50 post." Posted ([comment 7207925031](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-7207925031); text in collab/post_2026-11-27_results.md, with one line added for his BVI decision). The API shows exactly one new comment.
- Randolph on the BVI: "Let's plan on norman but always run anegada too, not sure which yet." Read as the Norman offing, 18 km south of Norman (the point recommended over the old one 4 km south). East_West_Study updated: the plan is now Norman offing (18.17N 64.58W), with Anegada W (18.72N 64.49W) run alongside it in every study.
- Cornwall (approach and hold): recommendation sent, decision still open.

## 2026-11-27, 02:30 UTC (21:30 local): 042B, v2 coasts, docs, Liz email, #50 draft

- Nothing new on #50 or by email.
- **042B** (approach south of Scilly, hold 30 km south of the Lizard): 80.8% (78.4-83.2). Paired with 039: A +3.6 (+0.9 to +6.3), B +5.0 (+2.4 to +7.6), B-A +1.4 (-0.7 to +3.5). Arrival x afloat after 3 days: 039 73%, A 76%, B 78%.
- **040c:** the UKHO points re-fetched (2,179 off Cornwall). The layer has no attributes, so only points where EMODnet's seabed is shallower than 5 m count (300 points, 7 areas).
- **v2 coasts built** (detail_*_v2.json): EMODnet patches under 2 m, UKHO hazards, wreck filter fixed. They load in 0.2 s; 20,000 land checks take 0.4 s. v1 is kept as run.
- **Docs:** Launch_Plan.md has a new section on the accurate coastline (037/039/042), with the arrival row marked "under review". East_West_Study.md has section 13 on BVI pickup points (036/038), with the holding point marked "under review". No decisions were changed. Both decisions are with Randolph. Copied to the PC.
- Sent the executive summary email to a friend of Randolph's, at his request.
- #50 results post drafted (collab/post_2026-11-27_results.md); it waits for Randolph's approval.
- Queue: 042 ended 20:40, 040c ran 20:41-20:41, and 041 (2025 weather) continues. The queue race fix and the five-year re-runs wait until 041 ends.

## 2026-11-27, 01:10 UTC (20:10 local): 3D viewer published; whole-boat STL

- Randolph asked whether the 3D models could be shared, then chose GitHub Pages with the viewer only ("Lets do the viewer"). An orphan `gh-pages` branch now holds only build-files/viewer/index.html and model.json, plus .nojekyll and a README. GitHub enabled Pages from that branch automatically: https://sheltonr2.github.io/drone-boat/ loads with all parts and no errors (checked in the browser).
- Added build-files/export/drone_boat_revE3_exterior.stl (9 MB, snapped to 1 mm, by build-files/source/export_stl.py) so GitHub's STL view shows the whole boat; checked that it renders.
- An executive summary email to a friend of Randolph's goes out with the 21:05 update, at his request, with the public links (viewer, STLs, Bluewater, maps, repo).

## 2026-11-27, 00:45 UTC (19:45 local): run 038 in, run 042A in, depth data in

- Nothing new on #50 or by email.
- **038, Mindelo -> each BVI point** (1000 voyages, 4 winters): every point arrives 79-88% of the time, with no groundings on the way.
  - P(pickup 3 days after arrival) = arrival x afloat at day 3: Norman offing 84%, St Croix N 80%, Anegada W 79%, Ginger SE 72%, Anegada N 72%, Jost Van Dyke N 66%, Norman (current plan) 48%.
  - At 7 days: Anegada W 75%, St Croix N 70%, Norman offing 68%, Norman 26%.
- **042A, approach 40-45 km south of Scilly to the Lizard offing:** 79.4% (76.9-81.8), against 75.8% for 039. Groundings fall from 6.4% to 2.7%: Scilly 44 -> 16, Lizard 11 -> 1. 042B (hold 30 km south of the Lizard) is still running.
- **040, depth data:**
  - EMODnet DTM grids for Cornwall and the Caribbean (none for Hatteras). The v2 builder turns the patches shallower than 2 m into outlines; they hug the OSM coast with a 100-300 m margin and fill the shallow inner waters of Scilly.
  - The UKHO open portal has wrecks and obstructions in the UK EEZ only (2,179 points and 11 areas off Cornwall; nothing for the BVI) and no open survey footprints.
  - Bug: the area layer overwrote the points file (same truncated name). Fixed; 040c re-fetches the points.
- **Queue race:** at 18:27 the queue window and the scheduled task both started 042. The duplicate exited and deleted running.lock, so the task went on to 040 and then 041, which now runs in parallel with 042 (harmless). The window does not refresh window.lock during a run. Fix after 041 ends (the .bat files cannot be edited while running), and queue the five-year re-runs only after 041 is done.

## 2026-11-26, 20:05 UTC (15:05 local): check; runs 036, 037 and 039 analysed

- Nothing new on #50 or by email. boat-sim commits through da48acb.
- Queue: 036 (finished 11:25), 039 (12:26) and 037 (12:53) are done. 038 started at 12:54 and has finished 2 of its 7 candidates. 040 and 041 are waiting.
- **036, BVI holding** (14 days station-keeping within 1 km; collab/runs_036/hold_analysis_036_037.py):
  - The current plan point, 4 km south of Norman Island, goes aground in 84.6% of holds (median 2.9 days), mostly on Norman/Peter and St John. The trades and the westward current set the boat downwind.
  - Anegada W: 7.2% aground (r90 42 km). St Croix N: 24.2%. Anegada N: 23.6%. Norman offing: 36.0%. Ginger SE: 54.0%. Jost Van Dyke N: 66.4%.
  - Run 038 so far: Mindelo -> Norman 88.2%, -> Norman offing 88.0%. A pickup 3 days after arrival comes to 48% at Norman and 84% at the Norman offing.
- **037, Cornwall holding:**
  - The Lizard offing goes aground in 12.8% of holds on the detailed coast (run 035 on Natural Earth: 3.0%).
  - 30 km south of the Lizard: 0.4% (r90 29 km). Scilly-Lizard gap: 20.0%. Mount's Bay: 55.0%.
- **039, the eastbound plan on detailed coasts:** 75.8% (73.0-78.4), against 81.6% for run 034. The difference:
  - 39 of 1,000 voyages wreck on the Isles of Scilly. The 49.6N 7.2W -> 49.7N 6.4W leg passes about 20 km south of them, and boats set north hit the Western Rocks. Natural Earth had no Scilly.
  - 11 go aground on Lizard Point during the run in.
  - 5 hit a *non-dangerous* wreck 10 km from the launch point off Hatteras. Bug: the v1 hazard filter matched "dangerous" inside "non-dangerous" (12 such wrecks off Hatteras, 3 in the VI). Fixed in make_detail_coast.py for v2; the v1 files are left as used.
- **042 prepared** (collab/runs_042): the same plan with the approach 40-45 km south of Scilly, (A) to the Lizard offing and (B) to a hold 30 km south of the Lizard, paired with 039. Randolph OK'd it at 15:40 local ("Queue it"): queued as 040b_approach_variants.run, after 040 and before 041.
- Draft map: docs/figures/pickup_map.png (docs/data/pickup_map.py, from collab/runs_036/pickup_analysis.py). It is completed when 038 finishes.
- No plan decisions changed.

## 2026-11-26, 15:15 UTC (10:15 local): depth data and 2025 weather queued

- Randolph: "Add the UK and EMODnet depth data and rerun with the 2025 weather." He will handle the recovery arrangements himself.
- Queued after 038: **040** `run_040_depth_data.bat` (docs/data/coast/fetch_depth_data.py). It fetches the EMODnet DTM (~115 m) for the three coast boxes and UKHO open data (catalogue and service lists, Wrecks and Obstructions in the boxes, and the footprints of bathymetry surveys there), about minutes. **041** `run_041_weather_2025.bat`: eastbound May-Nov 2025, then east-west Nov 2025-Jun 2026, about 40 GB and 2-4 days.
- Next: build v2 detail coasts (OSM + ENC + EMODnet shoals + UKHO hazards), then queue five-year re-runs of 036-039 (2021-2025 seasons; BVI holds Feb-Apr 2022-2026) once 041 is done. 036-039 keep the v1 coasts, so the depth data's effect can be compared.

## 2026-11-26, 14:55 UTC (09:55 local): accurate coastlines; runs 036-039 queued; Thanksgiving update posted

- Coastline: the simulator's Natural Earth 1:50m land mask missed most of the BVI cays and the Cornwall rocks. Added `detail_coast` (off by default, regression identical): OSM coastline plus NOAA ENC shoals, rocks and wrecks for the Virgin Islands and Hatteras, and OSM for Cornwall. Every step is checked every 60 m so the boat can't jump a cay. Data and sources are in docs/data/coast/README.md.
- Chart sources checked: NOAA ENC covers the USVI at harbour scale but the BVI only to 64.42W. There are no free Cornwall charts; UKHO's ADMIRALTY Marine Data Portal and EMODnet bathymetry are possible additions. GEBCO is too coarse.
- Queued on the PC (036 started 09:51 local): 036 BVI hold, 7 pickup points (Norman, Norman offing, Ginger SE, Jost Van Dyke N, Anegada W and N, St Croix N); 037 Cornwall hold, 4 points; 039 eastbound plan on the detailed coasts; 038 Mindelo to each BVI point. About 9 h.
- Posted the update and Thanksgiving wishes on #50 ([post](post_2026-11-26_update.md)).
- No plan decisions changed.

## 2026-11-26, 14:10 UTC (09:10 local): 032 download done; runs 033-035 finished and analysed

- Nothing new on #50 or by email.
- 032 finished on 26 Nov at 05:53 local: all 16 ERA5 months for the 2021-22 and 2022-23 winters, with 0 source-months missing and 128 GB free. Then 035 (6:00), 034 (7:00) and 033 (8:16) ran and finished, and the queue is empty.
- 035, holding with a 1 km deadband: it barely helps. At the Lizard offing, 3.0% aground (3.4% with 5 km) and a median furthest distance of 29 km (30). At Mount's Bay, 34.0% (38.2%). The boat can't hold against the stream, so the advice is to plan recovery for the arrival, not for a long hold. Added to docs/Launch_Plan.md.
- 034, Rev E3 on the final plan: 81.6% (79.1-83.9) vs Rev E1 81.0%, paired; median 121 days for both. Notes in docs/Launch_Plan.md and docs/DFM_Review.md section 4.
- 033, four winters for the BVI backup: Mindelo 87.8% (85.7-89.8), El Hierro 81.9%, Gran Canaria 78.4%; the ranking holds and all gaps are now outside the noise. New section 12 in docs/East_West_Study.md; docs/data/ew_033_analysis.py.
- No decisions changed. Results are in results/2026-11-26_*.

## 2026-11-26, 08:05 UTC (03:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: 15 of 16 ERA5 months (May 2023 took 5.8 h), and Jun 2023, the last, is requested.

## 2026-11-26, 02:05 UTC (21:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: 14 of 16 ERA5 months (Apr 2023 took 6.9 h), and May 2023 is requested.

## 2026-11-25, 20:05 UTC (15:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: Mar 2023 arrived after 9.4 h (CDS showed "degraded", with about 12,000 queued requests at 14:25 UTC; Randolph chose to keep the order), so 13 of 16 ERA5 months are in and Apr 2023 is requested. Three to go.

## 2026-11-25, 14:05 UTC (09:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: still 12 of 16 ERA5 months; Mar 2023 has been in the CDS queue for several hours, with DNS blips retried and the log updating. The queue is unchanged.

## 2026-11-25, 08:05 UTC (03:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: 12 of 16 ERA5 months (Feb 2023 took 5.9 h), and Mar 2023 is requested. Four months to go, roughly a day at this rate. The queue is unchanged.

## 2026-11-25, 02:05 UTC (21:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: 11 of 16 ERA5 months (Jan 2023 took 4.5 h), and Feb 2023 is requested; DNS blips are being retried. 032c/032d/033 are still queued.

## 2026-11-24, 20:05 UTC (15:05 local): 6-hourly check
- Nothing new on #50 since our two posts (read through the PC browser) and no email. 032: 10 of 16 ERA5 months stored (Dec 2022 done at 14:33 local). A DNS failure at 14:42 local is being retried every 2 min, and the queue window is alive. 034 and 035 haven't been run by hand, so they're queued as 032c/032d.

## 2026-11-24, 19:20 UTC (14:20 local): runs 034 and 035 queued

- Randolph: "do both". 034 is Rev E3 (20 W) on the final plan, paired with 026 (1000 voyages, about 1 h). 035 is the holding study with a 1 km station deadband (new scenario key station_radius_km, off by default; regression identical), paired with 028's station runs (about 20 min). Both are queued as 032c (035) and 032d (034), so they run after the 032 download and before 033. Randolph can double-click them to run them now, alongside the download.

## 2026-11-24, 19:05 UTC (14:05 local): run 028 analysed; 032 download resumed

- 028 (holding) finished at 13:36 local. Lizard offing: 3.4% aground in 14 days of holding (Mount's Bay mouth 38.2%); dead boats ground from 1.4 days (10th percentile; Mount's Bay 0.5). The model's station mode is a 5 km feather-and-return, so the distances are an upper bound. Section written in docs/Launch_Plan.md; collab/runs_026/hold_analysis.py; results/2026-11-24_hold028_*.
- 032b resumed at 13:37: 8 of 16 ERA5 months were already stored; Nov 2022 came at once (the CDS job had finished during the outage), and Dec 2022 is requested. 033 waits behind it.

## 2026-11-24, 18:40 UTC (13:40 local): 3D model and stability data posted on #50; queue running again

- The PC restarted again at about 13:25 local and killed the first 028 retry. Put another unlock.run and 028d_holding_after_restart.run in the queue; Randolph opened the queue window. 028 started at 13:28 and was on its last part (drift_mounts) at 13:34. 032b (download resume) and 033 follow.
- Missed on #50: the 20:05 and 02:05 checks read #50 through WebFetch of the API, which showed nothing new, but two comments had come in. **23 Nov 20:49 UTC (7113610456):** they agree the 19/46 re-score is within the noise and call the slow-median question answered. They want the 3D model as one .glb with separate named parts and the bow direction noted, "no hurry", and say nothing else is open. **24 Nov 16:35 UTC (7137912894):** Rev E1 is live in Bluewater (#658, #659), drawn as Rev C5 until our glTF arrives. They asked for a revE1_gz_curve.csv and inertias if we have them. Its Boatyard test sails to Portugal, not Cornwall. Future checks: read #50 through the browser on the PC, not WebFetch.
- Made and pushed (Randolph: "push an update to #50 ... if we dont [have the files], let's make them"):
  - build-files/export: Rev E3 as .glb (all parts, and exterior only) and OBJ+MTL; source/export_model.py.
  - designs/boat-sim/randolph_rev_e3.yaml.
  - docs/data/revE1_gz_curve.csv and revE3_gz_curve.csv, designs/revE1_geometry.json and revE3_geometry.json (inertia), from docs/data/stability_export.py.
- Posted on #50: 18:32 UTC (7140778631), the 3D model, Rev E3, the 2028 launch and the runs restarting (collab/post_2026-11-24_update.md); 18:34 UTC (7140821736), the GZ curve and inertia and a note that the Boatyard test goes to Portugal (collab/post_2026-11-24_stability.md). The API shows exactly these two new comments from us.

## 2026-11-24, 18:10 UTC (13:10 local): PC back; queue restarted
- What the outage left: run 032 stopped on 23 Nov at 08:54 local with 8 of 16 ERA5 months stored (all Copernicus Marine months were done earlier); 028b had just started and left a stale running.lock.
- With Randolph's go-ahead ("how can I get everything restarted"): put unlock.run, 028c_holding_after_outage.run (run_028_holding.bat) and 032b_ew_download_resume.run (run_032, which skips stored months) in the queue; 033 was still queued. Order: 028 holding, then the 032 download, then 033.
- Copied the Rev E3 files (0b999b9) and the 2028 docs (c59ab90) to the PC.

## 2026-11-24, 14:05 UTC (09:05 local): 6-hourly check
- Nothing new on #50 or by email. PC still down (part due today).

## 2026-11-24, 08:05 UTC (03:05 local): 6-hourly check
- Nothing new on #50 or by email. PC still down.

## 2026-11-24, 02:05 UTC (21:05 local): 6-hourly check
- Nothing new on #50 or by email. PC still down.

## 2026-11-23, 20:05 UTC (15:05 local): 6-hourly check
- Nothing new on #50 (read via the public API; ours of 22 Nov 13:59 is still the latest) or by email. PC still down awaiting a part (due 24 Nov), so the queue wasn't checked.

## 2026-11-23, 14:30 UTC (09:30 local): launch moved to May 2028; John told about the PC

- Randolph: "Plan for a 2028 launch." Launch window now 1–20 May 2028 (usable 1 Apr–15 Jun); the place, holding point and route are unchanged. Launch_Plan timeline rewritten around the Build Plan's five phases (bench and lake prototype to June 2027, ocean boat build June–September 2027, coastal trials October 2027 and March 2028); Build_Plan and Executive_Summary updated; notice drafts now say May 2028. The procurement Sheet was re-baselined: bench electronics by 7 Dec 2026, prototype rig, spar and panels in January, ocean composites in May 2027, YB3 in August 2027.
- Emailed John (Randolph chose email because #50 needs the PC's browser): Randolph's PC is down awaiting a part due tomorrow, so runs and downloads are delayed. The 2028 change wasn't mentioned.

## 2026-11-23, 14:05 UTC (09:05 local): 6-hourly check
- No email from John. PC off the bridge, so neither #50 (read through its browser) nor the queue could be checked; the fallback read of #50 needed approval and got no answer.

## 2026-11-23, 14:30 UTC (09:30 local): Rev E3 and the procurement schedule

- Randolph: "Go with your suggestion on 3 and let's get things going." DFM items 1-2 settled as Rev E3 (commit 0b999b9): stock solar, 2 x PV Logic STPVF010 10 W (380 x 250 mm) = 20 W, because no stock 15 W panel fits the 280 mm bays and run 027 showed 20 W costs nothing measurable; spar from stock, a 30 x 26 outer tube sleeved with an R&G 26 x 22 tube. BOM $4,914. Drawings, BOM, README, viewer and designs/revE3_design.json updated.
- Procurement schedule made as a private Sheet (link in chat), working back from 1 May 2027: composites by 25 Nov, all long-lead and overseas items (spar tubes, panels, YB3, SER-2000, servos, RockBLOCK, electronics) by 30 Nov, mechanical by 7 Dec, finishing by 4 Jan. Every BOM line is covered once.
- Run 028 (holding) not started: the PC is off the bridge.

## 2026-11-23, 08:05 UTC (03:05 local): 6-hourly check
- Nothing new on #50 or by email. 032: 7 of 16 ERA5 months done (May 2022 took 4.5 h); on June 2022.

## 2026-11-23, 02:05 UTC (21:05 local): 6-hourly check
- Nothing new on #50 or by email. 032 is on ERA5 month 7 of 16 (May 2022, requested 22:50 UTC).

## 2026-11-22, 23:10 UTC (18:10 local): old runs check (superseded by the 6-hourly; not rescheduled)
- 032: 6 of 16 ERA5 months done (April 2022 took 3.7 h). 028b and 033 still queued.

## 2026-11-22, 20:05 UTC (15:05 local): 6-hourly check
- Nothing new on #50 or from John by email. 032 has 5 of 16 ERA5 months (March 2022 took 5.8 h), so it's due about 24-25 Nov. 028b and 033 wait behind it.

## 2026-11-22, 14:00 UTC (09:00 local): reply posted

- Randolph approved the draft ("Send it"). Posted on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-7080209758), text in collab/post_2026-11-22_rescore_reply.md); the API shows exactly one new comment. It says our run 029 also got 19/46 on their dates (0/46 on the straight line), compares the losses, explains the slower crossings, and offers a glTF/OBJ export of the viewer model for Bluewater's Rev E1 if they say which format.

## 2026-11-22, 13:50 UTC (08:50 local): daily check-in

- Thread #50: one new comment from their team (22 Nov 11:05 UTC, issuecomment-7078210631).
  - Rev C5 re-scored with our waypoint: **19 of 46 (41.3%, 95% range 28-56%)**, median 130 days. 6 aground (all on the Maryland/Virginia shore soon after the drop), 11 lost, 9 at sea on 30 Nov. They say it agrees with our 48.0% within the noise, and that the waypoint was the whole difference (straight line: 3/46).
  - They listed the remaining set-up differences: daily launches; any Europe counts, mostly at 11W; ERA5 waves and GLORYS currents; their own waypoint and land rules; slower crossings. Their run is public in boat-sim Actions.
  - Rev E1 yaml merged as configs/randolph_rev_e1.yaml (#658). It isn't pickable in Bluewater yet: it needs a 3D model, and they said our viewer will help.
- Our run 029 had already got the same 19/46 on the same dates (and 0/46 on the straight line). Drafted a reply for Randolph's approval: collab/draft_2026-11-22_reply.md. It compares the two runs and offers a glTF/OBJ export of the viewer model. **Not posted.**
- PC queue: 032 (weather download) has 4 of 16 ERA5 months after 14 h (2.5-3.7 h a month), so it's due about Tuesday 24 Nov. There were DNS hiccups, recovered automatically. 028b and 033 wait behind it.
- Next: 18:07 check on 032/028b; daily check-in Mon 08:47.

## 2026-11-22, 05:00 UTC (00:00 local): results of runs 026, 027, 029, 030, 031

- Queue: 026, 027, 029, 030 and 031 finished between 17:37 and 22:40 local with no errors. 032 (the weather download) has been running since 22:41.
- **028 did not run.** The data check asked for December weather for every 2021-24 season, which a 14-30 day voyage doesn't need. Fixed: `cli.py` now scales the months after the window with max_days (unchanged for voyages of 120 days or more), and the synthetic regression is still identical. Queued again as 028b; it runs after 032, before 033.
- **026 final plan** (1000 voyages, 1-20 May 2021-24, Lizard offing v2):
  - 81.0% success (78.6-83.4), 76.6% reach the hold.
  - By year: 78 / 84 / 79 / 83.
  - Within 1 km: Scilly 5.4%, Manacles 2.2%.
  - Own-year tropical storm within 100 km: 1.0%. After the 30/70 losses: 80.8%.
- **027 DFM** (paired with 025):
  - Solar 30 W and 20 W both +0.0 success. SAFE reached on 9 and 26 of 500 voyages, against 0 at 40 W.
  - Spar 30x26: -2.2 (-3.6 to -1.0), reached -4.4. Voyages with the wing broken in a knockdown went from 10 to 40.
- **029 C5 boat-sim's way** (46 daily launches):
  - Straight line, no waypoint: 0/46 (39 aground: Nova Scotia 13, New England 13, Maryland 10, Newfoundland 3).
  - Our route on the same dates: 19/46 (41.3%).
  - Note: collab/runs_026/c5_029_note.md. Not posted.
- **030 fixes** (paired with 026):
  - Storm winds alone: -0.4 (-1.2 to +0.4); 7% of voyages met a corrected storm, max factor 1.52.
  - Knockdown severity alone: +0.6 (0.0 to +1.4).
  - Both: +0.5 (-0.2 to +1.2).
  - The options stay off by default.
- **031 westbound sea states:**
  - Hs >= 3 m 9% of the time, never 5 m (eastbound: 1.3% at 5 m or more).
  - Fatigue per crossing about the same as eastbound for the fin, post and arm.
  - Tail boom: even the old tube would use 7% of its life.
  - 2.3 M rudder movements.
- Docs:
  - Launch_Plan: 026, and 028 pending.
  - DFM_Review section 6: 027.
  - Hurricane_Risk 21 Nov update: 030.
  - Fatigue_Review and East_West_Study section 11: 031.
  - No decisions changed.

## 2026-11-21, 22:40 UTC (17:40 local): runs 026-033 queued (Randolph: "let's do all 7")

- Simulator options added, all off by default. Synthetic-weather voyages (Rev E1 and C5, three seeds) reproduce bit-for-bit with them off.
  - `storm_wind_correction`: near the year's HURDAT2 storms, ERA5 winds are scaled by 1/ratio (boat-sim #117), fully within 60 km and tapering to none at 250 km, capped at the best-track wind; waves by the square root. Grade D.
  - `knockdown_severity`: wing damage per knockdown x (Hs/3)^2 / 2.5. 2.5 is the mean (Hs/3)^2 at a knockdown on the planned route: 2.63 in run 025, 2.31 in 019a; westbound it's about 1.0.
  - `structure.spar`: the C2 spar table on a C3 boat, for the stock 30 x 26 tube.
  - Scenario `station` (start holding at a point) and `start_times` (one launch a day).
- Queue, in order (estimates from run 025's 30 min per 500 eastbound voyages):
  - 026 final plan on 2021-24, 1000 voyages, 1-20 May (~1 h);
  - 027 solar 30 W, solar 20 W and the 30 x 26 spar, paired with 025 (~1.5 h);
  - 028 holding at both points: 14 days station-keeping and 30 days dead drift, 15 Aug-15 Oct, 2021-24 (~35 min);
  - 029 Rev C5 on boat-sim's 46 daily launches, their straight route and ours (~12 min);
  - 030 model fixes on 026's seeds: both 1000, storms-only 500, severity-only 500 (~2 h);
  - 031 westbound sea states (~15 min);
  - 032 tropical-box weather for winters 2021-22 and 2022-23 (16 months, 1-3 days at CDS);
  - 033 Mindelo, Gran Canaria S and El Hierro S on those winters (~1.5 h).
- Generator: collab/runs_026/make_runs.py. Code 885f63e, copied to the PC.

## 2026-11-21, 22:15 UTC (17:15 local): check-in at Randolph's request; reply posted

- Thread #50: three comments from their team this morning (08:03, 08:04, 08:51 UTC), the first since 13 Nov.
  - An apology for the silence, a reply to each of our seven posts, and our four Bluewater notes fixed (#646: Rev C5 label, D72 bulb and 30 mm spar, hidden-pane frames, sound label). Their traffic grid (`data/traffic/ship_density_v1.nc`, CC BY 4.0) has no fishing effort. They have no storm-damage figure, no shoals in their land map and no trade-wind coverage (their map stops at 25N).
  - John told them to resume shared work. They want a Rev E1 yaml for Bluewater and started the Rev C5 re-score our way (Ocean City drop, SW Ireland, 1 May-15 Jun 2023, season to 30 Nov).
  - First re-score: 3 of 46 arrived, 29 aground, 13 lost, 1 at sea. They called it unfair themselves: a single great circle with no waypoints crossed Nova Scotia and Newfoundland, and 9 boats went back onto the Maryland shore. They asked for our waypoints, waypoint rule and drop point.
- Our side:
  - Wrote [designs/boat-sim/randolph_rev_e1.yaml](../designs/boat-sim/randolph_rev_e1.yaml), from the Rev D file, with a list of what their format leaves out (pump, detent, limp-home, weed manoeuvre).
  - Randolph chose to post on #50 only (no email to John). Posted the reply ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-7069998613), text collab/post_2026-11-21_rescore.md). The API shows exactly one new comment. It gives the 48.0% set-up (drop 38.32N 74.97W; waypoint 42N 48W within 25 km; 15 km land look-ahead; finish 40 km of 51.35N 9.70W or Europe; reporting or tracked arrivals only; 2023 weather to end of Nov; planning rates) and our news (18 Nov decisions, Rev E2 build files, 3D viewer). The email draft collab/email_2026-11-21_john.txt was not sent.
- PC queue: empty, unchanged since 025. No runs started.
- Next: watch for their re-scored number and the Rev E1 boat in Bluewater. Daily check-in Sun 08:47.

## 2026-11-21, 13:50 UTC (08:50 local): daily check-in (incomplete)

- Thread #50: not read. Randolph's PC (and so the built-in browser) was not connected, the GitHub API is not enabled for this cloud session, and a web fetch of the API waited for an approval nobody was there to give. Last known state (20 Nov): our 19 Nov 00:33 UTC post is the latest comment; no reply since 13 Nov 08:13 UTC.
- PC queue: not checked (PC offline). Last known: empty since 025. No runs started.
- Next daily check-in Sun 08:47; it reads anything posted since 19 Nov 00:33 UTC.

## 2026-11-20, 13:50 UTC (08:50 local): daily check-in

- Thread #50: nothing new from their side; our 19 Nov 00:33 UTC follow-up is still the latest comment (no reply since 13 Nov 08:13 UTC). Nothing to draft.
- PC queue: empty; queue_log.txt unchanged since 025 (19 Nov 00:13 local), nothing waiting. No runs started.
- Our side since the last check-in: the DFM pass (Rev E2 drawings, 34 STLs, BOM with links) and a browser 3D viewer of the boat and every printed part (build-files/viewer/). Not posted to their team (not asked).
- Still open: knockdown severity, the storm loss model, the visual pass of Bluewater's sailing screen, the #117 wind correction in the voyage loop.
- Next daily check-in Sat 08:47.

## 2026-11-19, 13:50 UTC (08:50 local): daily check-in

- Thread #50: nothing new from their side; our 19 Nov 00:33 UTC follow-up is the latest comment (no reply since 13 Nov 08:13 UTC).
- PC queue empty since 025 (00:13 local); no study checks pending. The decisions the check-in listed as open were made on 18 Nov (launch window, Lizard offing, Mindelo).
- Candidates for next runs (not queued; Randolph's call): a third and fourth tropical winter (2021-22, 2022-23) for the BVI backup; sea states and fatigue along the westbound tracks (downwind, Christmas trades); station-keeping and dead-boat drift at the Lizard offing; the open model items (knockdown severity, storm losses, #117 wind correction).
- Next daily check-in Fri 08:47.

## 2026-11-19, 05:40 UTC (00:40 local): Scilly approach fix (run 025) analysed

- 025 ran 23:12-00:13 local, no errors. Lizard offing with the new approach (via 49.60N 7.20W, 49.70N 6.40W): reached the hold 76.4% (+2.8, -1.0 to +6.8 vs 023b), within 1 km of Scilly 3.0% (was 12.0%); Seven Stones 1.2%, Wolf Rock 1.4%, the Lizard 1.2%, the Manacles 0.2%. Mount's Bay mouth: 71.8%, Scilly 3.0% (was 15.4%), Wolf Rock 5.6%.
- docs/Launch_Plan.md: the two-waypoint approach is now the plan's approach; Lizard offing remains first choice. docs/data/arrival_analysis.py extended. Docs copied to the PC. Not posted to John's team (not approved).

## 2026-11-19, 04:15 UTC (18 Nov 23:15 local): Randolph's decisions

- Launch window: 1-20 May target, 1 April-15 June usable (adopted).
- Holding point: the Lizard offing (49.85N 5.20W), with the mouth of Mount's Bay (49.97N 5.45W) as the alternative (adopted).
- East-west backup: Mindelo, Cape Verde, launch about 25 Nov-5 Jan for a March BVI arrival; fallback El Hierro or Gran Canaria via 20N 28W (adopted).
- Scilly approach fix approved: run 025 (run_arrival_v2.bat) brings boats in via 49.60N 7.20W and 49.70N 6.40W; both offshore holding points, 500 each. Queued on the PC; analysis check scheduled in about 80 minutes.
- docs/Launch_Plan.md and docs/East_West_Study.md updated with the decisions and copied to the PC.

## 2026-11-19, 00:35 UTC (18 Nov 19:35 local): offshore holding and BVI two-winter runs analysed; follow-up posted

- Queue finished and empty: 023 download 15:35 local (all 15 ERA5 months), 023b 16:38, 024a 17:01, 024b 18:14, 024c 18:39. No errors.
- 023b (docs/data/arrival_analysis.py): reached the hold, Lizard offing 73.6% (+8.8 vs Falmouth Bay), mouth of Mount's Bay 71.0% (+19.8 vs inside the bay); Manacles/Lizard close passes almost gone; still -4 to -6 points vs stopping 40 km out; 12-15% within 1 km of Scilly on the approach. Recommendation (Randolph's call): Lizard offing, Mount's Bay mouth as alternative; move the Bishop Rock waypoint out (not queued).
- 024 (docs/data/ew_024_analysis.py, two winters): Mindelo 86.0% (84.8/87.2), 93 d, 51% March arrivals, March arrivals launched 23 Nov-4 Jan (median 14 Dec); El Hierro south 81.0%; Gran Canaria south 78.0%; Mindelo +8.0 vs Gran Canaria, +5.0 vs El Hierro (paired). May launches 82.6% but 19.6% TS+ / 10.5% hurricane within 200 km. Southern BVI approach: Virgin Gorda <1 km 3%. Recommendation (Randolph's call): Mindelo, launch ~25 Nov-5 Jan.
- Fixed a half-month bucketing bug (day 31 counted separately) in ew_screen_analysis.py and ew_024_analysis.py; 022 doc numbers unaffected except the late-December bucket.
- Thread read first (nothing new from their side). Posted the follow-up promised on 16 Nov ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6995886553), text collab/post_2026-11-18_bvi2.md); API shows exactly one new comment.

## 2026-11-18, 13:50 UTC (08:50 local): daily check-in

- Thread #50: nothing new from their side; our 16 Nov 21:35 UTC BVI post is still the latest comment (no reply since 13 Nov 08:13 UTC).
- Queue: 023 still downloading. ERA5 13 of 15 months stored (2023-11..2024-10, 2025-08); CDS slowed to 160-270 min a month; 202509 requested 12:49 UTC, then 202510. Expected done about 15:30-16:30 local, then 023b and 024a/b/c (~3.5 h), about 19:00.
- Moved the 023b/024 check (analysis + approved follow-up post) from 17:30 to 19:30 local. Next daily check-in Thu 08:47.

## 2026-11-17, 13:50 UTC (08:50 local): daily check-in

- Thread #50: nothing new from their side; our 16 Nov 21:35 UTC BVI post is the latest comment (no reply since 13 Nov 08:13 UTC).
- Queue: 023 second-winter download running since Mon 15:21. SMOC and waves all stored (30 source-months); ERA5 6 of 15 (202311-202404), now taking 150-245 min a month; on 202405 since 11:48 UTC. 9 months left, so done about Wed 18 Nov 13:30 local, then 023b (~65 min) and 024a/b/c (~2.5 h), about 17:00.
- Moved the 023b/024 check (analysis + approved follow-up post) from Wed 16:45 to 17:30 local. Next daily check-in Wed 08:47.

## 2026-11-16, 21:40 UTC (16:40 local): holding points and BVI screen analysed; BVI comparison posted

- Queue: 021 finished 10:55, 021b 12:01, 022 15:21; 023 (second winter download) started 15:21, ERA5 ~3 h a month, about Wed 18 Nov midday.
- 021b (docs/data/arrival_analysis.py): reached the holding point Falmouth Bay 64.8%, Mount's Bay 51.2%; success vs stopping 40 km off Scilly -6.2 / -5.4 points; within 1 km of the Manacles 18% / Lizard 14% (Falmouth), Wolf Rock 9% / Runnelstone 8% (Mount's Bay). Recommendation pending: hold 10-15 km offshore. Queued 023b (run_arrival_offing.bat: Lizard offing and mouth of Mount's Bay).
- 022 (docs/data/ew_screen_analysis.py, one winter): Mindelo 89.7% (85 d, 42% March arrivals), Gran Canaria via 20N 28W 85.7% (111 d, 49% March), Gran Canaria direct 75.3% (142 d, arrives May), Lisbon 53.3% (65 aground). Weed x2 -1.0; storms 0-2%. For March: Mindelo early Dec-early Jan, Gran Canaria (south) ~10 Nov-10 Dec. New southern BVI approach (bvi_s) after ~10% passed within 1 km of Virgin Gorda's south rocks.
- 024a/b/c written and queued after 023b: Mindelo, Gran Canaria south and El Hierro south to the BVI on both winters, 500 each; Gran Canaria south May launches 2024/2025.
- Thread read first (nothing new from their side). Posted the BVI comparison and holding-point results as approved ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6930093866), text collab/post_2026-11-16_bvi.md); API shows exactly one new comment.
- Scheduled: Tue 08:47 daily check-in; Wed 18 Nov 16:45 local check for 023b/024 (posts the follow-up promised in today's comment).

## 2026-11-16, 13:58 UTC (08:58 local): daily check-in

- Thread #50: nothing new from their side; our 15 Nov 19:43 UTC update is the latest comment (no reply since 13 Nov 08:13 UTC).
- Queue: 021 tropical download still running. SMOC and waves all stored; ERA5 has 202411-202506 and is on 202507, the last month. CDS is now taking about 3 h a month (110-190 min). Expected done about 11:30 local, then 021b holding points (~80 min) and 022 BVI screen (~3 h), so about 16:00 local. 023 (15 more months) at this rate runs to about Wed 18 Nov midday.
- Moved the 021b/022 analysis + BVI post check from 13:00 to 16:30 local. Next daily check-in Tue 08:47.

## 2026-11-15, 19:45 UTC (14:45 local): launch windows and northern route analysed; update posted

- 019a-c (Rev E1, 45 km -> Cornwall, 2021-24, 500 each; docs/data/window_analysis.py): April 86.0%, 1-20 May 86.2%, 21 May-15 Jun 89.0%; paired vs 1-20 May -0.2 (-4.2 to +3.8) and +2.8 (-0.8 to +6.4); every year 82-90%; storm exposure 1.6 / 4.8 / 12.5%. Recommendation in docs/Launch_Plan.md (for Randolph to confirm): keep 1-20 May, treat 1 Apr-15 Jun as usable.
- 020 northern route (Cornwall -> New England, 300): 0 arrivals (0-1.3%); 88% still at sea at end of data after a median 175 days, about halfway. docs/East_West_Study.md 4b.
- Thread read first: no new comments since our 14 Nov 13:45 UTC post. Posted the update Randolph asked for ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6900195070), text collab/post_2026-11-15_update.md); API shows exactly one new comment.
- Scheduled: Mon 16 Nov 13:00 local check for 021b (holding points) and 022 (BVI screen), which posts the BVI comparison as approved; Mon 08:47 daily check-in.
- Results saved: results/2026-11-15_window_*_2021+2022+2023+2024_revE1_hatteras_stream__cornwall.json, results/2026-11-15_ew_2023+2024_cornwall__new_england.json; logs collab/run_log_plan_window_*_2026-11-15.txt (paths stripped).

## 2026-11-15, 19:35 UTC (14:35 local): Randolph's decisions: arrival holding, east-west backup to the BVI

- Arrival: the boat goes into a holding pattern somewhere safe but as close to the coast as possible, for an easy pickup. Two Cornwall holding points set up (collab/arrival/make_arrival.py): Falmouth Bay (approach S of Scilly, Wolf Rock and the Lizard, E of the Manacles) and Mount's Bay (S of Wolf Rock, into the bay downwind). 3 km arrival radius, watch lines for the rocks. Queued as 021b_arrival (run_arrival.bat, 2 x 500, same seeds as 017), after the tropical download. Synthetic-weather smoke tests ran without errors; they used the coarse fallback coastline, so they say nothing about success.
- East-west: a backup option. Recovery in the British Virgin Islands (holding point ~4 km S of Norman/Peter Islands, approach along 18.25 N clear of Anegada's reef); March arrival preferred. 022 screen re-aimed: 6 launch points -> BVI, southern route, weed x2, Gran Canaria -> Barbados for comparison; launches 1 Nov-15 Jan. docs/East_West_Study.md section 7.
- Randolph asked for an update to John's team at the 14:40 check; that check's instructions now include these decisions.
- Copied to the PC: arrival and BVI scenarios, run_arrival.bat, run_ew_screen.bat, docs.
- 14:14 local: Randolph approved posting the BVI comparison to John's team when it comes in. The 14:40 check schedules the 021b/022 check, which now posts the BVI comparison and the holding-point results (one comment); the Monday check-in prompt says the same.

## 2026-11-15, 19:05 UTC (14:05 local): daily check-in

- Thread #50: nothing new from their side; our 14 Nov 13:45 UTC status post is still the latest comment (no reply from them since 13 Nov 08:13 UTC).
- Queue: 018 finished 11:41 (all ERA5 months for 2021-24 now stored; the CDS failed-job fix wasn't needed this time), 018b 11:42 (nothing left to fetch), 019a 12:16, 019b 12:53, 019c 13:25, 020 northern route 13:49; 021 tropical download started 13:50 (9 months x era5/smoc/wav into workspace_ew; 211 GB free). 022 and 023 waiting.
- 020's mc result is fine, but its storm check failed: docs/data/hurdat2_atlantic_1981-2025_box.csv was never on the PC. Copied it there; the 14:40 check can rerun the storm check here in the repo.
- 021 built docs/data/hurdat2_atlantic_1981-2025_tropics.csv on the PC (NHC hurdat2-1851-2025-092326.txt, 17,564 points); copied into the repo.
- Scheduled: 019/020 analysis and the approved results post at 14:40 local today; next daily check-in Mon 08:47. 022 should finish Monday mid-morning; the Monday check-in will schedule its analysis if needed.
- Still open: knockdown damage scaling, storm loss model, Bluewater visual pass, #117 wind correction in the loop, Scilly arrival behaviour, Randolph's three east-west questions.

## 2026-11-15, 05:12 UTC (00:12 local): full update emailed to John

- Randolph said John's team hasn't been updating him and asked for a full 72-hour update with plans and ETAs by email. Sent from Randolph's Gmail (built-in browser) at 00:12 local, one recipient, text in collab/email_2026-11-15_john.txt; confirmed in Sent.
- 00:19 local, second email at Randolph's request: every #50 message between the teams 12-15 Nov (theirs 6, last 13 Nov 08:13 UTC; ours 9) with links, related boat-sim PRs, and what's still open (collab/email_2026-11-15_john_thread.txt). Both confirmed in Sent.
- Queue at 04:24 UTC: 018 has stored 7 of the 11 missing ERA5 months (about 2.2 h each); 4 left, done about 07:00 local; 019a-c about 09:00.

## 2026-11-14, 13:50 UTC (08:50 local): daily check-in

- Thread #50: nothing new from their side; our status post at 13:45 UTC is the latest comment.
- Queue: 018 (ERA5 2021-22 re-download) running since 08:01 local; 018b, 019a-c, 020-023 waiting. Scheduled: the 019 check and results post at Sun 15 Nov 12:30 local. Next daily check-in Sun 08:47 local.
- Since the last daily list: Rev D1 became Rev E/E1 and the launch recommendation was adopted (Hatteras 45 km -> Cornwall), so both are closed.

## 2026-11-14, 13:50 UTC (08:50 local): scheduled check; 015c and 017 analysed; download fix

- Queue: 016 finished 07:16 local but stored only 5 of 18 ERA5 months: CDS failed the job for era5 202109 (HTTP 400 "The job has failed") and our downloader stopped the whole ERA5 lane on any 4xx. 015c finished 07:29, 017 at 08:00. 018 started 08:01: the 2021-22 waves now come from WAVERYS (0.2 deg, about 3 min a month; all stored up to 202207 so far) and it is retrying the 13 missing ERA5 months (about 2 h each at CDS today).
- Fix: bulk.py treats CDS "The job has failed" as a server-side failure: retry twice after 10 min, then skip to the next month instead of stopping the lane. Other 4xx still stop it. Copied to the PC (matched HEAD first); 018b_download_retry queued before 019 to pick up anything still missing.
- 015c -> docs/data/fatigue_voyage.py: per crossing, fin root/stern post/cw arm use about 0.2% of fatigue life; the old 12x10 tail boom 130% (so Rev E1's 16x14 is necessary); servo moves 2.85 M per crossing with the filter, 3.6 M on a p90 voyage. Field Test P raised to 4 million movements.
- 017 -> docs/data/revE1_analysis.py: Rev E1 88.4% vs Rev E 87.6%, +0.8 (-1.4 to +3.0), same seeds. Cornwall-end watch lines can't show the final approach: the simulator stops 40 km from the target at Scilly. Arrival behaviour added to Launch_Plan open questions.
- Randolph asked (08:43 local) to update him and John's team now. Thread read first: no new comments from their side since our 02:57 UTC post. Posted the status update ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6878179574), text collab/post_2026-11-14_status.md); API shows exactly one new comment. The 019 launch-window results post (approved 13 Nov) is still to come.
- ETAs: 018 about Sun 15 Nov mid-morning; 019a-c Sun about noon; then 020-023 (East_West_Study.md).

## 2026-11-14, 03:40 UTC (13 Nov, 22:40 local): east-to-west plan; results posting approved

- Randolph approved posting the 017/019 results to #50 when they are in (13 Nov, 22:02 local). The 13:20 UTC check now does that (one post, via the browser).
- Randolph asked for an east-to-west plan: [docs/East_West_Study.md](../docs/East_West_Study.md). The trade-wind route Canaries -> Lesser Antilles (Oshen PC13's route), launch about 20 Nov-31 Jan, 90-125 days from the Canaries; first pair Gran Canaria -> Barbados; northern route not a candidate. Three questions for Randolph at the end.
- Simulator: westbound support (far_side "americas", launch windows across New Year, download --box, weed_zones by month, stormcheck --storm-csv; docs/data/make_hurdat_subset.py). Default behaviour checked identical byte for byte. PC copies of the four changed files matched HEAD before the update.
- Queue after 019: 020 northern route (existing data), 021 tropical-box download Nov 2024-Jul 2025 (own cache simulator\workspace_ew), 022 screen (12 runs x 300), 023 second winter + summer months. 024 written after 022.

## 2026-11-14, 02:57 UTC (13 Nov, 21:57 local): Rev E1; new runs queued; update to Maya's team

- Randolph decided: drop 45 km off Hatteras, leak SAFE limit 1.0 kg, 16 x 14 tail boom. Drawn as Rev E1 (part/firmware fixes): P08 and P09 sockets D16.2, boom axis z 278, D00/D06 notes, Revisions.md, Design_RevE.md. Simulator revE1_design.json; design.load accepts "E1". Counterweight +24 g (model), boom +12 g; earlier "30 g + 60 g" corrected.
- Download 016: Copernicus wave forecast archive starts Nov 2022, so 2021-22 wave months failed. bulk.py now uses WAVERYS (cmems_mod_glo_wav_my/myint 0.2deg) for months before 2022-11; re-download queued (018).
- Queue: 015c sea states (now on the Rev E 45 km tracks), 017 E1 baseline 2023-24, 018 waves, 019a-c launch windows on 2021-24. Watch lines added at the Cornwall end (Seven Stones, Scilly; approximate).
- Thread #50 read first: no replies since 13 Nov 10:56 UTC; their team made our C5 and Rev B sailable in Bluewater (#520, #523).
- At Randolph's request, posted a full update with plan and ETAs ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6870584552)): new route and the Diamond Shoals finding, Rev E and E1 results, naval checks, the WAVERYS heads-up, queue and ETAs, offers (Rev E1 yaml, C5 re-score). Text: collab/post_2026-11-14_update.md.

## 2026-11-14, 00:55 UTC (13 Nov, 19:55 local): naval review items 1-9 run

- Randolph approved items 1-5 of the naval-review follow-ups (fatigue/creep, flooded stability, steering workload, drift from the new drop, more weather years).
- PC runs finished: 013 (Rev E baseline and slow-boat), 014 (drop points), 015 (drift). Rev E Hatteras Inlet -> Cornwall 83.4% (+15.0 over Rev D); 45 km drop 87.6% (+4.2 over inlet, clear of the shoals); 70 km 86.8%; dog-leg doesn't clear the shoals. Speed x0.9: -0.6; x0.8: -5.0. Drift: inlet 14-17/32 aground in 30 days, 45 km 2-8/32, 70 km 0-3/32. Launch_Plan: 45 km recommended, 70 km alternative, for Randolph to confirm; onshore-wind launch rule added.
- 015b (sea states along tracks) failed at a voyage that ran into December 2024 (no data); fixed to skip and count those hours; re-queued as 015c, runs after the download.
- 016 download of April 2021-2024 and May-Nov 2021-2022 started 19:33 (245 GB free).
- Flooded stability (docs/Flooded_Stability.md): self-righting holds with 3 kg free water; GM -11%. Sump holds only 1.2 L, below Rev E's 1.5 kg SAFE limit: recommend 1.0 kg (asked).
- Fatigue/steering/motions (docs/Fatigue_Review.md): no fatigue concern except the tail boom in 5 m beam seas (recommend 16x14 tube, asked). The Rev E steering rule as written (2 deg deadband, one command per 10 s) loses the course in the 6-DOF model; replaced in the docs and D05 by a wave filter (~4 s). A crossing is ~2.7 million servo movements; Test P raised to 3 million.
- sixdof.py: optional rudder keys deadband_deg, update_s, cmd_deadband_deg, wave_filter_s (off by default; default run checked identical to the previous code).

## 2026-11-13, 21:06 UTC (16:06 local): plan changed to Hatteras -> Cornwall; Diamond Shoals found; naval review

- Randolph approved the plan change. docs/Launch_Plan.md rewritten; Executive Summary, Build Plan, README, Launch_Point_Study updated. designs/boat-sim files left at the Ocean City drop.
- While rewriting: the 10 km Hatteras Inlet drop sends ~52% of stage C tracks within 2 km of Diamond Shoals (not in the simulator's coastline); the 45 km charter point 0% within 10 km (docs/data/diamond_shoals_check.py). Drop point made provisional at the 45 km point. Lesson: check the chart at both ends, not only the simulator's map.
- Simulator: scenario key watch_lines (closest approach reported, voyage unchanged); design study key performance.speed_factor (inert at 1.0). Copied to the PC after checking its files matched the repo.
- docs/Naval_Review.md: what is covered, ten gaps ranked. Hull stress judged low value (girder factor 13).
- PC queue: 013 run_plan_baseline.bat started 16:02 (Rev E Hatteras Inlet -> Cornwall, then speed x0.9 and x0.8; 500 voyages each, 2023+2024). 014 run_launch_shoals.bat after it (Rev E -> Cornwall from the 45 km point, a 70 km point east of the shoals, and the inlet with a dog-leg). Both about 1 h 36 min; check at 19:20 local.

## 2026-11-13, 21:00 UTC (16:00 local): stage C and Rev E results

- Stage C (Rev D, 500 voyages per pair, 2023+2024, same seeds), 13:56–15:30: Hatteras Inlet -> Cornwall 68.4%, Hatteras Inlet -> SW Ireland 64.6%, Ocean City -> SW Ireland 59.2%. Best pair vs current plan +9.2 (+3.8 to +14.8), +9.2 in each year. Launch alone +5.4 (-0.2 to +10.8), destination alone +3.8 (-0.2 to +7.8). Recommendation written in docs/Launch_Point_Study.md for Randolph to decide; other docs unchanged.
- Rev E first run, 15:31–15:45: 76.4%, +14.4 (+7.6 to +21.2) over Rev D; 4 points under the package study (two weed measures, +0.7 kg, chance). docs/Design_RevE.md.
- Queue empty; PC idle.

## 2026-11-13, 19:20 UTC (14:20 local): Rev E drawn (reliability package approved)

- Randolph approved the reliability recommendations. Drawn as Rev E, not "D1": the pump is a new system and the humidity sensor a new sensor (docs/Revisions.md). docs/Design_RevE.md.
- Leaks: bilge pump on spacer P24 against the mast tube, strainer port of the keel box, outlet loop + check valve + deck fitting; keep-sailing response; vents, Schrader test valve, BME280. Servos: SER-2000 sealed rudder servos in cradles P12 (envelope an estimate, measure first), arms P26, spring pushrod links; potted tail servo with detent P25; deadband steering. Weed: fairing W1 (T21) and shedding manoeuvre W4.
- Correction: raked rudders (W3) are not a template change (tip would sit 160 mm aft, past the transom and off the stock); deferred with W2.
- 28.5 kg, DWL z 106, GM 0.180. About +$360 (total about $3,280). Sheets D00, D03-D06, D08; Field Tests O, P, Q added.
- Simulator: designs/revE_design.json; design.load() accepts revision "E" (copied to the PC; Rev D still the default). Rev E run queued as 012 after stage C (250 voyages, same seeds as Rev D).
- Stage C at 360/500 of its first run at 14:20, on time.

## 2026-11-13, 18:57 UTC (13:57 local): stage B, reliability and speed check results; stage C running

- PC queue ran cleanly: reliability 04:05–07:06, stage B 07:06–12:52, speed check 12:53–13:20 local. No errors.
- Stage B (docs/Launch_Point_Study.md): 4 launches x 3 destinations, Rev C5, 150 each. Pooled over destinations, Hatteras 45 km, Ocean City 100 km and Hatteras Inlet 10 km are each ~+4 over Ocean City 10 km (ranges cross zero) and tied with each other; SW Ireland = Cornwall, Brittany -2. Canaveral rerun 34.0% (flawed run 31.3%), still worst. Stage C pairs: Hatteras Inlet -> SW Ireland, Hatteras Inlet -> Cornwall, plus Ocean City -> SW Ireland.
- Reliability (docs/Reliability_Review.md): bilge pump + pump-and-sail 70.0% (+8.0, +4.8 to +11.6, 20 gained / 0 lost); full package 80.8% (+18.8, guesses flagged); weed pessimistic 61.2% (-0.8). Rev D1 recommendation written, awaiting Randolph; not drawn.
- Speed check PASS: identical on 80 real-weather voyages, 4.3-4.4x faster; faster code installed on the PC. make_batch.py time estimate updated (9 min per 150 voyages).
- Stage C queued as 011_launch_final.run (started 13:56 local): Rev D, 500 voyages per pair (250 per year, 2023 and 2024), ~1 h 36 min. Final check scheduled 15:50 local.

## 2026-11-13, 14:40 UTC (09:40 local): daily check-in, thread not read

- Could not read issue #50: the browser link to Randolph's PC was disconnected, the GitHub API is not enabled for boat-sim in this session, and a plain web fetch needed an approval nobody was around for. Nothing posted.
- Open items brought up to date in the next check-in (14 Nov, 08:47): stormcheck on real-weather tracks and the limp-home and destination decisions are done; still open are knockdown damage scaling, the storm loss model, Rev D1, the launch recommendation (stage C), the Bluewater visual pass, and the #117 wind correction in the voyage loop.
- Pending today: 13:50 check (stage B, reliability, speed check, queue stage C).

## 2026-11-13, 13:30 UTC (08:30 local): simulator speed-up, pending a check on the PC

- Randolph asked whether his GPU could help; it can't usefully (the time is Python overhead in sequential steps). Agreed instead: faster CPU code that must give bit-for-bit identical results.
- Rewrote the polar lookup and the land test (docs/Simulator_Speedup.md). Identical on 100k polar inputs, 49k land points on the Natural Earth coastline, and 84 full voyages incl. groundings; land test 10-13x faster, voyages ~6x faster on synthetic weather. DRONE_SIM_REFERENCE=1 keeps the old code.
- PC: full new package in simulator\speedup\drone_sim; run_speed_check.bat (request 010a, after stage B, before stage C) runs 80 real-weather voyages old vs new and installs vpp.py/env.py only if identical. The repo already has the new code; the PC uses it only after a PASS.
- The 13:50 check now also reports the speed check.

## 2026-11-13, 11:25 UTC (06:25 local): commitments to Maya's team done

- Correction: our 05:55 post offered to take the hurricane hazard half and asked for their ERA5 wind correction. Both were already done (our docs/Hurricane_Risk.md of 9 Nov; their #117 ratios, already in storms.ERA5_RATIO). Corrected in the follow-up post. Lesson: check the repo before promising work from a summary.
- Hurricane update on the 12 launch-study tracks (docs/Hurricane_Risk.md, docs/data/launch_storms.py): exposure ~3x the 9 Nov synthetic estimate (Ocean City May launch 15% within 200 km), because real-weather crossings are slow. Storms cost 0.7-1.5 points per launch point with the grade-D loss model; ranking unchanged; launch date matters more.
- Bluewater first look (title page, picker, their randolph_rev_c.yaml, 3D source): labels clear; their C5 yaml matches ours; 3D model has the C5 wing but a Rev B bulb (D68) and spar (25 mm); Rev D not in the picker; zero-size-canvas WebGL warnings with our pane hidden; sound flips on at first click. Visual pass of the sailing screen still to do (needs the browser pane on screen).
- Posted: https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6850834723

## 2026-11-13, 10:55 UTC (05:55 local): full update to John's team (Maya)

- Their team is back: Maya now leads it and is the main contact; their project is now Bluewater, a browser sailing simulator with our C5, Rev B and the Pearson in it (labelled as their model). They asked for a sync: our two or three current projects, and what we'd want from them. The C5 re-score is still on their list.
- At Randolph's request, posted a full update ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6850642299)): Rev D and its first run (62.0%), the 13-destination study, launch-point stage A, the reliability review, the schedule, and answers.
- Asked them for: regional fishing and traffic density (their #62); their ERA5-vs-IBTrACS wind correction. Told them we'd take the hurricane hazard half (their earlier unanswered question). Re-score: C5 still the right boat for it.
- Said we'd look at Bluewater and report anything that looks wrong.

## 2026-11-13, 09:55 UTC (04:55 local): launch study stage A results; stage B queued

- Stage A finished 04:04 (restarted batch ran cleanly). Rev C5, 150 paired voyages, all to SW Ireland: Hatteras 45 km (charter) 54.0, Ocean City 100 km (charter) 50.0, Hatteras Inlet 49.3, Virginia Beach 48.7, Ocean City 46.7, Cape Cod 46.6, Montauk 46.0, Maine 44.0, Charleston 43.3, Palm Beach 42.7, Barnegat 34.7, Canaveral 31.3 (route crossed the cape: 8 aground on day 0; rerun queued). With the fishing-ground mark-down, Maine and Cape Cod fall well behind.
- Waypoint rule check: abeam vs old rule at Ocean City +2.0 (-0.2 to +4.2), 137/150 identical.
- Reliability study (020) started at 04:05 before stage B could be queued; stage B (run_launch_pairs_2023.bat, request 010: HS/OCC/Hatteras/OC x Cornwall/Brittany + canaveral_east) follows, ~8:05 am to ~1:40 pm.

## 2026-11-13, 02:10 UTC (21:10 local, 12 Nov): runs survive unplugging

- Randolph confirmed he had unplugged the laptop. Added simulator/fix_run_queue_battery.bat (sets the task's AllowStartIfOnBatteries and DontStopIfGoingOnBatteries); setup_run_queue.bat now applies the same. cli.py now asks Windows not to sleep during every run (it only did with --wait-for-limits). Copied to the PC; the running stage-A run is unaffected (Python had already loaded cli.py), runs 2-12 pick it up.

## 2026-11-13, 01:55 UTC (20:55 local, 12 Nov): stage A restarted in a visible window

- The first stage-A run (009, started 18:02 by the scheduled task, hidden) died without writing anything: no Python processes left, stale running.lock. Likely cause: the laptop's scheduled task stops on battery power by default. Not confirmed.
- Randolph opened the new simulator/run_queue_window.bat. Queued unlock.run + 009b_launch_points_2023.run; stage A restarted in his window at 20:49, CPU 99%, 7/150 voyages after 5 min. The mc log now gets a progress line every 10 voyages.
- 020 (reliability study, 3 x 250) waits behind it.

## 2026-11-13, 01:15 UTC (20:15 local, 12 Nov): reliability review (servos, weed, leaks)

- Randolph asked for mitigations for the rudder and tail servos, weed (more sweep, no protruding bulb nose) and leaks (pressurised hull?), then suggested a bilge pump.
- Finding from the Rev D event logs: no boat was swamped; leak losses (41 of 95) come from the safe-mode response, which never releases. A tail servo that fails free was a certain loss (15 of 15). Both rudders lost in 32 voyages.
- docs/Reliability_Review.md: bilge pump + pump-and-sail response; pressure-decay test, membrane vents and a humidity sensor instead of a pressurised hull; sealed magnetic-encoder servos (Blue Trail SER-2000 kit + DFRobot), tail magnetic detent, deadband steering; weed: fin-bulb fairing, flush nose with the fin 90 mm forward (check in sim), raked rudders, shedding manoeuvre.
- Simulator: new design keys (leak_policy, bilge_pump, servo rate factors, tail_fail_free_share, weed catch/clear). Rev D as drawn is bitwise unchanged. Three 250-voyage runs queued on the PC as 020 (run_reliability_2023.bat, ~4 h) behind the launch study: pump only, full package, weed downside.
- Nothing posted to John.

## 2026-11-13, 00:45 UTC (19:45 local, 12 Nov): destination study final; Rev D as drawn

- 007 finished 16:57, 008 (Rev D) 17:59, 009 (launch study stage A) started 18:02 local.
- Destinations (Rev C5, 150 paired voyages): SW Ireland 44.7, Cornwall 44.7, West of Ireland 42.0, Brittany 41.3, Biscay 38.7, Galicia 38.0, Hebrides 38.0, Cádiz 36.7, Portugal 33.4, Canaries northern arc 22.0, Morocco 18.0, Canaries 10.7. Azores (separate) 52.7, 90-day median. Stage B destinations: SW Ireland, Cornwall, Brittany.
- Rev D as drawn: 62.0% (55.8-67.8), +14.0 over C5 paired (+6.5 to +21.5); matches the 61.2% study. 47 backup takeovers, 30 sailed in. Top first failures now rudder servos, tail servo, fouling, leaks.
- Not posted to John (their team is paused; destination results not approved for posting).

## 2026-11-12, 19:55 UTC (14:55 local): John's team has paused; plan posted

- John on #50 (two notes since our Rev D post): their side is pausing help while they get their process in order, because of repeated failures by the Claude agents running their project. Nothing on our side caused it. The Rev C5 re-score and any new requests are on hold; they will get in touch when ready.
- At Randolph's request, posted the launch-study plan and his message that we hope none of the team gets fired and are thinking of them ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6834278411)). No reply asked for. No destination results included.
- While they are paused: no requests to their team; keep reading the thread at check-ins.

## 2026-11-12, 19:45 UTC (14:45 local): launch-point study added

- Randolph asked to add launch points up and down the US Atlantic coast, then launch + destination pairs, guided by research. Plan and sources: docs/Launch_Point_Study.md.
- Research in brief: 8 Microtransat boats left Cape Cod and none passed 2,100 km (3 caught by fishing boats within 6 days); Newfoundland starts did far better; miniboats are dropped into the Gulf Stream, which is 1-3 miles off Palm Beach, 15-25 miles off Hatteras and about 250 km from Ocean City.
- Stage A: 12 launch points (Maine to Palm Beach, plus charter launches 100 km off Ocean City and 45 km off Hatteras), all to SW Ireland, Rev C5, 150 voyages, 2023. Queued on the PC as 009 (run_launch_points_2023.bat, about 8 h, resumes after a reboot). Stage B: best 3 launches x best 3 destinations. Stage C: best pairs on Rev D, 2023 + 2024.
- Simulator: new scenario option waypoint_rule "abeam" (a waypoint also counts once passed), used only by the launch scenarios; old scenarios unchanged. Ocean City is rerun with it as the baseline.
- In the batch-1 Ireland run from Ocean City, 9% of boats were lost or aground within 3 weeks and 11% ended aground on the home side.
- Scheduled: 19:30 destination check revised (no destination confirmation run; that is now stage C); new check 02:45 on 13 Nov for stage A and to queue stage B.

## 2026-11-12, 19:25 UTC (14:25 local): destination study, batch 1 (interim)

- 006 finished 12:32 local; 007 (batch 2) started 12:37 and takes about 37 minutes per aim point, so about 5:00 pm finish (not 1:30 pm as first estimated). 008 (Rev D) follows, about 6:25 pm. The 7:30 pm final check should find both done.
- Batch 1 (Rev C5, 150 paired voyages each): SW Ireland 44.7%, Cornwall 44.7%, Brittany 41.3%, Galicia 38.0%, Portugal 33.4%, Canaries 10.7%. Southern routes slower and more often still at sea at season end. Interim table in docs/Destination_Study.md. No recommendation until batch 2. Not posted to John.

## 2026-11-12, 16:45 UTC (11:45 local): Rev D posted to John

- Posted on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6829060738)): what Rev D is, mass and cost, new randolph_rev_d.yaml (rev_c back to C5, matching their Boatyard preset), the backup steering their schema can't express, the queued Rev D run, and our revision convention (C6 = Rev D).
- Their latest: C5 re-score our way needs fresh runs; their team is on a game push for a day or so.

## 2026-11-12, 16:30 UTC (11:30 local): C6 renamed Rev D; revision convention

- Randolph agreed C6 should be a new letter: it adds a system. Renamed throughout (drawings, docs, simulator `revision` "D", designs/revD_design.json, run_revD_2023.bat, boat-sim randolph_rev_d.yaml; randolph_rev_c.yaml and revC_design.json back to C5). New docs/Design_RevD.md and docs/Revisions.md (convention + history).
- PC: Rev D files copied; queue item 008_revC6_2023.run now runs run_revD_2023.bat (filename kept; stale revC6 files on the PC are unused).
- Randolph approved sharing Rev D with John, with our revision convention.

## 2026-11-12, 16:05 UTC (11:05 local): Rev C6 drawn

- Randolph approved drawing the limp-home controller as Rev C6, with potting and the RockBLOCK Plus.
- Drawn: P21 limp-home case (bulkhead x 300), P22 switchover pod (bulkhead x 1260), P23 RockBLOCK Plus bowl in the hatch lid; main GPS moved to P05 (it sat under the aft solar panel). Sheets D00, D01, D03, D07, D08, D20, D21; T16 lid cut. 27.8 kg, GM 0.182, DWL z 104.
- New docs: Limp_Home_Spec.md, Potting_Spec.md; Test N in Field_Tests.md; C6 section in Design_RevC.md; parts and budget updated (+~$370, RockBLOCK Plus price not confirmed).
- Simulator: C6 is the default (limp_home fitted, electronics_protection 0.6/0.5, wet factor 1.3); pre-C6 files keep their behaviour. Copied to the PC; queued 008 run_revC6_2023.bat behind 007. Not shared with John yet.

## 2026-11-12, 15:25 UTC (10:25 local): limp-home results

- 004b and 005 finished (07:44, 08:43); 006 destinations started 08:47.
- Scoring bug: `_arrival_outcome` returned arrived_adrift for any box-dead arrival, including limp-home sailed arrivals. Fixed (limp_on -> tracked/silent). Runs rescored from event logs: limp 59.6% (+11.6 vs C5, +7.6..+15.6), limp+elec 61.2% (+13.2, +8.7..+17.7). Guessed factors: 85% speed, 0.5x failure rate, no rudder/tail failures while it steers.
- Electronics_Review.md updated. Posting to John (approved).

## 2026-11-12, 14:50 UTC (09:50 local): re-score reply posted

- Randolph approved; posted on #50 accepting John's offer to re-score C5 our way, with the corrected 121-day median. Removed the posted drafts.

## 2026-11-12, 13:55 UTC (08:55 local): daily check-in

- John on #50: their 15% vs our 48% is scoring. Their finish = Microtransat rule (within 25 km of 39.5N 13.5W; landfall doesn't count; >10 days silent DQ), 150-day cutoff, launches 1 Apr-30 Jun 2015-2019. Offered to re-score C5 our way. Reply drafted in collab/draft_50_rescore.md (accepts the offer; notes our corrected median is 121 days). Not posted: needs Randolph's approval.
- Old check-in items: both logs (drift 2024, C1 compare) were analysed on 11 Nov; verbose batch files are on the PC. Still open: severity-scaled knockdown damage, stormcheck on real-weather tracks.
- Queue: 004b limp run in progress since 06:57.

## 2026-11-12, 11:45 UTC (06:45 local): PC back after a Windows update reboot; first corrected results

- PC rebooted overnight (Windows update) during 004 run_limp_2023.bat (started 23:17, lost). 002 and 003 finished before it. Cleared the stale lock (queue/unlock.run) and requeued 004 as 004b; 005, 006, 007 still queued.
- Corrected simulator, 2023, 250 voyages paired: Rev C 43.6%, C5 48.0% (+4.4, -3.1..+11.9), C5 + better electronics 52.8% (+4.8 vs C5, +1.5..+8.1). Median 121 days all. Wing losses 40 -> 3. Keel joint 2.
- Results and sanitized logs saved with 2026-11-12 names; Design_RevC.md and Electronics_Review.md updated.

## 2026-11-12, 02:20 UTC (21:20 local): Pearson link not posted; PC offline

- Randolph asked to send John the sailboatdata link for his Pearson 31-2. Not posted: the browser and file tools for the PC disappeared and the device bridge reports the PC not connected. gh in this session cannot write to boat-sim, and attaching the repo with push access was refused. Draft saved in collab/draft_50_pearson.md.
- The overnight checks (03:15, 08:30, 13:45) need the PC connected to read results.

## 2026-11-12, 01:35 UTC (20:35 local): plan and ETAs posted to John

- At Randolph's request, posted the overnight run plan and expected finish times on #50 (six queue items, results post about 03:15; destination ranking Thursday afternoon if Randolph wants it shared). Asked whether they have a view on landfall or regional traffic data.
- Queue check: 002 running since 19:57, no errors in its log so far.

## 2026-11-12, 01:25 UTC (20:25 local): destination study widened to 13

- Randolph asked how the six were chosen and whether others should be simulated. They were a quick latitude sweep, not optimised. Added batch 2 (queue item 007, `run_destinations2_2023.bat`): Bay of Biscay, west of Ireland, Outer Hebrides, Gulf of Cadiz, Morocco, Canaries by the northern arc, Azores (flagged: only if it counts as across). Rationale and exclusions in docs/Destination_Study.md.
- Scheduled checks: 08:30 interim (first six), 13:45 final (all 13, recommendation, confirmation run). The original 08:30 check could not be deleted (permission denied), so its message was replaced with a "superseded, do nothing" note.

## 2026-11-12, 01:30 UTC (20:30 local): destination study queued

- Randolph asked for destinations other than Ireland with the highest survival odds across the Atlantic.
- Simulator: scenario `africa_landfall_counts`; `atlantic_islands_count` can be "no_azores"; `LandMask.far_side()`. Arrival record gains `landfall`.
- `collab/destinations/` six scenarios (SW Ireland, Cornwall, Brittany, Galicia, Portugal, Canaries); `simulator/run_destinations_2023.bat` (150 voyages each, C5, 2023). Queued as 006 after the four electronics/baseline runs. `docs/Destination_Study.md` has the plan and expectations.
- Weather box 26-60N, 82W-0: Norway, Iceland, West Africa south of 26N not possible without new downloads.

## 2026-11-12, 01:15 UTC (20:15 local): limp-home option, overnight runs

- Randolph: check results and post overnight; asked what potting and the backup controller do to survival odds.
- Added a limp-home controller option to the simulator (`design["limp_home"]`, off by default): when the main box dies, a separate potted board keeps steering at 0.85 x speed; fails at 0.5 x the electronics rate (GUESSES). While it runs, rudder/tail failures are not rolled (slightly optimistic).
- Queued on the PC: 004 run_limp_2023.bat (C5 + limp-home), 005 run_limp_electronics_2023.bat (both). With 002 and 003 that is four runs, done about 03:00 local.
- Overnight check scheduled: read results, post to John (approved), report.

## 2026-11-12, 01:00 UTC (19:50 local): simulator angle bug, wing study corrected, electronics review

- Scheduled resume after Randolph's usage reset. Posted update 1 to John (C5 run data, answers on the wing questions).
- John's team: Habaneros fine (brought in as a precaution). Their -16% was their stall-rule bug (PR #325); our VPP has the same rule.
- Found: the voyage simulator passed wind angles in DEGREES to the radians polar since the first commit (sim.py hybrid_step and 6-DOF alpha lookup), so every heading sailed at the dead-downwind speed. All results before today are superseded. The wing study script had the same bug (its -4% was dead downwind only). Fixed; Polar now raises on angles > 3.2; polar cache keyed with MODEL_VERSION 2. Wing stall now lift-based (cl_stall 1.03) for the wing only. docs/Simulator_Angle_Bug.md.
- Corrected wing study: 0.8 x 0.375 m -1.7% average speed, -3% upwind VMG. C5 stands.
- Electronics review (docs/Electronics_Review.md): board potting not considered before; 83/250 C5 voyages had an electronics failure, ~60 from the dry base rate. Recommended: coat all, pot sensors/power/joints, RockBLOCK Plus, limp-home controller (not drawn).
- Queued on the PC: 002 run_fixed_compare_2023.bat (C5 vs C0, corrected sim; started 20:xx) and 003 run_electronics_2023.bat (guessed improvement factors).
- Randolph: tell John he has a Pearson 31-2, deep keel (not wing keel). In update 2.

## 2026-11-11, 18:30: first Rev C5 run (via the run queue)

- Run queue worked: request picked up 15:32, run finished 18:15 (`collab/queue_log_2026-11-11.txt`).
- C5: 40.4% (34.5-46.6) verified arrivals, lost 16%, at sea 28%, median 145 days; wing damage 4 (was 38), keel joint 10, electronics 47 (top cause).
- C2 with the structural model on: 20.0%; every reporting arrival had lost a rudder servo (model near-certain without servo-savers, on top of fitted rates). Not a fair baseline.
- C5 speed on fault-free voyages 1.17 kn vs Rev C 1.23 (-5%); median 130 vs 118 days. Between our 4% and John's 16%. Wing-speed discrepancy still not investigated.
- Not posted to John.

## 2026-11-11, 16:10: personal question relayed; John's wing check disagrees

- Posted on #50 at Randolph's request: a personal question for John's project manager to put to John directly ("I see the Habaneros have moved, how are they doing?").
- John's team ran C4 vs C5 through their port of our foil model: -16% averaged over 3-15 m/s and 50-165 deg (downwind -2 to -12%; at 50 deg from about 9 m/s C5 makes no way), against our -4%. They think theirs is pessimistic (earlier stall at low aspect ratio, 20 deg angle cap) and asked what our 4% averages over and whether our stall angle changes with aspect ratio. Not yet answered or investigated.

## 2026-11-11, 16:30: run queue for the PC

- The PC was locked, so Claude could not start `run_revC5_2023.bat` by double-click (File Explorer access was granted; nothing was clicked). Randolph chose the run queue.
- Added `simulator/run_queue.bat`, `setup_run_queue.bat`, `remove_run_queue.bat`, `queue/README.txt`; copied to the PC with a first request `queue/001_revC5_2023.run`. Not tested on Windows. Randolph has to double-click `setup_run_queue.bat` once.

## 2026-11-11, 16:10: Rev C5 wing, results to John

- Randolph approved the 0.8 x 0.375 m wing and posting the study. Rev C5: D00, D01, D06, T15; simulator wing dims, spar 0.67 kg, `wing_shape_factor` 0.25; 26.92 kg, GM 0.188, counterweight 0.85 kg. `designs/revC5_design.json`, `simulator/run_revC5_2023.bat` (C5 then C2, measured breaker model). Copied to the PC.
- Posted the wing study and C5 to John on #50.
- Randolph asked what it would take for Claude to start PC runs itself: answered (no command tool in this session; options are his go-ahead to double-click batch files in File Explorer, or a scheduled-task run queue). Nothing set up.

## 2026-11-11, 15:30: Rev C4 shared, wing shape study done

- Randolph: correct the record with John, decide Delrin vs 316 and draw all changes, share, tell John about a wing study and run it.
- Already on #50: the correction with sources, and the Rev C4 post (acetal ball bearings with glass balls on O-rings plus plain catcher lands in P07; build notes; `docs/Rudder_Health_Spec.md`), which also says the wing study is starting. Commit b08ed2c.
- Wing shape study (`docs/Wing_Shape_Study.md`): 0.8 x 0.375 m gives -4% speed, slap load 52%, spar-break chance per knockdown 4-8 times lower. Recommended; not drawn. Results not yet posted to John.
- The PC had not started the C3 run (no log there). Copied the current simulator ("measured" breaker default), `run_revC3_measured_2023.bat`, C4 drawings and docs to the PC.

## 2026-11-11, 13:00: research review; strike model corrected against buoy data

- Randolph asked for deeper research (naval design, ocean loads, materials) while his C3 run goes. Wrote `docs/Research_Review.md`.
- Main correction: measured buoy accelerations in real breakers (about 1 g sideways; JMSE 2021 9(2) 214) show the slam model for plunging breakers overstated shock by about ten times. Added `plunge_model="measured"` to `docs/data/strike_sim.py`. Stern post (40 vs 115 N*m) and counterweight arm (20 vs 53) are not fail points; wing spar and rudder servos unchanged. Correction added at the top of Structural_Review.md.
- Simulator default breaker set is now "measured" (tables regenerated; wing factor for C3 0.27). New `simulator/run_revC3_measured_2023.bat` and `designs/revC2_structure_measured_design.json`. NOT copied to the PC: Randolph's run with the older "gentle" set is in progress.
- Other findings: C-Star PC13 (1.2 m) completed the autonomous Microtransat in Sept 2026, 0.96 kn average (our sim: 1.0 kn); stainless in stagnant seawater (mast bearings, rudder stocks, keel rods); white oak bonds with prep; H80 minimum shear 0.95 MPa.
- Proposed, not drawn: mast bearing spec and seal, drawing notes, sticking-rudder detection, a shorter wider wing study.
- `collab/draft_50_correction.md`: draft correction for John, not posted.

## 2026-11-11, afternoon: Rev C3 and the structural-failure model

- Randolph approved all five structural-review changes and asked for drawings, documents, simulator and a post to John.
- Rev C3: YB3 in a flush foredeck well (the tail boom sweeps the deck at z 270 and the aft deck is under the solar panels, so not the aft deck as first proposed); 20 x 2 fibreglass stern post; 12 mm fibreglass rod counterweight arm; servo-savers and +/-40 deg stops; 30 x 22 spar, bearings 130 apart, P07 137 long; second inner ply over the sump. P07 and P19 reprinted (STL rebuilt). 26.93 kg, waterline z 102, GM 0.182, CG 24 mm forward (trim about 0.4 deg bow down: check at the float test).
- Simulator: `drone_sim/structure.py` + `structure_tables.json` (from `docs/data/make_structure_tables.py`): per-knockdown breaks of keel joint, stern post, counterweight arm, tail boom, rudder servo/stock; wing rate x max(C3/C2 ratio, 0.1). Default design = C3 with the model on ("gentle" breakers). Designs saved before C3 load with it off. `designs/revC2_structure_design.json` = C2 with it on.
- New run file `simulator/run_revC3_2023.bat` (C3, then C2 with the model on; 250 voyages each, 2023). Copied to the PC with the simulator.
- Live docs (Executive Summary, Build Plan) got a "Changes since Rev C" section. 3D page not updated (still shows the YB3 on the post).
- Posted to John on #50 at Randolph's request.

## 2026-11-11, midday: whole-boat structural review

- Randolph asked for a naval-engineer's review of every stress point, with simulation behind the guesses. Wrote `docs/data/strike_sim.py` (sway/roll strike simulation with flexible parts), `docs/data/structural_checks.py` and `docs/Structural_Review.md`.
- Simulated values that replace guesses (Hs 5 m): hull picks up 75% of the water speed; half of it in 0.014 s (plunging) or 0.2 s (spilling); roll rate median 0.9-1.5 rad/s, 95% about 3; peak hull acceleration 16 g typical, 68 g 1 in 20 (plunging).
- Fail points: stern post (carries both the main antenna and the YB3), counterweight arm, rudder servos back-driven, wing spar. Hull, deck, hatch, keel rods, battery mounts pass.
- Wing loss per knockdown: model 0.0002-0.03 depending on breaker assumptions; simulator uses 0.0009. Not changed.
- Proposed (not drawn, waiting for Randolph): YB3 to the deck + fibreglass post, fibreglass rod counterweight arm, servo-savers, 30 x 22 spar with stronger bearing housing, second inner ply over the sump. Proposed tests L (breaker test with IMU logging) and M (wing slap).
- Not posted to John.

## 2026-11-11, 09:40: C1 comparison and 2024 drift tests in

- Rev C1, 250 voyages, 2023, near-coast: 45.6% (39.5-51.8) verified arrivals against 38.8% for Rev C as first drawn. Electronics failures 31 vs 37, but wing damage also fell 38 to 28, so most of the gap is chance.
- 2024 bulk drift tests (3.3% leeway), aground within 30 days: 25 km 8/16, 50 km 7/16, 100 km 2/16, 150 km 0/16 (2023: 16, 13, 8, 5). Early-May drops grounded in both years.
- Both logs saved in collab/. Docs: Design_RevC.md, Route_MidAtlantic.md. These runs used the C1 masses (before the C2 fin).

## 2026-11-11, later: Rev C2 keel fin

- Randolph approved the fin change (option 1). Rev C2: hardwood core, 6 x 6 oz + carbon strip each side, 60 mm tenon into a keel-box socket, floors at x 650 and x 800, hull doubler. D00, D03, D04 redrawn; T12, T13 relabelled; new T19, T20; Field Test K (60 kg proof load).
- Simulator default is now C2 masses: 26.41 kg, waterline z 101, GM 0.190, max GZ 0.372 at 105 deg, self-righting. Rev B and the C0/C1 files are unchanged. No keel-loss event added (not asked for).
- Real added mass is 1.1 kg, not the 0.75 kg first quoted.
- Removed `simulator/CON` (written by console.py on Linux; CON is a reserved name on Windows and would break a checkout there). console.py now uses CON only on Windows.
- Not done: speed model rerun at 26.4 kg, 3D viewer and live docs still say C/C1, proof test and keel-loss event options 2 and 3 partly open (test K written; simulator event not added). Not posted to John.

## 2026-11-11, evening: keel fin strength model

- Randolph asked for a physics estimate of John's "keel or structure lost" event. Wrote `docs/data/keel_reliability.py` and `docs/Keel_Structure_Loads.md`.
- Finding: the Rev C fin as drawn (XPS core, 3 x 6 oz) has 113 N*m root strength, 3.2 times the static knockdown load, and the model breaks it within one voyage under every load assumption. Hardwood core + 6 x 6 oz + carbon strips: 1,103 N*m, 0 to 10% per voyage.
- John's placeholder (4e-5 x (Hs/3)^2) is about right for a solid-cored fin; about 8% of voyages on our knockdown counts.
- Not done: drawing change, hull-joint floors, proof test in Field_Tests.md, simulator event. Waiting for Randolph's decision. Not posted to John.

## 2026-11-11, 13:50 (scheduled check)

- John answered the "stuck inverted" question: it is a per-knockdown dice roll in his hazard model, not physics: p_inverted_stuck 4e-5 × (Hs/3)², capped at 5%, standing in for keel, ballast or structural loss. Over several hundred knockdowns that is a few percent per voyage. He will relabel it "keel or structure lost (knockdown damage)" for self-righting boats. Our call whether to set it to 0 or our own rate in `randolph_rev_c.yaml`.
- Our simulator has no keel/structure-loss event, so it is optimistic by about that much. Open decision for Randolph: add one (suggested: John's 4e-5 form as a placeholder, grade D) or leave it out.
- No direct answer yet on whether his team is working today, but he replied within the hour.
- Still open on our side: severity-scaled knockdown damage, stormcheck on the real-weather tracks, 2024 drift tests and the C1 comparison (running on Randolph's PC).

## 2026-11-11, 13:20

- Posted the two-year run, Rev C1 and a Veterans Day "are you working today?" question on #50 ([comment](https://github.com/jcolter11374/boat-sim/issues/50#issuecomment-6796314219)).
- John's 10 km vs 85 km rerun of Rev C (six 2020 dates): beach groundings 2 → 1, no finishes either way; "the drop point cured the too-close groundings, not the overall picture". Two of his Rev C runs ended "stuck inverted"; asked what causes it, since our GZ curve is positive to 180°.
- John asked for details of Randolph's own (personal) boat to add to his sim. Left for Randolph to answer.
- Batch files now show a banner and a live progress line (`drone_sim/console.py`); Randolph asked for this.

## 2026-11-11, 13:00

- **500-voyage run done (Rev C as first drawn, near-coast, 2023+2024): 41.0% verified (36.8–45.4).** 2023 43.2%, 2024 38.8%. Lost 15.4%, position known 81.6%, US-coast groundings 8/500. 30.4% still at sea on 30 Nov, only 18 of 152 still sailing normally.
- The 2023 half (43.2%) vs last night's 250-run (38.8%) for the same configuration shows the noise is ~±4 points; Rev B vs Rev C and 10 km vs 100 km are not resolved at 250 runs.
- Early-May launches did worst in both years (36%, 33%); suggestive only.
- Bulk download complete (all 14 months). Bulk vs Open-Meteo on one no-failure voyage: 112.7 vs 117.6 days.

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
