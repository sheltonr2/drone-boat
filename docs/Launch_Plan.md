# Launch plan: off Hatteras, North Carolina, to Cornwall, 1–20 May window

*Rewritten 13 November 2026, when Randolph changed the plan from Ocean City → south-west Ireland to Hatteras → Cornwall ([Launch_Point_Study.md](Launch_Point_Study.md)). The earlier Ocean City plan is in the repo history. Contact details and rules change, so confirm each one when you act on it. Items marked **(confirm)** are ones I couldn't verify.*

## Why these choices

| Decision | Choice | Evidence |
|---|---|---|
| Launch area | **Off Hatteras, North Carolina** | Rev D, 500 voyages per pair, 2023 and 2024 weather: Hatteras → Cornwall 68.4% against 59.2% for Ocean City → SW Ireland, +9.2 points (+3.8 to +14.8), the same in both years. The Gulf Stream is close, so the boat is 200 km out in under 3 days instead of 7 and losses roughly halve |
| Drop point | **Provisional: about 45 km out, 34.95°N 75.35°W, on the Gulf Stream's inshore edge, by offshore charter.** Not the 10 km point off the inlet that the study first recommended | **Diamond Shoals.** They run 13–22 km south-east from Cape Hatteras with as little as 1 m over them, and the simulator's coastline doesn't hold them. About half the simulated tracks from the 10 km point crossed them ([Naval_Review.md](Naval_Review.md)); none from the 45 km point came within 10 km. The two points tied on success in stage B. Runs to confirm on Rev E, and to test a point further east and a dog-leg from the inlet, are queued (13 Nov) |
| Destination | **Cornwall and the Isles of Scilly** (aim point 49.95°N 6.3°W); any European landfall counts | Tied with SW Ireland in the destination study and stage B, +3.8 (−0.2 to +7.8) in stage C |
| Launch window | **1–20 May**, earliest suitable weather day | Storm exposure rises through June ([Hurricane_Risk.md](Hurricane_Risk.md)). Not yet re-run for this route: April is untested because that weather isn't downloaded |
| Before launch | **3-week coastal trial passed** (Field Test F) and **second tracker fitted** | These two items are worth the most odds per dollar ([Failure_Rates.md](Failure_Rates.md) §5) |

## Timeline

| When | What |
|---|---|
| **Now – Jan** | Build per the [Build Plan](Build_Plan.md). Fit and bench-test the backup tracker ([Backup_Tracker.md](Backup_Tracker.md)). Order the labels |
| **Feb** | Field tests A–E (tow, inclining, self-righting, wing balance, solar day). Spar proof-load test. Start servo life Test P (5 weeks) |
| **Mar – mid-Apr** | Field Test F, the 3-week coastal trial: 14 days in a row with no unexplained reboot, leak or reporting gap. Freeze the firmware afterwards |
| **By 1 Apr** | Book the Hatteras charter (below). Send the Coast Guard, fishery and UK notices (drafts below) |
| **20–30 Apr** | Final prep: charge, desiccant change, pressure-decay test, both trackers reporting, photos and serial numbers on file, last software check |
| **1–20 May** | Drive to Hatteras and launch on the first day that meets the weather criteria. Allow several days there: the weather picks the day |
| **During** | Daily check of both trackers. Weekly summary to the Microtransat list, if entered, and to the collaboration thread |
| **Arrival** | Notify HM Coastguard (Falmouth) when within ~50 nm. Arrange recovery or a finder's contact |

## Boat and launch

