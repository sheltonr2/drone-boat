"""Local web app: python -m drone_sim.server  (opens http://127.0.0.1:8765)."""
import json, os, sys, threading, time, traceback, uuid, webbrowser, copy, math, mimetypes, re
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import numpy as np

from . import design as D
from . import geometry, vpp as vppmod
from .sim import Voyage, prepare_design, DEFAULT_SCENARIO
from .failures import DEFAULT_RATES, RATE_SETS, DEFAULT_RATE_SET
from .montecarlo import run_montecarlo

ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(ROOT, "static")
WORK = os.path.abspath(os.environ.get("DRONE_SIM_HOME", os.path.join(os.path.dirname(ROOT), "workspace")))
CACHE = os.path.join(WORK, "cache"); UPLOADS = os.path.join(WORK, "uploads"); RESULTS = os.path.join(WORK, "results")
for p in (CACHE, UPLOADS, RESULTS):
    os.makedirs(p, exist_ok=True)

JOBS = {}


def jsonable(o):
    if isinstance(o, dict): return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray): return jsonable(o.tolist())
    if isinstance(o, (np.floating,)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, float): return None if not math.isfinite(o) else o
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


class Job:
    def __init__(self, kind, design, scenario, extra):
        self.id = uuid.uuid4().hex[:10]; self.kind = kind
        self.status = "queued"; self.progress = 0.0; self.logs = []; self.result = None; self.error = None
        self.live = None; self.cancel = False; self.t0 = time.time()
        self.design, self.scenario, self.extra = design, scenario, extra

    def log(self, *a):
        msg = " ".join(str(x) for x in a)
        self.logs.append(f"{time.strftime('%H:%M:%S')}  {msg}")
        self.logs = self.logs[-300:]

    def run(self):
        self.status = "running"
        try:
            if self.kind == "voyage":
                def prog(f, st):
                    if self.cancel: raise KeyboardInterrupt("cancelled")
                    self.progress = f
                    self.live = dict(lat=st["lat"], lon=st["lon"], soc=st["soc"], heading=st["heading"])
                v = Voyage(self.design, self.scenario, cache_dir=CACHE, log=self.log, progress=prog)
                self.result = v.run()
            else:
                def prog(f, r):
                    self.progress = f
                    self.live = dict(done=int(round(f*self.extra.get("n_runs", 1))), last=r.get("outcome"))
                self.result = run_montecarlo(self.design, self.scenario, n_runs=int(self.extra.get("n_runs", 50)),
                                             window=self.extra.get("window"), processes=self.extra.get("processes"),
                                             cache_dir=CACHE, log=self.log, progress=prog, cancelled=lambda: self.cancel)
            self.result = jsonable(self.result)
            with open(os.path.join(RESULTS, f"{self.kind}_{self.id}.json"), "w") as fh:
                json.dump(self.result, fh)
            self.status = "done"; self.progress = 1.0
        except KeyboardInterrupt:
            self.status = "cancelled"
        except Exception as e:
            self.error = f"{e}"; self.status = "error"; self.log(traceback.format_exc())


