"""Run 040 (26 Nov 2026): fetch depth and hazard data for the detailed coastlines, on Randolph's PC.

Randolph, 26 Nov 2026: "Add the UK and EMODnet depth data". The detail coasts (make_detail_coast.py) use
OpenStreetMap shorelines everywhere, plus NOAA ENC hazards in the Virgin Islands and off Hatteras. Two gaps:
west Cornwall has no free charts (rocks come from OSM only), and NOAA's charts stop at 64.42W, so Anegada and the
east of the BVI have only OSM reef outlines. This script fetches, standard library only:

1. EMODnet Bathymetry DTM (CC-BY 4.0, ~115 m, 1/16 arc-minute), via its WCS, for each region box. It covers
   European waters; the Caribbean and Hatteras requests are made only to record whether it covers them.
2. UK Hydrographic Office (ADMIRALTY Marine Data Portal, Open Government Licence):
   - a search of the portal's catalogue (wrecks, obstructions, bathymetry, the BVI, Cornwall), saved for review;
   - the service list of its ArcGIS server, saved for review;
   - the Wrecks and Obstructions data set inside our three boxes, from whichever feature layer or file the
     catalogue offers (UKHO is the charting authority for the BVI, so this also covers east of 64.42W);
   - footprints of bathymetry surveys that touch our boxes (with their download details), saved only: the
     surveys themselves can be large, so we pick which to fetch after seeing the list;
   - a bathymetry grid from an image service, if the server has one that answers for our boxes.

Nothing is fetched that the boxes do not need, and no single file over 300 MB is downloaded.
Output: docs/data/coast/raw_040/ and a log. Usage (from the repo root):
    python docs/data/coast/fetch_depth_data.py --out docs/data/coast/raw_040 --log collab/run_log_040_depth_data.txt
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request

BOXES = {  # name: (lat0, lat1, lon0, lon1), the same boxes as make_detail_coast.py
    "cornwall": (49.78, 50.55, -6.55, -3.95),
    "carib": (17.62, 18.88, -65.12, -64.17),
    "hatteras": (34.83, 35.92, -76.25, -75.03),
}
EMOD = "https://ows.emodnet-bathymetry.eu/wcs"
UKHO_PORTAL = "https://datahub.admiralty.co.uk/portal/sharing/rest"
UKHO_SERVER = "https://datahub.admiralty.co.uk/server/rest/services"
MAX_BYTES = 300 * 1024 * 1024
UA = {"User-Agent": "drone-boat-sim/1.0 (github.com/sheltonr2/drone-boat; coastline hazard model)"}

LOGF = None
def log(msg):
    line = time.strftime("%H:%M:%S ") + str(msg)
    print(line, flush=True)
    if LOGF:
        with open(LOGF, "a", encoding="utf-8") as f: f.write(line + "\n")


def get(url, params=None, timeout=180, max_bytes=MAX_BYTES):
    if params: url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, safe=",():")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        n = r.headers.get("Content-Length")
        if n and int(n) > max_bytes: raise IOError(f"too large ({int(n)/1e6:.0f} MB): {url}")
        chunks, total = [], 0
        while True:
            b = r.read(1 << 20)
            if not b: break
            total += len(b)
            if total > max_bytes: raise IOError(f"too large (> {max_bytes/1e6:.0f} MB): {url}")
            chunks.append(b)
        return b"".join(chunks), r.headers.get("Content-Type", "")


def get_json(url, params=None, **kw):
    data, _ = get(url, params, **kw)
    return json.loads(data.decode("utf-8", "replace"))


def save(out, name, data):
    p = os.path.join(out, name)
    with open(p, "wb" if isinstance(data, bytes) else "w", **({} if isinstance(data, bytes) else {"encoding": "utf-8"})) as f:
        f.write(data if isinstance(data, (bytes, str)) else json.dumps(data, indent=1))
    log(f"  saved {name} ({os.path.getsize(p)/1e6:.2f} MB)")
    return p


def is_tiff(b): return b[:4] in (b"II*\x00", b"MM\x00*")


# ---------------------------------------------------------------- 1. EMODnet DTM
def emodnet(out, summary):
    log("== EMODnet Bathymetry DTM (WCS)")
    for name, (la0, la1, lo0, lo1) in BOXES.items():
        tries = [
            ("WCS 2.0.1", dict(service="WCS", version="2.0.1", request="GetCoverage", coverageId="emodnet__mean",
                               format="image/tiff", subset=None)),
            ("WCS 1.0.0", dict(service="WCS", version="1.0.0", request="GetCoverage", coverage="emodnet:mean",
                               crs="EPSG:4326", BBOX=f"{lo0},{la0},{lo1},{la1}", format="image/tiff",
                               interpolation="nearest", resx=f"{1/960:.10f}", resy=f"{1/960:.10f}")),
        ]
        got = None
        for label, p in tries:
            try:
                if p.get("subset", 0) is None:
                    p = dict(p); p.pop("subset")
                    url = EMOD + "?" + urllib.parse.urlencode(p) + f"&subset=Lat({la0},{la1})&subset=Long({lo0},{lo1})"
                    data, ctype = get(url)
                else:
                    data, ctype = get(EMOD, p)
                if is_tiff(data):
                    got = save(out, f"emodnet_dtm_{name}.tif", data); summary["emodnet"][name] = dict(ok=True, via=label, file=os.path.basename(got))
                    break
                log(f"  {name} {label}: not a TIFF ({ctype}): {data[:300]!r}")
            except Exception as e:  # noqa: BLE001
                log(f"  {name} {label}: {type(e).__name__}: {str(e)[:300]}")
        if not got: summary["emodnet"][name] = dict(ok=False)


# ---------------------------------------------------------------- 2. UKHO
def ukho_catalogue(out, summary):
    log("== UKHO ADMIRALTY Marine Data Portal: catalogue search")
    items = {}
    for q in ["wrecks", "obstructions", "wrecks and obstructions", "bathymetry", "bathymetry survey",
              "Virgin Islands", "Anegada", "Cornwall", "Lizard", "Overseas Territories"]:
        try:
            r = get_json(UKHO_PORTAL + "/search", dict(q=q, f="json", num=100))
            for it in r.get("results", []):
                items[it["id"]] = {k: it.get(k) for k in ("id", "title", "type", "url", "size", "snippet", "licenseInfo",
                                                           "extent", "modified", "typeKeywords", "access")}
            log(f"  '{q}': {r.get('total', 0)} items")
        except Exception as e:  # noqa: BLE001
            log(f"  '{q}': {type(e).__name__}: {str(e)[:300]}")
    save(out, "ukho_catalogue.json", list(items.values()))
    summary["ukho"]["catalogue_items"] = len(items)
    return list(items.values())


def ukho_services(out, summary):
    log("== UKHO ArcGIS server: service list")
    found = []
    try:
        root = get_json(UKHO_SERVER, dict(f="json"))
        folders = [""] + root.get("folders", [])
        for fo in folders:
            try:
                r = root if fo == "" else get_json(f"{UKHO_SERVER}/{fo}", dict(f="json"))
                for s in r.get("services", []):
                    url = f"{UKHO_SERVER}/{s['name']}/{s['type']}"
                    entry = dict(name=s["name"], type=s["type"], url=url, layers=[])
                    if s["type"] in ("FeatureServer", "MapServer"):
                        try:
                            info = get_json(url, dict(f="json"))
                            entry["layers"] = [dict(id=l["id"], name=l.get("name")) for l in info.get("layers", [])]
                        except Exception as e:  # noqa: BLE001
                            entry["error"] = str(e)[:200]
                    found.append(entry)
            except Exception as e:  # noqa: BLE001
                log(f"  folder {fo}: {type(e).__name__}: {str(e)[:200]}")
    except Exception as e:  # noqa: BLE001
        log(f"  service list: {type(e).__name__}: {str(e)[:300]}")
    save(out, "ukho_services.json", found)
    summary["ukho"]["services"] = len(found)
    return found


def query_layer(layer_url, box, tag):
    """All features of an ArcGIS feature/map layer inside a box, as GeoJSON, paging through the results."""
    la0, la1, lo0, lo1 = box
    feats, offset = [], 0
    for _ in range(300):
        p = dict(where="1=1", geometry=f"{lo0},{la0},{lo1},{la1}", geometryType="esriGeometryEnvelope", inSR="4326",
                 spatialRel="esriSpatialRelIntersects", outFields="*", outSR="4326", f="geojson",
                 resultOffset=offset, resultRecordCount=1000)
        r = get_json(layer_url + "/query", p)
        if "error" in r: raise IOError(json.dumps(r["error"])[:300])
        fs = r.get("features", [])
        feats += fs
        more = r.get("exceededTransferLimit") or (r.get("properties") or {}).get("exceededTransferLimit")
        if not fs or (not more and len(fs) < 1000): break
        offset += len(fs)
    log(f"    {tag}: {len(feats)} features")
    return dict(type="FeatureCollection", features=feats)


def ukho_wrecks(out, summary, items, services):
    log("== UKHO Wrecks and Obstructions")
    done = False
    layers = []
    for s in services:
        for l in s.get("layers", []):
            if re.search(r"wreck|obstruct", f"{s['name']} {l.get('name')}", re.I):
                layers.append((f"{s['url']}/{l['id']}", f"{s['name']} / {l.get('name')}"))
    for it in items:
        if re.search(r"wreck|obstruct", it.get("title") or "", re.I) and it.get("url") and it.get("type") in ("Feature Service", "Map Service"):
            u = it["url"].rstrip("/")
            if re.search(r"/\d+$", u): layers.append((u, it["title"]))
            else:
                try:
                    info = get_json(u, dict(f="json"))
                    layers += [(f"{u}/{l['id']}", f"{it['title']} / {l.get('name')}") for l in info.get("layers", [])]
                except Exception as e:  # noqa: BLE001
                    log(f"  {it['title']}: {str(e)[:200]}")
    seen = set()
    for url, title in layers:
        if url in seen: continue
        seen.add(url)
        log(f"  layer: {title} ({url})")
        res = {}
        try:
            for name, box in BOXES.items():
                fc = query_layer(url, box, name)
                res[name] = len(fc["features"])
                if fc["features"]:   # name from the layer URL (service + layer id), so two layers never share a file
                    m = re.search(r"/services/(.+?)/(?:Feature|Map)Server/(\d+)", url)
                    safe = re.sub(r"[^A-Za-z0-9]+", "_", f"{m.group(1)}_{m.group(2)}" if m else title).strip("_")[-60:]
                    save(out, f"ukho_wrecks_{safe}_{name}.geojson", json.dumps(fc))
                    done = True
        except Exception as e:  # noqa: BLE001
            log(f"    query failed: {type(e).__name__}: {str(e)[:300]}")
        summary["ukho"].setdefault("wreck_layers", {})[title] = res
    if not done:   # no queryable layer: try a downloadable file item instead
        for it in items:
            if re.search(r"wreck|obstruct", it.get("title") or "", re.I) and it.get("type") in (
                    "CSV", "Shapefile", "File Geodatabase", "GeoJson", "Microsoft Excel", "Code Attachment", "ZIP"):
                if it.get("size") and it["size"] > MAX_BYTES:
                    log(f"  {it['title']}: {it['size']/1e6:.0f} MB, over the limit; not downloaded"); continue
                try:
                    data, _ = get(f"{UKHO_PORTAL}/content/items/{it['id']}/data")
                    ext = {"CSV": "csv", "GeoJson": "geojson", "Microsoft Excel": "xlsx"}.get(it["type"], "zip")
                    save(out, f"ukho_wrecks_item_{it['id']}.{ext}", data)
                    summary["ukho"]["wreck_file"] = it["title"]; done = True
                    break
                except Exception as e:  # noqa: BLE001
                    log(f"  {it['title']}: {type(e).__name__}: {str(e)[:300]}")
    summary["ukho"]["wrecks_ok"] = done


def ukho_surveys(out, summary, items, services):
    log("== UKHO bathymetry surveys: footprints in our boxes (list only)")
    layers = []
    for s in services:
        for l in s.get("layers", []):
            if re.search(r"bathy|survey|DAC|HI\d|surface", f"{s['name']} {l.get('name')}", re.I):
                layers.append((f"{s['url']}/{l['id']}", f"{s['name']} / {l.get('name')}"))
    for it in items:
        if re.search(r"bathy|survey", it.get("title") or "", re.I) and it.get("type") == "Feature Service" and it.get("url"):
            u = it["url"].rstrip("/")
            layers.append((u if re.search(r"/\d+$", u) else u + "/0", it["title"]))
    seen, n = set(), 0
    for url, title in layers[:40]:
        if url in seen: continue
        seen.add(url)
        log(f"  layer: {title}")
        try:
            for name, box in BOXES.items():
                fc = query_layer(url, box, name)
                if fc["features"]:
                    m = re.search(r"/services/(.+?)/(?:Feature|Map)Server/(\d+)", url)
                    safe = re.sub(r"[^A-Za-z0-9]+", "_", f"{m.group(1)}_{m.group(2)}" if m else title).strip("_")[-60:]
                    save(out, f"ukho_surveys_{safe}_{name}.geojson", json.dumps(fc)); n += 1
        except Exception as e:  # noqa: BLE001
            log(f"    query failed: {type(e).__name__}: {str(e)[:200]}")
    summary["ukho"]["survey_footprint_files"] = n


def ukho_grids(out, summary, services):
    log("== UKHO bathymetry image services (grids)")
    for s in services:
        if s["type"] != "ImageServer" or not re.search(r"bathy|depth|dtm|surface", s["name"], re.I): continue
        for name, (la0, la1, lo0, lo1) in BOXES.items():
            w = min(4000, int((lo1 - lo0) * 1800)); h = min(4000, int((la1 - la0) * 1800))   # ~2 arc-seconds
            try:
                data, ctype = get(s["url"] + "/exportImage", dict(bbox=f"{lo0},{la0},{lo1},{la1}", bboxSR=4326, imageSR=4326,
                                                                  size=f"{w},{h}", format="tiff", pixelType="F32",
                                                                  noData=-99999, interpolation="RSP_NearestNeighbor", f="image"))
                if is_tiff(data):
                    safe = re.sub(r"[^A-Za-z0-9]+", "_", s["name"]).strip("_")[:50]
                    save(out, f"ukho_grid_{safe}_{name}_{w}x{h}.tif", data)
                    summary["ukho"].setdefault("grids", []).append(f"{s['name']} {name}")
                else:
                    log(f"  {s['name']} {name}: not a TIFF ({ctype}) {data[:200]!r}")
            except Exception as e:  # noqa: BLE001
                log(f"  {s['name']} {name}: {type(e).__name__}: {str(e)[:200]}")


def main():
    global LOGF
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/data/coast/raw_040")
    ap.add_argument("--log", default=None)
    ap.add_argument("--only", choices=["wrecks"], default=None, help="wrecks: only re-fetch the UKHO Wrecks and Obstructions (run 040c)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    LOGF = a.log
    log(f"Run 040: depth and hazard data -> {a.out}")
    summary = dict(started=time.strftime("%Y-%m-%d %H:%M:%S"), emodnet={}, ukho={})
    if a.only == "wrecks":   # run 040c: the 040 points file was overwritten by the area layer (same truncated name)
        services = ukho_services(a.out, summary)
        ukho_wrecks(a.out, summary, [], services)
        summary["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save(a.out, "summary_040c.json", summary); log("Summary: " + json.dumps(summary)); return
    steps = [("EMODnet", lambda: emodnet(a.out, summary))]
    for label, fn in steps:
        try: fn()
        except Exception as e: log(f"{label} failed: {e}")  # noqa: BLE001
    items, services = [], []
    try: items = ukho_catalogue(a.out, summary)
    except Exception as e: log(f"catalogue failed: {e}")  # noqa: BLE001
    try: services = ukho_services(a.out, summary)
    except Exception as e: log(f"services failed: {e}")  # noqa: BLE001
    for label, fn in [("wrecks", lambda: ukho_wrecks(a.out, summary, items, services)),
                      ("surveys", lambda: ukho_surveys(a.out, summary, items, services)),
                      ("grids", lambda: ukho_grids(a.out, summary, services))]:
        try: fn()
        except Exception as e: log(f"{label} failed: {e}")  # noqa: BLE001
    summary["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save(a.out, "summary.json", summary)
    log("Summary: " + json.dumps(summary))


if __name__ == "__main__":
    sys.exit(main())
