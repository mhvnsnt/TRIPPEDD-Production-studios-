#!/usr/bin/env python3
"""LOTI v3 final assembly — per-part beat structure, smear-free edit.
EbSynth mid-segment interpolation frames were muddy (QC'd by eye); the edit
keeps only clean keyframe-anchored ranges and lands each part-change under a
campy HIT (flash + starburst/poof/spin). Timing is computed, not hardcoded.

Beat map (computed below):
  0-22.9   v1 footage
  beatA: clean -> EYES ignite (gradual)            HIT1 @endA
  beatB: eyes -> | EARS pop                        HIT2 @cutB
  beatC: ears -> | GRIN widens                      HIT3 @cutC
  beatD: grin -> | green TRACKSUIT (+spin gag)      HIT4 @cutD
  beatE: tracksuit -> | 80% at the JUMP             HIT5 @cutE
  K3 hero hold 1.5s -> freeze 0.3s -> poof 0.4s -> mascot reveal 2.0s (100%)
  iris -> swap card -> title -> slogan -> disclaimers -> end button
"""
import subprocess, os, sys

D = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(os.path.dirname(D), "luck-of-the-irish-commercial-final.mp4")
EBS = os.path.join(D, "ebs")
FX = os.path.join(D, "fx")
COMP = os.path.join(D, "comp")
V2 = os.path.join(os.path.dirname(D), "v2")
SEG = os.path.dirname(D)
FF = ["ffmpeg", "-y", "-v", "error"]
FPS_WORK = 8
FLASH_D = 0.4
POP_D = 0.5

# (segment, [clean ranges as (start,end) inclusive, 0-based]) — from eye QC
BEATS = [
    ("beatA", "segA", [(0, 16)],  "eyes"),
    ("beatB", "segB", [(0, 5), (12, 15)], "ears"),
    ("beatC", "segC", [(0, 4), (12, 15)], "grin"),
    ("beatD", "segD", [(0, 3), (14, 19)], "tracksuit"),
    ("beatE", "segE", [(0, 4), (13, 15)], "jump80"),
]

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label}", flush=True); sys.exit(1)

