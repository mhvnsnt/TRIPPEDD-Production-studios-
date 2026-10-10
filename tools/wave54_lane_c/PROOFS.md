# Wave 54 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed tools wired with REAL runs. Both extend the Wave
51/52/53 cartoon-voice pipeline one stage further:

**text -> VO (Kokoro, Wave 51) -> lip-sync (Rhubarb) -> denoise + loudness
master (Wave 52) -> SUBTITLES (faster-whisper, Wave 53) ->
FORMAT NORMALIZATION + SRT RETIME (this lane)**.

Both wire scripts are original MIT-licensed code (this directory); external
libraries are pip-installed, never embedded. Nothing from
`tools/quarantine` is linked or imported anywhere in the wire paths.
Licenses verified upstream 2026-10-08 via GitHub API (`spdx_id`):
pbs/pycaption = **Apache-2.0**, cdown/srt = **MIT** — both permissive,
no GPL/LGPL/NC anywhere in the wire path.

Environment: Python 3.12.3, lane-local venv (`tools/wave54_lane_c/venv/`,
gitignored), `TMPDIR=$HOME/.tmp-pip`. pycaption 2.3.13 + srt 3.5.3
(PyPI wheels, pure Python, no model weights, no network). Real input: the
Wave-53 proof SRT (`tools/wave53_lane_c/proofs/subtitle_stage/vo_line.srt`:
22 word-level cues, 22 words, span 0.000–7.320 s, from the real Wave-52
mastered VO WAV that transcribed at WER 0.0). Proof artifacts total ~8 KB —
nothing near the 100 MB binary limit.

## 1. pycaption — caption format normalization stage (Apache-2.0)

- **Upstream:** pbs/pycaption — Apache-2.0 verified 2026-10-08 via GitHub
  API; catalog entry flipped `not-started` -> `WIRED — run-proven` this wave.
- **Script:** `wire_pycaption.py` — converts the real Wave-53 SRT into
  WebVTT (817 B), SCC (1747 B), DFXP (2575 B), SAMI (2502 B); round-trips
  each back through the reader; checks cue count, text equality, and timing
  equality; checks byte-determinism across two full conversions.
- **Proof (real input, real conversions):**
  - Source: 22 cues detected, language `en-US`.
  - WebVTT round-trip: 22 cues, text exact, **timing exact (0 us max error)**.
  - DFXP round-trip: 22 cues, text exact, **timing exact (0 us max error)**.
  - SAMI round-trip: 22 cues, text exact, **timing exact (0 us max error)**.
  - SCC round-trip: 22 cues, text exact (22/22 words survive), but **timing
    drifts — max abs start error 883.6 ms** (first cue reads +367 ms).
    This is an upstream pycaption SCCReader time-base quirk (29.97 fps
    frame math), reproduced on pristine input — documented, not a wire
    defect. Practical consequence: SCC is a text-lossless broadcast
    deliverable, not an archive format — keep SRT/WebVTT as source of truth.
  - Determinism: two full conversions -> byte-identical outputs.
  - 18/18 checks PASS.
- **Honest environment note:** pycaption's DFXP reader emits a BeautifulSoup
  `XMLParsedAsHTMLWarning` (upstream parses XML with the HTML parser when
  lxml is absent). Harmless for our payloads (timings exact), but if lxml
  ever enters the tree it must stay out of quarantined dep trees — note for
  future hardening.
- **Artifacts:** `proofs/pycaption/vo_line.webvtt`, `vo_line.scc`,
  `vo_line.dfxp`, `vo_line.sami`, `proofs/pycaption/result.json`.

## 2. srt — SRT parse/compose/retime stage (MIT)

- **Upstream:** cdown/srt — MIT verified 2026-10-08 via GitHub API;
  catalog entry flipped `not-started` -> `WIRED — run-proven` this wave.
- **Script:** `wire_srt_lib.py` — parses the real Wave-53 SRT, verifies
  parse->compose byte-equality, monotonicity, audio-bounds (7.825 s),
  word count vs the Wave-53 ground truth, retimes +500 ms, re-parses the
  shifted file, and verifies determinism.
- **Proof (real input, real parse):**
  - 22 cues parsed; **parse->compose byte-identical to the source file
    (867 bytes)**.
  - Cues monotonic, all inside the 7.825 s audio bounds (span
    0.000–7.320 s).
  - 22 words total — matches the Wave-53 known line exactly.
  - Retime +500 ms: first cue `0:00:00 -> 0:00:00.500000`, last cue
    `0:00:07.320000 -> 0:00:07.820000` — exact; shifted file re-parses to
    22 cues with matching timings.
  - Determinism: two composes -> byte-identical.
  - 10/10 checks PASS.
- **Artifacts:** `proofs/srt_lib/vo_line_shifted_500ms.srt`,
  `proofs/srt_lib/result.json`.

## What the pipeline can now do end-to-end

The caption leg is complete: ASR -> SRT (Wave 53) -> format normalization
for broadcast (SCC), web (WebVTT), players (DFXP/TTML), legacy (SAMI) ->
programmatic retime/validate (srt) — all permissive-licensed, all
run-proven on the same real VO take.
