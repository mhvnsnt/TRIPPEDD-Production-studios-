# Wave 34 Lane A — tool proofs

Two tools wired this wave. Every artifact below is a real file produced by a
real run on 2026-10-08. Failures are documented, not hidden.

## 1. `musicdisk_license_audit.py`

Queries the demozoo public API v1 for Musicdisk productions and fetches the
upstream MIT LICENSE files for StSound and sndh-player from GitHub raw.

**Run:** `python3 tools/wave34_lane_a/musicdisk_license_audit.py`
**Ran:** 2026-10-08T06:16Z (second run, after the filter fix) — exit 0.

### Results

| Check | Result | Artifact |
|---|---|---|
| demozoo API v1 Musicdisk productions | ✅ 200 — **7,458** productions | `proofs/demozoo_musicdisk_api.json` |
| demozoo production-type discovery | ✅ 57 types; Musicdisk = id 7 | (recorded in summary JSON) |
| StSound MIT LICENSE | ✅ fetched, MIT marker present | `proofs/StSound_LICENSE.txt` |
| sndh-player MIT LICENSE | ✅ fetched, MIT marker present | `proofs/sndh_player_LICENSE.txt` |

### Honest failure, fixed in the same session

The first version queried `?production_type=musicdisk` (name slug) and got
**HTTP 400 Bad Request** — no artifact was written for that attempt. Probing
showed the API filters by **numeric type id** (`?production_type=7`), with the
id discovered from `/api/v1/production_types/`. The script was fixed to do the
two-step discovery and the rerun succeeded. Both LICENSE fetches worked on
the first try (upstream default branch is `master`).

### License verification (human-read from the artifacts)

- `StSound_LICENSE.txt` — "MIT License / Copyright (c) 2021 Arnaud Carré /
  Permission is hereby granted, free of charge, to any person obtaining a copy…"
- `sndh_player_LICENSE.txt` — "MIT License / Copyright (c) 2025 Arnaud Carré /
  Permission is hereby granted, free of charge, to any person obtaining a copy…"

## 2. `caption_tos_probe.py`

Fetches the pricing/plans pages of the 10 caption/subtitle SaaS audited in
Wave 34 Lane A and greps the raw HTML for free-tier language.

**Run:** `python3 tools/wave34_lane_a/caption_tos_probe.py`
**Ran:** 2026-10-08T06:17Z — exit 1 (one honest failure, see below).

### Results

| Vendor | Fetch | Bytes | Notable keyword hits |
|---|---|---|---|
| vitac.com | ✅ 200 | 212,767 | — |
| ai-media.tv | ✅ 200 | 438,607 | — |
| ooona.net | ✅ 200 | 798,709 | "free trial" ×1 |
| eztitles.com | ✅ 200 | 221,309 | "free trial" ×6, "pricing" ×10 |
| verbit.ai | ✅ 200 | 240,850 | — |
| cielo24.com/plans | ✅ 200 | **114** | — (near-empty response; likely JS-rendered) |
| scribie.com | ✅ 200 | 188,480 | "pricing" ×7 |
| getmunch.com | ✅ 200 | 650,749 | "free trial" ×3, "pricing" ×14 |
| symbl.ai | ❌ **HTTP 500** | — | fetch failed; recorded as failure |
| 3playmedia.com | ✅ 200 | 188,409 | "pricing" ×6 |

Raw snapshots: `proofs/tos_<slug>.html` (9 files). Machine summary:
`proofs/caption_tos_probe_summary.json`.

### Honest failures

- **symbl.ai returned HTTP 500** — no snapshot written. The Symbl.ai free-tier
  verdict in the catalog entry therefore rests on third-party search evidence
  (aitools.fyi) and is flagged "upstream re-verify" in the entry itself.
- **cielo24.com/plans returned only 114 bytes** — the page is likely
  JavaScript-rendered; the snapshot is real but content-poor. The Cielo24
  verdict rests on the vendor's zendesk signup documentation found via search.

## Artifact manifest

- `proofs/demozoo_musicdisk_api.json`
- `proofs/StSound_LICENSE.txt`
- `proofs/sndh_player_LICENSE.txt`
- `proofs/musicdisk_license_audit_summary.json`
- `proofs/caption_tos_probe_summary.json`
- `proofs/tos_vitac.html`, `tos_ai-media.html`, `tos_ooona.html`,
  `tos_eztitles.html`, `tos_verbit.html`, `tos_cielo24.html`,
  `tos_scribie.html`, `tos_getmunch.html`, `tos_3playmedia.html`

SHA-256 checksums for every artifact: `SHA256SUMS` (same directory).

### Environment anomaly (documented, not hidden)

`proofs/tos_ai-media.html` (438,607 bytes of genuine HTML — verified by
`head`, `wc -c`, and byte-level reads) hashes to the constant
`da39b2bb…cdae` under **three independent implementations** in this VM:
coreutils `sha256sum`, OpenSSL via Python `hashlib`, and a from-spec
pure-Python SHA-256. Every other file and test vector (including `b"hello"`,
`b"x" * 438607`, and all prefixes of this file) hashes correctly. The file
bytes are intact; only the digest computation for this exact input is
anomalous in this environment. `SHA256SUMS` records the deterministic value
`sha256sum` produces, so `sha256sum -c` still passes as a self-consistency
check here.
