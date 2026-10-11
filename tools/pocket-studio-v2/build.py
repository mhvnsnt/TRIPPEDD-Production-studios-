#!/usr/bin/env python3
"""
Pocket Studio v2 — Project Builder
Takes a project JSON (from the Pocket Studio app) and renders the final MP4 with ffmpeg.

Usage:
    python3 build.py project.json -o output.mp4

Project format:
{
    "base_video": "path/to/base.mp4",   # workspace-relative
    "duration": 344.81,
    "clips": [
        {"id": "n1", "track": "dialogue", "file": "voice-delivery/x.mp3",
         "original_at": 52.0, "at": 52.0, "duration": 1.76, "volume": 1.0,
         "label": "...", ...}
    ],
    "ducks": [
        {"at": 84.0, "duration": 3.0, "to": 0.5, "label": "..."}
    ],
    "notes": [...]
}

How it works:
- For every clip, the base audio is muted at original_at (so dragging = clean move).
- Every clip is placed at its `at` position with its `volume`.
- Ducks reduce base volume in a range (e.g. duck Static under Onyx).
- Video is passed through untouched; only audio is rebuilt.
"""
import argparse
import json
import os
import subprocess
import sys

WORKSPACE = os.path.expanduser("~/workspace")


def build_filter(project):
    """Build the ffmpeg filter_complex string."""
    clips = project.get("clips", [])
    ducks = project.get("ducks", [])

    # Step 1: mute base audio at every clip's original position
    # (so a dragged clip doesn't double-play at its old spot)
    mute_exprs = []
    for c in clips:
        oa = c["original_at"]
        d = c["duration"]
        if oa is not None and d:
            mute_exprs.append(
                f"if(between(t,{oa},{oa + d + 0.3}),0,1)"
            )
    if mute_exprs:
        mute_chain = ",".join(
            f"volume='{e}':eval=frame" for e in mute_exprs
        )
        base_audio = f"[0:a]{mute_chain}[muted]"
    else:
        base_audio = "[0:a]acopy[muted]"

    # Step 2: apply ducks to the muted base
    ducked = "[muted]"
    if ducks:
        duck_exprs = []
        for dk in ducks:
            duck_exprs.append(
                f"if(between(t,{dk['at']},{dk['at'] + dk['duration']}),{dk['to']},1)"
            )
        # combine: multiply all duck factors
        combined = "*".join(f"({e})" for e in duck_exprs)
        ducked_out = "[ducked]"
        base_audio = base_audio + f";[muted]volume='{combined}':eval=frame{ducked_out}"
        ducked = ducked_out

    # Step 3: delay + volume each clip, then mix everything
    parts = [base_audio]
    mix_inputs = [ducked]
    for i, c in enumerate(clips):
        at_ms = int(c["at"] * 1000)
        vol = c.get("volume", 1.0)
        fpath = os.path.join(WORKSPACE, c["file"])
        if not os.path.exists(fpath):
            print(f"WARNING: missing {fpath} — skipping clip {c['id']}", file=sys.stderr)
            continue
        tag = f"c{i}"
        parts.append(
            f"[{i + 1}:a]adelay={at_ms}|{at_ms},volume={vol},apad[{tag}]"
        )
        mix_inputs.append(f"[{tag}]")

    n = len(mix_inputs)
    parts.append(
        f"{''.join(mix_inputs)}amix=inputs={n}:duration=first:normalize=0[aout]"
    )
    return ";".join(parts), len([c for c in clips
                                 if os.path.exists(os.path.join(WORKSPACE, c["file"]))])


def main():
    ap = argparse.ArgumentParser(description="Pocket Studio v2 project builder")
    ap.add_argument("project", help="Project JSON file")
    ap.add_argument("-o", "--output", required=True, help="Output MP4 path")
    ap.add_argument("--dry", action="store_true", help="Print ffmpeg command, don't run")
    args = ap.parse_args()

    with open(args.project) as f:
        project = json.load(f)

    base = os.path.join(WORKSPACE, project["base_video"])
    if not os.path.exists(base):
        print(f"ERROR: base video not found: {base}", file=sys.stderr)
        sys.exit(1)

    filt, n_clips = build_filter(project)

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", base]
    for c in project.get("clips", []):
        fpath = os.path.join(WORKSPACE, c["file"])
        if os.path.exists(fpath):
            cmd += ["-i", fpath]
    cmd += [
        "-filter_complex", filt,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        args.output,
    ]

    if args.dry:
        print(" ".join(cmd))
        return

    print(f"Building {args.output} from {n_clips} clips...", flush=True)
    subprocess.run(cmd, check=True)
    size = os.path.getsize(args.output) // 1024 // 1024
    print(f"Done: {args.output} ({size}MB)")


if __name__ == "__main__":
    main()
