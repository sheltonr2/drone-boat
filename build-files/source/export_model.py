"""Export the 3D viewer model (build-files/viewer/model.json) as glTF binary (.glb) and Wavefront OBJ (+ .mtl)
for game engines and other tools, e.g. Bluewater in jcolter11374/boat-sim.

Run from anywhere:  python build-files/source/export_model.py
Writes build-files/export/drone_boat_revE3.glb (all 99 parts), drone_boat_revE3_exterior.glb (outside parts only),
drone_boat_revE3.obj with drone_boat_revE3.mtl, and parts.csv.

Frame of the exported files (glTF convention, right-handed):
  +Y up, +Z forward (towards the bow), +X to port; metres.
  Origin: on the centreline, at midships (750 mm aft of the bow) and at the design waterline (106 mm above the hull bottom).
The design frame (design.py) is x aft from the bow, y to port, z up from the hull bottom, in millimetres, which is
left-handed, so the mapping X = y, Y = z - DWL, Z = 750 - x mirrors it and the triangle winding is flipped to keep
outward faces outward. Each placed component becomes one node (99 in Rev E3) with its transform baked into the
vertices, so every node sits at the identity and the file needs no negative-determinant matrices.
"""
import base64, csv, json, os, struct
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "viewer", "model.json")
OUT = os.path.join(ROOT, "export")

# Base colours from the viewer (build-files/viewer/index.html, MAT), as sRGB hex, with roughness and metalness.
COL = {
    "hull_orange": ("#ff5b12", 0.30, 0.0), "hull_boot": ("#f4f4f0", 0.30, 0.0), "antifoul": ("#55160f", 0.78, 0.0),
    "deck": ("#d9ddd9", 0.82, 0.0), "deckpaint": ("#e3e6e2", 0.82, 0.0), "wing": ("#f7f7f4", 0.28, 0.0),
    "carbon": ("#1b1d21", 0.35, 0.0), "frp": ("#e7e1c8", 0.42, 0.0), "lead": ("#5f646b", 0.55, 0.7),
    "white": ("#f1f1ee", 0.45, 0.0), "petg": ("#3d6a86", 0.36, 0.0), "asa": ("#efefea", 0.58, 0.0),
    "pla": ("#d8b25c", 0.50, 0.0), "black": ("#141516", 0.50, 0.0), "lamp": ("#ffffff", 0.15, 0.0),
    "steel": ("#c9cdd2", 0.22, 1.0), "darkgrey": ("#33373d", 0.60, 0.0), "yellow": ("#ffc81a", 0.42, 0.0),
    "pvc": ("#d6d7d2", 0.48, 0.0), "alu": ("#b4bac2", 0.34, 0.9), "brass": ("#c9a45c", 0.30, 1.0),
    "h80": ("#dccb7c", 0.70, 0.0), "ply": ("#c79f69", 0.68, 0.0), "glass": ("#b9c9b0", 0.35, 0.0),
    "g10": ("#b9c66a", 0.40, 0.0), "xps": ("#86b8e8", 0.90, 0.0), "glassbox": ("#ddd5bd", 0.50, 0.0),
    "battery": ("#2a3a52", 0.45, 0.0), "hammond": ("#8b9399", 0.38, 0.0), "clearlid": ("#d8ecff", 0.05, 0.0),
    "pcb": ("#1f6b3a", 0.40, 0.0), "pcbblue": ("#1a4c8f", 0.40, 0.0), "pcbred": ("#9f1c1c", 0.40, 0.0),
    "solar": ("#1b2a4a", 0.20, 0.0),
}
ALPHA = {"xps": 0.38, "clearlid": 0.28, "lamp": 0.92}
EMISSIVE = {"lamp": "#fff4d6"}


