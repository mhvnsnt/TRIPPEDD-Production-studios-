#!/usr/bin/env python3
"""Kiko pier song v2 — ADDITIVE orchestration expansion.

RULES: existing piano/strings/choir pad (v1 WAV) are UNTOUCHED.
This script composes ONLY the new layers as MIDI, renders them with the
numpy GM synth (video-fix-tools/midi/render_midi.py), then mixes them
on top of v1 and appends the new ending (sustained Dm13 hold -> ABRUPT CUT).

Structure: D minor, 60 BPM. New layers 0:08-2:26. THE HOLD 2:26-2:32.
Cut dead at 2:32. 1s digital silence. Total ~2:33.
"""
import mido
import numpy as np
import subprocess
import wave
import os

AUDIO = os.path.expanduser("~/workspace/trippedd-studio/production/WIZARD_GANG_EP01/audio")
V1 = os.path.join(AUDIO, "kiko-pier-song-full-instrumental.wav")
V2 = os.path.join(AUDIO, "kiko-pier-song-full-instrumental-v2.wav")
TMP = "/tmp/kiko_v2"
os.makedirs(TMP, exist_ok=True)

SR = 44100
TPB = 480
def s2t(s):
    return int(round(s * 960))  # 120 BPM tempo map

# ---------------- chord data ----------------
# MIDI refs: D2=38 D3=50 D4=62 D5=74 D6=86 | A1=33 A2=45 A3=57 | G1=31 | Bb1=34 | F1=29
CHORDS = {
    "Dm":     {"bass": 38, "triad": [62, 65, 69], "e9": 64, "e11": 67, "e13": 71},
    "Bb":     {"bass": 34, "triad": [58, 62, 65], "e9": 60, "e11": 63, "e13": 67},
    "Gm":     {"bass": 31, "triad": [55, 58, 62], "e9": 57, "e11": 60, "e13": 64},
    "A":      {"bass": 33, "triad": [57, 61, 64], "e9": 59, "e11": 62, "e13": 66},
    "F":      {"bass": 29, "triad": [53, 57, 60], "e9": 55, "e11": 58, "e13": 62},
    "Bbmaj7": {"bass": 34, "triad": [58, 62, 65], "e9": 60, "e11": 63, "e13": 67},
    "Gm7":    {"bass": 31, "triad": [55, 58, 62], "e9": 57, "e11": 60, "e13": 64},
    "A7":     {"bass": 33, "triad": [57, 61, 64], "e9": 59, "e11": 62, "e13": 66},
}

REGIONS = [
    (8.0, 13.5, "Dm"), (13.5, 19.0, "Bb"), (19.0, 24.5, "Gm"), (24.5, 30.0, "A"),
    (30.0, 35.5, "Bb"), (35.5, 41.0, "Gm"), (41.0, 46.5, "A"), (46.5, 52.0, "A"),
    (52.0, 57.5, "Dm"), (57.5, 63.0, "Bb"), (63.0, 68.5, "F"), (68.5, 74.0, "A"),
    (74.0, 79.5, "Dm"), (79.5, 85.0, "Bbmaj7"), (85.0, 90.5, "Gm7"), (90.5, 96.0, "A7"),
    (96.0, 99.7, "Bb"), (99.7, 103.3, "Gm"), (103.3, 107.0, "Dm"),
    (107.0, 110.7, "Bb"), (110.7, 114.3, "F"), (114.3, 118.0, "A"),
    (118.0, 122.0, "Gm"), (122.0, 126.0, "Bb"), (126.0, 130.0, "A"),
    (130.0, 134.0, "Dm"), (134.0, 138.0, "Bb"), (138.0, 142.0, "F"), (142.0, 146.0, "A"),
]
BRIDGE = (118.0, 130.0)
HOLD_START, HOLD_END = 146.0, 152.0

def in_bridge(st):
    return BRIDGE[0] <= st < BRIDGE[1]

# ---------------- MIDI helpers ----------------
def new_mid():
    mid = mido.MidiFile(ticks_per_beat=TPB)
    t = mido.MidiTrack()
    t.append(mido.MetaMessage("set_tempo", tempo=500000, time=0))
    mid.tracks.append(t)
    return mid

