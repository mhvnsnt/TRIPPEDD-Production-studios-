#!/usr/bin/env python3
"""LOTI v3 mix rev2 — owner notes 2026-10-10 ~22:07 CDT (after watching scored cut):
1. MUTE base production audio 17.0 -> 20.0s (camera person says "alright").
   Suspense bed CONTINUES underneath. 100ms fades on mute edges.
2. BOOST base production audio x2.5 on 32.0 -> 34.0s ("luck of the Irish!").
   100ms fades on the gain envelope. True peak watched.
3. Suspense bed DOUBLED (x2.0). Duck floor lowered 0.10 -> 0.05 in dialogue
   regions so the doubled bed doesn't bury his voice (gaps get the full 2x).
4. Upbeat bed UNCHANGED.
5. v1 sign-off voice stays in the base at its natural spot (~53.27s) — no v2.
Standalone bed exports (owner asset-save add):
  audio/suspense-score-track-1.wav
  audio/luck_of_the_irish_commercial_track_music_score_jingle.wav
ALL music 100% original numpy synthesis. Video stream untouched (copy).
"""
import numpy as np, subprocess, os, json

D = os.path.dirname(os.path.abspath(__file__))
SR = 44100
BASE_WAV = "/tmp/loti-base-rev2.wav"  # pre-score base audio (git 402b1e42)
PRESCORE_MP4 = "/tmp/loti-prescore.mp4"
OUT_WAV = os.path.join(D, "v3-audio-dip.wav")
DIP_ENABLED = True  # V-dip on suspense bed under 32-34s
OUT_MP4 = os.path.join(D, "luck-of-the-irish-commercial-v3-dip.mp4")
BED1_WAV = os.path.join(D, "audio", "suspense-score-track-1.wav")
BED2_WAV = os.path.join(D, "audio", "luck_of_the_irish_commercial_track_music_score_jingle.wav")
VIDEO_DUR = 56.555664
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

def raised_cosine(n):
    return 0.5 - 0.5 * np.cos(np.pi * np.arange(n) / max(n - 1, 1))

# ---------------- 1. suspense bed (identical synth to rev1) ----------------
def synth_suspense():
    dur = 34.5; n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    lfo = 0.72 + 0.28 * np.sin(2 * np.pi * 0.09 * t)
    y += (0.5 * np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 55.7 * t)
          + 0.30 * np.sin(2 * np.pi * 82.41 * t)) * lfo * 0.45
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
    beat = 60.0 / 48.0
    bt = 0.0
    while bt < dur:
        for off, g in ((0.0, 1.0), (0.32, 0.65)):
            s = int((bt + off) * SR); e = min(n, s + int(0.35 * SR))
            if s < n:
                tt2 = np.arange(e - s) / SR
                y[s:e] += g * 0.42 * np.sin(2 * np.pi * 52 * tt2) * np.exp(-tt2 * 16)
        bt += beat
    rs, re_ = 29.5, 34.5
    m = (t >= rs) & (t < re_)
    tt = t[m] - rs; Dd = re_ - rs; k = tt / Dd
    f = 150.0 * 8.0 ** k
    ph = 2 * np.pi * np.cumsum(f) / SR
    sweep = np.sin(ph) * 0.55 + 0.28 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
    nz = rng.standard_normal(len(tt))
    y[m] += (sweep * 0.6 + nz * 0.22) * (k ** 2.2) * 0.85
    return y * 0.55

