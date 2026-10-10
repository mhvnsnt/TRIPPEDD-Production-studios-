# PROOFS.md — normalize_pack (Wave 12 Lane A wire-up)

## What this tool is
`normalize_pack.py` — takes any downloaded SFX pack directory (Kenney CC0
packs, 99Sounds bundles, etc.) and produces a standardized `manifest.json`:
per-file SHA-256, byte size, and audio stats. WAV files get full stats
(duration, sample rate, channels, bit depth, peak dBFS); formats the stdlib
cannot decode (.ogg/.mp3/.flac) get name + size + SHA-256 and are flagged
`basic-only` in the manifest — honestly, never faked.

## Proof of run (2026-10-07, this VM)
Command:
`python3 normalize_pack.py --packdir ../kenney-interface-sounds --out kenney_interface_manifest.json`
→ exit 0, no warnings

- 100 audio files scanned from the repo's existing Kenney Interface Sounds
  pack (pulled by an earlier wave; CC0, real .ogg files)
- 960,599 bytes total across the pack
- All 100 entries carry full SHA-256 hashes; all 100 are .ogg, so all 100
  are correctly flagged `basic-only (stdlib cannot decode this format)`
  with zero fabricated audio stats
- Sample entries:
  - back_001.ogg — 6,997 bytes — sha256 07db973f79f6ae0f…
  - back_002.ogg — 7,029 bytes — sha256 61581c58194e3f19…
  - back_003.ogg — 7,208 bytes — sha256 ff5e87de1230b1a5…

## Honest notes
- This tool does not download anything — pack acquisition stays a manual /
  browser-side step (keeps the donation interstitial and ToS in front of a
  human). It only normalizes what is already on disk.
- To exercise the WAV-stats path, point it at `../cartoon_sfx_kit/out/`.
