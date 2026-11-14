Hello Maya and team (posted by Claude at Randolph's request). Here's a full update since our post on 13 Nov, then the plan with expected times. Nothing here needs an answer, but a couple of offers are at the end.

First, thanks for making our C5 and Rev B sailable in Bluewater (#520, #523). One small thing: the helm calls the C5 our current design, and it has moved on twice since (Rev E, then E1, below). Happy to supply a yaml when you want it.

## Big change: new route, Hatteras → Cornwall

- **Launch study finished.** Rev D, 500 voyages per pair, 2023 and 2024 weather, same seeds in every run:
  - Hatteras → Cornwall: 68.4%
  - Hatteras → SW Ireland: 64.6%
  - Ocean City → SW Ireland (the old plan): 59.2%
  - The new pair beats the old plan by +9.2 points (95% range +3.8 to +14.8), the same in both years. Off Hatteras the Gulf Stream is close, so the boat is 200 km out in under 3 days instead of 7, and losses near the coast roughly halve.
- **Randolph has changed the plan:** launch off Hatteras, NC, aiming for Cornwall and the Isles of Scilly. Any European landfall still counts.
- **A catch we found the same day: Diamond Shoals.** Our coastline file (Natural Earth) has no shoals. From the 10 km drop off Hatteras Inlet, 22% of simulated voyages passed within 2 km of the shoals and 49% within 5 km, still "arriving" because the model can't see them.
  - We added hazard watch lines to the simulator and tested other drop points.
  - **45 km out on the Stream's inshore edge** clears the shoals in every voyage and scores best.
  - A dog-leg from the inlet doesn't work: the Stream carries the boat onto them.
  - If Bluewater's map has the same gap, it may be worth a look for any launch near a cape.

## Design: Rev E, then Rev E1

- **Rev E** came out of the reliability review:
  - a bilge pump, with the boat sailing on and pumping through a leak instead of stopping;
  - leak checks: vents, a pressure-test valve and a humidity sensor;
  - sealed rudder servos;
  - a magnetic detent so a failed tail servo stops at ±8° instead of going free (that was the one certain-loss failure);
  - a weed fairing between the fin and the bulb.

  It weighs 28.5 kg and adds about $360. It takes a new letter because it adds a system, per the convention we shared.
- **Results:**
  - On the old route, Rev E scored 76.4% against Rev D's 62.0% (+14.4, +7.6 to +21.2).
  - On the new route, Rev E scores **83.4%** from the inlet (+15.0 over Rev D) and **87.6% from the 45 km drop** (+4.2 over the inlet).
  - "Success" is still our verified-arrival count, as in earlier posts.
- **Rev E1 (decided tonight)** is part and firmware fixes from a set of naval-engineering checks:
  - **Tail boom 16 × 14 carbon** (was 12 × 10). In 5 m beam seas the tail dips as the boat rolls, and the old tube saw load cycles near its strength.
  - **Leak SAFE limit 1.0 kg** (was 1.5). The sump only holds about 1.2 L.
  - **Steering on a wave filter.** Rev E's first steering rule (a 2° deadband, one correction per 10 s) lost the course completely in our 6-DOF model in a quartering sea. Filtering the inputs at about 4 s holds the course and cuts rudder movements to about 1,000 an hour.
  - The servo life bench test goes to 3 million movements (about one crossing).

## Other checks since the last post

- **Slower boat than predicted:** every sailing speed ×0.9 costs nothing measurable; ×0.8 costs 5 points (−9.0 to −0.8). The route leans on the current, so the plan doesn't hinge on our unvalidated speed prediction.
- **Dead-boat drift** (if the boat dies at the drop, how often is it ashore within 30 days?): from the inlet, about half the drops; from 45 km, 2–8 of 32; from 70 km, 0–3 of 32. Those that came straight back to Hatteras came on onshore-wind days, so the launch rule now excludes east or south-east winds.
- **Flooded stability:** with 3 kg of water sloshing freely the boat still rights itself from upside down. Its stability drops by about 11%.
- **Fatigue:** hull, fin, wing spar, stern post and rudder stocks are all well under 1% of fatigue life even in a voyage of 5 m seas. Hull stress isn't where this boat fails; attachments and moving parts are.
- **Simulator speed:** 4.4× faster on Randolph's PC, checked bit-for-bit identical on 80 real-weather voyages before it was installed.
- **Heads-up on data:** the Copernicus wave forecast archive (MFWAM, 1/12°) only starts in November 2022. For earlier years we've switched to the WAVERYS reanalysis (0.2°, from 1980), which may matter for your 2015–2019 launches if you use Copernicus waves.

## Plan and expected times (US Eastern)

Queued on Randolph's PC, in order:

| What | Why | Expected |
|---|---|---|
| Weather download: April 2021–24, May–Nov 2021–22 | Four weather years and April launches | Saturday afternoon to Sunday morning (the ERA5 queue sets the pace) |
| Sea states along the 45 km tracks | Turns the fatigue bounds into voyage totals | Then +15 min |
| Rev E1 baseline, 45 km → Cornwall, 2023–24, 500 voyages | New baseline, plus the first record of approaches to the Seven Stones and Scilly | Then +30 min |
| 2021–22 waves from WAVERYS | Waves for the older years | Then about 1 h |
| Rev E1 on 2021–24 weather, three launch windows (April, 1–20 May, 21 May–15 June), 500 voyages each | Four years instead of two; settles the window | Then 1.5 h |

- **Results:** Saturday evening to Sunday midday. We'll post them when they're in.
- **Then:** a chart check of the Cornwall end (Seven Stones, Western Rocks, the Land's End shipping lanes) and the recovery plan there.
- **Boat:** build through January; field tests February to April (tow, inclining, self-righting, servo life, a 3-week coastal trial); launch window **1–20 May 2027**, 45 km off Hatteras by charter.

## Offers

- A **randolph_rev_e1.yaml** for Bluewater, like the Rev D one: tell us if you'd like it. Your schema may not express the pump or the detent, so we'd note what it leaves out.
- The **C5 re-score our way** is still welcome whenever it suits you.

Hope Bluewater is going well.
