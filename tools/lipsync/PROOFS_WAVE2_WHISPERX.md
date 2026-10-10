# PROOFS — Whisper-class phoneme-alignment lip-sync upgrade (Wave 2, Lane B)

Date: 2026-10-08. Branch: `anim-wave2-lane-b`.

## What was built

`tools/lipsync/whisper_align_to_timeline.py` — a second lip-sync engine next to
the Wave 1 Rhubarb pipeline. It produces a **phoneme-timed viseme timeline**
*with the spoken words attached*, in the same gapless JSON schema as
`rhubarb_to_timeline.py`, so animators can scrub by word and re-target visemes
per word without re-running audio.

`tools/lipsync/compare_timelines.py` — side-by-side Rhubarb vs whisper-align
comparison: duration-weighted viseme agreement, boundary MAE, span counts.

## Stack (documented fallback — read this before the numbers)

WhisperX proper was **not** run: this sandbox has no GPU and no torch, and the
full WhisperX path needs torch plus a ~1.2 GB English phone-alignment model.
The Wave 2 brief explicitly authorizes the fallback, which is what shipped:

| stage | source | real or approximated |
|---|---|---|
| word-level timestamps | faster-whisper base (Systran, MIT), CPU int8, VAD-filtered | **REAL** — neural ASR |
| word → phones | CMUdict via `pronouncing` (BSD-3-Clause) | **REAL** — G2P lookup |
| phone boundaries *inside* a word span | proportional split by phone-class duration weights (vowels 3, fricatives/sonorants 2, stops 1), anchored on the real word span | **APPROXIMATION** — documented, not acoustic |
| phones → visemes | Wave 1 Arpabet→viseme table + 4 Wave 2 extensions (IH→A, ER→C, NG→C, SH/ZH→C, same mouth classes) | deterministic mapping |

The comparison against Rhubarb's *acoustic* viseme boundaries below is exactly
the measurement of how far off the approximation is.

## Real proofs

### A. Static EP02 L1 (same line as Wave 1 — the side-by-side target)

Input: `proofs/lane-b/static_L1_standin_raw.wav` (8.25 s, espeak-ng stand-in VO —
voice is a stand-in; the TIMELINE is the proof, per Wave 1).

- Transcript (faster-whisper base, verbatim): "I-O! You see that fire? That's the
  **math** signal, baby! Council's in session! Everybody move like you got
  somewhere to be!" — note "math" for "bat": the espeak stand-in's flat
  rendering, honestly transcribed; the approved line says "bat signal".
- 22 words with timestamps, **74 phone segments, 0 OOV**, 62-span timeline —
  **VERIFY: PASS** (gapless 0.00–8.25, all visemes in {A..H, X}).
- Artifacts: `proofs/wave2/whisperx_upgrade/static_L1_whisper_timeline.json`,
  `static_L1_whisper_meta.json` (words + phone segments), `COMPARISON_static_L1.md`.

### B. Newest voice-clone audio (no newer VO exists in the lanes)

Checked `~/workspace/voice-clone-work/` 2026-10-08: cipher/, billsaber/,
sombra/ lanes are still rendering (watchers running, no finished VO files).
Newest finished audio is `static_voice_test.m4a` (2026-10-08 01:46), converted
to 16 kHz mono (`static_voice_test_16k.wav`, 12.93 s).

- Transcript (verbatim): "Hi, yo, it's the Certified G, the realist dude in the
  room. You got a problem with static? Then step UP because I'm talking
  circles around all y'all and I ain't even warmed up yet. How you doing?"
- 39 words, **125 phone segments, 0 OOV** (incl. "y'all" → Y AO L).
- Both engines run on it: Rhubarb → 73 cues, 66 moves, VERIFY PASS;
  whisper-align → 98 spans, 89 moves, VERIFY PASS.
- Artifacts: `static_voice_test_16k.wav`, `static_voice_test_cues.tsv`,
  `static_voice_test_rhubarb_timeline.json`, `static_voice_test_whisper_timeline.json`,
  `static_voice_test_whisper_meta.json`, `COMPARISON_static_voice_test.md`.

## Side-by-side results (honest reading)

| metric | Static L1 | voice_test |
|---|---|---|
| duration-weighted viseme agreement | **21.3%** | **23.8%** |
| boundary MAE (Rhubarb bnd → nearest whisper bnd) | **56 ms** | **54 ms** |
| spans: Rhubarb / whisper | 35 / 62 | 73 / 98 |
| rest (X) coverage: Rhubarb / whisper | 18.9% / 26.5% | 14.2% / 23.0% |

Reading: the two engines agree closely on **where** mouths change (54–56 ms
boundary MAE — sub-frame at 24 fps is 41.7 ms, so this is ~1.3 frames), but
disagree on **which** viseme labels go there (21–24% agreement). Three
documented causes: (1) different phone→viseme conventions — Rhubarb's internal
Preston Blair mapping vs the Wave 1 documented table; (2) the espeak
stand-in's flat prosody confuses Rhubarb (the documented 2.1 s B hold on L1);
(3) the whisper path's word-internal boundaries are proportional splits, not
acoustic measurements. None of this was tuned to flatter the numbers.

The whisper path's value-add is not boundary precision — it is the attached
words/phones (`_meta.json`): animators scrub by word, and visemes can be
re-targeted per word without re-running audio. Rhubarb remains the
acoustic-boundary reference; the two timelines are complementary, and
`compare_timelines.py` keeps them honest against each other.

## SHA-256 (proof artifacts)

```
406cb523858a2ddfe46f829a3df2ed905a0ac6a0459dee6c0bddc21e87a7d774  static_L1_whisper_meta.json
9333150c1b42a6f748f080bd8d524706b1d52afb96d9f49a916f643234cbfb9d  static_L1_whisper_timeline.json
37b00e0a4fdd3d170ef599587e4712d7f80ade957e103f15b5fde11ddb990c87  static_voice_test_rhubarb_timeline.json
6c3f9648562e5516f24dbe9aedbc5977749064f98b7c6cb58bebf8d131524c1d  static_voice_test_whisper_meta.json
ef9d27d0cec5568e4e4c9d628c4d0a12a53b4188bd4cb6363d33052b52d94cd7  static_voice_test_whisper_timeline.json
afada4073df32bf2833f820bf2b1078fca2e9bc4c20a6546906ab3a4dc053bd8  static_voice_test_cues.tsv
ae8acb2fecfe03fec261387100e833a902e076613178d4594d905f154b6d0ced  static_voice_test_16k.wav
```

(Full list in `proofs/wave2/whisperx_upgrade/SHA256SUMS.txt`.)

## Reproduce

```bash
cd tools/lipsync
# whisper-align path (needs: pip install faster-whisper pronouncing)
python3 whisper_align_to_timeline.py proofs/lane-b/static_L1_standin_raw.wav /tmp/out_timeline.json
# comparison (needs both timelines built)
python3 compare_timelines.py proofs/lane-b/static_L1_timeline.json /tmp/out_timeline.json /tmp/comparison.md
```
