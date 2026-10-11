#!/usr/bin/env python3
"""LOTI v3 score upgrade — owner direction 2026-10-10 (voice-transcribed):
1. ORIGINAL suspense bed 0 -> freeze (~34.5s): low drone, dissonant swells,
   heartbeat pulse, riser into the freeze, hard cut. Ducked under dialogue.
2. ORIGINAL upbeat cartoon/commercial bed 34.8 -> end (Looney Tunes vibe),
   ducked under the sign-off voice.
3. New Piper sign-off voice at 53.0s ("Th-th-th-that's the Irish, folks!"),
   replacing the temp TTS read (old track zeroed 53.4 -> end).
ALL music 100% original numpy synthesis. No samples, no library music.
Video untouched (stream copy). Same duration.
"""
import numpy as np, subprocess, os, sys

D = os.path.dirname(os.path.abspath(__file__))
SR = 44100
BASE_WAV = "/tmp/loti-current-audio.wav"
VOICE_WAV = "/tmp/piper-ryan.wav"          # "Th-th-th-that's the Irish, folks!"
OUT_WAV = os.path.join(D, "v3-audio-scored.wav")
OUT_MP4 = os.path.join(D, "luck-of-the-irish-commercial-v3.mp4")
SRC_MP4 = OUT_MP4 + ".score-src"            # safety copy of pre-score cut
FF = ["ffmpeg", "-y", "-v", "error"]
rng = np.random.default_rng(11)

def load_wav(p):
    import wave
    w = wave.open(p); n = w.getnframes(); ch = w.getnchannels(); sr = w.getframerate()
    assert sr == SR, f"sr {sr}"
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    return x.reshape(-1, ch)

def save_wav(p, x):
    import wave
    x = np.clip(x, -1, 1)
    w = wave.open(p, "wb"); w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

def env_smooth(x, win_s=0.3):
    mono = x.mean(axis=1)
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, mode="same"))
    k = np.ones(int(win_s * SR)) / int(win_s * SR)
    return np.convolve(rms, k, mode="same")

# ---------------- 1. suspense bed ----------------
def synth_suspense():
    dur = 34.5; n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    # low drone: 55 + 55.7 (beating) + 82.4, slow LFO
    lfo = 0.72 + 0.28 * np.sin(2 * np.pi * 0.09 * t)
    y += (0.5 * np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 55.7 * t)
          + 0.30 * np.sin(2 * np.pi * 82.41 * t)) * lfo * 0.45
    # dissonant string-ish swells (minor 2nd cluster), 3s attack
    for st0 in (4.0, 12.0, 20.0, 28.0):
        m = (t >= st0) & (t < st0 + 7.0)
        tt = t[m] - st0
        a = np.clip(tt / 3.0, 0, 1); r = np.clip((7.0 - tt) / 3.0, 0, 1)
        e = np.minimum(a, r)
        chord = np.zeros_like(tt)
        for f0, amp in ((110.0, 0.5), (116.54, 0.45), (164.81, 0.30), (233.08, 0.20)):
            vib = 1 + 0.0012 * np.sin(2 * np.pi * 5.5 * tt)
            for h, ha in ((1, 1.0), (2, 0.4), (3, 0.22), (4, 0.10)):
                chord += amp * ha * np.sin(2 * np.pi * f0 * h * vib * tt)
        y[m] += chord * e * 0.14
    # heartbeat pulse, 48 bpm, lub-dub
    beat = 60.0 / 48.0
    bt = 0.0
    while bt < dur:
        for off, g in ((0.0, 1.0), (0.32, 0.65)):
            s = int((bt + off) * SR); e = min(n, s + int(0.35 * SR))
            if s < n:
                tt2 = np.arange(e - s) / SR
                y[s:e] += g * 0.42 * np.sin(2 * np.pi * 52 * tt2) * np.exp(-tt2 * 16)
        bt += beat
    # riser 29.5 -> 34.5: rising sweep + rising noise, hard cut at freeze
    rs, re_ = 29.5, 34.5
    m = (t >= rs) & (t < re_)
    tt = t[m] - rs; Dd = re_ - rs; k = tt / Dd
    f = 150.0 * 8.0 ** k
    ph = 2 * np.pi * np.cumsum(f) / SR
    sweep = np.sin(ph) * 0.55 + 0.28 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
    nz = rng.standard_normal(len(tt))
    y[m] += (sweep * 0.6 + nz * 0.22) * (k ** 2.2) * 0.85
    return y * 0.55

# ---------------- 2. upbeat cartoon bed ----------------
def midi(m): return 440.0 * 2 ** ((m - 69) / 12.0)

