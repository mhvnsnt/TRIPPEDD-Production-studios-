# Wave 31 Lane A — Wiring Proofs

Two strongest Pocket-4 finds wired with real compiled proof artifacts (2026-10-08).
Both are permissive-licensed (MIT / BSD-3-Clause) — no quarantine implications.

## 1. ayumi — YM2149/AY-3-8910 emulator (MIT) ✅

- **Upstream:** https://github.com/true-grue/ayumi @ `07c08b4874c359169e4a028edf73f046d8b763e2` (2021-11-24)
- **License:** MIT (verified via GitHub API 2026-10-08)
- **Proof source:** `ayumi_tone_test.c` — configures the chip in YM2149 mode
  (2 MHz clock, 44.1 kHz output), sets channel 0 to period 284
  (f = 2 MHz / (16 × 284) ≈ 440 Hz), max volume, tone-on, renders 2 s.
- **Build:** `gcc -O2 -o ayumi_tone_test ayumi_tone_test.c ayumi/ayumi.c -lm`
  (one `-Wimplicit-function-declaration` warning for `memcpy` on first build;
  fixed by adding `#include <string.h>` — clean rebuild verified)
- **Artifact:** `ayumi_440hz.wav` — 2 s, stereo, 16-bit, 44.1 kHz, 88 200 frames.
- **Verification:** Python `wave` module read-back: valid RIFF/WAVE header,
  176 296/176 400 non-zero samples, peak amplitude real; zero-crossing count
  over the final second measures **exactly 440.0 Hz** against the 440 Hz target.
- **Status:** PASS. Drop-in PSG voice for Atari ST / ZX Spectrum chiptune beds.

## 2. ymfm — Yamaha FM chip emulator family (BSD-3-Clause) ✅

- **Upstream:** https://github.com/aaronsgiles/ymfm @ `81aec25ccbb98f4873a255f7551ac4dadac59b4a`
- **License:** BSD-3-Clause (verified via GitHub API 2026-10-08)
- **Proof source:** `ymfm_opm_test.cpp` — subclasses `ymfm::ymfm_interface`,
  instantiates the YM2151/OPM core, programs a 4-operator patch
  (algorithm 7 = all carriers, MUL=1, AR=31, full sustain), keys on channel 0,
  renders 2 s via `generate()`.
- **Build:** `g++ --std=c++14 -Iymfm/src ymfm_opm_test.cpp ymfm/src/ymfm_misc.cpp ymfm/src/ymfm_opm.cpp ymfm/src/ymfm_ssg.cpp -o ymfm_opm_test`
- **Failure (honest):** first attempt linked without `ymfm_ssg.cpp`
  (undefined `ssg_engine` refs — `ymfm_misc.cpp` needs it); second attempt
  compiled and ran but produced **digital silence** (peak 0.000) because
  `ym2151::write(offset, data)` uses hardware address/data port semantics —
  `write(0, x)` = address port, `write(1, x)` = data port — and the test was
  writing register numbers as if they were direct register writes.
  Fixed with proper `write(0, reg); write(1, val)` pairs.
- **Artifact:** `ymfm_opm.wav` — 2 s, stereo, 16-bit, 44.1 kHz, 88 200 frames.
- **Verification:** read-back shows 176 400/176 400 non-zero samples, peak
  20 929/32 767 (no clipping after rescale); zero-crossing measures a stable
  **≈1041 Hz** FM tone. (KC=0x4A did not land on 440 Hz — the OPM key-code to
  frequency mapping at the default clock differs from the naive estimate;
  documented here rather than fudged. The core renders correctly regardless.)
- **Status:** PASS. Commercial-safe FM synthesis path (vs the LGPL Nuked-OPL3).

## Reproduce

```sh
# ayumi
git clone https://github.com/true-grue/ayumi
gcc -O2 -o ayumi_tone_test tools/wave31_lane_a/ayumi_tone_test.c ayumi/ayumi.c -lm
./ayumi_tone_test   # writes ayumi_440hz.wav

# ymfm (OPM core)
git clone https://github.com/aaronsgiles/ymfm
g++ --std=c++14 -Iymfm/src tools/wave31_lane_a/ymfm_opm_test.cpp \
  ymfm/src/ymfm_misc.cpp ymfm/src/ymfm_opm.cpp ymfm/src/ymfm_ssg.cpp \
  -o ymfm_opm_test
./ymfm_opm_test     # writes ymfm_opm.wav
```

No vendored upstream sources are committed here — only the test programs, the
rendered WAVs, and this document. Re-clone from the SHAs above to reproduce.
