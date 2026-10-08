# Wave 28 Lane A — wire proofs

Two small metadata-only wire proofs for entries added this wave. No binaries,
no media downloads, no copyrighted expression — metadata only.

## 1. PD shape-note tunebook IA index — `wire_pd_tunebook_ia.py`

Queries the public Internet Archive `advancedsearch` API for the three PD
tunebook entries (Southern Harmony 1835, Christian Harmony 1866, New Harp of
Columbia 1867) and writes `proof-pd-tunebook-ia.json` (identifiers, titles,
dates, item URLs).

Run 2026-10-07: 19 item records across 3 queries, including the 1835 Walker
`Southern Harmony` scan (`southernharmonym0000walk`). All three works are
pre-1929 = public domain.

## 2. SNESmusic.org composers index sample — `wire_snesmusic_composers.py`

Fetches the live SNESmusic.org v2 composers index (letter "A" page) and
extracts composer names + profile links into `proof-snesmusic-composers.json`.

Run 2026-10-07: 50 composer records parsed from the 23 KB index page (names
only — no SPC files downloaded). Note: the site's RSS update feed
(`v2/feed.xml.php`) is currently empty, so the composers index is the better
metadata leg.

Both scripts use stdlib only (`urllib`, `json`, `re`).
