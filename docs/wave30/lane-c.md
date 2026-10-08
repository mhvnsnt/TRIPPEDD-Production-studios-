# Wave 30 Lane C — tool wiring report (2026-10-08)

Scope: tool wiring lane. No branch was switched, no production/WIZARD_GANG_EP01/ paths touched.
Commits built via plumbing (`read-tree`/`update-index`/`write-tree`/`commit-tree`) against the
shared checkout's object store with a private index; pushed as `<sha>:refs/heads/wave30-lane-c`.

## 1. Global Jukebox PLOS ONE open dataset — WIRED ✅

- Canonical data DOI located (public, no paywall): **10.5281/zenodo.4898406**
  ("The Global Jukebox: Cantometrics", v0.1-alpha). Resolved via the repo's Zenodo badge
  (`zenodo.org/badge/latestdoi/337558145`, repo id 337558145 = theglobaljukebox/cantometrics).
- PLOS ONE paper: 10.1371/journal.pone.0275469 — Data Availability: coded data at
  github.com/theglobaljukebox, archived on Zenodo per-release.
- Downloaded artifact: `theglobaljukebox/cantometrics-v0.1-alpha.zip`, 3,293,252 bytes.
  md5 `2a814fd801b87ab561247b8b0f6184e6` **matches the Zenodo API record checksum exactly**;
  SHA-256 `c39f64819938ca60d08a0f119bb2eecb2df502e166c65ed9748d3e12f350e73e`;
  28 files / 17,057,792 bytes uncompressed.
- Wiring script: `tools/wave30_lane_c/wire_global_jukebox.py` — downloads from the DOI,
  verifies md5+SHA-256, extracts, parses all 8 CSV tables, prints a wiring report, and
  enforces hard gates. Ran 2026-10-08: **WIRE OK** (gates: raw/songs.csv 6,043 rows,
  37 Cantometric variables, 5,779 coded songs; cldf/data.csv 213,823 rows, distinct var_ids
  line_1..line_37, 216 codes, 37 variable definitions; sample row song_id=1/var_id=line_1/code=4.0).
- Proof document: `tools/wave30_lane_c/PROOFS.md` (DOI resolution trail, checksums, file
  listing, parse counts, license note, limits).
- Catalog entry updated (append-only): Global Jukebox row in `docs/RESOURCE_CATALOG.md` →
  Status: wired.
- Honest limits: Zenodo archive is v0.1-alpha (2021-06-03) only — three records
  (4895898/4895999/4898406) are duplicate uploads of the same release; 4898406 is the
  latestdoi target. Audio recordings are stream-only on theglobaljukebox.org and were not
  downloaded — coded data only.

## 2. VGMTrans — Qt dev libs re-check — STILL ABSENT

- Quick check 2026-10-08: no `qtbase5-dev`/`qt6-base-dev` installed, no `qmake`/`qmake6`.
  Compilers (cmake, g++, make) present but Qt headers missing — VGMTrans build remains
  impossible on this VM. Catalog note appended (Wave 30 Lane C).

## 3. Speaches Docker — container runtime re-check — STILL ABSENT

- Quick check 2026-10-08: no docker/podman/nerdctl binaries; `systemctl` reports docker
  service inactive. Smoke test remains deferred. Catalog note appended (Wave 30 Lane C).

## 4. Live-browser items — NEED PARENT/ROOT DELEGATION (not attempted, not faked)

- **Vsub free-tier re-check**: requires live browser — recorded here as
  "needs parent/root live-browser delegation."
- **NotebookLM / Eightify status**: requires live browser — recorded here as
  "needs parent/root live-browser delegation."

A subagent cannot operate a live browser; no results for these two items exist and none
were fabricated. An eligible parent/root agent should delegate them to a browser task.
