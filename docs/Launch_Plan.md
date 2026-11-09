# Launch plan: Ocean City, 100 km drop, 1–20 May window

*Draft, 9 November 2026. It ties together the simulator's launch findings and the paperwork. Contact details and rules change, so confirm each one when you act on it. Items marked **(confirm)** are ones I couldn't verify.*

## Why these choices

| Decision | Choice | Evidence |
|---|---|---|
| Launch window | **1–20 May**, earliest suitable weather day | Tropical-cyclone exposure rises from ~5% (May) to 17% (June) of voyages ([Hurricane_Risk.md](Hurricane_Risk.md)). April has almost no storm risk, but the Gulf Stream crossing is colder and rougher, so treat it as a fallback |
| Drop point | **~100 km (54 nm) ESE of Ocean City, 38.02°N 74.01°W**, inshore of Baltimore Canyon | In real-weather drift tests, 3 of 4 dead boats dropped 25 km out went ashore within 5 days. Re-run pending with the new leeway model ([Route_MidAtlantic.md](Route_MidAtlantic.md)) |
| Before launch | **3-week coastal trial passed** (Field Test F) and **second tracker fitted** | These two items are worth the most odds per dollar ([Failure_Rates.md](Failure_Rates.md) §5) |

## Timeline

| When | What |
|---|---|
| **Now – Jan** | Build per the [Build Plan](Build_Plan.md). Fit and bench-test the backup tracker ([Backup_Tracker.md](Backup_Tracker.md)). Order the labels |
| **Feb** | Field tests A–E (tow, inclining, self-righting, wing balance, solar day). Spar proof-load test ([Storm_Loads.md](Storm_Loads.md)) |
| **Mar – mid-Apr** | Field Test F, the 3-week coastal trial: 14 days in a row with no unexplained reboot, leak or reporting gap. Freeze the firmware afterwards |
| **By 1 Apr** | Book the charter (below). Send the Coast Guard, fishery and Irish notices (drafts below) |
| **20–30 Apr** | Final prep: charge, desiccant change, both trackers reporting, photos and serial numbers on file, last software check |
| **1–20 May** | Launch on the first day that meets the weather criteria |
| **During** | Daily check of both trackers. Weekly summary to the Microtransat list, if entered, and to the collaboration thread |
| **Arrival** | Notify the Irish Coast Guard when within ~50 nm. Arrange recovery or a finder's contact |

## Charter and drop

