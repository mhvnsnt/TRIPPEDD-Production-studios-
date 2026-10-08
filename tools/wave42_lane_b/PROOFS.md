# PROOFS.md — Wave 42 Lane B tool wiring

Two production-relevant tools, both permissively licensed, both exercised
against their REAL APIs with REAL proof artifacts. No stubs, no mocks.
Neither tool is in the LICENSE_QUARANTINE (both MIT — commercial-safe).
Quarantined code was never linked, imported, or wired.

Run environment: `/home/hatch/.cache/w42b_venv` (Python 3.12 venv;
webrtcvad 2.0.10, pysubs2 1.9.0, numpy 2.5.3, setuptools<81 for webrtcvad's
pkg_resources import). Re-run:
`/home/hatch/.cache/w42b_venv/bin/python wire_webrtcvad.py`
`/home/hatch/.cache/w42b_venv/bin/python wire_pysubs2.py`

## 1. webrtcvad (MIT) — voice activity detection

- Upstream: github.com/wiseman/py-webrtcvad (Google WebRTC VAD wrapper)
- Production relevance: speech/silence segmentation for the captions and
  voice pipelines (`tools/captions`, `tools/video_pipeline/auto_caption.py`,
  `voiceover.py`) — finding speech regions before ASR, trimming dead air.
- What was run (`wire_webrtcvad.py`):
  1. Synthesized a deterministic 7 s fixture WAV (`fixture_vad.wav`):
     16 kHz mono 16-bit PCM — 1 s silence, 2 s speech-like signal (harmonic
     stack + 4 Hz syllabic AM + noise), 1 s silence, 2 s speech-like, 1 s silence.
  2. Ran `webrtcvad.Vad(aggressiveness=2).is_speech()` over 30 ms frames
     (233 frames), merged voiced runs into segments (3-frame bridging).
- Proof artifacts:
  - `fixture_vad.wav` — 224,044 bytes; verified parse: 1 ch, 16-bit,
    16000 Hz, 112,000 frames = 7.00 s, peak |sample| = 15,000 (real signal).
  - `vad_frames.txt` — 233-char voiced/unvoiced decision string.
  - `vad_segments.json` — detected segments (0.99–3.09 s) and (3.99–6.12 s)
    vs ground truth (1.0–3.0 s) and (4.0–6.0 s): 2/2 matched, verdict PASS.
  - `vad_report.txt` — human-readable summary.
- Verdict: **PASS** — real VAD decisions on real audio, no stub.

## 2. pysubs2 (MIT) — subtitle parse / shift / convert

- Upstream: github.com/tkarabela/pysubs2
- Production relevance: the captions pipeline (`tools/captions`,
  `tools/video_pipeline/auto_caption.py`) — retiming, format conversion
  SRT ↔ ASS ↔ VTT for episode deliverables.
- What was run (`wire_pysubs2.py`):
  1. Wrote deterministic 5-cue fixture (`fixture.srt`).
  2. Loaded via `pysubs2.load`, shifted all cues +2500 ms (`subs.shift`),
     saved `shifted.srt`.
  3. Converted to ASS (`converted.ass`) and WebVTT (`converted.vtt`).
  4. Re-loaded all three outputs; asserted cue count, exact start times
     (+2500 ms), and exact text round-trip. Also exercised the SSAFile API
     (`make_time` ms math: 90.25 s → 90250 ms, 1:32.75 → 92750 ms).
- Proof artifacts:
  - `fixture.srt`, `shifted.srt` (first cue now `00:00:03,500 --> 00:00:06,000`),
    `converted.ass`, `converted.vtt` — all re-parse to 5 cues, starts and
    texts byte-exact.
  - `subs_report.json` — per-format round-trip checks, all true, verdict PASS.
- Verdict: **PASS** — real parse/shift/convert round trips, no stub.

## Cycle-13 re-verification evidence (same directory)

- `cycle13_verify.py` — upstream fetch script used for the cycle-13 checks
  (GitHub API + Codeberg API + raw license-file fetches).
- `cycle13_results.json` — raw per-row fetch results (HTTP status, archived
  flags, spdx ids, pushed_at, license markers) backing the row stamps in
  `docs/LICENSE_QUARANTINE.md`.

## SHA256SUMS

All proof artifacts are checksummed in `SHA256SUMS` (verify with
`sha256sum -c SHA256SUMS`). Largest artifact: `fixture_vad.wav` (224 KB) —
well under the 100 MB binary limit; no binaries in git beyond this WAV.