def lin(hexcol):
    """sRGB hex to linear RGB (glTF base colours are linear)."""
    c = np.array([int(hexcol[i:i + 2], 16) / 255.0 for i in (1, 3, 5)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def load():
    J = json.load(open(SRC))
    blob = base64.b64decode(J["bin"])
    G = {}
    for k, g in J["geoms"].items():
        q = np.frombuffer(blob, np.int16, g["nv"] * 3, g["pos"]).reshape(-1, 3).astype(np.float64)
        v = (q + 32768.0) * np.array(g["sc"]) + np.array(g["lo"])
        n = np.frombuffer(blob, np.int8, g["nv"] * 3, g["nrm"]).reshape(-1, 3).astype(np.float64) / 127.0
        f = np.frombuffer(blob, np.uint16 if g["it"] == 16 else np.uint32, g["nf"] * 3, g["idx"]).reshape(-1, 3).astype(np.int64)
        G[k] = (v, n, f)
    return J, G


def to_out(v, dwl, mid):
    """Design frame (mm, x aft, y port, z up from bottom) to export frame (m, X port, Y up from DWL, Z forward)."""
    return np.c_[v[:, 1], v[:, 2] - dwl, mid - v[:, 0]] / 1000.0


def build():
    J, G = load()
    dwl, mid = J["dwl"], J["L"] / 2.0
    nodes = []          # (id, name, group, interior, info, ref, [(mat, pos, nrm, idx)])
    for a in J["assembly"]:
        v, n, f = G[a["geom"]]
        M = np.array(a["m"], dtype=np.float64).reshape(4, 4).T      # three.js fromArray is column-major
        vw = v @ M[:3, :3].T + M[:3, 3]
        nw = n @ M[:3, :3].T
        nw /= np.maximum(np.linalg.norm(nw, axis=1, keepdims=True), 1e-9)
        P = to_out(vw, dwl, mid).astype(np.float32)
        N = np.c_[nw[:, 1], nw[:, 2], -nw[:, 0]].astype(np.float32)
        # The export frame mirrors the design frame, so the winding flips; a placement that itself mirrors
        # (negative determinant, as for some printed parts) flips it back.
        F = f if np.linalg.det(M[:3, :3]) < 0 else f[:, [0, 2, 1]]
        mat = a["mat"]
        prims = []
        if mat == "hull":
            # The viewer paints the hull in a shader: antifouling to 14 mm above the DWL, a 13 mm white boot stripe,
            # hi-vis orange above. Here the triangles are split by their centroid height instead.
            zc = vw[f].mean(axis=1)[:, 2]
            for m2, sel in (("antifoul", zc < dwl + 14), ("hull_boot", (zc >= dwl + 14) & (zc < dwl + 27)),
                            ("hull_orange", zc >= dwl + 27)):
                if sel.any():
                    prims.append((m2, F[sel]))
        else:
            prims.append((mat if mat in COL else "white", F))
        nodes.append(dict(id=a["id"], name=a["name"], group=a["group"], interior=bool(a.get("interior")),
                          info=a.get("info", ""), ref=a.get("ref", ""), P=P, N=N, prims=prims))
    return J, nodes


def write_glb(J, nodes, path):
    mats = sorted({m for nd in nodes for m, _ in nd["prims"]})
    mi = {m: i for i, m in enumerate(mats)}
    materials = []
    for m in mats:
        hx, rough, metal = COL[m]
        bc = list(lin(hx)) + [ALPHA.get(m, 1.0)]
        md = dict(name=m, pbrMetallicRoughness=dict(baseColorFactor=[round(x, 5) for x in bc], roughnessFactor=rough, metallicFactor=metal))
        if m in ALPHA:
            md["alphaMode"] = "BLEND"
        if m in EMISSIVE:
            md["emissiveFactor"] = [round(x, 5) for x in lin(EMISSIVE[m])]
        if m in ("hull_orange", "hull_boot", "antifoul"):
            md["doubleSided"] = True        # the hull is an open shell; its inside is visible in cut-away views
        materials.append(md)
    buf = bytearray(); views = []; accs = []; meshes = []; gnodes = []

    def add_view(data, target):
        while len(buf) % 4:
            buf.append(0)
        off = len(buf); buf.extend(data)
        views.append(dict(buffer=0, byteOffset=off, byteLength=len(data), target=target))
        return len(views) - 1

    for nd in nodes:
        P, N = nd["P"], nd["N"]
        pv = add_view(P.tobytes(), 34962)
        accs.append(dict(bufferView=pv, componentType=5126, count=len(P), type="VEC3",
                         min=[float(x) for x in P.min(0)], max=[float(x) for x in P.max(0)]))
        pa = len(accs) - 1
        nv = add_view(N.tobytes(), 34962)
        accs.append(dict(bufferView=nv, componentType=5126, count=len(N), type="VEC3"))
        na = len(accs) - 1
        prims = []
        for m, F in nd["prims"]:
            idx = F.astype(np.uint32).ravel()
            iv = add_view(idx.tobytes(), 34963)
            accs.append(dict(bufferView=iv, componentType=5125, count=len(idx), type="SCALAR"))
            prims.append(dict(attributes=dict(POSITION=pa, NORMAL=na), indices=len(accs) - 1, material=mi[m], mode=4))
        meshes.append(dict(name=nd["id"], primitives=prims))
        gnodes.append(dict(name=nd["id"], mesh=len(meshes) - 1,
                           extras=dict(label=nd["name"], group=nd["group"], interior=nd["interior"], info=nd["info"], drawing_ref=nd["ref"])))
    root = dict(name="drone_boat_rev" + J["version"], children=list(range(len(gnodes))),
                extras=dict(units="metres", up="+Y", forward="+Z (bow)", port="+X",
                            origin="centreline, midships (750 mm aft of the bow), design waterline",
                            length_m=J["L"] / 1000, mass_kg=J["mass"], revision=J["version"], date=J["date"],
                            source="https://github.com/sheltonr2/drone-boat (build-files/viewer/model.json)", license="MIT"))
    gnodes.append(root)
    gltf = dict(asset=dict(version="2.0", generator="drone-boat build-files/source/export_model.py",
                           copyright="Randolph Shelton, MIT licence"),
                scene=0, scenes=[dict(name="drone_boat", nodes=[len(gnodes) - 1])], nodes=gnodes, meshes=meshes,
                materials=materials, accessors=accs, bufferViews=views, buffers=[dict(byteLength=len(buf))])
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    while len(buf) % 4:
        buf.append(0)
    with open(path, "wb") as fh:
        fh.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(buf)))
        fh.write(struct.pack("<II", len(js), 0x4E4F534A)); fh.write(js)
        fh.write(struct.pack("<II", len(buf), 0x004E4942)); fh.write(bytes(buf))


