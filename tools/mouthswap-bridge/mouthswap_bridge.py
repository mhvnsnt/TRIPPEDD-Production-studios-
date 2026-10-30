#!/usr/bin/env python3
"""mouthswap_bridge.py -- Rhubarb Lip Sync -> timed mouth-swap plan (SPEC T-2).

The bridge between Rhubarb (which outputs *when* each mouth shape happens)
and the shows' mouth-drawing libraries (which hold the shapes as images).
Until now, turning Rhubarb's phoneme timings into exposed mouth drawings
was hand work. This tool automates it.

Inputs (pick one audio source):
  --audio FILE          a voice recording in any format ffmpeg reads; the
                        bridge converts it and runs Rhubarb itself
  --rhubarb FILE        an existing Rhubarb output (.json or .tsv)

Plus, always:
  --mouth-dir DIR       folder of mouth images named by Rhubarb shape code
                        (A B C D E F G H X). A file matches a code when its
                        stem is the code itself or starts with the code
                        followed by '_' or '-' (e.g. A.png, B_open.png,
                        mouth-C.png does NOT match -- the code must lead).
  --fps N               scene frame rate the plan is keyed at (default 30)

Outputs (all written into --out DIR):
  mouthswap_timing.csv  one row per mouth exposure:
                        frame, frame_end, phoneme, mouth_file, start_s, end_s
                        This is the exposure/timing sheet for the 2D side
                        (ffmpeg compositing, Tahoma2D cell mapping).
  mouthswap_plan.json   the same plan in machine form (fps, total frames,
                        resolved absolute mouth image paths per cue).
  mouthswap_blender.py  a self-contained Blender script (plan embedded).
                        Run it in Blender and it builds the timed swap:
                        one image plane per mouth shape, visibility keyed
                        frame-accurately at the scene fps.

Frame convention (used everywhere in this tool):
  Frames are 1-based. Frame f covers the time interval
  [(f-1)/fps, f/fps), and it exposes the mouth shape that is active at
  the frame's start instant, (f-1)/fps. Cues are gap-filled with shape X
  (rest) before framing, so every frame gets exactly one shape; a cue
  shorter than one frame that contains no frame start is absorbed by its
  neighbours (standard exposure practice at the scene fps). The CSV's
  start_s/end_s are the frame-quantized times.

Original implementation, written for TRIPPEDD Production Studios.
Rhubarb Lip Sync is by Daniel S. Wolf (MIT-style license); this bridge only
consumes its documented output formats and invokes its CLI.
"""

import argparse
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

SHAPES = ["A", "B", "C", "D", "E", "F", "G", "H", "X"]
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp")
EPS = 1e-6

DEFAULT_RHUBARB = os.path.expanduser("~/workspace/tools/rhubarb/rhubarb")
HERE = os.path.dirname(os.path.abspath(__file__))


def die(msg):
    print(f"mouthswap_bridge: error: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- audio side

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"command failed: {' '.join(cmd)}\n{r.stderr[-1500:]}")
    return r


