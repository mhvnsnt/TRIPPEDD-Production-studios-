# Wave 23 Lane A — Netlabel long tail (part 2) + National-library AV holdings

**Entries proposed: 23** (`####` entries below) · **Honest negatives documented: 40+** · Audit date: 2026-10-07
Coordinator: append-only into RESOURCE_CATALOG.md; do NOT renumber existing rows. Dedup greps run pre-append (see Method).

---

## Pocket 1 — Netlabel long tail, part 2 (13 entries)

Wave-20's licenseurl audit established that the Internet Archive netlabel long tail is overwhelmingly CC-BY-NC. This wave audited **90 more IA netlabel sub-collections** (batches 1–3, raw JSON in this folder: `w23_batch1.json`, `w23_batch2.json`, `w23_batch3.json`; full sub-collection index `nl_subcollections.json` — 2,000 of 2,014 sub-collections of the `netlabels` collection). Result: **zero clean-majority labels**. The entries below are the honest survivors: mixed collections whose per-item `licenseurl` metadata (set by uploaders at upload time) pins a verified CC-BY/CC0/PDM subset — same ⚠️ per-release-check treatment as the existing Netlabels.org entry — plus two blanket-grant survivals (Opsound, Shtooka).

### IA netlabel collection — the parent directory

#### Internet Archive — Netlabels collection ⚠️ directory — per-item CC check
- **What:** The Internet Archive's own curated "netlabels" collection: 2,014 label sub-collections, 77,007 audio items (counts verified 2026-10-07 via archive.org advancedsearch API). The surviving home of the 2000s netlabel scene — every release carries a per-item `licenseurl` field.
- **URL:** https://archive.org/details/netlabels
- **License:** ⚠️ Per-item CC licenses — most items are CC-BY-NC-* (research lane only); filter to `licenseurl` containing `/licenses/by/`, `/publicdomain/zero/`, or `/publicdomain/mark/` for the commercial-safe slice. Check EACH item.
- **Free tier:** free streaming + downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Discovery layer for all three waves' netlabel audits (W19/W20/W23). Workflow: advancedsearch `collection:netlabels AND mediatype:audio`, read `licenseurl` per item, keep proof. [Wave 23 Lane A]

### Mixed collections with verified clean subsets (⚠️ per-release check)

#### On-Mix (ONMP) ⚠️ mixed — 61 CC-BY items of 240
- **What:** Dutch e-label (est. 2006, on-mix.com) — non-genre-specific netlabel, 240 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Aon-mix
- **License:** ⚠️ Mixed — 61 of 240 audio items carry CC-BY licenseurl (44× CC-BY 3.0, 16× CC-BY 3.0 NL, 1× CC-BY 4.0; verified 2026-10-07); the rest are BY-NC*. Sonicsquirrel lists no blanket label license — per-item check mandatory.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Largest clean subset found in this wave's 90-collection sweep. Filter `licenseurl` for `/licenses/by/` (plain BY only, not by-nc). [Wave 23 Lane A]

#### Quantum Bit Netlabel ⚠️ mixed — 26 CC-BY items of 122
- **What:** Italian electronic netlabel — 122 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Aquantumbit-label
- **License:** ⚠️ Mixed — 26 of 122 audio items carry CC-BY licenseurl (23× CC-BY 3.0, 2× CC-BY 2.5 IT, 1× CC-BY 4.0; verified 2026-10-07); remainder BY-NC/BY-SA/BY-ND.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Use only the plain-BY items; the 43 BY-SA/BY-ND items need per-release review. [Wave 23 Lane A]

#### Toucan Music ⚠️ mixed — 19 CC-BY items of 208
- **What:** UK eclectic netlabel (Toucan) — 208 releases on archive.org; appeared on a 2017 netlabel podcast tracklist.
- **URL:** https://archive.org/search?query=collection%3Atoucan
- **License:** ⚠️ Mixed — 19 of 208 audio items carry CC-BY licenseurl (9× CC-BY 3.0, 7× CC-BY 2.0 UK, 3× CC-BY 2.5; verified 2026-10-07); 124 BY-NC, 63 BY-SA.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** [Wave 23 Lane A]

#### Vulpiano Records ⚠️ mixed — 17 clean items of 232
- **What:** Netlabel, 232 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Avulpiano-records
- **License:** ⚠️ Mixed — 17 of 232 audio items carry CC-BY/CC0 licenseurl (verified 2026-10-07); 208 BY-NC.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Small clean slice of a mostly-NC label — filter, don't browse. [Wave 23 Lane A]

