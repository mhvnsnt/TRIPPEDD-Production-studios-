#!/usr/bin/env python3
"""EP02 segment renderer: approved stills -> 1920x1080/30fps segments via subtle zoompan.
Deterministic, likeness-safe (no AI morphing)."""
import subprocess, os, sys

BASE = os.path.expanduser("~/workspace/trippedd-studio/production/WIZARD_GANG_EP01")
STILLS = os.path.join(BASE, "ep02-stills")
SEG = os.path.join(BASE, "ep02-segments")
os.makedirs(SEG, exist_ok=True)

# (shot, seconds, motion)
SHOTS = [
    ("10-1", 6, "zin"), ("10-2", 6, "zin"),
    ("11-1", 6, "zin"), ("11-2", 5, "panR"), ("11-3", 5, "hold"),
    ("12-1", 10, "zin"), ("12-2", 5, "zin"), ("12-3", 5, "panL"),
    ("13-1", 8, "zin"), ("13-2", 8, "hold"), ("13-3", 8, "panR"), ("13-4", 8, "zin"),
    ("14-1", 10, "zin"), ("15-1", 10, "hold"), ("16-1", 9, "panL"),
    ("17-1", 9, "hold"), ("18-1", 10, "zin"), ("19-1", 9, "panR"),
    ("20-1", 8, "zin"), ("21-1", 8, "hold"), ("22-1", 9, "panR"),
    ("23-1", 9, "zin"), ("24-1", 10, "zin"), ("25-1", 6, "zin_fast"),
    ("26-1", 8, "zin"), ("27-1", 12, "zout"), ("27-2", 13, "hold"),
    ("28-1", 20, "zin_slow"), ("29-1", 5, "hold"),
]

def zp_expr(motion, frames):
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if motion == "zin":
        return f"z='min(1+0.00045*on,1.15)':x='{cx}':y='{cy}'"
    if motion == "zin_fast":
        return f"z='min(1+0.0009*on,1.20)':x='{cx}':y='{cy}'"
    if motion == "zin_slow":
        return f"z='min(1+0.00018*on,1.12)':x='{cx}':y='{cy}'"
    if motion == "zout":
        return f"z='max(1.12-0.00035*on,1.0)':x='{cx}':y='{cy}'"
    if motion == "panR":
        return f"z=1.10:x='(iw-iw/zoom)*on/{frames}':y='{cy}'"
    if motion == "panL":
        return f"z=1.10:x='(iw-iw/zoom)*(1-on/{frames})':y='{cy}'"
    if motion == "hold":
        return f"z=1.06:x='{cx}+12*on/{frames}':y='{cy}'"
    raise ValueError(motion)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd[:6]), r.stderr[-500:], file=sys.stderr)
        return False
    return True

ok, failed = 0, []
for shot, secs, motion in SHOTS:
    frames = secs * 30
    src = os.path.join(STILLS, f"ep02-shot-{shot}.png")
    dst = os.path.join(SEG, f"seg-{shot}.mp4")
    if os.path.exists(dst):
        # verify duration
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1", dst],
                           capture_output=True, text=True)
        try:
            if abs(float(r.stdout.strip().split("=")[1]) - secs) < 0.1:
                print(f"skip {shot} (exists, ok)")
                ok += 1
                continue
        except Exception:
            pass
    vf = f"scale=4096:-2,zoompan={zp_expr(motion, frames)}:d={frames}:s=1920x1080:fps=30"
    cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", src,
           "-vf", vf, "-frames:v", str(frames),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", dst]
    print(f"render {shot} ({secs}s, {motion})...", flush=True)
    if run(cmd):
        ok += 1
    else:
        failed.append(shot)

print(f"DONE: {ok} ok, {len(failed)} failed: {failed}")
sys.exit(1 if failed else 0)
