# Wave 29 Lane B — tool wiring proofs (2026-10-07)

Two keyless tools from Wave 29 Lane A's new entries were smoke-tested with
real network proof artifacts. Both PASS. Two candidates were deferred
(honest reasons below — no fake artifacts).

## 1. e-codices IIIF Image API — PASS ✅

- **Script:** `tools/wave29_lane_b/ecodices_iiif_pull.py`
- **Catalog entry:** e-codices — Virtual Manuscript Library of Switzerland
  (⚠️ per-item rights; this test uses only the API mechanics, no reuse claim)
- **What it does:** hits the IIIF Image API v2 (Loris) at
  `https://www.e-codices.unifr.ch/loris/csg/csg-0359/csg-0359_000a.jp2`
  (Cod. Sang. 359 — St. Gall, c. 920/930, folio 000a): fetches `info.json`,
  asserts `@context` = `http://iiif.io/api/image/2/context.json` and real
  dimensions, then pulls a 150px-wide JPEG thumbnail and asserts JPEG magic.
- **Proofs:** `proofs/ecodices_report.json` (PASS, width 3328 × height 4992,
  profile `http://iiif.io/api/image/2/level2.json`),
  `proofs/ecodices_csg0359_000a_info.json` (full info.json),
  `proofs/ecodices_csg0359_000a_thumb.jpg` (4,298 bytes, 99×150 JPEG —
  eyes-on verified: real medieval manuscript folio, text block visible).
- **Keyless:** yes. License scope: filter to PUBLIC_DOMAIN-marked manuscripts
  for commercial-safe use (per catalog entry).

## 2. WeGA RESTful OpenAPI — PASS ✅

- **Script:** `tools/wave29_lane_b/wega_api_smoke.py`
- **Catalog entry:** Carl-Maria-von-Weber-Gesamtausgabe (WeGA) digital edition
  (⚠️ texts-only open; API itself is a real documented REST interface)
- **What it does:** fetches `http://www.weber-gesamtausgabe.de/api/v1/openapi.json`,
  asserts 14 paths exist; runs `/documents/findByDate?date=1810-03-04`
  (returns real diary entries, e.g. A064400 "Montag, 26. Februar 1810");
  runs `/search/entity?q=Weber` (200 hits); fetches `/documents/A064400`.
- **Proofs:** `proofs/wega_report.json` (PASS, 14 paths, sample records).
- **Keyless:** yes. The edition's texts are openly accessible via the API;
  music/audio content is not part of this API (letters, diaries, writings,
  bibliography only) — the catalog entry's ⚠️ framing stands.

## Deferred (honest, no smoke-test possible this pass)

- **Speaches (Docker)** — deferred: `docker info` fails on this VM; no
  container runtime present. Per brief, no turns burned.
- **VGMTrans (Qt build)** — deferred: no Qt dev libs on this VM
  (no qmake/qmake6, no libQt5/6Core in ldconfig). Per brief, not attempted.
- **Global Jukebox open dataset** — deferred: the PLOS ONE (Nov 2022)
  open-access Cantometric dataset download location was not pinpointed from
  the homepage this pass (no data/download links found); recording
  downloads are stream-only per the catalog entry. Left for Wave 30.
- Remaining Wave-29 SaaS entries (Deciphr, Vsub, Taption, Wispr Flow, etc.)
  are sign-in-required proprietary services — not keyless, not wirble
  without accounts; correctly excluded from wiring.

## Reproducibility

Both scripts are stdlib-only (`urllib`), runnable as:
`python3 tools/wave29_lane_b/ecodices_iiif_pull.py`
`python3 tools/wave29_lane_b/wega_api_smoke.py`
They exit non-zero on any assertion failure and write all artifacts plus
JSON reports into `tools/wave29_lane_b/proofs/`.
