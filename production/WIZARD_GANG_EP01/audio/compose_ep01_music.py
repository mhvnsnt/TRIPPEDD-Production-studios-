#!/usr/bin/env python3
"""WIZARD GANG Ep1 'THE SUMMIT' — per-scene background music stems.
100% original code synthesis (numpy). No samples, no third-party loops.
All melodies/motifs composed for this episode. Target: beds under dialogue.
Scored block: 0:50-5:00 (S10-S29). Full mix ~= 250s incl. Act-2 smash transitions.
"""
import numpy as np, wave, os, math

SR = 44100
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- core ----------
def n2f(m):  # midi -> hz
    return 440.0 * 2.0 ** ((m - 69) / 12.0)

def T(dur):
    return np.arange(int(round(dur * SR)), dtype=np.float64) / SR

def adsr_env(n, a, d, s, r, sustain_level=0.6):
    a_n, d_n, r_n = int(a*SR), int(d*SR), int(r*SR)
    s_n = max(0, n - a_n - d_n - r_n)
    env = np.zeros(n)
    if a_n: env[:a_n] = np.linspace(0, 1, a_n)
    if d_n: env[a_n:a_n+d_n] = np.linspace(1, sustain_level, d_n)
    if s_n: env[a_n+d_n:a_n+d_n+s_n] = sustain_level
    if r_n: env[n-r_n:] = np.linspace(sustain_level if s_n or d_n else 1, 0, r_n)
    return env

def exp_env(n, tau):
    t = np.arange(n) / SR
    return np.exp(-t / tau)

def sine(f, dur, phase=0.0):
    t = T(dur)
    if np.isscalar(f):
        return np.sin(2*np.pi*f*t + phase)
    return np.sin(2*np.pi*np.asarray(f)*t + phase)

def tri(f, dur):
    return 2*np.abs(2*((T(dur)*f) % 1.0) - 1) - 1

def sqr(f, dur, duty=0.5):
    return np.where((T(dur)*f) % 1.0 < duty, 1.0, -1.0)

def saw(f, dur):
    return 2*((T(dur)*f) % 1.0) - 1

def noise(dur, seed=None):
    rng = np.random.default_rng(seed)
    return rng.standard_normal(int(round(dur*SR)))

def fft_lowpass(x, fc):
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1/SR)
    X = X / (1.0 + (f/max(fc,1))**2)
    return np.fft.irfft(X, n)

def fft_highpass(x, fc):
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1/SR)
    X = X * (f**2/(f**2+max(fc,1)**2))
    return np.fft.irfft(X, n)

def stereo(mono, width=0.0, seed=7):
    m = np.asarray(mono, dtype=np.float64)
    if width <= 0:
        return np.stack([m, m], axis=1)
    n = noise(len(m)/SR, seed=seed) * 0.0  # placeholder-free width via delay
    d = int(0.012*SR)
    side = np.zeros_like(m); side[d:] = (m[:-d]-m[d:])*0.0
    # simple width: slightly decorrelated copy via tiny delay
    r = np.zeros_like(m); r[d:] = m[:-d]
    l = m.copy()
    return np.stack([l*(1-width/2)+r*(width/2), r*(1-width/2)+l*(width/2)], axis=1)

def place(base, sig, at):
    """Add mono/stereo sig into stereo base at time `at` (seconds)."""
    s = np.asarray(sig, dtype=np.float64)
    if s.ndim == 1: s = np.stack([s, s], axis=1)
    i = int(round(at*SR))
    j = min(len(base), i+len(s))
    if i < len(base) and j > i:
        base[i:j] += s[:j-i]
    return base

def finish(x, peak=0.5):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1: x = np.stack([x, x], axis=1)
    x = np.tanh(x*0.9)/np.tanh(0.9) * 0.98  # gentle soft-clip
    p = np.max(np.abs(x))
    if p > 1e-9:
        x = x / p * peak
    return x.astype(np.float32)

def bed(dur):
    return np.zeros((int(round(dur*SR)), 2), dtype=np.float64)

# ---------- drums ----------
def kick(dur=0.4, f0=150, f1=44):
    n = int(round(dur*SR)); t = np.arange(n)/SR
    f = f1 + (f0-f1)*np.exp(-t/0.03)
    ph = np.cumsum(2*np.pi*f/SR)
    return np.sin(ph) * exp_env(n, 0.09)

def sub_hit(dur=1.6, f=52):
    n = int(round(dur*SR))
    return (sine(f, dur) * exp_env(n, 0.5)).astype(np.float64)

def tom(f0, dur=0.45):
    n = int(round(dur*SR)); t = np.arange(n)/SR
    f = f0*0.55 + f0*0.45*np.exp(-t/0.06)
    ph = np.cumsum(2*np.pi*f/SR)
    return np.sin(ph)*exp_env(n, 0.16)

