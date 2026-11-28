"""Reference codec for the boat <-> shore protocol, version 1 (PROTOCOL.md). Standard library only.

    python dronemsg.py --vectors   rewrite vectors.json (the shared test vectors for the C++ codec)
    python -m unittest test_dronemsg
"""
import hashlib, hmac, json, os, struct, sys, zlib

MO_MAGIC, MT_MAGIC = 0xD1, 0xD2
TAG_LEN = 16
REPORT_FMT = "<IiiHHHhHHBHbbBbBBBBII"
REPORT_FIELDS = ("time", "lat", "lon", "sog_cms", "cog_cdeg", "heading_cdeg", "awa_ddeg", "aws_cms", "batt_mv", "soc",
                 "solar_dw", "wing_deg", "rudder_deg", "humidity", "temp_c", "leak", "mode", "wp_index", "pump_runs",
                 "last_cmd_seq", "faults")
REPORT_LEN = struct.calcsize(REPORT_FMT)
assert REPORT_LEN == 43
MODES = ("sail", "sail+thrust", "station", "drift", "safe", "limp-home")
FAULTS = ("main_gps", "compass", "wind_vane", "autopilot_link", "rudder_port", "rudder_stbd", "tail_servo", "pump",
          "camera", "sd_card", "modem_retry", "low_battery", "limp_home", "watchdog_reset", "command_rejected", "humidity_high")
SEC_ACK, SEC_PHOTO, SEC_DIAG, SEC_LOG = 1, 2, 3, 4
ACK_RESULTS = ("applied", "bad_signature", "old_sequence", "bad_value", "unknown_command", "wrong_boat")
OPS = {"SET_ROUTE": 1, "GOTO": 2, "MODE": 3, "SET_REPORT": 4, "HOLD": 5, "GEOFENCE": 6, "DIAG": 7, "REBOOT": 8,
       "PHOTO": 9, "CLIP": 10, "SET_PHOTO": 11}
OP_NAMES = {v: k for k, v in OPS.items()}


class ProtocolError(ValueError):
    pass


def deg_to_e7(x): return int(round(x * 1e7))
def e7_to_deg(i): return i / 1e7
def _pt(lat, lon): return struct.pack("<ii", deg_to_e7(lat), deg_to_e7(lon))


# ---------------------------------------------------------------- MO: boat to shore
def encode_report(r):
    return struct.pack(REPORT_FMT, *(int(r.get(k, 0)) for k in REPORT_FIELDS))


def decode_report(b):
    if len(b) != REPORT_LEN: raise ProtocolError("report length")
    d = dict(zip(REPORT_FIELDS, struct.unpack(REPORT_FMT, b)))
    d["lat_deg"], d["lon_deg"] = e7_to_deg(d["lat"]), e7_to_deg(d["lon"])
    d["mode_name"] = MODES[d["mode"]] if d["mode"] < len(MODES) else f"mode {d['mode']}"
    d["fault_names"] = [n for i, n in enumerate(FAULTS) if d["faults"] >> i & 1]
    return d


def section(kind, payload): return struct.pack("<BH", kind, len(payload)) + payload
def ack_section(seq, result, index=0xFF): return section(SEC_ACK, struct.pack("<IBB", seq, result, index))
def photo_section(photo_id, part, parts, total, data): return section(SEC_PHOTO, struct.pack("<HBBI", photo_id, part, parts, total) + data)
def text_section(kind, text): return section(kind, text.encode("utf-8"))


def encode_mo(boat_id, session, report, sections=()):
    body = struct.pack("<BBH", MO_MAGIC, boat_id, session & 0xFFFF) + encode_report(report) + b"".join(sections)
    return body + struct.pack("<I", zlib.crc32(body) & 0xFFFFFFFF)


def decode_mo(b):
    if len(b) < 4 + REPORT_LEN + 4: raise ProtocolError("too short")
    body, crc = b[:-4], struct.unpack("<I", b[-4:])[0]
    if zlib.crc32(body) & 0xFFFFFFFF != crc: raise ProtocolError("CRC mismatch")
    magic, boat, session = struct.unpack("<BBH", body[:4])
    if magic != MO_MAGIC: raise ProtocolError(f"not an MO message (magic 0x{magic:02X})")
    out = dict(boat_id=boat, session=session, report=decode_report(body[4:4 + REPORT_LEN]), acks=[], photos=[], diag=[], log=[], unknown=[])
    i = 4 + REPORT_LEN
    while i < len(body):
        if i + 3 > len(body): raise ProtocolError("truncated section header")
        kind, n = struct.unpack("<BH", body[i:i + 3]); p = body[i + 3:i + 3 + n]
        if len(p) != n: raise ProtocolError("truncated section")
        if kind == SEC_ACK:
            seq, res, idx = struct.unpack("<IBB", p)
            out["acks"].append(dict(seq=seq, result=ACK_RESULTS[res] if res < len(ACK_RESULTS) else res, index=None if idx == 0xFF else idx))
        elif kind == SEC_PHOTO:
            pid, part, parts, total = struct.unpack("<HBBI", p[:8])
            out["photos"].append(dict(photo_id=pid, part=part, parts=parts, total=total, data=p[8:]))
        elif kind == SEC_DIAG:
            out["diag"].append(dict(kv.split("=", 1) if "=" in kv else (kv, "") for kv in p.decode("utf-8", "replace").split(";") if kv))
        elif kind == SEC_LOG:
            out["log"].append(p.decode("utf-8", "replace"))
        else:
            out["unknown"].append(dict(kind=kind, data=p))
        i += 3 + n
    return out


