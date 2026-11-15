# WIRING — OpenFaceFX 0.24.0 (FaceFX-style lip-sync curves)
**Status: WIRED+PROVEN — 2026-11-13**
**Upstream:** https://github.com/OpenFaceFX/OpenFaceFX — MIT, numpy-only.
**Install:** `pip install openfacefx` (PyPI, version 0.24.0 installed 2026-11-13)
into a venv at `~/workspace/tools/openfacefx/venv/` (system Python 3.12.3,
numpy is the only runtime dependency). No models, no downloads, no GPU.
**Proof files:** `~/workspace/tools/openfacefx/proof/` — `track-naive.json`,
`track-energy.json`, `track-from-rhubarb.json`.
**Source checkout (examples + docs):**
`~/workspace/_wizard-gang-wireup-20261113/phase4-outside-tools/work/offx-src/`
(clone of the repo, depth 1, for `examples/voice.wav`).

## Gap it fills
Rhubarb (already wired) gives stepped Preston-Blair mouth cues (A–H/X) from
audio. OpenFaceFX is the stage AFTER Rhubarb: it turns cues — or a transcript
+ WAV duration — into smooth 15-viseme (Oculus/Meta convention) animation
curves with Cohen–Massaro coarticulation, keyframed per channel, exported as
`openfacefx.track` JSON (and CSV). Its `from-cues` importer reads Rhubarb
tsv/xml/json, Moho .dat and Papagayo .pgo, so it slots directly onto the
existing Rhubarb pipeline instead of replacing it. It also has a `captions`
mode (SRT/WebVTT from the SAME alignment the lip curves use — captions and
lip-sync from one source, which matters for phone viewing) and an `mfa` mode
that consumes Montreal Forced Aligner TextGrids for production accuracy.

## Proof (run 2026-11-13, on the project's own examples/voice.wav, 1.60 s)
```
$ venv/bin/python -m openfacefx naive --text "hello world" --wav examples/voice.wav -o proof/track-naive.json
wrote proof/track-naive.json: 7 channels, 93 keyframes, 1.60s
$ venv/bin/python -m openfacefx energy --wav examples/voice.wav -o proof/track-energy.json
wrote proof/track-energy.json: 4 channels, 15 keyframes, 1.60s
$ # Rhubarb bridge (Tahoma2D-bundled Rhubarb 1.13.0):
$ rhubarb -r pocketSphinx -f json -o rhubarb-cues.json examples/voice.wav   # -> mouthCues JSON
$ venv/bin/python -m openfacefx from-cues --format json-cues -o proof/track-from-rhubarb.json rhubarb-cues.json
wrote proof/track-from-rhubarb.json: 3 channels, 18 keyframes, 1.60s
```
The naive output (7 channels / 93 keyframes / 1.60 s) matches the project's
own README quickstart figure exactly. CLI surface verified: naive, mfa,
from-timing, from-cues, captions, audit, from-csv, from-vmd, energy, studio,
convert, export-layers, batch, emotion and more (`--help` lists 26 commands).

## Corrections to the Oct 29 audit
- The audit called OpenFaceFX "alpha status (its own badge)", STORED-ONLY
  source. It is now 0.24.0 on PyPI with a full CLI and CI-verified Linux
  builds — installed and proven here, not alpha.
- The audit said it "exports OpenToonz `.dat`". The current version IMPORTS
  .dat (Moho .dat via from-cues) and exports JSON/CSV plus retargets
  (ARKit, CC4, VRM, Live2D, Spine, Godot). No .dat exporter was found in
  0.24.0 — do not claim one.

## Limits learned
- The `naive` aligner is approximate: it spreads the transcript's phonemes
  evenly across the WAV duration (no acoustic alignment). Production-accurate
  timing needs either the `mfa` path (Montreal Forced Aligner — evaluated
  separately in this lane) or Rhubarb cues via `from-cues` (proven above).
- The Rhubarb cues on the demo voice were coarse (one long G cue) — that is
  PocketSphinx recognition on that clip, not an OpenFaceFX defect; with real
  WG dialogue lines the cue stream will be richer.
- The `studio` subcommand is a web workspace (serves locally, opens a
  browser) — not headless-proven here; the CLI pipeline is the proven part.
