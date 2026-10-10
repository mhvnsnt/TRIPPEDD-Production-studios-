# Wave 20 Lane A — proof artifacts

## Netlabel license audit (tool wiring proof)

- Tool: `tools/music/wave20_laneA_netlabel_audit.py`
- Run: 2026-10-07, archive.org advancedsearch API, 11 netlabel collections, audio items only
- Outputs:
  - `netlabel_license_audit_20261007-223722.json` (per-item: identifier, title, licenseurl, class, uploader, date)
  - `netlabel_license_audit_20261007-223722.csv` (same, tabular)
- Result: 4,176 audio items audited; 2,135 clean (CC0/PDM/CC-BY), rest NC / BY-SA/BY-ND / unknown.
- Honest failure: none in the audit run itself; all 11 collections returned data.

## Proof audio download (real bytes proof)

- File: `proof_audio/hr097_track06.mp3`
- Source: https://archive.org/download/hr097/hr097_yunclas_06_last_words_of_the_demiurge.mp3
- Release: hr097 — YUNCLAS "THE ANTICOSMICK ACCELERATION" (hazard_records, Spain)
- License on release page: CC0 1.0 Universal (uploader at@ankitoner.com, label operator)
- SHA-256: e95fad75f54f483251baac73ed8a2b936d67fd7b95a0d1a46d5e76c5e10a2df5
- ffprobe: 296.80 s, 7,458,894 bytes, MP3, 44.1 kHz, stereo
- Honest failure: first download attempt (no `-L` flag) returned HTTP 200 with 0 bytes —
  archive.org requires following the redirect. Retry with `-L` succeeded; byte count
  matches the metadata `size` field exactly (7458894). The 0-byte file was deleted,
  not kept.

## License verification provenance (pocket 1)

All library rights statements were quoted from the institutions' own rights pages
(onb.ac.at/en/use, bne.es reproduction rules PDF, loc.gov/free-to-use,
loc.gov/legal/understanding-copyright, bsb-muenchen.de image use page,
biodiversitylibrary.org via Harvard/Illinois library guides, hathitrust.org/the-collection,
British Library statement via PetaPixel + Wikimedia Commons "no known copyright
restrictions" marks). Search-result URLs recorded in lane working notes.
