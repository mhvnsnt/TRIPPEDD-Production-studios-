# Wave 19 — Lane C notes (tools wiring + feasibility)

Date: 2026-10-07. Sandbox: `/home/hatch` (100 GB volume, 99% full).

## 1. Speaches Docker check — DEFERRED (no container runtime)
- Searched: `docker`, `podman`, `nerdctl`, `crictl` binaries — **none in PATH**;
  `/var/run/docker.sock` — **absent**.
- **Verdict: no container runtime exists in this sandbox.** Speaches (MIT,
  STT + diarization + TTS in one container) cannot be smoke-tested here.
- Not faking it: no proof artifact produced. Speaches stays on the
  "needs Docker" deferral list until a runtime is available (Wave N+1 or a
  Docker-capable runner). If a runtime appears, the test is:
  `docker run -p 8000:8000 ghcr.io/speaches-ai/speaches:latest` then hit
  `/v1/audio/transcriptions` with a tiny WAV.

## 2. VGMTrans / HivelyTracker reassessment
- **VGMTrans — DEFERRED again (Qt too heavy, still).**
  VGMTrans is a Qt5/Qt6 application (cmake + Qt dev libs required).
  Checked: `/usr/include/qt*` absent, `qmake`/`qmake6` absent,
  `ldconfig -p | grep qt6` empty. `cmake` alone is present but useless
  without Qt. Installing Qt dev libs = hundreds of MB to ~1 GB of apt
  packages; volume is 99% full (1.6 GB free). No real build path exists in
  this sandbox. Deferred honestly — same call as Wave 18.
- **HivelyTracker — WIRED via `hvl2wav` (this wave's win).**
  Wave 18's "no CLI" verdict was only half-right: HivelyTracker itself is a
  GUI tracker, but upstream
  [pete-gordon/hivelytracker](https://github.com/pete-gordon/hivelytracker)
  (BSD-3-Clause) ships `hvl2wav/`, a self-contained offline CLI that renders
  AHX/HVL modules to 16-bit WAV — **no GUI, no SDL, no Qt; gcc only**.
  - Built in this sandbox with `/usr/bin/gcc` from ~79 KB of verbatim source
    (warnings only, no errors) → `tools/music/hvl2wav/hvl2wav` (163 KB).
  - Real render proof (see `tools/music/hvl2wav/PROOF.md`): two upstream demo
    modules (`illuminated.hvl` 1.5 KB, `karma.ahx` 15.8 KB) rendered to valid
    stereo 44.1 kHz WAVs (57.6 s and 194.6 s, non-silent PCM, RMS ~18.8k).
  - Bundled: verbatim `src/`, one-step `BUILD.sh`, `README.md`,
    `demo/illuminated.hvl` for one-command reproduction.
  - Pairs with the Wave 18 `dumb_mod2wav` wiring (MOD/S3M/XM/IT); together
    the music lane now covers tracker formats end-to-end.
  - WAV outputs deliberately NOT committed (10–34 MB each); reproducible on demand.

## 3. Wired-tools spot-check (2 tools, both PASS)
- **`tools/captions/caption_qa.py`** — PASS. stdlib-only subtitle QC gate.
  - `proofs/caption_qa_defects.srt` → exit 1, 3 errors / 4 warnings (correct:
    deliberate-defects demo).
  - `proofs/caption_qa_clean.srt` → exit 0, 0 errors, 0 warnings.
- **`tools/captions/ttconv_tool.py`** — PASS via its documented isolated venv
  (`~/venvs/wave12-captions/bin/python`): `--demo` SRT→VTT→SRT roundtrip,
  "3 cue texts identical". System python lacks `ttconv` — venv is the
  supported path, unchanged from Wave 12.

## 4. god-molecule-studio — no Wave 19 changes
- `git status` clean; nothing in Wave 19's scope (Docker, VGMTrans,
  HivelyTracker, caption spot-checks) touches it. In sync, no action taken —
  same as the last several waves.

## Commit log (branch wave19-lane-c)
- hvl2wav wiring + PROOF.md
- docs/wave19/lane-c-notes.md (this file)
