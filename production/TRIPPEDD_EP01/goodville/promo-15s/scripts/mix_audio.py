#!/usr/bin/env python3
"""Assemble the 15s promo audio: TEMP scratch dialogue + synthesized whack SFX.
All synthetic, no AI voice cloning. Whacks are numpy-synthesized (sine burst + noise)."""
import numpy as np, wave, os, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(BASE, "audio")
SR, DUR = 22050, 15.0
N = int(SR * DUR)

def load_wav(p):
    w = wave.open(p)
    assert w.getframerate() == SR and w.getnchannels() == 1, p
    data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    w.close()
    return data

def whack():
    t = np.arange(int(SR*0.14)) / SR
    tone = np.sin(2*np.pi*95*t) * np.exp(-t*38)
    click = np.random.default_rng(3).standard_normal(len(t)) * np.exp(-t*90) * 0.5
    s = (tone + click)
    return (s / np.abs(s).max() * 15000).astype(np.int16)

mix = np.zeros(N)
def place(data, at_sec):
    i = int(at_sec * SR)
    j = min(N, i + len(data))
    mix[i:j] += data[:j-i]

place(load_wav(os.path.join(AUDIO, "line1_TEMP.wav")), 0.3)
place(load_wav(os.path.join(AUDIO, "line2a_TEMP.wav")), 3.3)
place(load_wav(os.path.join(AUDIO, "line2b_TEMP.wav")), 11.0)
place(whack().astype(float), 10.33)   # punch 1 (f248)
place(whack().astype(float), 11.67)   # punch 2 (f280)

mix = np.clip(mix, -32768, 32767).astype(np.int16)
out = os.path.join(AUDIO, "promo_mix_TEMP.wav")
w = wave.open(out, "w")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(mix.tobytes()); w.close()
print("wrote", out, f"{len(mix)/SR:.2f}s")
