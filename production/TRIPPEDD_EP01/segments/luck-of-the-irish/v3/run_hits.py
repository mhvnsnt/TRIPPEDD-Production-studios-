#!/usr/bin/env python3
"""LOTI v3 — HITS pass only (step 9 of assemble_v3.py), run in FOREGROUND.
Reads computed hit times from comp/v3-hittimes.txt. Replicates the exact
filter graph from assemble_v3.py so the result matches the planned assembly."""
import subprocess, os, sys

D = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(D, "comp")
FX = os.path.join(D, "fx")
FF = ["ffmpeg", "-y", "-v", "error"]
FLASH_D = 0.4
POP_D = 0.5

ht = {}
with open(os.path.join(COMP, "v3-hittimes.txt")) as f:
    for line in f:
        k, v = line.strip().split("=")
        ht[k] = float(v)
H1, H2, H3, H4, H5 = ht["H1"], ht["H2"], ht["H3"], ht["H4"], ht["H5"]
T_JUMP = ht["JUMP"]
print(f"HITS: H1={H1} H2={H2} H3={H3} H4={H4} H5={H5} JUMP={T_JUMP}", flush=True)

def win(t0, d=FLASH_D):
    return f"between(t,{t0:.3f},{t0+d:.3f})"

fc = "[0:v]format=yuv420p[base];"
inputs = ["-i", f"{COMP}/v3-base.mp4",
          "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_white.png",
          "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_green.png",
          "-i", f"{COMP}/v3-starburst-pop.mp4",
          "-i", f"{COMP}/v3-poof-pop.mp4",
          "-loop", "1", "-t", "2", "-i", f"{FX}/speedlines.png"]
fc += (f"[1:v]scale=1920:1080,format=yuva420p,"
       f"fade=t=in:st=0:d=0.08:alpha=1,fade=t=out:st={FLASH_D-0.12}:d=0.12:alpha=1[fw];"
       f"[2:v]scale=1920:1080,format=yuva420p,"
       f"fade=t=in:st=0:d=0.08:alpha=1,fade=t=out:st={FLASH_D-0.12}:d=0.12:alpha=1[fg];"
       f"[3:v]format=yuva420p[sb];[4:v]format=yuva420p[pf];"
       f"[5:v]scale=1920:1080,format=yuva420p[sl];")
cur = "base"
# HIT1 eyes: white flash + starburst
fc += (f"[{cur}][fw]overlay=0:0:enable='{win(H1)}'[b1];"
       f"[b1][sb]overlay=(W-w)/2:(H-h)/2:enable='{win(H1, POP_D)}'[b2];"); cur = "b2"
# HIT2 ears: white flash + poof pop (upper center)
fc += (f"[{cur}][fw]overlay=0:0:enable='{win(H2)}'[b3];"
       f"[b3][pf]overlay=(W-w)/2:(H-h)/2-260:enable='{win(H2, POP_D)}'[b4];"); cur = "b4"
# HIT3 grin: green flash + starburst
fc += (f"[{cur}][fg]overlay=0:0:enable='{win(H3)}'[b5];"
       f"[b5][sb]overlay=(W-w)/2:(H-h)/2:enable='{win(H3, POP_D)}'[b6];"); cur = "b6"
# HIT4 tracksuit: white flash + SPIN (clothes spin-morph gag) + starburst
fc += (f"[{cur}]split=2[sp0][sp1];"
       f"[sp0]trim=start={H4:.3f}:end={H4+0.6:.3f},setpts=PTS-STARTPTS,"
       f"rotate='2*PI*t/0.6':fillcolor=black,format=yuv420p[spun];"
       f"[sp1][spun]overlay=0:0:enable='{win(H4, 0.6)}'[b7];"
       f"[b7][fw]overlay=0:0:enable='{win(H4)}'[b8];"
       f"[b8][sb]overlay=(W-w)/2:(H-h)/2:enable='{win(H4, POP_D)}'[b9];"); cur = "b9"
# HIT5 jump: white flash + speedlines through the hold
fc += (f"[{cur}][fw]overlay=0:0:enable='{win(H5)}'[b10];"
       f"[b10][sl]overlay=0:0:format=auto:enable='{win(T_JUMP, 1.5)}'[vout];")
fc += "[vout]format=yuv420p[v]"

print("[HITS pass] starting ffmpeg...", flush=True)
r = subprocess.run(FF + inputs + ["-filter_complex", fc, "-map", "[v]",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
          f"{COMP}/v3-hits.mp4"])
if r.returncode != 0:
    print("FATAL: HITS pass failed", flush=True); sys.exit(1)
sz = os.path.getsize(f"{COMP}/v3-hits.mp4")
print(f"[HITS pass] done, {sz} bytes", flush=True)
assert sz > 1_000_000, "v3-hits.mp4 suspiciously small"
print("HITS OK")
