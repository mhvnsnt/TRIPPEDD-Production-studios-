#!/usr/bin/env python3
"""LOTI v3 pass 4 (spin) split in two to dodge the memory spike:
4a renders just the 0.6s rotated segment; 4b overlays it + flash + starburst."""
import subprocess, os, sys

D = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(D, "comp")
FX = os.path.join(D, "fx")
FLASH_D, POP_D = 0.4, 0.5
H4 = 27.9
E = ["ffmpeg", "-y", "-v", "error"]
FW = (f"scale=1920:1080,format=yuva420p,fade=t=in:st=0:d=0.08:alpha=1,"
      f"fade=t=out:st={FLASH_D-0.12}:d=0.12:alpha=1")

def win(t0, d=FLASH_D):
    return f"between(t,{t0:.3f},{t0+d:.3f})"

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label} rc={r.returncode}", flush=True); sys.exit(1)

# 4a: rotated 0.6s segment only (tiny job)
run(E + ["-ss", f"{H4:.3f}", "-t", "0.6", "-i", f"{COMP}/hits3.mp4",
         "-vf", "rotate='2*PI*t/0.6':fillcolor=black,format=yuv420p,setpts=PTS-STARTPTS",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
         f"{COMP}/spun-seg.mp4"], "pass4a spun segment")

# 4b: overlay spun segment + white flash + starburst onto hits3
run(E + ["-i", f"{COMP}/hits3.mp4",
         "-i", f"{COMP}/spun-seg.mp4",
         "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_white.png",
         "-i", f"{COMP}/v3-starburst-pop.mov",
         "-filter_complex",
         f"[0:v]format=yuv420p[base];"
         f"[base][1:v]overlay=0:0:enable='{win(H4,0.6)}'[b1];"
         f"[2:v]{FW}[fw];[3:v]format=rgba[sb];"
         f"[b1][fw]overlay=0:0:enable='{win(H4)}'[b2];"
         f"[b2][sb]overlay=(W-w)/2:(H-h)/2:enable='{win(H4,POP_D)}',format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "16", "-preset", "fast", f"{COMP}/hits4.mp4"], "pass4b spin composite")

sz = os.path.getsize(f"{COMP}/hits4.mp4")
print(f"hits4.mp4: {sz} bytes", flush=True)
assert sz > 30_000_000, "hits4.mp4 too small"
print("PASS4 OK")