def add_track(mid, program, channel, notes):
    """notes: list of (start_s, end_s, pitch, vel)"""
    tr = mido.MidiTrack()
    if channel != 9:
        tr.append(mido.Message("program_change", program=program, channel=channel, time=0))
    ev = []
    for st, en, p, v in notes:
        if en <= st:
            continue
        ev.append((s2t(st), 1, p, v))
        ev.append((s2t(en), 0, p, 0))
    ev.sort(key=lambda e: (e[0], -e[1]))
    last = 0
    for tick, typ, p, v in ev:
        dt = max(0, tick - last)
        last = tick
        if typ == 1:
            tr.append(mido.Message("note_on", note=p, velocity=min(127, v), channel=channel, time=dt))
        else:
            tr.append(mido.Message("note_off", note=p, velocity=0, channel=channel, time=dt))
    mid.tracks.append(tr)

# ---------------- compose new layers ----------------
mid = new_mid()

# 1. SOLO CELLO (GM43, ch1) — lyrical line, all sections (bridge: soft, sparse)
cello = []
for i, (st, en, cn) in enumerate(REGIONS):
    ch = CHORDS[cn]
    dur = en - st
    if in_bridge(st):
        cello.append((st, en, ch["triad"][0], 45))
        continue
    motif = [ch["triad"][0] + 12, ch["triad"][1] + 12, ch["triad"][2] + 12, ch["e9"] + 12]
    if i % 2 == 1:
        motif = motif[::-1]
    n = 4
    for j, p in enumerate(motif):
        ns, ne = st + j * dur / n, st + (j + 1) * dur / n + 0.12
        cello.append((ns, min(ne, en), p, 72))
add_track(mid, 43, 1, cello)

# 2. HARP (GM25 pluck, ch2) — broken 9th arpeggios
harp = []
for st, en, cn in REGIONS:
    ch = CHORDS[cn]
    patt = [ch["bass"] + 24, ch["triad"][0] + 12, ch["triad"][1] + 12,
            ch["triad"][2] + 12, ch["e9"] + 12, ch["triad"][2] + 12,
            ch["triad"][1] + 12, ch["triad"][0] + 12]
    step = 1.0 if in_bridge(st) else 0.5
    vel = 45 if in_bridge(st) else 60
    t = st
    k = 0
    while t < en - 0.1:
        harp.append((t, t + step * 0.9, patt[k % len(patt)], vel))
        t += step
        k += 1
# harp run into the hold (144-146): ascending A minor to D6
run = [45, 49, 52, 57, 61, 64, 69, 74, 77, 81, 86]
for j, p in enumerate(run):
    harp.append((144.0 + j * 0.18, 144.0 + j * 0.18 + 0.25, p, 70))
add_track(mid, 25, 2, harp)

# 3. CELESTA (GM9 bell, ch3) — sparse D6 glints
celesta = []
for t in [8, 12, 16, 20, 24, 28, 118, 122, 126, 146]:
    celesta.append((t, t + 1.5, 86, 48))
add_track(mid, 9, 3, celesta)

# 4. SOLO VIOLA (GM42, ch4) — enters 30s; bridge: static Gm(add9) hold
viola = []
for st, en, cn in REGIONS:
    if st < 30.0:
        continue
    ch = CHORDS[cn]
    if in_bridge(st):
        continue
    viola.append((st, st + (en - st) / 2, ch["triad"][1], 66))
    viola.append((st + (en - st) / 2, en, ch["triad"][2], 66))
# bridge static hold: Gm(add9) = G3 Bb3 D4 A3, 12s unmoving (Gorecki stillness)
for t in [118.0, 122.0, 126.0]:
    for p in [55, 58, 62, 57]:
        viola.append((t, t + 4.0, p, 50))
add_track(mid, 42, 4, viola)

# 5. BASSOON (GM71 reed, ch5) — enters 74s (verse 2), low counterline
bassoon = []
for st, en, cn in REGIONS:
    if st < 74.0:
        continue
    ch = CHORDS[cn]
    vel = 48 if in_bridge(st) else 58
    bassoon.append((st, st + (en - st) / 2, ch["bass"] + 12, vel))
    bassoon.append((st + (en - st) / 2, en, ch["bass"] + 19, vel))