def snare(dur=0.22):
    n = int(round(dur*SR))
    nz = fft_highpass(noise(dur, seed=11), 1200)*exp_env(n, 0.045)
    tone = sine(190, dur)*exp_env(n, 0.05)
    return 0.6*nz + 0.5*tone

def rim(dur=0.08):
    n = int(round(dur*SR))
    return (sine(1720, dur)+0.5*sine(860, dur))*exp_env(n, 0.012)*0.5

def hat(dur=0.05, open_=False):
    d = 0.28 if open_ else dur
    n = int(d*SR)
    return fft_highpass(noise(d, seed=23), 7000)*exp_env(n, 0.02 if not open_ else 0.09)*0.5

def shaker(dur=0.09):
    n = int(round(dur*SR))
    return fft_highpass(noise(dur, seed=31), 5000)*exp_env(n, 0.03)*0.4

def clap(dur=0.25):
    n = int(round(dur*SR))
    x = np.zeros(n)
    for k, g in enumerate([0.0, 0.018, 0.036]):
        i = int(g*SR); m = min(n-i, int(0.05*SR))
        x[i:i+m] += fft_highpass(noise(0.05, seed=40+k), 1500)[:m]*exp_env(m, 0.015)
    return x*0.5

def crash(dur=1.6):
    n = int(round(dur*SR))
    return fft_highpass(noise(dur, seed=55), 4000)*exp_env(n, 0.5)*0.45

def riser(dur, f0=200, f1=4000):
    n = int(round(dur*SR)); t = np.arange(n)/SR
    nz = fft_highpass(noise(dur, seed=61), 800)
    amp = (t/dur)**2
    sw = sine(f0+(f1-f0)*(t/dur)**1.5, dur)*0.15
    return (nz*0.5+sw)*amp

def whoosh_hit(dur=0.42):
    """Smash-cut transition bed for Act 2."""
    n = int(round(dur*SR))
    r = riser(dur*0.55)*0.8
    out = np.zeros(n)
    out[:len(r)] += r
    k = kick(0.3); out[int(0.55*dur*SR):int(0.55*dur*SR)+len(k)] += k[:max(0, n-int(0.55*dur*SR))]
    return out*0.7

# ---------- pitched instruments (all original voicings) ----------
def bass_note(m, dur, bright=0.25):
    n = int(round(dur*SR))
    f = n2f(m)
    x = sine(f, dur) + bright*sine(2*f, dur)*0.5 + bright*0.3*tri(f, dur)
    return x * np.minimum(1, exp_env(n, dur*0.45) + 0.25)

def ep_chord(midis, dur, seed=3):
    n = int(round(dur*SR))
    x = np.zeros(n)
    for m in midis:
        f = n2f(m)
        x += sine(f, dur)*exp_env(n, dur*0.6)*0.5 + sine(2*f, dur)*exp_env(n, dur*0.3)*0.12
    x += noise(dur, seed=seed)*0.004
    return x * adsr_env(n, 0.02, 0.1, 0.4, min(0.4, dur*0.3))

def pad(midis, dur, cutoff=900, det=4):
    n = int(round(dur*SR))
    x = np.zeros(n)
    for m in midis:
        f = n2f(m)
        x += saw(f, dur) + saw(f*(1+det/1200), dur)
    x = fft_lowpass(x, cutoff)*0.3
    return x * adsr_env(n, min(1.5, dur*0.3), 0.5, 0.5, min(2.0, dur*0.3))

def pluck_ks(m, dur, damp=0.996):
    """Karplus-Strong pluck. Original pitches only."""
    f = n2f(m); n = int(round(dur*SR)); N = max(2, int(SR/f))
    rng = np.random.default_rng(int(m*13+5))
    buf = rng.standard_normal(N)
    out = np.zeros(n); idx = 0
    prev = 0.0
    for i in range(n):
        v = buf[idx]
        out[i] = v
        nv = damp*0.5*(v + prev)
        prev = v; buf[idx] = nv
        idx = (idx+1) % N
    return out*0.8

def arp_note(m, dur, wave_='square'):
    n = int(round(dur*SR)); f = n2f(m)
    x = sqr(f, dur)*0.5 if wave_=='square' else tri(f, dur)*0.6
    return x*exp_env(n, dur*0.5)

def wind_bed(dur, seed=101, level=0.16):
    n = int(round(dur*SR))
    x = fft_lowpass(noise(dur, seed=seed), 400)
    lfo = 0.6+0.4*sine(0.07, dur)
    return x*lfo*level

def fire_crackle(dur, seed=202, density=26, level=0.5):
    rng = np.random.default_rng(seed)
    n = int(round(dur*SR)); x = np.zeros(n)
    for _ in range(int(density*dur)):
        i = rng.integers(0, n-200); m = rng.integers(40, 200)
        x[i:i+m] += fft_highpass(noise(m/SR, seed=rng.integers(9999)), 2500)[:m]*exp_env(m, 0.008)*rng.uniform(0.2,1.0)
    return x*level

