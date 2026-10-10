# Wave 22 Lane A — catalog deepening (2026-10-07)

## Counts
- Catalog: 2,201 → **2,304** (+103 new `####` entries; baseline was 2,201 on origin/main, not 2,196 — local main was 5 behind)
- Quarantine: rows 201–204 → **205–231** (+27 GPL/AGPL/LGPL rows)
- Netlabel ToS audit: 19 ❓ netlabels investigated against their own sites/FAQs
  - Re-badged to ⚠️: Bump Foot (CC BY-NC-SA per own about page), Soisloscerdos (CC NC + attribution per own Bandcamp bio), ogredung (CC BY-ND-NC 1.0 per release pages), hippocamp (CC-flagged per netlabellist), 8bitpeoples (site now a commercial store — no blanket grant), Trekkie Trax (now a commercial JASRAC-registered label), Netlabels.org (directory, many NC), Subvert.fm (platform, per-release)
  - Still ❓ (honestly unverifiable): ALTEMA (own site 403s), MarginalRec., Chipmusic.org, ChipMusic.org, illmatikvibes, binkcrsh, floppyswop, Kreislauf (site dead), chiptune (netlabel), Section 27 blogspot (blog deleted), Telefuture (site dead), KEYGENMUSiC (player site, not a label), Pterodactyl Squad, Ubiktune

## New sections appended (append-only; no existing entries touched except netlabel badge/license lines)
- National-library digitization & OCR tooling (+26 net): Tesseract, OCRmyPDF, Kraken, OCR-D, OCRopus, OCR4all, tesseract.js, EasyOCR, PaddleOCR, doctr, Donut, olmOCR, MMOCR, RapidOCR, Surya, scikit-image, pyvips, Cantaloupe, Loris, Mirador, Universal Viewer, biiif, node-iiif, RAIS, Annona, Recogito 2, OpenRefine, JabRef
- Audio restoration & processing (+14): torchaudio, noisereduce, audiomentations, Open-Unmix, Asteroid, nussl, pyrubberband, resampy, RNNoise, DeepFilterNet, PaddleSpeech (+ Camelot/Tabula/pdfplumber/pdfminer.six PDF extraction)
- EBU-TT Live reference implementations (+5): EBU-TT XSD family, IRT imsced, IRT xcf_suite_ttml, ebu/benchmarkstt, ebu/dash.js EBU-TT-D branch
- National-library catalog APIs & open data (+28): DigitalNZ, NLS Data Foundry, NLS Maps API, BNE datos, DDB, LOC JSON, NDL Search, KBR, Google Books, Open Library, BHL, Papers Past, TNA Discovery, Canadiana, Rumsey, VIAF, WorldCat Search, Wikidata, KB Sweden, KB Denmark, NLW, BNP, NB Norway, NLB Singapore, NL Greece, NL Ireland, OpenAlex, Unpaywall
- Military-band recordings, new jurisdictions (+27): NL, IT, ES, PL, AT, BE, SE, DK, PT, IE, CH, NZ, IL, TR, ZA, TH, BR, CL, MX, GR, CZ, HU, MY, ID, PH, PK, EE

## Wire-up proofs (tools/wave22_lane_a/proofs/)
- IRT EBU-TT-D sample → ttconv → valid SRT (8+ cues)
- LOC JSON API: 63 results for "military band"
- Finna API: 2,812 records for "sotilassoittokunta"
- noisereduce: +3.18 dB SNR on synthetic test
- Tesseract 5.3.4: 100% on rendered test page

## Honest gaps / failures
- Skipped (license unverifiable): ultimatevocalremovergui, eScriptorium, BookScanWizard (repo not found)
- WORLD vocoder + pyworld + librosa + Demucs + Spleeter: dropped — already in catalog (dedup)
- Military-band official sites often block/empty on curl (esercito.it, defensie.nl) — those entries say "verify before reuse" rather than claiming terms
- Several national-library entries are ⚠️/❓ with per-item verification notes — the lane's honest outcome, not a defect

## Wave 23 thin-pocket candidates
1. **Netlabel long tail, part 2**: ~60 more ❓-badged music entries in Wave-3 tables (GameSounds.xyz, FlashKit, Kunst der Fuge, Battle of the Bits) + the still-❓ labels above (ALTEMA, MarginalRec.) — revisit after 6 months (sites die fast in this scene)
2. **National-library AV holdings**: only NLN/NB Norway + LOC covered for audio; BNF Gallica audio, DNB Deutsches Musikarchiv, and NLA oral-history collections unverified
3. **EBU-TT Live carriage**: WebSocket/filesystem carriage demos from the toolkit (ebu-dummy-encoder) not yet smoke-tested — needs Python 3.11 + poetry env
4. **Military bands, remaining jurisdictions**: ~40 more (Baltics beyond EE, Balkans, Middle East, Central Asia, Oceania microstates, Caribbean) + date-PD 78rpm band recordings on Commons/IA (the only ✅ lane in this pocket)
5. **Digitization hardware**: DIY book scanners (Internet Archive Scribe, DIY Book Scanner community) — open hardware designs, not yet cataloged
6. **Rights-statement standards**: RightsStatements.org vocabulary + per-institution rights APIs (the machine-readable layer behind all the ⚠️ badges)