# ---------------------------------------------------------------- MT: shore to boat
def _cmd(op, payload): return struct.pack("<BH", op, len(payload)) + payload


def encode_command(name, **a):
    """One command as bytes. Arguments in degrees, metres, minutes, bytes, as PROTOCOL.md."""
    op = OPS[name]
    if name == "SET_ROUTE": p = struct.pack("<B", len(a["points"])) + b"".join(_pt(*q) for q in a["points"])
    elif name == "GOTO": p = _pt(a["lat"], a["lon"])
    elif name == "MODE": p = struct.pack("<B", a["mode"] if isinstance(a["mode"], int) else MODES.index(a["mode"]))
    elif name == "SET_REPORT": p = struct.pack("<H", a["minutes"])
    elif name == "HOLD": p = _pt(a["lat"], a["lon"]) + struct.pack("<H", a["radius_m"])
    elif name == "GEOFENCE":
        pts = a.get("points", []); p = struct.pack("<BB", a["action"], len(pts)) + b"".join(_pt(*q) for q in pts)
    elif name == "DIAG": p = b""
    elif name == "REBOOT": p = struct.pack("<B", a["target"])
    elif name == "PHOTO": p = struct.pack("<BHI", a["kind"], a.get("stored", 0), a.get("max_bytes", 10000))
    elif name == "CLIP": p = struct.pack("<BI", a["seconds"], a["max_bytes"])
    elif name == "SET_PHOTO": p = struct.pack("<BBH", a["per_day"], a["hour_utc"], a["max_bytes"])
    return _cmd(op, p)


def check_command(name, a):
    """The same range checks the boat makes (except the coastline mask). Returns an error string or None."""
    def lat_ok(la, lo): return -90 <= la <= 90 and -180 <= lo <= 180
    if name == "SET_ROUTE":
        if not 1 <= len(a["points"]) <= 50: return "a route has 1 to 50 points"
        if not all(lat_ok(*q) for q in a["points"]): return "point out of range"
    if name in ("GOTO", "HOLD") and not lat_ok(a["lat"], a["lon"]): return "point out of range"
    if name == "HOLD" and not 200 <= a["radius_m"] <= 5000: return "radius 200 to 5000 m"
    if name == "MODE" and (a["mode"] if isinstance(a["mode"], int) else MODES.index(a["mode"])) > 4: return "mode 0 to 4"
    if name == "SET_REPORT" and not 30 <= a["minutes"] <= 1440: return "report interval 30 to 1440 minutes"
    if name == "GEOFENCE" and a["action"] == 1 and not 3 <= len(a.get("points", [])) <= 20: return "a fence has 3 to 20 points"
    if name == "PHOTO" and not 2000 <= a.get("max_bytes", 10000) <= 100000: return "max bytes 2,000 to 100,000"
    if name == "CLIP" and not (1 <= a["seconds"] <= 10 and a["max_bytes"] <= 100000): return "1 to 10 s, up to 100,000 bytes"
    if name == "SET_PHOTO" and not (0 <= a["per_day"] <= 4 and 0 <= a["hour_utc"] <= 23 and 2000 <= a["max_bytes"] <= 20000):
        return "0 to 4 a day, hour 0-23, 2,000 to 20,000 bytes"
    return None


def encode_mt(key, boat_id, seq, issued_at, commands):
    """commands: list of (name, kwargs). Returns the signed message."""
    for name, a in commands:
        err = check_command(name, a)
        if err: raise ProtocolError(f"{name}: {err}")
    body = struct.pack("<BBII", MT_MAGIC, boat_id, seq, issued_at) + b"".join(encode_command(n, **a) for n, a in commands)
    return body + hmac.new(key, body, hashlib.sha256).digest()[:TAG_LEN]


def decode_command(op, p):
    name = OP_NAMES.get(op)
    pt = lambda b: tuple(e7_to_deg(v) for v in struct.unpack("<ii", b))
    if name == "SET_ROUTE":
        n = p[0]; return name, dict(points=[pt(p[1 + 8 * i:9 + 8 * i]) for i in range(n)])
    if name == "GOTO": la, lo = pt(p); return name, dict(lat=la, lon=lo)
    if name == "MODE": return name, dict(mode=p[0])
    if name == "SET_REPORT": return name, dict(minutes=struct.unpack("<H", p)[0])
    if name == "HOLD": la, lo = pt(p[:8]); return name, dict(lat=la, lon=lo, radius_m=struct.unpack("<H", p[8:10])[0])
    if name == "GEOFENCE": return name, dict(action=p[0], points=[pt(p[2 + 8 * i:10 + 8 * i]) for i in range(p[1])])
    if name == "DIAG": return name, {}
    if name == "REBOOT": return name, dict(target=p[0])
    if name == "PHOTO": k, s, m = struct.unpack("<BHI", p); return name, dict(kind=k, stored=s, max_bytes=m)
    if name == "CLIP": s, m = struct.unpack("<BI", p); return name, dict(seconds=s, max_bytes=m)
    if name == "SET_PHOTO": n, h, m = struct.unpack("<BBH", p); return name, dict(per_day=n, hour_utc=h, max_bytes=m)
    return f"op_{op}", dict(raw=p)