add_track(mid, 71, 5, bassoon)

# 6. BASS CLARINET (GM72 flute, ch6) — enters 74s, pairs with bassoon
bclar = []
for st, en, cn in REGIONS:
    if st < 74.0:
        continue
    ch = CHORDS[cn]
    vel = 44 if in_bridge(st) else 52
    bclar.append((st, en, ch["triad"][1] - 12, vel))
add_track(mid, 72, 6, bclar)

# 7. DIVISI VIOLINS HIGH (GM41, ch7) — enters 52s; extensions above
divvi = []
for st, en, cn in REGIONS:
    if st < 52.0 or in_bridge(st):
        continue
    ch = CHORDS[cn]
    if st < 74.0:
        vel = 65
        notes = [ch["e9"] + 12, ch["triad"][2] + 12]
    elif st < 96.0:
        vel = 40
        notes = [ch["e9"] + 12]
    elif st < 118.0:
        vel = 70
        notes = [ch["e9"] + 12, ch["e11"] + 12]
    else:
        vel = 80
        notes = [ch["e9"] + 12, ch["e11"] + 12, ch["e13"] + 12]
    for p in notes:
        divvi.append((st, en, p, vel))
add_track(mid, 41, 7, divvi)

# 8. LOW CELLOS/BASSES (GM44, ch8) — enters 30s; root-fifth pedal
low = []
for st, en, cn in REGIONS:
    if st < 30.0:
        continue
    ch = CHORDS[cn]
    # bridge Eb detour: 124-126 play Eb pedal under Bb region
    if 122.0 <= st < 126.0:
        low.append((st, min(st + 2.0, en), ch["bass"], 60))
        if en > st + 2.0:
            low.append((st + 2.0, en, 39, 60))  # Eb2
        continue
    low.append((st, st + (en - st) / 2, ch["bass"], 62))
    low.append((st + (en - st) / 2, en, ch["bass"] + 7, 62))
add_track(mid, 44, 8, low)

# 9. FRENCH HORNS muted (GM61 brass, ch9) — enters 96s; swells
horns = []
for st, en, cn in REGIONS:
    if st < 96.0 or in_bridge(st):
        continue
    ch = CHORDS[cn]
    mid_t = st + (en - st) / 2
    for p in ch["triad"]:
        horns.append((st, mid_t, p, 60))
        horns.append((mid_t, en, p, 82))
add_track(mid, 61, 9, horns)

# 10. TROMBONES (GM58 brass, ch11) — final chorus ONLY
tbn = []
for st, en, cn in REGIONS:
    if st < 130.0:
        continue
    ch = CHORDS[cn]
    for p in [ch["bass"] + 12, ch["triad"][0], ch["triad"][2]]:
        tbn.append((st, en, p, 88))
add_track(mid, 58, 11, tbn)

# 11. PIPE ORGAN (GM19 organ, ch12) — enters 96s pp, grows
organ = []
for st, en, cn in REGIONS:
    if st < 96.0:
        continue
    ch = CHORDS[cn]
    if st < 118.0:
        vel = 55
        notes = [ch["bass"] - 12]
    elif in_bridge(st):
        vel = 50
        notes = [ch["bass"] - 12]
    elif st < 130.0:
        vel = 62
        notes = [ch["bass"] - 12, ch["bass"]]
    else:
        vel = 85
        notes = [ch["bass"] - 12, ch["bass"], ch["triad"][0], ch["triad"][1]]
    for p in notes:
        organ.append((st, en, p, vel))
add_track(mid, 19, 12, organ)

# 12. TIMPANI (ch10 drums, notes 45/47) — final chorus rolls + crescendo into hold
timp = []
t = 130.0
k = 0
while t < 144.0:
    timp.append((t, t + 0.2, 45 if k % 2 == 0 else 47, 52))
    t += 0.25
    k += 1
t = 144.0
v = 60
while t < 146.0:
    timp.append((t, t + 0.2, 45, v))
    t += 0.2
    v += 4
add_track(mid, 0, 9, timp)

