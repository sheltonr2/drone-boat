# Rev F: a daily photo from the boat

Drawn 27 Nov 2026; adopted the same day. Rev F is Rev E3 plus a small camera on the stern post and an Iridium IMT modem in place of the SBD modem. It is a new letter because it adds a system (the camera) and changes the comms (docs/Revisions.md). Nothing else on the boat changes. **Adopted 27 Nov 2026: Rev F is the boat we build and the design the plan's runs use from now on.** Runs made before that date used Rev E3; the 60-day check below shows Rev F sails the same.

## What changes

| | Rev E3 | Rev F |
|---|---|---|
| Modem | RockBLOCK Plus (Iridium SBD, 340 B per message) | RockBLOCK Plus 9704 (Iridium IMT, up to 100 KB per message, 4.8 kbps), same 137 × 40 mm puck in the same bowl P23 |
| Camera | none | Seeed XIAO ESP32S3 Sense (OV3660, 2048 × 1536, microSD) in a pod on the stern post |
| New parts | | P28 camera pod clamp, P29 camera housing (window seat and hood) |
| Wiring | W3: nav light, 4-core | W3: nav light and camera, 6-core; fifth load switch for the camera; companion UART0 to the camera |
| Mass | 28.5 kg | 28.7 kg (+0.18 kg pod, cable and camera; the 9704 is 20 g lighter) |
| Parts (BOM) | $4,914 | $5,041 (+$127) |
| Airtime | ~$39/month (4-hour SBD reports) | ~$42/month (IMT 500 KB plan, reports and a photo a day) |

## Why IMT

A useful still is 5–10 KB even at 640 × 480. On SBD that is 15–30 messages per photo, each a separate session with its own chance of failing, and about 200 credits ($24–$40) per photo. Iridium IMT sends it as one message. Ground Control's plans put IMT below SBD once a boat sends more than about 10 KB a month, and a photo a day is about 300 KB a month.

The RockBLOCK Plus 9704 is the IMT version of the puck we already use: the same footprint, a 7–30 V supply, under 2 W while sending, and a 3 m cable. It draws up to 6.7 W for about 30 s when it starts, so fuse F6 becomes a slow-blow. It costs about $479.

## Camera pod (P28, P29)

- The pod clamps to the stern post at z 472–522 mm, below the nav light and above the vane, looking aft and 10° down. Aft is the one view that never has the wing in it, and shows the wake, the sea state and the rudders.
- P29 is a printed cup: 46 mm OD, 62 mm long, with a 40 × 3 mm borosilicate window bonded into a seat, a 12 mm hood over it and a drain slot in the bottom.
- The camera board is conformal-coated and potted except the lens, with a silica gel pack in the cup. The cable runs down the post inside W3.
- Drawings: D01 (general arrangement), D07 (stern post), D23 and D24 (P28, P29), and D30 (wiring) are updated. The cover sheet lists Rev F.

## Software

1. Once a day at local noon, the companion switches the camera on through its load switch.
2. The camera takes a full-resolution photo and saves it to its microSD card. Then it makes a 640 × 480 JPEG, lowering the quality until it fits in 10 KB, and sends it to the companion over UART0. The camera is then switched off.
3. The companion attaches the photo to the next report and sends both as one IMT message. Commands come back in the same session, as now.
4. A new `PHOTO` command asks for a still now, a bigger still, or a stored full-resolution photo cut into pieces. A `CLIP` command can send a short low-resolution clip (under 100 KB). At about $0.40 per KB over the plan, a clip is worth sending only for something worth seeing; the $50 plan (1 MB) leaves room for a few a month.
5. The shore server moves from the SBD webhook to Ground Control's IMT (Cloudloop) webhook. The dashboard shows the latest photo next to the track.
6. If the camera doesn't answer within 60 s, the companion gives up for that day and sets a fault bit. A dead camera never holds up a report.

The modem uses a different serial protocol from the SBD RockBLOCK, so the comms code is rewritten. Ground Control publishes a library for it.

## Power

| | Energy |
|---|---|
| Report session, IMT (estimate) | ~25 J (was ~6 J on SBD) |
| Daily photo: camera ~20 s at 0.45 W, then ~40 s sending at under 2 W | ~90 J |
| Extra per day | ~0.06 Wh |

The boat uses about 30 Wh a day, so this is lost in the noise. The session figures are estimates and need to be measured on the bench.

## Cost

- Parts: +$127 net. The modem is about $60 more than the RockBLOCK Plus ($479 against $419). The camera, microSD, window, cable, inserts, screws, silica gel and a spare camera make up the rest (build-files/BOM.csv).
- Airtime: the IMT post-paid plans are $17 (no data), $25 (50 KB), $34 (250 KB), $42 (500 KB) and $50 (1 MB) a month, with a 3-month minimum and $0.30–$0.50 per KB over the plan. Every message is charged at least 25–75 bytes. Six reports a day are about 8 KB a month and a photo a day is about 300 KB, so the $42 plan fits with room for commands and a few bigger photos. The E3 SBD plan at 4-hour reports is about $39 a month.

## Simulator

`designs/revF_design.json` adds the camera mass and the IMT energy and billing. The new options (`comms.imt`, `comms.photo_per_day`, `comms.photo_bytes`, `power.photo_session_j`) are off unless a design file sets them, and the regression runs are unchanged bit for bit. On a 60-day test voyage Rev F sent 60 photos (616 KB) for $83 of airtime against $77 for Rev E3, with the same track and battery. A full Monte Carlo isn't needed: 0.18 kg at 0.5 m raises the centre of gravity by about 2 mm, and the energy is under 0.2% of the daily budget.

## Risks

- **Salt on the window.** Spray will dry on the glass. The hood, the 10° tilt and a hydrophobic coating help, but expect some hazy days. A photo a day is still a check on the boat even when it's soft.
- **Condensation.** The cup is sealed with a gel pack, and the board is potted. A fog test (fridge to sun) on the bench will show whether it needs a vent.
- **A flooded camera must not take down the boat.** The camera has its own load switch and fuse, and the UART has series resistors, so a short in the pod costs only the photos.
- **New modem.** The 9704 and IMT are newer than SBD, with less field history on small boats. The YB3 backup tracker is unchanged, so a modem fault still leaves a position report.
- **3-month minimum** on the IMT plan. Start the plan for the coastal trial, not months before.

## Tests to add

1. Desk: the 9704 and camera on the bench supply. Measure each session's energy and check photo size against JPEG quality.
2. Fog test: pod in a fridge for an hour, then into the sun, photo every 5 minutes.
3. Spray test: hose with salt water and let it dry, check the photo.
4. Lake test: daily photos for a week, through the shore server to the dashboard.
5. Fault test: unplug the camera mid-photo; the report must still go out.
