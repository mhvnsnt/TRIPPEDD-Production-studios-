#!/usr/bin/env python3
"""LOTI commercial v2 — audio timeline builder. Run from the v2/ dir."""
import subprocess, os, sys

V2 = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(os.path.dirname(V2), "luck-of-the-irish-commercial-final.mp4")
FF = ["ffmpeg", "-y", "-v", "error"]

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label} failed", flush=True); sys.exit(1)

def sine(f, d, dst):
    run(FF + ["-f", "lavfi", "-i", f"sine=frequency={f}:duration={d}:sample_rate=48000",
              "-c:a", "pcm_s16le", dst], f"sine {f}Hz")

def noise(d, dst, color="pink"):
    run(FF + ["-f", "lavfi", "-i", f"anoisesrc=color={color}:duration={d}:sample_rate=48000",
              "-c:a", "pcm_s16le", dst], f"noise {d}s")

# ---- v1 production audio bed 0-35 -> timeline 0-37 (1s gaps at 24, 29) ----
for ss, t, n in [(0, 24, "a0"), (24, 4, "a1"), (28, 7, "a2")]:
    run(FF + ["-ss", str(ss), "-t", str(t), "-i", V1, "-vn",
              "-c:a", "pcm_s16le", f"tmp-{n}.wav"], f"v1 audio {n}")
run(FF + ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
           "-t", "1", "-c:a", "pcm_s16le", "tmp-sil1.wav"], "silence 1s")
run(FF + ["-i", "tmp-a0.wav", "-i", "tmp-sil1.wav", "-i", "tmp-a1.wav",
          "-i", "tmp-sil1.wav", "-i", "tmp-a2.wav",
          "-filter_complex", "[0:a][1:a][2:a][3:a][4:a]concat=n=5:v=0:a=1[bed]",
          "-map", "[bed]", "-c:a", "pcm_s16le", "tmp-bed37.wav"], "bed 37s")

# ---- riser 22.9-37.0 (14.1s): layered sines + noise, crescendo via afade ----
sine(90, 14.1, "tmp-r1.wav"); sine(180, 14.1, "tmp-r2.wav"); noise(14.1, "tmp-rn.wav")
run(FF + ["-i", "tmp-r1.wav", "-i", "tmp-r2.wav", "-i", "tmp-rn.wav", "-filter_complex",
    "[0:a]volume=0.35[s1];[1:a]volume=0.22[s2];[2:a]volume=0.30,lowpass=f=5000[ns];"
    "[s1][s2][ns]amix=inputs=3:normalize=0,volume=0.5,"
    "afade=t=in:st=0:d=14.1:curve=exp,adelay=22900|22900[riser]",
    "-map", "[riser]", "-c:a", "pcm_s16le", "tmp-riser.wav"], "riser")

# ---- impacts (afade decay envelopes) ----
def impact(dst, gain=1.0):
    run(FF + ["-f", "lavfi", "-i", "sine=frequency=55:duration=0.7:sample_rate=48000",
              "-f", "lavfi", "-i", "anoisesrc=color=white:duration=0.3:sample_rate=48000",
              "-filter_complex",
              "[0:a]volume=0.85,afade=t=out:st=0:d=0.65:curve=exp[b];"
              "[1:a]volume=0.5,afade=t=out:st=0:d=0.28:curve=exp[n];"
              f"[b][n]amix=inputs=2:normalize=0,volume={gain}[o]",
              "-map", "[o]", "-c:a", "pcm_s16le", dst], f"impact g={gain}")
impact("tmp-imp1.wav", 1.0); impact("tmp-imp2.wav", 1.0); impact("tmp-imp3.wav", 1.35)
run(FF + ["-i", "tmp-imp1.wav", "-i", "tmp-imp2.wav", "-i", "tmp-imp3.wav", "-filter_complex",
    "[0:a]adelay=24000|24000,apad=whole_dur=37[i1];"
    "[1:a]adelay=29000|29000,apad=whole_dur=37[i2];"
    "[2:a]adelay=37500|37500,apad=whole_dur=37[i3];"
    "[i1][i2][i3]amix=inputs=3:normalize=0,atrim=duration=37[imps]",
    "-map", "[imps]", "-c:a", "pcm_s16le", "tmp-imps.wav"], "impacts placed")

