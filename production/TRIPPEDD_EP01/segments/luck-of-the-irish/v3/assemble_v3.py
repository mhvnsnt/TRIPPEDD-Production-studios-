#!/usr/bin/env python3
"""LOTI v3 final assembly. Run from v3/ dir after EbSynth segments complete."""
import subprocess, os, sys, glob

D = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(os.path.dirname(D), "luck-of-the-irish-commercial-final.mp4")
EBS = os.path.join(D, "ebs")
FX = os.path.join(D, "fx")
COMP = os.path.join(D, "comp")
V2 = os.path.join(os.path.dirname(D), "v2")
SEG = os.path.dirname(D)
FF = ["ffmpeg", "-y", "-v", "error"]

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label}", flush=True); sys.exit(1)

def dur(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(o.stdout.strip())

# sanity: EbSynth outputs must exist
for f in ["seg1_ebs.mp4", "seg2_ebs.mp4"]:
    assert os.path.exists(os.path.join(EBS, f)), f"MISSING {f} — EbSynth not done"

# 1. base 0->22.9 from v1
run(FF + ["-ss", "0", "-t", "22.9", "-i", V1, "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", "-preset", "fast", f"{COMP}/p1-base.mp4"], "p1 base 0-22.9")

# 2. ignition already built (2.6s) -> p2
# 3/5. flashes: 2-frame white flashes
run(FF + ["-loop", "1", "-framerate", "30", "-t", "0.0667", "-i", f"{FX}/flash_white.png",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", f"{COMP}/flash.mp4"], "flash 2f")

# 4. seg1 ebs -> 30fps 1080p
run(FF + ["-i", f"{EBS}/seg1_ebs.mp4", "-vf",
          "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
          "-c:v", "libx264", "-crf", "18", "-preset", "fast", f"{COMP}/p4-seg1.mp4"], "p4 seg1")

# 6. seg2 ebs -> 30fps 1080p
run(FF + ["-i", f"{EBS}/seg2_ebs.mp4", "-vf",
          "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
          "-c:v", "libx264", "-crf", "18", "-preset", "fast", f"{COMP}/p6-seg2.mp4"], "p6 seg2")

# 7. K3 hold 1.5s: last seg2 frame + speedlines + punch-in
run(FF + ["-i", f"{COMP}/p6-seg2.mp4", "-i", f"{FX}/speedlines.png", "-filter_complex",
          "[0:v]trim=start_frame=134:end_frame=135,setpts=PTS-STARTPTS,scale=1920:1080[k3];"
          "[k3]zoompan=z='1+0.06*on/45':d=45:s=1920x1080:fps=30[zoom];"
          "[zoom][1:v]overlay=0:0:format=auto:enable='gte(t,0.5)',format=yuv420p[v]",
          "-map", "[v]", "-t", "1.5", "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", f"{COMP}/p7-k3hold.mp4"], "p7 k3 hold+speedlines")

# 8. freeze 0.3s (same last frame, no zoom)
run(FF + ["-i", f"{COMP}/p6-seg2.mp4", "-vf",
          "trim=start_frame=134:end_frame=135,setpts=PTS-STARTPTS,scale=1920:1080,"
          "fps=30,format=yuv420p",
          "-t", "0.3", "-c:v", "libx264", "-crf", "18", f"{COMP}/p8-freeze.mp4"], "p8 freeze")

# 9. poof 0.4s over freeze (python-built frames for scaling poof)
run(["python3", "-c", f"""
from PIL import Image
import subprocess
fr = subprocess.run(['ffmpeg','-v','error','-i','{COMP}/p8-freeze.mp4','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True)
base = Image.open(__import__('io').BytesIO(fr.stdout)).convert('RGBA').resize((1920,1080))
poof = Image.open('{FX}/poof.png').convert('RGBA')
import os
os.makedirs('{COMP}/poof_frames', exist_ok=True)
for i in range(12):
    s = 0.3 + 1.4*(i/11)
    pw,ph = int(1920*s), int(1080*s)
    p = poof.resize((pw,ph), Image.LANCZOS)
    f = base.copy(); f.alpha_composite(p, ((1920-pw)//2,(1080-ph)//2))
    f.convert('RGB').save(f'{COMP}/poof_frames/p-%02d.png' % i)
print('poof frames done')
"""], "poof frames")
run(FF + ["-framerate", "30", "-i", f"{COMP}/poof_frames/p-%02d.png",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
          f"{COMP}/p9-poof.mp4"], "p9 poof")

# 10. mascot reveal already built (2.0s) -> p10 = comp/mascot_reveal.mp4
# 11. iris close/open on mascot -> into 2D swap card (reuse v1 mask technique, simplified: fade through green)
run(FF + ["-i", f"{COMP}/mascot_reveal.mp4", "-i", f"{V2}/card-2d-swap.mp4", "-filter_complex",
          "[0:v]trim=0:1.0,setpts=PTS-STARTPTS[mh];"
          "[1:v]trim=0:1.0,setpts=PTS-STARTPTS,format=yuv420p[sw];"
          "[mh][sw]xfade=transition=circlecrop:duration=1.0:offset=0.5,fps=30,format=yuv420p[v]",
          "-map", "[v]", "-t", "2.0", "-c:v", "libx264", "-crf", "18",
          f"{COMP}/p11-iris.mp4"], "p11 iris to swap card")

# 12. concat everything: p1, p2(ignition), flash, p4, flash, p6, p7, flash, p8, p9, p10, p11,
#     rest of swap card, title, slogan, disclaimers, end button
# swap card remainder (after the 1s used in iris)
sw_dur = dur(f"{V2}/card-2d-swap.mp4")
run(FF + ["-ss", "1.0", "-i", f"{V2}/card-2d-swap.mp4", "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", f"{COMP}/p12-swaprest.mp4"], "p12 swap rest")
parts = [f"{COMP}/p1-base.mp4", f"{COMP}/ignition_base.mp4", f"{COMP}/flash.mp4",
         f"{COMP}/p4-seg1.mp4", f"{COMP}/flash.mp4", f"{COMP}/p6-seg2.mp4",
         f"{COMP}/p7-k3hold.mp4", f"{COMP}/flash.mp4", f"{COMP}/p8-freeze.mp4",
         f"{COMP}/p9-poof.mp4", f"{COMP}/mascot_reveal.mp4", f"{COMP}/p11-iris.mp4",
         f"{COMP}/p12-swaprest.mp4",
         os.path.join(SEG, "title-card.mp4"), f"{V2}/card-slogan-1.mp4",
         os.path.join(SEG, "disclaimers-card.mp4"), f"{V2}/card-thats-the-irish-folks.mp4"]
for p in parts:
    assert os.path.exists(p), f"MISSING part {p}"
with open(f"{COMP}/concat.txt", "w") as f:
    for p in parts:
        f.write(f"file '{p}'\n")
run(FF + ["-f", "concat", "-safe", "0", "-i", f"{COMP}/concat.txt",
          "-i", os.path.join(D, "v3-audio-38s.wav"),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
          "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
          os.path.join(D, "luck-of-the-irish-commercial-v3.mp4")], "FINAL ASSEMBLY")
print("V3 ASSEMBLY COMPLETE")