- **Getting there:** Hatteras village is about 5–6 hours' drive south of Ocean City **(confirm from home)**.
- **Boat:** a Gulf Stream fishing charter out of Hatteras village. Those boats run 20–30 nm to the Stream as a matter of routine, and their skippers cross Hatteras Inlet daily. The boat must lift 29 kg over the side. A half-day booking should cover a 25 nm run out, the launch and an hour's escort **(confirm prices and whether a skipper will take it)**.
- **The inlet:** Hatteras Inlet shoals badly and changes fast. The Coast Guard has repeatedly warned of depths of 2–4 ft in its channels and of unreliable buoys. Don't take a borrowed or rented boat through it; go with someone who runs it every day, and ask about the inlet's state when booking. Oregon Inlet (about 90 minutes north) is the fallback port **(confirm)**.
- **Diamond Shoals:** keep the drop point and the boat's first two days well south and east of the shoals. The autopilot's first waypoint must not let the Stream carry it across them.
- **Weather to go:** winds under 15 kt and seas under 1.5 m at the drop point, no gale forecast on the Stream for 72 hours, and **no strong northerly**: a north or north-east wind against the Gulf Stream raises steep breaking seas, the worst conditions the boat can meet on day one. The Ocean City plan's "offshore wind" rule was written for that coast. The equivalent for Hatteras needs the dead-boat drift tests re-run from the new point ([Naval_Review.md](Naval_Review.md)).
- **Escort:** stay with the boat for the first hour, until it is clearly holding course and both trackers have reported twice.
- **Early-failure recovery:** from 45 km out in the Stream, a boat that fails is carried north-east at 2–3 kn, away from the coast. That makes a recovery in the first week unlikely, unlike the Ocean City plan. This is the main thing given up, and it makes the coastal trial (Test F) matter more.
- **Drop procedure:**
  1. Power on and confirm a report from both trackers before leaving the dock.
  2. At the drop point, lower the boat by its lifting strop on the lee side with the charter boat stopped.
  3. Release it and escort it as above. Confirm the autopilot holds course and the next reports arrive.
  4. Log the time, position and photos.
- **Abort criteria:** no satellite report within 30 minutes, the boat won't hold course, or a leak alarm. Recover the boat and try again another day.

## Notices

None of these are permits for a vessel this size, as far as I can tell. They are notifications that avoid surprises and earn goodwill.