def pluck(f0, dur_s, bright=0.35):
    n = int(dur_s * SR); t = np.arange(n) / SR
    e = np.exp(-t * (6.0 / max(dur_s, 0.05)) * 0.28)
    return (np.sin(2 * np.pi * f0 * t) + bright * np.sin(2 * np.pi * 3 * f0 * t)) * e

def kick():
    n = int(0.16 * SR); t = np.arange(n) / SR
    f = 42 + 78 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22) * 0.9

def snare():
    n = int(0.14 * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    return (nz * 0.55 * np.exp(-t * 30) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)) * 0.7

def hat(open_=False):
    n = int((0.09 if open_ else 0.045) * SR)
    nz = np.diff(rng.standard_normal(n + 1))
    return nz * np.exp(-np.arange(n) / SR * (90 if not open_ else 30)) * 0.30

def synth_upbeat():
    start, end = 34.8, 56.5
    dur = end - start; n = int(dur * SR)
    y = np.zeros(n)
    bpm = 132.0; beat = 60.0 / bpm
    progs = [48, 43, 45, 41]  # C G Am F (midi roots), one per bar
    K, S, H = kick(), snare(), hat()
    def put(seg, at_s):
        s = int(at_s * SR); e = min(n, s + len(seg))
        if s < n: y[s:e] += seg[:e - s]
    bar = 4 * beat
    nbar = 12
    for b in range(nbar):
        root = progs[b % 4]; t0 = b * bar
        # drums: bouncy kick 1, 2&, 3, 4& ; snare 2,4 ; swung hats 8ths
        for bt_pos in (0, 1.5, 2, 3.5): put(K, t0 + bt_pos * beat)
        for bt_pos in (1, 3): put(S, t0 + bt_pos * beat)
        for e8 in range(8):
            sw = 0.06 * beat if e8 % 2 else 0.0
            put(H, t0 + e8 * 0.5 * beat + sw)
        # bass bounce: R R 5 R | R R 5 8
        pat = [0, 0, 7, 0, 0, 0, 7, 12]
        for e8, iv in enumerate(pat):
            put(pluck(midi(root + iv - 12), 0.22, 0.25) * 0.55, t0 + e8 * 0.5 * beat)
        # offbeat stab chords
        chord = {48: (60, 64, 67), 43: (59, 62, 67), 45: (57, 60, 64), 41: (53, 57, 60)}[root]
        for bt_pos in (0.5, 1.5, 2.5, 3.5):
            st = np.zeros(int(0.14 * SR)); tt = np.arange(len(st)) / SR
            for mm in chord: st += np.sin(2 * np.pi * midi(mm) * tt)
            put(st * np.exp(-tt * 28) * 0.16, t0 + bt_pos * beat)
        # melody: 2-bar phrases A / B
        if b % 2 == 0:
            mel = [(0, .5, 76), (.5, .5, 79), (1, .5, 81), (1.5, .5, 79), (2, 1, 76),
                   (3, .5, 74), (3.5, .5, 72), (4, .5, 74), (4.5, .5, 76), (5, 1, 79), (6, 2, 76)]
        else:
            mel = [(0, .5, 72), (.5, .5, 76), (1, .5, 79), (1.5, .5, 81), (2, 1, 83),
                   (3, .5, 81), (3.5, .5, 79), (4, .5, 76), (4.5, .5, 74), (5, 1, 76), (6, 2, 72)]
        for off_b, d_b, mm in mel:
            put(pluck(midi(mm), d_b * beat * 0.95) * 0.5, t0 + off_b * beat)
    # final tag: ascending run + big C hit + sparkle
    tag_t = 11 * bar
    for i, mm in enumerate((72, 74, 76, 79, 81, 84)):
        put(pluck(midi(mm), 0.16) * 0.55, tag_t + i * 0.5 * beat)
    hit_t = tag_t + 3.5 * beat
    big = np.zeros(int(0.6 * SR)); tt = np.arange(len(big)) / SR
    for mm in (48, 52, 55, 60, 64, 72):
        big += np.sin(2 * np.pi * midi(mm) * tt)
    put(big * np.exp(-tt * 5) * 0.22, hit_t)
    put(np.sin(2 * np.pi * 2093 * tt) * np.exp(-tt * 9) * 0.25, hit_t + 0.02)
    # fades
    fi = int(0.8 * SR); y[:fi] *= np.linspace(0, 1, fi)
    fo = int(0.4 * SR); y[-fo:] *= np.linspace(1, 0, fo)
    return y * 0.5, start

