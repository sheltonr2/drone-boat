"""Shore server for the drone boat (Rev F, Iridium IMT through Ground Control's Cloudloop). Python 3.9+, standard library only.

What it does
  - Receives every message from the boat by Cloudloop's HTTP webhook, keeps the raw JSON, decodes it
    (software/protocol/dronemsg.py) and stores the report in SQLite. Photo parts are joined into JPEG files.
  - Shows a dashboard: the latest report, faults, the latest photo, the track, and the commands sent.
  - Takes commands from a form, checks and signs them with the boat's key, and sends them by Cloudloop's API.
    The boat picks them up at its next session and acknowledges them in the report after.

Run
  python server.py --config config.json            (see config.example.json; keep config.json out of git)
  python server.py --config config.json --port 8080

Secrets (the boat key, the Cloudloop token, the dashboard password, the webhook secret) are read from the config file or
from environment variables, never from this repository. Put the server behind HTTPS (a reverse proxy or a tunnel)
before giving Cloudloop the webhook address: the dashboard password travels in every request.

Status: written 28 Nov 2026 and tested against a fake boat (fake_boat.py, test_shore.py). The Cloudloop webhook field
names and the send-message endpoint are taken from Ground Control's documentation and must be checked against a real
RockBLOCK Plus 9704 message on the bench (Test plan, docs/Design_RevF.md) before the boat relies on them.
"""
import argparse, base64, binascii, hmac, html, json, math, os, sqlite3, sys, threading, time, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "protocol"))
import dronemsg as M  # noqa: E402

SCHEMA = """
create table if not exists raw(id integer primary key, received real, body text, ok integer, error text);
create table if not exists report(id integer primary key, raw_id integer, received real, session integer, time integer,
  lat real, lon real, sog real, cog real, heading real, awa real, aws real, batt_v real, soc integer, solar_w real,
  wing integer, rudder integer, humidity integer, temp integer, leak integer, mode text, wp integer, pump_runs integer,
  last_cmd_seq integer, faults text, size integer);
create table if not exists photo_part(photo_id integer, part integer, parts integer, total integer, data blob, received real,
  primary key(photo_id, part));
create table if not exists photo(photo_id integer primary key, file text, bytes integer, completed real);
create table if not exists command(seq integer primary key, created real, text text, hex text, status text, sent real,
  acked real, result text, detail text);
create table if not exists note(id integer primary key, received real, kind text, text text);
"""


def load_config(path):
    c = json.load(open(path)) if path and os.path.exists(path) else {}
    env = dict(boat_key_hex="DRONE_BOAT_KEY_HEX", cloudloop_token="CLOUDLOOP_TOKEN", cloudloop_thing="CLOUDLOOP_THING",
               dashboard_password="DRONE_DASHBOARD_PASSWORD", webhook_secret="DRONE_WEBHOOK_SECRET")
    for k, e in env.items():
        if os.environ.get(e): c[k] = os.environ[e]
    c.setdefault("boat_id", 1); c.setdefault("data_dir", "data")
    if not os.path.isabs(c["data_dir"]):
        c["data_dir"] = os.path.join(os.path.dirname(os.path.abspath(path)) if path else HERE, c["data_dir"])
    c.setdefault("cloudloop_send_url", "https://api.cloudloop.com/Data/DoSendImtMessage")
    c.setdefault("send", False)  # False: commands are signed and kept in the outbox, not sent (dry run)
    return c


