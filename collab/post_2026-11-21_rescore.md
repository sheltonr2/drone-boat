Hello Maya and team (posted by Claude at Randolph's request). Thank you for this morning's replies, and no apology needed. We're glad shared work is back on. Answers first, then a short update.

## Rev E1 for Bluewater

It's in our repo: [`designs/boat-sim/randolph_rev_e1.yaml`](https://github.com/sheltonr2/drone-boat/blob/main/designs/boat-sim/randolph_rev_e1.yaml). It's built from the Rev D file you already have, and the header lists every change.

What your format leaves out, as far as we can tell:

- **The bilge pump.** In our model a leak starts the pump and the boat keeps sailing. It only goes to SAFE once 1.0 kg of water is aboard with the pump running.
- **The tail detent.** A tail servo that lets go holds the fin at ±8° instead of flapping free. We approximated this by raising `steering_jam_share` to 0.9.
- **The limp-home backup controller** (from Rev D). It has its own GPS, compass and power, and takes over the starboard rudder and the tail if the main box dies.
- **The weed-shedding manoeuvre.** We approximated it with a faster `entangle_clear_per_day` (0.3).

The servo and weed figures are still guesses until our bench and tow tests. "Our model, not their simulator" is the right label.

## The Rev C5 re-score: how our 48.0% run was set up

1. **Drop point:** 38.32N 74.97W, the same as yours. So the nine boats back on the Maryland shore come from the route, not the drop. Our first leg heads east-north-east, out to sea (see 2).
2. **Route:** one waypoint at **42.0N 48.0W**, then the target at **51.35N 9.70W**, off Mizen Head. The waypoint keeps the boat south of the Grand Banks, which also keeps it well clear of Nova Scotia and Newfoundland.
3. **Waypoint rule:** a waypoint counts as reached within **25 km**. In that run it did *not* count once passed. Our "passed abeam also counts" rule came later, in the launch study.
4. **Land avoidance:** every 10 minutes the autopilot checks the chosen heading for land within **15 km** ahead. If there is land, it tries headings up to 180° either side, in 15° steps, and takes the first clear one that isn't too close to the wind. If none is clear, it feathers the wing. A boat with no land check on a straight line will meet Cape Sable, as yours did.
5. **Finish:** within **40 km** of the target, or any landfall in Europe (Natural Earth countries with CONTINENT = Europe). The Azores, Madeira and the Canaries don't count.
6. **What counts as a success:** an arrival while still reporting on the main link (33.6%) or tracked by the YB3 (14.4%), which makes **48.0%**. Arrivals that had gone silent (1.2%) or were drifting with no steering (5.6%) are *not* counted.
7. **Launches and weather:**
   - 250 voyages at random times between 1 May and 15 June 2023.
   - Weather: ERA5 winds, Copernicus SMOC currents and MFWAM waves, sampled on a 1° grid, with 0.25° in 30–50N, 80–38W.
   - Each voyage ends at 240 days or when our weather data runs out at the end of November 2023, which is close to your 30 November.
8. **Failures:** our "planning" rate set, with the Rev C5 structural model on.

The full scenario is [`collab/bulk_mc_2023_10km.json`](https://github.com/sheltonr2/drone-boat/blob/main/collab/bulk_mc_2023_10km.json), over the defaults in [`simulator/drone_sim/sim.py`](https://github.com/sheltonr2/drone-boat/blob/main/simulator/drone_sim/sim.py). The autopilot's route and land logic is in [`autopilot.py`](https://github.com/sheltonr2/drone-boat/blob/main/simulator/drone_sim/autopilot.py).

**Hatteras to Cornwall:** not needed for the C5 re-score. The Ocean City set-up is the one that matches our 48.0%. If you later want to run Rev E1 on our current route, here it is:

- Drop at 34.95N 75.35W.
- Waypoints at 35.0N 74.9W, 42.0N 48.0W, 49.6N 7.2W, 49.7N 6.4W and 49.83N 5.8W, each counted once passed abeam.
- A holding point in the Lizard offing at 49.85N 5.20W.

Our figures for that route are 88.4% for Rev E1 arriving within 40 km of Scilly, and 76.4% reaching the Lizard hold.

## Our news since 19 Nov

- **Decisions (18 Nov):**
  - launch window 1–20 May 2027;
  - holding point in the Lizard offing;
  - two extra waypoints that keep the boat well clear of Scilly on the approach. Boats passing within 1 km of Scilly fell from 12.0% to 3.0%.
  - The east-to-west backup now launches from Mindelo for a March arrival in the BVI.
- **Build files (Rev E2):** a design-for-manufacture pass, so the boat can be built by a hobbyist:
  - 28 drawing sheets, including wiring, laminates, hardware and a print guide;
  - 34 printable STL files;
  - a full bill of materials with purchase links, about $4,870 in total.
  - The details are in [`build-files/`](https://github.com/sheltonr2/drone-boat/tree/main/build-files) and [`docs/DFM_Review.md`](https://github.com/sheltonr2/drone-boat/blob/main/docs/DFM_Review.md).
- **A 3D model** of the whole boat and every printed part, which runs in a browser: [`build-files/viewer/`](https://github.com/sheltonr2/drone-boat/tree/main/build-files/viewer). Serve the folder locally to open it. You're welcome to use it for Bluewater's Rev E1 model, and the hull and foil shapes come straight from our `design.py`.

Thank you also for the Bluewater fixes (#646) and the traffic-density grid. We'll look at the sailing screen again when we can and tell you here.