def analyze(design):
    boat = geometry.Boat(design)
    summ = boat.summary()
    prep = prepare_design(design, CACHE, log=lambda *a: None)
    P = prep["polar"]
    tws_list = [3, 5, 8, 12, 16]
    twa = list(range(30, 181, 10))
    polar = {str(t): [round(P(t, math.radians(a), 0.5 if t < 8 else 1.5, 1.0, ("u",))["u"]*1.944, 3) for a in twa] for t in tws_list}
    vmg = {str(t): [round(math.degrees(x)) for x in P.best_vmg_angles(t)] for t in tws_list}
    return jsonable(dict(summary=summ, outlines=geometry.outlines(boat), polar=dict(twa=twa, kn=polar, vmg=vmg)))


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, code, body, ctype="application/json", extra=None):
        if not isinstance(body, (bytes, bytearray)):
            body = json.dumps(jsonable(body)).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(n) if n else b""

    def do_GET(self):
        u = urlparse(self.path); p = u.path
        if p == "/" or p.startswith("/static/"):
            f = os.path.join(STATIC, "index.html" if p == "/" else p[len("/static/"):])
            f = os.path.abspath(f)
            if not f.startswith(STATIC) or not os.path.exists(f): return self._send(404, {"error": "not found"})
            return self._send(200, open(f, "rb").read(), mimetypes.guess_type(f)[0] or "application/octet-stream")
        if p == "/api/defaults":
            return self._send(200, dict(design=D.default_design(), editable=D.EDITABLE, scenario=DEFAULT_SCENARIO,
                                        failures=DEFAULT_RATES, rate_sets=RATE_SETS, rate_set=DEFAULT_RATE_SET, cpu=os.cpu_count(), workspace=WORK))
        m = re.match(r"^/api/job/([0-9a-f]+)$", p)
        if m:
            j = JOBS.get(m.group(1))
            if not j: return self._send(404, {"error": "no such job"})
            since = int(parse_qs(u.query).get("log", ["0"])[0])
            out = dict(id=j.id, kind=j.kind, status=j.status, progress=j.progress, live=j.live, error=j.error,
                       logs=j.logs[since:], log_total=len(j.logs), elapsed=round(time.time() - j.t0, 1))
            if j.status == "done": out["result"] = j.result
            return self._send(200, out)
        m = re.match(r"^/api/export/([0-9a-f]+)$", p)
        if m:
            j = JOBS.get(m.group(1))
            if not j or not j.result: return self._send(404, {"error": "no result"})
            return self._send(200, json.dumps(dict(kind=j.kind, design=j.design, result=j.result)).encode(), "application/json",
                              {"Content-Disposition": f'attachment; filename="drone_sim_{j.kind}_{j.id}.json"'})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path); p = u.path
        try:
            if p == "/api/analyze":
                body = json.loads(self._body() or b"{}")
                return self._send(200, analyze(D.merge(D.DEFAULT, body.get("design", {}))))
            if p == "/api/upload_mesh":
                q = parse_qs(u.query); name = os.path.basename(q.get("name", ["mesh.stl"])[0])
                if not name.lower().endswith((".stl", ".obj")): return self._send(400, {"error": "STL or OBJ only"})
                path = os.path.join(UPLOADS, f"{uuid.uuid4().hex[:6]}_{name}")
                open(path, "wb").write(self._body())
                spec = dict(path=path, role=q.get("role", ["hull"])[0], units=q.get("units", ["mm"])[0],
                            axes=q.get("axes", ["x_aft_z_up"])[0], auto_place=True)
                V, F, info = geometry.import_mesh(spec)
                ext = (V.max(0) - V.min(0)).round(3).tolist()
                return self._send(200, dict(spec=spec, info=info, extent_m=ext))
            if p in ("/api/run", "/api/montecarlo"):
                body = json.loads(self._body() or b"{}")
                design = D.merge(D.DEFAULT, body.get("design", {}))
                scenario = {**copy.deepcopy(DEFAULT_SCENARIO), **body.get("scenario", {})}
                j = Job("voyage" if p == "/api/run" else "montecarlo", design, scenario, body.get("mc", {}))
                JOBS[j.id] = j
                threading.Thread(target=j.run, daemon=True).start()
                return self._send(200, dict(id=j.id))
            m = re.match(r"^/api/job/([0-9a-f]+)/cancel$", p)
            if m and m.group(1) in JOBS:
                JOBS[m.group(1)].cancel = True; return self._send(200, dict(ok=True))
            return self._send(404, {"error": "not found"})
        except Exception as e:
            return self._send(500, {"error": str(e), "trace": traceback.format_exc()})


def main():
    port = int(os.environ.get("DRONE_SIM_PORT", "8765"))
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    url = f"http://127.0.0.1:{port}/"
    print(f"Solar-sail drone simulator running at {url}  (Ctrl+C to stop)")
    print(f"Data cache and results: {WORK}")
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