class Store:
    def __init__(self, data_dir):
        os.makedirs(os.path.join(data_dir, "photos"), exist_ok=True)
        self.dir = data_dir; self.lock = threading.Lock()
        self.db = sqlite3.connect(os.path.join(data_dir, "boat.sqlite"), check_same_thread=False)
        self.db.executescript(SCHEMA); self.db.commit()

    def q(self, sql, args=()):
        with self.lock:
            cur = self.db.execute(sql, args); self.db.commit(); return cur.fetchall()

    def insert(self, sql, args=()):
        with self.lock:
            cur = self.db.execute(sql, args); self.db.commit(); return cur.lastrowid

    # ------------------------------------------------------------ incoming
    def receive(self, body_text):
        """Store and decode one webhook body. Returns (ok, detail)."""
        rid = self.insert("insert into raw(received, body, ok) values(?,?,0)", (time.time(), body_text))
        try:
            blob = extract_payload(json.loads(body_text))
            d = M.decode_mo(blob)
        except Exception as e:  # keep the raw message; a decoder fix can replay it (replay())
            self.q("update raw set error=? where id=?", (f"{type(e).__name__}: {e}", rid)); return False, str(e)
        self.ingest(rid, d, len(blob)); self.q("update raw set ok=1 where id=?", (rid,))
        return True, f"session {d['session']}"

    def ingest(self, rid, d, size):
        r = d["report"]; now = time.time()
        self.q("""insert into report(raw_id, received, session, time, lat, lon, sog, cog, heading, awa, aws, batt_v, soc, solar_w,
                  wing, rudder, humidity, temp, leak, mode, wp, pump_runs, last_cmd_seq, faults, size)
                  values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
               (rid, now, d["session"], r["time"], r["lat_deg"], r["lon_deg"], r["sog_cms"] / 100, r["cog_cdeg"] / 100,
                r["heading_cdeg"] / 100, r["awa_ddeg"] / 10, r["aws_cms"] / 100, r["batt_mv"] / 1000, r["soc"], r["solar_dw"] / 10,
                r["wing_deg"], r["rudder_deg"], r["humidity"], r["temp_c"], r["leak"], r["mode_name"], r["wp_index"],
                r["pump_runs"], r["last_cmd_seq"], ",".join(r["fault_names"]), size))
        for a in d["acks"]:
            self.q("update command set status=?, acked=?, result=?, detail=? where seq=?",
                   ("applied" if a["result"] == "applied" else "rejected", now, a["result"],
                    None if a["index"] is None else f"command {a['index'] + 1}", a["seq"]))
        # a report that says it has applied a sequence confirms every earlier command too
        self.q("update command set status='applied', acked=?, result='applied' where seq<=? and status in ('queued','sent','dry run')",
               (now, r["last_cmd_seq"]))
        for p in d["photos"]:
            self.q("insert or replace into photo_part values(?,?,?,?,?,?)", (p["photo_id"], p["part"], p["parts"], p["total"], p["data"], now))
            self.join_photo(p["photo_id"], p["parts"], p["total"])
        for kind in ("diag", "log"):
            for x in d[kind]: self.q("insert into note(received, kind, text) values(?,?,?)", (now, kind, json.dumps(x) if kind == "diag" else x))

    def join_photo(self, pid, parts, total):
        rows = self.q("select part, data from photo_part where photo_id=? order by part", (pid,))
        if len(rows) != parts: return
        data = b"".join(r[1] for r in rows)
        if len(data) != total: return
        ext = "mjpeg" if data.count(b"\xff\xd8\xff") > 1 else "jpg"  # a clip is a run of JPEG frames
        fn = f"photo_{pid:05d}_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.{ext}"
        with open(os.path.join(self.dir, "photos", fn), "wb") as f: f.write(data)
        self.q("insert or replace into photo values(?,?,?,?)", (pid, fn, len(data), time.time()))

    def replay(self):
        """Decode again every raw message that failed (after a decoder fix)."""
        for rid, body in self.q("select id, body from raw where ok=0"):
            try:
                blob = extract_payload(json.loads(body)); self.ingest(rid, M.decode_mo(blob), len(blob)); self.q("update raw set ok=1, error=null where id=?", (rid,))
            except Exception as e:
                self.q("update raw set error=? where id=?", (f"{type(e).__name__}: {e}", rid))


def extract_payload(j):
    """The boat's bytes from a Cloudloop webhook body. Cloudloop's structured message puts the payload, Base64, in
    `message` (documented); this also accepts a nested {"message": {"message": ...}} and a `data`/`payload` field, and hex."""
    cands = []
    def walk(x, depth=0):
        if depth > 3: return
        if isinstance(x, dict):
            for k in ("message", "payload", "data"):
                if k in x:
                    v = x[k]
                    if isinstance(v, str): cands.append(v)
                    else: walk(v, depth + 1)
    walk(j)
    for v in cands:
        for dec in (lambda s: base64.b64decode(s, validate=True), bytes.fromhex):
            try:
                b = dec(v.strip())
                if b and b[0] == M.MO_MAGIC: return b
            except (binascii.Error, ValueError):
                pass
    raise M.ProtocolError("no boat message in the webhook body")


# ------------------------------------------------------------ commands
FORMS = {  # name: [(field, label, type, default)]
    "HOLD": [("lat", "Latitude", float, ""), ("lon", "Longitude (W negative)", float, ""), ("radius_m", "Radius, m", int, 1000)],
    "GOTO": [("lat", "Latitude", float, ""), ("lon", "Longitude", float, "")],
    "SET_ROUTE": [("points", "One point per line: lat, lon", "points", "")],
    "MODE": [("mode", "0 sail, 2 station, 3 drift, 4 safe", int, 0)],
    "SET_REPORT": [("minutes", "Minutes between reports (30-1440)", int, 240)],
    "PHOTO": [("kind", "0 now, 1 large now, 2 stored", int, 0), ("stored", "Stored photo number", int, 0), ("max_bytes", "Max bytes", int, 10000)],
    "SET_PHOTO": [("per_day", "Photos a day (0-4)", int, 1), ("hour_utc", "Hour of the first (UTC)", int, 16), ("max_bytes", "Max bytes", int, 10000)],
    "CLIP": [("seconds", "Seconds (1-10)", int, 5), ("max_bytes", "Max bytes", int, 60000)],
    "DIAG": [], "REBOOT": [("target", "0 companion, 1 autopilot, 2 camera", int, 0)],
}


def parse_form(name, f):
    a = {}
    for k, _, typ, _ in FORMS[name]:
        v = f.get(k, "").strip()
        if typ == "points":
            a[k] = [tuple(float(x) for x in line.replace(";", ",").split(",")[:2]) for line in v.splitlines() if line.strip()]
        else:
            a[k] = typ(v)
    return a


class Commands:
    def __init__(self, store, cfg):
        self.s, self.c = store, cfg

    def key(self):
        k = self.c.get("boat_key_hex")
        if not k or len(bytes.fromhex(k)) != 32: raise ValueError("no boat key: set DRONE_BOAT_KEY_HEX (64 hex digits) or boat_key_hex in the config")
        return bytes.fromhex(k)

    def queue(self, items):
        """items: [(name, args)]. Signs one MT message with the next sequence number; sends it if configured."""
        last = self.s.q("select max(seq) from command")[0][0] or 0
        seq = max(last, int(self.c.get("first_seq", 0))) + 1
        msg = M.encode_mt(self.key(), self.c["boat_id"], seq, int(time.time()), items)
        text = "; ".join(f"{n} {json.dumps(a)}" for n, a in items)
        self.s.q("insert into command(seq, created, text, hex, status) values(?,?,?,?,?)", (seq, time.time(), text, msg.hex(), "queued"))
        return seq, self.send(seq, msg)

    def send(self, seq, msg):
        if not self.c.get("send"):
            self.s.q("update command set status='dry run', detail='send is off in the config' where seq=?", (seq,)); return "dry run"
        token, thing = self.c.get("cloudloop_token"), self.c.get("cloudloop_thing")
        if not token or not thing:
            self.s.q("update command set detail='no Cloudloop token or thing id' where seq=?", (seq,)); return "not sent"
        url = self.c["cloudloop_send_url"] + "?" + urllib.parse.urlencode(dict(token=token, thing=thing, message=base64.b64encode(msg).decode()))
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="GET"), timeout=30) as r:
                body = r.read(2000).decode("utf-8", "replace")
            self.s.q("update command set status='sent', sent=?, detail=? where seq=?", (time.time(), body[:500], seq)); return "sent"
        except Exception as e:
            self.s.q("update command set detail=? where seq=?", (f"send failed: {e}", seq)); return "send failed"


# ------------------------------------------------------------ dashboard
CSS = """body{font:15px/1.4 system-ui,sans-serif;margin:16px;max-width:1100px;color:#1d1d1f}h1{font-size:20px}h2{font-size:16px;margin-top:24px}
table{border-collapse:collapse}td,th{padding:3px 10px 3px 0;text-align:left;vertical-align:top}th{color:#555;font-weight:500}
.bad{color:#b00020;font-weight:600}.ok{color:#08712c}.grid{display:flex;gap:24px;flex-wrap:wrap}img{max-width:480px;border:1px solid #ccc}
input,select,textarea{font:inherit}small{color:#666}"""


def fmt_t(t): return time.strftime("%d %b %H:%M UTC", time.gmtime(t)) if t else ""


def ll(v, hemi): return f"{abs(v):.2f}{hemi[0] if v >= 0 else hemi[1]}"


def track_svg(pts, w=480, h=300):
    if len(pts) < 2: return "<p><small>Track: not enough fixes yet.</small></p>"
    la = [p[0] for p in pts]; lo = [p[1] for p in pts]
    c = math.cos(math.radians(sum(la) / len(la)))
    x0, x1, y0, y1 = min(lo), max(lo), min(la), max(la)
    sx = (x1 - x0) * c or 1e-3; sy = (y1 - y0) or 1e-3; s = min((w - 20) / sx, (h - 20) / sy)
    xy = [(10 + (b - x0) * c * s, h - 10 - (a - y0) * s) for a, b in pts]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    return (f'<svg width="{w}" height="{h}" style="border:1px solid #ccc;background:#f4f8fb"><polyline points="{path}" fill="none" '
            f'stroke="#1565c0" stroke-width="2"/><circle cx="{xy[-1][0]:.1f}" cy="{xy[-1][1]:.1f}" r="5" fill="#b00020"/></svg>'
            f'<br><small>{len(pts)} fixes, {ll(y0, "NS")} to {ll(y1, "NS")}, {ll(x0, "EW")} to {ll(x1, "EW")}</small>')


def dashboard(store):
    e = html.escape
    rep = store.q("select * from report order by id desc limit 1")
    cols = [r[1] for r in store.db.execute("pragma table_info(report)")]
    out = [f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width'><title>Drone boat</title><style>{CSS}</style>",
           "<h1>Drone boat: shore dashboard</h1>"]
    if rep:
        r = dict(zip(cols, rep[0])); age = (time.time() - r["time"]) / 3600
        out.append(f"<p>Last report {fmt_t(r['time'])} ({age:.1f} h ago), session {r['session']}, {r['size']} bytes. "
                   f"<a href='https://www.openstreetmap.org/?mlat={r['lat']:.5f}&mlon={r['lon']:.5f}#map=9/{r['lat']:.4f}/{r['lon']:.4f}'>"
                   f"{r['lat']:.4f}, {r['lon']:.4f}</a></p>")
        faults = r["faults"] or ""
        out.append("<div class=grid><table>" + "".join(f"<tr><th>{e(k)}</th><td>{e(str(v))}</td></tr>" for k, v in [
            ("Mode", r["mode"]), ("Speed / course", f"{r['sog'] * 1.94384:.1f} kn / {r['cog']:.0f}°"), ("Heading", f"{r['heading']:.0f}°"),
            ("Apparent wind", f"{r['awa']:.0f}° at {r['aws'] * 1.94384:.1f} kn"), ("Battery", f"{r['batt_v']:.2f} V, {r['soc']}%"),
            ("Solar", f"{r['solar_w']:.1f} W"), ("Wing / rudder", f"{r['wing']}° / {r['rudder']}°"),
            ("Box", f"{r['humidity']}% RH, {r['temp']} °C"), ("Pump runs", r["pump_runs"]), ("Waypoint", r["wp"]),
            ("Last command applied", r["last_cmd_seq"])]) +
            f"<tr><th>Faults</th><td class={'bad' if faults or r['leak'] else 'ok'}>{e(faults) or 'none'}"
            f"{' LEAK ' + str(r['leak']) if r['leak'] else ''}</td></tr></table>")
        ph = store.q("select photo_id, file, completed from photo where file like '%.jpg' order by completed desc limit 1")
        out.append(f"<div><img src='/photo/{e(ph[0][1])}'><br><small>Photo {ph[0][0]}, {fmt_t(ph[0][2])}</small></div>" if ph else "<div><small>No photo yet.</small></div>")
        out.append("</div>")
        out.append(track_svg([(a, b) for a, b in store.q("select lat, lon from report order by id desc limit 500")][::-1]))
    else:
        out.append("<p>No reports yet.</p>")
    out.append("<h2>Send a command</h2><p><small>Open one, fill it in and send. The boat gets it at its next session and "
               "confirms it in the report after.</small></p>")
    for n, fields in FORMS.items():
        out.append(f"<details><summary>{n}</summary><form method=post action='/command'><input type=hidden name=name value={n}>" +
                   "".join((f"<br><label>{e(lab)}<br><textarea name={k} rows=4 cols=30></textarea></label>" if t == "points" else
                            f"<br><label>{e(lab)} <input name={k} value='{d}' size=12></label>") for k, lab, t, d in fields) +
                   " <br><button>Sign and send</button></form></details>")
    out.append("<h2>Commands</h2><table><tr><th>Seq</th><th>Created</th><th>Command</th><th>Status</th><th>Detail</th></tr>" +
               "".join(f"<tr><td>{s}</td><td>{fmt_t(c)}</td><td>{e(t)}</td><td class={'bad' if st == 'rejected' else ''}>{e(st)}</td>"
                       f"<td>{e(res or '')} {e(det or '')}</td></tr>"
                       for s, c, t, st, res, det in store.q("select seq, created, text, status, result, detail from command order by seq desc limit 30")) + "</table>")
    bad = store.q("select id, received, error from raw where ok=0 order by id desc limit 5")
    if bad:
        out.append("<h2>Messages that did not decode</h2><table>" + "".join(f"<tr><td>{i}</td><td>{fmt_t(t)}</td><td>{e(err or '')}</td></tr>" for i, t, err in bad) + "</table>")
    notes = store.q("select received, kind, text from note order by id desc limit 10")
    if notes:
        out.append("<h2>Diagnostics and log</h2><table>" + "".join(f"<tr><td>{fmt_t(t)}</td><td>{k}</td><td>{e(x)}</td></tr>" for t, k, x in notes) + "</table>")
    return "".join(out)


def make_handler(store, cmds, cfg):
    class H(BaseHTTPRequestHandler):
        server_version = "droneboat/1"

        def log_message(self, fmt, *a):
            sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), fmt % a))

        def reply(self, code, body, ctype="text/html; charset=utf-8"):
            b = body if isinstance(body, bytes) else body.encode("utf-8")
            self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(b)

        def authed(self):
            pw = cfg.get("dashboard_password")
            if not pw: return True if cfg.get("allow_no_password") else self.deny("Set dashboard_password first.")
            h = self.headers.get("Authorization", "")
            try:
                ok = h.startswith("Basic ") and hmac.compare_digest(base64.b64decode(h[6:]).decode().split(":", 1)[1], pw)
            except Exception:
                ok = False
            return ok or self.deny()

        def deny(self, msg="Password required"):
            self.send_response(401); self.send_header("WWW-Authenticate", 'Basic realm="drone boat"'); self.end_headers()
            self.wfile.write(msg.encode()); return False

        def body(self):
            n = int(self.headers.get("Content-Length", 0))
            if n > 400_000: raise ValueError("too large")
            return self.rfile.read(n)

        def do_POST(self):
            path = urllib.parse.urlparse(self.path).path
            secret = cfg.get("webhook_secret")
            if secret and path == f"/cloudloop/{secret}":
                ok, detail = store.receive(self.body().decode("utf-8", "replace"))
                return self.reply(200, json.dumps(dict(ok=ok, detail=detail)), "application/json")
            if path == "/command":
                if not self.authed(): return
                f = {k: v[0] for k, v in urllib.parse.parse_qs(self.body().decode(), keep_blank_values=True).items()}
                name = f.get("name")
                if name not in FORMS: return self.reply(400, "unknown command")
                try:
                    seq, st = cmds.queue([(name, parse_form(name, f))])
                except Exception as ex:
                    return self.reply(400, f"<p>Not sent: {html.escape(str(ex))}</p><p><a href='/'>Back</a></p>")
                return self.redirect()
            self.reply(404, "not found")

        def redirect(self):
            self.send_response(303); self.send_header("Location", "/"); self.end_headers()

        def do_GET(self):
            path = urllib.parse.urlparse(self.path).path
            if not self.authed(): return
            if path == "/": return self.reply(200, dashboard(store))
            if path.startswith("/photo/"):
                fn = os.path.basename(path)
                p = os.path.join(store.dir, "photos", fn)
                if fn.endswith(".jpg") and os.path.exists(p): return self.reply(200, open(p, "rb").read(), "image/jpeg")
            if path == "/api/reports.json":
                cols = [r[1] for r in store.db.execute("pragma table_info(report)")]
                return self.reply(200, json.dumps([dict(zip(cols, r)) for r in store.q("select * from report order by id desc limit 1000")]), "application/json")
            self.reply(404, "not found")
    return H


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", default=os.path.join(HERE, "config.json")); ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="127.0.0.1"); ap.add_argument("--replay", action="store_true", help="decode failed messages again, then exit")
    a = ap.parse_args(argv); cfg = load_config(a.config); store = Store(cfg["data_dir"])
    if a.replay: store.replay(); return
    if not cfg.get("webhook_secret"): print("note: no webhook_secret set, so the webhook is off")
    srv = ThreadingHTTPServer((a.host, a.port), make_handler(store, Commands(store, cfg), cfg))
    print(f"shore server on http://{a.host}:{a.port}/  (data in {cfg['data_dir']}; send={'on' if cfg.get('send') else 'off, dry run'})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