#### ComputerMusicNeix ⚠️ mixed — 15 clean items of 227
- **What:** Netlabel, 227 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Acomputermusicneix
- **License:** ⚠️ Mixed — 15 of 227 audio items carry CC-BY licenseurl (verified 2026-10-07); 127 BY-NC, 74 BY-SA.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** [Wave 23 Lane A]

#### Tales About Nothing ⚠️ mixed — 14 clean items of 356
- **What:** Netlabel, 356 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Atalesaboutnothing
- **License:** ⚠️ Mixed — 14 of 356 audio items carry CC0/CC-BY licenseurl (4× CC0 1.0, 10× CC-BY 3.0; verified 2026-10-07); 194 BY-SA, 107 BY-NC.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** [Wave 23 Lane A]

#### D-Trash Records ⚠️ mixed — 9 CC-BY items of 220
- **What:** Canadian breakcore/hard-electronic netlabel (D-Trash) — 220 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Ad-trash-records
- **License:** ⚠️ Mixed — 9 of 220 audio items carry CC-BY licenseurl (5× CC-BY 2.5 CA, 2× CC-BY 4.0, 2× CC-BY 3.0; verified 2026-10-07); 140 BY-NC.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Aggressive electronic styles fit horror/action scoring; verify each item's licenseurl. [Wave 23 Lane A]

#### Rodent Tapes ⚠️ mixed — 16 clean items of 837
- **What:** Netlabel (Rodent Tapes backstage collection) — 837 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Arodenttapesbackstage
- **License:** ⚠️ Mixed — 16 of 837 audio items carry CC0/PDM licenseurl (12× PDM 1.0, 3× PDM 1.0 http, 1× CC0; verified 2026-10-07); 787 BY-NC.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** [Wave 23 Lane A]

#### nowaytwowayout ⚠️ mixed — 16 clean items of 532
- **What:** Netlabel, 532 releases on archive.org.
- **URL:** https://archive.org/search?query=collection%3Anowaytwowayout
- **License:** ⚠️ Mixed — 16 of 532 audio items carry CC-BY licenseurl (verified 2026-10-07); 509 BY-NC.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** [Wave 23 Lane A]

#### Southern City's Lab ⚠️ mixed — 10 clean items of 214
- **What:** Russian DIY netlabel (est. 2012) — indie rock, garage, punk, IDM, sound art; 214 releases on archive.org; Bandcamp page claims "a Creative Commons license" with variant unpinned.
- **URL:** https://archive.org/search?query=collection%3Asouthern-citys-lab
- **License:** ⚠️ Mixed — 10 of 214 audio items carry CC-BY/CC0 licenseurl (verified 2026-10-07); 197 BY-NC. Label-level variant never pinned → per-item check mandatory.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Secondary sources (Paperblog) confirm CC but not the variant — the IA metadata is the only pinned evidence. [Wave 23 Lane A]

### Blanket-grant survivals

#### Opsound (archived pool) ✅ CC BY-SA — gift-economy sound pool
- **What:** Sal Randolph's pioneering free-culture music pool (2002–; site now defunct) — uncurated CC sound pool; works hosted by contributors, indexed centrally, many mirrored into the IA netlabels collection.
- **URL:** https://archive.org/details/netlabels (surviving files via the IA netlabels collection)
- **License:** ✅ CC BY-SA (typically 2.5; some plain CC-BY) — documented on Creative Commons' own feature page on Opsound ("licensed under a Creative Commons Attribution Share-Alike license… people can use freely — even for commerce"), 2026-10-07.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Label site dead — source the actual files from IA mirrors and keep the licenseurl proof. Share-alike applies to adaptations synced to picture (CC BY-SA adaptation rule) — fine for score beds, flag for trailer use. [Wave 23 Lane A]

