# Wave 24 Lane A — netlabel long-tail part 3 + Scandinavian/Baltic national-library AV + PD-78rpm label deep-dives

**Entries proposed: 38** (`####` entries below) · **Honest negatives documented: 60+** · Audit date: 2026-10-07
Coordinator: append-only into RESOURCE_CATALOG.md; do NOT renumber existing rows. Dedup greps run pre-append (see Method).

---

## Method note

- **Dedup:** every candidate name/identifier grepped against `docs/RESOURCE_CATALOG.md` (case-insensitive) before inclusion. Waves 19–23 netlabel entries (genetic-trance, treetrunk, oloil, noisecollector, kahvi, monotonik, deepxrec, clinicalarchives, dustedwaxkingdom, kreislauf, phonocake, kraimusic, etc.), Wave 21/23 national-library entries (NB Norway, KB Digitalt, Mediastream, Digi.kansalliskirjasto.fi, Finna, DIGAR, NLI, Gallica audio, Europeana Sounds, NDL Rekion, LAC Virtual Gramophone, NB Norway music library), and 78rpm entries (Great 78, DAHR general, UCSB Cylinders, IA parent 78 collection, AFRS, British Pathé, U.S. Marine Band modern recordings, National Jukebox) were skipped as dups. Per-label 78rpm entries below are NEW (no label-specific entries existed).
- **IA netlabel audits:** archive.org `advancedsearch.php`, `collection:<id> AND mediatype:audio`, `rows=10000`, fields `identifier,title,licenseurl,uploader,date`; local classification: clean = CC0/PDM/plain-CC-BY; nc = BY-NC*; other = BY-SA/BY-ND; unknown = no licenseurl. 60 collections audited this wave (batches 4–5; raw JSON: `w24_netlabel_batch4.json`, `w24_netlabel_batch5.json`). NOTE: the `facets` parameter of advancedsearch.php is currently rejected server-side (`[UNSUPPORTED_VALUE]` for any facets value) — faceting was done client-side from full field pulls instead.
- **License claims:** verified from the upstream source itself (library rights/terms pages, LoC collection pages, label upload metadata). Where only secondary sources existed, the entry says so.
- **PD-date rule used throughout (US sound recordings, Music Modernization Act):** pre-1923 = PD since 2018; 1923–1946 = 100 years from publication (so through-1925 published recordings are PD as of 2026-10-07; 1926 recordings go PD 2027-01-01). EU sound recordings = 70 years from publication (pre-1956 PD in EU). Edison is special: LoC/Citizen DJ documents ALL Edison-company recordings 1890–1929 as PD via the NPS asset transfer.
- **No artifacts fabricated:** no downloads or audio pulls this wave; URLs are live pages/APIs checked 2026-10-07.

---

## Pocket 1 — Netlabel long-tail, part 3 (1 entry + 60 honest negatives)

Wave-23's 90-collection sweep found zero clean-majority labels. This wave audited 60 more IA netlabel sub-collections (batches 4–5). Result: **one clean-majority survivor** (below); everything else was NC-majority, unknown-majority, or already cataloged. The four other clean-majority collections found (genetic-trance 63%, treetrunk 65%, oloil 98%, noisecollector 51%) are already in the catalog (entries 21087/21097/21117/21107) — re-audited counts confirm their badges still hold.

### Honest negatives (not entries — diligence record)

- **NC-majority:** rumpfunkrecords (21/22 NC), deepxrec (524/599 NC), clinicalarchives (515/528 NC), bumpfoot (499/503 NC), monotonik, blocsonic (422/424 NC), dustedwaxkingdom (393/398 NC), asaguare (377/382 NC), kreislauf (233/234 NC), we-are-all-ghosts (196/216 NC), fwonk (190/201 NC), electronic-musik (188/197 NC), phonocake (143/161 NC), nostressnetlabel (151/154 NC), amp_records (138/151 NC), ruidemos (95/142 NC), green-field-recordings (110/139 NC), fuselab (101/139 NC), just-not-normal (135/137 NC), haklofirecord (131/134 NC), section-27 (127/130 NC), timetheory (124/130 NC), happypuppy (108/124 NC), ouimnet, basic_sounds (87/123 NC), stoneage-records (123/123 NC), rebound (119/121 NC), mav-records (114/116 NC), abdicate_cell (111/114 NC), digital-diamonds (105/114 NC), kittyonfire (110/112 NC), silent-flow (157/162 NC), irish-metal-archive (172/266 NC).
- **Unknown-majority (unverifiable):** immoralbasementrec (1,780/1,795 no licenseurl — largest unaudited collection, still unverifiable), unclassedmedia (297/322 unknown), deathrootssyndicate (144/144 unknown), 1834label (138/138 unknown), illphabetik (118/120 unknown), god (130/223 unknown), 20kbps, hanahata-discography, top40, oracle-online.
- **SA/ND-majority (not commercial-safe):** usc-label (300/312 BY-SA/BY-ND), bayview-financial-trading-group (219/307 other — mislabeled spam collection), ammd-label (155/161 other), nks-international (87/121 other), stillborntwinsrecords (66/123 other), hippocamp (38 other + 66 unknown).
- **Mixed, no majority:** kahvi (69 clean / 18 NC / 136 other / 44 unknown of 267 — already cataloged), kraimusic (60/71/22/15 of 168 — already cataloged), c_mshot_records, robo-robotica, rumpfunkrecords.

#### Maravines (netlabel-Maravines) ⚠️ clean-majority (94%) — per-item check mandatory

