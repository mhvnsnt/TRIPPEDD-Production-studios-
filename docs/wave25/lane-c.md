# Wave 25 Lane C — tool wiring + smoke tests (2026-10-07)

**Branch:** `wave25-lane-c` (cut from main; pushed at end of lane).
**Mandate:** wire 2–3 strongest tools from Lane A's 31 new catalog entries with REAL proof artifacts.

## Tools wired

### 1. PD 78rpm puller — `tools/music/wave25_laneC_pd78_pull.py`
Wires Lane A's **Pocket 4 PD-label deep-dives** (DAHR Columbia/OKeh/Brunswick/Decca/
Berliner/Zonophone entries). DAHR itself has **no public JSON API** (server-rendered
CodeIgniter PHP; 403s non-browser UAs), so the wireup goes through the Internet
Archive's official metadata API against the **Great 78 collection** (`collection:georgeblood`,
187,021 audio items) — the same corpus class.

- Pulls Great 78 audio metadata via `archive.org/advancedsearch.php`, parses recording
  year client-side, keeps only **pre-1923** items (PD per MMA, conservative through-1925 slice).
- Writes `pd78_manifest.json` + `pd78_items.csv`.
- Smoke test: downloaded one PD track ("Hosanna In The Highest — Haydn Quartette", 1898,
  2,752,595 bytes), SHA-256 `7211a4acc98354d8…`, ffprobe duration 107.77 s, **binary deleted**.

Proofs: `tools/music/evidence_wave25_laneC/pd78/pd78_manifest.json`,
`tools/music/evidence_wave25_laneC/pd78/pd78_items.csv` (300 rows scanned, 300 PD items, 0 unparseable dates).

### 2. Clean-majority netlabel puller — `tools/music/wave25_laneC_clean_netlabels.py`
Wires Lane A's **Pocket 1** 4 clean-majority survivors:
`happy-new-year-recordings` (5/5), `kusoj` (8/12), `marly-records` (2/2), `383records` (3/4).

- Per-item `licenseurl` re-check against clean definition (CC0-1.0 / PDM-1.0 / plain
  CC-BY 4.0/3.0/2.5 + legacy CC public-domain-dedication URL); BY-NC*/BY-SA/BY-ND excluded.
- Writes `clean_netlabels_manifest.json` with per-item clean download URLs + skip detail.
- Smoke test: downloaded one clean track from kusoj (CC-BY-3.0, 4,643,563 bytes),
  SHA-256 `4f0657ec4ed160d3…`, ffprobe duration 290.09 s, **binary deleted**.

Proof: `tools/music/evidence_wave25_laneC/clean_netlabels/clean_netlabels_manifest.json`
(23 items scanned → 18 clean, 5 skipped).

**Honest finding:** first run scored kusoj 3/12 vs Lane A's 8/12 — the difference was my
over-strict license regex (missed legacy `creativecommons.org/licenses/publicdomain/` and
`by/2.5` URLs), not a metadata change. Regex corrected; counts now match Lane A exactly.
The 4 `no licenseurl` kusoj items and the unlicensed `383records` item stay skipped —
"clean-majority" ≠ "all clean", enforced per item.

## Honest failures / deferrals (not wired)

- **Caption SaaS free tiers (Pocket 3 — Dubverse, quso.ai, Nova A.I., Wavel AI):** all require
  account sign-in for the free tier; there is no keyless API/CLI to smoke-test in this
  sandbox. No wiring attempted — deferral recorded, not faked. (Self-hosted whisper/faster-whisper
  captioning is already wired in `tools/captions/` from earlier waves — the stronger,
  commercial-safe caption path.)
- **AWS Transcribe / Google Cloud STT free tiers:** need cloud credentials; not available here.
- **DAHR direct API:** does not exist as a documented public endpoint; guessed `/api/v1/search`
  returned CloudFront 403. Wired via IA Great 78 instead (above).
- **Type Studio:** vendor URL + free-tier limits still unpinned (Lane A flagged) — no wiring.

## License check
- Scripts are Python stdlib only. `ffprobe` used as a CLI probe only — FFmpeg default build
  is LGPL-2.1-or-later, explicitly NOT quarantined per Wave-1 convention; not linked.
- No GPL/AGPL software introduced; no new `LICENSE_QUARANTINE.md` rows needed.
- Pulled license classes: pre-1923 recordings (PD) + CC0/PDM/plain-CC-BY — commercial-safe.
  Composition-PD caveat recorded in manifest and script docstrings.

## Commits
- `wave25-lane-c` — PD78 puller + proofs; clean-netlabel puller + proofs; this lane report.

## Open for coordinator
- DAHR wire-up remains a gap if direct DAHR metadata access is ever wanted; IA Great 78
  covers the PD-audio need without it.
- Caption SaaS free tiers still need a live-browser lane with sign-in credentials.
