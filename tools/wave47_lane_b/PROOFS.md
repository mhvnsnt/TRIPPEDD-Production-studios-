# Wave 47 Lane B — Tool Wires (permissive licenses) — PROOFS.md

**Date:** 2026-10-08 · **Branch:** `wave47-lane-b` · **Lane:** B
**Rules:** standalone-binary tool use only — never linked/imported into shipping
paths. Licenses verified from upstream sources, never assumed.

---

## Wire 1 — stb_image + stb_image_write (public domain) ✅ PASS

- **Upstream:** https://github.com/nothings/stb — single-file image loader/encoder.
- **License verified 2026-10-08:** `stb_image.h` v2.30 header reads "public domain
  image loader"; GitHub API spdx_id on nothings/stb = MIT (dual MIT/public-domain
  licensing). Vendored headers in `vendor/` (downloaded 2026-10-08 from master).
- **Script:** `wire_stb_image.py`
- **What was run:** generated a deterministic 256×128 RGB test PNG (Pillow:
  gradient + checker + red diagonal) → compiled `test_img.c` (gcc, includes
  `stb_image.h` + `stb_image_write.h`) → `stbi_load()` the PNG (reported
  `w=256 h=128 channels_in=3`) → `stbi_write_bmp()` wrote `decoded.bmp` →
  Pillow re-opened the BMP and byte-compared all 98,304 pixel bytes against
  the source PNG → **identical**. The C program also wrote a raw P6 PPM whose
  pixel payload was likewise verified byte-identical.
- **Proof artifacts** (`proofs_stb_image/`): `fixture.png` (2,219 B, source),
  `decoded.bmp` (98,358 B — real converted file), `decoded.ppm` (98,319 B),
  `c_output.txt` (C program stdout).
- **Honest failures:** none — first run PASS.

## Wire 2 — miniaudio (public domain OR MIT-0) ✅ PASS

- **Upstream:** https://github.com/mackron/miniaudio — single-file audio
  decode/encode/playback library.
- **License verified 2026-10-08:** `miniaudio.h` v0.11.25 header reads "Choice
  of public domain or MIT-0. See license statements at the end of this file."
  Vendored header in `vendor/` (downloaded 2026-10-08 from master).
- **Script:** `wire_miniaudio.py`
- **What was run:** generated a deterministic 1.0 s 440 Hz sine WAV (44,100 Hz,
  16-bit mono, 44,100 frames) with stdlib `wave` → compiled `test_audio.c`
  (gcc + `-lm -lpthread -ldl`) → `ma_decoder_init_file()` on `fixture.wav`
  (reported `frames=44100 channels=1 rate=44100 format=2/s16`) → read all PCM
  frames to `raw_decoded.pcm` → `ma_encoder_init_file()` WAV wrote those frames
  to `reencoded.wav` → re-decoded and **byte-compared PCM: MATCH**. Python
  re-verified `raw_decoded.pcm` (88,200 bytes) byte-identical to the fixture's
  sample data.
- **Proof artifacts** (`proofs_miniaudio/`): `fixture.wav` (88,244 B, source),
  `raw_decoded.pcm` (88,200 B), `reencoded.wav` (88,244 B — real converted
  file, SHA-256 identical to fixture), `c_output.txt` (C program stdout).
- **Honest failure logged:** first run failed at encoder init — `ma_encoder_init_file`
  was called with `(encoder, path, config)` but the 0.11.x API order is
  `(path, config, encoder)` (compiler warnings in the debug pass revealed it).
  Fixed, rerun PASS.

---

## Verification summary

| Wire | License | Proof | Result |
|---|---|---|---|
| stb_image / stb_image_write | Public domain (MIT dual) | PNG → BMP lossless round trip, pixels byte-identical | ✅ PASS |
| miniaudio | Public domain OR MIT-0 | WAV decode → PCM; encode → WAV → decode, PCM MATCH | ✅ PASS |

SHA256SUMS: all 8 proof files, verified OK at commit time.
