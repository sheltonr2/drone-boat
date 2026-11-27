"""Whole-boat STL of Rev E3 (outside parts only), for sharing: GitHub shows .stl files as a 3D model you can spin.

Same geometry as drone_boat_revE3_exterior.glb (export_model.py), snapped to 1 mm, in millimetres with Z up and +X forward, the usual
STL convention. Writes build-files/export/drone_boat_revE3_exterior.stl. Run from the repo root:
    python build-files/source/export_stl.py
"""
import os, struct, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_model import build, OUT  # noqa: E402


def main():
    J, nodes = build()
    tris = []
    for nd in nodes:
        if nd["interior"]: continue
        # export frame (m; X port, Y up, Z forward) -> STL (mm; x forward, y port, z up); a proper rotation, so the
        # winding is unchanged
        P = np.c_[nd["P"][:, 2], nd["P"][:, 0], nd["P"][:, 1]] * 1000.0
        for _, F in nd["prims"]:
            tris.append(P[F])
    # Snap to a 1 mm grid and drop the triangles that collapse: about 30% fewer, so the file stays under 10 MB and
    # GitHub's 3D view loads it. Nothing visible changes at the scale of a 1.5 m boat.
    T = np.round(np.concatenate(tris)).astype(np.float32)
    T = T[~(np.all(T[:, 0] == T[:, 1], 1) | np.all(T[:, 1] == T[:, 2], 1) | np.all(T[:, 0] == T[:, 2], 1))]
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    rec = np.zeros(len(T), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    rec["n"], rec["v"] = n, T
    path = os.path.join(OUT, f"drone_boat_rev{J['version']}_exterior.stl")
    with open(path, "wb") as fh:
        hdr = f"Drone boat Rev {J['version']} exterior, mm, z up, x forward; github.com/sheltonr2/drone-boat (MIT)".encode()[:80]
        fh.write(hdr.ljust(80, b" ")); fh.write(struct.pack("<I", len(T))); fh.write(rec.tobytes())
    print(path, len(T), "triangles", round(os.path.getsize(path) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
