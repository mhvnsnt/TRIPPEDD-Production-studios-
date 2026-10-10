# PROOFS — Lip-sync VO test (Wave 3, Lane C)

Date: 2026-10-08. Branch: `wave3-anim-lane-c`.

## VO check result: NOT YET LANDED as of 2026-10-08 04:24 UTC

Checked `~/workspace/voice-clone-work/` at 04:21 UTC and again at 04:24 UTC
2026-10-08 (cutoff: files newer than 2026-10-08 04:00 UTC). All non-venv audio
in the cipher/, sombra/, billsaber/ lanes, newest first:

| file | mtime (UTC) |
|---|---|
| `billsaber/billsaber_ref_trim15.wav` | 2026-10-08 03:23 |
| `sombra/samples/priest_ref_19s.wav` | 2026-10-08 02:17 |
| `sombra/samples/priest_region_26m40_37m40.wav` | 2026-10-08 01:50 |
| `billsaber/billsaber_ref_freestyle.wav` | 2026-10-08 01:47 |
| `static_voice_test.m4a` (lane root, static) | 2026-10-08 01:46 |

These are reference takes and the earlier static test — **none is a newly
rendered character VO from the cipher/, sombra/, or billsaber/ lanes newer
than the 04:00 UTC cutoff**. (The `.wav` files inside `cipher/venv/` are
scipy/gradio/s3tokenizer package test data, not VO renders — excluded.)

**Therefore the end-to-end lip-sync test was NOT run. No test is claimed.**
`tools/lipsync/whisper_align_to_timeline.py` (faster-whisper → CMUdict phones
→ visemes) and the per-character mouth charts in
`tools/lipsync/viseme_charts/` (cipher, sombra, static, narrator) remain
staged and ready for the first VO that lands — when it does, the test is:
run the VO through the pipeline, compare against the character's mouth
chart, and record the audio file's SHA-256 in this doc's successor section.

## What this lane did instead (per brief): voice-directed retiming research

Per the Wave 3 Lane C brief, with no VO to test, the lane cataloged **11
open-source tools that retime animation to voice delivery** — every license
verified from upstream sources, never assumed:

- New catalog section `## Audio-driven animation retiming (motion synced to
  voice delivery)` appended to `docs/ANIMATION_TOOL_CATALOG.md`
  (9 entries: MuseTalk MIT, ffsubsync MIT, sherpa-onnx Apache-2.0,
  Prosodylab-Aligner MIT, auditok MIT, SpeechBrain Apache-2.0,
  EchoMimic Apache-2.0, silero-vad MIT, ZeroEGGS ⚠️ non-commercial).
- 2 GPL-family tools added to `docs/ANIMATION_QUARANTINE.md` rows 104–105
  (TarsosDSP GPL-3.0, alass GPL-3.0-or-later).
- Considered but NOT cataloged (license unverifiable from upstream this
  lane): VideoReTalking (no license statement found in upstream README),
  SyncNet (original Oxford release ambiguous research-only; modern
  reimplementations claim MIT — kept out rather than guess), WhisperTiming
  (could not locate the upstream repo/license). Any of these can be added in
  a later lane with a verified source.

Catalog count rule: 349 `####` headings before this lane → 358 after
(9 new entries; quarantine rows don't count).
