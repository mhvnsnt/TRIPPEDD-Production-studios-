#!/usr/bin/env python3
"""
animatic_builder_wg.py -- Storyboard images + timing + temp audio -> timed animatic.

Wizard Gang adaptation of Cape Jones `production/pipeline/animatic_builder.py`
(CJ main @ 2026-11-13, 3,775 B, read in full). The CJ render path (per-panel
ffmpeg holds -> concat, optional audio) is unchanged; the WG deltas are marked
WG-ADAPT below.

WG-ADAPT 1 -- CHECK FIRST. `--check` loads the timing file, verifies every
panel file exists, prints the panel count + total duration, and exits 0/1
without rendering. EP02 has NO storyboard panels yet (outline §7: boards
MISSING for all 21 segments) -- `--check` is how a lane proves the gap instead
of faking panels, and how a real board drop gets validated before a render.

WG-ADAPT 2 -- EP02 SCENE TIMING. `--from-ep02-scenes` reads
`wg_ep02_scenes_timing.csv` (20 scenes, real durations from EP02-OUTLINE.md
§2) and expects one panel per scene (`s10.png` ... `s29.png` in the boards
dir). Until boards exist, `--check` on that file correctly reports 20 missing
panels -- that IS the expected result today.

WG-ADAPT 3 -- WG TIMING STANDARD (PR #306). Default 24 fps on twos; the 12
drawings-per-second floor applies to the finished clip, and the exposure sheet
is the shot's companion doc. Output stays a 1920x1080 master; a 30 fps delivery
(EP02 v8b's render rate) is a conversion of the 24 fps master, not a
re-animation. Hard cuts are the default transition (timing standard §3).

Input: a directory of storyboard panels (PNG/JPG) + a timing file.
  Timing file (CSV or simple text):
    panel001.png,3.0        # 3 seconds
    panel002.png,1.5
    panel003.png,4.0

  Or --beat-file with JSON: {"panels": [{"file": "...", "duration": 3.0}, ...]}

Optional: --audio track.mp3 (temp music/dialogue laid under the animatic)
Optional: --transition 0.3 (crossfade seconds between panels)

Output: MP4 animatic at 24fps, 1920x1080 (panels letterboxed).

Example:
  python3 animatic_builder_wg.py boards/ timing.csv --audio temp_music.mp3 -o animatic.mp4
  python3 animatic_builder_wg.py boards/ wg_ep02_scenes_timing.csv --check
  python3 animatic_builder_wg.py boards/ wg_ep02_scenes_timing.csv -o ep02_animatic.mp4
"""
import argparse, csv, json, os, subprocess, sys

FPS = 24
W, H = 1920, 1080

# WG-ADAPT 2: EP02 scene timing file shipped beside this script.
EP02_SCENES_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "wg_ep02_scenes_timing.csv")


def load_timing(path):
    panels = []
    if path.endswith(".json"):
        data = json.load(open(path))
        items = data.get("panels", data)
        for it in items:
            panels.append((it["file"], float(it.get("duration", 2.0))))
    else:
        with open(path) as f:
            for row in csv.reader(f):
                if not row or row[0].strip().startswith("#"):
                    continue
                panels.append((row[0].strip(), float(row[1].strip())))
    return panels


def check_panels(boards_dir, panels):
    """WG-ADAPT 1: verify panels exist; report, do not render."""
    missing = []
    for fname, dur in panels:
        src = os.path.join(boards_dir, fname)
        if not os.path.exists(src):
            missing.append(src)
    total = sum(d for _, d in panels)
    print(f"check: {len(panels)} panels, {total:.1f}s total")
    if missing:
        print(f"check: MISSING {len(missing)} panel(s):")
        for m in missing:
            print(f"  MISSING {m}")
        print("check: FAIL -- boards for these panels do not exist yet "
              "(EP02 outline §7: storyboards MISSING for all 21 segments).")
        return 1
    print("check: all panels present -- OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Storyboard -> timed animatic (WG)")
    ap.add_argument("boards_dir", nargs="?")
    ap.add_argument("timing", nargs="?", help="CSV or JSON timing file")
    ap.add_argument("-o", "--output", help="output mp4 (required unless --check)")
    ap.add_argument("--audio", help="Temp audio track (mp3/wav)")
    ap.add_argument("--transition", type=float, default=0.0,
                    help="Crossfade seconds between panels")
    ap.add_argument("--fps", type=int, default=24, help="WG timing standard: 24 fps")
    ap.add_argument("--check", action="store_true",
                    help="WG: verify panels exist + total duration, do not render")
    ap.add_argument("--from-ep02-scenes", action="store_true",
                    help="WG: use wg_ep02_scenes_timing.csv (20 EP02 scenes, real durations)")
    args = ap.parse_args()

    if args.from_ep02_scenes:
        args.timing = EP02_SCENES_CSV
    if not args.boards_dir or not args.timing:
        ap.error("boards_dir and timing required (or --from-ep02-scenes with a boards dir)")
    if not args.check and not args.output:
        ap.error("-o/--output is required unless --check")

    panels = load_timing(args.timing)
    if not panels:
        sys.exit("No panels in timing file.")

    if args.check:
        sys.exit(check_panels(args.boards_dir, panels))

    # Build per-panel clips, then concat
    segs = []
    tmpdir = "/tmp/animatic_build_wg"
    os.makedirs(tmpdir, exist_ok=True)
    for i, (fname, dur) in enumerate(panels):
        src = os.path.join(args.boards_dir, fname)
        if not os.path.exists(src):
            sys.exit(f"Missing panel: {src}")
        seg = os.path.join(tmpdir, f"seg_{i:03d}.mp4")
        # pad to 1080p, hold for duration
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
              f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,"
              f"format=yuv420p")
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", src,
                        "-t", str(dur), "-vf", vf,
                        "-r", str(args.fps), "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "20", seg],
                       check=True, capture_output=True)
        segs.append(seg)

    # Concat (with optional xfade — simple concat if transition=0)
    if args.transition > 0 and len(segs) > 1:
        # full xfade chain is verbose; do pairwise for now
        print("NOTE: --transition uses simple concat for >2 panels in v1; "
              "xfade chain coming. Using hard cuts.", file=sys.stderr)

    lst = os.path.join(tmpdir, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p"]
    if args.audio:
        cmd += ["-i", args.audio, "-c:a", "aac", "-b:a", "160k", "-shortest"]
    cmd += [args.output]
    subprocess.run(cmd, check=True)
    total = sum(d for _, d in panels)
    print(f"animatic -> {args.output} ({len(panels)} panels, {total:.1f}s)")


if __name__ == "__main__":
    main()
