# KIKO PIER SCENE — Music Bed

**File:** `audio/kiko-pier-scene-music-8s.wav`
**Duration:** 8.000s exactly (44.1kHz, 16-bit WAV, 706KB)
**Peak:** -1.0 dBFS (headroom for foghorn + water SFX layering)

## Musical Spec

- **Key:** D minor
- **Tempo:** 60 BPM (1 beat = 1.0s, 8 beats total)
- **Voices:** Piano (GM 0) + Strings (GM 48) + Choir Pad (GM 88)
- **Built:** 2026-10-11, numpy GM synth (`video-fix-tools/midi/render_midi.py`), MIDI composed by hand

## Structure (matches EP01 3:57–4:05)

| Time | Section | What's happening |
|------|---------|------------------|
| 0.0–2.0s | **Moonlit fog** | Low Dm drone (strings + choir pad), single sparse piano D5 like a water drop. Quiet, atmospheric. |
| 2.0–4.0s | **The song begins** | Bb major lift (VI) — the musical-theater turn. Piano melody enters: A–Bb–A–G, stepwise and singable. Strings swell underneath. |
| 4.0–6.0s | **Swell** | Gm → A (iv → V), tension builds. Choir pad thickens. Piano melody aches upward: F (held) → E → F. |
| 6.0–7.5s | **Peak** | Resolve to Dm. Piano hits D5 — his big note. Full strings + choir. |
| 7.5–8.0s | **BUTTON** | Dm slam across 4 octaves (piano + strings + choir). Hard hit, 30ms fade to avoid click. Scene cuts here. |

## Dynamic Arc (measured RMS per 0.5s)

```
0.0-2.0s  ▁▁▂▂  quiet intro (0.045-0.076)
2.0-4.0s  ▃▃▃▃  melody enters (0.085-0.095)
4.0-6.0s  ▅▅▅▆  swell (0.132-0.148)
6.0-7.5s  ▆▇██  peak + resolve (0.157-0.200)
7.5-8.0s  ████  BUTTON (0.271)
```

## Notes for Mix

- Leave the low end open: no bass instrument, so the foghorn SFX sits clean underneath.
- Midrange has room for Kiko's vocal (Japanese + broken English) — piano melody is the guide, not a competitor.
- The choir pad is subtle by design; it's atmosphere, not a feature.
- If the scene needs more comedy, duck the music 2dB when he starts singing — let his earnestness carry it.
