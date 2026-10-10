# Wave 53 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed tools wired with REAL runs. Both extend the Wave
51/52 cartoon-voice pipeline one stage further:

**text -> VO (Kokoro, Wave 51) -> lip-sync (Rhubarb, Wave 51) ->
denoise + loudness master (Wave 52) -> SUBTITLES (this lane)**,

plus an image-pipeline HDR plate stage (OpenImageIO). Both wire scripts are
original MIT-licensed code (this directory); external libs/binaries/models are
invoked, never embedded. Nothing from `tools/quarantine` is linked or
imported anywhere in the wire paths.

Environment: Python 3.12.3, lane-local venv (`tools/wave53_lane_c/venv/`,
gitignored), `TMPDIR` pointed at lane-local `.scratch/` (`/tmp` is a 512 MB
tmpfs). faster-whisper 1.0.3 + ctranslate2 4.8.2 + av 12.3.0 +
OpenImageIO 3.1.18.1 (PyPI wheels); ffmpeg 8.1.2 / ffprobe (Ubuntu build).
Whisper `tiny` model (OpenAI weights, MIT) cached in `.scratch/hf`
(~75 MB, gitignored). Proof artifacts total ~372 KB — nothing near the
100 MB binary limit.

## 1. faster-whisper — subtitle post-stage (MIT)

- **Upstream:** SYSTRAN/faster-whisper — MIT verified 2026-10-08 via GitHub
  API (`spdx_id: MIT`); catalog entry (Wave 2) flipped
  `not-started` -> `WIRED — run-proven` this wave.
- **License:** MIT (upstream + model weights). Wire script MIT.
- **Script:** `wire_subtitle_stage.py` — transcribes the Wave 52 mastered
  podcast WAV (`tools/wave52_lane_c/proofs/audio_mastering/
  master_podcast_16lufs_stereo.wav`: 7.825 s, 24 kHz stereo) with
  word-level timestamps (seeded decode, temperature 0.0), writes SRT +
  WebVTT, muxes the SRT as a `mov_text` track into an MP4 deliverable next
  to the mastered audio, then extracts it back and byte-compares cues.
- **Proof (real input, real decode):**
  - Hypothesis: "Ladies and gentlemen, the streets are watching tonight.
    Two fighters step into the alley and only one walks out with the
    crown." — **WER 0.0** vs the known Wave 51 ground-truth line
    (22 words; the comma after "alley" is dropped — punctuation only,
    not a word error).
  - 2 segments, 22 word timings, all monotonic and inside the 7.825 s
    audio bounds; timing coverage 0.000–7.320 s.
  - Language detected `en` (p=1.0). Decode 2.11 s on CPU for 7.8 s audio.
  - Mux: `deliverable_subtitled.mp4` carries `audio/aac` +
    `subtitle/mov_text`; extracted SRT cues are byte-equal to the source
    SRT (round-trip PASS).
  - Determinism: two full transcribes -> identical word JSON.
  - 11/11 checks PASS.
- **Honest environment note:** faster-whisper >= 1.0.3 passes
  `metadata_errors="ignore"` to `av.open()`, but the newest PyAV wheel
  (19.0.1) dropped that kwarg while 14.4.0 has no cp312 wheel here — so the
  lane pins **av==12.3.0** (last wheel with the kwarg) alongside
  faster-whisper==1.0.3. Documented in the venv; no upstream code was
  modified.
- **Artifacts:** `proofs/subtitle_stage/vo_line.srt`,
  `proofs/subtitle_stage/vo_line.vtt`,
  `proofs/subtitle_stage/deliverable_subtitled.mp4`,
  `proofs/subtitle_stage/extracted_roundtrip.srt`,
  `proofs/subtitle_stage/result.json`.

## 2. OpenImageIO — HDR plate read/write QC (Apache-2.0)

- **Upstream:** AcademySoftwareFoundation/OpenImageIO — Apache-2.0 verified
  2026-10-08 via GitHub API (`spdx_id: Apache-2.0`); catalog entry
  (Wave 7 A) flipped `not-started` -> `WIRED — run-proven` this wave.
- **License:** Apache-2.0 (upstream). Wire script MIT.
- **Script:** `wire_oiio_plate.py` — reads a REAL pipeline frame through
  OIIO (`tools/wave50_lane_c/proofs/caption_burnin/proof_frame_1_5s.png`:
  640x360x3, rendered pixels), writes OpenEXR (half float, zip) with
  production metadata attributes, reads it back, and measures.
- **Proof (real bytes in/out):**
  - EXR half round-trip max abs per-channel error: **2.43e-04**
    (0–1 scale; well inside the half-precision quantization bound).
  - Metadata round-trip: custom attributes (`wave53:lane`,
    `wave53:tool`, `Software`) read back byte-equal.
  - OIIO `computePixelStats` average vs numpy mean: max disagree
    **9.58e-05** (expected: OIIO stats run on the UINT8 buffer, numpy on
    float32 — accumulation-path difference, gate set at 1e-3, not 1e-6).
  - Determinism: two EXR writes -> byte-identical files.
  - **Lossy control (reported, not gated):** PNG -> JPEG q95 measures
    max abs diff **0.998** — sharp white-text-on-black edges get mauled
    by 4:2:0 chroma subsampling. Lossy is lossy; documented as the honest
    reason plates stay EXR.
  - 7/7 checks PASS.
- **Artifacts:** `proofs/oiio_plate/plate_half.exr`,
  `proofs/oiio_plate/plate_half_b.exr`, `proofs/oiio_plate/plate_q95.jpg`,
  `proofs/oiio_plate/result.json`.

## Deferred / honest failures

- faster-whisper 1.2.1 (latest) could not be used: it requires the
  `metadata_errors` kwarg in `av.open()` and the only cp312-compatible
  PyAV wheel in this environment (19.0.1) rejects it. Pinned to the
  working combination faster-whisper==1.0.3 + av==12.3.0 instead of
  patching upstream code. If a future PyAV restores the kwarg, re-pin.
- PD-score ingestion was not repeated: Wave 50 Lane C already wired
  `wire_pd_score.py` with real archive.org proofs — a second fetch would
  be duplication, not new wiring.