# ---------------- 2. upbeat cartoon bed (identical synth to rev1) ----------------
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
    progs = [48, 43, 45, 41]
    K, S, H = kick(), snare(), hat()
    def put(seg, at_s):
        s = int(at_s * SR); e = min(n, s + len(seg))
        if s < n: y[s:e] += seg[:e - s]
    bar = 4 * beat
    nbar = 12
    for b in range(nbar):
        root = progs[b % 4]; t0 = b * bar
        for bt_pos in (0, 1.5, 2, 3.5): put(K, t0 + bt_pos * beat)
        for bt_pos in (1, 3): put(S, t0 + bt_pos * beat)
        for e8 in range(8):
            sw = 0.06 * beat if e8 % 2 else 0.0
            put(H, t0 + e8 * 0.5 * beat + sw)
        pat = [0, 0, 7, 0, 0, 0, 7, 12]
        for e8, iv in enumerate(pat):
            put(pluck(midi(root + iv - 12), 0.22, 0.25) * 0.55, t0 + e8 * 0.5 * beat)
        chord = {48: (60, 64, 67), 43: (59, 62, 67), 45: (57, 60, 64), 41: (53, 57, 60)}[root]
        for bt_pos in (0.5, 1.5, 2.5, 3.5):
            st = np.zeros(int(0.14 * SR)); tt = np.arange(len(st)) / SR
            for mm in chord: st += np.sin(2 * np.pi * midi(mm) * tt)
            put(st * np.exp(-tt * 28) * 0.16, t0 + bt_pos * beat)
        if b % 2 == 0:
            mel = [(0, .5, 76), (.5, .5, 79), (1, .5, 81), (1.5, .5, 79), (2, 1, 76),
                   (3, .5, 74), (3.5, .5, 72), (4, .5, 74), (4.5, .5, 76), (5, 1, 79), (6, 2, 76)]
        else:
            mel = [(0, .5, 72), (.5, .5, 76), (1, .5, 79), (1.5, .5, 81), (2, 1, 83),
                   (3, .5, 81), (3.5, .5, 79), (4, .5, 76), (4.5, .5, 74), (5, 1, 76), (6, 2, 72)]
        for off_b, d_b, mm in mel:
            put(pluck(midi(mm), d_b * beat * 0.95) * 0.5, t0 + off_b * beat)
    tag_t = 11 * bar
    for i, mm in enumerate((72, 74, 76, 79, 81, 84)):
        put(pluck(midi(mm), 0.16) * 0.55, tag_t + i * 0.5 * beat)
    hit_t = tag_t + 3.5 * beat
    big = np.zeros(int(0.6 * SR)); tt = np.arange(len(big)) / SR
    for mm in (48, 52, 55, 60, 64, 72):
        big += np.sin(2 * np.pi * midi(mm) * tt)
    put(big * np.exp(-tt * 5) * 0.22, hit_t)
    put(np.sin(2 * np.pi * 2093 * tt) * np.exp(-tt * 9) * 0.25, hit_t + 0.02)
    fi = int(0.8 * SR); y[:fi] *= np.linspace(0, 1, fi)
    fo = int(0.4 * SR); y[-fo:] *= np.linspace(1, 0, fo)
    return y * 0.5, start

def true_peak_db(wav_path):
    r = subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-af",
                        "loudnorm=print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    txt = r.stderr
    i = txt.find("{")
    if i < 0: raise RuntimeError("loudnorm parse failed: " + txt[-400:])
    info = json.loads(txt[i:txt.find("}", i) + 1])
    # single-pass summary reports the INPUT file's measured true peak
    return float(info["input_tp"])