1. **US Coast Guard.** In 2026 the Coast Guard issued a safety alert after unmanned operations near port approaches began without notice. It asks operators to notify the cognizant Captain of the Port and the nearest Command Center before starting. Hatteras is in the **Sector North Carolina** Captain of the Port zone (Wilmington). Its Command Center has been listed as (910) 343-3880 **(confirm)**. Ask about a Local Notice to Mariners entry.
2. **Fisheries.** Cape Hatteras is the boundary between the Mid-Atlantic and South Atlantic fishery councils, so send a courtesy note to both and to the North Carolina Division of Marine Fisheries **(confirm the right contacts)**. The Hatteras charter fleet and marina notice boards reach the boats most likely to meet it on day one.
3. **United Kingdom.**
   - Send a courtesy email to HM Coastguard (Falmouth) and the Isles of Scilly harbour authority (St Mary's) before launch, and again when the boat is within ~50 nm, with live tracker links **(confirm addresses)**.
   - **Receiver of Wreck:** anyone who recovers the boat in UK waters, or brings it into the UK, must report it to the Receiver of Wreck within 28 days (Merchant Shipping Act 1995). The report is what gets it back to its owner. Tell the Receiver in advance that the boat is coming, and say so on the labels: row@mcga.gov.uk.
   - **Shipping:** traffic separation schemes lie off Land's End and round the Isles of Scilly. The boat can't follow the rule for crossing them, and the simulator has no model of ship traffic there. Aim for the west side of the Scillies and recover it before it reaches the lanes.
4. **France and Ireland.** A boat that misses Cornwall lands in Brittany or southern Ireland. Send the same courtesy note to CROSS Corsen (Brittany) and the Irish Coast Guard once the track shows which way it is going **(confirm)**.
5. **Microtransat (optional).** Entry is free. It requires a public tracker and an onboard position log at least every 6 hours. Our route isn't one of their standard start lines, so check whether they'd accept it **(confirm)**.

### Draft: Coast Guard notice (email)

> **Subject:** Notification: small unmanned research sailboat, departure ~25 nm SE of Hatteras Inlet NC, 1–20 May 2027
>
> We plan to release a 1.5 m unmanned autonomous sailboat (solar-powered, wing sail, about 29 kg) at approximately 34°57'N 075°21'W, about 25 nm south-east of Hatteras Inlet and south of Diamond Shoals, on one day between 1 and 20 May 2027. It will be escorted for the first hour, then sail and drift north-east with the Gulf Stream at 1–3 kn, bound for south-west England. It carries a radar reflector, high-visibility orange panels, labels and an all-round white light, and it reports its position by Iridium every 3 hours. Live track: [link]. Contact: [name, phone, email], 24/7 during the first week. Please advise whether you would like a Local Notice to Mariners entry or any other information.

### Draft: fishery note

> A small unmanned research sailboat (1.5 m, orange, wing sail, radar reflector) will be released on the Gulf Stream's edge south-east of Hatteras Inlet between 1 and 20 May 2027, heading north-east and then across to England. If you see it, please leave it be. It isn't adrift. If it is caught in your gear, please photograph it and contact [phone/email]; we'll arrange recovery and a reward. Live track: [link].

## Labels and marking

- **Both sides of the hull and the wing,** in large letters: "RESEARCH VESSEL – UNMANNED – PLEASE DO NOT REMOVE – IT IS NOT ADRIFT". Add a contact phone/email and "REWARD FOR REPORT". Repeat in French and Spanish for the European end. For a UK landfall add: "FOUND IN UK WATERS? REPORT TO THE RECEIVER OF WRECK (row@mcga.gov.uk) AND THE OWNER".
- **Colour:** fluorescent orange deck and wing panels (Microtransat suggests bright panels and warning labels).
- **Light:** the collision rules expect a sailing vessel under 7 m to show sidelights and a sternlight where practicable, or a white light. An all-round white LED at a few hundred milliwatts, switched on at night by the controller, is cheap power-wise. Add it to the power budget.
- **AIS:** a class B transponder needs a ship station licence and MMSI, and an AIS-SART is for distress only, so it can't be used as a tracking beacon. Skip AIS unless the power budget and licensing work out **(confirm with the FCC if wanted)**.

## Open questions

- **The drop point** (45 km, a point further east, or the inlet with a dog-leg): settled by the queued runs and by what a Hatteras skipper says.
- North Carolina: the boat has had no motor since Rev C, so state numbering should not apply **(confirm)**.
- Liability or third-party insurance for a drifting hull: worth one call to a marine insurer.
- Recovery in Cornwall or the Scillies: a local contact (a sailing club, the harbour office at St Mary's, a fisherman, or a Microtransat alumnus) willing to collect the boat.
- Customs: bringing the boat ashore in the UK is an import. Ask the Receiver of Wreck or HMRC what a recovered research instrument needs **(confirm)**.

## Sources

- Microtransat rules (collision precautions; position log every 6 hours; lights recommended): <https://sourceforge.net/p/microtransat/wiki/2021%20rules>, <https://sourceforge.net/p/microtransat/wiki/2016%20Rules>
- USCG safety alert on notice for unmanned operations (2026): <https://professionalmariner.com/safety-alert-lack-of-notice-for-unmanned-vessel-operations/>
- Sector North Carolina, Command Center number as published in 2015 and 2023: <https://ocracokeobserver.com/2015/05/18/coast-guard-to-temporarily-discontinue-navigation-aids-at-hatteras-inlet/>, <https://atlanticintracoastal.org/s/AIWA-Presentation_CAPT-List-Nov-23.pdf>
- Hatteras Inlet shoaling: <https://darenc.gov/departments/planning/grants-waterways/hatteras-inlet/hatteras-inlet-current-issues-impacts>, <https://waterwayguide-data.com/nav-alert/4-16594/nc-hatteras-inlet-channel-shoaling>, <https://dredgewire.com/dredging-needs-of-hatteras-inlet-discussed-at-waterways-commission-meeting/>
- Diamond Shoals: <https://en.wikipedia.org/wiki/Diamond_Shoals>, <https://www.dncr.nc.gov/blog/2023/12/05/diamond-shoals-b-41>, <https://www.lighthousefriends.com/light.asp?ID=1690>
- UK Receiver of Wreck (report within 28 days): <https://gov.uk/wreck-and-salvage-law>, <https://www.gov.uk/report-wreck-material>
- Land's End and Scilly traffic separation schemes: <https://www.pbo.co.uk/news/new-traffic-separation-scheme-for-lands-end-12040>
- NMFS / Saildrone notice to fixed-gear fishermen: <https://www.workboat.com/coastal-inland-waterways/noaa-says-keep-lookout-for-saildrones-cruising-gulf-of-maine>