def write_obj(J, nodes, path_obj, path_mtl):
    mats = sorted({m for nd in nodes for m, _ in nd["prims"]})
    with open(path_mtl, "w") as fh:
        fh.write(f"# Drone boat Rev {J['version']} materials (sRGB colours)\n")
        for m in mats:
            hx, rough, metal = COL[m]
            c = [int(hx[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
            fh.write(f"\nnewmtl {m}\nKd {c[0]:.4f} {c[1]:.4f} {c[2]:.4f}\nKa 0 0 0\nKs 0.04 0.04 0.04\nd {ALPHA.get(m, 1.0)}\nillum 2\n")
    with open(path_obj, "w") as fh:
        fh.write(f"# Drone boat Rev {J['version']} ({J['date']}), from github.com/sheltonr2/drone-boat, MIT licence\n")
        fh.write("# Metres; +Y up, +Z forward (bow), +X port; origin on the centreline at midships and the design waterline.\n")
        fh.write(f"mtllib {os.path.basename(path_mtl)}\n")
        base = 1
        for nd in nodes:
            fh.write(f"o {nd['id']}\n")
            fh.write("".join(f"v {x:.5f} {y:.5f} {z:.5f}\n" for x, y, z in nd["P"]))
            fh.write("".join(f"vn {x:.4f} {y:.4f} {z:.4f}\n" for x, y, z in nd["N"]))
            for m, F in nd["prims"]:
                fh.write(f"usemtl {m}\n")
                G = F + base
                fh.write("".join(f"f {a}//{a} {b}//{b} {c}//{c}\n" for a, b, c in G))
            base += len(nd["P"])


def main():
    os.makedirs(OUT, exist_ok=True)
    J, nodes = build()
    stem = "drone_boat_rev" + J["version"]
    write_glb(J, nodes, os.path.join(OUT, stem + ".glb"))
    write_obj(J, nodes, os.path.join(OUT, stem + ".obj"), os.path.join(OUT, stem + ".mtl"))
    # A lighter file for games: only what shows from outside (no interior structure, electronics or hidden fittings).
    write_glb(J, [nd for nd in nodes if not nd["interior"]], os.path.join(OUT, stem + "_exterior.glb"))
    with open(os.path.join(OUT, "parts.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["node", "name", "group", "interior", "materials", "triangles", "drawing_ref", "info"])
        for nd in nodes:
            w.writerow([nd["id"], nd["name"], nd["group"], nd["interior"], " ".join(m for m, _ in nd["prims"]),
                        sum(len(F) for _, F in nd["prims"]), nd["ref"], nd["info"]])
    allP = np.vstack([nd["P"] for nd in nodes])
    tris = sum(len(F) for nd in nodes for _, F in nd["prims"])
    print(f"{len(nodes)} nodes, {tris} triangles; bounds (m) min {allP.min(0).round(3)} max {allP.max(0).round(3)}")
    for f in sorted(os.listdir(OUT)):
        print(f"  {f}: {os.path.getsize(os.path.join(OUT, f)) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
