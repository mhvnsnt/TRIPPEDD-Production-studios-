# Wave 20 Lane A — diligence notes (honest negatives)

Entries investigated but NOT catalogued as new `####` entries, with reasons.
These count as diligence, not as catalog entries. [Wave 20 Lane A]

## Pocket 1 — university-library digitizations

- **Wellcome Collection / Smithsonian Open Access / NYPL / Getty / DPLA / Europeana / Tokyo Dawn / Maltine / Bunkai-Kei**: all already catalogued as `####` entries — skipped as dups (pre-append dedup greps). No new entries needed.
- **Gallica (BnF)**: already catalogued (❓) — re-verified this wave; terms UNCHANGED (BnF/Europeana PRO: royalty-free only for strictly private use; commercial reuse of PD scans needs BnF agreement). Entry left as ❓ — correctly badged. No update.
- **Soisloscerdos netlabel**: EXCLUDED as clean — Bandcamp bio states works shared "bajo licencias Creative Commons, de uso no comercial" (CC BY-NC). NC = no-go for the clean-license pocket.
- **Austrian Literature Online (ALO)**: Innsbruck/Graz/Linz university digitization project — PD works digitized, but no blanket reuse statement verified this pass; ONB/ANNO entry covers the Austrian national-library layer. Future lane.

## Pocket 2 — demoscene netlabel long tail

- **stroboskop-label (Slovakia)**: NOT catalogued as clean despite 31/33 "clean"-classified items — release stroboskop030 (burningboy, "Penetration", marked CC-BY 3.0) contains "a remake of Rihanna's hit single S&M". A CC-BY mark on uncleared third-party material = unreliable label licensing hygiene. Documented here as the wave's cautionary example of why per-release verification is mandatory. The audit tool still covers it for research.
- **Test Tube (Monocromatica, Portugal)**: NOT catalogued — every release page says only "This work is licensed under a Creative Commons License" with NO variant pinned (tube012, tube099, tube222, tube228, tube234 verified). Unpinned variant = unverifiable = no entry.
- **Webbed Hand Records**: license page states CC BY-NC-ND 3.0 for (nearly) all releases — NC-ND = no-go for clean pocket. Not catalogued.
- **Ektoplazm / Tarapita Sounds**: "Released under a Creative Commons license for noncommercial usage" — NC = no-go. Not catalogued.
- **Netwaves Records**: CC BY-NC-SA per Creative Commons case study — NC = no-go. Not catalogued.
- **Comfortstand / 8bitpeoples / Bump Foot / Acroplane**: license unverified or NC this pass — no entries; 8bitpeoples entry already exists as ❓.
- **20kbps**: label site dead (20kbps.sofapause.ch unreachable); no verifiable license statement found this pass — no entry.
- **Dead label sites (genetic-trance.jimdo.com, noisecollector.net, hazardrecords.com, r-archives.net)**: original homepages unreachable; verification done via the labels' own archive.org release pages (label-operator uploaders + per-item licenseurl metadata). This is the long-tail reality: archive.org IS the surviving release/license page for these labels.

## Method note — archive.org licenseurl audit

The `tools/music/wave20_laneA_netlabel_audit.py` tool queries the archive.org
advancedsearch API per netlabel collection and classifies each audio item's
`licenseurl` (set by the uploader at upload time). Uploaders were verified as
the label operators/artists themselves (kahvi: nik@kahvi.org; treetrunk:
mystifiedthomas@gmail.com; ozkye: ozkyesound@yahoo.it; r-archives:
mikelrnieto@gmail.com; hazard_records: at@ankitoner.com; noisecollector:
noisecollector@gmail.com; oloil: ktktkk@gmail.com; deepxrec: dimonu@uralweb.ru;
kraimusic: onlyrealkrai@gmail.com; genetic-trance: alexios@ukr.net).

Full-collection results (2026-10-07, audio items only):
| collection | items | clean (CC0/PDM/BY) | NC | BY-SA/BY-ND | unknown |
|---|---|---|---|---|---|
| genetic-trance | 921 | 583 | 19 | 5 | 314 |
| oloil | 522 | 513 | 0 | 0 | 9 |
| treetrunk | 821 | 530 | 207 | 80 | 4 |
| deepxrec | 599 | 61 | 524 | 0 | 14 |
| noisecollector | 354 | 180 | 6 | 145 | 23 |
| kahvi | 267 | 69 | 18 | 106 | 74 |
| kraimusic | 168 | 60 | 71 | 22 | 15 |
| ozkye-sound-netlabel | 106 | 9 | 74 | 2 | 21 |
| hazard_records | 103 | 38 | 0 | 0 | 65 |
| r-archives | 62 | 61 | 0 | 0 | 1 |
| stroboskop-label | 33 | 31 | 0 | 1 | 1 |

Key doctrine confirmation: NC dominance holds across the long tail (deepxrec
524/599 NC, kahvi 106/267 BY-SA, noisecollector 145/354 BY-SA/BY-ND). The
"clean" bucket is real but ALWAYS requires per-release licenseurl checks —
the stroboskop/Rihanna case proves label-level trust is insufficient.
