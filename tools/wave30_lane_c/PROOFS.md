# Wave 30 Lane C — Global Jukebox wiring proofs

Source paper: Wood et al. (2022), "The Global Jukebox: A public database of performing
arts and culture", PLOS ONE 17(11): e0275469 — https://doi.org/10.1371/journal.pone.0275469

Date wired: 2026-10-08. Wiring script: `wire_global_jukebox.py`
(run `python3 wire_global_jukebox.py --zip <file>` to reproduce; no `--zip` downloads
the DOI artifact itself and verifies it before parsing).

## 1. Data DOI located (public, no paywall)

- Canonical data DOI: **10.5281/zenodo.4898406** — "The Global Jukebox: Cantometrics", v0.1-alpha
- Resolved via the repo's Zenodo badge URL `https://zenodo.org/badge/latestdoi/337558145`
  (GitHub repo id 337558145 = theglobaljukebox/cantometrics) → redirects to record 4898406.
- Concept record 4895897; records 4895898 / 4895999 / 4898406 are all v0.1-alpha
  (duplicate uploads of the same release; 4898406 is the latestdoi target).
- GitHub release v0.1-alpha (2021-06-03) is the only release; no newer upstream data.
- Upstream repo: https://github.com/theglobaljukebox/cantometrics (Data Availability
  statement in the PLOS ONE article points at https://github.com/theglobaljukebox;
  audio is streaming-only on theglobaljukebox.org and was NOT downloaded — coded data only).

## 2. Download verified

- Download URL: https://zenodo.org/records/4898406/files/theglobaljukebox/cantometrics-v0.1-alpha.zip?download=1
- Size: 3,293,252 bytes (matches Zenodo API `files[0].size`)
- md5: `2a814fd801b87ab561247b8b0f6184e6` — **exact match to Zenodo API record checksum**
- SHA-256 (computed locally): `c39f64819938ca60d08a0f119bb2eecb2df502e166c65ed9748d3e12f350e73e`
- Zip contents: 28 files / 17,057,792 bytes uncompressed, single top dir
  `theglobaljukebox-cantometrics-6f93b1c/` (commit hash in dir name).

## 3. Parse proof (from the script's own run, 2026-10-08)

| table | rows | notes |
|---|---|---|
| raw/data.csv | 5,779 | 37 Cantometric line variables + ids |
| raw/songs.csv | 6,043 | song metadata |
| raw/societies.csv | 1,246 | society metadata |
| cldf/data.csv | 213,823 | long-format codings |
| cldf/songs.csv | 5,779 | |
| cldf/societies.csv | 984 | |
| etc/codes.csv | 216 | code meanings |
| etc/variables.csv | 37 | variable definitions |

- Distinct CLDF `var_id`: **37** (line_1..line_37 — the 37 Cantometric variables, incl. CV7/CV10/CV23/CV37 cited in the paper)
- Distinct `song_id` in CLDF codings: **5,779**
- Sample row: `{'song_id': '1', 'society_id': '17557', 'var_id': 'line_1', 'code': '4.0'}`
- Script hard gates (raw/songs=6043 rows, 37 vars, 5779 songs) **PASS** → `WIRE OK`.

## 4. License

Repo ships `LICENSE.txt`; data is CC-BY per the PLOS ONE article (open access, "permits
unrestricted use ... provided the original author and source are credited"). Citation:
Lomax (1968); Wood et al. (2021), accessed 2026-10-08.

## 5. Limits / honest notes

- The Zenodo archive holds **v0.1-alpha (2021-06-03) only**; GitHub main has since added
  cldf/ refinements, but no new Zenodo release exists — wiring pins the versioned DOI.
- Audio recordings are streaming-only on theglobaljukebox.org with restrictions
  (see paper §2.6); not in scope — coded data only.
