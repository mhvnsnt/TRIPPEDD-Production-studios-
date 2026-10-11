#!/usr/bin/env python3
"""Sensorium gate — automatic QC gates for every promo/show render.

Runs taste + Goodville style_hold + smell + sync, outputs pass/fail.
This gates by default — no more "could not run."

Usage:
  gate.py --video promo.mp4 [--taste-min 0.35] [--style-min 0.70]

Exit codes: 0 = all gates pass, 1 = one or more gates fail.
Thresholds are QC proxies, not absolute — eye verification is final.

Gates:
  TASTE: mean aesthetic score >= taste-min (default 0.35)
  STYLE: mean Goodville style_hold >= style-min (default 0.70)
  SMELL: no more than 3 severe temporal pops (score > 3.0)
  SYNC:  no "talking head, no speech" / "speech, frozen face" flags
"""
import argparse, subprocess, sys, os, json, tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = "/home/hatch/workspace/tools/sensorium-venv/bin/python"


def sample_frames(video, fps=1.0):
    """Yield (t, bgr) sampled frames."""
    import cv2
    cap = cv2.VideoCapture(video)
    vfps = cap.get(cv2.CAP_PROP_FPS) or 24
    step = max(1, int(round(vfps / fps)))
    idx, out = 0, []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            out.append((idx / vfps, frame))
        idx += 1
    cap.release()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--taste-min", type=float, default=0.35)
    ap.add_argument("--style-min", type=float, default=0.70)
    ap.add_argument("--json", action="store_true", help="JSON report")
    a = ap.parse_args()

    sys.path.insert(0, _HERE)
    from aesthetic import taste_score
    from goodville_style import goodville_style_hold

    report = {"video": a.video, "gates": {}}

    # TASTE + STYLE on sampled frames
    tastes, styles = [], []
    for t, frame in sample_frames(a.video, fps=1.0):
        ts, _ = taste_score(frame)
        tastes.append(float(ts))
        s, _ = goodville_style_hold(frame)
        styles.append(s)
    import numpy as np
    taste_mean = float(np.mean(tastes)) if tastes else 0
    style_mean = float(np.mean(styles)) if styles else 0
    style_min = float(np.min(styles)) if styles else 0
    report["gates"]["taste"] = {
        "mean": round(taste_mean, 3), "threshold": a.taste_min,
        "pass": taste_mean >= a.taste_min}
    report["gates"]["style_hold"] = {
        "mean": round(style_mean, 3), "min": round(style_min, 3),
        "threshold": a.style_min, "pass": style_mean >= a.style_min}

    # SMELL via sensorium CLI (parse temporal pops)
    r = subprocess.run([VENV_PY, os.path.join(_HERE, "sensorium.py"),
                        "smell", a.video],
                       capture_output=True, text=True, timeout=300)
    severe_pops = 0
    for line in r.stdout.splitlines():
        if "temporal pops:" in line:
            # format: "temporal pops: 8.75s(3.374), ..."
            for chunk in line.split("temporal pops:")[1].split(","):
                try:
                    score = float(chunk.split("(")[1].rstrip(")"))
                    if score > 3.0:
                        severe_pops += 1
                except (IndexError, ValueError):
                    pass
    report["gates"]["smell"] = {
        "severe_pops": severe_pops, "pass": severe_pops <= 3}

    # SYNC via sensorium CLI
    import re
    dur = 15.0
    m = re.search(r"duration=(\d+\.?\d*)", subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1", a.video],
        capture_output=True, text=True).stdout)
    if m:
        dur = float(m.group(1))
    r = subprocess.run([VENV_PY, os.path.join(_HERE, "sensorium.py"),
                        "sync", a.video, "0", str(dur)],
                       capture_output=True, text=True, timeout=300)
    flags = []
    for line in r.stdout.splitlines():
        if line.strip().startswith("flags:"):
            inner = line.split("flags:")[1].strip()
            if inner != "[]":
                flags = [inner]
    report["gates"]["sync"] = {"flags": flags, "pass": len(flags) == 0}

    report["pass"] = all(g["pass"] for g in report["gates"].values())

    if a.json:
        print(json.dumps(report, indent=1))
    else:
        for name, g in report["gates"].items():
            mark = "PASS" if g["pass"] else "FAIL"
            print(f"[{mark}] {name}: {g}")
        print(f"\nOVERALL: {'PASS' if report['pass'] else 'FAIL'}")

    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
