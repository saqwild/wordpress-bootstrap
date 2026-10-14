"""Render every frame in parallel chunks (resumable: finished frames are skipped).

  python3 render_all.py --python venv/bin/python --build <dir> [--jobs 3] [--chunks 12]
"""
import argparse
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--python", required=True, help="interpreter with the bpy module")
    ap.add_argument("--build", required=True)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--chunks", type=int, default=12)
    args = ap.parse_args()

    build = pathlib.Path(args.build)
    n = json.loads((build / "timeline.json").read_text())["frames"]
    size = -(-n // args.chunks)
    ranges = [(a, min(a + size, n)) for a in range(0, n, size)]

    def done(a, b):
        return (build / f"anchors_{a:05d}_{b:05d}.json").exists()

    def run(r):
        a, b = r
        if done(a, b):
            return f"{a}-{b} already done"
        log = open(build / f"log_{a:05d}.txt", "w")
        rc = subprocess.call([args.python, str(HERE / "lock.py"), "--build", str(build), "--frames", str(a), str(b)],
                             stdout=log, stderr=subprocess.STDOUT)
        return f"{a}-{b} exit {rc}"

    with ThreadPoolExecutor(args.jobs) as pool:
        for msg in pool.map(run, ranges):
            print(msg, flush=True)
    missing = [r for r in ranges if not done(*r)]
    print("ALL DONE" if not missing else f"MISSING {missing}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