- **Boat:** an Ocean City offshore sportfishing charter. Canyon trips to the shelf-edge canyons (Baltimore, Washington, Poor Man's) are a staple there, and 54 nm should be within their normal range **(confirm distances with the captain)**. Ask for a half-day "drop and return" or ride along on a canyon trip. Budget roughly a half-to-full-day offshore charter rate **(confirm locally; prices vary a lot by boat)**.
- **Weather to go:** forecast winds under 15 kt and seas under 1.5 m at the drop, and no gale on the shelf for 72 hours. A westerly or northwesterly component is ideal, because it pushes the boat offshore.
- **Drop procedure:**
  1. Power on and confirm a report from both trackers before leaving the dock.
  2. At the drop point, lower the boat by its lifting strop on the lee side with the charter boat stopped.
  3. Release the boat and watch it sail away for 10 minutes. Confirm the autopilot holds course and the next reports arrive.
  4. Log the time, position and photos.
- **Abort criteria:** no satellite report within 30 minutes, the boat won't hold course, or a leak alarm. Recover the boat and try again another day.

## Notices

None of these are permits for a vessel this size, as far as I can tell. They are notifications that avoid surprises and earn goodwill.

1. **US Coast Guard (Captain of the Port and Local Notice to Mariners).** In 2026 the Coast Guard issued a safety alert after unmanned operations near port approaches began without notice. It asks operators to notify the cognizant Captain of the Port and the nearest Command Center before starting, following its Unmanned, Autonomous and Remote-Control Operations Work Instruction. For waters off Ocean City, ask District 5 which Sector covers the drop point **(confirm)**. A District 5 Local Notice to Mariners contact listed by WHOI is (757) 398-6486.
2. **Fisheries.** Send a courtesy note to the Mid-Atlantic Fishery Management Council and NOAA's Greater Atlantic Regional Fisheries Office. NMFS used this route to warn fixed-gear fishermen about Saildrones in the Gulf of Maine. Ocean City marina notice boards and the local charter captains' association reach the boats most likely to meet it.
3. **Ireland.** Send a courtesy email to the Irish Coast Guard (MRCC Dublin) and the Marine Institute before launch, and again when the boat is within ~50 nm, with live tracker links.
4. **Microtransat (optional).** Entry is free. It requires a public tracker and an onboard position log at least every 6 hours. Our route isn't one of their standard start lines, so check whether they'd accept it **(confirm)**.

### Draft: Coast Guard notice (email)

> **Subject:** Notification: small unmanned research sailboat, departure ~54 nm ESE of Ocean City MD, 1–20 May 2027
>
> We plan to release a 1.5 m unmanned autonomous sailboat (solar-powered, wing sail, about 21 kg) at approximately 38°01'N 074°01'W on one day between 1 and 20 May 2027. It will sail east at 1–2 kn toward south-west Ireland and will be in the area for about two days. It carries a radar reflector, high-visibility orange panels, labels and an all-round white light, and it reports its position by Iridium every 3 hours. Live track: [link]. Contact: [name, phone, email], 24/7 during the first week. Please advise whether you would like a Local Notice to Mariners entry or any other information.

### Draft: fishery note

> A small unmanned research sailboat (1.5 m, orange, wing sail, radar reflector) will cross the shelf east of Ocean City between 1 and 20 May 2027, heading for Ireland. If you see it, please leave it be. It isn't adrift. If it is caught in your gear, please photograph it and contact [phone/email]; we'll arrange recovery and a reward. Live track: [link].

## Labels and marking

- **Both sides of the hull and the wing,** in large letters: "RESEARCH VESSEL – UNMANNED – PLEASE DO NOT REMOVE – IT IS NOT ADRIFT". Add a contact phone/email and "REWARD FOR REPORT". Repeat in French, Spanish and Irish for the European end.
- **Colour:** fluorescent orange deck and wing panels (Microtransat suggests bright panels and warning labels).
- **Light:** the collision rules expect a sailing vessel under 7 m to show sidelights and a sternlight where practicable, or a white light. An all-round white LED at a few hundred milliwatts, switched on at night by the controller, is cheap power-wise. Add it to the power budget.
- **AIS:** a class B transponder needs a ship station licence and MMSI, and an AIS-SART is for distress only, so it can't be used as a tracking beacon. Skip AIS unless the power budget and licensing work out **(confirm with the FCC if wanted)**.

## Open questions

- Maryland DNR: does a boat with an electric thruster, launched in federal waters, need state numbering? **(confirm)**
- Liability or third-party insurance for a drifting hull: worth one call to a marine insurer.
- Recovery in Ireland: a local contact (yacht club, Marine Institute or a Microtransat alumnus) willing to collect the boat.

## Sources

- Microtransat rules (collision precautions; position log every 6 hours; lights recommended): <https://sourceforge.net/p/microtransat/wiki/2021%20rules>, <https://sourceforge.net/p/microtransat/wiki/2016%20Rules>
- USCG safety alert on notice for unmanned operations (2026): <https://professionalmariner.com/safety-alert-lack-of-notice-for-unmanned-vessel-operations/>
- District Local Notice to Mariners contacts (WHOI): <https://www.whoi.edu/?p=13290>
- NMFS / Saildrone notice to fixed-gear fishermen: <https://www.workboat.com/coastal-inland-waterways/noaa-says-keep-lookout-for-saildrones-cruising-gulf-of-maine>
