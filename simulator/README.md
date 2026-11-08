# Solar-Sail Drone Simulator

A voyage simulator for the 1.5 m solar-and-sail ocean drone, with real historic weather, waves,
ocean currents and tides. You can change the design (hull, keel, bulb, rudder, wing, tail, power)
or upload a whole new design, then run single voyages or hundreds of Monte Carlo runs to estimate
the odds of reaching Europe.

## Install and start (Windows)

1. Install Python 3.10 or newer from python.org and tick **"Add python.exe to PATH"**.
2. Unzip this folder somewhere, for example `Documents\drone_sim`.
3. Double-click **`setup_windows.bat`** (one time; installs numpy into a private `.venv`).
4. Double-click **`run_simulator.bat`**. Your browser opens at http://127.0.0.1:8765.

On macOS or Linux, run `./run_simulator.sh`.

Everything runs on your computer. Weather data is downloaded on demand from Open-Meteo (free, no account or key)
and cached in `workspace/cache`, so repeat runs over the same dates are fast and work offline.

## The four tabs

1. **Design**: sliders for every main dimension, plus buttons to save and load designs and upload an STL or OBJ model.
   The page shows mass, waterline, stability (righting-arm curve, self-righting check), the rig counterweight,
   a speed polar, a mass breakdown and a cost estimate, with a to-scale side and plan view.
2. **Voyage**: click the map to set the start, target and waypoints, then pick the start date and time, data source,
   physics model, failure rates and a schedule of commands from shore (`SET_ROUTE`, `GOTO`, `MODE`,
   `SET_REPORT`, `THRUSTER_POLICY`, `GEOFENCE`, `DIAG`, `REBOOT`).
3. **Run**: runs one voyage, showing the track coloured by speed, events and failures, and charts of speed and wind,
   waves and heel, battery and solar, and currents and tide. You can export the result as JSON.
4. **Odds (Monte Carlo)**: runs many voyages with new failure draws and random start dates inside a window
   (for example June of 2022 to 2025). It reports the success rate with a 95% range, the distribution of
   crossing times, what ended the failed runs, and every track on the map.

## Data

| Source | Variables | Period |
|---|---|---|
| Open-Meteo Historical Weather API (ERA5) | 10 m wind and gusts, shortwave radiation, cloud, air temperature | 1940 to a few days ago |
| Open-Meteo Marine API | wave height, period and direction; swell; ocean current (Eulerian + waves + tides); sea level incl. tides; sea-surface temperature | waves since 1940; **currents and tides since January 2022** |
| Natural Earth 1:50m land | coastline for landfall and avoiding land | downloaded once; a coarse built-in outline is the fallback |

Start dates must be January 2022 or later for currents and tides. **Synthetic** weather is an offline test mode only.
It produces realistic-looking but invented North Atlantic weather.

## Physics

**Hybrid model (default).** At each step (default 5 minutes) the boat sits in force and moment equilibrium
(a velocity prediction program). Surge, sway, yaw and heel are solved together with:

- a finite-span foil model for the wing, keel and rudder, valid through stall and reverse flow;
- ITTC-57 friction, wave-making resistance and added resistance in waves;
- hull windage;
- a wind gradient and wave-trough sheltering;
- the exact righting-arm curve from the 3D geometry.

The results are tabulated into a polar over wind speed, wind angle, wave height and fouling drag. On top of the polar it adds:

- heading dynamics;
- currents and Stokes drift;
- breaking-wave knockdowns and capsize, using the boat's own stability curve;
- the autopilot, power, satellite and failure models.

A 100-day crossing takes about 5 seconds.

**Full 6-DOF model.** This integrates rigid-body motion every 0.05 s, plus the free-rotating wing as a 7th degree of freedom, in an
irregular directional JONSWAP sea built from each hour's wave data. The forces are:

- exact submerged volume and centroid of the hull and appendages under the local sea surface;
- Froude-Krylov forces, added mass and radiation damping;
- strip-theory lift and drag on the keel, rudder, wing and tail, using local wind, current and wave-orbital flow. The wing
  works as a hydrofoil when it is knocked into the water;
- servo-driven rudder and tail with real control loops.

Breaking waves hit the boat as roll impulses, and the physics decides whether it recovers. Expect roughly
**0.5 hours of computer time per simulated day**. Use it for storms or a few days at a time, and use Hybrid for crossings and Monte Carlo.

**Other models.** These are shared by both physics models:

- Autopilot: VMG-optimal tacking and gybing, land and geofence avoidance, storm, safe and drift modes.
- Power: solar from measured irradiance, heel and capsize; loads; cold-charge cutoff.
- Iridium: credits, failed sessions in heavy seas or when knocked down, commands delivered at the next good session.
- Failures: leaks, servo jams, fouling, weed and fishing line, collisions, capture near land, electronics, software hangs.
  Every hazard rate is editable on the Voyage tab.

## Uploading new designs

- **Design file (.json)**: everything on the sliders plus masses, equipment positions, power and costs. Save one from the
  Design tab and edit it.
- **STL or OBJ**: choose **Hull only** (replaces the parametric hull) or **Whole boat** (replaces hull, keel, bulb and rudder volumes).
  Pick the units and axes. The mesh must be watertight; the page warns you if it is not.
  For a whole-boat mesh, enter the total mass. The foil sliders still set the keel, rudder and wing areas used for lift.

## Command line

```
python -m drone_sim.cli selftest                                   # check geometry, physics and Open-Meteo access
python -m drone_sim.cli voyage --scenario my_scenario.json
python -m drone_sim.cli mc --scenario my_scenario.json --runs 200 --from 2022-06-01 --to 2022-06-30 --years 2022,2023,2024,2025
```

## Limits (read before trusting a number)

- Resistance, added resistance, wave sheltering and hazard rates are engineering estimates. None have been checked
  against this boat. Calibrate them with lake and coastal trial data: speeds, power use and roll motions.
- The 6-DOF model uses a locally planar sea surface (good for waves much longer than the boat). It does not
  model green water on deck or slamming; breaking waves are modelled as impulses.
- Open-Meteo marine data is about 8 km resolution and not meant for coastal navigation. Near harbours,
  tidal streams can be stronger than the model shows.
- Failure odds depend almost entirely on the hazard rates you enter. Treat Monte Carlo results as
  "how sensitive is success to X", not as a forecast.

## Results viewer

`drone_sim/static/results_viewer.html` is a standalone page: open it in any browser (no server needed) and drop in a results `.json` exported from the Run or Monte Carlo tab (or written by the command line) to view and share the track, charts and odds.

## Calibrating with field tests

`python -m drone_sim.calibrate predict` prints what the model expects from the tow and inclining tests in
[docs/Field_Tests.md](../docs/Field_Tests.md). Feed your measurements back with
`python -m drone_sim.calibrate tow ...` (fits the hull drag factor) and `python -m drone_sim.calibrate incline ...`
(measures GM). Solar losses (salt, charge controller, wiring, hot cells) are set under `"power"` in the design file
and marked GUESS until the solar-day test is done. The Monte Carlo now reports the odds for each launch month.
