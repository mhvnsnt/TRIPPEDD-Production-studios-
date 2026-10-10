#!/usr/bin/env python3
"""LOTI v3 final assembly — per-part beat structure.
Run from v3/ dir after EbSynth segments (segA..segE styled.mp4) complete.

Beat map (t in seconds):
  0-22.9   v1 footage
  22.9-25.0 segA: clean -> S1 EYES ignite        HIT1 @25.0  white flash + starburst
  25.0-27.0 segB: S1 -> S2 ELF EARS pop          HIT2 @27.0  white flash + poof pop
  27.0-29.0 segC: S2 -> S3 GRIN widens           HIT3 @29.0  green flash + starburst
  29.0-31.5 segD: S3 -> S4 green TRACKSUIT       HIT4 @31.5  white flash + SPIN + starburst
  31.5-33.5 segE: S4 -> S5 80% at the JUMP       HIT5 @33.5  flash + speedlines + punch-in
  33.5-35.0 K3 hold (hero beat)
  35.0-35.3 freeze | 35.3-35.7 poof | 35.7-37.7 mascot reveal (100%)
  37.7+ iris -> swap card -> title -> slogan -> disclaimers -> end button
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
HITS = [25.0, 27.0, 29.0, 31.5, 33.5]
FLASH_D = 0.4   # 12 frames @30fps — the PR '93 twenty-frame flash grammar, tightened
POP_D = 0.5

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label}", flush=True); sys.exit(1)

def dur(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(o.stdout.strip())

# sanity: all 5 EbSynth outputs must exist
for s in ["segA", "segB", "segC", "segD", "segE"]:
    p = os.path.join(EBS, s, "styled.mp4")
    assert os.path.exists(p), f"MISSING {p} — EbSynth not done"

os.makedirs(COMP, exist_ok=True)

# 1. base 0->22.9 from v1
run(FF + ["-ss", "0", "-t", "22.9", "-i", V1, "-vf", "fps=30,format=yuv420p",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
          f"{COMP}/v3-p1-base.mp4"], "p1 base 0-22.9")

# 2. normalize each styled segment to 1080p30
seg_durs = []
for s in ["segA", "segB", "segC", "segD", "segE"]:
    out = f"{COMP}/v3-{s}.mp4"
    run(FF + ["-i", f"{EBS}/{s}/styled.mp4", "-vf",
              "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
              "-c:v", "libx264", "-crf", "18", "-preset", "fast", out], f"{s} normalize")
    seg_durs.append(dur(out))
print("seg durations:", seg_durs, flush=True)

# 3. starburst pop clip (0.5s, scales 0.3->1.25 with slight overshoot)
run(["python3", "-c", f"""
from PIL import Image
import subprocess, io, os
sb = Image.open('{FX}/starburst.png').convert('RGBA')
os.makedirs('{COMP}/sb_frames', exist_ok=True)
for i in range(15):
    t = i/14
    s = 0.3 + 0.95*t + 0.08*(t**2)
    w,h = int(900*s), int(900*s)
    p = sb.resize((w,h), Image.LANCZOS)
    c = Image.new('RGBA',(900,900),(0,0,0,0))
    c.alpha_composite(p, ((900-w)//2,(900-h)//2))
    c.save(f'{COMP}/sb_frames/sb-%02d.png' % i)
print('sb frames done')
"""], "starburst frames")
run(FF + ["-framerate", "30", "-i", f"{COMP}/sb_frames/sb-%02d.png",
          "-vf", "scale=900:900,format=yuva420p",
          "-c:v", "libx264", "-pix_fmt", "yuva420p", "-crf", "18",
          f"{COMP}/v3-starburst-pop.mp4"], "starburst pop clip")

# 4. poof pop clip (0.5s, scales up, for ears beat)
run(["python3", "-c", f"""
from PIL import Image
import os
poof = Image.open('{FX}/poof.png').convert('RGBA')
os.makedirs('{COMP}/pf_frames', exist_ok=True)
for i in range(15):
    t = i/14
    s = 0.25 + 1.1*t
    w,h = int(700*s), int(700*s)
    p = poof.resize((w,h), Image.LANCZOS)
    c = Image.new('RGBA',(700,700),(0,0,0,0))
    c.alpha_composite(p, ((700-w)//2,(700-h)//2))
    c.save(f'{COMP}/pf_frames/pf-%02d.png' % i)
print('poof frames done')
"""], "poof frames")
run(FF + ["-framerate", "30", "-i", f"{COMP}/pf_frames/pf-%02d.png",
          "-vf", "scale=700:700,format=yuva420p",
          "-c:v", "libx264", "-pix_fmt", "yuva420p", "-crf", "18",
          f"{COMP}/v3-poof-pop.mp4"], "poof pop clip")

# 5. K3 hold 1.5s: last segE frame, punch-in (hero beat before the freeze)
run(FF + ["-i", f"{COMP}/v3-segE.mp4", "-filter_complex",
          "[0:v]trim=start_frame=58:end_frame=59,setpts=PTS-STARTPTS,"
          "zoompan=z='1+0.08*on/45':d=45:s=1920x1080:fps=30,format=yuv420p[v]",
          "-map", "[v]", "-t", "1.5", "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", f"{COMP}/v3-k3hold.mp4"], "k3 hold 33.5-35")

# 6. freeze 0.3s (same frame, no zoom)
run(FF + ["-i", f"{COMP}/v3-segE.mp4", "-vf",
          "trim=start_frame=58:end_frame=59,setpts=PTS-STARTPTS,fps=30,format=yuv420p",
          "-t", "0.3", "-c:v", "libx264", "-crf", "18",
          f"{COMP}/v3-freeze.mp4"], "freeze 35-35.3")

# 7. poof 0.4s over freeze (mascot transition)
run(["python3", "-c", f"""
from PIL import Image
import subprocess, io, os
fr = subprocess.run(['ffmpeg','-v','error','-i','{COMP}/v3-freeze.mp4','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True)
base = Image.open(io.BytesIO(fr.stdout)).convert('RGBA').resize((1920,1080))
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
          f"{COMP}/v3-poof.mp4"], "poof 35.3-35.7")

# 8. iris: mascot reveal -> 2D swap card (reuse v2 card + circlecrop xfade)
run(FF + ["-i", f"{COMP}/mascot_reveal.mp4", "-i", f"{V2}/card-2d-swap.mp4", "-filter_complex",
          "[0:v]trim=0:1.0,setpts=PTS-STARTPTS[mh];"
          "[1:v]trim=0:1.0,setpts=PTS-STARTPTS,format=yuv420p[sw];"
          "[mh][sw]xfade=transition=circlecrop:duration=1.0:offset=0.5,fps=30,format=yuv420p[v]",
          "-map", "[v]", "-t", "2.0", "-c:v", "libx264", "-crf", "18",
          f"{COMP}/v3-iris.mp4"], "iris to swap card")
run(FF + ["-ss", "1.0", "-i", f"{V2}/card-2d-swap.mp4", "-c:v", "libx264", "-pix_fmt", "yuv420p",
          "-crf", "18", f"{COMP}/v3-swaprest.mp4"], "swap rest")

# 9. concat base (no hits yet)
parts = [f"{COMP}/v3-p1-base.mp4", f"{COMP}/v3-segA.mp4", f"{COMP}/v3-segB.mp4",
         f"{COMP}/v3-segC.mp4", f"{COMP}/v3-segD.mp4", f"{COMP}/v3-segE.mp4",
         f"{COMP}/v3-k3hold.mp4", f"{COMP}/v3-freeze.mp4", f"{COMP}/v3-poof.mp4",
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

# 10. hits pass: flashes + starburst/poof pops + speedlines + spin at HIT4
#    starburst placements: HIT1,HIT3,HIT4,HIT5 center; HIT2 ears -> poof pop
fc = "[0:v]format=yuv420p[base];"
inputs = ["-i", f"{COMP}/v3-base.mp4",
          "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_white.png",
          "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_green.png",
          "-i", f"{COMP}/v3-starburst-pop.mp4",
          "-i", f"{COMP}/v3-poof-pop.mp4",
          "-loop", "1", "-i", f"{FX}/speedlines.png"]
flash_w, flash_g, sb, pf, sl = 1, 2, 3, 4, 5
fc += (f"[{flash_w}:v]scale=1920:1080,format=yuva420p,fade=t=in:st=0:d=0.1:alpha=1,"
       f"fade=t=out:st={FLASH_D-0.15}:d=0.15:alpha=1[fw];"
       f"[{flash_g}:v]scale=1920:1080,format=yuva420p,fade=t=in:st=0:d=0.1:alpha=1,"
       f"fade=t=out:st={FLASH_D-0.15}:d=0.15:alpha=1[fg];"
       f"[{sb}:v]format=yuva420p[sb];[{pf}:v]format=yuva420p[pf];"
       f"[{sl}:v]scale=1920:1080,format=yuva420p[sl];")
cur = "base"
# HIT1 @25.0: white flash + starburst center
fc += (f"[{cur}][fw]overlay=0:0:enable='between(t,25.0,25.4)'[b1];"
       f"[b1][sb]overlay=(W-w)/2:(H-h)/2:enable='between(t,25.0,25.5)'[b2];")
cur = "b2"
# HIT2 @27.0: white flash + poof pop (ears, upper-center)
fc += (f"[{cur}][fw]overlay=0:0:enable='between(t,27.0,27.4)'[b3];"
       f"[b3][pf]overlay=(W-w)/2:(H-h)/2-260:enable='between(t,27.0,27.5)'[b4];")
cur = "b4"
# HIT3 @29.0: green flash + starburst center
fc += (f"[{cur}][fg]overlay=0:0:enable='between(t,29.0,29.4)'[b5];"
       f"[b5][sb]overlay=(W-w)/2:(H-h)/2:enable='between(t,29.0,29.5)'[b6];")
cur = "b6"
# HIT4 @31.5: white flash + starburst + SPIN (clothes spin-morph gag)
fc += (f"[{cur}]split=2[sp0][sp1];"
       f"[sp0]trim=start=31.5:end=32.1,setpts=PTS-STARTPTS,"
       f"rotate='2*PI*(t)/0.6':fillcolor=black,format=yuv420p[spun];"
       f"[sp1][spun]overlay=0:0:enable='between(t,31.5,32.1)'[b7];"
       f"[b7][fw]overlay=0:0:enable='between(t,31.5,31.9)'[b8];"
       f"[b8][sb]overlay=(W-w)/2:(H-h)/2:enable='between(t,31.5,32.0)'[b9];")
cur = "b9"
# HIT5 @33.5: white flash + speedlines during the hold
fc += (f"[{cur}][fw]overlay=0:0:enable='between(t,33.5,33.9)'[b10];"
       f"[b10][sl]overlay=0:0:format=auto:enable='between(t,33.5,35.0)'[vout];")
fc += "[vout]format=yuv420p[v]"
run(FF + inputs + ["-filter_complex", fc, "-map", "[v]",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
          f"{COMP}/v3-hits.mp4"], "HITS pass")

# 11. final: hits video + v3 audio
run(FF + ["-i", f"{COMP}/v3-hits.mp4", "-i", os.path.join(D, "v3-audio-38s.wav"),
          "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
          "-movflags", "+faststart",
          os.path.join(D, "luck-of-the-irish-commercial-v3.mp4")], "FINAL MUX")
print("V3 ASSEMBLY COMPLETE")
