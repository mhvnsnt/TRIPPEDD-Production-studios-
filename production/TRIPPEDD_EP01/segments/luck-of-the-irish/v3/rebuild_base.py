#!/usr/bin/env python3
"""Rebuild v3-poof.mp4 with the CLEAN hand-drawn poof, then re-concat v3-base.mp4.
(Steps 6 + 8 of assemble_v3.py.)"""
import subprocess, os, sys

D = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(D, "comp")
FX = os.path.join(D, "fx")
EBS = os.path.join(D, "ebs")
V2 = os.path.join(os.path.dirname(D), "v2")
SEG = os.path.dirname(D)
E = ["ffmpeg", "-y", "-v", "error"]

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label}", flush=True); sys.exit(1)

K3PNG = os.path.abspath(f"{EBS}/segE/styled-frames/styled-0015.png")

# step 6: poof 0.4s over freeze — CLEAN hand-drawn poof, capped scale + fade-out
# (v2: the old 1.7x scale whited out the frame; this erupts and dissipates)
run(["python3", "-c", f"""
from PIL import Image
import os
base = Image.open('{K3PNG}').convert('RGBA').resize((1920,1080))
poof = Image.open('{FX}/poof.png').convert('RGBA')
os.makedirs('{COMP}/poof_frames', exist_ok=True)
for i in range(12):
    s = 0.3 + 0.8*(i/11)
    pw,ph = int(1920*s), int(1080*s)
    p = poof.resize((pw,ph), Image.LANCZOS)
    if i >= 8:
        a = int(255 * (1 - (i-7)/4))
        p.putalpha(p.split()[3].point(lambda v: v*a//255))
    f = base.copy(); f.alpha_composite(p, ((1920-pw)//2,(1080-ph)//2))
    f.convert('RGB').save(f'{COMP}/poof_frames/p-%02d.png' % i)
print('poof frames done')
"""], "poof frames (clean v2)")
run(E + ["-framerate", "30", "-i", f"{COMP}/poof_frames/p-%02d.png",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
         f"{COMP}/v3-poof.mp4"], "v3-poof.mp4")

# step 8: concat base
parts = [f"{COMP}/v3-p1-base.mp4"] + [f"{COMP}/v3-{b}.mp4" for b in
         ["beatA", "beatB", "beatC", "beatD", "beatE"]] + \
        [f"{COMP}/v3-k3hold.mp4", f"{COMP}/v3-freeze.mp4", f"{COMP}/v3-poof.mp4",
         f"{COMP}/mascot_reveal.mp4", f"{COMP}/v3-iris.mp4", f"{COMP}/v3-swaprest.mp4",
         os.path.join(SEG, "title-card.mp4"), f"{V2}/card-slogan-1.mp4",
         os.path.join(SEG, "disclaimers-card.mp4"), f"{V2}/card-thats-the-irish-folks.mp4"]
for p in parts:
    assert os.path.exists(p), f"MISSING part {p}"
with open(f"{COMP}/v3-concat.txt", "w") as f:
    for p in parts:
        f.write(f"file '{p}'\n")
run(E + ["-f", "concat", "-safe", "0", "-i", f"{COMP}/v3-concat.txt",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
         f"{COMP}/v3-base.mp4"], "base concat")
print("BASE REBUILD OK")
