# Wave 51 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed audio tools wired with REAL runs, forming an
end-to-end cartoon-voice pipeline: **text -> neural VO (Kokoro) -> lip-sync
mouth timings (Rhubarb)**. Both wire scripts are original MIT-licensed code
(this directory); external binaries/models are invoked, never embedded.

Environment: Python 3.12.3, torch 2.14.1+cpu, kokoro 0.9.4 (pip),
soundfile 0.14.0, ffmpeg 8.1.2 / ffprobe, system espeak-ng (G2P subprocess
only). Lane-local venv in this directory; model weights
(hexgrad/Kokoro-82M, already in the HF cache) are gitignored and NOT
committed — never commit anything >100MB. Network used only for the initial
rhubarb binary download (GitHub release) and spacy en-core-web-sm G2P dep.

## 1. Kokoro (Kokoro-82M) — neural character TTS
- **Upstream:** hexgrad/kokoro — model weights Apache-2.0 (verified via HF
  model card frontmatter 'license: apache-2.0', consistent with the catalog
  entry). espeak-ng is invoked only as a G2P subprocess (not linked).
- **License:** Apache-2.0 (upstream). Wire script MIT.
- **Script:** `wire_kokoro_tts.py` — synthesizes an ORIGINAL VO line with
  voice `af_heart`, writes 24 kHz mono WAV, verifies with ffprobe +
  stdlib wave ground truth + ffmpeg loudnorm measurement + seeded
  reproducibility check.
- **Proof (network for model/binary only; synthesis fully local):**
  - Line (original, no copyrighted text): "Ladies and gentlemen, the
    streets are watching tonight. Two fighters step into the alley, and only
    one walks out with the crown."
  - Synthesis: 7.825 s, 24000 Hz, 1 ch, pcm_s16le, 187,800 frames,
    375,644 bytes. ffprobe duration agrees to the millisecond.
  - Signal: RMS 0.0511, peak 0.52 (no clipping), DC offset ~0 (no blowout),
    per-octile RMS 0.059/0.046/0.050/0.034/0.051/0.053/0.077/0.021 with 28%
    near-silent frames = real spoken prosody with natural pauses.
  - Loudness (ffmpeg loudnorm): integrated **-25.21 LUFS**, true peak
    **-5.68 dBFS**, LRA 2.20 — measurable broadcast-style stats for the
    mastering lane.
  - Perf: pipeline load 7.35 s (cached), synthesis 15.75 s for 7.8 s audio
    (~2x real-time on 2 vCPU).
  - HONEST stochasticity finding: Kokoro's generator is stochastic by
    design — an unseeded third pass differs (max|diff| = 0.092, earlier run
    0.252). With `torch.manual_seed(0)` pinned, two passes are byte-exact
    (max|diff| = 0.0). The committed WAV is the seeded, reproducible render.
    Production rule: pin a seed for deterministic VO takes; treat unseeded
    takes as new performances.
  - All 9 checks → **PASS**
- **Artifacts:** `proofs/kokoro_tts/voice_line.wav` (0.38 MB),
  `proofs/kokoro_tts/result.json`

## 2. Rhubarb Lip Sync — WAV -> mouth-shape timings
- **Upstream:** DanielSWolf/rhubarb-lip-sync v1.14.0 — MIT, verified from
  upstream LICENSE.md (2026-10-08): "Rhubarb Lip Sync is released under the
  MIT license"; all third-party deps MIT/BSD/Boost-permissive. Upstream
  license terms: the generated lip-sync data belongs to the user. Binary
  invoked as an external process (with its `res/` folder next to it per
  upstream docs), never embedded.
- **License:** MIT (upstream). Wire script MIT.
- **Script:** `wire_rhubarb_lipsync.py` — runs rhubarb (tsv, PocketSphinx
  recognizer, dialog file, extended shapes GHX) on the REAL Kokoro WAV and
  validates the TSV: >= 5 events, shapes in {A..H, X}, monotonic timestamps
  within audio duration, first event < 1.5 s, speech coverage > 50%, and
  run-twice byte-identical determinism.
- **Proof (no network at run time):**
  - Input: the real Kokoro `voice_line.wav` (7.825 s) + matching dialog.txt.
  - Output: **47 mouth-shape events**, all 9 shapes used (A B C D E F G H X),
    first event @ 0.00 s, last ends 7.83 s (= audio end), speech coverage
    **0.81**, timestamps monotonic and within duration.
  - Determinism: two runs byte-identical TSV (sha256
    `79204bea7ff567829da2c92f3a522926612ccb3eb2028799a738319d375a539c`).
  - TSV sample (time, shape): `0.00 X / 0.33 H / 0.43 C / 0.50 B ...`
  - All 11 checks → **PASS**
- **Artifacts:** `proofs/rhubarb_lipsync/mouth_shapes_run1.tsv`,
  `proofs/rhubarb_lipsync/mouth_shapes_run2.tsv`, `proofs/rhubarb_lipsync/dialog.txt`,
  `proofs/rhubarb_lipsync/result.json`

## Honest failure log
- First Kokoro run: loudnorm JSON parsing failed — `-v quiet` suppresses
  loudnorm's own stderr JSON. Fixed by dropping `-v quiet` (used
  `-hide_banner`). Documented, not hidden.
- First Rhubarb run: parser assumed 3-column TSV; Rhubarb's TSV is
  2-column (time, shape) change-points. Fixed parser (end time = next row's
  time). 0-event run recorded, then corrected — proof chain re-run clean.
- pip: `--no-build-isolation` failed (venv lacks setuptools build backend);
  fixed with setuptools+wheel in venv.
- pip: default PyPI torch pulled the ~2.5 GB CUDA build; killed at 95% disk
  and reinstalled torch from the CPU index (~200 MB). Disk-health call,
  documented.
- Kokoro initial determinism check failed honestly (max|diff| 0.252):
  generator is stochastic; the script now pins a seed and records the
  finding instead of faking a PASS.
