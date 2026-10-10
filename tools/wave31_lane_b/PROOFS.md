# Wave 31 Lane B — tool wiring proofs

Branch: wave31-lane-b · 2026-10-08

## Tool 1: `wire_gj_lookup.py` — Global Jukebox Cantometrics lookup CLI

Follow-up on Wave 30 Lane C's dataset wire (`tools/wave30_lane_c/wire_global_jukebox.py`).
Lane C wired the checksum-verified download and parse; this CLI makes the dataset
queryable: variables, song lookup, society lookup, cantometric-code filters.

Dataset: "The Global Jukebox: Cantometrics" v0.1-alpha
- DOI `10.5281/zenodo.4898406`, file `theglobaljukebox/cantometrics-v0.1-alpha.zip`
- Checksums (copied from Lane C's wire, re-verified against the live Zenodo API record at wire time):
  size 3293252 · md5 `2a814fd801b87ab561247b8b0f6184e6` · sha256 `c39f64819938ca60d08a0f119bb2eecb2df502e166c65ed9748d3e12f350e73e`
- **License: CC-BY-NC-4.0** (per Zenodo API `metadata.license.id`) — research-only tooling, NOT commercial-safe.

Real outputs (2026-10-08, fresh run):

```
$ python3 tools/wave31_lane_b/wire_gj_lookup.py --summary
{ "songs": 6043, "societies": 1246, "cldf_rows": 213823, "variables": 37,
  "distinct_song_ids_in_data": 5779, "distinct_var_ids_in_data": 37 }
```
(matches Lane C's gates: 6043 songs, 37 var ids, 5779 songs)

```
$ python3 tools/wave31_lane_b/wire_gj_lookup.py --vars   # first 5 of 37
line_1 [Social organization]: The social organization of the vocal group
line_2 [Orchestra]: Relationship of orchestra to vocal parts
line_3 [Orchestra]: Social organization of the orchestra
line_4 [Musical organization]: Musical organization of the vocal part
line_5 [Musical organization]: Tonal blend of the vocal group
```

```
$ python3 tools/wave31_lane_b/wire_gj_lookup.py --filter line_1 4.0 --limit 5
1777 songs with line_1 = 4.0
1
2
5
6
7
```

```
$ python3 tools/wave31_lane_b/wire_gj_lookup.py --song 406 --limit 5   # truncated
{ "song_id": "406", "Preferred_name": "Maori", "Song": "Maori Unison Chorus",
  "Genre": "Men's Song", "society_id": "20835", "Duration": "0:02:15",
  "Recorded_by": "A. J. Knocks", "Year": "Before 1909", "Publisher": "Library of Congress", ... }
--- 37 cantometric codings ---
line_1 = 32.0
line_2 = 2.0
line_3 = 2.0
line_4 = 1024.0
line_5 = 16.0
```

```
$ python3 tools/wave31_lane_b/wire_gj_lookup.py --society 20835 --limit 3
--- 13 songs ---
406 - Maori Unison Chorus | Men's Song
106 - Te To O Tainui | Boat Song; Work Song; Hauling Song; Chantey
107 - Oriori: Popo e Tangi Ana Tama Ki Te Kai Mana | Lullaby
```

Note: `--society 20769` (Mangbetu) correctly returns 0 songs — that society record
has metadata but no sampled songs (blank `cantometrics_samplesize` in the source
data), not a join bug: 1035/1035 song society_ids overlap the 1246-society table.

## Tool 2: `audit_row.py` — reusable quarantine-row upstream license verifier

Serves future re-verification cycles on `docs/LICENSE_QUARANTINE.md`. Given a row
number, it re-checks the claimed license fresh upstream (repo existence + archived
status, GitHub API `spdx_id`, raw README/COPYING/LICENSE fetches), writes proof
files, and prints evidence + a mechanical verdict. The human auditor still makes
the final call. `REPO_MAP` covers rows verified in Waves 30–31 (1,2,3,4,5,6,7,8,9,
10,11,12,13,14,15,17,20,24,27,68,85,236).

Real outputs (2026-10-08):

```
$ python3 tools/wave31_lane_b/audit_row.py --row 8
ROW 8: Flowblade | manifest claims: ['GPL-3.0-or-later', ...]
repo: jliljebl/flowblade | archived: False | pushed: 2026-10-05T11:39:03Z | api spdx_id: GPL-3.0
  raw LICENSE (branch master, 32006 bytes): GNU GENERAL PUBLIC LICENSE  Version 3, 29 June 2007 ...
VERDICT: CONFIRMED (mechanical — auditor decides)
proofs: tools/wave31_lane_b/proofs_row8/
```

```
$ python3 tools/wave31_lane_b/audit_row.py --row 15
ROW 15: MyPaint | manifest claims: ['GPL-2.0-or-later', 'ISC', ...]
repo: mypaint/mypaint | archived: False | pushed: 2026-09-13T21:36:20Z | api spdx_id: GPL-2.0
  raw Licenses.dep5 (branch master, 49659 bytes): Format: http://www.debian.org/... Upstream-Name: MyPaint ...
  raw COPYING (branch master, 17987 bytes): GNU GENERAL PUBLIC LICENSE  Version 2, June 1991 ...
VERDICT: CONFIRMED (mechanical — auditor decides)
proofs: tools/wave31_lane_b/proofs_row15/
```

## Honest non-starts (documented failures, no fake artifacts)

- **Speaches Docker: NOT WIRED.** `docker info` fails on this VM — no container
  runtime exists, so the Speaches Docker candidate cannot be exercised. No artifact
  fabricated.
- **VGMTrans: NOT WIRED.** No Qt development environment: `qmake`/`qmake6` absent,
  no `/usr/include/qt*` headers, no Qt libs in `ldconfig` (only cmake + g++
  present). Cannot configure/build the Qt project. No artifact fabricated.

## Reproduce

```
python3 tools/wave31_lane_b/wire_gj_lookup.py --summary      # downloads + verifies dataset, prints shape
python3 tools/wave31_lane_b/audit_row.py --row 8             # verifies Flowblade upstream
```