# 13. CLOCK TICK (ch10, note 42 hat) — verses only, very soft
tick = []
t = 8.0
while t < 52.0:
    tick.append((t, t + 0.05, 42, 22))
    t += 1.0
t = 74.0
while t < 96.0:
    tick.append((t, t + 0.05, 42, 22))
    t += 1.0
add_track(mid, 0, 9, tick)

layers_mid = os.path.join(TMP, "kiko_v2_layers.mid")
mid.save(layers_mid)
print(f"layers MIDI saved: {sum(len(t) for t in mid.tracks)} events")

# ---------------- ending MIDI (local 0-7s) ----------------
# THE HOLD: full-power Dm13 (D F A C E G B) strings+keys+brass+organ, 6s, then end.
em = new_mid()
hold = []
# base voices (re-voiced for the hold — new material, v1 never had a hold)
# piano GM0: rolled attack then sustain
proll = [50, 53, 57, 60, 64, 67, 71, 74]
for j, p in enumerate(proll):
    hold.append(("piano", 0, j * 0.1, j * 0.1 + 0.5, p, 62))
for p in [62, 65, 69]:
    hold.append(("piano", 0, 0.8, 6.0, p, 55))
# strings base GM48
for p in [50, 53, 57, 60, 64, 67, 69, 72]:
    hold.append(("strings", 48, 0, 6.0, p, 68))
# choir pad GM88
for p in [62, 65, 69, 76]:
    hold.append(("choir", 88, 0, 6.0, p, 58))
# divisi violins shimmer GM41
for p in [76, 79, 83, 86]:
    hold.append(("dvln", 41, 0, 6.0, p, 75))
# violas GM42
for p in [65, 69, 72]:
    hold.append(("dvia", 42, 0, 6.0, p, 65))
# cellos GM43
for p in [50, 57, 62]:
    hold.append(("vc", 43, 0, 6.0, p, 70))
# basses GM44
for p in [26, 38]:
    hold.append(("cb", 44, 0, 6.0, p, 75))
# horns GM61
for p in [57, 62, 65]:
    hold.append(("hn", 61, 0, 6.0, p, 72))
# trombones GM58
for p in [50, 57, 62]:
    hold.append(("tbn", 58, 0, 6.0, p, 80))
# organ GM19 — the cathedral
for p in [26, 38, 50, 53, 57, 60, 64]:
    hold.append(("org", 19, 0, 6.0, p, 88))
# celesta final glint GM9
hold.append(("cel", 9, 0, 1.5, 86, 45))
# timpani single grounding hit (ch10)
hold.append(("timp", -1, 0, 0.3, 45, 70))

PROG = {"piano": 0, "strings": 48, "choir": 88, "dvln": 41, "dvia": 42,
        "vc": 43, "cb": 44, "hn": 61, "tbn": 58, "org": 19, "cel": 9}
CHN = {"piano": 1, "strings": 2, "choir": 3, "dvln": 4, "dvia": 5,
       "vc": 6, "cb": 7, "hn": 8, "tbn": 10, "org": 11, "cel": 12, "timp": 9}
for name, prog, st, en, p, v in hold:
    tr = mido.MidiTrack()
    ch = CHN[name]
    if ch != 9:
        tr.append(mido.Message("program_change", program=PROG[name], channel=ch, time=0))
    tr.append(mido.Message("note_on", note=p, velocity=v, channel=ch, time=s2t(st)))
    tr.append(mido.Message("note_off", note=p, velocity=0, channel=ch, time=s2t(en) - s2t(st)))
    em.tracks.append(tr)

ending_mid = os.path.join(TMP, "kiko_v2_ending.mid")
em.save(ending_mid)
print("ending MIDI saved")

# ---------------- render ----------------
RENDER = os.path.expanduser("~/workspace/video-fix-tools/midi/render_midi.py")
layers_wav = os.path.join(TMP, "kiko_v2_layers.wav")
ending_wav = os.path.join(TMP, "kiko_v2_ending.wav")
subprocess.run(["python3", RENDER, "--input", layers_mid, "--output", layers_wav], check=True)
subprocess.run(["python3", RENDER, "--input", ending_mid, "--output", ending_wav], check=True)

