import sys, os, json, time
import numpy as np
from sdf import mesh, write_stl, check_watertight, volume
from decimate import decimate
import parts as Pm

OUT = "out/stl"; os.makedirs(OUT, exist_ok=True)
os.makedirs("out/cache", exist_ok=True)
only = sys.argv[1:]
report = {}
for stem, pid, kw in Pm.BUILD:
    if only and stem not in only and pid not in only:
        continue
    t0 = time.time()
    f, bounds = Pm.PARTS[pid]['build'](**kw)
    size = max(b[1] - b[0] for b in bounds)
    res = 0.25 if size < 70 else (0.35 if size < 130 else 0.45)
    v0, fc0, grid = mesh(f, bounds, res=res)
    v, fc = decimate(v0, fc0, max_err=0.03)
    ok, bad = check_watertight(fc)
    write_stl(f"{OUT}/{stem}.stl", v, fc, stem)
    xs, ys, zs, vol = grid
    np.savez_compressed(f"out/cache/{stem}.npz", xs=xs, ys=ys, zs=zs, vol=(vol < 0))
    ext = (v.max(0) - v.min(0)).round(1).tolist()
    report[stem] = dict(pid=pid, tris=len(fc), watertight=ok, bad_edges=bad, extent=ext,
                        volume_cm3=round(volume(v, fc) / 1000, 1), res=res, sec=round(time.time() - t0, 1))
    print(stem, report[stem], flush=True)
prev = {}
if os.path.exists("out/stl_report.json"):
    prev = json.load(open("out/stl_report.json"))
prev.update(report)
json.dump(prev, open("out/stl_report.json", "w"), indent=1)
