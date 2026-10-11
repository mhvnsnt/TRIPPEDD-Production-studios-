# KIKO PIER — Full Song Instrumental

**File:** `audio/kiko-pier-song-full-instrumental.wav`
**Duration:** 151.8s (2:31.8) — 44.1kHz, 16-bit WAV
**Peak:** -1.0 dBFS
**SHA-256:** `6d1beb9959c8d05b86ada0bdfc4015e4e3fae07797d9d61fd384259f7921b3c4`
**Built:** 2026-10-11, hand-composed MIDI → numpy GM synth (`video-fix-tools/midi/render_midi.py`)

## Musical Spec (matches the 8s scene piece)

- **Key:** D minor
- **Tempo:** 60 BPM (1 beat = 1.0s)
- **Voices:** Piano (GM 0) + Strings (GM 48) + Choir Pad (GM 88)
- **First 8 seconds:** byte-for-byte verbatim from `kiko-pier-scene-music-8s.wav` (verified)

## Structure

| Time | Section | Chords | What's happening |
|------|---------|--------|------------------|
| 0:00–0:08 | **Scene piece (verbatim)** | Dm → Bb → Gm → A → Dm | Moonlit fog → song begins → swell → peak → BUTTON. The EP01 3:57–4:05 version. |
| 0:08–0:30 | **Verse 1** | Dm \| Bb \| Gm \| A | Stripped back. Piano water-drops + soft strings. Intimate — Kiko alone on the pier. |
| 0:30–0:52 | **Pre-chorus** | Bb \| Gm \| A \| A | Builds. Choir pad enters. Piano melody gets insistent. Tension rises. |
| 0:52–1:14 | **Chorus** | Dm \| Bb \| F \| A | Full swell. His big moment. Strings + choir + piano all in. |
| 1:14–1:36 | **Verse 2** | Dm \| Bbmaj7 \| Gm7 \| A7 | Darker variation. 7th colors. Choir lingers underneath. |
| 1:36–1:58 | **Pre-chorus 2 → Chorus 2** | Bb \| Gm \| Dm \| Bb \| F \| A (compressed) | Driving, bigger. Piano runs push into the second chorus. |
| 1:58–2:10 | **Bridge** | Gm \| Bb \| A | Quietest moment. Piano almost solo, aching. Then builds into... |
| 2:10–2:30 | **Final chorus** | Dm \| Bb \| F \| A \| Dm | Biggest. Full forces. |
| 2:28–2:32 | **Outro BUTTON** | Dm slam (4 octaves) | Same slam as the 8s piece. Hard cut point. |

## Chord Chart (D minor ballad)

```
Verse:       | Dm  | Bb  | Gm  | A   |  (i - VI - iv - V)
Pre-chorus:  | Bb  | Gm  | A   | A   |  (VI - iv - V - V)
Chorus:      | Dm  | Bb  | F   | A   |  (i - VI - III - V)
Verse 2:     | Dm  | Bbmaj7 | Gm7 | A7 |  (darker colors)
Bridge:      | Gm  | Bb  | A   |      |  (iv - VI - V)
Final:       | Dm  | Bb  | F   | A  | Dm | + BUTTON
```

## Vocal Entry Points

The vocal (Kiko: Japanese + broken English, baritone) was composed *around* — piano melody stays D4–D5, leaving D3–D4 open for his voice.

| Time | Section | Vocal guidance |
|------|---------|----------------|
| 0:10 | Verse 1 | Enters after 2s piano intro. Soft, conversational. Japanese. |
| 0:32 | Pre-chorus | More urgency. Mix Japanese + broken English. |
| 0:54 | Chorus | Full voice. His big sung moment. "The theater is empty. Encore anyway." |
| 1:16 | Verse 2 | Darker delivery. Lower energy, more menacing. |
| 1:38 | Pre-chorus 2 | Driving. Building to... |
| 1:40 | Chorus 2 | Bigger than chorus 1. |
| 2:00 | Bridge | Bare, vulnerable. Almost whispered. Then swells. |
| 2:12 | Final chorus | Everything he's got. Belt it. |
| 2:28 | Button | Cut with the slam. |

## Mix Notes

- **No bass instrument** — low end left open for foghorn SFX (scene version).
- **Piano is a guide, not a competitor** — sparse in verses, fuller in choruses, but always leaves the baritone range open.
- **Choir pad is atmosphere** — subtle by design, thickens in choruses.
- **Duck 2dB** when Kiko sings — let his earnestness carry the comedy.
- The 8s scene piece and this full song **cut together seamlessly** — same key, tempo, voices, and the opening 8s is identical.

## Build Notes

- MIDI composed by hand in `/tmp/kiko_song_compose.py` (archived in git with this doc).
- Rendered with `video-fix-tools/midi/render_midi.py` (donor-first per repo AGENTS.md).
- First 8s spliced from the original WAV (byte-verified), 30ms crossfade at the joint to prevent clicks.
- `soundfile` + `mido` via pip (system packages, reversible).
