#!/usr/bin/env python3
"""LOTI commercial v2 — final assembly: concat video segments, mux with audio."""
import subprocess, os, sys, json

V2 = os.path.dirname(os.path.abspath(__file__))
FF = ["ffmpeg", "-y", "-v", "error"]

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label} failed", flush=True); sys.exit(1)

SEGS = ["seg01-live-a.mp4", "seg02-ignite.mp4", "seg03-morph1.mp4", "seg04-live-l1.mp4",
        "seg05-morph2.mp4", "seg06-live-l2.mp4", "seg07-freeze.mp4", "seg08-morph3.mp4",
        "seg09-iris.mp4", "seg10-mascot.mp4", "card-2d-swap.mp4", "../title-card.mp4",
        "card-slogan-1.mp4", "../disclaimers-card.mp4", "card-thats-the-irish-folks.mp4"]

# verify all inputs exist and log durations
durs = []
for s in SEGS:
    if not os.path.exists(s):
        print(f"FATAL: missing {s}", flush=True); sys.exit(1)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", s], capture_output=True, text=True)
    d = float(r.stdout.strip()); durs.append(d)
    print(f"  {s}: {d:.2f}s", flush=True)
total = sum(durs)
print(f"  TOTAL video: {total:.2f}s", flush=True)

# concat filter (single pass, uniform re-encode)
inputs, filt = [], ""
for i, s in enumerate(SEGS):
    inputs += ["-i", s]
    filt += f"[{i}:v]setpts=PTS-STARTPTS,scale=1920:1080,fps=30,format=yuv420p[v{i}];"
filt += "".join(f"[v{i}]" for i in range(len(SEGS)))
filt += f"concat=n={len(SEGS)}:v=1:a=0,format=yuv420p[vout]"
run(FF + inputs + ["-filter_complex", filt, "-map", "[vout]", "-r", "30",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-an", "v2-video-only.mp4"], "concat video")

# audio: rebuild to exactly match video duration
aud = "v2-audio-66s.wav"
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", aud], capture_output=True, text=True)
ad = float(r.stdout.strip())
print(f"  audio {aud}: {ad:.2f}s vs video {total:.2f}s", flush=True)
if abs(ad - total) > 0.05:
    if ad > total:
        af = f"atrim=duration={total}"
    else:
        af = f"apad=whole_dur={total}"
    run(FF + ["-i", aud, "-af", af, "-c:a", "pcm_s16le", "v2-audio-final.wav"],
        "audio length match")
    aud = "v2-audio-final.wav"

run(FF + ["-i", "v2-video-only.mp4", "-i", aud,
    "-map", "0:v", "-map", "1:a",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
    "-movflags", "+faststart", "-shortest",
    "luck-of-the-irish-commercial-v2.mp4"], "mux final")
print("FINAL ASSEMBLY DONE", flush=True)
