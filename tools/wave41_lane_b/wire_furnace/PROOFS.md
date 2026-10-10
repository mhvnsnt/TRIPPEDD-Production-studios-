# PROOFS.md — Furnace wire (Wave 41 Lane B)

Quarantine rows 122 + 271 — **Furnace** (tildearrow/furnace), GPL-2.0-or-later,
re-verified in cycle 12. The wire exercises Furnace ONLY as a standalone tool
(permitted standalone tool use / research only — never linked or imported into
shipping paths). The quarantined binary itself is never committed to git: it
is downloaded to a local cache dir at run time (`~/.cache/furnace_wire` or
`$FURNACE_WIRE_CACHE`).

## What was run

`python3 wire_furnace.py` (2026-10-08, from a clean cache):

1. Downloaded official upstream release `furnace-0.6.8.3-linux-x86_64.tar.gz`
   (37,610,122 bytes) from `github.com/tildearrow/furnace/releases/tag/v0.6.8.3`.
2. Extracted; `furnace -version` → exit 0 (binary identity confirmed).
3. Headless-rendered the upstream demo song `demos/blank/Exquisite Invitation.fur`
   (882 bytes, deterministic upstream fixture) via
   `furnace -loglevel error -console -output proof_render.wav "Exquisite Invitation.fur"`
   → exit 0.

## Proof artifact

`proof_render.wav` — 10,164,220 bytes, verified header parse:

- RIFF / WAVE, Microsoft PCM, 16 bit, stereo, 44100 Hz
- data chunk: 10,164,176 bytes → **57.62 s** of rendered audio
- content check: peak |sample| = 25,877, RMS = 6,451.1 over first 2M samples —
  **real non-silent rendered audio**, not a stub or zero-filled file

## Files

| file | role |
|---|---|
| `wire_furnace.py` | the wire (re-runnable; downloads binary to cache, renders, validates, writes manifest) |
| `Exquisite Invitation.fur` | upstream demo-song fixture (882 bytes, input only) |
| `proof_render.wav` | headless-rendered proof artifact (57.62 s stereo WAV) |
| `proof_manifest.json` | machine-readable proof record (WAV header facts, rc codes, SHA-256) |
| `SHA256SUMS` | checksums of the committed artifacts |
| `PROOFS.md` | this file |

Verify: `sha256sum -c SHA256SUMS`

## Honest notes

- The export prints a console progress bar and one harmless ALSA warning
  (`open /dev/snd/seq failed` — no MIDI hardware in this environment; the
  render path does not use MIDI). Neither affects the artifact.
- The rendered song is the upstream demo, not project audio; the proof is that
  the quarantined tool executes correctly headless and produces valid output.
- License facts for the wired tool were re-verified in cycle 12 (row 122):
  GPL-2.0-or-later via README footnotes; upstream live, not archived.
