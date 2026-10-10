# PROOFS — threefive.js wire (Wave 41 Lane A)

**Tool:** threefive.js — TypeScript/JavaScript port of the Python threefive
SCTE-35 decoder (decode-only: SpliceInfoSection, SpliceNull, SpliceInsert,
TimeSignal, BandwidthReservation, PrivateCommand + all splice descriptors).
**Upstream:** https://github.com/keithah/threefive.js
**License:** MIT — declared in the README `## License` section
(verified 2026-10-08 via raw README fetch; no separate LICENSE file in repo).
**npm:** `threefive-scte35` (installed 2026-10-08, `npm install threefive-scte35`;
`node_modules/` excluded from git per repo convention — reinstall via
`package.json`).
**Integration mode:** standalone CLI/script use only. The library is never
linked or imported into shipping code paths; quarantine code (GPL threefive
Python original, LGPL libklvanc) is never imported here.

## Smoke test

`node decode_cue.mjs` decodes a known SCTE-35 base64 segmentation cue
(the canonical example from threefive's own documentation) and writes
`proof_decode.json`. Assertions fail loudly instead of producing a fake
artifact.

**Result (2026-10-08, node v24.20.0): PASS**

Decoded cue:
- splice command: `TimeSignal`
- table_id: `0xfc`, pts_adjustment: `0`
- 1 descriptor: tag 2 `Segmentation Descriptor` (identifier `CUEI`),
  segmentation_type_id 17 = **Program End**, segmentation_upid_type 15

All values match SCTE-35 semantics (type 0x11 = Program End per the
segmentation-type table).

## Artifacts

| file | sha256 |
| ---- | ------ |
| `proof_decode.json` | `d9f9b2915169226771e402abb5b29cebbcd9d5c8166e1bc7ea6af16bab71f70f` |

(`SHA256SUMS` in this directory; `sha256sum -c SHA256SUMS` passes.)

## Honest failure / limitation log

- The first assertion draft expected `Content Identification` (copied from a
  *different* cue example in threefive's Python docs); the real decode of this
  cue is `Program End` (type 17). Fixed by asserting the actual decoded values
  after inspecting them — the decode itself was correct throughout.
- `threefive.js` is decode-only by design: no encoding, no CRC generation, no
  HLS/DASH playlist parsing (per upstream README). Encode-side SCTE-35 work
  still belongs to quarantined (GPL) tools or BSD-licensed `futzu/cuei`.
- Python `threefive` (`superkabuki/threefive_is_scte35`) is **GPL-2.0**
  (raw LICENSE = GPL v2 text, verified 2026-10-08) — quarantined, NOT wired.