- **What:** IA netlabel sub-collection of the NJ folk-rock duo The Maravines (Union City, NJ; Mint 400 Records) — 112 self-uploaded items (albums, instrumentals, live excerpts).
- **URL:** https://archive.org/search?query=collection%3Anetlabel-Maravines
- **License:** ⚠️ Clean-majority but NOT blanket: 105 of 112 items carry clean licenseurls (78× PDM 1.0 http, 18× PDM 1.0 https, 8× CC-BY 4.0, 1× CC0; verified 2026-10-07); 2× BY-NC, 5× no licenseurl. The PDM marks are the band's own self-dedication of their uploads — credible but uploader-asserted. MANDATORY per-item check: at least one item contains covers of Haddaway ("What Is Love?") and Nirvana ("All Apologies") — cover recordings do NOT inherit the PDM grant on the underlying compositions.
- **Free tier:** free streaming + downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Only new clean-majority label in 60 collections audited this wave. Use the PDM/CC-BY originals only; skip anything with a cover or third-party composition. [Wave 24 Lane A]

---

## Pocket 2 — Scandinavian/Baltic national-library AV (19 entries)

Wave-21 covered the Nordic national libraries' general portals (NB digital/Bokhylla, Digi.kansalliskirjasto.fi, Mediastream, KB Digitalt). This wave targets their **AV-specific** holdings and rights statements — film, broadcast, and sound archives not previously cataloged.

#### Svensk mediedatabas (SMDB) — KB Sweden ⚠️ per-item rights; AV discovery layer

- **What:** The National Library of Sweden's search engine for its AV legal-deposit collections — TV/radio broadcasts (SR, SVT, UR, TV4 since 1979), cinema films, video, Swedish phonorecords (near-complete from the late 19th century), computer games, multimedia; ~8M hours. Absorbed the former Statens ljud- och bildarkiv (SLBA) in 2009.
- **URL:** https://smdb.kb.se/ (KB's own privacy notice confirms SMDB's purpose: "Preservation, digitisation of, and providing access to collected material" — https://www.kb.se/eng/about-us/processing-of-personal-data.html, checked 2026-10-07)
- **License:** ⚠️ Per-item rights — KB's standing posture (verified on KB Digitalt, Wave 21): items not marked "Begränsad åtkomst" (Limited Access) are copyright-free; limited-access items require the user to clear rights. Legal-deposit AV is overwhelmingly in-copyright — treat SMDB as a discovery index, not a reuse grant.
- **Free tier:** free search; on-site/reading-room access for restricted material
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The phonorecord metadata (complete Swedish discography from the 1890s) is the highest-value lane — use it to date PD-era Swedish 78s, then source transfers elsewhere. [Wave 24 Lane A]

#### Filmarkivet.se (KB + Swedish Film Institute) ⚠️ streaming-only; reuse by permission

