# Wave 39 Lane B — PD SFX dataset ingestion proofs

Ingested pack: **The Essential Retro Video Game Sound Effects Collection [512 sounds]**
Source: <https://opengameart.org/content/512-sound-effects-8-bit-style>
License: **CC0-1.0** (public domain dedication) — claimed on the OGA pack page, re-fetched fresh 2026-10-08.

## Run
`python3 tools/wave39_lane_b/wire_pd_sfx_ingest.py`

## Results
| Check | Result |
|---|---|
| OGA page license claim | ✅ CC0 confirmed on page (HTTP 200) |
| Pack download | ✅ 20582855 bytes |
| Extraction | ✅ 512 WAV files |
| ffprobe catalog | ✅ 512/512 probed; total 306.4 s |
| Sample-rate mix | 44100Hz/1ch x512 |
| SHA256SUMS | ✅ 512/512 verified on read-back |

## Artifacts
- `dataset_manifest.json` — per-file sha256, bytes, duration, sample rate, channels
- `SHA256SUMS` — verifiable checksums for the whole dataset
- `wav/` — the ingested CC0 WAV files

Quarantine framing: CC0/public-domain content only; nothing GPL/AGPL involved.
No fetch failures this run.
