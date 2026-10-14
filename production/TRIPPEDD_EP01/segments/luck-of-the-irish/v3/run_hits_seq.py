#!/usr/bin/env python3
"""LOTI v3 HITS — sequential passes (one hit per ffmpeg invocation).
The monolithic 11-overlay graph gets SIGKILLed on this box; sequential
simple passes use a fraction of the memory. Intermediates at crf 16,
final at crf 18. Hit times from comp/v3-hittimes.txt."""
import subprocess, os, sys

D = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(D, "comp")
FX = os.path.join(D, "fx")
FLASH_D, POP_D = 0.4, 0.5

ht = {}
with open(os.path.join(COMP, "v3-hittimes.txt")) as f:
    for line in f:
        k, v = line.strip().split("=")
        ht[k] = float(v)
H1, H2, H3, H4, H5, T_JUMP = ht["H1"], ht["H2"], ht["H3"], ht["H4"], ht["H5"], ht["JUMP"]
print(f"HITS: {H1} {H2} {H3} {H4} {H5} JUMP={T_JUMP}", flush=True)

def win(t0, d=FLASH_D):
    return f"between(t,{t0:.3f},{t0+d:.3f})"

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label} rc={r.returncode}", flush=True); sys.exit(1)

E = ["ffmpeg", "-y", "-v", "error"]
FW = (f"scale=1920:1080,format=yuva420p,fade=t=in:st=0:d=0.08:alpha=1,"
      f"fade=t=out:st={FLASH_D-0.12}:d=0.12:alpha=1")

# pass 1: HIT1 eyes — white flash + starburst
if not os.path.exists(f"{COMP}/hits1.mp4"):
    run(E + ["-i", f"{COMP}/v3-base.mp4",
         "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_white.png",
         "-i", f"{COMP}/v3-starburst-pop.mov",
         "-filter_complex",
         f"[0:v]format=yuv420p[base];[1:v]{FW}[fw];[2:v]format=rgba[sb];"
         f"[base][fw]overlay=0:0:enable='{win(H1)}'[b1];"
         f"[b1][sb]overlay=(W-w)/2:(H-h)/2:enable='{win(H1,POP_D)}',format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "16", "-preset", "fast", f"{COMP}/hits1.mp4"], "pass1 HIT1 eyes")

# pass 2: HIT2 ears — white flash + SMALL STARBURST above the head (ears stay visible)
# (poof art was junky AI blobs — starburst is the clean authored hit)
if not os.path.exists(f"{COMP}/hits1.mp4"):
    raise SystemExit("hits1.mp4 missing — run pass 1 first")
run(E + ["-i", f"{COMP}/hits1.mp4",
         "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_white.png",
         "-i", f"{COMP}/v3-starburst-pop.mov",
         "-filter_complex",
         f"[0:v]format=yuv420p[base];[1:v]{FW}[fw];[2:v]format=rgba,scale=540:540[sb2];"
         f"[base][fw]overlay=0:0:enable='{win(H2)}'[b1];"
         f"[b1][sb2]overlay=(W-w)/2:(H-h)/2-380:enable='{win(H2,POP_D)}',format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "16", "-preset", "fast", f"{COMP}/hits2.mp4"], "pass2 HIT2 ears")

# pass 3: HIT3 grin — green flash + starburst
run(E + ["-i", f"{COMP}/hits2.mp4",
         "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_green.png",
         "-i", f"{COMP}/v3-starburst-pop.mov",
         "-filter_complex",
         f"[0:v]format=yuv420p[base];[1:v]{FW}[fg];[2:v]format=rgba[sb];"
         f"[base][fg]overlay=0:0:enable='{win(H3)}'[b1];"
         f"[b1][sb]overlay=(W-w)/2:(H-h)/2:enable='{win(H3,POP_D)}',format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "16", "-preset", "fast", f"{COMP}/hits3.mp4"], "pass3 HIT3 grin")

# pass 4: HIT4 tracksuit — spin gag, split into two sub-passes (memory-safe)
run(["python3", os.path.join(D, "run_pass4.py")], "pass4 HIT4 spin (split)")

# pass 5: HIT5 jump — white flash + speedlines through the hold
run(E + ["-i", f"{COMP}/hits4.mp4",
         "-loop", "1", "-t", str(FLASH_D), "-i", f"{FX}/flash_white.png",
         "-loop", "1", "-t", "2", "-i", f"{FX}/speedlines.png",
         "-filter_complex",
         f"[0:v]format=yuv420p[base];[1:v]{FW}[fw];"
         f"[2:v]scale=1920:1080,format=yuva420p[sl];"
         f"[base][fw]overlay=0:0:enable='{win(H5)}'[b1];"
         f"[b1][sl]overlay=0:0:enable='{win(T_JUMP,1.5)}',format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "18", "-preset", "fast", f"{COMP}/v3-hits.mp4"], "pass5 HIT5 jump")

sz = os.path.getsize(f"{COMP}/v3-hits.mp4")
print(f"v3-hits.mp4: {sz} bytes", flush=True)
assert sz > 10_000_000, "v3-hits.mp4 suspiciously small"
# cleanup intermediates
for f in ["hits1.mp4", "hits2.mp4", "hits3.mp4", "hits4.mp4"]:
    os.remove(os.path.join(COMP, f))
print("HITS SEQUENTIAL OK")