#### Shtooka Project ⚠️ CC-licensed spoken-word collections
- **What:** Cooperative project (Nicolas Vion) building free audio collections of words/expressions/proverbs spoken by native speakers — 75,000+ recordings across 15+ languages (French, Russian, Ukrainian, English, Dutch, Czech, Chinese, German…); feeds the Tatoeba/Lingua Libre ecosystem.
- **URL:** https://wiki.creativecommons.org/index.php?title=Shtooka_Project_-_free_audio_collections_of_words (CC directory listing; collections at shtooka.net)
- **License:** ⚠️ Listed in Creative Commons' own content directory as a CC-licensed sound portal; French Wikipedia describes the collections as released "sous licence libre" — variant varies by collection, confirm per collection before use.
- **Free tier:** free downloads
- **Repo lane:** trippedd (dialogue/VO reference)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pronunciation/VO reference goldmine for multilingual dialogue; not music — do not file under score. [Wave 23 Lane A]

---

## Pocket 2 — National-library AV holdings (10 entries)

Only libraries with verifiable AV-rights statements are entered. General Gallica/Polona/BDH/Finna/Trove portal entries already exist — these are the AV-specific holdings layers.

#### Europeana Sounds / Europeana Music / Europeana Radio ⚠️ per-item rights
- **What:** The Europeana Sounds aggregation: 600,000+ audio files from 24 European institutions (12 countries; incl. the British Library, BnF, DNB/Deutsches Musikarchiv, National Library of Latvia, CNRS sound archives) — music, spoken word, environment recordings, radio programmes, sound effects; plus the Europeana Music thematic portal and Europeana Radio (200,000-track shuffle).
- **URL:** https://www.europeana.eu/en (project results: https://www.dnb.de/EN/Professionell/ProjekteKooperationen/Projektarchiv/2017/europeanaSounds/europeanaSounds_node.html)
- **License:** ⚠️ Per-item rights via Europeana's "Can I use it?" filter (CC0/CC-BY/PDM/rightsstatements.org) — verified 2026-10-07 via DNB's project page. Much of the corpus is in-copyright; filter to open licences only.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** This is the open-AV face of the DNB Deutsches Musikarchiv (which has no public digital reuse itself — see negatives). CNRS contributed 38,000 sounds, mostly pre-1963 for free access. [Wave 23 Lane A]

#### National Diet Library (Japan) — Historical Recordings Collection (Rekion) ⚠️ expired-copyright subset
- **What:** NDL's Historical Recordings Collection: ~50,000 early Japanese 78rpm/metal-disc recordings (c. 1900–1950) — traditional Japanese music, folk, rakugo, kabuki, classical, opera, popular music, speeches.
- **URL:** https://dl.ndl.go.jp/ (collection announcement: https://www.ndl.go.jp/en/news/ — Rekion; NDL Newsletter No.192)
- **License:** ⚠️ The NDL itself flags "recordings with expired copyright" as the internet-available subset (~1,090+ items per NDL Newsletter 192; ~2,400 streaming online per NDL announcement Dec 2017, verified 2026-10-07 via infodocket quoting NDL) — the rest is on-premises/partner-library only.
- **Free tier:** free streaming (expired-copyright subset)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** NDL bibliographic open datasets include the Rekion metadata — machine-filterable. Period Japanese scoring material unavailable anywhere else. [Wave 23 Lane A]

#### Gallica (BnF) — documents sonores ⚠️ per-item "Droits"
- **What:** The audio layer of Gallica: 52,004 audio recordings (2024 count) — early French speech (incl. the 1911 Archives de la parole), historical recordings, radio.
- **URL:** https://gallica.bnf.fr/ (filter: type de document "Enregistrement sonore"; conditions: https://www.bnf.fr/fr/conditions-dutilisation-de-gallica)
- **License:** ⚠️ Per-item "Droits" field. Verified 2026-10-07: Europeana PRO states Gallica materials are "royalty-free and available free of charge when used strictly for private purpose"; Wave-20 verification stands — commercial reuse of even PD-marked items needs a BnF agreement. Check the item's rights statement, then the CGU.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Companion to the existing general Gallica entry — this is the audio-specific rights lane. BnF sound archive holds 1M+ recordings total; only the digitized Gallica subset is online. [Wave 23 Lane A]

#### Library and Archives Canada — Virtual Gramophone ⚠️ per-item copyright
- **What:** LAC's discography of Canadian 78rpm recordings (c. 1900–1950s) — early Canadian music, speeches, humour; full label transcriptions per record.
- **URL:** https://www.bac-lac.gc.ca/eng/discover/films-videos-sound-recordings/virtual-gramophone/
- **License:** ⚠️ Per item — LAC transcribes each record's label rights notice; no blanket reuse grant. Verified 2026-10-07: pre-1955 Canadian sound recordings are commonly public domain under Canadian rules (LAC public-domain guidelines), but donor/label restrictions can still apply — confirm on the item page.
- **Free tier:** free streaming/reference
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strongest North-American PD-78rpm lane after the IA Great 78 quarantine. [Wave 23 Lane A]

