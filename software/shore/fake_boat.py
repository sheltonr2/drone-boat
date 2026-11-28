"""A fake boat for testing the shore server: posts messages shaped like Cloudloop webhooks.

    python fake_boat.py --url http://127.0.0.1:8080/cloudloop/<webhook_secret> --reports 12 --photo-every 6

Each report moves the boat a little along a course; every Nth report carries a small test photo (made with Pillow
if it is installed, otherwise a tiny placeholder JPEG). It can also acknowledge a command sequence (--ack SEQ).
"""
import argparse, base64, io, json, math, os, sys, time, urllib.request, uuid
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "protocol"))
import dronemsg as M  # noqa: E402

# a valid 1 x 1 grey JPEG, for when Pillow is missing
TINY_JPEG = base64.b64decode(
    "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////"
    "wAALCAABAAEBAREA/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AKp//2Q==")


def test_photo(n, w=640, h=480, quality=40):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return TINY_JPEG
    im = Image.new("RGB", (w, h), (120, 160, 200)); d = ImageDraw.Draw(im)
    d.rectangle([0, h * 0.55, w, h], fill=(40, 80, 110))
    for i in range(0, w, 40): d.line([i, h * 0.55 + (i * 7 + n * 13) % 30, i + 30, h * 0.6], fill=(220, 230, 240), width=2)
    d.text((10, 10), f"fake boat photo {n}", fill=(255, 255, 255))
    b = io.BytesIO(); im.save(b, "JPEG", quality=quality); return b.getvalue()


def report(i, lat0=18.10, lon0=-64.41, last_seq=0):
    t = int(time.time()) - (12 - i) * 4 * 3600
    lat, lon = lat0 + 0.01 * math.sin(i / 3), lon0 - 0.02 * i
    return dict(time=t, lat=M.deg_to_e7(lat), lon=M.deg_to_e7(lon), sog_cms=35 + i % 5, cog_cdeg=27000, heading_cdeg=26500,
                awa_ddeg=-1500, aws_cms=650, batt_mv=13150, soc=85 - i % 7, solar_dw=120, wing_deg=-10, rudder_deg=2,
                humidity=40, temp_c=27, leak=0, mode=2, wp_index=0, pump_runs=0, last_cmd_seq=last_seq, faults=0)


def webhook_body(mo):
    """The documented Cloudloop structured message: id, receivedAt, identity, header.imt, message (Base64)."""
    return dict(id=str(uuid.uuid4()), receivedAt=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                identity=dict(thingId="fake-thing"), header=dict(imt=dict(topicId=244, size=len(mo), crcError=False)),
                message=base64.b64encode(mo).decode())


def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as r: return json.loads(r.read())


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--url", required=True); ap.add_argument("--reports", type=int, default=6)
    ap.add_argument("--photo-every", type=int, default=6); ap.add_argument("--ack", type=int, default=None)
    a = ap.parse_args(argv)
    for i in range(a.reports):
        secs = []
        if a.ack is not None and i == a.reports - 1: secs.append(M.ack_section(a.ack, 0))
        if a.photo_every and i % a.photo_every == a.photo_every - 1:
            jpg = test_photo(i); secs.append(M.photo_section(100 + i, 0, 1, len(jpg), jpg))
        mo = M.encode_mo(1, i, report(i, last_seq=a.ack if (a.ack is not None and i == a.reports - 1) else 0), secs)
        print(i, len(mo), "bytes", post(a.url, webhook_body(mo)))


if __name__ == "__main__":
    main()
