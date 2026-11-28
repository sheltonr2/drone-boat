# Boat ↔ shore message protocol, version 1 (Rev F, Iridium IMT)

Drafted 28 Nov 2026 for Rev F (docs/Design_RevF.md). It replaces the SBD layout in docs/Build_Plan.md: IMT carries up to 100 KB per message, so a report, an acknowledgement and a photo travel together in one message, and commands carry a longer signature.

The reference implementation is [`dronemsg.py`](dronemsg.py) (shore) and [`software/boat/lib/dronemsg`](../boat/lib/dronemsg) (boat, C++). Both are tested against the same vectors in [`vectors.json`](vectors.json), so a change to one must be made in the other and the vectors regenerated (`python dronemsg.py --vectors`).

All integers are little-endian. Latitude and longitude are signed 32-bit integers in units of 1e-7 degree.

## Boat to shore (MO): one message per session

| Offset | Size | Field |
|---|---|---|
| 0 | 1 | Magic and version: `0xD1` |
| 1 | 1 | Boat id (1 for the first boat) |
| 2 | 2 | Session counter, uint16, wraps |
| 4 | 43 | Report (below) |
| 47 | ... | Zero or more sections: type uint8, length uint16, payload |
| end − 4 | 4 | CRC-32 (IEEE, as zlib.crc32) of everything before it |

IMT has its own CRC on the air; this one also catches a message broken between the modem and the companion, or by the shore server's own handling.

### Report (43 bytes)

| Offset | Type | Field | Unit |
|---|---|---|---|
| 0 | uint32 | time | Unix seconds, UTC, from GPS |
| 4 | int32 | lat | 1e-7 deg |
| 8 | int32 | lon | 1e-7 deg |
| 12 | uint16 | speed over ground | cm/s |
| 14 | uint16 | course over ground | 0.01 deg |
| 16 | uint16 | heading | 0.01 deg |
| 18 | int16 | apparent wind angle | 0.1 deg, −1800 to 1800 |
| 20 | uint16 | apparent wind speed | cm/s |
| 22 | uint16 | battery | mV |
| 24 | uint8 | state of charge | % |
| 25 | uint16 | solar power | 0.1 W |
| 27 | int8 | wing (tail) angle | deg |
| 28 | int8 | rudder angle | deg |
| 29 | uint8 | humidity in the box | % |
| 30 | int8 | temperature in the box | °C |
| 31 | uint8 | leak flags | bit 0 sump, bit 1 box, bit 2 battery box |
| 32 | uint8 | mode | 0 sail, 1 sail + thrust, 2 station, 3 drift, 4 safe, 5 limp-home |
| 33 | uint8 | current waypoint index | |
| 34 | uint8 | pump runs since the last report | |
| 35 | uint32 | last command sequence applied | |
| 39 | uint32 | fault bits | below |

Fault bits: 0 main GPS, 1 compass, 2 wind vane, 3 autopilot link, 4 rudder servo port, 5 rudder servo starboard, 6 tail servo, 7 pump, 8 camera, 9 SD card, 10 modem retry, 11 low battery, 12 limp-home active, 13 watchdog reset since the last report, 14 command rejected (see the ACK section), 15 humidity high.

### Sections

| Type | Name | Payload |
|---|---|---|
| 0x01 | ACK | uint32 command sequence, uint8 result (0 applied, 1 bad signature, 2 old sequence, 3 bad value, 4 unknown command, 5 wrong boat), uint8 index of the failing command (0xFF for none) |
| 0x02 | PHOTO | uint16 photo id, uint8 part index, uint8 part count, uint32 total bytes, then the JPEG bytes of this part |
| 0x03 | DIAG | UTF-8 text, `key=value` pairs separated by `;` |
| 0x04 | LOG | UTF-8 text, one line |

A daily photo (10 KB or less) goes as a single PHOTO part. A bigger photo or a clip is cut into parts of up to 60 KB, one per session, and the shore server joins them by photo id.

## Shore to boat (MT): signed commands

| Offset | Size | Field |
|---|---|---|
| 0 | 1 | Magic and version: `0xD2` |
| 1 | 1 | Boat id |
| 2 | 4 | Sequence number, uint32, must be higher than the last one the boat applied |
| 6 | 4 | Issued at, Unix seconds |
| 10 | ... | Commands: opcode uint8, length uint16, payload |
| end − 16 | 16 | HMAC-SHA256 of everything before it, with the boat's key, first 16 bytes |

The key is 32 random bytes, stored in the boat's flash and on the shore server, never in this repository. A message whose signature fails, whose sequence is not higher than the last one applied, or whose boat id is wrong is ignored and reported in the next ACK. The boat checks every command before applying any: if one fails, none are applied.

### Commands

| Opcode | Name | Payload | Checks on the boat |
|---|---|---|---|
| 0x01 | SET_ROUTE | uint8 n, then n × (lat, lon) | 1 ≤ n ≤ 50; every point at sea on the boat's coastline mask |
| 0x02 | GOTO | lat, lon | at sea |
| 0x03 | MODE | uint8 mode (as in the report, 0–4) | thrust only if a thruster is fitted |
| 0x04 | SET_REPORT | uint16 minutes | 30 to 1440 |
| 0x05 | HOLD | lat, lon, uint16 radius m | at sea; radius 200 to 5000 |
| 0x06 | GEOFENCE | uint8 action (0 clear all, 1 add), uint8 n, n × (lat, lon) | 3 ≤ n ≤ 20 to add |
| 0x07 | DIAG | none | |
| 0x08 | REBOOT | uint8 target (0 companion, 1 autopilot, 2 camera) | |
| 0x09 | PHOTO | uint8 kind (0 now, standard size; 1 now, large; 2 a stored photo), uint16 stored photo number, uint32 max bytes | max bytes 2,000 to 100,000 |
| 0x0A | CLIP | uint8 seconds, uint32 max bytes | 1 to 10 s; max bytes up to 100,000 |
| 0x0B | SET_PHOTO | uint8 photos per day, uint8 hour (UTC) of the first, uint16 max bytes | 0 to 4 a day; 2,000 to 20,000 bytes |

## Costs

A report alone is 51 bytes, which IMT charges as its 25–75-byte minimum per message. A report with a 10 KB photo is about 10.1 KB. Six reports a day plus a photo a day come to about 310 KB a month (docs/Design_RevF.md).
