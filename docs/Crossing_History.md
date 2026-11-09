# History of small autonomous ocean crossings

*Compiled 8 November 2026 for the drone-boat / boat-sim collaboration (our half of the agreed work split). Machine-readable version of the Microtransat table: [`docs/data/crossing_attempts.csv`](data/crossing_attempts.csv). Failure rates derived from it: [`Failure_Rates.md`](Failure_Rates.md).*

## Bottom line

- **Between 2010 and 2023, 1 of 37 Microtransat attempts finished.** That was SailBuoy's *SB Met* in 2018, which sailed Newfoundland to Ireland in 79.5 days. A second boat, *OpenTransat* (2019), physically crossed in 186 days but went silent near Valentia, outside the finish zone. The first finish in the sailing class came in September 2026, when Oshen's *C-Star PC13* (1.2–1.3 m, 56 kg) sailed Gran Canaria to Barbados in 127 days. It was Oshen's third attempt.
- **Most boats are lost in the first week, close to land.** Half of all Microtransat attempts had ended by day 7. The usual killers near the coast are tidal groundings, being picked up by fishermen, and going silent.
- **Offshore, the boats die slowly.** Once past about 150 km from land, the record shows about **0.013 mission-ending events per day** (95% CI 0.006–0.025). The main causes are rig or weather damage, the boat going silent (often after steering erratically first), and antenna faults.
- **Professional vehicles of similar size have now crossed.** Seasats' *Lightfish* (3.7 m, solar-electric, US Navy) took 62–63 days from South Carolina to Portugal in 2025. *SD 1021* (Saildrone, 7 m) took 75 days from Bermuda to the UK in 2019, after a Gulf Stream storm had rolled it and broken its wing. These crossings succeeded because of redundancy, a shakedown, and help from the operators on shore. Luck was not the reason.
- **For us:** our boat is in the Microtransat size class, and so is its main risk: the boat sailing on, but silently, in the first two weeks. We are launching from the US Mid-Atlantic coast, so we cross a busy fishing shelf (scallop, longline and trawl grounds) for the first 2–4 days. The USNA boats that left Cape Cod show this is where boats get caught or picked up.

## 1. Microtransat Challenge, 2010–2023 (official record)

The Microtransat is the reference dataset for our class. It is open to boats up to 2.4 m with no human help after launch. Boats can sail east to west (Europe to the Caribbean or North America) or west to east (Newfoundland, Nova Scotia or New England to Europe). The table below comes from the official history page. We added causes from team reports where the page gives them. "Days" means days until the last report.