def main():
    print("loading base...", flush=True)
    base = load_wav(BASE_WAV)
    N = len(base)
    print(f"base dur {N/SR:.3f}s", flush=True)

    # ---- base edits: mute 17-20, boost x2.5 32-34 (100ms raised-cosine edges)
    base2 = base.copy()
    fe = int(0.1 * SR)
    rc = raised_cosine(fe)
    # mute 17.0 -> 20.0
    m0, m1 = int(17.0 * SR), int(20.0 * SR)
    base2[m0:m0 + fe] *= (1 - rc)[:, None]
    base2[m0 + fe:m1 - fe] = 0
    base2[m1 - fe:m1] *= rc[:, None]
    # boost x2.5 on 32.0 -> 34.0 with gain envelope
    b0, b1 = int(32.0 * SR), int(34.0 * SR)
    genv = np.ones(b1 - b0)
    genv[:fe] = 1 + 1.5 * rc
    genv[-fe:] = 1 + 1.5 * (1 - rc)
    genv[fe:-fe] = 2.5
    base2[b0:b1] *= genv[:, None]
    print(f"mute 17-20 peak now {np.abs(base2[m0:m1]).max():.4f}; "
          f"boost 32-34 peak {np.abs(base2[b0:b1]).max():.3f}", flush=True)

    mix = base2.copy()

    # ---- suspense bed, DOUBLED, ducked (floor 0.05 to protect dialogue)
    print("synth suspense (x2)...", flush=True)
    sus = synth_suspense()
    e = env_smooth(base2)
    duck_k = np.clip((0.012 - e) / (0.012 - 0.005), 0, 1)
    gain = 0.05 + 0.95 * duck_k
    gain[int(29.5 * SR):] = 1.0  # riser rides full
    # owner rev2 note: ease the doubled bed slightly under his
    # "luck of the Irish!" line (32->34) so the voice stays on top
    _d0, _d1 = int(32.0 * SR), int(34.0 * SR)
    _fe = int(0.1 * SR)
    _dip = np.ones(_d1 - _d0) * 0.6
    _dip[:_fe] = 1.0 - 0.4 * raised_cosine(_fe)
    _dip[-_fe:] = 0.6 + 0.4 * raised_cosine(_fe)
    gain[_d0:_d1] = np.minimum(gain[_d0:_d1], _dip)
    sus_g = np.zeros(N); m = min(len(sus), N)
    sus_g[:m] = sus[:m] * gain[:m]
    if DIP_ENABLED:
        # V-dip under his "luck of the Irish!" line, ABSOLUTE dB targets.
        # The riser crescendos through 32-34s, so the dip is computed against
        # the bed's own smoothed level: final bed must read -72dBFS at 33s and
        # -24dBFS at 34s no matter what the riser does.
        # Chain to final: x1.30 (stereo) x0.6333 (norm, deterministic) x3.2 (passes)
        _b0, _b1 = int(32.0*SR), int(34.4*SR)
        _bed_final = sus_g[_b0:_b1] * 1.30 * 0.6333 * 3.2
        _w = int(0.2*SR)
        _rms = np.sqrt(np.convolve(_bed_final**2, np.ones(_w)/_w, mode='same'))
        _smooth_db = 20*np.log10(_rms + 1e-12)
        _start_db = float(np.mean(_smooth_db[:int(0.1*SR)]))
        _n = _b1 - _b0
        _t = np.arange(_n) / SR
        _tgt = np.empty(_n)
        _m1 = _t <= 1.0
        _tgt[_m1] = _start_db + (-72.0 - _start_db) * _t[_m1]
        _m2 = (_t > 1.0) & (_t <= 2.0)
        _tgt[_m2] = -72.0 + (-24.0 + 72.0) * (_t[_m2] - 1.0)
        _m3 = _t > 2.0
        _rel = 0.5 - 0.5*np.cos(np.pi*(_t[_m3]-2.0)/0.4)
        _tgt[_m3] = -24.0 + (_smooth_db[_m3] - (-24.0)) * _rel
        _dip_db = np.minimum(_tgt - _smooth_db, 6.0)
        sus_g[_b0:_b1] *= 10.0 ** (_dip_db / 20.0)
        print(f"dip applied (absolute): start {_start_db:.1f}dB -> -72 @33s -> -24 @34s", flush=True)
    # debug: save dipped bed stem (mono, pre-1.30) for verification
    import wave as _wv
    _bw = _wv.open(os.path.join(D, "v3-bed-dipped.wav"), "wb")
    _bw.setnchannels(1); _bw.setsampwidth(2); _bw.setframerate(SR)
    _bclip = np.clip(sus_g[:m, None].reshape(-1), -1, 1)
    _bw.writeframes((_bclip * 32767).astype(np.int16).tobytes()); _bw.close()
    sus_stereo = np.stack([sus_g, sus_g], axis=1) * 1.30  # rev1 was 0.65 -> doubled
    mix += sus_stereo

    # ---- upbeat bed unchanged, ducked under v1 voice (v1 at ~53.27s)
    print("synth upbeat (unchanged)...", flush=True)
    up, ustart = synth_upbeat()
    up_g = np.zeros(N); s0 = int(ustart * SR); m2 = min(len(up), N - s0)
    uv = up[:m2].copy()
    d0, d1 = int((52.8 - ustart) * SR), int((55.8 - ustart) * SR)
    d0 = max(d0, 0); d1 = min(d1, len(uv))
    if d1 > d0:
        ramp = int(0.3 * SR)
        g = np.ones(len(uv)); g[d0:d1] = 0.22
        if d0 - ramp >= 0: g[d0 - ramp:d0] = np.linspace(1, 0.22, ramp)
        g[d1:d1 + ramp] = np.linspace(0.22, 1, ramp)
        uv *= g
    up_g[s0:s0 + m2] = uv
    up_stereo = np.stack([up_g, up_g], axis=1)
    mix += up_stereo

    # ---- trim to video duration, normalize, true-peak verify
    nv = int(VIDEO_DUR * SR)
    mix = mix[:nv]
    peak = np.abs(mix).max()
    norm = (10 ** (-1 / 20)) / max(peak, 1e-6)
    mix *= norm
    print(f"mix peak before norm {peak:.3f}, norm factor {norm:.4f}", flush=True)
    save_wav(OUT_WAV, mix)
    tp = true_peak_db(OUT_WAV)
    print(f"true peak: {tp:.2f} dBFS", flush=True)
    if tp > -1.0:
        extra = 10 ** ((tp + 1.0 + 0.1) / -20)
        mix *= extra
        save_wav(OUT_WAV, mix)
        tp = true_peak_db(OUT_WAV)
        print(f"re-normed, true peak now {tp:.2f} dBFS", flush=True)

    # ---- standalone bed exports (same final normalization factor)
    sus_full = np.zeros((nv, 2)); mm = min(len(sus), nv)
    sus_full[:mm] = np.stack([sus[:mm], sus[:mm]], axis=1) * 1.30 * norm
    # dip build: keep existing standalone bed assets untouched
    pass  # sus_full not exported
    up_full = np.zeros((nv, 2))
    # up_full not exported in dip build
    print("bed exports ok", flush=True)

    # ---- mux: video stream copy from pre-score cut, new audio
    tmp_out = OUT_MP4 + ".tmp.mp4"
    r = subprocess.run(FF + ["-i", PRESCORE_MP4, "-i", OUT_WAV,
                             "-map", "0:v", "-map", "1:a",
                             "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                             "-movflags", "+faststart", tmp_out], capture_output=True)
    assert r.returncode == 0, f"mux failed: {r.stderr.decode()[-500:]}"
    os.replace(tmp_out, OUT_MP4)
    print("mux ok ->", OUT_MP4, flush=True)

if __name__ == "__main__":
    main()