#### National Library of Australia — Oral History and Folklore collection ⚠️ per-item access conditions
- **What:** NLA's OH&F collection — Australia's most significant oral-history interview and folklore field-recording program (incl. extensive musician interviews); 1,000+ recordings delivered online with timed summaries/transcripts.
- **URL:** https://www.library.gov.au/services/copyright-library-collections/rights-and-oral-history-and-folklore-collection (rights page)
- **License:** ⚠️ Per-item access conditions set by interviewees (verified 2026-10-07 on NLA's own rights page): tiers range from "open for research, personal copies and public use" (usable) to "written permission required for public use" (clearance needed). Check each record's access statement.
- **Free tier:** free streaming (open tier)
- **Repo lane:** trippedd (dialogue/VO reference)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Companion to the existing Trove entry — this is the audio-oral-history rights lane. Published sound recordings: 70 years from publication (AU). [Wave 23 Lane A]

#### National Library of Israel — National Sound Archive ⚠️ per-item "Possible uses"
- **What:** The NLI Music Department's National Sound Archive — the world's largest collection of ethnographic and commercial recordings of Israeli and Jewish music (records, CDs, tapes; half commercial via legal deposit/purchase, half field/interview/Kol Yisrael recordings).
- **URL:** https://www.nli.org.il/en/at-your-service/who-we-are/collections/music-collection (usage FAQ: https://www.nli.org.il/en/at-your-service/reference/online-access)
- **License:** ⚠️ Per item — NLI's own FAQ (verified 2026-10-07): "The NLI does not own the copyright of the items in its collections… On each item's information page you will find a section labeled 'Possible uses'" — check it per item.
- **Free tier:** free streaming (where permitted)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** [Wave 23 Lane A]

#### Österreichische Mediathek ⚠️ reference archive — per-recording rights
- **What:** Austria's national audio/video archive (shellac, vinyl, tapes, DAT, CDs, video; incl. the Günther Schifter inter-war shellac collection, post-war Rot-Weiß-Rot radio, Burgtheater premieres from 1955) — online portals incl. "Österreich am Wort" (9,000+ recordings).
- **URL:** https://www.mediathek.at/ (Austrian National Library use terms: https://www.onb.ac.at/en/use)
- **License:** ⚠️ Reference archive — no blanket reuse. Verified 2026-10-07: ONB's use page states ONB asserts no copyright of its own over online content but "the user must clarify any existing third-party rights to the content individually before any subsequent use."
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Commercial reuse = individual clearance per recording. [Wave 23 Lane A]

#### Swiss National Sound Archives (Fonoteca) ⚠️ streaming open, reuse licensed
- **What:** The sound archive of Switzerland — a section of the Swiss National Library; 500,000+ sound carriers (classical, rock, jazz, folk, spoken word, field recordings, interviews).
- **URL:** https://www.fonoteca.ch/
- **License:** ⚠️ Verified 2026-10-07: online catalogue searchable and recordings listenable via the website / ~50 AV stations; copying "possible for private purposes against payment and on request also for professional purposes" — i.e. reuse is paid/permission-based, not open.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Reference value high, reuse cost non-zero — budget for licensing if sampled. [Wave 23 Lane A]

#### BAnQ numérique ⚠️ CC/PD license badges per item
- **What:** The digital portal of Bibliothèque et Archives nationales du Québec (Quebec's national library + archives) — 3M+ digitized documents; legal deposit covers sound recordings since 1992.
- **URL:** https://numerique.banq.qc.ca/
- **License:** ⚠️ Per-item badges — verified 2026-10-07: since spring 2019 BAnQ marks works with Creative Commons / public-domain badges (100,000 documents released into the public domain); filter by the item's licence badge.
- **Free tier:** free access
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Francophone-North-American counterpart to Gallica's rights regime. [Wave 23 Lane A]

#### Memobase (Memoriav) ⚠️ per-item rights
- **What:** Switzerland's national AV-heritage network portal — aggregates AV metadata from 67 Swiss institutions (incl. the Swiss National Sound Archives, Cinémathèque suisse).
- **URL:** https://memobase.ch/
- **License:** ⚠️ Per-item rights — verified 2026-10-07: Swiss Federal Archives notes that publishing or commercially using held AV records requires a permit; rights vary by contributing institution — check per item.
- **Free tier:** free discovery/streaming
- **Repo lane:** trippedd (music/sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Discovery layer, not a rights grant — pair with the Fonoteca entry. [Wave 23 Lane A]

---

## Honest negatives (diligence, not entries)

### Netlabel audits — NC-majority (verified via archive.org licenseurl, 2026-10-07)
The following IA sub-collections were fully audited and are **NC-majority** (typically 85–100% BY-NC*). Representative counts: sirona-records 871/887 NC; mahorka 478/506; eg0cide 236/261; netwaves 738/784 (+CC case study: BY-NC-SA); monokrak 237/283; pueblo_nuevo 266/283; panospria 90/98; deepindub 150/219; labelnetlabel 44/51; webbed_hand 288/295 (own site: CC BY-NC-ND 3.0 — Wave 20); comfort_stand 83/87; netwaves-bpm 201/230; zimmer 168/214; 1bit_wonder 33/33; takepillsdie 214/223; wm 117/123; afmusic 143/162; miga 49/51; no-source 64/71; nishi 73/119; zeromoon 123/176; bfw-recordings 234/256; yesnowave 132/139; dadaist-audio 187/187; murmure-intemporel 190/190; mnmnrecords 568/573; jazzaria 565/567; o2label 298/325; dienstbar 417/470; cianorbe 647/663; postunder 51/65; headphonica 107/121; sp-net 115 other + 40 NC; abandonment 167/167; psychocandies-netlabel 167/168; 17sons 173/175; ghgrnetlabel 159/175; racketinmyhead 211/236; surrism-phonoethics 232/238; le-colibri-necrophile 211/321; mindblasting 277/286; free-music-charts 52/65; vkrsradio 113/116; sociopath-recordings 253/274; candymind 19/32; non_quality_audio 322 other + 54 NC; lostfrog 192/213; ffs 154/155; bad-panda 97/106; free_sample_zone 50/51; birdsong 25/40; dubroom 65/68; postmoderncore 88/88; love-torture 259/263; dna-production 203/208; mine-all-mine-records 193/200; senmuthdiscography 208/212 NC (Senmuth — no clean grant found). **Rule reinforced: "free netlabel" ≠ commercial-safe.**

### Netlabel audits — unverifiable / dead
- **test_tube (Test Tube/Monocromatica):** 58/58 items with NO licenseurl; every release page says "licensed under a Creative Commons License" with variant unpinned — carried over from Wave 20, unchanged. ❓
- **ende-records:** 630 items, zero licenseurl metadata — unverifiable. ❓
- **killyourownarchive:** 420/500 unknown. ❓
- **rawcoffinrec:** 352/352 unknown. ❓
- **mimi:** 273/273 unknown. ❓
- **embajadoresdelamusicacolombiana:** 227/227 unknown. ❓
- **sutemos:** label site down since 2012 (domain parked); 29 IA items mostly unlicensed — no verifiable license statement. ❓
- **Thinner:** no CC grant — label pivoted commercial (GEMA-era paid downloads per tokafi interview); site dead. 🚫
- **Couchblip:** no license statement found on any accessible source. ❓
- **Brad Sucks:** site returned HTTP 500 on fetch 2026-10-07 — upstream license statement unverifiable this pass. ❓
- **danosongs.com (Dan-O):** current site is a personal-brand page with no reuse terms (old royalty-free licensing page gone). ❓
- **Tryad:** secondary sources confirm a CC release but variant unpinned; band site dead. ❓
- **Starfrosch:** blog/podcast "mostly Creative Commons" — no pinned blanket grant. ❓

### National-library AV — excluded / already covered
- **DNB Deutsches Musikarchiv (Leipzig):** physical/reading-room access only (German National Library card required) — no open digital AV reuse; its open-AV contribution flows through Europeana Sounds (entered above). 🚫 as standalone.
- **musicSG (National Library Board, Singapore):** NLB Digital Library Terms of Use — "download and print the Materials on this website for personal, non-commercial use only"; access "where the copyrights granted by the owners permit." No commercial grant. 🚫 NC.
- **British Library Sounds:** already catalogued as 🚫 no-commercial (Wave 16). Not duplicated.
- **Polona / BDH / Finna / Trove / Gallica-general / NB Norway:** AV-adjacent portals already catalogued — not duplicated; this wave adds only the AV-specific rights lanes.

---

## Method note
- **Dedup:** every candidate name/identifier grepped against `docs/RESOURCE_CATALOG.md` before inclusion (case-insensitive). Waves 19/20 netlabel entries (kahvi, treetrunk, noisecollector, oloil, r-archives, deepxrec, hazard_records, kraimusic, ozkye, stroboskop, genetic-trance, clinical-archives, monotonik, ektoplazm, etc.) and Wave 16–22 national-library entries (Gallica, Polona, BDH, Finna, Trove, NB Norway, BL Sounds, NDL Search API) were skipped as dups.
- **IA audits:** archive.org `advancedsearch.php`, `collection:<id> AND mediatype:audio`, fields `identifier,title,licenseurl,uploader,date`; classification: clean = CC0/PDM/plain-CC-BY; nc = BY-NC*; other = BY-SA/BY-ND; unknown = no licenseurl. 90 collections audited this wave (batches 1–3). Raw JSON kept in this folder.
- **License claims:** verified from the upstream source itself (label release-page metadata, library rights/terms pages, CC directory). Where only secondary sources existed, the entry says so.
- **No artifacts fabricated:** no downloads, no audio pulls this wave; URLs are live pages/APIs checked 2026-10-07.

## Sources checked (all 2026-10-07)
- archive.org advancedsearch API (90 netlabel collections + netlabels parent collection: 77,007 audio items, 2,014 sub-collections)
- https://archive.org/details/netlabels (parent collection page; JS-heavy — counts via API)
- http://sonicsquirrel.net/detail/label/on_mix/524 ; http://sonicsquirrel.net/detail/label/Starfrosch/1529 (label metadata)
- https://en.paperblog.com/10-more-netlabels-to-follow-1307708/ (Southern City's Lab CC claim)
- https://creativecommons.org/learn/features/opsound ; https://en.wikipedia.org/wiki/Opsound (Opsound BY-SA pool)
- https://wiki.creativecommons.org/index.php?title=Shtooka_Project_-_free_audio_collections_of_words (Shtooka CC directory)
- https://www.dnb.de/EN/Professionell/ProjekteKooperationen/Projektarchiv/2017/europeanaSounds/europeanaSounds_node.html ; https://www.dnb.de/EN/Ueber-uns/Presse/ArchivPM2014/europeanaSounds.html (Europeana Sounds 600k)
- https://dl.ndl.go.jp/view/download/digidepo_9551749_po_NDL-Newsletter192_928.pdf (NDL Rekion: 48,700 recordings; 1,090 expired-copyright online)
- https://www.infodocket.com/2017/12/22/japan-national-diet-library-makes-approximately-300-more-historical-audio-recordings-available-online/ (NDL announcement)
- https://pro.europeana.eu/data/gallica-is-the-digital-library-of-the-bibliotheque-nationale-de-france-bnf (Gallica royalty-free/private-use)
- https://www.bac-lac.gc.ca/eng/discover/films-videos-sound-recordings/virtual-gramophone/ (Virtual Gramophone)
- https://www.library.gov.au/services/copyright-library-collections/rights-and-oral-history-and-folklore-collection (NLA OH&F rights)
- https://www.nli.org.il/en/at-your-service/who-we-are/collections/music-collection ; https://www.nli.org.il/en/at-your-service/reference/online-access (NLI Sound Archive; "Possible uses" FAQ)
- https://www.onb.ac.at/en/use (ONB third-party-rights rule)
- https://en.wikipedia.org/wiki/Österreichische_Mediathek ; https://en.wikipedia.org/wiki/Swiss_National_Sound_Archives (Mediathek / Fonoteca scope)
- https://www.fonoteca.ch/ ; https://www.lugano.ch/en/vivere-lugano/cultura-e-tempo-libero/biblioteche/fonoteca-nazionale-svizzera/ (Fonoteca: section of Swiss NL; paid/permission reuse)
- https://en.wikipedia.org/wiki/BAnQ_num%C3%A9rique (BAnQ CC/PD badges since 2019; 100k PD docs)
- https://www.nlb.gov.sg/main/Terms-of-Use (musicSG NC — negative)
- https://en.wikipedia.org/wiki/German_Music_Archive (DMA physical-access only — negative)