| # | Year | Boat (team) | Launched from | Days | Track km | How it ended |
|---|---|---|---|---|---|---|
| 1 | 2010 | Pinta (Aberystwyth Univ.) | Valentia, Ireland | 18.0 | 653 | Computer failed after 87 km under autonomy; drifted, then lost |
| 2 | 2011 | Breizh Spirit (ENSTA Bretagne) | Brest, France | 8.0 | 194 | Sail damage; recovered at sea |
| 3 | 2012 | Breizh Spirit DCNS (ENSTA Bretagne) | France | 4.7 | 229 | Reports stopped; washed ashore in Ireland weeks later |
| 4 | 2012 | Snoopy Sloop 8 (Team Joker) | Barton-on-Sea, UK | 0.3 | 12.5 | Hit a rocky beach, Isle of Wight |
| 5 | 2013 | Erwan 1 (École Navale) | Brest, France | 4.2 | 220 | Transmissions stopped; picked up by a passing boat |
| 6 | 2013 | Snoopy Sloop 9 (Team Joker) | Barton-on-Sea, UK | 0.6 | 28 | Ashore, Isle of Wight |
| 7 | 2014 | ABoat Time (US Naval Academy) | Cape Cod, MA | 5.5 | 408 | Caught in a scallop dredger's net |
| 8 | 2014 | Snoopy Sloop 9 | Barton-on-Sea, UK | 1.0 | 62 | Ashore, Isle of Wight |
| 9 | 2014 | Snoopy Sloop 9 | Boscombe, UK | 2.4 | 185 | Ashore, Portland |
| 10 | 2015 | Snoopy Sloop 10 | Boscombe, UK | 12.4 | 853 | Never left the Channel; ashore at Brighton |
| 11 | 2015 | ABoat Time (USNA) | Cape Cod, MA | 9.4 | 477 | Software bug; aground in Nova Scotia |
| 12 | 2015 | Breizh Tigresse (ENSTA/Dalhousie) | Halifax, NS | 32.3 | 1,427 | Steered erratically, then lost |
| 13 | 2016 | That'll Do (Epsom College) | off Salcombe, UK | 4.9 | 374 | Went silent; found ashore flooded, keel sheared off |
| 14 | 2016 | ABoat Time (USNA) | Cape Cod, MA | 6.0 | 324 | Taken by a fishing boat |
| 15 | 2016 | Trawler Bait (USNA) | Cape Cod, MA | 15.8 | 433 | Storm damaged the sail and wind sensor; recovered |
| 16 | 2016 | OpenTransat (A. Osusky) | Newfoundland | 25.0 | 898 | Went silent; never found |
| 17 | 2016 | Snoopy Sloop 10 | Boscombe, UK | 0.9 | 84 | Lost; never found |
| 18 | 2016 | Gortobot V2 (C. Gorton) | Gloucester, MA | 8.0 | 361 | Went silent; found in the Azores 9 months later |
| 19 | 2017 | SB Wave (SailBuoy) | Newfoundland | 68.9 | 4,682 | Antenna fault sent it into failsafe; picked up by a fishing boat |
| 20 | 2017 | ABoat Time (USNA) | Cape Cod, MA | 2.8 | 263 | Taken by a fishing boat |
| 21 | 2017 | Trawler Bait (USNA) | Cape Cod, MA | 39.1 | 2,113 | Lost its wind sensor in a gale; picked up by a fishing boat |
| 22 | 2017 | Phil's boat (P. Smith) | Chesil Beach, UK | 7.0 | 267 | Picked up by a fishing boat |
| 23 | 2018 | **SB Met (SailBuoy)** | Newfoundland | **79.5** | **5,354** | **Finished (first Microtransat finish)** |
| 24 | 2018 | That'll Do Two (Epsom College) | Isle of Wight | 4.5 | 365 | Went silent |
| 25 | 2018 | Sea Leon (Dalhousie) | Sydney, NS | 76.1 | 3,763 | Steered erratically, then lost; found in Ireland 2019 |
| 26 | 2018 | Gortobot v3 | Halibut Point, MA | 10.2 | 828 | Aground on Nantucket |
| 27 | 2019 | Snoopy Sloop 11 | Boscombe, UK | 6.9 | 848 | Taken by a fishing boat, Lulworth |
| 28 | 2019 | OpenTransat (A. Osusky) | Newfoundland | 185.8 | 6,041 | Crossed; went silent near Valentia, outside the finish zone; wing found in France |
| 29 | 2019 | EC Crossing (Epsom College) | off Selsey, UK | 3.2 | 277 | Contact lost |
| 30 | 2019 | Gortobot v4 | Halibut Point, MA | 2.3 | 143 | Sail motor failed; withdrawn |
| 31 | 2020 | Phil's Boat (P. Smith) | Chesil Beach, UK | 51.4 | 1,748 | Damaged; withdrawn; found in France 2021 |
| 32 | 2020 | Brave Puffin (S. Asipenko) | Cape Cod, MA | 82.8 | 2,138 | Comms lost |
| 33 | 2020 | Bearly Assailable (USCG Academy) | Cape Cod, MA | 45.7 | 2,091 | Hit by Tropical Storm Kyle |
| 34 | 2020 | Endeavour (Epsom College) | Chesil Beach, UK | 11.6 | 577 | Ashore on Jersey |
| 35 | 2021 | Return to Sender (Epsom College) | Cornwall, UK | n/a | n/a | Aground on Scilly; later recovered in Spain |
| 36 | 2022 | Snoopy Sloop 11 | Boscombe, UK | n/a | n/a | Tracker stopped |
| 37 | 2023 | Phloat (P. Smith) | Chesil Beach, UK | ~42 | n/a | Fault; sent home and recovered near Poole |

**2026:** Oshen's *C-Star PC13* left Gran Canaria on 7 May and finished east of Barbados on 13 September (127 days, 2,926 nm). On about day 113 it sailed through a developing low linked to Tropical Storm Dolly, and it diagnosed and worked around its own rudder problems along the way. Oshen's two earlier boats had failed on waterproofing, durability and component faults. One of them sailed from Plymouth for 277 days and covered about three quarters of the distance before a storm destroyed its sail. Oshen also sent a sister boat, *PC8*, into the eyewall of Hurricane Humberto for NOAA in 2025.

### What the Microtransat record says (analysis in `docs/data/hazard_analysis.py`)

| Measure | All attempts (35 with a duration) | West-to-east only (17), our direction |
|---|---|---|
| Still sailing and reporting after 3 days | 80% | 88% |
| … after 7 days | 54% | 76% |
| … after 14 days | 37% | 59% |
| … after 30 days | 29% | 47% |
| … after 60 days | 14% | 29% |
| … after 90 days | 4% | 9% |

How the 33 failed attempts with a published duration ended:

| Cause | Near land (<~150 km) | Open ocean | Notes |
|---|---|---|---|
| Went silent, cause unknown | 7 | 2 | Also 2 offshore boats that steered erratically before going silent |
| Ran aground (tide or navigation) | 7 | 0 | Mostly English Channel launches. Our simulator models this physically and does not use a hazard rate for it |
| Taken or caught by fishermen | 5 (4 taken, 1 netted) | 0* | *Two offshore boats were picked up after another fault had already disabled them |
| Rig or weather damage | 2 | 3 | Includes TS Kyle (2020) |
| Electronics, software, actuators, flooding | 4 | 1 (antenna) | Flooding: That'll Do, keel sheared off |

Three things about this data matter for how we use it:
1. **Survivor bias the other way.** Microtransat boats are mostly student and hobby builds with little sea time before launch. That makes the record a **pessimistic bracket** for a careful build. It is not a forecast for us.
2. **"Went silent" hides the real cause.** In the Global Drifter Program, 68% of drifters that die simply stop transmitting (Lumpkin et al. 2012). Silence is the normal way a small floating electronics package dies, and the root cause is usually power, comms or water getting in. Some silent boats are also picked up and switched off. *That'll Do* went silent and was later found flooded.
3. **Phase matters more than total days.** In the record, the near-land hazard is about 9 times the open-ocean hazard (0.116 vs 0.013 per day). A boat that survives the first week is a much better bet than the raw 1-in-37 suggests.

## 2. Other autonomous and unmanned crossings

| Year | Vehicle | Type, size | Route | Result | Lesson for us |
|---|---|---|---|---|---|
| 2009 | RU27 *Scarlet Knight* (Rutgers) | Underwater glider | New Jersey → Spain | Crossed in 221 days | Long missions are possible with slow, low-power vehicles |
| 2011–13 | Wave Glider PacX (Liquid Robotics) | Wave-powered surface vehicle, 4 launched | San Francisco → Australia / Japan | 2 of 4 reached Australia (one after servicing in Samoa); 1 rescued; 1 left drifting | 50% on a professional product. Barnacles grew wherever there was no antifouling. Storms with 26 ft waves and 60 kn winds |
| 2013 | *Scout* (student team) | Solar powered | Rhode Island → Spain | Covered 1,300+ mi, then comms lost | Earlier attempts ended with a servo failure |
| 2012–14 | Educational Passages miniboats | 1.5 m, no autopilot, GPS tracker only | Launched in the Gulf Stream | Many reach Europe (e.g. *Crimson Tide*: South Carolina, Dec 2012 → Guernsey, Feb 2014; *Inspiration*: Rhode Island shelf break → UK after 245 days, 2022). Some loop in the gyre or come ashore in Nova Scotia | A boat that only drifts and sails downwind reaches Europe slowly but often. This is our "dead boat" baseline |
| 2015–16 | *Solar Voyager* | Solar kayak | Gloucester, MA → Portugal | First attempt failed early; 2016 attempt **caught in a fishing net** and recovered by the Canadian Navy | Fishing gear catches boats offshore too, not just near the coast |
| 2016 | *SeaCharger* | Solar | California → Hawaii → New Zealand | Reached Hawaii in 41 days; on the leg to NZ the rudder/propeller failed a few hundred km short, after ~155 days | Wear-out failures in steering show up after about 100 days |
| 2019 | Saildrone *SD 1021* | 7 m wing sail | Bermuda → UK (75 d), UK → Newport (68 d) | Both crossings succeeded. Earlier, in February, a 58 kn Gulf Stream storm with 12 m seas rolled it and broke its wing; backup systems got it to Bermuda for a new wing | **The Gulf Stream in winter breaks wings, even on 7 m professional boats.** Redundancy is what saved it |
| 2021–24 | NOAA–Saildrone hurricane missions | 7 m, 5–12 vehicles a year | Tropical Atlantic | Vehicles survived hurricanes, including Cat 4 *Sam*, and SD 1045 was redeployed in 2023 | A purpose-built rig can survive the eyewall, but our 1.5 m boat is not that rig |
| 2025 | *Lightfish* (Seasats, US Navy) | Solar-electric, 3.7 m, ~136 kg | Sullivan's Island, SC → Tróia, Portugal | 62–63 days, launched 30 June 2025; arrived with barnacles and needing minor repairs and fuel for its generator | Closest analogue to our route. Iridium **plus** Starlink, AIS, cameras, and active operators |
| 2026 | Oshen *C-Star PC13* | Sail, 1.2–1.3 m, 56 kg | Gran Canaria → Barbados | 127 days, finished | Same size class as us. Success came on the third try, after fixing waterproofing and durability |

## 3. Patterns that matter for our design and operation