def sizzle_bed(dur, seed=303, level=0.10):
    return fft_highpass(noise(dur, seed=seed), 6000)*level*(0.7+0.3*sine(0.4, dur))

def vinyl_crackle(dur, seed=404, level=0.05):
    return fire_crackle(dur, seed=seed, density=8, level=level)

def fog_horn(dur=3.0, f=58):
    n = int(round(dur*SR))
    x = sine(f, dur)+0.4*sine(f*1.5, dur)+0.25*sine(f*2.02, dur)
    return x*adsr_env(n, 0.8, 0.4, 0.4, 1.2)*0.5

def fireworks_pop(at_seed):
    n = int(0.5*SR)
    x = fft_highpass(noise(0.5, seed=at_seed), 2000)*exp_env(n, 0.06)
    x += sine(300, 0.5)*exp_env(n, 0.03)*0.3
    return x*0.6

def whistle_gliss(dur=0.5, f0=1800, f1=2600):
    n = int(round(dur*SR)); t = np.arange(n)/SR
    f = f0+(f1-f0)*(t/dur)
    ph = np.cumsum(2*np.pi*f/SR)
    return np.sin(ph)*adsr_env(n, 0.05, 0.05, 0.3, 0.1)*0.35

def feedback_squeal(dur=0.8):
    n = int(round(dur*SR)); t = np.arange(n)/SR
    f = 2350+180*np.sin(2*np.pi*9*t)
    ph = np.cumsum(2*np.pi*f/SR)
    return np.sin(ph)*adsr_env(n, 0.02, 0.05, 0.25, 0.15)*0.30

def flash_hit():
    n = int(0.6*SR)
    x = fft_highpass(noise(0.6, seed=707), 3000)*exp_env(n, 0.02)*0.5
    x += sub_hit(0.6, 48)
    return x

