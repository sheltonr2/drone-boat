"""Write a HURDAT2 best-track subset for the simulator's storm-encounter check (drone_sim/storms.py).

The original subset (hurdat2_atlantic_1981-2025_box.csv) covers 20-62N, 85W-5E: the eastbound route.
The east-west study (docs/East_West_Study.md) crosses the tropics, where most storms form, so it needs
the tropical box. This script makes that file the same way:

    python make_hurdat_subset.py                       # downloads the newest HURDAT2 file from NOAA NHC
    python make_hurdat_subset.py hurdat2-1851-2025.txt # or uses a file you already have

Output: hurdat2_atlantic_1981-2025_tropics.csv next to this script (0-45N, 90W-5E, 1981-2025, synoptic times).
HURDAT2 is public domain (NOAA National Hurricane Center).
"""
import os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = "https://www.nhc.noaa.gov/data/hurdat/"
BOX = dict(lat=(0.0, 45.0), lon=(-90.0, 5.0))
YEARS = (1981, 2025)
OUT = os.path.join(HERE, "hurdat2_atlantic_1981-2025_tropics.csv")


def fetch():
    html = urllib.request.urlopen(INDEX, timeout=60).read().decode("utf-8", "replace")
    names = sorted(set(re.findall(r"hurdat2-1851-(\d{4})-(\d{6})\.txt", html)))
    if not names:
        sys.exit("No hurdat2-1851-*.txt file found on " + INDEX)
    yr, stamp = max(names, key=lambda n: (n[0], n[1][4:6] + n[1][0:4]))   # newest season, then newest date (MMDDYY)
    fn = f"hurdat2-1851-{yr}-{stamp}.txt"
    print("Downloading", INDEX + fn)
    data = urllib.request.urlopen(INDEX + fn, timeout=300).read().decode("utf-8", "replace")
    return fn, data


def main():
    if len(sys.argv) > 1:
        fn = os.path.basename(sys.argv[1]); data = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    else:
        fn, data = fetch()
    rows, sid = [], None
    for line in data.splitlines():
        f = [x.strip() for x in line.split(",")]
        if len(f) >= 3 and f[0][:2] in ("AL", "EP", "CP") and len(f[0]) == 8:
            sid = f[0]; continue
        if len(f) < 7 or sid is None or not f[0].isdigit():
            continue
        y = int(f[0][:4])
        if not (YEARS[0] <= y <= YEARS[1]) or f[1] not in ("0000", "0600", "1200", "1800"):
            continue
        lat = float(f[4][:-1]) * (1 if f[4][-1] == "N" else -1)
        lon = float(f[5][:-1]) * (-1 if f[5][-1] == "W" else 1)
        if not (BOX["lat"][0] <= lat <= BOX["lat"][1] and BOX["lon"][0] <= lon <= BOX["lon"][1]):
            continue
        ts = f"{f[0][:4]}-{f[0][4:6]}-{f[0][6:8]}T{f[1][:2]}:{f[1][2:]}Z"
        rows.append(f"{sid},{ts},{lat},{lon},{int(f[6])},{f[3]}")
    with open(OUT, "w", newline="\n") as o:
        o.write(f"# NOAA NHC HURDAT2 Atlantic best tracks ({fn}), public domain.\n")
        o.write(f"# Subset: {YEARS[0]}-{YEARS[1]}, synoptic times (00/06/12/18 UTC), points inside "
                f"{BOX['lat'][0]:.0f}-{BOX['lat'][1]:.0f}N, {-BOX['lon'][0]:.0f}W-{BOX['lon'][1]:.0f}E. "
                "Wind = 1-min max sustained (kt), -99 = missing.\n")
        o.write("# Status: TD TS HU tropical; SD SS subtropical; EX extratropical; LO low; WV wave; DB disturbance.\n")
        o.write("storm_id,time_utc,lat,lon,max_wind_kt,status\n")
        o.write("\n".join(rows) + "\n")
    print(f"Wrote {len(rows)} points to {OUT}")


if __name__ == "__main__":
    main()
