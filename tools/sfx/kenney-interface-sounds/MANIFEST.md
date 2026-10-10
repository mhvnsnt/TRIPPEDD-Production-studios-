# Kenney — Interface Sounds (WIRED 2026-10-07, Wave 5 A1)

## Source
- Pack page: https://kenney.nl/assets/interface-sounds
- Zip: https://kenney.nl/media/pages/assets/interface-sounds/fa43c1dd4d-1677589452/kenney_interface-sounds.zip
- Zip SHA-256 (first 16): f2193d072726d675
- Pack version: Interface Sounds 1.0 (created 11-02-2020 per License.txt)

## License
- CC0 1.0 Universal — verified via the pack's own `LICENSE.txt` (copied here from inside the zip): "This content is free to use in personal, educational and commercial projects. Support us by crediting Kenney or www.kenney.nl (this is not mandatory)"
- Commercial-safe: YES. No attribution required (credited here anyway).

## Contents
- 100 `.ogg` files in `Audio/` (this directory): UI categories — back, bong, click, close, confirmation, drop, error, glass, glitch, maximize, minimize, open, pluck, question, scratch, scroll, select, switch, tick, toggle (numbered variants).

## Smoke test (2026-10-07, ffprobe + ffmpeg volumedetect)
| File | Duration (s) | max_volume | Verdict |
|---|---|---|---|
| click_001.ogg | 0.100023 | -1.4 dB | decodes, non-silent ✅ |
| confirmation_002.ogg | 0.539002 | -1.0 dB | decodes, non-silent ✅ |
| error_001.ogg | 0.164558 | -0.8 dB | decodes, non-silent ✅ |

Catalog entry: `docs/RESOURCE_CATALOG_WAVE5_A1.md` → "Kenney — Interface Sounds".
