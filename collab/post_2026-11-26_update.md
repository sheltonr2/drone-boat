(posted by Claude at Randolph's request)

@jcolter11374 Happy Thanksgiving to you, Maya and the whole Bluewater team! Here are the results we promised, and what's running next.

**Results in (runs 033–035, all on the PC that's back up):**
- **Westbound backup, four winters (2021–22 to 2024–25):** Mindelo, Cape Verde, still wins at **87.8%** (85.7–89.8), ahead of El Hierro at 81.9% and Gran Canaria at 78.4%, routed via 20N 28W. With four winters, all three gaps are outside the noise. Mindelo's median crossing is 85 days, and the boats that arrive in March launch around mid-December. ([`docs/East_West_Study.md`](https://github.com/sheltonr2/drone-boat/blob/main/docs/East_West_Study.md) section 12)
- **Rev E3 (two stock 10 W panels, 20 W in total) on the final eastbound plan:** 81.6% against Rev E1's 81.0% on the same 1,000 launches, with a median of 121 days for both. Half the solar costs nothing measurable.
- **Holding at the far end:** a tighter station-keeping deadband (1 km instead of 5 km) barely helps. At under 1 kn the boat can't stem the tidal streams off the Lizard, and still strays 20–30 km. So we're planning recovery around the arrival itself, not a long hold.

**A finding that may matter to your simulator too: the coastline.** Like many sims, ours used Natural Earth 1:50m. Near our launch and pickup points that turns out to miss a lot. It has no Isles of Scilly and no tip of the Lizard peninsula. In the Virgin Islands it has no Anegada, Jost Van Dyke, Norman or Peter Island, and Tortola and St John are 6–9-point outlines. We've added detailed local coastlines from OpenStreetMap and charted hazards from NOAA's free electronic charts. For the Virgin Islands that means drying and sub-1.8 m areas, rocks, wrecks and Horseshoe Reef; for Hatteras, the shoals and wrecks; for Cornwall, the shoreline only. Scenarios use them through a new `detail_coast` key, off by default; the files and sources are in [`docs/data/coast`](https://github.com/sheltonr2/drone-boat/tree/main/docs/data/coast). The same files would drop into Bluewater if your Hatteras or Cornwall coasts are coarse too.

**Running now (runs 036–039, about 9 hours):** a pickup-point study on the accurate coastlines. For the BVI there are seven candidates:
- south of Norman and Peter Islands (the current plan);
- further out, 18 km south;
- south-east of Ginger and Cooper Islands;
- north of Jost Van Dyke;
- west of Anegada;
- north of Anegada;
- north of St Croix.

Each gets the crossing from Mindelo, 14 days of holding and a dead-boat drift. Cornwall gets the same holding tests at four candidates, including two further offshore, and the whole eastbound plan is re-run on the accurate coasts. I'll post the results here, with a map.
