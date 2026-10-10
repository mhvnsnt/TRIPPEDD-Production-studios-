#!/usr/bin/env python3
"""WIZARD GANG EP02 — visual rebuild assembly (EP01 image-animation method).

Replaces the REJECTED zoompan slideshow. One real motion clip per approved
still (media.generate_video image-animation), assembled per EP02_SHOT_LIST.md.

Timeline: 0:00-0:50 pilot cold open (pilot-50s.mp4, UNCHANGED, keeps audio) +
0:50-5:00 new show (250s, silent — no voices: every line is DRAFT pending
owner script approval per VOICE_STATUS.md voice law).

REFUSES to build if any shot's clip is missing — no silent placeholders,
no slideshow substitution. Ever.
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ANIM = os.path.join(HERE, "ep02-animated")
PILOT = os.path.join(HERE, "pilot-50s.mp4")
TMP = os.path.join(HERE, "assemble_ep02_tmp")
OUT = os.path.join(HERE, "wizard-gang-ep02-16x9.mp4")

# shot -> duration seconds (EP02_SHOT_LIST.md). 26-1 -> 27-1 has a 5s fog wipe
# (2.5s fade-to-white tail on 26-1 + 2.5s fade-from-white head on 27-1).
SHOTS = [
    ("10-1", 6), ("10-2", 6),
    ("11-1", 6), ("11-2", 5), ("11-3", 5),
    ("12-1", 10), ("12-2", 5), ("12-3", 5),
    ("13-1", 8), ("13-2", 8), ("13-3", 8), ("13-4", 8),
    ("14-1", 10), ("15-1", 10), ("16-1", 9), ("17-1", 9), ("18-1", 10),
    ("19-1", 9), ("20-1", 8), ("21-1", 8), ("22-1", 9), ("23-1", 9),
    ("24-1", 10), ("25-1", 6), ("26-1", 8),
    # 5s fog wipe transition (26-1 -> 27-1) fills 4:05-4:10
    ("27-1", 12), ("27-2", 13), ("28-1", 20), ("29-1", 5),
]
# shots whose 10s clip must be time-stretched to hit duration (EP01 precedent)
STRETCH = {"27-2": 1.3, "28-1": 2.0}

FIT = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"
VENC = ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-r", "30", "-an"]


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], flush=True)
        sys.exit(1)


def clip_for(shot):
    pat = os.path.join(ANIM, f"media-generation-ep02-anim-{shot}-0-*.mp4")
    hits = sorted(glob.glob(pat))
    if not hits:
        print(f"FATAL: no animation clip for shot {shot} (pattern {pat})", flush=True)
        print("FATAL: refusing to build with missing shots — no placeholders.", flush=True)
        sys.exit(2)
    return hits[0]


def seg(shot, dur):
    """Build one normalized segment (skip if already built)."""
    path = os.path.join(TMP, f"seg-{shot}.mp4")
    if os.path.exists(path):
        print(f"skip {shot} (exists)", flush=True)
        return path
    src = clip_for(shot)
    vf = FIT
    extra_in = []
    if shot in STRETCH:
        f = STRETCH[shot]
        vf = f"setpts={f}*PTS," + vf
        # stretch first, then trim to exact duration
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", src,
           "-vf", vf, "-t", str(dur)] + VENC + [path]
    run(cmd)
    return path


def main():
    os.makedirs(TMP, exist_ok=True)
    if not os.path.exists(PILOT):
        print(f"FATAL: pilot not found: {PILOT}", flush=True)
        sys.exit(2)

    segfiles = []
    for i, (shot, dur) in enumerate(SHOTS):
        p = seg(shot, dur)
        # fog wipe: fade 26-1 tail to white / 27-1 head from white
        if shot == "26-1" or shot == "27-1":
            wp = os.path.join(TMP, f"seg-{shot}-wipe.mp4")
            if not os.path.exists(wp):
                if shot == "26-1":
                    vf = f"fade=t=out:st={dur-2.5}:d=2.5:color=white"
                else:
                    vf = "fade=t=in:st=0:d=2.5:color=white"
                run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", vf] + VENC + [wp])
            p = wp
        segfiles.append(p)

    # pilot: re-encode to match (video as-is, keep its audio)
    pilot_norm = os.path.join(TMP, "pilot-norm.mp4")
    if not os.path.exists(pilot_norm):
        run(["ffmpeg", "-v", "error", "-y", "-i", PILOT,
             "-vf", "scale=1920:1080,fps=30",
             "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-r", "30",
             "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000",
             pilot_norm])

    # show block: concat segments (video only)
    show_list = os.path.join(TMP, "show.txt")
    with open(show_list, "w") as f:
        for p in segfiles:
            f.write(f"file '{p}'\n")
    show_block = os.path.join(TMP, "show-block.mp4")
    if not os.path.exists(show_block):
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
             "-i", show_list, "-c", "copy", show_block])

    # silent stereo bed for the show portion
    silence = os.path.join(TMP, "silence-250.m4a")
    if not os.path.exists(silence):
        run(["ffmpeg", "-v", "error", "-y",
             "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
             "-t", "250", "-c:a", "aac", "-b:a", "128k", silence])

    # final: pilot (a/v) + show video + silence
    run(["ffmpeg", "-v", "error", "-y",
         "-i", pilot_norm, "-i", show_block, "-i", silence,
         "-filter_complex",
         "[0:v][1:v]concat=n=2:v=1:a=0[v];[0:a][2:a]concat=n=2:v=0:a=1[a]",
         "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000",
         "-movflags", "+faststart", OUT])
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