1. **Shake the boat down before the crossing.** The successful vehicles (Saildrone, SailBuoy, Lightfish, Oshen PC13) all came from teams with long sea time on the same hardware, and Oshen succeeded only on its third boat. Most Microtransat failures in the first week look like infant-mortality failures: seals, integration bugs, and navigation code that had never seen a tide. **We add Field Test F: a 14–30 day moored or coastal shakedown** (see `Failure_Rates.md` §5).
2. **Get off the shelf fast and keep away from fishermen.** In the record, fishermen took or caught a boat about once every 45 near-land days, and the USNA boats leaving Cape Cod lost three of six attempts this way. The simulator now applies this hazard out to ~150 km from land. Countermeasures include a large "research vessel, do not remove" label with a contact number, a notice through the regional fishery council (NMFS did this for Saildrone's Gulf of Maine survey), and an offshore drop point.
3. **Plan for the silent boat.** Comms is the most common single point of failure. Our build already has a backup D-cell on the comms rail and a watchdog. Next steps would be a second, independent tracker with its own battery and antenna, which is cheap insurance for the "silent but sailing" case, and logging the reason for every reboot.
4. **Rig damage in storms is the main open-ocean killer.** Our route crosses the Gulf Stream and runs about 100 days through the spring and summer North Atlantic. The wing, mast bearing and tail are the parts to over-design, and knockdown testing (Field Test C) should include a mast-in-water load case.
5. **Steering wear shows up after about 100 days.** SeaCharger's steering failed after about 155 days, and PC13 had to cope with rudder problems. Over 100+ days, servo choice and sealing matter. A rudder that fails centred, so the wing can still drive the boat downwind, is a cheap and valuable feature.
6. **Hurricane season sits in the second half of a May launch.** *Bearly Assailable* (August launch from Cape Cod) was hit by TS Kyle, and *PC13* met a system linked to TS Dolly around day 113. With a May launch we should be east of 40°W by July, which is where the HURDAT2 work (next task) needs to put numbers on the risk.

## Sources

- Microtransat Challenge, official history (all 2010–2023 attempts): [microtransat.org/history.php](https://www.microtransat.org/history.php)
- Oshen *C-Star PC13*: [Ocean News](https://oceannews.com/news/science-technology/oshens-c-star-pc13-becomes-first-autonomous-vessel-to-cross-the-atlantic-unaided/); [Yacht.de](https://www.yacht.de/en/yachts/small-cruiser/microtransat-challenge-c-star-pc13-became-the-first-autonomous-robotic-boat-to-cross-the-atlantic/); [Science Times](https://www.sciencetimes.com/articles/62633/20260922/robotic-sailboat-crosses-atlantic-after-traveling-5400-kilometers-without-human-intervention.htm); [Interesting Engineering](https://interestingengineering.com/transportation/tiny-autonomous-boat-crosses-atlantic-microtransat)
- Saildrone SD 1021: [fastest Atlantic crossing](https://www.saildrone.com/news/saildrone-completes-fastest-atlantic-crossing-unmanned-vehicle); [first east-to-west crossing](https://www.saildrone.com/news/first-autonomous-vehicle-atlantic-crossing-east-west)
- NOAA–Saildrone hurricane missions: [2023 blog](https://www.pmel.noaa.gov/usv-hurricane/2023/mission-blog-2023.html); [2024 mission](https://www.pmel.noaa.gov/usv-hurricane/2024/index.html); [AMS 2024 summary](https://ams.confex.com/ams/36Hurricanes/webprogram/Paper441830.html)
- Seasats *Lightfish*: [NIWC Atlantic / DVIDS](https://www.dvidshub.net/news/printable/551741); [NIWC Atlantic news](https://www.niwcatlantic.navy.mil/Media/News-Stories/Article/4340011/success-at-sea-unmanned-surface-vessel-completes-fastest-transatlantic-crossing/); [Defense News](https://www.defensenews.com/unmanned/2025/11/21/solar-powered-unmanned-surface-vessel-sets-new-speed-crossing-atlantic/); [AFCEA Signal](https://www.afcea.org/signal-media/us-navy-dives-deep-data-density)
- Educational Passages miniboats: [Crimson Tide](https://educationalpassages.org/boats/crimson-tide/); [URI GSO, *Inspiration*](https://web.uri.edu/gso/?p=176910); [CBC, Cape Breton wreck](https://www.cbc.ca/lite/story/1.6979128); [USS Constitution Museum, *Warrior* looping](https://ussconstitutionmuseum.org/2024/10/24/miniboat-loops-in-the-atlantic/)
- NMFS / Saildrone fishing-gear notice: [WorkBoat](https://www.workboat.com/coastal-inland-waterways/noaa-says-keep-lookout-for-saildrones-cruising-gulf-of-maine)
- Wave Glider PacX, Scout, Solar Voyager, SeaCharger, RU27: project and press reports gathered earlier in this work (see the reference list in `Failure_Rates.md`)
