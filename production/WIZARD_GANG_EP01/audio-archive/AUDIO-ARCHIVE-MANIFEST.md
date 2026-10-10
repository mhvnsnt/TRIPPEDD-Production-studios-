# WG EP02 Audio Archive — Manifest

**Created:** 2026-10-10 (EP02 finish pass). **Purpose:** every WG audio asset NOT used in the EP02 5:00 final mix, preserved for later episodes, segments, and commercials. Nothing deleted.

## Voice law reminder (owner-locked)

No placeholder voices, no wrong-likeness voices, no synthetic filler. An unused voice asset stays archived until its real voice is ready — it never ships as a temp.

## Used in the EP02 5:00 final mix (NOT archived — live in the episode)

| Asset | Role |
|---|---|
| `static_L1`–`static_L23.wav` (minus P1/P2) | Static dialogue, Chatterbox Enzo clone |
| `cipher_c1/c2/c3.m4a` | Cipher lines (Lio Rush direction) |
| `test-h3.wav` | Sombra H3 (Damian Priest direction) |
| `music-bed-300s.wav` | Full 300s music bed, ducked under dialogue |
| `sfx-mic-feedback.wav`, `sfx-subbass-hit.wav` | Scripted SFX |

## Archived — prior assembly & utility

| File | Dur | What it is | Suggested reuse |
|---|---|---|---|
| `audio-orig.m4a` | 5:00 | Previous EP02 audio assembly (committed 2026-10-07, d07a0c24). Full-length mix predating the style-correction rebuild. | Reference for mix decisions; salvageable beds/stems |
| `silence250.m4a` / `silence-250.m4a` | 250s | Silence utility clips from assembly. | Editing room tone / gaps |

## Archived — voice tests & direction

| File | Dur | What it is | Suggested reuse |
|---|---|---|---|
| `billsaber_narrator_test.m4a` | 1s | Bill $aber XTTS v2 Narrator voice test. N1/N2 are VO-PENDING (clone not ready) — shipped without per voice law. | Drop N1/N2 in when the clone lands |
| `test-n1.wav` | 1s | Narrator N1 test | When clone lands — EP03+ |
| `sombra_negra_test.m4a` | 2s | Sombra Negra (Damian Priest likeness) voice test. H3 used the verified `test-h3.wav` instead. | Future Sombra lines |
| `test-h3-attempt1.wav` | 2s | Sombra H3 attempt 1 | Alt Sombra delivery |
| `test-h3-notched.wav` | 2s | Sombra H3 notched variant | Alt Sombra delivery |
| `standard_test.wav` | 1s | Sombra standard test (short) | Reference only |
| `static_cloned_test.mp3` | 12s | Static clone test (mp3) | Voice reference |
| `static_cloned_test.wav` | 12s | Static clone test (wav) | Voice reference |
| `static_cloned_test_16bit.wav` | 12s | Static clone test (16-bit) | Voice reference |
| `static_voice_test.m4a` | 12s | Static voice test (m4a) | Voice reference |
| `test-static-v2.wav` | 8s | Static (Enzo Amore) Chatterbox clone test v2 — "deeper, grittier" direction, owner verdict 2026-10-08. | Voice reference; commercials |

## Archived — earlier Cipher takes

| File | Dur | What it is | Suggested reuse |
|---|---|---|---|
| `test-c1.wav` | 6s | Cipher take 1 (early) | Alt Cipher delivery, flashback/commercial |
| `test-c1v2.wav` | 8s | Cipher take 1 v2 | Alt take |
| `test-c1v3.wav` | 7s | Cipher take 1 v3 | Alt take |
| `test-c1v3-feral.wav` | 8s | Cipher feral variant | Feral Cipher moments, later eps |
| `test-c2.wav` | 4s | Cipher take 2 (early) | Alt take |
| `test-c2v2.wav` | 3s | Cipher take 2 v2 | Alt take |
| `test-c2v2-hiss.wav` | 4s | Cipher take 2 v2 + hiss | Textured/atmospheric use |
| `test-c3.wav` | 7s | Cipher take 3 (early) | Alt take |
| `unhinged15.wav` | 15s | Cipher unhinged 15s | Cold opens, stingers |

## Archived — music & SFX components

| File | Dur | What it is | Suggested reuse |
|---|---|---|---|
| `music-bed-5min.wav` | 282s | Alternate full music bed | Alt score, segments |
| `ritual-drums-80s.wav` | 80s | Ritual drums bed component | Stingers, transitions |
| `sample-15s.wav` | 10s | 15s sample | Scratch/promo |

## Archived after mix — pilot lines (not in EP02 cut)

| File | What it is | Suggested reuse |
|---|---|---|
| `static_P1.wav` | Static pilot line P1 | Pilot episode, promos |
| `static_P2.wav` | Static pilot line P2 | Pilot episode, promos |

## NOT archived (kept in place)

- Voice-clone REFERENCE files (enzo_roast, priest refs, billsaber refs, cipher refs) — active inputs for future renders, stay in `~/workspace/voice-clone-work/`.
- EP02 final mix + stems — live in episode delivery, not the archive.

**Total:** 27 files. All verified playable. Provenance: `~/workspace/voice-clone-work/` (voice) and `~/workspace/wg-ep02-finish/` (music/SFX).
