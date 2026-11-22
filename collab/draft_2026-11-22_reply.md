DRAFT for Randolph's approval (not posted). Reply to jcolter11374's comment of 22 Nov 11:05 UTC on boat-sim #50 (issuecomment-7078210631).

---

Hello Maya and team (posted by Claude at Randolph's request). Thank you for the re-score. It's a good result for both simulators.

## We ran the same 46 dates too

Before your number came in, we ran Rev C5 in our own simulator on your set-up: one launch a day at 12:00 UTC, 1 May to 15 June 2023, from 38.32N 74.97W (our run 029, [note](https://github.com/sheltonr2/drone-boat/blob/main/collab/runs_026/c5_029_note.md)).

| 46 daily launches, 2023 | Yours | Ours |
|---|---|---|
| Straight line to 51.4N 10.0W, no waypoint | 3 of 46 | **0 of 46**: 39 aground (Nova Scotia 13, New England / Long Island 13, the Maryland–Virginia shore 10, Newfoundland 3) |
| Via 42.0N 48.0W | **19 of 46 (41.3%)** | **19 of 46 (41.3%)** (13 reporting + 6 tracked), median 125 days |

The same count from two independent models, on two sets of weather data. The arrivals aren't the same 19 voyages, and the counts are small, so it's agreement within the noise rather than proof. But both simulators say the same two things: the waypoint south of the Grand Banks is the whole difference, and Rev C5 sits in the 40s from an Ocean City drop.

The losses look alike too:

| | Yours | Ours |
|---|---|---|
| Aground | 6, all on the Maryland and Virginia shore soon after the drop | 4, of which 1 was on that shore after 25 days and 3 were on Nova Scotia or New England |
| Lost | 11: fishermen, breaking seas, one dead box | 8: 4 struck by a vessel, 1 picked up, 3 keels broken in knockdowns in 7–10 m seas |
| Still at sea at the end of November | 9 | 12 |
| Arrived drifting (not counted) | | 3 |

**On your point 5 (slower crossings):** ours are slower on this sample too. The median is 125 days for these 46, against 121 for our 250 random launches. So most of your 9-day gap is probably the late-May and June dates, which meet lighter winds, rather than the models. Our 12 boats still at sea at the end of November are the same effect.

## Rev E1 in Bluewater

Thank you for taking the file in (#658). For the 3D model, everything in our browser viewer is generated from `build-files/source/design.py` and the STLs in `build-files/stl/`, and it's all in our repo under MIT. If a glTF or OBJ export of the whole boat would save you work (hull, deck, keel and bulb, wing and tail, the stern post and the printed parts, in metres, with the waterline at y = 0), say which format and we'll add one.

Thanks again for the kind words on the build files.

---
Notes for Randolph:
- Our 0/46 against their 3/46 on the straight line: our boats hit land earlier, because our 15 km look-ahead can't avoid a coast the course points straight at.
- Offering the glTF/OBJ export commits us to a small job, about an hour. Delete that sentence if you'd rather not.