# ---------------- 3. voice ----------------
def prep_voice():
    # pitch up +3 semitones, cartoon lift; to 44.1k stereo.
    # Committed asset: audio/leprechaun-line-v2.wav (never overwritten by hand).
    out = os.path.join(D, "audio", "leprechaun-line-v2.wav")
    r = subprocess.run(FF + ["-i", VOICE_WAV, "-af",
        "rubberband=pitch=1.189207,aresample=44100,aformat=channel_layouts=stereo,volume=0.9",
        "-c:a", "pcm_s16le", out], capture_output=True)
    assert r.returncode == 0, "voice prep failed"
    return load_wav(out)

# ---------------- assemble ----------------
def main():
    print("loading base...", flush=True)
    base = load_wav(BASE_WAV)
    N = len(base)
    T = N / SR
    print(f"base dur {T:.3f}s", flush=True)

    # kill temp sign-off read (53.4 -> end was silent except temp voice)
    base2 = base.copy()
    z0 = int(53.4 * SR)
    fz = min(int(0.05 * SR), N - z0)
    if fz > 0:
        base2[z0:z0 + fz] *= np.linspace(1, 0, fz)[:, None]
    if z0 + fz < N:
        base2[z0 + fz:] = 0

    mix = base2.copy()

    # suspense bed, ducked by base envelope:
    # dialogue sits ~0.02 RMS, gaps ~0.005 -> full duck above 0.012, full bed below 0.005
    # duck floor 0.10 keeps dialogue +6dB over the bed; gaps still feel the bed
    print("synth suspense...", flush=True)
    sus = synth_suspense()
    e = env_smooth(base2)
    duck_k = np.clip((0.012 - e) / (0.012 - 0.005), 0, 1)
    gain = 0.10 + 0.90 * duck_k
    # the riser (29.5->34.5) rides at FULL gain over everything: it is an effect,
    # not ambience — it must overwhelm into the freeze-frame hard cut
    gain[int(29.5 * SR):] = 1.0
    sus_g = np.zeros(N); m = min(len(sus), N)
    sus_g[:m] = sus[:m] * gain[:m]
    mix += np.stack([sus_g, sus_g], axis=1) * 0.65

    # upbeat bed 34.8 -> 56.5, ducked under voice 52.8 -> 55.8
    print("synth upbeat...", flush=True)
    up, ustart = synth_upbeat()
    up_g = np.zeros(N); s0 = int(ustart * SR); m2 = min(len(up), N - s0)
    uv = up[:m2].copy()
    d0, d1 = int((52.8 - ustart) * SR), int((55.8 - ustart) * SR)
    d0 = max(d0, 0); d1 = min(d1, len(uv))
    if d1 > d0:
        ramp = int(0.3 * SR)
        g = np.ones(len(uv)); g[d0:d1] = 0.22
        g[d0 - ramp:d0] = np.linspace(1, 0.22, ramp) if d0 - ramp >= 0 else g[d0 - ramp:d0]
        g[d1:d1 + ramp] = np.linspace(0.22, 1, ramp)
        uv *= g
    up_g[s0:s0 + m2] = uv
    mix += np.stack([up_g, up_g], axis=1)

    # new voice at 53.0s
    print("voice...", flush=True)
    v = prep_voice()
    v0 = int(53.0 * SR); m3 = min(len(v), N - v0)
    mix[v0:v0 + m3] += v[:m3] * 1.25
    print(f"voice placed at 53.0s, dur {len(v)/SR:.2f}s, peak {np.abs(v).max():.3f}", flush=True)

    # peak normalize to -1 dBFS
    peak = np.abs(mix).max()
    mix *= (10 ** (-1 / 20)) / max(peak, 1e-6)
    print(f"mix peak before norm {peak:.3f}, after {np.abs(mix).max():.4f}", flush=True)
    save_wav(OUT_WAV, mix)

    # mux: video stream copy from the safety copy, new audio
    if not os.path.exists(SRC_MP4):
        os.link(OUT_MP4, SRC_MP4)
        print("safety copy linked", flush=True)
    tmp_out = OUT_MP4 + ".tmp.mp4"
    r = subprocess.run(FF + ["-i", SRC_MP4, "-i", OUT_WAV,
                             "-map", "0:v", "-map", "1:a",
                             "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                             "-movflags", "+faststart", tmp_out], capture_output=True)
    assert r.returncode == 0, f"mux failed: {r.stderr.decode()[-500:]}"
    os.replace(tmp_out, OUT_MP4)
    print("mux ok ->", OUT_MP4, flush=True)

if __name__ == "__main__":
    main()
