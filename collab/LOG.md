# Collaboration log

Newest first. Each check of boat-sim records what was new and what we did.

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