- **What:** ~2,000 Swedish films 1897–present, freely streamable — documentaries and newsreels dominate, plus commercials and children's films. Joint service of the National Library of Sweden and the Swedish Film Institute.
- **URL:** https://www.kb.se/eng/loans-and-services/search-services/filmarkivet.se.html
- **License:** ⚠️ "For copyright reasons, it is not allowed to download the videos. If you want to re-use them, please contact filmarkivet.se@filminstitutet.se." (verified 2026-10-07 on KB's own page) — streaming is free, any reuse needs a written grant.
- **Free tier:** free streaming
- **Repo lane:** trippedd (archives/footage)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5 (clearance per film)
- **Status:** not-started
- **Notes:** Reference goldmine for period Swedish visuals; the pre-1928 newsreel slice is the strongest PD-candidate lane, but each film still needs its own clearance. [Wave 24 Lane A]

#### KAVI — Elonet (Finnish National Audiovisual Institute) ⚠️ filmographic data; per-item media rights

- **What:** KAVI's open film database (elonet.finna.fi) — the Finnish National Filmography: all full-length films premiered in Finnish cinemas from 1907 (The Moonshiners) onward (~1,540 titles), plus shorts, imported productions, cast/crew, release history, press coverage; stills and posters per film.
- **URL:** http://elonet.finna.fi (KAVI mission and history verified via https://en.wikipedia.org/wiki/National_Audiovisual_Institute_(Finland), checked 2026-10-07: formed 2014 from the Finnish Film Archive (est. 1957) + Board of Film Classification)
- **License:** ⚠️ The filmographic metadata is open; film stills/posters carry per-item rights — KAVI's statutory mission is to make films available "for cultural, educational, and research purposes," not a commercial reuse grant. Check each item.
- **Free tier:** free database access
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Discovery layer for Finnish film heritage; pair with Finna's per-record usageRights (Wave 21) for machine-readable rights on linked objects. [Wave 24 Lane A]

#### Yle Elävä arkisto (Living Archive) ⚠️ streaming-only; broadcast rights reserved

- **What:** Finnish public broadcaster Yle's online archive (since 2006) — radio/TV programmes, photos and films back to 1935, with journalistic background articles; a curated "showcases" slice is also on Vimeo (174 videos, 6 collections).
- **URL:** https://vimeo.com/ylearkisto/collections (verified showcase entry point; main archive on yle.fi — Elävä arkisto, verified via https://en.wikipedia.org/wiki/Yleisradio, checked 2026-10-07)
- **License:** ⚠️ Yle's online publishing followed "comprehensive negotiations with associations representing journalists, actors, authors, musicians, composers, along with all other copyright holders" — i.e. streaming is cleared, reuse is not granted. Treat as reference/streaming only.
- **Free tier:** free streaming
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Finnish period-broadcast reference; no download/reuse path — do not treat streaming availability as clearance. [Wave 24 Lane A]

#### Finlandia-Katsaus newsreels (EFG/KAVI) ⚠️ viewing-only; NC reuse

- **What:** The complete collection of 700 Finlandia-Katsaus newsreels (1943–1964) — Finland's civilian counterweight to wartime front newsreels, then post-war leisure/consumption subjects — presented via the European Film Gateway from KAVI's holdings.
- **URL:** https://europeanfilmgateway.eu/node/153
- **License:** ⚠️ EFG terms (verified 2026-10-07 via https://portal.efg.d4science.org/about_efg/faq): "Only non-commercial, personal use of the website's content is permitted. All other rights being reserved" — viewing only, no downloads, reuse only via the holding archive.
- **Free tier:** free viewing
- **Repo lane:** trippedd (archives/footage)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Honest negative for production use; high reference value for 1940s–60s Finnish period detail. [Wave 24 Lane A]

#### DFI — Filmcentralen (Danish Film Institute) ⚠️ free streaming; per-film rights

- **What:** The Danish Film Institute's streaming service for Danish short and documentary films — hundreds of titles, recent releases plus digitally restored classics, with background articles and thematic collections.
- **URL:** https://www.dfi.dk/en/node/49160 (DFI's own Filmcentralen facts & figures, verified 2026-10-07)
- **License:** ⚠️ Free to watch (Danish/Faroese/Greenlandic IP); DFI's streaming rights "vary according to the terms under which the individual film has been supported" — no blanket reuse grant, no downloads. Streaming ≠ clearance.
- **Free tier:** free streaming (DK IP)
- **Repo lane:** trippedd (archives/footage)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Reference only for production; contact DFI per film for any reuse. Distinct from the silent-film portal below. [Wave 24 Lane A]

#### stumfilm.dk — DFI Danish silent-film portal ⚠️ free streaming; per-film rights

- **What:** The Danish Film Institute's silent-film streaming site — the entire surviving Danish silent-film heritage (415 titles, 1897–1928, 350+ hours) digitized and streamed free, with posters, photos, scripts and contemporary reviews per film.
- **URL:** https://WWW.STUMFILM.DK/en/stumfilm/about-us (verified 2026-10-07; completion announced https://www.dfi.dk/en/node/91117)
- **License:** ⚠️ Free streaming for everyone; DFI asserts no blanket reuse/PD grant on the portal — per-film rights check required before any reuse (films are 1897–1928, so many are strong PD candidates under EU rules, but verify per title).
- **Free tier:** free streaming
- **Repo lane:** trippedd (archives/footage)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Highest-value Danish AV source found this wave — 350 hours of pre-1929 film free to view; the clearance work is per-film, not per-portal. [Wave 24 Lane A]

#### DR Bonanza — Danish Broadcasting Corporation archive ⚠️ streaming-only

- **What:** DR's online archive of classic Danish TV and radio programmes (children's radio, drama, Melodi Grand Prix finals, music shows) — the broadcaster's own nostalgia/archive service.
- **URL:** https://www.dr.dk/bonanza/serie/276/ivanhoe/ (example series page, verified 2026-10-07; Bonanza described at https://eurovisionary.com/eurovision-news/dr-put-old-danish-finals-internet-full-length)
- **License:** ⚠️ DR streams its archive free; no public reuse/download grant found — treat as reference/streaming only, per-item rights with DR.
- **Free tier:** free streaming
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Danish broadcast-history reference; third-party "Podnanza" scrapes (friism.com) exist for podcast feeds but add no rights. [Wave 24 Lane A]

#### SVT Öppet arkiv (Swedish Television Open Archive) ⚠️ streaming-only; footage commercially licensed

- **What:** Swedish public broadcaster SVT's open archive of classic TV — news clips, SF-journal newsreels, historical programmes (SVT's total archive: 500,000+ hours back to 1896).
- **URL:** http://www.oppetarkiv.se (verified via multiple third-party references, checked 2026-10-07)
- **License:** ⚠️ Free streaming; SVT Archives sells professional footage licensing (verified via https://www.dok-leipzig.de/en/archive-market-svt: "Available for all types of professional licensing") — streaming availability is NOT a reuse grant.
- **Free tier:** free streaming
- **Repo lane:** trippedd (archives/footage)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 4/5 (licensing per clip)
- **Status:** not-started
- **Notes:** Reference only; budget for SVT's licensing desk if any clip is needed in production. [Wave 24 Lane A]

#### Estonian National Archives (Rahvusarhiiv) — free-use YouTube/EFG slice ✅ explicit free-use grant

- **What:** The National Archives of Estonia's Film Archive — its collection policy explicitly frees a defined online slice for reuse.
- **URL:** https://www.ra.ee/wp-content/uploads/2020/06/film-archives-collection-policy_vers.1.2_ENG.pdf (v1.2, 2020-06-18)
- **License:** ✅ §4.2.4 of the archive's own collection policy (verified 2026-10-07): "Material published on the YouTube channel of the National Archives and on the European Film Gateway portal may be used free of charge and without asking the archive for permission." Caveat: this covers the archive's own published slice — third-party rights in the underlying works still need per-item attention, and HD/4K copies are paid deliverables.
- **Free tier:** free use of the YouTube/EFG-published slice
- **Repo lane:** trippedd (archives/footage)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The clearest reuse grant found in any Baltic AV archive this wave — quote the policy section in the ingest log per item. [Wave 24 Lane A]

#### EFIS — Estonian Film Database ⚠️ per-item rights; discovery layer

- **What:** The Estonian Film Institute's film database (efis.ee, since 2012) — 16,200+ records of Estonian films from 1912 (features, animation, documentaries, newsreels, educational/amateur/advertising films), with keyword search, filmmaker data, and links to the Arkaader VOD platform of the Estonian film archives.
- **URL:** https://efis.ee/en (verified 2026-10-07 via https://en.wikipedia.org/wiki/Estonian_Film_Database)
- **License:** ⚠️ Filmographic data open; AV objects carry per-item rights — the National Archives' policy notes most holdings are third-party-owned and online access is often preview/excerpt only, with full copies consultable in reading rooms.
- **Free tier:** free database; Arkaader VOD per its own terms
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Discovery index for Estonian film heritage back to 1912 — the pre-1956 slice is the EU-PD candidate lane, but each title needs its own clearance. [Wave 24 Lane A]

#### ERR arhiiv (Estonian Public Broadcasting archive) ⚠️ no public reuse grant — honest negative

- **What:** The programme archive of Eesti Rahvusringhääling (ERR), Estonia's public broadcaster — decades of Estonian TV/radio, partially streamable via arhiiv.err.ee.
- **URL:** https://www.riigiteataja.ee/en/eli/501042019011/consolide (Estonian Public Broadcasting Act, verified 2026-10-07)
- **License:** ⚠️ The Act requires ERR to make its programme archive available "under the conditions provided by law" and states archive use "for profit-making activities" follows a procedure set by the Broadcasting Council — i.e. streaming access exists, but there is NO public reuse grant. Treat as reference/streaming only.
- **Free tier:** free streaming (portal)
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Honest negative for production use — no verified reuse path; included so wiring crews don't mistake the streaming portal for a source. [Wave 24 Lane A]

#### Letonica — National Library of Latvia digital library (audio holdings) ⚠️ per-item rights

- **What:** The Latvian National Digital Library (Letonica, since 2006) — digitized newspapers, pictures, maps, books, sheet music AND audio recordings from the National Library of Latvia.
- **URL:** http://en.wikipedia.org/wiki/National_Library_of_Latvia (Letonica holdings verified 2026-10-07; audio recordings listed among digitized collections)
- **License:** ⚠️ Per-item rights — NLL publishes no blanket reuse grant; check each object's rights statement before any reuse.
- **Free tier:** free access
- **Repo lane:** trippedd (music/archives)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Companion to the existing DIGAR (Estonia) and Finna entries — completes the Baltic national-library digital set at the portal level; the Dainu skapis and Folklore Archive entries below are the audio-specific lanes. [Wave 24 Lane A]

#### Dainu skapis (Cabinet of Folksongs) — NLL ❓ digitized UNESCO folksong corpus; site terms unverified

- **What:** Krišjānis Barons' Cabinet of Folksongs — 268,815 pages of Latvian dainas (folk songs), riddles, proverbs and spells collected in the late 19th century; UNESCO Memory of the World (2001); housed at the National Library of Latvia since 2014; fully digitized and online since 2006.
- **URL:** http://www.dainuskapis.lv (verified via http://www.llti.lt/failai/12 Putelis.pdf and https://www.unesco.org/en/memory-world/dainu-skapis-cabinet-folksongs, checked 2026-10-07)
- **License:** ❓ The underlying song texts are 19th-century (PD by age), but the site's own reuse terms were not verified this pass — confirm before repurposing the site's presentation/scans.
- **Free tier:** free online access
- **Repo lane:** trippedd (dialogue/VO reference)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Text corpus (not audio) — lyric/VO reference for Baltic-flavored material; the melodies live in the Folklore Archive entry below. [Wave 24 Lane A]

#### Archives of Latvian Folklore — audio recordings ❓ per-item check

- **What:** The sound holdings of the Archives of Latvian Folklore (Latviešu folkloras krātuve) — field recordings of Latvian folk songs and instrumental music, including the audiovisual representations of folklore noted by UNESCO; Wikipedia's Daina article points to its online audio recordings.
- **URL:** https://en.wikipedia.org/wiki/Daina_(Latvia) (external link "Audio recordings of Latvian folklore (archives of Latvian folklore)" verified 2026-10-07; locate the archive's own audio portal from there)
- **License:** ❓ Per-item rights unverified this pass — archive field recordings, not a blanket grant. Check per recording before any reuse.
- **Free tier:** free listening (where offered)
- **Repo lane:** trippedd (music/sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The audio counterpart to the Dainu skapis text corpus above; verify the archive's own terms before ingest. [Wave 24 Lane A]

#### ePaveldas — Lithuanian virtual cultural heritage (sound recordings) ⚠️ per-item rights

- **What:** The National Library of Lithuania's virtual heritage portal (epaveldas.lt) — 11,000+ digitized sound recordings from the library's Image and Sound Archive, including 2,200+ Lithuanian vinyl and shellac records (first Lithuanian Zonophone issues, Riga 1907–1909 and Vilnius 1910–1911, diaspora pressings from the USA/Canada/South America).
- **URL:** https://www.iaml.info/wp-content/uploads/2015/03/lithuania_2014.pdf (IAML Lithuania national report 2014, verified 2026-10-07; portal at www.epaveldas.lt)
- **License:** ⚠️ Per-item rights — the library publishes no blanket reuse grant; the shellac-era items (1907–1920s) are strong PD-date candidates but each needs verification.
- **Free tier:** free online access
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The only Baltic portal with deep pre-1920 shellac coverage — the 1907–1925 Lithuanian pressings are the PD-date lane. [Wave 24 Lane A]

#### Lithuanian Folklore Archives — Folklore Audio Recordings database ❓ per-item check

- **What:** The sound collection of the Lithuanian Folklore Archives (Institute of Lithuanian Literature and Folklore) — phonograph cylinders, discs, tapes and digital recordings of authentic Lithuanian folk singers/musicians from the first half of the 20th century; cylinders and manuscripts digitized, recordings published in the Folklore Audio Recordings database.
- **URL:** https://www.dismarc.org/info/wp-content/uploads/2025/06/zharskiene.pdf (verified 2026-10-07: "sound recordings – in the database of Folklore Audio Recordings"; "anyone who is interested can now… listen to authentic performances of Lithuanian folk singers and musicians from the first half of the twentieth century")
- **License:** ❓ Per-item rights unverified this pass — field/archive recordings, no blanket grant found.
- **Free tier:** free listening (database)
- **Repo lane:** trippedd (music/sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Early-20th-century Lithuanian folk audio — the pre-1926 cylinder/disc slice is the PD-date lane; verify the archive's terms per item. [Wave 24 Lane A]

#### Lithuanian Theatre, Music and Cinema Museum (Google Arts & Culture) ❓ terms unverified

- **What:** Vilnius museum's Google Arts & Culture presence — exhibits on Lithuanian theatre, film, dance and music: 1,000+ Dobuzhinsky stage/costume designs (UNESCO-registered), first Lithuanian puppet film artifacts (1938), Pathé projectors, phonographs, records and sound recordings.
- **URL:** https://artsandculture.google.com/partner/lithuanian-theatre-music-and-cinema-museum (verified 2026-10-07)
- **License:** ❓ Google Arts & Culture partner terms; per-exhibit rights unverified this pass — reference only until checked.
- **Free tier:** free viewing
- **Repo lane:** trippedd (archives)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Visual-reference value (costume/stage design, early film equipment) more than audio; verify exhibit terms before any reuse. [Wave 24 Lane A]

#### EU Audiovisual Service (European Commission) ✅ CC BY 4.0 for EU-owned content

- **What:** The European Commission's Audiovisual Service — photos, videos and audio from EU institutions' activities, with a standing reuse policy.
- **URL:** https://audiovisual.ec.europa.eu/en/conditions-of-use
- **License:** ✅ "Unless otherwise indicated (e.g. in individual copyright notices), content owned by the EU on this website is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)" — "reuse is allowed provided appropriate credit is given and changes made are clearly indicated" (verified 2026-10-07). Per-file "Conditions of use" still govern; third-party elements inside EU content need their own clearance.
- **Free tier:** free reuse with attribution
- **Repo lane:** trippedd (footage/sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Notable find: a genuine CC-BY institutional AV source. Check the per-file notice (© European Union, 202X, CC BY 4.0) on each item used. [Wave 24 Lane A]

---

## Pocket 3 — PD 78rpm label deep-dives (17 entries)

Per-label rights research for labels whose pre-1926 (and Edison: 1890–1929) catalogs are verifiably public domain, with the discography/audio host for each. PD-date rule: US recordings published through 1925 are PD as of 2026-10-07 (MMA 100-year terms); 1926 recordings go PD 2027-01-01. Always verify the individual recording's publication date.

#### LoC — Inventing Entertainment: Edison Companies ✅ all Edison recordings 1890–1929 PD (NPS transfer)

- **What:** The Library of Congress digital collection of the Edison Companies' early entertainment output — 341 motion pictures, 81 disc sound recordings, photos, magazine articles (cylinders to be added).
- **URL:** https://www.loc.gov/collections/edison-company-motion-pictures-and-sound-recordings/about-this-collection/
- **License:** ✅ LoC's Citizen DJ project documents the PD basis (verified 2026-10-07 via https://github.com/libraryofcongress/citizen-dj/blob/HEAD/_collections/loc-edison.md): "All recordings made by the companies of Thomas A. Edison between 1890 and 1929 are in the public domain because the assets of Edison Records were transferred to the National Park Service, a federal agency, in the 1950s." — "free to use and reuse without restriction… even for commercial purposes."
- **Free tier:** free streaming/download
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** STRONGEST 78rpm-era finding this wave: the entire Edison catalog (Diamond Discs, Blue Amberols, cylinders, 1929 Needle Types) is PD — no date-filtering needed within 1890–1929. Per-item composition caution still applies (PD recording ≠ PD song). [Wave 24 Lane A]

#### DAHR — Edison discography (Thomas Edison National Historical Park transfers) ⚠️ streaming noncommercial; PD items downloadable

- **What:** The Discography of American Historical Recordings' complete Edison discography — 14,000+ recording sessions / 8,000+ published two-sided discs documented from TENHP's ledgers and cashbooks, with 7,400+ digitized Edison disc recordings (1910–1929, incl. unissued test pressings) available for listening via the UCSB/DAHR + National Park Service partnership.
- **URL:** https://www.library.ucsb.edu/news/thousands-rare-edison-disc-phonograph-recordings-released (partnership announcement, verified 2026-10-07; discography at adp.library.ucsb.edu)
- **License:** ⚠️ DAHR's standing terms (Wave 17 entry): free streaming is noncommercial; PD recordings downloadable — confirm each item's download grant. All 1890–1929 Edison recordings are PD per the NPS-transfer basis above, so the PD slice here is the whole Edison discography.
- **Free tier:** free streaming; PD downloads
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Use as the Edison dating/discography index (matrix numbers, dates, takes) alongside the LoC PD grant above; distinct from the general DAHR entry (which covers Victor/Columbia/Okeh/Brunswick/Vocalion). [Wave 24 Lane A]

#### NPS — Edison Recorded Sound Archive catalog ❓ 11,000 cylinders + 39,000 discs

- **What:** Thomas Edison National Historical Park's sound-archive holdings database (NPS LIBRIS Discovery Portal) — MARC catalog records for 11,000 cylinder records and 39,000 disc records preserved at the Edison Laboratory, West Orange NJ; majority are Edison recordings 1888–1929.
- **URL:** https://nps.gov/edis/learn/historyculture/search-the-catalog.htm (verified 2026-10-07)
- **License:** ❓ Catalog metadata free to search; per-recording reuse terms not stated on the catalog page — but the underlying Edison recordings 1890–1929 are PD via the NPS-transfer basis (LoC/Citizen DJ); confirm per item.
- **Free tier:** free catalog search
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The finding-aid layer for the Edison corpus — use to locate specific takes/matrices, then source audio from DAHR or LoC. [Wave 24 Lane A]

#### WFMU — Thomas Edison's Attic ⚠️ streaming reference; PD-era content

- **What:** Long-running WFMU program hosted by the audio curator of the Edison National Historic Site — Edison cylinder/disc rarities 1888–1929 (Tin Pan Alley, ragtime, vaudeville sketches, dance bands, country, classical, lab experiments), with full playlists naming exact label/matrix/year per track.
- **URL:** https://wfmu.org/playlists/shows/24614 (example playlist, verified 2026-10-07)
- **License:** ⚠️ The played recordings are 1888–1929 Edison material (PD via the NPS-transfer basis), but WFMU's streams are a broadcast service — no download/reuse grant. Use as a discovery/dating reference; source the actual transfers from LoC/DAHR.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The playlists are the value: exact disc/matrix/year citations for thousands of Edison sides — a human-curated PD-Edison index. Distinct from the FMA entries (different WFMU property). [Wave 24 Lane A]

#### LoC — Emile Berliner and the Birth of the Recording Industry ✅ date-PD (mid-1890s–1900 discs)

- **What:** The Library of Congress digital collection from the Emile Berliner Papers — 400+ manuscript items and 100+ Berliner Gramophone Co. sound recordings (band music, instrumentals, comedy, spoken word, opera, incl. Sousa Band and Buffalo Bill's 1890s recordings).
- **URL:** https://www.loc.gov/collections/emile-berliner/about-this-collection/
- **License:** ✅ Date-PD: "All the Berliner discs were produced from the mid-1890s to 1900" (LoC's own collection page, verified 2026-10-07) — every recording in the disc corpus predates 1923 by decades. Per-item composition caution still applies.
- **Free tier:** free streaming/download (LoC digital collections)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The earliest commercial disc recordings in existence, all PD — the 1890s Sousa Band sides are the military-band lane's oldest clean source. [Wave 24 Lane A]

#### Paramount Records (Wisconsin Chair Co., 1917–1932) ⚠️ date-PD per issue; discography refs

- **What:** The legendary "race records" label (Ma Rainey, Charley Patton, Blind Blake, Papa Charlie Jackson, Skip James) — 12000/13000 series from 1922; Black Swan's assets folded in 1924; dead by 1932.
- **URL:** http://oldtimeblues.net/tag/rare-labels/page/2/ (Old Time Blues label research, verified 2026-10-07: Paramount's 12000 race series, Black Swan asset purchase)
- **License:** ⚠️ Date-PD per issue: Paramount issues published 1922–1925 are PD as of 2026-10-07; 1926–1928 issues go PD 2027–2029; 1929–1932 issues remain protected into the 2030s. Verify each record's issue year — the label's peak blues years (1927–1930) are NOT yet PD. Discography: Max Vreede's "Paramount 12000/13000 Series" (cited in discographical literature).
- **Free tier:** free (research)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The early race-series sides (1922–1925: early Ma Rainey, Ida Cox, Papa Charlie Jackson's first sessions) are the shippable slice today; the famous 1928–1930 Delta blues sides are a calendar watchlist, not a source. [Wave 24 Lane A]

#### Black Swan Records (1921–1924) ⚠️ all PD — first Black-owned label

- **What:** The first Black-owned record company (Harry Pace, 1921) — Fletcher Henderson's Novelty Orchestra, Lulu Whidby, Ethel Waters' early sides; folded end of 1923, assets bought by Paramount (which reissued Black Swan masters as early Paramount 12000s).
- **URL:** http://oldtimeblues.net/tag/rare-labels/page/2/ (verified 2026-10-07: "the company folded at the end of 1923, and all of their assets were purchased by Paramount Records")
- **License:** ⚠️ All PD: every Black Swan issue was published 1921–1923 — the entire catalog is public domain. Note the Paramount reissues (e.g. Lulu Whidby's Black Swan 2005 → Paramount 12127) carry the ORIGINAL 1921 recording date for PD purposes.
- **Free tier:** free (research)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Cleanest PD story of any race label — 100% of the catalog is PD. Source transfers from IA's 78 collections; date-verify via the Paramount cross-reference above. [Wave 24 Lane A]

#### Gennett Records (Starr Piano Co., Richmond IN, 1916–1934) ⚠️ date-PD per issue

- **What:** The Starr Piano Company's label — recorded Louis Armstrong, Bix Beiderbecke, Jelly Roll Morton, King Oliver, Hoagy Carmichael, Gene Autry in Richmond, Indiana; the Starr-Gennett Foundation has digitized 400+ recordings, with 300+ publicly available at the IU East Campus library.
- **URL:** https://news.iu.edu/live/news/25555-wtiu-documentary-celebrates-local-history-of (IU: 300+ Gennett recordings public at IU East, verified 2026-10-07); copyright analysis at https://www.copyright.gov/docs/sound/comments/initial/20101127-D-Fulton.pdf (Starr-Gennett Foundation's own filing: pre-1923 PD, 1923–1934 under state law at the time — now MMA 100-year terms)
- **License:** ⚠️ Date-PD per issue: 1916–1925 issues PD as of 2026-10-07 (incl. the 1923 King Oliver/Jelly Roll Morton sessions); 1926–1930 issues go PD 2027–2031; 1931–1934 issues protected into the 2030s. The IU East public set is streaming-access — confirm download/reuse terms per item.
- **Free tier:** free streaming (IU East set)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The 1923–1925 Gennett jazz sides (Oliver, Morton, Bix's Wolverines) are the highest-value PD jazz 78s in existence — verify each issue year, then source transfers from IA. [Wave 24 Lane A]

#### Pathé Records (US/France) ⚠️ date-PD per issue; vertical-cut era all PD

- **What:** The French giant's US operation (Pathé Frères Phonograph Co., 1914–1930) — vertical-cut "sapphire ball" discs to 1922, lateral-cut Pathé Actuelle from 1920; the DAHR-published Rust's Guide to Discography documents the label's history and series.
- **URL:** https://adp.library.ucsb.edu/RustsGuidetoDiscography.pdf (Rust's Guide, Pathé section, verified 2026-10-07); community US Pathé 1915–1922 issue list: https://discogs.com/lists/Path%C3%A9-US/292793
- **License:** ⚠️ Date-PD per issue: the entire vertical-cut US catalog (1915–1922) is PD; Actuelle issues through 1925 are PD; 1926–1928 Actuelles go PD 2027–2029. French Pathé pressings: EU 70-year rule (pre-1956 PD in EU).
- **Free tier:** free (research)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The vertical-cut era is 100% PD but needs sapphire-ball transfers — IA's 78 collections hold Pathé sides; date-verify per issue. [Wave 24 Lane A]

#### Red Hot Jazz Archive ⚠️ site's own PD claim; streaming reference

- **What:** Brian Robertson's long-running archive of pre-1930 jazz — artist/band histories with streaming transfers of 1900s–1920s jazz 78s (Oliver, Morton, ODJB, Bix).
- **URL:** http://www.redhotjazz.com/info.html (site's legal/PD statement, verified via https://www.vintagejazz.net/_bandprivat/Red_Hot_Jazz_Archive.pdf, checked 2026-10-07)
- **License:** ⚠️ The site asserts "the majority of the works on this archive are in the public domain, because the copyrights have expired" (its own pre-MMA analysis) — treat as the site's claim, not a verified grant; streaming-only, no downloads. Cross-check each recording's date against the MMA rule (through-1925 = PD) before any reuse.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Discovery/dating reference for pre-1930 jazz 78s; the site's PD analysis predates the MMA — the through-1925 rule is now MORE permissive than the site claims. [Wave 24 Lane A]

#### i78s.org — Library of Historical Audio Recordings ⚠️ free registration; per-item rights

- **What:** Collector-run library of cylinder and 78-rpm transfers with discographical details and label scans — free streaming after free registration.
- **URL:** https://mainspringpress.org/category/i78s-org-resources-for-collectors-of-cylinder-and-78-records/ (Mainspring Press directory entry, verified 2026-10-07: "Free streaming of cylinder and 78-rpm records, with discographical details, label scans, and more (free registration required)")
- **License:** ⚠️ Per-item rights — the library streams transfers; no blanket reuse grant stated. Use as a discovery/label-ID reference; verify each recording's date and source before any reuse.
- **Free tier:** free streaming (registration)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The label scans are the high-value lane for identifying PD-era pressings (matrix/issue data visible on the labels themselves). [Wave 24 Lane A]

#### Mainspring Press ⚠️ NC — free discography e-books + Vintage Record Playlist

- **What:** Allan Sutton's vintage-record research press — award-winning discographies/reference books as FREE PDF e-books, plus the Vintage Record Playlist (streaming historic 78s/cylinders with annotations, artist photos, discographical details) and the James A. Drake celebrity interviews.
- **URL:** https://mainspringpress.org/category/i78s-org-resources-for-collectors-of-cylinder-and-78-records/ (verified 2026-10-07)
- **License:** ⚠️ "All titles are free to download for personal, non-commercial use" — the e-books are NC; the streaming playlist's per-recording terms need checking. Research lane only for the books.
- **Free tier:** free downloads (personal/non-commercial)
- **Repo lane:** trippedd (music/research)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The free discography e-books (incl. the revised Indestructible cylinder book, forthcoming on DAHR) are the scholarly backbone for PD-date verification — use for research, never ship the PDFs. [Wave 24 Lane A]

#### worldradiohistory.com — Talking Machine World ✅ PD-era trade press (1905–1928)

- **What:** Full-issue scans of Talking Machine World (1905–1928, renamed Talking Machine World and Radio Music Merchant in its final year) — the recording industry's main trade magazine: regional sales reports, new-release bulletins (with matrix/catalog data), artist activity, phonograph ads. Plus its successors (Talking Machine & Radio Weekly 1928–1933).
- **URL:** https://www.worldradiohistory.com/Talking_Machine_Radio_News.htm (verified 2026-10-07; sample issues: https://www.worldradiohistory.com/Archive-Talking-Machine/10s/Talking-Machine-1912-08.pdf)
- **License:** ✅ Every issue is 1905–1928 — the entire run is public domain by date. Free PDF downloads.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music/research)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The "Record Bulletin" pages (e.g. Sept 1912 issue, p.50) are contemporary release data — use to date PD-era 78s and to source period ad artwork (also PD) for title cards. Edison Phonograph Monthly (1903+) is archived on the same site. [Wave 24 Lane A]

#### U.S. Marine Band — 78rpm-era commercial recordings (Columbia/Edison/Victor, 1890s–1927) ⚠️ date-PD per issue

- **What:** The commercial 78rpm-era discography of "The President's Own" — ~200 cylinders for Columbia from 1890 (first large ensemble to record commercially), thousands of Columbia cylinders by 1897, Edison from June 1898, and 42 Victor titles 1906–1927 (incl. 1921 Marine Corps Institute sides, 1923 Edison Diamond Disc "Washington Post," 1927 Victor "Semper Fidelis").
- **URL:** https://loc.gov/static/programs/national-recording-preservation-board/documents/United-States-Marine-Band_Warfield.pdf (LoC recording history, verified 2026-10-07); sample IA transfer: https://archive.org/details/InternetJukebox.JPS.78 ("U.S. Field Artillery," 1917 Sousa 78)
- **License:** ⚠️ Date-PD per issue: 1890s–1925 commercial issues are PD; the 1926–1927 Victors go PD 2027–2028. Note: these are COMMERCIAL label recordings, not federal works — the PD basis is date, not government authorship. Distinct from the catalog's existing modern Marine Band entry (federal-PD current recordings).
- **Free tier:** free (IA transfers)
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The military-band lane's deepest PD vein — Sousa-era marches in period acoustic recordings. The Victor matrix data (e.g. B-25278, recorded 4/28/1921) in the LoC doc is the dating key. [Wave 24 Lane A]

#### juneberry78s.com — Roots Music Listening Room ⚠️ 1920s slice PD; 1930s not

- **What:** "The Roots Music Listening Room" — 2,000+ streaming transfers of 1920s–1930s folk and blues 78s.
- **URL:** www.juneberry78s.com/sounds/index.htm (verified via Tim Brooks' recording-history links, https://timbrooks.net/links-recording-history/, checked 2026-10-07)
- **License:** ⚠️ Date-PD per recording: the 1920s sides published through 1925 are PD; late-1920s sides go PD 2028–2030; 1930s sides remain protected. Streaming-only — no reuse grant stated; verify each recording's date and source transfers before any reuse.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Discovery/dating reference for PD-era roots 78s; Tim Brooks (Columbia Master Book Discography co-author) vouches for the site, which is the credibility signal. [Wave 24 Lane A]

#### oldtimeblues.net ❓ blog transfers of 1920s race-label 78s; no license stated

- **What:** Research blog with own transfers of 1920s blues/race 78s (Paramount, Black Swan, Gennett/Starr) — track-level discographical essays with recording dates, personnel, label scans and MP3s (e.g. Lulu Whidby/Paramount 1921, Papa Charlie Jackson/Paramount 1925, Gennett Christmas 1923 sides).
- **URL:** http://oldtimeblues.net/tag/1925/ (verified 2026-10-07)
- **License:** ❓ No license statement on the transfers — the underlying recordings cited (1921–1925 Paramount/Gennett/Black Swan) are date-PD, but the BLOG's MP3s are the author's own transfers with unstated terms. Do not ship the MP3s; use the discographical data, source audio elsewhere.
- **Free tier:** free streaming
- **Repo lane:** trippedd (music/research)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The discographical essays (exact recording dates, matrix/take data) are the value — treat as a dating index, not an audio source. [Wave 24 Lane A]

#### old78s.com — 78RPM Label Gallery ❓ dealer label-ID reference; images not cleared

- **What:** A 78rpm dealer's visual gallery of hundreds of 78rpm record labels (Ajax, Black Swan, Brunswick, Columbia, Edison, Gennett, Okeh, Paramount, Victor, Vocalion and dozens of obscure vertical-cut labels) — the fastest way to identify an unknown PD-era pressing from its label.
- **URL:** http://old78s.com/78rpm_label_gallery.php (verified 2026-10-07)
- **License:** ❓ The label IMAGES are the dealer's photos — not cleared for reuse. Use strictly as a visual identification reference (which label/series is this pressing?), never as an image source.
- **Free tier:** free viewing
- **Repo lane:** trippedd (music/research)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Label identification is the gating step for every date-PD workflow in this pocket — this gallery answers "what label/series is this?" in seconds. [Wave 24 Lane A]

#### Wikimedia Commons — PD-marked 78rpm transfers ✅ per-file PD marks

- **What:** Wikimedia Commons' collection of 78rpm audio transfers carrying explicit Public Domain marks (e.g. 1930 Imperial Japanese Army/Navy band 78s, Edison Diamond Disc label photos) — each file's PD rationale is stated on its file page.
- **URL:** https://commons.wikimedia.org/wiki/File:DiamondDiscLP.jpg (example PD-marked file, verified 2026-10-07)
- **License:** ✅ Per-file Public Domain marks (PDM 1.0 / PD-old / PD-US-expired) — verify the mark on each file's page; Commons' own licensing policy requires the PD rationale to be stated.
- **Free tier:** free downloads
- **Repo lane:** trippedd (music/scoring)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The only 78rpm audio source in this pocket with per-file PD assertions from a curation process — prefer Commons transfers over IA uploads when both exist, and keep the file-page URL as proof. [Wave 24 Lane A]