# ---------------- mix ----------------
def load_wav(p):
    w = wave.open(p)
    assert w.getframerate() == SR and w.getnchannels() == 1
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    w.close()
    return d

v1 = load_wav(V1)
layers = load_wav(layers_wav)
ending = load_wav(ending_wav)

# v1 is 151.77s; layers render is ~147s (notes to 146 + tail). Pad/trim to 146s.
CUT = int(146.0 * SR)
v1_seg = v1[:CUT]
lay_seg = layers[:CUT]
if len(lay_seg) < CUT:
    lay_seg = np.pad(lay_seg, (0, CUT - len(lay_seg)))

# adaptive gain: new layers ~ -7dB under v1 in the chorus region (52-74s)
c0, c1 = int(52 * SR), int(74 * SR)
rms_v1 = np.sqrt(np.mean(v1_seg[c0:c1] ** 2)) + 1e-9
rms_lay = np.sqrt(np.mean(lay_seg[c0:c1] ** 2)) + 1e-9
gain = (rms_v1 / rms_lay) * 10 ** (-7 / 20)
gain = min(gain, 0.8)
print(f"v1 chorus RMS {rms_v1:.0f}, layers RMS {rms_lay:.0f}, gain {gain:.3f}")

base = v1_seg + lay_seg * gain

# ending: local 0-6s hold + cut. Find zero-crossing near 6.0s for the abrupt cut.
HOLD_S = int(6.0 * SR)
# search for zero crossing in [5.98, 6.02]
zc = HOLD_S
seg = ending[max(0, HOLD_S - int(0.02 * SR)):HOLD_S + int(0.02 * SR)]
best, bestd = HOLD_S, 1e9
for i in range(1, len(seg)):
    if seg[i - 1] <= 0 < seg[i] or seg[i - 1] >= 0 > seg[i]:
        idx = max(0, HOLD_S - int(0.02 * SR)) + i
        if abs(idx - HOLD_S) < bestd:
            bestd, best = abs(idx - HOLD_S), idx
CUT_END = best
print(f"abrupt cut at local {CUT_END / SR:.4f}s (target 6.0)")
end_hold = ending[:CUT_END].copy()
# 2ms anti-click ramp (inaudible as fade, kills the discontinuity click)
nr = int(0.002 * SR)
ramp = np.linspace(1.0, 0.0, nr)
end_hold[-nr:] *= ramp
# match ending level to base: normalize ending peak to base peak
peak_base = np.max(np.abs(base)) + 1e-9
peak_end = np.max(np.abs(end_hold)) + 1e-9
end_hold *= (peak_base / peak_end) * 1.05  # hold hits slightly hotter
print(f"ending peak matched: base {peak_base:.0f} -> hold {np.max(np.abs(end_hold)):.0f}")

# crossfade 40ms at 146s
XF = int(0.04 * SR)
out_len = CUT + len(end_hold) + SR  # +1s silence
out = np.zeros(out_len, dtype=np.float32)
out[:CUT] = base
# equal-power crossfade
t = np.linspace(0, np.pi / 2, XF)
fout = np.cos(t) ** 2
fin = np.sin(t) ** 2
out[CUT - XF:CUT] = base[CUT - XF:CUT] * fout + end_hold[:XF] * fin
out[CUT:CUT + len(end_hold) - XF] = end_hold[XF:]
# (tail after is already zeros = digital silence)

# final normalize to -1 dBFS
peak = np.max(np.abs(out)) + 1e-9
out *= (10 ** (-1 / 20) * 32767 / peak)
print(f"final: {len(out) / SR:.2f}s, peak normalized to -1dBFS")

w = wave.open(V2, "w")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes(out.astype(np.int16).tobytes())
w.close()
print("wrote", V2)

# section RMS report (verify new layers are present but not dominant)
import math
for name, a, b in [("verse1", 8, 30), ("chorus1", 52, 74), ("final", 130, 146), ("hold", 146, 152)]:
    i0, i1 = int(a * SR), min(int(b * SR), len(out))
    seg = out[i0:i1]
    print(f"  {name}: RMS {20 * math.log10(np.sqrt(np.mean(seg**2)) + 1e-9):.1f} dBFS")