def save_wav(path, x):
    x = np.asarray(x, dtype=np.float32)
    if x.ndim == 1: x = np.stack([x, x], axis=1)
    x = np.clip(x, -1, 1)
    pcm = (x*32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return path

# ================= SCENES (all durations in seconds; times relative to 0:50) =================
def scene_s10():
    """THE SUMMONS 12s — sub-bass flare, wind, heartbeat drums, rising tom roll."""
    d = 12.0; x = bed(d)
    x = place(x, wind_bed(d, level=0.20), 0)
    x = place(x, sub_hit(2.2, 50), 0.0)
    x = place(x, riser(2.0)*0.6, 0.0)          # green flare whoosh
    t = 1.2
    while t < 4.0:                              # heartbeat pairs
        x = place(x, kick(0.4, 120, 42)*0.9, t); x = place(x, kick(0.4, 120, 42)*0.7, t+0.38)
        t += 1.6
    t = 4.2                                     # ritual toms enter
    while t < 7.6:
        x = place(x, tom(95)*0.8, t); t += 0.85
    t = 8.0                                     # rising 16th roll
    f = 80
    while t < 11.2:
        x = place(x, tom(f)*0.75, t); f += 6; t += 0.21
    x = place(x, sub_hit(1.8, 46)*1.1, 11.2)    # slam into S11
    x = place(x, crash(1.2)*0.5, 11.2)
    return finish(x, peak=0.55)

def scene_s11():
    """THE MEETING 16s — solemn taiko ritual; drums die at 13.5s (candle gutters)."""
    d = 16.0; x = bed(d)
    x = place(x, pad([38, 45, 50, 57], 14.5, cutoff=600)*0.9, 0)   # low D-minor drone
    x = place(x, wind_bed(d, seed=102, level=0.10), 0)
    bpm = 72.0; spb = 60.0/bpm
    t = 0.6
    k = 0
    while t < 13.2:                              # taiko pattern: DUN - - ka - DUN ka
        x = place(x, tom(78)*1.0, t)
        x = place(x, tom(120)*0.55, t+spb*1.5)
        x = place(x, tom(78)*0.9, t+spb*2.0)
        x = place(x, tom(150)*0.5, t+spb*2.75)
        t += spb*4; k += 1
    x = place(x, tom(70)*1.0, 13.0)              # final drum, then it dies
    x = place(x, fire_crackle(13.0, seed=203, density=6, level=0.10), 0)  # ritual candles
    # 13.5-16: drone thins, near-silence tail
    tail = bed(2.5); tail = place(tail, pad([38, 45], 2.5, cutoff=400)*0.5, 0)
    x = place(x, tail, 13.5)
    return finish(x, peak=0.5)

def scene_s12():
    """ORDER OF BUSINESS 20s — roll-call snare cadence + 8 solemn stabs."""
    d = 20.0; x = bed(d)
    bpm = 100.0; spb = 60.0/bpm
    t = 0.0
    while t < 19.0:                              # snare cadence
        for s in range(4):
            x = place(x, snare()* (0.9 if s == 0 else 0.55), t+s*spb)
        x = place(x, kick(0.3, 110, 50)*0.7, t)
        t += spb*4
    stabs = [[38,50,57,62],[36,48,55,60],[38,50,57,62],[34,46,53,58],
             [38,50,57,62],[36,48,55,62],[41,53,57,65],[38,50,57,62]]
    for i, ch in enumerate(stabs):                # 8 names land
        x = place(x, ep_chord(ch, 1.4)*0.85, 1.6+i*1.9)
    x = place(x, sub_hit(2.0, 44)*1.2, 15.8)     # Ashes DECLARES
    x = place(x, crash(1.4)*0.6, 15.8)
    # war-fund pooled: soft coin-ish shimmer (synth, original)
    for i in range(5):
        x = place(x, arp_note(88+i*3, 0.18)*0.4, 17.2+i*0.35)
    x = place(x, shaker(0.5)*0.8, 18.6)          # dice rattle hint -> S14
    x = place(x, shaker(0.5)*0.8, 18.9)
    return finish(x, peak=0.5)

def scene_s13():
    """THE DERAIL BEGINS 32s — solemn pad decays; warm cookout boombap takes over."""
    d = 32.0; x = bed(d)
    x = place(x, pad([38,45,50,57], 6.0, cutoff=700)*0.8, 0)   # solemnity fades
    x = place(x, sizzle_bed(28.0, level=0.10), 4.0)             # grill sizzle
    bpm = 90.0; spb = 60.0/bpm
    bassline = [38,38,41,38, 36,36,43,41, 38,38,41,45, 36,34,36,38]  # original
    chords = [[50,53,57,60],[46,50,53,57],[48,53,57,60],[50,53,57,62]]
    t = 4.0; bi = 0; ci = 0
    while t < 30.5:
        bar = spb*4
        x = place(x, kick(0.35)*0.85, t); x = place(x, kick(0.35)*0.7, t+spb*2.5)
        x = place(x, snare()*0.8, t+spb); x = place(x, snare()*0.8, t+spb*3)
        for s in range(8):
            x = place(x, hat(0.05)*(0.5 if s%2 else 0.35), t+s*spb/2)
        for s in range(4):
            x = place(x, bass_note(bassline[(bi+s)%len(bassline)], spb*0.9)*0.75, t+s*spb)
        if bi % 8 == 0:
            x = place(x, ep_chord(chords[ci % len(chords)], bar*0.95)*0.55, t); ci += 1
        bi += 4; t += bar
    # comedic bounce accent: little bass fill into Act 2
    x = place(x, bass_note(45, 0.25)*0.8, 30.6); x = place(x, bass_note(47, 0.25)*0.8, 30.85)
    x = place(x, bass_note(50, 0.4)*0.9, 31.1)
    return finish(x, peak=0.5)

def scene_s14():
    """DICE GAME 10s — tense swingy groove; dice shaker rolls at the end."""
    d = 10.0; x = bed(d)
    bpm = 96.0; spb = 60.0/bpm
    riff = [38,38,41,38, 39,38,36,38]            # original tense riff
    t = 0.0; i = 0
    while t < 9.0:
        x = place(x, kick(0.3)*0.8, t); x = place(x, rim()*0.8, t+spb*0.66)
        x = place(x, snare()*0.7, t+spb*1.33)
        for s in range(3):
            x = place(x, hat(0.05)*0.45, t+s*spb*0.66)
        x = place(x, bass_note(riff[i % len(riff)], spb*0.6)*0.8, t)
        i += 1; t += spb*2
    for k in range(6):                            # dice roll
        x = place(x, shaker(0.12)*0.9, 7.6+k*0.28)
    x = place(x, rim()*1.0, 9.3)                  # aces land — map gone
    x = place(x, sub_hit(0.9, 55)*0.8, 9.3)
    return finish(x, peak=0.5)

def scene_s15():
    """ARCADE 10s — original chiptune bounce; Echo copies the claw."""
    d = 10.0; x = bed(d)
    bpm = 128.0; spb = 60.0/bpm
    # original 8-bar square arp melody (D minor pentatonic, own contour)
    mel = [62,65,69,65, 62,60,62,65, 69,72,69,65, 67,65,62,60]
    t = 0.0; mi = 0
    while t < 9.6:
        for s in range(4):
            x = place(x, arp_note(mel[(mi+s) % len(mel)], spb*0.45)*0.55, t+s*spb/2)
        x = place(x, kick(0.25, 160, 60)*0.7, t)
        x = place(x, snare()*0.5, t+spb)
        for s in range(4):
            x = place(x, hat(0.04)*0.4, t+s*spb/2)
        mi += 4; t += spb*2
    # claw-machine servo blips (original intervals) + plushie win sparkle
    for k, m in enumerate([76, 79, 76, 74]):
        x = place(x, arp_note(m, 0.12)*0.5, 3.9+k*0.3)
    for k, m in enumerate([72, 76, 79, 84]):
        x = place(x, arp_note(m, 0.15)*0.55, 8.2+k*0.16)
    return finish(x, peak=0.45)

def scene_s16():
    """BASKETBALL 9s — 90s hoop bounce; synth whistle accents."""
    d = 9.0; x = bed(d)
    bpm = 92.0; spb = 60.0/bpm
    bassline = [36,36,39,41, 36,34,36,39]        # original
    t = 0.0; i = 0
    while t < 8.4:
        x = place(x, kick(0.32)*0.95, t); x = place(x, kick(0.32)*0.75, t+spb*1.75)
        x = place(x, snare()*0.9, t+spb); x = place(x, snare()*0.9, t+spb*3)
        for s in range(8):
            x = place(x, hat(0.05)*(0.55 if s % 2 else 0.4), t+s*spb/2)
        x = place(x, bass_note(bassline[i % len(bassline)], spb*0.8)*0.85, t+i*0)
        for s in range(2):
            x = place(x, bass_note(bassline[(i+s) % len(bassline)], spb*0.45)*0.8, t+s*spb*2)
        i += 2; t += spb*4
    x = place(x, whistle_gliss(0.45, 1700, 2500)*0.8, 2.0)
    x = place(x, whistle_gliss(0.45, 1700, 2500)*0.8, 6.2)
    # ball-bounce thumps
    for k in range(4):
        x = place(x, tom(110)*0.4, 0.9+k*1.9)
    return finish(x, peak=0.5)

def scene_s17():
    """BODEGA 9s — lo-fi stroll; Static won't stop talking to the owner."""
    d = 9.0; x = bed(d)
    bpm = 84.0; spb = 60.0/bpm
    x = place(x, vinyl_crackle(d, level=0.06), 0)
    chords = [[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,60]]  # original lo-fi loop
    t = 0.0; ci = 0
    while t < 8.6:
        bar = spb*4
        x = place(x, kick(0.3, 100, 45)*0.7, t)
        x = place(x, snare()*0.55, t+spb*2)
        for s in range(8):
            x = place(x, hat(0.05)*0.3, t+s*spb/2)
        x = place(x, ep_chord(chords[ci % len(chords)], bar*0.9)*0.5, t)
        x = place(x, bass_note([41,40,38,36][ci % 4], bar*0.5)*0.7, t)
        ci += 1; t += bar
    return finish(x, peak=0.45)

def scene_s18():
    """NIGHT MARKET 10s — sway groove; ominous pulse when IT SEES glows."""
    d = 10.0; x = bed(d)
    bpm = 80.0; spb = 60.0/bpm
    t = 0.0; i = 0
    bassline = [38,41,43,41, 38,36,38,41]
    while t < 9.4:
        x = place(x, tom(95)*0.7, t); x = place(x, tom(125)*0.6, t+spb*0.75)
        x = place(x, shaker(0.09)*0.6, t+spb*0.5); x = place(x, shaker(0.09)*0.6, t+spb*1.5)
        x = place(x, bass_note(bassline[i % len(bassline)], spb*0.8)*0.75, t)
        i += 1; t += spb*2
    # IT SEES tag glow ~6.5s: low ominous pulse + detuned shimmer
    x = place(x, sub_hit(2.4, 41)*0.9, 6.4)
    x = place(x, sine(110*1.007, 2.0)*exp_env(int(2.0*SR), 0.8)*0.12, 6.4)
    x = place(x, ep_chord([45,51,56], 2.2)*0.4, 6.4)
    return finish(x, peak=0.5)

def scene_s19():
    """SUBWAY 9s — train-chug rhythm; 'tactical movement' field trip."""
    d = 9.0; x = bed(d)
    bpm = 100.0; spb = 60.0/bpm
    t = 0.0; i = 0
    bassline = [36,36,36,39, 36,36,41,39]        # original driving line
    while t < 8.6:
        for s in range(4):                        # chugga-chugga
            x = place(x, fft_highpass(noise(0.09, seed=500+i*4+s), 900)*exp_env(int(0.09*SR), 0.02)*0.35, t+s*spb/2)
        x = place(x, kick(0.28)*0.75, t)
        x = place(x, snare()*0.6, t+spb)
        x = place(x, bass_note(bassline[i % len(bassline)], spb*0.45)*0.8, t)
        x = place(x, bass_note(bassline[(i+4) % len(bassline)], spb*0.45)*0.8, t+spb)
        i += 1; t += spb*2
    # rail clack accents
    for k in range(3):
        x = place(x, rim()*0.7, 1.4+k*2.4)
    return finish(x, peak=0.5)

def scene_s20():
    """BRIDGE 8s — 'classified exchange': tense low pizz groove (mozzarella sticks)."""
    d = 8.0; x = bed(d)
    bpm = 70.0; spb = 60.0/bpm
    line = [33,None,36,None, 31,None,33,34]      # original sparse line
    t = 0.0; i = 0
    while t < 7.6:
        m = line[i % len(line)]
        if m:
            x = place(x, pluck_ks(m, spb*1.2)*0.55, t)
        if i % 4 == 0:
            x = place(x, tom(70)*0.8, t)
        if i % 8 == 6:
            x = place(x, hat(0.05)*0.35, t)
        i += 1; t += spb
    x = place(x, pad([33,40,45], 7.5, cutoff=500)*0.7, 0)
    return finish(x, peak=0.45)

def scene_s21():
    """PARKING GARAGE 8s — 'secure location': minimal spy-ish pulse."""
    d = 8.0; x = bed(d)
    bpm = 66.0; spb = 60.0/bpm
    t = 0.0; i = 0
    while t < 7.6:
        x = place(x, kick(0.3, 90, 40)*0.55, t)          # muted pulse
        if i % 2 == 1:
            x = place(x, pluck_ks([45,43,41,40][i % 4], spb*1.5)*0.4, t+spb*0.5)
        if i % 4 == 3:
            x = place(x, shaker(0.08)*0.3, t)
        i += 1; t += spb*2
    x = place(x, pad([36,43,48], 7.8, cutoff=450)*0.6, 0)
    return finish(x, peak=0.42)

def scene_s22():
    """SKATE PARK 9s — pop-punk-ish bounce; Cipher eats concrete at ~7s."""
    d = 9.0; x = bed(d)
    bpm = 140.0; spb = 60.0/bpm
    riff = [40,40,43,45, 47,45,43,40]            # original power-chord-ish riff
    t = 0.0; i = 0
    while t < 6.8:
        for s in range(2):
            m = riff[(i+s) % len(riff)]
            n = int(spb*0.5*SR)
            ch = (saw(n2f(m), spb*0.5)+saw(n2f(m+7), spb*0.5))*0.25
            ch = fft_lowpass(ch, 2400)
            x = place(x, ch*exp_env(n, 0.08), t+s*spb*0.5)
        x = place(x, kick(0.28)*0.85, t); x = place(x, snare()*0.85, t+spb*0.5)
        x = place(x, snare()*0.85, t+spb*1.5)
        for s in range(4):
            x = place(x, hat(0.04)*0.5, t+s*spb/2)
        i += 2; t += spb*2
    x = place(x, crash(1.8)*0.9, 6.9)            # the trick fails
    x = place(x, sub_hit(1.2, 50)*0.9, 6.9)
    # 1s of silence, then one comedic low 'womp'
    x = place(x, bass_note(31, 0.8)*0.9, 8.0)
    return finish(x, peak=0.52)

def scene_s23():
    """STUDIO 9s — podcast 'war room' bounce; Static hijacks the mic ~7s."""
    d = 9.0; x = bed(d)
    bpm = 100.0; spb = 60.0/bpm
    t = 0.0; i = 0
    bassline = [41,41,44,41, 39,39,41,44]
    while t < 8.6:
        x = place(x, kick(0.3)*0.8, t); x = place(x, clap()*0.6, t+spb)
        x = place(x, clap()*0.6, t+spb*3)
        for s in range(8):
            x = place(x, hat(0.05)*0.4, t+s*spb/2)
        x = place(x, bass_note(bassline[i % len(bassline)], spb*0.7)*0.8, t)
        x = place(x, ep_chord([53,57,60], spb*1.8)*0.45, t+spb*2)
        i += 1; t += spb*4
    x = place(x, feedback_squeal(0.9)*1.0, 6.9)  # mic hijack squeal
    x = place(x, kick(0.3)*0.8, 8.0)             # groove sheepishly resumes
    x = place(x, bass_note(41, 0.4)*0.7, 8.0)
    return finish(x, peak=0.5)

def scene_s24():
    """CARNIVAL 10s — dark calliope waltz (original); hard stop for Sombra's stone face."""
    d = 10.0; x = bed(d)
    bpm = 100.0; spb = 60.0/bpm                  # beat; waltz bars of 3
    # original A-minor waltz melody
    mel = [69,72,76, 74,72,69, 67,69,72, 69,67,64, 69,72,76, 79,76,74, 72,74,69, 67,0,0]
    bass = [45,52,57]
    t = 0.0; mi = 0; bar = 0
    while t < 8.2:
        for b in range(3):
            x = place(x, bass_note(bass[b % 3]-12, spb*0.9)*0.55, t+b*spb)
        for b in range(3):
            m = mel[(mi+b) % len(mel)]
            if m:
                x = place(x, (sqr(n2f(m), spb*0.85)*0.28+sqr(n2f(m)*2, spb*0.85)*0.10)*exp_env(int(spb*0.85*SR), 0.2), t+b*spb)
        mi += 3; bar += 1; t += spb*3
    # 8.3s: music stops DEAD — Sombra holds the plushie, stone-faced
    return finish(x, peak=0.45)

def scene_s25():
    """THE GRILL INCIDENT 6s — fire riser, big hit, then casual cover-up."""
    d = 6.0; x = bed(d)
    x = place(x, fire_crackle(2.2, seed=206, density=60, level=0.7), 0)
    x = place(x, riser(2.0, 300, 5000)*0.9, 0.2)
    x = place(x, sub_hit(1.4, 46)*1.2, 2.1)      # flare!
    x = place(x, crash(1.4)*0.8, 2.1)
    # 2.6-6: "everything's fine" — breezy plucks, burgers fine
    t = 2.7
    while t < 5.7:
        x = place(x, pluck_ks([57,60,64,62][int(t*2) % 4], 0.5)*0.45, t)
        x = place(x, shaker(0.08)*0.4, t+0.25)
        t += 0.5
    x = place(x, sizzle_bed(3.0, seed=304, level=0.08), 2.7)
    return finish(x, peak=0.55)

def scene_s26():
    """THE PIER 8s — Kiko alone: sparse plucks, fog horn, fog bed."""
    d = 8.0; x = bed(d)
    x = place(x, wind_bed(d, seed=103, level=0.22), 0)     # fog
    x = place(x, fog_horn(3.2, 55)*0.9, 0.6)
    x = place(x, fog_horn(3.4, 49)*0.8, 4.4)
    # original lonely motif (theatrical, unbothered)
    for at, m in [(1.2,69),(2.1,67),(3.0,64),(4.9,69),(5.8,72),(6.7,67)]:
        x = place(x, pluck_ks(m, 1.6)*0.55, at)
    x = place(x, pad([45,52,57,64], 7.6, cutoff=700)*0.55, 0.2)
    return finish(x, peak=0.45)

def scene_s27():
    """THE ADJOURNMENT 25s — warm night groove, fireworks, embers."""
    d = 25.0; x = bed(d)
    bpm = 76.0; spb = 60.0/bpm
    x = place(x, fire_crackle(d, seed=207, density=10, level=0.14), 0)  # embers
    chords = [[48,55,60,64],[46,53,58,62],[45,52,57,60],[43,50,55,59]]  # original warm loop
    bassline = [36,38,41,38]
    t = 0.0; ci = 0
    while t < 20.0:
        bar = spb*4
        x = place(x, kick(0.32, 110, 45)*0.7, t)
        x = place(x, snare()*0.5, t+spb*2)
        for s in range(8):
            x = place(x, hat(0.05)*0.28, t+s*spb/2)
        x = place(x, bass_note(bassline[ci % len(bassline)], bar*0.6)*0.7, t)
        x = place(x, ep_chord(chords[ci % len(chords)], bar*0.95)*0.5, t)
        ci += 1; t += bar
    for i, at in enumerate([2.0, 6.0, 9.0, 13.0, 17.0, 21.0]):  # fireworks bloom
        x = place(x, fireworks_pop(800+i)*0.9, at)
        x = place(x, sub_hit(1.0, 50)*0.4, at)
    # last 5s: groove thins to pad + embers
    x = place(x, pad([48,55,60], 5.0, cutoff=800)*0.6, 20.0)
    return finish(x, peak=0.5)

def scene_s28():
    """THE PHOTO / BUTTON 20s — warm swell, flash at ~16.5s, 2s freeze, quiet."""
    d = 20.0; x = bed(d)
    x = place(x, pad([48,55,60,64,67], 17.0, cutoff=1100)*0.8, 0)   # warm swell
    # gentle original motif: 'nothing was resolved'
    for at, m in [(2.0,64),(4.5,62),(7.0,60),(9.5,62),(12.0,64),(14.0,67)]:
        x = place(x, pluck_ks(m, 1.8)*0.4, at)
    x = place(x, flash_hit()*1.0, 16.4)            # firework flash = camera flash
    x = place(x, pad([48,55,60,64], 2.2, cutoff=900)*0.9, 16.5)     # freeze holds 2s
    # 18.7-20: fade to near silence
    return finish(x, peak=0.5)

def scene_s29():
    """IDENT 5s — logo sting: sub hit + shimmer + trippy wobble."""
    d = 5.0; x = bed(d)
    x = place(x, sub_hit(2.0, 46)*1.1, 0.0)
    x = place(x, crash(1.6)*0.5, 0.0)
    n = int(3.0*SR); t = np.arange(n)/SR          # shimmer cluster gliss
    f = 1200+2400*(t/3.0)
    ph = np.cumsum(2*np.pi*f/SR)
    x = place(x, np.sin(ph)*exp_env(n, 0.9)*0.18, 0.4)
    n2 = int(2.5*SR); t2 = np.arange(n2)/SR       # trippy wobble under TRIPPEDD card
    wob = np.sin(2*np.pi*(110+18*np.sin(2*np.pi*5*t2))*t2)*exp_env(n2, 1.1)*0.35
    x = place(x, wob, 2.4)
    return finish(x, peak=0.55)

SCENES = [
    ("s10_the_summons", 12.0, scene_s10, "0:50-1:02", "Summons tension: sub-bass flare, wind, heartbeat drums, rising tom roll into the meeting."),
    ("s11_the_meeting", 16.0, scene_s11, "1:02-1:18", "Solemn ritual taiko under the opening; drums die at 13.5s when the candle gutters out."),
    ("s12_order_of_business", 20.0, scene_s12, "1:18-1:38", "Roll-call snare cadence; 8 solemn stabs for 8 names; Ashes' declaration hit; dice-rattle hint."),
    ("s13_the_derail_begins", 32.0, scene_s13, "1:38-2:10", "Solemn pad decays into a warm 90bpm cookout boombap; grill sizzle; comedic bass fill into Act 2."),
    ("s14_dice_game", 10.0, scene_s14, "2:10-2:20", "Tense swingy groove; dice shaker roll; rimshot when Cipher rolls aces — the map is gone."),
    ("s15_arcade", 10.0, scene_s15, "2:20-2:30", "Original chiptune bounce; claw-servo blips; plushie-win sparkle."),
    ("s16_basketball", 9.0, scene_s16, "2:30-2:39", "90s hoop bounce; synth whistle accents; ball-bounce thumps."),
    ("s17_bodega", 9.0, scene_s17, "2:39-2:48", "Lo-fi stroll with vinyl crackle; the war fund buys chips."),
    ("s18_night_market", 10.0, scene_s18, "2:48-2:58", "Sway groove; ominous low pulse when the IT SEES tag glows."),
    ("s19_subway", 9.0, scene_s19, "2:58-3:07", "Train-chug rhythm; driving bass; 'tactical movement' field trip."),
    ("s20_bridge", 8.0, scene_s20, "3:07-3:15", "Tense sparse pizz groove; the 'classified exchange' is mozzarella sticks."),
    ("s21_parking_garage", 8.0, scene_s21, "3:15-3:23", "Minimal spy-ish pulse; folding chairs; total secrecy."),
    ("s22_skate_park", 9.0, scene_s22, "3:23-3:32", "Pop-punk-ish bounce; crash at the failed trick; one comedic low 'womp'."),
    ("s23_studio", 9.0, scene_s23, "3:32-3:41", "Talk-show bounce; mic-feedback squeal when Static hijacks the mic."),
    ("s24_carnival", 10.0, scene_s24, "3:41-3:51", "Dark original calliope waltz; music stops DEAD for Sombra's stone face."),
    ("s25_grill_incident", 6.0, scene_s25, "3:51-3:57", "Fire riser + flare hit; hard cut to casual 'everything's fine' plucks."),
    ("s26_the_pier", 8.0, scene_s26, "3:57-4:05", "Kiko alone: fog bed, fog horns, sparse theatrical plucks."),
    ("s27_the_adjunction", 25.0, scene_s27, "4:10-4:35", "Warm 76bpm night groove; fireworks blooms; ember bed; groove thins at the end."),
    ("s28_the_photo_button", 20.0, scene_s28, "4:35-4:55", "Warm swell + 'nothing was resolved' motif; flash at 16.5s; 2s freeze; quiet."),
    ("s29_ident", 5.0, scene_s29, "4:55-5:00", "Logo sting: sub hit, shimmer gliss, trippy wobble under the TRIPPEDD card."),
]

def main():
    stems = []
    for name, dur, fn, tc, desc in SCENES:
        print(f"composing {name} ({dur}s) ...", flush=True)
        x = fn()
        assert abs(len(x)/SR - dur) < 0.05, f"{name}: duration drift {len(x)/SR}"
        path = os.path.join(OUT, name + ".wav")
        save_wav(path, x)
        stems.append((name, dur, tc, desc, x))
        print(f"  wrote {path}", flush=True)
    # full show mix: stems in order; 0.42s smash transitions between Act-2 beats (S14..S26)
    mix = bed(0.1)
    trans = whoosh_hit(0.42)
    act2_names = [s[0] for s in stems[4:17]]  # s14..s26 = 13 beats
    for i, (name, dur, tc, desc, x) in enumerate(stems):
        mix = np.concatenate([mix, x]) if len(mix) > 1 else x.copy()
        if name in act2_names and name != act2_names[-1]:
            mix = np.concatenate([mix, np.stack([trans, trans], axis=1).astype(np.float64)])
    mix = finish(mix, peak=0.55)
    mp = os.path.join(OUT, "ep01_full_mix_0050-0500.wav")
    save_wav(mp, mix)
    print(f"full mix: {len(mix)/SR:.2f}s -> {mp}")
    # report line for manifest
    with open(os.path.join(OUT, "_stem_report.txt"), "w") as f:
        for name, dur, tc, desc, x in stems:
            peak = float(np.max(np.abs(x))); rms = float(np.sqrt(np.mean(x.astype(np.float64)**2)))
            f.write(f"{name}.wav | {dur:.1f}s | {tc} | peak {peak:.3f} | rms {rms:.4f} | {desc}\n")
        f.write(f"ep01_full_mix_0050-0500.wav | {len(mix)/SR:.2f}s | 0:50-5:00 | full show mix\n")

if __name__ == "__main__":
    main()