# ---- whoosh 38.5-41.8 (swell) + sting 41.8, on 7.3s tail bed ----
noise(3.3, "tmp-wh.wav", color="white")
sine(220, 1.5, "tmp-st1.wav"); sine(277.18, 1.5, "tmp-st2.wav"); sine(329.63, 1.5, "tmp-st3.wav")
run(FF + ["-i", "tmp-wh.wav", "-i", "tmp-st1.wav", "-i", "tmp-st2.wav", "-i", "tmp-st3.wav",
    "-filter_complex",
    "[0:a]volume=0.55,highpass=f=300,afade=t=in:st=0:d=1.65,afade=t=out:st=1.65:d=1.65,"
    "adelay=1500|1500,apad=whole_dur=7.3[wh];"
    "[1:a]volume=0.4,afade=t=out:st=0:d=1.4:curve=exp[s1];"
    "[2:a]volume=0.4,afade=t=out:st=0:d=1.4:curve=exp[s2];"
    "[3:a]volume=0.4,afade=t=out:st=0:d=1.4:curve=exp[s3];"
    "[s1][s2][s3]amix=inputs=3:normalize=0,adelay=4800|4800,apad=whole_dur=7.3[st];"
    "[wh][st]amix=inputs=2:normalize=0[tail]",
    "-map", "[tail]", "-c:a", "pcm_s16le", "tmp-tail73.wav"], "tail 7.3s")

# ---- part1: 44.3s ----
run(FF + ["-i", "tmp-bed37.wav", "-i", "tmp-riser.wav", "-i", "tmp-imps.wav",
          "-i", "tmp-tail73.wav", "-filter_complex",
    "[0:a][1:a][2:a]amix=inputs=3:normalize=0[p1];[p1][3:a]concat=n=2:v=0:a=1[part1]",
    "-map", "[part1]", "-c:a", "pcm_s16le", "tmp-part1.wav"], "part1 44.3s")

# ---- part2: card audios (v1 cards are video-only -> silence) ----
def card_audio(src, dst, silence_dur=None, trim_to=None):
    if silence_dur:
        run(FF + ["-f", "lavfi", "-i",
                  f"anullsrc=channel_layout=stereo:sample_rate=48000:d={silence_dur}",
                  "-c:a", "pcm_s16le", dst], f"silence {silence_dur}s for {src}")
    else:
        cmd = FF + ["-i", src, "-vn"]
        if trim_to:
            cmd += ["-af", f"atrim=duration={trim_to}"]
        cmd += ["-c:a", "pcm_s16le", dst]
        run(cmd, f"card audio {src}")

card_audio("card-2d-swap.mp4", "tmp-c1.wav", trim_to=3.0)
card_audio("../title-card.mp4", "tmp-c2.wav", silence_dur=4)
card_audio("card-slogan-1.mp4", "tmp-c3.wav", trim_to=3.0)
card_audio("../disclaimers-card.mp4", "tmp-c4.wav", silence_dur=8)
card_audio("card-thats-the-irish-folks.mp4", "tmp-c5.wav", trim_to=4.0)
run(FF + ["-i", "tmp-part1.wav", "-i", "tmp-c1.wav", "-i", "tmp-c2.wav", "-i", "tmp-c3.wav",
          "-i", "tmp-c4.wav", "-i", "tmp-c5.wav", "-filter_complex",
    "[0:a][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1,"
    "volume=0.89,alimiter=limit=0.89[aout]",
    "-map", "[aout]", "-c:a", "pcm_s16le", "v2-audio-66s.wav"], "full audio")

# ---- level check ----
r = subprocess.run(FF + ["-i", "v2-audio-66s.wav", "-af",
    "volumedetect,astats=metadata=1:reset=1", "-f", "null", "-"],
    capture_output=True, text=True)
for line in (r.stderr or "").splitlines():
    if "max_volume" in line or "RMS level" in line:
        print("   ", line.strip())
print("AUDIO DONE", flush=True)
