#!/usr/bin/env python3
"""LOTI commercial v3 — audio timeline builder. Run from the v3/ dir."""
import subprocess, os, sys

V3 = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(os.path.dirname(V3), "luck-of-the-irish-commercial-final.mp4")
FF = ["ffmpeg", "-y", "-v", "error"]
SR = 48000

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label} failed", flush=True); sys.exit(1)

def sine(f, d, dst):
    run(FF + ["-f", "lavfi", "-i", f"sine=frequency={f}:duration={d}:sample_rate={SR}",
              "-c:a", "pcm_s16le", dst], f"sine {f}Hz")

def noise(d, dst, color="pink"):
    run(FF + ["-f", "lavfi", "-i", f"anoisesrc=color={color}:duration={d}:sample_rate={SR}",
              "-c:a", "pcm_s16le", dst], f"noise {d}s")

# ---- production bed 0->35 (untouched) ----
run(FF + ["-ss", "0", "-t", "35", "-i", V1, "-vn", "-c:a", "pcm_s16le", "tmp-v3-bed35.wav"], "v1 bed 0-35")

# ---- riser 22.9->35 (12.1s): layered sines + noise, exp crescendo ----
sine(90, 12.1, "tmp-v3-r1.wav"); sine(180, 12.1, "tmp-v3-r2.wav"); noise(12.1, "tmp-v3-rn.wav")
run(FF + ["-i", "tmp-v3-r1.wav", "-i", "tmp-v3-r2.wav", "-i", "tmp-v3-rn.wav", "-filter_complex",
    "[0:a]volume=0.35[s1];[1:a]volume=0.22[s2];[2:a]volume=0.30,lowpass=f=5000[ns];"
    "[s1][s2][ns]amix=inputs=3:normalize=0,volume=0.5,"
    "afade=t=in:st=0:d=12.1:curve=exp,adelay=22900|22900[riser]",
    "-map", "[riser]", "-c:a", "pcm_s16le", "tmp-v3-riser.wav"], "riser")

# ---- impacts ----
def impact(dst, gain=1.0, dur=0.7):
    run(FF + ["-f", "lavfi", "-i", f"sine=frequency=55:duration={dur}:sample_rate={SR}",
              "-f", "lavfi", "-i", "anoisesrc=color=white:duration=0.3:sample_rate=48000",
              "-filter_complex",
              "[0:a]volume=0.85,afade=t=out:st=0:d=0.65:curve=exp[b];"
              "[1:a]volume=0.5,afade=t=out:st=0:d=0.28:curve=exp[n];"
              f"[b][n]amix=inputs=2:normalize=0,volume={gain}[o]",
              "-map", "[o]", "-c:a", "pcm_s16le", dst], f"impact g={gain}")

impact("tmp-v3-imp1.wav", 0.9)   # K1 slam @ 25.5
impact("tmp-v3-imp2.wav", 1.0)   # K2 slam @ 29
impact("tmp-v3-imp3.wav", 1.15)  # K3/jump @ 33.5
impact("tmp-v3-imp4.wav", 1.3)   # poof @ 35.3
run(FF + ["-i", "tmp-v3-imp1.wav", "-i", "tmp-v3-imp2.wav", "-i", "tmp-v3-imp3.wav", "-i", "tmp-v3-imp4.wav",
          "-filter_complex",
          "[0:a]adelay=25500|25500,apad=whole_dur=38[i1];"
          "[1:a]adelay=29000|29000,apad=whole_dur=38[i2];"
          "[2:a]adelay=33500|33500,apad=whole_dur=38[i3];"
          "[3:a]adelay=35300|35300,apad=whole_dur=38[i4];"
          "[i1][i2][i3][i4]amix=inputs=4:normalize=0,atrim=duration=38[imps]",
          "-map", "[imps]", "-c:a", "pcm_s16le", "tmp-v3-imps.wav"], "impacts placed")

# ---- reveal sting @ 35.7: bright major chord stab ----
sine(220, 1.8, "tmp-v3-st1.wav"); sine(277.18, 1.8, "tmp-v3-st2.wav"); sine(329.63, 1.8, "tmp-v3-st3.wav"); sine(440, 1.8, "tmp-v3-st4.wav")
run(FF + ["-i", "tmp-v3-st1.wav", "-i", "tmp-v3-st2.wav", "-i", "tmp-v3-st3.wav", "-i", "tmp-v3-st4.wav",
          "-filter_complex",
          "[0:a]volume=0.35,afade=t=out:st=0:d=1.7:curve=exp[s1];"
          "[1:a]volume=0.35,afade=t=out:st=0:d=1.7:curve=exp[s2];"
          "[2:a]volume=0.35,afade=t=out:st=0:d=1.7:curve=exp[s3];"
          "[3:a]volume=0.30,afade=t=out:st=0:d=1.7:curve=exp[s4];"
          "[s1][s2][s3][s4]amix=inputs=4:normalize=0,adelay=35700|35700,apad=whole_dur=38[sting]",
          "-map", "[sting]", "-c:a", "pcm_s16le", "tmp-v3-sting.wav"], "reveal sting")

# ---- poof noise burst @ 35.3 ----
noise(0.5, "tmp-v3-poofn.wav", color="white")
run(FF + ["-i", "tmp-v3-poofn.wav", "-filter_complex",
          "[0:a]volume=0.6,lowpass=f=3000,afade=t=out:st=0:d=0.45:curve=exp,adelay=35300|35300,apad=whole_dur=38[pf]",
          "-map", "[pf]", "-c:a", "pcm_s16le", "tmp-v3-poof.wav"], "poof burst")

# ---- mix all: 38s master, cards tail silence appended at assembly ----
run(FF + ["-i", "tmp-v3-bed35.wav", "-i", "tmp-v3-riser.wav", "-i", "tmp-v3-imps.wav",
          "-i", "tmp-v3-sting.wav", "-i", "tmp-v3-poof.wav", "-filter_complex",
          "[0:a]apad=whole_dur=38[bed];"
          "[bed][1:a][2:a][3:a][4:a]amix=inputs=5:normalize=0,alimiter=limit=0.95[aout]",
          "-map", "[aout]", "-c:a", "pcm_s16le", "v3-audio-38s.wav"], "mix 38s")
print("AUDIO DONE: v3-audio-38s.wav")