def dur(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(o.stdout.strip())

os.makedirs(COMP, exist_ok=True)

# 1. base 0->22.9 from v1
run(FF + ["-ss", "0", "-t", "22.9", "-i", V1, "-vf", "fps=30,format=yuv420p",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
          f"{COMP}/v3-p1-base.mp4"], "p1 base 0-22.9")

# 2. build beat clips from clean frame ranges; compute timeline
#    (symlink selected frames -> image2 with explicit framerate; concat demuxer
#    miscounts still-image segments)
t = 22.9
beat_info = {}
for name, seg, ranges, label in BEATS:
    seldir = f"{COMP}/{name}-sel"
    run(["rm", "-rf", seldir], f"clean {name}-sel")
    os.makedirs(seldir, exist_ok=True)
    idx = 0
    for a, b in ranges:
        for n in range(a, b + 1):
            os.symlink(os.path.abspath(f"{EBS}/{seg}/styled-frames/styled-{n:04d}.png"),
                       f"{seldir}/sel-{idx:04d}.png")
            idx += 1
    nframes = idx
    cut_t = (ranges[0][1] - ranges[0][0] + 1) / FPS_WORK if len(ranges) > 1 else None
    bd = nframes / FPS_WORK
    out = f"{COMP}/v3-{name}.mp4"
    run(FF + ["-framerate", str(FPS_WORK), "-i", f"{seldir}/sel-%04d.png",
              "-vf", "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
              "-c:v", "libx264", "-crf", "18", "-preset", "fast", out],
        f"{name} ({label}) {nframes}f")
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames",
              "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
              "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
    assert got == round(bd * 30), f"{name}: expected {round(bd*30)}f got {got}f"
    beat_info[name] = {"start": t, "dur": bd,
                       "cut": (t + cut_t) if cut_t else None,
                       "end": t + bd}
    t += bd

H1 = beat_info["beatA"]["end"]          # eyes done
H2 = beat_info["beatB"]["cut"]          # ears pop
H3 = beat_info["beatC"]["cut"]          # grin
H4 = beat_info["beatD"]["cut"]          # tracksuit + spin
H5 = beat_info["beatE"]["cut"]          # jump 80%
T_JUMP = beat_info["beatE"]["end"]
print(f"HITS: {H1:.3f} {H2:.3f} {H3:.3f} {H4:.3f} {H5:.3f} JUMP={T_JUMP:.3f}", flush=True)
with open(f"{COMP}/v3-hittimes.txt", "w") as f:
    f.write(f"H1={H1}\nH2={H2}\nH3={H3}\nH4={H4}\nH5={H5}\nJUMP={T_JUMP}\n")

# 3. starburst pop clip + poof pop clip (authored)
run(["python3", "-c", f"""
from PIL import Image
import os
sb = Image.open('{FX}/starburst.png').convert('RGBA')
os.makedirs('{COMP}/sb_frames', exist_ok=True)
for i in range(15):
    tt = i/14
    s = 0.3 + 0.95*tt + 0.08*(tt**2)
    w,h = int(900*s), int(900*s)
    p = sb.resize((w,h), Image.LANCZOS)
    c = Image.new('RGBA',(900,900),(0,0,0,0))
    c.alpha_composite(p, ((900-w)//2,(900-h)//2))
    c.save(f'{COMP}/sb_frames/sb-%02d.png' % i)
poof = Image.open('{FX}/poof.png').convert('RGBA')
os.makedirs('{COMP}/pf_frames', exist_ok=True)
for i in range(15):
    tt = i/14
    s = 0.25 + 1.1*tt
    w,h = int(700*s), int(700*s)
    p = poof.resize((w,h), Image.LANCZOS)
    c = Image.new('RGBA',(700,700),(0,0,0,0))
    c.alpha_composite(p, ((700-w)//2,(700-h)//2))
    c.save(f'{COMP}/pf_frames/pf-%02d.png' % i)
print('pop frames done')
"""], "pop frames")
run(FF + ["-framerate", "30", "-i", f"{COMP}/sb_frames/sb-%02d.png",
          "-vf", "scale=900:900,format=yuva420p",
          "-c:v", "libx264", "-pix_fmt", "yuva420p", "-crf", "18",
          f"{COMP}/v3-starburst-pop.mp4"], "starburst pop clip")
run(FF + ["-framerate", "30", "-i", f"{COMP}/pf_frames/pf-%02d.png",
          "-vf", "scale=700:700,format=yuva420p",
          "-c:v", "libx264", "-pix_fmt", "yuva420p", "-crf", "18",
          f"{COMP}/v3-poof-pop.mp4"], "poof pop clip")

# 4. K3 hero hold 1.5s from beatE's last styled frame (punch-in)
K3PNG = os.path.abspath(f"{EBS}/segE/styled-frames/styled-0015.png")
run(FF + ["-loop", "1", "-framerate", "30", "-i", K3PNG,
          "-vf", "scale=1920:1080,"
          "zoompan=z='1+0.08*on/45':d=45:s=1920x1080:fps=30,format=yuv420p",
          "-t", "1.5", "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", f"{COMP}/v3-k3hold.mp4"], "k3 hold")
T_HOLD_END = T_JUMP + 1.5

# 5. freeze 0.3s (same frame, no zoom)
run(FF + ["-loop", "1", "-framerate", "30", "-t", "0.3", "-i", K3PNG,
          "-vf", "scale=1920:1080,format=yuv420p",
          "-c:v", "libx264", "-crf", "18",
          f"{COMP}/v3-freeze.mp4"], "freeze")
T_FREEZE_END = T_HOLD_END + 0.3

# 6. poof 0.4s over freeze
run(["python3", "-c", f"""
from PIL import Image
import os
base = Image.open('{K3PNG}').convert('RGBA').resize((1920,1080))
poof = Image.open('{FX}/poof.png').convert('RGBA')
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
          f"{COMP}/v3-poof.mp4"], "poof")
T_POOF_END = T_FREEZE_END + 0.4
T_MASCOT_END = T_POOF_END + 2.0

# 7. iris: mascot reveal -> 2D swap card
run(FF + ["-i", f"{COMP}/mascot_reveal.mp4", "-i", f"{V2}/card-2d-swap.mp4", "-filter_complex",
          "[0:v]trim=0:1.0,setpts=PTS-STARTPTS[mh];"
          "[1:v]trim=0:1.0,setpts=PTS-STARTPTS,format=yuv420p[sw];"
          "[mh][sw]xfade=transition=circlecrop:duration=1.0:offset=0.5,fps=30,format=yuv420p[v]",
          "-map", "[v]", "-t", "2.0", "-c:v", "libx264", "-crf", "18",
          f"{COMP}/v3-iris.mp4"], "iris to swap card")
run(FF + ["-ss", "1.0", "-i", f"{V2}/card-2d-swap.mp4", "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", f"{COMP}/v3-swaprest.mp4"], "swap rest")

# 8. concat base
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
run(FF + ["-f", "concat", "-safe", "0", "-i", f"{COMP}/v3-concat.txt",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
          f"{COMP}/v3-base.mp4"], "base concat")

# 9. hits pass — sequential (one hit per ffmpeg invocation).
# The monolithic 11-overlay filter graph gets SIGKILLed on this box (~10s,
# no OOM log); v3/run_hits_seq.py is the proven replacement (5 sequential
# passes, ~2.5 min each). Old monolithic code preserved in git history.
run(["python3", os.path.join(D, "run_hits_seq.py")], "HITS pass (sequential)")

# 10. audio with impacts at computed hit times (built by build_audio_v3.py reading hittimes)
run(["python3", os.path.join(D, "build_audio_v3.py")], "v3 audio")

# 11. final mux
run(FF + ["-i", f"{COMP}/v3-hits.mp4", "-i", os.path.join(D, "v3-audio-beats.wav"),
          "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
          "-movflags", "+faststart",
          os.path.join(D, "luck-of-the-irish-commercial-v3.mp4")], "FINAL MUX")
print("V3 ASSEMBLY COMPLETE")
