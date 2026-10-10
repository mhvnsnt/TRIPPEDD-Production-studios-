#!/usr/bin/env python3
"""build_soundscape.py — original 50s Wizard Gang pilot soundscape (numpy synthesis).

All sounds are synthesized from scratch (filtered noise, sine drops, metallic
ticks). No samples, no recordings — zero license baggage. Layout follows the
SHORT_01 storyboard AUD lines exactly.

Shot map (seconds): 1:0-5  2:5-11  3:11-16  4:16-21  5:21-27  6:27-32
                    7:32-37  8:37-42 (8a 37-39.5, 8b reveal 39.5-42)  9:42-50
Usage: python3 build_soundscape.py -o soundscape_50s.wav
"""
import argparse, os
import numpy as np
import wave

SR = 44100
DUR = 50.0
N = int(SR * DUR)
rng = np.random.default_rng(20261007)


def write_wav(path, s):
    s = np.clip(s, -1, 1)
    pcm = (s * 32767).astype(np.int16)
    with wave.open(path, "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(pcm.tobytes())


def blank():
    return np.zeros(N)


def add(dst, sig, t):
    i = int(t * SR)
    j = min(N, i + len(sig))
    dst[i:j] += sig[:j - i]
    return dst


def lowpass(x, k=64):
    ker = np.ones(k) / k
    return np.convolve(x, ker, mode="same")


def room_tone(dur, level=0.05):
    """City-night bed: lowpassed noise, slow swell."""
    n = int(dur * SR)
    s = lowpass(rng.standard_normal(n), 256)
    s /= np.abs(s).max() + 1e-9
    swell = 0.7 + 0.3 * np.sin(2 * np.pi * np.arange(n) / (SR * 9))
    return s * swell * level


def wind(dur, level=0.06):
    n = int(dur * SR)
    s = lowpass(rng.standard_normal(n), 512)
    s /= np.abs(s).max() + 1e-9
    gust = 0.5 + 0.5 * np.sin(2 * np.pi * np.arange(n) / (SR * 7) + 1.3) ** 2
    return s * gust * level


def fire_crackle(dur, level=0.10, density=26):
    """Random bandpassed pops over a soft hiss."""
    n = int(dur * SR)
    out = lowpass(rng.standard_normal(n), 48) * 0.25
    for _ in range(int(dur * density)):
        t = rng.random() * dur
        ln = int(SR * (0.02 + rng.random() * 0.06))
        pop = rng.standard_normal(ln) * np.exp(-np.arange(ln) / (SR * 0.015))
        i = int(t * SR)
        if i + ln < n:
            out[i:i + ln] += pop * (0.4 + rng.random() * 0.6)
    out /= np.abs(out).max() + 1e-9
    return out * level


def sub_hit(t0=0.0, dur=1.6, f0=70, f1=34, level=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.exp(-t / 0.45)
    return np.sin(ph) * env * level


def sub_swell(dur, level=0.22):
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = np.sin(np.pi * t / dur) ** 2
    return np.sin(2 * np.pi * 48 * t) * env * level


def chains(dur, level=0.12, n_hits=7):
    """Metallic ticks: short highpassed noise bursts, clustered."""
    n = int(dur * SR)
    out = np.zeros(n)
    for _ in range(n_hits):
        t = rng.random() * dur
        ln = int(SR * 0.05)
        tick = rng.standard_normal(ln)
        tick = tick - lowpass(tick, 8)  # crude highpass
        tick *= np.exp(-np.arange(ln) / (SR * 0.012))
        i = int(t * SR)
        if i + ln < n:
            out[i:i + ln] += tick * (0.5 + rng.random() * 0.5)
    out /= np.abs(out).max() + 1e-9
    return out * level


def drum_hits(times, level=0.4, f0=95, f1=45, dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    one = np.sin(ph) * np.exp(-t / 0.16) * level
    out = blank()
    for tt in times:
        add(out, one, tt)
    return out


def bell(t0=0.0, level=0.25):
    dur = 2.5
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 660 * t) * np.exp(-t / 0.9)
         + 0.4 * np.sin(2 * np.pi * 1320 * t) * np.exp(-t / 0.5))
    return s * level


def heartbeat(t0, level=0.5):
    out = blank()
    add(out, sub_hit(dur=0.5, f0=65, f1=38, level=level), t0)
    add(out, sub_hit(dur=0.5, f0=58, f1=34, level=level * 0.8), t0 + 0.32)
    return out


def siren(t0, dur=4.0, level=0.02):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 700 + 120 * np.sin(2 * np.pi * 0.25 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * level * np.sin(np.pi * t / dur) ** 2


def sting(t0, level=0.4):
    """Ident sting: short riser into a hit."""
    out = blank()
    n = int(1.2 * SR); t = np.arange(n) / SR
    riser = np.sin(2 * np.pi * np.linspace(220, 880, n) * t) * (t / 1.2) * 0.25
    add(out, riser, t0)
    add(out, sub_hit(dur=1.4, f0=90, f1=40, level=level), t0 + 1.2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="soundscape_50s.wav")
    a = ap.parse_args()

    mix = blank()
    # Bed: room tone + wind across the whole 50s (ducks under cards at the end)
    mix += room_tone(DUR, 0.045)
    mix += wind(DUR, 0.05)

    # SHOT 1 (0-5): fire crackle + sub-bass swell into shot 2
    mix = add(mix, fire_crackle(6.0, 0.10), 0.0)
    mix = add(mix, sub_swell(5.0, 0.20), 0.5)

    # SHOT 2 (5-11): chains + single sub hit as he faces camera (~10)
    mix = add(mix, chains(6.0, 0.12, 8), 5.0)
    mix = add(mix, sub_hit(dur=1.6, level=0.5), 9.8)

    # SHOT 3 (11-16): fire crackle rises, low ritual drum enters
    mix = add(mix, fire_crackle(5.0, 0.13, 34), 11.0)
    mix = add(mix, drum_hits([11.5, 13.0, 14.5], 0.38), 0)

    # SHOT 4 (16-21): ritual drum + faint distant siren
    mix = add(mix, drum_hits([16.2, 17.4, 18.6, 19.8], 0.36), 0)
    mix = add(mix, siren(17.0, 4.0, 0.018), 0)

    # SHOT 5 (21-27): drum pattern doubles + chains
    mix = add(mix, drum_hits([21.2, 22.0, 22.8, 23.6, 24.4, 25.2, 26.0], 0.36), 0)
    mix = add(mix, chains(6.0, 0.10, 6), 21.0)

    # SHOT 6 (27-32): drum + single deep bell
    mix = add(mix, drum_hits([27.3, 28.8, 30.3], 0.36), 0)
    mix = add(mix, bell(0, 0.22), 29.0)

    # SHOT 7 (32-37): drop to fire crackle + one heartbeat bass pulse
    mix = add(mix, fire_crackle(5.0, 0.09, 22), 32.0)
    mix = add(mix, heartbeat(34.5, 0.5), 0)

    # SHOT 8 (37-42): breath of wind, drum stops for one beat (~40)
    w = wind(5.0, 0.09)
    mix = add(mix, w, 37.0)

    # SHOT 9 (42-50): music cuts; fading chains, then ident sting
    mix = add(mix, chains(4.0, 0.08, 4), 42.0)
    mix = add(mix, sting(45.5, 0.4), 0)

    # gentle master fade at the very end
    nfade = int(SR * 1.5)
    mix[-nfade:] *= np.linspace(1, 0, nfade)
    mix /= np.abs(mix).max() + 1e-9
    mix *= 0.89

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    write_wav(a.out, mix)
    print(f"WROTE {a.out}  {DUR:.1f}s")


if __name__ == "__main__":
    main()
