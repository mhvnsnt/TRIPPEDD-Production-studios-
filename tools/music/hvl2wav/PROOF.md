# PROOF — hvl2wav wiring (Wave 19, Lane C, 2026-10-07)

## Build
- Source: `src/` = verbatim `hvl2wav/` dir from pete-gordon/hivelytracker
  (master @ build time, commit f393ca7; files: hvl2wav.c, replay.c,
  replay.h, types.h, makefile, hvl2wav.1 — total ~79 KB fetched from
  raw.githubusercontent.com).
- Toolchain: `/usr/bin/gcc`, `/usr/bin/make` (pre-installed). Only the
  `-Wall -O3 -lm` flags the upstream makefile asks for.
- Warnings only (strncpy truncation in replay.c) — no errors.
- Output: `hvl2wav` binary, 163,192 bytes, ELF x86_64.
- Rebuild is one step: `./BUILD.sh` (verified it reproduces the binary).

## Real render runs (this sandbox, not simulated)
| Input (from upstream Songs/) | Size | Render | WAV out | Duration | Peak | RMS |
|---|---|---|---|---|---|---|
| `illuminated.hvl` | 1,499 B | `./hvl2wav -oilluminated.wav illuminated.hvl` → "ALL DONE!" | 44.1 kHz stereo 16-bit | 57.6 s | 32768 | 18805 |
| `karma.ahx` | 15,788 B | `./hvl2wav -okarma.wav -f44100 karma.ahx` → "ALL DONE!" | 44.1 kHz stereo 16-bit | 194.6 s | 32768 | 18884 |

Verified with Python `wave`: valid RIFF/WAVE headers, non-silent PCM
(RMS ~18.8k, full-scale peaks) — actual chiptune audio, not empty buffers.
WAV outputs were NOT committed (they'd be ~10/34 MB); the renders are
reproducible with the bundled `demo/illuminated.hvl`:
`./hvl2wav -o/tmp/x.wav demo/illuminated.hvl`.

## License
BSD-3-Clause (pete-gordon/hivelytracker LICENSE) — safe for the stack.