def decode_mt(key, b, boat_id=None, last_seq=None):
    """Verify and decode. Raises ProtocolError with the ACK result name if the boat would reject it."""
    if len(b) < 10 + TAG_LEN: raise ProtocolError("bad_value")
    body, tag = b[:-TAG_LEN], b[-TAG_LEN:]
    if not hmac.compare_digest(hmac.new(key, body, hashlib.sha256).digest()[:TAG_LEN], tag): raise ProtocolError("bad_signature")
    magic, boat, seq, issued = struct.unpack("<BBII", body[:10])
    if magic != MT_MAGIC: raise ProtocolError("bad_value")
    if boat_id is not None and boat != boat_id: raise ProtocolError("wrong_boat")
    if last_seq is not None and seq <= last_seq: raise ProtocolError("old_sequence")
    cmds, i = [], 10
    while i < len(body):
        op, n = struct.unpack("<BH", body[i:i + 3]); cmds.append(decode_command(op, body[i + 3:i + 3 + n])); i += 3 + n
    return dict(boat_id=boat, seq=seq, issued_at=issued, commands=cmds)


# ---------------------------------------------------------------- shared test vectors
VEC_KEY = bytes(range(32))  # test key only; the real key never goes in the repository
VEC_REPORT = dict(time=1840000000, lat=deg_to_e7(49.70), lon=deg_to_e7(-5.20), sog_cms=41, cog_cdeg=8750, heading_cdeg=9120,
                  awa_ddeg=-1350, aws_cms=820, batt_mv=13210, soc=87, solar_dw=143, wing_deg=-12, rudder_deg=3, humidity=41,
                  temp_c=17, leak=0, mode=2, wp_index=4, pump_runs=1, last_cmd_seq=7, faults=(1 << 8) | (1 << 10))
VEC_COMMANDS = [("HOLD", dict(lat=18.1022, lon=-64.4051, radius_m=1000)), ("SET_REPORT", dict(minutes=240)),
                ("SET_ROUTE", dict(points=[(42.0, -48.0), (48.9, -7.2), (49.1, -6.2)])), ("PHOTO", dict(kind=0, stored=0, max_bytes=10000)),
                ("MODE", dict(mode="station"))]


def vectors():
    photo = bytes((i * 37 + 11) & 0xFF for i in range(300))
    mo = encode_mo(1, 513, VEC_REPORT, [ack_section(7, 0), photo_section(12, 0, 1, len(photo), photo), text_section(SEC_DIAG, "v=1.0;up=86400")])
    mt = encode_mt(VEC_KEY, 1, 8, 1840000100, VEC_COMMANDS)
    return dict(note="Generated by software/protocol/dronemsg.py --vectors. Test key only.", key=VEC_KEY.hex(), report=VEC_REPORT,
                photo=photo.hex(), mo=mo.hex(), mo_report_only=encode_mo(1, 513, VEC_REPORT).hex(), mt=mt.hex(),
                mt_commands=[[n, a] for n, a in VEC_COMMANDS])


def c_header(v):
    """The same vectors as a C header for the boat codec's host test."""
    def arr(name, hexs):
        b = bytes.fromhex(hexs); rows = [", ".join(f"0x{x:02x}" for x in b[i:i + 16]) for i in range(0, len(b), 16)]
        return f"static const uint8_t {name}[{len(b)}] = {{\n  " + ",\n  ".join(rows) + "\n};\n"
    r = v["report"]
    rep = "static const dronemsg::Report VEC_REPORT = {" + ", ".join(str(r[k]) for k in REPORT_FIELDS) + "};\n"
    return ("// Generated by software/protocol/dronemsg.py --vectors. Do not edit. Test key only.\n#pragma once\n#include <stdint.h>\n"
            '#include "dronemsg.h"\n' + rep + arr("VEC_KEY", v["key"]) + arr("VEC_PHOTO", v["photo"]) + arr("VEC_MO", v["mo"])
            + arr("VEC_MO_REPORT_ONLY", v["mo_report_only"]) + arr("VEC_MT", v["mt"]))


if __name__ == "__main__" and "--vectors" in sys.argv:
    here = os.path.dirname(os.path.abspath(__file__)); v = vectors()
    with open(os.path.join(here, "vectors.json"), "w") as f: json.dump(v, f, indent=1)
    h = os.path.join(here, "..", "boat", "lib", "dronemsg", "test", "vectors.h")
    os.makedirs(os.path.dirname(h), exist_ok=True)
    with open(h, "w") as f: f.write(c_header(v))
    print("wrote vectors.json and", os.path.normpath(h))
