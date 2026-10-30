#!/usr/bin/env python3
"""verify_timing.py -- check a MouthSwap timing sheet against Rhubarb.

Independently re-derives the expected mouth shape for every frame from the
RAW Rhubarb JSON cues (frame f shows the shape active at the frame's start
instant, (f-1)/fps; time covered by no cue means X/rest) and compares it
against the per-frame expansion of the bridge's CSV. Exits non-zero and
prints every mismatch if the sheet is not frame-for-frame exact.

Usage:
  python3 verify_timing.py --rhubarb rhubarb.json --csv mouthswap_timing.csv \
      --fps 30 [--blender-dump dump.json]

With --blender-dump (produced by check_blender.py inside Blender) the
per-frame visible shape from the built Blender rig is compared as well.
"""

import argparse
import csv
import json
import math
import sys

EPS = 1e-4


def expected_code(cues, t):
    for s, e, v in cues:
        if s - EPS <= t < e - EPS:
            return v
    return "X"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rhubarb", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--fps", type=int, required=True)
    ap.add_argument("--blender-dump")
    args = ap.parse_args()

    with open(args.rhubarb) as fh:
        data = json.load(fh)
    cues = [(float(c["start"]), float(c["end"]), c["value"].strip().upper())
            for c in data["mouthCues"]]
    duration = float(data["metadata"]["duration"])
    total = int(math.ceil(duration * args.fps - 1e-6))

    csv_map = {}
    with open(args.csv) as fh:
        for row in csv.DictReader(fh):
            for f in range(int(row["frame"]), int(row["frame_end"]) + 1):
                if f in csv_map:
                    print(f"FAIL: frame {f} covered twice in CSV")
                    return 1
                csv_map[f] = row["phoneme"]

    dump = None
    if args.blender_dump:
        with open(args.blender_dump) as fh:
            dump = json.load(fh)
        if dump["fps"] != args.fps:
            print(f"FAIL: Blender scene fps {dump['fps']} != {args.fps}")
            return 1

    mismatches = 0
    for f in range(1, total + 1):
        want = expected_code(cues, (f - 1) / args.fps)
        got_csv = csv_map.get(f)
        if got_csv != want:
            print(f"frame {f}: CSV={got_csv} expected={want}")
            mismatches += 1
        if dump is not None:
            got_b = dump["frames"].get(str(f))
            if got_b != want:
                print(f"frame {f}: Blender={got_b} expected={want}")
                mismatches += 1
    if mismatches:
        print(f"FAIL: {mismatches} mismatched frames out of {total}")
        return 1
    extra = [f for f in csv_map if f > total]
    if extra:
        print(f"FAIL: CSV covers {len(extra)} frames past the audio "
              f"(frames {extra[:5]}...)")
        return 1
    print(f"PASS: {total} frames @ {args.fps}fps match Rhubarb "
          f"frame-for-frame ({len(cues)} raw cues)"
          + (" including the Blender rig" if dump else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
