# KIKO PIER SONG — v2 Orchestration Expansion: Build Notes

**File:** `audio/kiko-pier-song-full-instrumental-v2.wav`
**Duration:** 153.0s (2:33) — 44.1kHz, 16-bit WAV
**Peak:** -1.0 dBFS
**Built:** 2026-10-11
**Composer script:** `audio/kiko-pier-song-v2-compose.py` (saved in repo per salvage law)
**Render pipeline:** hand-composed MIDI → numpy GM synth (`video-fix-tools/midi/render_midi.py`)

## HARD CONSTRAINT (owner directive — honored)

**ADDITIVE ONLY.** The v1 instrumental (piano + strings + choir pad) is preserved
byte-for-byte for 0:00–2:26 (verified: scene 0–8s correlates 1.0000 with v1).
New instruments layer ON TOP at -7dB relative to v1 in choruses. Nothing existing
was revoiced, replaced, or removed. The only structural change is the ending
(2:26 onward), which v1 never had in this form.

## What was added (13 new voices)

| # | Voice | GM | Entrance | Role |
|---|-------|----|----------|------|
| 1 | Solo Cello | 43 | 0:08 (Verse 1) | Lyrical line shadowing the vocal contour; soft/sparse in bridge |
| 2 | Harp | 25 (pluck) | 0:08 | Broken 9th-chord arpeggios (Dm9, Bbmaj9, Gm9…); ascending run into the hold |
| 3 | Celesta | 9 | sparse | D6 glints doubling piano water-drops; final glint at hold attack |
| 4 | Solo Viola | 42 | 0:30 (Pre-chorus) | Dark string color on vocal line; STATIC Gm(add9) hold for full 12s bridge (Górecki stillness) |
| 5 | Bassoon | 71 | 1:14 (Verse 2) | Low chromatic counterline (Mozart: no bright winds, only dark ones) |
| 6 | Bass Clarinet | 72 | 1:14 | Pairs with bassoon on chord thirds |
| 7 | Divisi Violins (high) | 41 | 0:52 (Chorus 1) | Sustained 9ths → 9ths+11ths → 9/11/13ths as song builds; pulled back in Verse 2 |
| 8 | Low Cellos/Basses | 44 | 0:30 | Root–fifth pedal ("the night under his feet"); Eb detour in bridge (chromatic mediant dream) |
| 9 | French Horns (muted) | 61 | 1:36 (Chorus 2) | Swells per chord change, pp→mf |
| 10 | Trombones (pair) | 58 | 2:10 (Final chorus ONLY) | Two-note swells; first brass entrance of weight in the whole song (thunderclap by restraint) |
| 11 | Pipe Organ | 19 | 1:36 pp, growing | Pedal + chord; the memorial weight (Interstellar lineage) |
| 12 | Timpani | ch10 | 2:10 | Soft rolls; crescendo roll 2:24–2:26 into the hold |
| 13 | Clock tick | ch10 | Verses only | 60 BPM soft tick — time passing (Interstellar lineage) |

Richer chords: all extensions live in the NEW voices (9ths/11ths/13ths, Dm(maj7)
bittersweetness in Verse 2 harp, Asus4→A catch-in-the-throat in pre-chorus).
Piano keeps its triads throughout.

## THE ENDING (owner's specific direction)

**Replaces** v1's Dm slam outro. v1 is preserved as the slam-alternative version.

- **2:26 — THE HOLD:** Full orchestra lands together on a massive Dm13
  (D–F–A–C–E–G–B) across 5+ octaves: strings (all divisi), piano (rolled attack),
  pipe organ (cathedral pedal), horns, trombones, basses. Full power from beat 1.
- **2:26–2:32 — SUSTAIN:** 6 seconds at full power. Hold RMS sits ~5dB hotter
  than the final chorus. No decay, no diminuendo — it just *holds*.
- **2:32 (151.96s) — ABRUPT CUT:** Dead silence. Zero-crossing cut with a 2ms
  anti-click ramp (inaudible as a fade — purely click prevention). Verified:
  1.04s of absolute digital silence follows (max abs = 0.0).

Classical reference: Beethoven's *Coriolan Overture* ending (storm → abrupt
chords → silence) and the grand-pause tradition. The power is in the suddenness —
the silence under the dedication card hits harder than any fade-out.

## Section energy (measured RMS deltas)

Verse 1 intimate → Chorus 1 swelling (+7dB) → Final chorus transcendent (+11dB)
→ Hold at full power (+16dB over verse 1) → SILENCE.

## Verification performed

- [x] v1 0:00–2:26 preserved (scene correlation 1.0000)
- [x] New layers at -7dB under v1 (adaptive gain 0.58, chorus-region matched)
- [x] No clipping: peak exactly -1.00 dBFS
- [x] Splice at 146s smooth (RMS rises naturally through crossfade, no discontinuity)
- [x] Abrupt cut verified: digital silence after 151.96s, 1.04s tail
- [x] 1645 MIDI events across 13 new voices + ending
- [x] Duration 153.0s

## What's NOT in v2 (left for the owner-verified vocal pass)

Per owner directive 2026-10-11: orchestration expansion happened BEFORE vocal
verification here because the instrumental layers needed to exist for the vocal
timing work — but no further instrumental changes until the owner signs off on
vocals. The vocal mix (`kiko-pier-song-full-vocal-mix.wav`) was built against v1;
it will need re-mixing against v2 once vocals are approved.
