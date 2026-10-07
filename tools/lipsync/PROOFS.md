# PROOFS — rhubarb-lip-sync

Date: 2026-10-07. Rhubarb Lip Sync 1.14.0 (GPL-3.0 — standalone CLI tool,
never linked into shipping code; see program docs/LICENSE_QUARANTINE.md).

## Install

- Release: `Rhubarb-Lip-Sync-1.14.0-Linux.zip`
  (DanielSWolf/rhubarb-lip-sync, v1.14.0)
- Staged: `tools/lipsync/bin/rhubarb` (`chmod +x`) + `tools/lipsync/bin/res/`
  (required Sphinx acoustic-model data — the binary needs it alongside).
- Version check: `./bin/rhubarb --version` → `Rhubarb Lip Sync version 1.14.0`.

## Smoke test

Input: 3.05s of real Piper TTS speech
("The council does not explain itself. It declares.",
`proofs/rhubarb_speech_3s.wav`, copied from the piper smoke test).

    ./bin/rhubarb -f tsv -o proofs/rhubarb_test.tsv proofs/rhubarb_speech_3s.wav

Result: `proofs/rhubarb_test.tsv` — 25 mouth-cue rows spanning 0.00–3.05s,
shapes A B C D E G H + X (rest), e.g.:

    0.00    X
    0.20    B
    0.24    C
    ...
    2.90    X
    3.05    X

(An earlier run on a 3s sine tone also completed, outputting X/rest
throughout — expected for non-speech; the speech run above is the
meaningful proof.)

## Hashes (sha256)

- `proofs/rhubarb_test.tsv`: `16ada20d9f881b40900cc7779d238bd49f3acbd7b43b730dc1879b80c48d6bfa`
- `proofs/rhubarb_speech_3s.wav`: `517caf9ec6e08a60c61a9ea71ae283e7ba67a598e29f253e014b7c1093a679cd`
