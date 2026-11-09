#!/usr/bin/env python3
"""Proof for WG105 Kiko V004:
1) render the 8 master pose frames FROM the built .fla (fla_render),
2) check pose distinctness numerically on the figure region,
3) build a frame-strip sheet from those FLA renders,
4) interpolate the same pose specs in PIL -> motion MP4."""
import os, subprocess, sys
sys.path.insert(0, "/home/hatch/workspace/fla-build")
sys.path.insert(0, "/home/hatch/workspace/fla-build/kiko-rebuild-v4-20261107")
import numpy as np
from PIL import Image, ImageDraw
from fla_render import FLA, warp
from build_kiko_v4 import POSES, POSE_NAMES, part_matrices, STACK, CANVAS

RB = "/home/hatch/workspace/fla-build/kiko-rebuild-v4-20261107"
XFL = "/home/hatch/workspace/fla-build/out/WG105_ORIGINAL_PUPPET_KIKO_VERSION_004"
MASTER = "WG105_KIKO_PUPPET_V004/WG_KIKO_FRONT_PUPPET"
BG = (32, 32, 32)

# ---- 1) FLA pose renders ----
fla = FLA(XFL)
fla.canvas_for = lambda name: CANVAS
pose_imgs = []
for i, nm in enumerate(POSE_NAMES):
    img = fla.render_symbol(MASTER, i)
    bg = Image.new("RGBA", img.size, BG + (255,)); bg.alpha_composite(img)
    bg.convert("RGB").save(f"{RB}/proof/poses/pose_{i}_{nm}.png")
    pose_imgs.append(np.asarray(bg.convert("RGB")).astype(int))
    print("fla pose", i, nm)

# ---- 2) distinctness vs NEUTRAL on figure region ----
base = pose_imgs[0]
for i, nm in enumerate(POSE_NAMES):
    d = np.abs(pose_imgs[i] - base).sum(axis=2)
    print(f"pose {nm:14s} vs NEUTRAL: mean|diff|={d.mean():6.2f}  pixels changed={(d > 30).mean()*100:5.1f}%")

# ---- 3) frame strip from FLA renders ----
TW = 296
strip = Image.new("RGB", (TW * 4 + 50, (int(TW * CANVAS[1] / CANVAS[0]) + 26) * 2 + 30), (12, 12, 18))
d = ImageDraw.Draw(strip)
TH = int(TW * CANVAS[1] / CANVAS[0])
for i, nm in enumerate(POSE_NAMES):
    im = Image.open(f"{RB}/proof/poses/pose_{i}_{nm}.png").resize((TW, TH))
    x, y = 10 + (i % 4) * (TW + 10), 10 + (i // 4) * (TH + 26)
    strip.paste(im, (x, y)); d.text((x + 4, y + TH + 6), f"pose {i} - {nm}", fill=(255, 220, 120))
strip.save(f"{RB}/proof/kiko_frame_strip.png"); print("strip ok")

# ---- 4) MP4: PIL interpolation between the same pose specs ----
parts_img = {n: Image.open(f"{RB}/parts/{n}.png") for n in STACK}
def render_pose(spec, size):
    M = part_matrices(spec)
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for n in STACK:
        out.alpha_composite(warp(parts_img[n], M[n], CANVAS))
    bg = Image.new("RGBA", CANVAS, BG + (255,)); bg.alpha_composite(out)
    return bg.convert("RGB").resize(size, Image.LANCZOS)

KEYS = [(0, "NEUTRAL"), (20, "ARMS_RAISED"), (38, "NEUTRAL"), (56, "POINT_R"),
        (76, "STEP_FORWARD"), (94, "HOOD_TILT_BOW"), (112, "WAVE_L"), (132, "GUARD"),
        (152, "NEUTRAL")]
SPECS = dict(POSES)
ALLPARTS = sorted({k for s in SPECS.values() for k in s} |
                  {"head","torso","coat_L","coat_R","upper_arm_L","upper_arm_R","forearm_L","forearm_R",
                   "hand_L","hand_R","thigh_L","thigh_R","shin_L","shin_R","shoe_L","shoe_R"})
def interp(f):
    for (f0, n0), (f1, n1) in zip(KEYS, KEYS[1:]):
        if f0 <= f <= f1:
            t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
            t = t * t * (3 - 2 * t)
            s0, s1 = SPECS[n0], SPECS[n1]
            out = {}
            for p in ALLPARTS:
                a = s0.get(p, (0, 0, 0)); b = s1.get(p, (0, 0, 0))
                out[p] = tuple(a[j] + (b[j] - a[j]) * t for j in range(3))
            return out
    return dict(SPECS["NEUTRAL"])

SIZE = (444, 786)
import io
proc = subprocess.Popen(["ffmpeg", "-y", "-f", "image2pipe", "-framerate", "24",
                         "-vcodec", "png", "-i", "-", "-c:v", "libx264", "-crf", "17",
                         "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                         f"{RB}/proof/kiko_real-motion_proof.mp4"],
                        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for f in range(KEYS[-1][0] + 1):
    buf = io.BytesIO(); render_pose(interp(f), SIZE).save(buf, "PNG")
    proc.stdin.write(buf.getvalue())
proc.stdin.close(); proc.wait()
mp4 = f"{RB}/proof/kiko_real-motion_proof.mp4"
print("mp4:", os.path.getsize(mp4), "bytes,", KEYS[-1][0] + 1, "frames (streamed, no frame files)")