def run_rhubarb(rhubarb_bin, audio, dialog, recognizer, workdir):
    """Convert audio to 16kHz mono WAV (Rhubarb's requirement) and run it."""
    wav = os.path.join(workdir, "audio_16k.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", audio,
         "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav])
    out_json = os.path.join(workdir, "rhubarb.json")
    cmd = [rhubarb_bin, "-r", recognizer, "-f", "json", "-o", out_json]
    if dialog:
        cmd += ["-d", dialog]
    cmd.append(wav)
    run(cmd)
    return out_json


# ------------------------------------------------------------- cue ingestion

def load_rhubarb_json(path):
    with open(path) as fh:
        data = json.load(fh)
    cues = [(float(c["start"]), float(c["end"]), c["value"].strip().upper())
            for c in data.get("mouthCues", [])]
    duration = None
    meta = data.get("metadata") or {}
    if meta.get("duration") is not None:
        duration = float(meta["duration"])
    return cues, duration


def load_rhubarb_tsv(path, duration_override=None):
    """Load Rhubarb TSV.

    Rhubarb's own TSV export has TWO columns (start, shape): a shape
    holds until the next row starts, and Rhubarb appends a sentinel row
    at the audio duration. Three-column files (start, end, shape) are
    also accepted. --duration overrides the total length when given.
    """
    rows = []
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                parts = line.split()
            if len(parts) < 2:
                continue
            try:
                start = float(parts[0])
            except ValueError:
                continue  # header or comment line
            if len(parts) >= 3:
                try:
                    end = float(parts[1])
                except ValueError:
                    continue
                rows.append((start, end, parts[2].strip().upper(), True))
            else:
                rows.append((start, None, parts[1].strip().upper(), False))
    cues = []
    for i, (start, end, value, explicit_end) in enumerate(rows):
        if not explicit_end:
            if i + 1 < len(rows):
                end = rows[i + 1][0]
            else:
                end = duration_override if duration_override else start
        cues.append((start, end, value))
    if duration_override is not None:
        duration = duration_override
    else:
        duration = max((e for _, e, _ in cues), default=None)
    return cues, duration


def load_rhubarb(path, duration_override=None):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return load_rhubarb_json(path)
    if ext == ".tsv":
        return load_rhubarb_tsv(path, duration_override)
    die(f"unsupported Rhubarb output '{path}' (expected .json or .tsv)")


# ------------------------------------------------------------ plan building

def normalize_cues(cues, duration):
    """Sort, clip overlaps, drop empty cues, fill gaps with X (rest)."""
    cues = [(s, e, v) for (s, e, v) in cues if e > s and v]
    cues.sort(key=lambda c: c[0])
    clipped = []
    for i, (s, e, v) in enumerate(cues):
        if i + 1 < len(cues):
            e = min(e, cues[i + 1][0])
        if e > s:
            clipped.append((s, e, v))
    if duration is None:
        duration = max((e for _, e, _ in clipped), default=0.0)
    filled = []
    t = 0.0
    for s, e, v in clipped:
        if s > t + EPS:
            filled.append((t, s, "X"))
        filled.append((max(s, t), e, v))
        t = e
    if duration > t + EPS:
        filled.append((t, duration, "X"))
    # merge adjacent rows with the same shape
    merged = []
    for s, e, v in filled:
        if merged and merged[-1][2] == v and abs(merged[-1][1] - s) < 1e-4:
            merged[-1] = (merged[-1][0], e, v)
        else:
            merged.append((s, e, v))
    return merged, duration


def build_rows(cues, duration, fps):
    """Quantize the (contiguous, gap-filled) cue list to frames.

    Frame f exposes the shape active at its start instant (f-1)/fps.
    Consecutive frames with the same shape compress into one row whose
    start_s/end_s are the frame-quantized times.
    """
    total = int(math.ceil(duration * fps - EPS)) if duration > 0 else 0
    rows = []
    ci = 0
    for f in range(1, total + 1):
        t = (f - 1) / fps
        while ci < len(cues) - 1 and t >= cues[ci][1] - 1e-9:
            ci += 1
        code = cues[ci][2] if t >= cues[ci][0] - 1e-9 else "X"
        if rows and rows[-1]["phoneme"] == code:
            rows[-1]["frame_end"] = f
            rows[-1]["end_s"] = f / fps
        else:
            rows.append({"start_s": t, "end_s": f / fps, "phoneme": code,
                         "frame": f, "frame_end": f})
    return rows, total


# ----------------------------------------------------------- mouth library

def resolve_mouths(mouth_dir, needed_shapes):
    """Map each Rhubarb shape code to an image file in mouth_dir.

    A file matches code C when its stem == C, or its stem starts with
    C + '_' or C + '-'. Longest-stem (most specific) match wins is not
    needed: an exact stem match always beats a prefixed one.
    """
    if not os.path.isdir(mouth_dir):
        die(f"mouth dir not found: {mouth_dir}")
    files = [f for f in sorted(os.listdir(mouth_dir))
             if f.lower().endswith(IMAGE_EXTS)]
    resolved = {}
    for code in SHAPES:
        exact = [f for f in files
                 if os.path.splitext(f)[0].upper() == code]
        prefixed = [f for f in files
                    if os.path.splitext(f)[0].upper().startswith((code + "_", code + "-"))]
        pick = (exact or prefixed or [None])[0]
        if pick:
            resolved[code] = os.path.abspath(os.path.join(mouth_dir, pick))
    missing = [c for c in needed_shapes if c not in resolved]
    if missing:
        if "X" in resolved:
            for c in missing:
                print(f"mouthswap_bridge: warning: no image for shape {c}; "
                      f"falling back to X ({os.path.basename(resolved['X'])})",
                      file=sys.stderr)
                resolved[c] = resolved["X"]
        else:
            die(f"mouth dir {mouth_dir} has no image for shapes "
                f"{', '.join(missing)} and no X (rest) image to fall back to")
    unused = [c for c in resolved if c not in needed_shapes]
    if unused:
        print(f"mouthswap_bridge: note: shapes not used by this line: "
              f"{', '.join(unused)}", file=sys.stderr)
    return resolved


# ----------------------------------------------------------------- outputs

def write_csv(rows, resolved, out_path):
    with open(out_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["frame", "frame_end", "phoneme", "mouth_file",
                    "start_s", "end_s"])
        for r in rows:
            w.writerow([r["frame"], r["frame_end"], r["phoneme"],
                        resolved[r["phoneme"]],
                        f"{r['start_s']:.4f}", f"{r['end_s']:.4f}"])


def write_blender_script(plan, out_path):
    template_path = os.path.join(HERE, "blender_mouthswap.py")
    if not os.path.isfile(template_path):
        die(f"Blender template missing next to the bridge: {template_path}")
    with open(template_path) as fh:
        src = fh.read()
    marker = "EMBEDDED_PLAN = None"
    if marker not in src:
        die("blender_mouthswap.py is missing its EMBEDDED_PLAN marker line")
    embedded = "EMBEDDED_PLAN = " + json.dumps(plan, indent=1)
    with open(out_path, "w") as fh:
        fh.write(src.replace(marker, embedded, 1))


# --------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Rhubarb phoneme timings -> timed mouth-swap plan "
                    "(CSV timing sheet + Blender swap script).")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--audio", help="voice audio file; bridge runs Rhubarb")
    src.add_argument("--rhubarb", help="existing Rhubarb output (.json/.tsv)")
    ap.add_argument("--mouth-dir", required=True,
                    help="folder of mouth images named by shape code A-H, X")
    ap.add_argument("--fps", type=int, default=30,
                    help="scene frame rate to key at (default 30)")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--dialog", help="dialog text file (improves Rhubarb)")
    ap.add_argument("--duration", type=float,
                    help="total audio seconds; only needed to override the "
                         "length inferred from a TSV input")
    ap.add_argument("--recognizer", default="pocketSphinx",
                    choices=["pocketSphinx", "phonetic"])
    ap.add_argument("--rhubarb-bin", default=DEFAULT_RHUBARB,
                    help=f"Rhubarb binary (default {DEFAULT_RHUBARB})")
    args = ap.parse_args(argv)

    if args.fps <= 0:
        die("--fps must be a positive integer")

    if args.audio:
        if not os.path.isfile(args.rhubarb_bin):
            die(f"Rhubarb binary not found: {args.rhubarb_bin}")
        if not shutil.which("ffmpeg"):
            die("ffmpeg not on PATH (needed to convert audio for Rhubarb)")
        os.makedirs(args.out, exist_ok=True)
        # Temp workdir sits next to --out, not in the system temp dir:
        # on the studio VM /tmp is a small tmpfs that fills up.
        work_parent = os.path.dirname(os.path.abspath(args.out))
        with tempfile.TemporaryDirectory(prefix="mouthswap-",
                                         dir=work_parent) as td:
            rhubarb_out = run_rhubarb(args.rhubarb_bin, args.audio,
                                      args.dialog, args.recognizer, td)
            cues, duration = load_rhubarb(rhubarb_out)
            # keep a copy of the raw Rhubarb output next to the plan
            shutil.copyfile(rhubarb_out,
                            os.path.join(args.out, "rhubarb.json"))
    else:
        cues, duration = load_rhubarb(args.rhubarb, args.duration)

    if not cues:
        die("no mouth cues found in the Rhubarb output")

    cues, duration = normalize_cues(cues, duration)
    rows, total_frames = build_rows(cues, duration, args.fps)
    needed = {r["phoneme"] for r in rows}
    unknown = needed - set(SHAPES)
    if unknown:
        die(f"Rhubarb output contains shapes outside the basic A-H/X set: "
            f"{', '.join(sorted(unknown))} (extended shapes are not "
            f"supported by this bridge)")
    resolved = resolve_mouths(args.mouth_dir, needed)

    plan = {
        "tool": "mouthswap-bridge",
        "version": 1,
        "fps": args.fps,
        "frame_start": 1,
        "frame_end": total_frames,
        "duration_s": round(duration, 4),
        "mouth_files": {c: resolved[c] for c in sorted(resolved)
                        if c in needed},
        "cues": [
            {"frame": r["frame"], "frame_end": r["frame_end"],
             "phoneme": r["phoneme"], "mouth_file": resolved[r["phoneme"]],
             "start_s": round(r["start_s"], 4),
             "end_s": round(r["end_s"], 4)}
            for r in rows
        ],
    }

    os.makedirs(args.out, exist_ok=True)
    csv_path = os.path.join(args.out, "mouthswap_timing.csv")
    plan_path = os.path.join(args.out, "mouthswap_plan.json")
    blender_path = os.path.join(args.out, "mouthswap_blender.py")
    write_csv(rows, resolved, csv_path)
    with open(plan_path, "w") as fh:
        json.dump(plan, fh, indent=1)
    write_blender_script(plan, blender_path)

    print(f"mouthswap_bridge: {len(rows)} mouth exposures, "
          f"{total_frames} frames @ {args.fps}fps "
          f"({duration:.2f}s)")
    print(f"  timing sheet : {csv_path}")
    print(f"  plan         : {plan_path}")
    print(f"  blender script: {blender_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
