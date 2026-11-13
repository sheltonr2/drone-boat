"""Compare two Monte Carlo result files, ignoring only run-time fields (wall_s). Exit 0 if identical.
Used by run_speed_check.bat to prove a faster simulator gives exactly the same answers (13 Nov 2026)."""
import json, sys

def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in ("wall_s",)}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x

def first_diff(a, b, path=""):
    if type(a) is not type(b): return f"{path}: {a!r:.80} vs {b!r:.80}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: return f"{path}.{k}: missing on one side"
            d = first_diff(a[k], b[k], f"{path}.{k}")
            if d: return d
    elif isinstance(a, list):
        if len(a) != len(b): return f"{path}: {len(a)} vs {len(b)} items"
        for i, (u, v) in enumerate(zip(a, b)):
            d = first_diff(u, v, f"{path}[{i}]")
            if d: return d
    elif a != b:
        return f"{path}: {a!r:.80} vs {b!r:.80}"
    return None

if __name__ == "__main__":
    a = strip(json.load(open(sys.argv[1]))); b = strip(json.load(open(sys.argv[2])))
    d = first_diff(a, b)
    n = len(a.get("result", {}).get("runs", []))
    if d is None:
        print(f"IDENTICAL: {n} voyages, every field the same apart from run time")
        sys.exit(0)
    print(f"DIFFERENT: first difference at {d}")
    sys.exit(1)
