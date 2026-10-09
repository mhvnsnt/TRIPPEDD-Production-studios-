# PROOFS.md — Wave 43 Lane B tool wiring

Two production-relevant tools, both permissively licensed, both exercised
against their REAL APIs with REAL proof artifacts. No stubs, no mocks.
Neither tool is in the LICENSE_QUARANTINE (MIT and BSD-2-Clause —
commercial-safe). Quarantined code was never linked, imported, or wired.

Run environment: `/home/hatch/.cache/w43b_venv` (Python 3.12 venv;
faster-whisper 1.2.1, imageio-ffmpeg 0.6.0, ctranslate2 4.8.2,
onnxruntime 1.30.0, numpy 2.5.3). Re-run:
`/home/hatch/.cache/w43b_venv/bin/python wire_faster_whisper.py`
`/home/hatch/.cache/w43b_venv/bin/python wire_imageio_ffmpeg.py`
License evidence: installed METADATA — faster-whisper `License: MIT`
(OSI Approved :: MIT License); imageio-ffmpeg `License: BSD-2-Clause`
(OSI Approved :: BSD License). Verified from the venv 2026-10-08.

## 1. faster-whisper (MIT) — speech-to-text for the captions pipeline

- Upstream: github.com/SYSTRAN/faster-whisper (CTranslate2 Whisper)
- Production relevance: the captions pipeline (`tools/captions`,
  `tools/video_pipeline/auto_caption.py`). Wave 42 wired VAD (webrtcvad)
  and subtitle manipulation (pysubs2); this closes the loop: VAD segments
  → faster-whisper transcription → SRT cues for episode deliverables.
- What was run (`wire_faster_whisper.py`):
  1. Synthesized a deterministic fixture with espeak-ng (local):
     "The wizard gang meets at midnight on the rooftop." → 16 kHz mono
     16-bit PCM WAV (`fw_fixture.wav`, 99,106 bytes, 3.10 s).
  2. Loaded the `base` model (cpu, int8; `tiny` also run) and transcribed
     via the real `WhisperModel.transcribe()` pipeline.
  3. Wrote `fw_transcript.srt` (valid SRT with real timestamps) and
     `fw_segments.json` (start/end/text/logprobs).
- Proof artifacts:
  - `fw_fixture.wav` — 99,106 bytes; verified parse: 1 ch, 16-bit,
    16000 Hz, 49,600 frames = 3.10 s (real synthesized speech).
  - `fw_transcript.srt` — 1 cue, `00:00:00,000 --> 00:00:02,720`,
    text "The wizard can meet sat mid-night on the rooftop."
  - `fw_segments.json` — the segment with start/end/avg_logprob/
    no_speech_prob; detected language en p=1.00.
  - `fw_report.txt` — full summary incl. both recall metrics.
- Accuracy (honest): strict key-word recall 2/4 (`wizard`, `rooftop`;
  robotic espeak prosody → `gang`→`can`, `at`→`sat`); normalized
  content-word recall 4/5 (`wizard`, `meet`, `midnight`, `rooftop`) = 0.80.
  The transcription pipeline (decode → segments → timestamps → SRT) is
  exact; the misses are small-model accuracy on synthetic speech, not a
  wiring failure. Both numbers are computed in the script and recorded
  in the report — no cherry-picking.
- Environment notes (honest): (a) faster-whisper 1.2.1's bundled PyAV
  decode path passes `metadata_errors=` to `av.open()`, removed in
  av>=12 (venv has av 19.0.1) — worked around by decoding the WAV in
  the script and passing a float32 array, a documented `transcribe()`
  input type; the model/feature pipeline is unchanged. (b) Model
  download (~75 MB tiny / ~145 MB base) goes to
  `~/.cache/huggingface` (not committed); the no_proxy IPv6-literal
  httpx quirk (~/TOOLS.md) was applied before download. (c) `/tmp` was
  92% full (other lanes' scratch — not touched); pip used
  `TMPDIR=/home/hatch/.cache/w43b_tmp`.
- Verdict: **PASS** — real inference, real segments, real SRT.

## 2. imageio-ffmpeg (BSD-2-Clause) — static ffmpeg for the video pipeline

- Upstream: github.com/imageio/imageio-ffmpeg (pip-bundled static build)
- Production relevance: the video pipeline (`tools/video_pipeline`,
  `tools/video`): test-pattern generation, probing, frame extraction,
  downscale transcode — primitives every promo/entrance render pass
  needs. The bundled ffmpeg 7.0.2-static binary is used as a standalone
  tool via subprocess (never linked) — the quarantine doctrine's
  standalone-tool pattern; the imageio-ffmpeg package itself is
  BSD-2-Clause.
- What was run (`wire_imageio_ffmpeg.py`):
  1. Resolved the binary via `imageio_ffmpeg.get_ffmpeg_exe()`
     (79,826,272 bytes, `ffmpeg version 7.0.2-static`).
  2. Encoded a 2 s 640x360@30fps `testsrc` pattern → `ffmpeg_test.mp4`
     (13,290 bytes, libx264 crf 30).
  3. Probed it via `ffmpeg -i` stderr parse: duration 2.00 s, 640x360,
     30 fps.
  4. Extracted the frame at t=1.0 s → `ffmpeg_frame.png` (40,218 bytes);
     PNG magic + IHDR verified by hand (struct unpack): 640x360.
  5. Downscale-transcoded 640x360 → 320x180 → `ffmpeg_test_360p.mp4`
     (9,107 bytes).
- Proof artifacts: `ffmpeg_test.mp4`, `ffmpeg_frame.png` (open it —
  real test pattern), `ffmpeg_test_360p.mp4`, `ffmpeg_probe.json`,
  `ff_report.txt`.
- One script bug found and fixed honestly: the first probe regex
  assumed ffmpeg 6's stream-line layout; ffmpeg 7 emits more fields —
  regex relaxed to `Video: [^\n]*?(\d{2,5}x\d{2,5})`, re-run green.
- Verdict: **PASS** — real encode/probe/extract/transcode, no stub.

## Quarantine compliance

GPL/AGPL tools are NEVER wired: both tools here are permissive
(MIT / BSD-2-Clause), verified from installed package metadata. No
quarantine-listed code was imported, linked, or executed. The ffmpeg
binary is a standalone subprocess tool, not a linked library.
