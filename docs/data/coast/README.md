# Detailed coastlines and charted hazards (26 Nov 2026)

The simulator's default coastline is Natural Earth 1:50m. Near the launch and pickup points that is far too coarse. In it, Anegada, Jost Van Dyke, Norman and Peter Islands, the Isles of Scilly and the tip of the Lizard peninsula are missing altogether, and Tortola or St John are 6-to-9-point outlines. Scenarios can now set `detail_coast` (one file or a list) to use these files instead inside their boxes.

| File | Area | Built from |
|---|---|---|
| `detail_carib.json` | US and British Virgin Islands, 17.62–18.88N, 65.12–64.17W | OSM shoreline (248 islands, islets and rocks), 43 OSM reef areas (Horseshoe Reef included), NOAA ENC hazards: 1,202 depth areas under 1.8 m, 1,350 rocks, 56 wrecks, 347 obstructions |
| `detail_cornwall.json` | West Cornwall and Scilly, 49.78–50.55N, 6.55–3.95W | OSM shoreline: 1,888 islands, islets and rocks plus the mainland |
| `detail_hatteras.json` | Cape Hatteras and Diamond Shoals, 34.83–35.92N, 76.25–75.03W | OSM shoreline and NOAA ENC hazards: 426 depth areas under 1.8 m, wrecks and obstructions |

`make_detail_coast.py` rebuilds them from the raw downloads in this folder (`osm_coast_*.json`, `osm_reef_carib.json`, `noaa_enc_*.json`). The rules for what counts as a hazard for a 0.6 m-draft boat are in its `enc_hazards()`.

**Coverage gaps.** NOAA's charts cover the US Virgin Islands at harbour scale, but the BVI only on the 1:100,000 coastal chart, and nothing east of 64.42W (eastern Virgin Gorda and Anegada). There, the hazards come from OpenStreetMap's shoreline and reefs only. Cornwall has no free official vector charts. Its rocks come from OpenStreetMap, which maps most drying rocks as islets, plus the existing watch lines (Manacles, Runnelstone, Wolf Rock, Seven Stones). Free seabed depth grids that could fill these gaps: EMODnet DTM (about 115 m, European waters and parts of the Caribbean) and the UKHO ADMIRALTY Marine Data Portal (UK survey bathymetry and wrecks, Open Government Licence). GEBCO (about 450 m, global) is too coarse for shoals.

**Licences.** © OpenStreetMap contributors, ODbL 1.0. NOAA ENC Direct to GIS data are US Government work and **not for navigation**.
