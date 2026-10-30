#!/usr/bin/env python3
"""Finish the Ashes FLA proof package: frames 53-71, MP4, frame strip,
pose sheet, Gumball-vs-Ashes structure sheet, motion verification numbers.
Safe to re-run; exits early if the sandbox write block is still active."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw

B = "/home/hatch/workspace/fla-build"
FR = f"{B}/proof/frames"

# 0) write-block probe
try:
    Image.new("RGB", (8, 8), (1, 2, 3)).save("/tmp/_probe.png")
    if os.path.getsize("/tmp/_probe.png") == 0: raise IOError("zero-byte")
except Exception as e:
    print("WRITE BLOCK STILL ACTIVE:", e); sys.exit(3)
print("writes OK")

# 1) remaining frames
from fla_render import FLA
fla = FLA(f"{B}/out/WG101ARRIVAL_Sc001_Clean_V001_ASH")
for f in range(72):
    p = f"{FR}/f{f:03d}.png"
    if os.path.exists(p) and os.path.getsize(p) > 10000: continue
    fla.render_scene(f).convert("RGB").save(p)
    print("rendered", f, flush=True)

# 2) MP4
mp4 = f"{B}/proof/WG101ARRIVAL_Sc001_V001.mp4"
subprocess.run(["ffmpeg", "-y", "-framerate", "24", "-i", f"{FR}/f%03d.png",
                "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", mp4], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("mp4:", os.path.getsize(mp4), "bytes")

# 3) frame strip [0,12,20,32,44,56,66,71]
beats = [(0, "NEUTRAL"), (12, "ANTICIPATION"), (20, "GESTURE+TALK"), (32, "GESTURE+TALK"),
         (44, "POINT"), (56, "TRANSITION"), (66, "SETTLE (blink)"), (71, "REST_X grin hold")]
TW, TH = 470, 264
strip = Image.new("RGB", (TW * 4 + 50, (TH + 26) * 2 + 30), (12, 12, 18))
d = ImageDraw.Draw(strip)
for i, (f, label) in enumerate(beats):
    im = Image.open(f"{FR}/f{f:03d}.png").resize((TW, TH))
    x, y = 10 + (i % 4) * (TW + 10), 10 + (i // 4) * (TH + 26)
    strip.paste(im, (x, y))
    d.text((x + 4, y + TH + 6), f"frame {f} - {label}", fill=(255, 220, 120))
strip.save(f"{B}/proof/frame_strip.png"); print("strip ok")

# 4) pose sheet
poses = [(0, "NEUTRAL"), (3, "GESTURE_WIDE"), (7, "POINT"), (9, "SETTLE")]
PW, PH = 300, 648
sheet = Image.new("RGB", (PW * 4 + 50, PH + 40), (16, 16, 24))
d = ImageDraw.Draw(sheet)
for i, (f, label) in enumerate(poses):
    im = Image.open(f"{B}/proof/pose_{f}.png").resize((PW, PH))
    x = 10 + i * (PW + 10)
    sheet.paste(im, (x, 10)); d.text((x + 4, PH + 18), label, fill=(255, 220, 120))
sheet.save(f"{B}/proof/poses_sheet.png"); print("poses sheet ok")

# 5) structure sheet — Gumball GB200 puppet 008 vs WG101 Ashes puppet V001
rows = [
    ("", "GUMBALL GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008", "WG101_ORIGINAL_PUPPET_ASHES_VERSION_001"),
    ("format", "CS5.5 XFL (zipped .fla), 25 fps", "XFL 2.1 (zipped .fla), 24 fps container"),
    ("stage", "2730x1625 asset-container sheet", "1920x1080 asset-container sheet"),
    ("view rigs", "4 (STD / back / side / TQ)", "1 (FRONT) — only view his art has"),
    ("master pose library", "95 frames, 13 labels (STAND_UP..WALK)", "13 frames, 13 labels (NEUTRAL..TRANSITION)"),
    ("HEADCOMP", "309 frames, per-view head variants", "8 face states (blink/talk/smile/look/angry)"),
    ("MOUTH", "280 frames, ~124 drawings, phoneme labels", "14 Mouth Set One shapes (labelled) + grill deform"),
    ("EYESCOMP", "445 frames, expression categories + pupils", "12 frames: colourway swaps + base-white set"),
    ("hands", "drawn hand sets per view", "hand_R segmented (wrist pivot) — no hand_L in art"),
    ("validation", "original production file", "unzip round-trip + FlashXFLParser full parse"),
]
W, H = 1560, 40 + len(rows) * 44
img = Image.new("RGB", (W, H), (14, 14, 20)); d = ImageDraw.Draw(img)
d.text((16, 12), "PUPPET STRUCTURE — GUMBALL PRODUCTION vs WIZARD GANG (same anatomy)", fill=(255, 220, 120))
cols = [16, 300, 830]
for r, row in enumerate(rows):
    y = 44 + r * 44
    if r == 0: d.rectangle([0, y - 4, W, y + 34], fill=(40, 40, 60))
    for c, txt in enumerate(row):
        d.text((cols[c], y), txt, fill=(230, 230, 240) if c else (160, 200, 255))
img.save(f"{B}/proof/structure_sheet.png"); print("structure sheet ok")

# 6) motion verification: pixel-diff between consecutive strip frames
import numpy as np
prev = None
for f, label in beats:
    a = np.array(Image.open(f"{FR}/f{f:03d}.png")).astype(int)
    if prev is not None:
        diff = np.abs(a - prev).mean()
        changed = (np.abs(a - prev).sum(axis=2) > 30).mean() * 100
        print(f"frame {f} ({label}): mean|diff| vs prev strip frame = {diff:.2f}, pixels changed = {changed:.1f}%")
    prev = a
print("PROOF PACKAGE COMPLETE")
