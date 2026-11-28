# Rev F software: satellite link, shore server and camera

Started 28 Nov 2026 while the simulator ran on the PC. This is the comms half of the "Software plan" in docs/Build_Plan.md, written for Rev F (docs/Design_RevF.md): the RockBLOCK Plus 9704 on Iridium IMT, and the stern-post camera. The mission manager (route, weather avoidance, safe mode, MAVLink to the Pixhawk) is not written yet; the comms code talks to it through `boat/comms/src/mission.h`.

**Status:** everything that can run on a PC has been run and its tests pass. The firmware has been checked for syntax against stand-in Arduino headers only. None of it has run on a real ESP32, camera or modem. The bench test below is the next step.

## What's here

| Folder | What it is | Runs on | Tested |
|---|---|---|---|
| [`protocol/`](protocol) | The message format ([PROTOCOL.md](protocol/PROTOCOL.md)) and its reference codec, `dronemsg.py` | Anywhere | `test_dronemsg.py` |
| [`shore/`](shore) | Shore server: Cloudloop webhook, SQLite store, photos, dashboard, signed commands. Python standard library only | A small always-on computer or cloud host, behind HTTPS | `test_shore.py`, with `fake_boat.py` |
| [`boat/lib/dronemsg`](boat/lib/dronemsg) | The boat's codec in portable C++, with its own SHA-256/HMAC and CRC | Companion ESP32 | Byte-for-byte against the Python codec's vectors |
| [`boat/lib/camlink`](boat/lib/camlink) | Framing for the UART between the companion and the camera | Both ESP32s | `test_camlink.cpp` |
| [`boat/lib/comms_core`](boat/lib/comms_core) | The session logic: report, daily photo, photo parts, sending, receiving and checking commands | Companion ESP32 | `test_comms.cpp`, with a fake boat, camera and modem |
| [`boat/comms`](boat/comms) | Companion firmware (Feather ESP32-S3 with PSRAM): the modem, the camera power and UART, flash settings, bench console | Companion ESP32 | Syntax only |
| [`boat/camera`](boat/camera) | Camera firmware (XIAO ESP32S3 Sense): full-size photo to SD, a 10 KB still or a clip on request | Camera | Syntax only |

Run every test: `python software/run_tests.py` (the C++ tests need g++ or clang++; on the Windows PC they are skipped unless one is installed).

## How a day works

1. At each report time (every 4 hours by default) and at the photo time (16:00 UTC by default), the companion wakes the modem.
2. If a photo is due, it switches the camera on. The camera saves a full-size photo and an XGA copy to its SD card, and returns a 640 × 480 still of 10 KB or less. Then the camera is switched off again.
3. The companion sends one message: the 43-byte report, the acknowledgement of the last commands, and the photo. Without a photo it is 51 bytes.
4. It listens for a minute for commands that the shore has queued. It checks each command message's signature and sequence number and every value. If any check fails it applies none of them. Route, mode and hold go to the mission manager. Photo, report-interval and camera commands are handled in the comms code.
5. If a command asks for a photo, a clip or diagnostics, a second session follows at once, so the answer doesn't wait 4 hours.
6. The shore server stores the report and saves the photo. The dashboard shows them with the track and each command's status.

## Setting up (when the hardware is here)

1. **Key.** On your own computer, run `python software/shore/make_key.py`. It prints 64 hex digits. Put them in the shore server's `config.json` (or the `DRONE_BOAT_KEY_HEX` environment variable). Type `key <the digits>` on the companion's USB console. Never commit the key: anyone with it can steer the boat.
2. **Shore server.** Copy `shore/config.example.json` to `config.json` and run `python server.py --config config.json`. Put it behind HTTPS with a reverse proxy or a tunnel, and set a dashboard password and a webhook secret. In Cloudloop, point the boat's HTTP webhook at `https://<your host>/cloudloop/<webhook secret>`. Keep `"send": false` until the bench test has shown the send endpoint working, then set the Cloudloop token and thing id and turn it on.
3. **Companion.** `cd software/boat/comms && pio run -t upload`. Set the pins in `src/main.cpp` from the wiring sheet (D30). The RockBLOCK library holds 5,000-byte messages by default on Arduino; the build sets `IMT_PAYLOAD_SIZE=12000` for a 10 KB photo. If the library ignores the flag, edit its `imt_queue.h`.
4. **Camera.** `cd software/boat/camera && pio run -t upload`, with a FAT32 microSD card in.

## Bench test (adds to docs/Design_RevF.md "Tests to add")

1. Camera alone, on USB: check it says HELLO at 921600 baud, then that a PHOTO request returns a still under 10 KB and writes `_full` and `_large` files to the card.
2. Companion and camera: type `time <unix seconds>`, then `now`. Check the console log, and that the camera's 5 V switches off afterwards.
3. Add the modem, outdoors with a clear sky. Check that `now` delivers the message to the shore server's webhook and the dashboard shows the report and photo. **Check the webhook's JSON field names against `extract_payload()` in `shore/server.py` now.** Keep the raw body: the server stores it in `raw`, and `server.py --replay` decodes failed ones again after a fix.
4. Send a HOLD and a PHOTO from the dashboard with `send` on. Check that the boat applies them, the photo comes back in a second session, and the command shows "applied".
5. Measure the energy of a report session and a photo session (Design_RevF.md estimates 25 J and 90 J) and update `designs/revF_design.json`.

## Open points

- `rbBegin()`'s port name on Arduino: check the library's `ArduinoBasicSendandReceive.ino` example.
- Cloudloop's send endpoint (`Data/DoSendImtMessage`, Base64 payload) and the webhook body come from Ground Control's documentation. Both are unverified until the bench test.
- The pins in `boat/comms/src/main.cpp` are placeholders until the box is wired.
- Bigger messages: a stored large photo (60-100 KB) goes in about 12 KB parts, one per session, unless the library's payload size is raised (about 230 KB of RAM at 100 KB, per its README).
- The mission manager, the coastline mask behind `mission_point_at_sea()`, and the power manager's sleep schedule are still to write.
