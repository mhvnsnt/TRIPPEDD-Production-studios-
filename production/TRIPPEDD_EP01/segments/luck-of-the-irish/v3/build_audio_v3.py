#!/usr/bin/env python3
"""V3 audio: production bed 0->35.7 untouched, riser 22.9->35,
impacts at each part-beat HIT (25.0/27.0/29.0/31.5/33.5 + 35.3),
poof burst @35.3, reveal sting @35.7. Cards near-silent. Peak-normalized, no clip."""
import numpy as np, subprocess, os

D = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(os.path.dirname(D), "luck-of-the-irish-commercial-final.mp4")
SR = 44100
OUT = os.path.join(D, "v3-audio-beats.wav")

# 1. production bed: v1 audio 0->40s
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0", "-t", "40", "-i", V1,
                      "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
bed = np.frombuffer(raw.stdout, dtype=np.float32).reshape(-1, 2)
n = len(bed)
mix = bed.copy()

def add(stereo, t, dur, fn):
    s = int(t*SR); e = min(n, s+int(dur*SR))
    if s >= n: return
    seg = fn(np.arange(e-s)/SR, dur)
    m = min(len(seg), e-s)
    stereo[s:s+m] += seg[:m][:, None] if seg.ndim == 1 else seg[:m]

rng = np.random.default_rng(7)

# 2. riser 22.9->35: rising filtered noise, Hulk-hum style low throb + sheen
def riser(t, dur):
    env = (t/dur)**2.2
    noise = rng.standard_normal(len(t))
    # crude rising sweep: mix of low throb (55->110Hz) and airy noise
    throb = np.sin(2*np.pi*(55+55*t/dur)*t) * 0.5
    return (noise*0.25 + throb) * env * 0.55
add(mix, 22.9, 12.1, riser)

# 3. impacts at each HIT: punchy sine-drop + click
def impact(t, dur, base=90.0):
    f = base*np.exp(-t*6) + 38
    tone = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9)
    click = rng.standard_normal(len(t)) * np.exp(-t*60) * 0.6
    return (tone*0.9 + click) * 0.8
for ht in [25.0, 27.0, 29.0, 31.5, 33.5, 35.3]:
    add(mix, ht, 0.6, impact)

# 4. poof burst @35.3: soft noise whoosh
def poof(t, dur):
    return rng.standard_normal(len(t)) * np.exp(-((t-0.15)/0.12)**2) * 0.5
add(mix, 35.3, 0.5, poof)

# 5. reveal sting @35.7: bright rising major arp (C E G C), cartoon hero
def sting(t, dur):
    notes = [261.63, 329.63, 392.0, 523.25]
    y = np.zeros_like(t)
    for i, f0 in enumerate(notes):
        st = i*0.09
        m = t >= st
        tt = t[m]-st
        y[m] += np.sin(2*np.pi*f0*tt)*np.exp(-tt*4)*0.35
    return y
add(mix, 35.7, 1.2, sting)

# 6. cards near-silent: duck everything after 39s
duck = int(39*SR)
if duck < n:
    fade = np.linspace(1, 0, min(n-duck, 2*SR))
    mix[duck:duck+len(fade)] *= fade[:, None]
    mix[duck+len(fade):] = 0

# 7. peak normalize to -1 dBFS (no clipping)
peak = np.abs(mix).max()
mix *= (10**(-1/20)) / max(peak, 1e-6)
print(f"peak before norm: {peak:.3f}, after: {np.abs(mix).max():.4f}")

st = mix.astype(np.float32).tobytes()
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2",
                "-i", "-", "-c:a", "pcm_s16le", OUT], input=st, check=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
