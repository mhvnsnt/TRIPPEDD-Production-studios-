### EBU-TT Live reference implementations — Wave 22 (+5)

#### EBU-TT XSD schema family (ebu org) ⚠️ mixed — two BSD-3, two unlicensed
- **What:** The machine-readable EBU-TT schema set: ebu-tt (Part 1), ebu-tt-xsd, ebu-tt-m-xsd (metadata mapping), ebu-tt-3-xsd (Live) — the normative XSDs any EBU-TT implementation validates against
- **URL:** https://github.com/ebu/ebu-tt / https://github.com/ebu/ebu-tt-xsd / https://github.com/ebu/ebu-tt-m-xsd / https://github.com/ebu/ebu-tt-3-xsd
- **License:** ⚠️ Mixed: ebu-tt-xsd and ebu-tt-m-xsd are BSD-3-Clause (verified 2026-10-07: GitHub API spdx_id); ebu-tt and ebu-tt-3-xsd carry NO license assertion — schemas themselves are informative publications of the EBU spec family, but reuse the unlicensed repos only for validation, not redistribution
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Use these XSDs to validate ttconv/imscJS output before treating it as broadcast-grade EBU-TT. [Wave 22 Lane A]

#### imsced (IRT) ✅ commercial-safe
- **What:** IRT's web-based IMSC subtitle editor (Vue) — author and preview IMSC/EBU-TT-D documents in the browser against the IMSC spec
- **URL:** https://github.com/IRT-Open-Source/imsced
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id IRT-Open-Source/imsced)
- **Free tier:** N/A (self-hosted web app)
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** From the same IRT team behind the SCF conversion framework already in the catalog — consistent broadcast-subtitle lineage. [Wave 22 Lane A]

#### xcf_suite_ttml (IRT) ✅ commercial-safe
- **What:** IRT's XSLT transform suite for TTML — profile, validate, and convert TTML documents (the XSLT companion to the SCF framework)
- **URL:** https://github.com/IRT-Open-Source/xcf_suite_ttml
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id IRT-Open-Source/xcf_suite_ttml)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** XSLT transforms run anywhere (even in-browser) — handy for EBU-TT-D profiling without a Python dependency. [Wave 22 Lane A]

#### benchmarkstt (EBU) ✅ commercial-safe
- **What:** EBU's open AI benchmarking toolkit for speech-to-text services — score ASR engines on accuracy/latency for live-subtitling workflows
- **URL:** https://github.com/ebu/benchmarkstt
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id ebu/benchmarkstt)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/live-STT)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** EBU-TT Live needs a live caption source — this is how you objectively pick the STT engine (Whisper/faster-whisper/Vosk/sherpa) feeding it. [Wave 22 Lane A]

#### dash.js EBU-TT-D subtitling branch (EBU) ✅ commercial-safe
- **What:** EBU's fork of dash.js with EBU-TT-D subtitle rendering in HTML/CSS overlay — the reference DASH player integration for EBU-TT-D (later merged upstream)
- **URL:** https://github.com/ebu/dash.js/tree/ebu-subtitling-dev
- **License:** ✅ BSD-3-Clause (verified 2026-10-07: LICENSE.md on the repo's master branch opens with the BSD license grant; same license family as upstream dash.js)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Reference implementation for rendering EBU-TT-D in a DASH web player — relevant if episodes ever ship with broadcast-style caption tracks. [Wave 22 Lane A]

### National-library catalog APIs & open data — Wave 22 (+26)

#### DigitalNZ API ⚠️ metadata-open, per-item rights
- **What:** Aggregated NZ cultural-heritage metadata API — millions of items from Aotearoa institutions (titles, descriptions, dates, creators) + pointers to partner items
- **URL:** https://digitalnz.org/developers
- **License:** ⚠️ "The API is free and open for anyone to use" for metadata; the API returns pointers/thumbnails to partner items — item reuse governed by each content partner (verified 2026-10-07 via the official Developers page; see Developer API Terms of Use)
- **Free tier:** Free, no key mentioned
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Metadata-only aggregation — great discovery index, but every reuse decision happens on the partner's own rights statement. [Wave 22 Lane A]

#### NLS Data Foundry ✅ CC0 open datasets
- **What:** National Library of Scotland's open-data publishing platform — digitised collections with METS/ALTO, image files, plain text, MARCXML/Dublin Core metadata, and map/spatial data
- **URL:** https://data.nls.uk/data/
- **License:** ✅ Datasets released under Creative Commons CC0 (verified 2026-10-07: dataset analyses cite "License: Creative Commons CC-0"; one dataset dual CC0 + OGL-UK-3.0) — confirm per-dataset page
- **Free tier:** Free downloads
- **Repo lane:** trippedd (digitization/corpora)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Full OCR text + ALTO for digitised collections — a ready-made historical-text corpus with clean licensing. [Wave 22 Lane A]

#### NLS Historic Maps API ✅ CC-BY 3.0
- **What:** National Library of Scotland's historic-map tile/API service (maps.nls.uk) — georeferenced OS and military maps as embeddable layers
- **URL:** https://maps.nls.uk/projects/api/
- **License:** ✅ CC BY 3.0 Unported (verified 2026-10-07: "Licence and terms of use" on the official API page — embed, display, derive, with attribution to NLS)
- **Free tier:** Free (MapTiler Cloud key for tiles)
- **Repo lane:** trippedd (bg plates/maps)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Attribution required — "National Library of Scotland" + link, in the work's documentation for derivatives. [Wave 22 Lane A]

#### BNE datos.bne.es ⚠️ linked open data — verify per dataset
- **What:** Biblioteca Nacional de España's Linked Open Data portal — SPARQL/RDF over BNE collections and authority data
- **URL:** https://datos.bne.es/inicio.html
- **License:** ⚠️ Published as Linked Open Data (verified 2026-10-07: portal describes itself as LOD publication); BNE's legal notice governs reuse — verify per dataset before production use
- **Free tier:** Free
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Authority-data reconciliation (Spanish names/subjects) is the main win; media rights stay per-item. [Wave 22 Lane A]

#### DDB API ⚠️ CC0 metadata, per-object media rights
- **What:** Deutsche Digitale Bibliothek API — 40M+ objects from ~500 German museums, archives, libraries (books, images, audio, video) via REST/JSON+XML (EDM)
- **URL:** https://api.deutsche-digitale-bibliothek.de
- **License:** ⚠️ v2 read routes public, no key; metadata CC0 (no attribution required); object *media* carry per-object rights (verified 2026-10-07 via API docs and DDB's own "all object pages indicate how you may reuse an object")
- **Free tier:** Free, keyless (v2 reads)
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The metadata layer is the safe part — treat every media file as rights-reserved until its object page says otherwise. [Wave 22 Lane A]

#### LOC JSON API ⚠️ keyless, per-item rights statements
- **What:** Library of Congress JSON/YAML API over loc.gov — collections metadata plus IIIF image services, full-text OCR services, and A/V streaming microservices
- **URL:** https://www.loc.gov/apis/
- **License:** ⚠️ API public and keyless (verified 2026-10-07: official API docs); rights live on each item's rights statement — the API exposes them, it doesn't waive them
- **Free tier:** Free, keyless
- **Repo lane:** trippedd (digitization/discovery)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Includes IIIF + OCR-text endpoints — programmatic access to one of the world's largest digitization programs. Filter by rights statement before reuse. [Wave 22 Lane A]

#### NDL Search API ⚠️ application required, per-provider licensing
- **What:** National Diet Library of Japan's federated search API (NDL Search) — books, articles, digitized materials across Japanese institutions
- **URL:** https://ndlsearch.ndl.go.jp/en/help/api
- **License:** ⚠️ Use requires an application form (commercial orgs included); metadata licensing varies per providing institution — "check the list of API-providing databases to see whether the metadata you want to use is licensed" (verified 2026-10-07)
- **Free tier:** Application-based
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Discovery index for Japanese material; the NDL Digital Collections entry's download prohibition still applies to the content itself. [Wave 22 Lane A]

#### KBR (Royal Library of Belgium) ❓ no public API terms found
- **What:** Belgium's national library — BelgicaPress newspaper portal, opac.kbr.be catalogue, digitized collections
- **URL:** https://www.kbr.be/en
- **License:** ❓ No public API or developer terms found (checked 2026-10-07); BelgicaPress portal exists but carries no blanket reuse grant visible — verify per item
- **Free tier:** Free browsing
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-only until KBR publishes API/open-data terms. [Wave 22 Lane A]

#### Google Books API ⚠️ ToS-gated, no commercial use without permission
- **What:** Google's Books API family — volume search, metadata, and Embedded Viewer for book content
- **URL:** https://developers.google.com/books
- **License:** ⚠️ Governed by Google's API Terms of Service (developers.google.com/books/terms): not a replacement for commercial services; no commercial use without Google's written permission; metadata may be cached but not redistributed in bulk; 1,000 req/day unauthenticated (verified 2026-10-07)
- **Free tier:** 1,000 requests/day/IP without key
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Metadata lookup only for our purposes — never a content source; prefer Open Library/LOC for anything reused. [Wave 22 Lane A]

#### Open Library API ⚠️ free, mission-scoped usage guidelines
- **What:** Internet Archive's Open Library APIs — book/author search, covers, works/editions, reading logs; monthly bulk data dumps
- **URL:** https://openlibrary.org/developers/api
- **License:** ⚠️ Free keyless API with usage guidelines (verified 2026-10-07: "not intended to serve as a data backend for high-traffic commercial services"; identify with User-Agent+email; bulk via dumps) — metadata dumps are openly downloadable; covers via IA have their own terms
- **Free tier:** Free (1 req/s default, 3 req/s identified)
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Use dumps for bulk work, API for human-scale lookup — and respect the volunteer-funded infrastructure. [Wave 22 Lane A]

#### BHL API ⚠️ key required, per-item rights
- **What:** Biodiversity Heritage Library API v3 — 59M+ pages of biodiversity literature (15th–21st c.), taxonomic name indexing, full-text search
- **URL:** https://www.biodiversitylibrary.org/api3
- **License:** ⚠️ API key required (free, from getapikey.aspx) (verified 2026-10-07: BHL's own API announcements); content is open-access literature but partners have also contributed in-copyright material with permission — check per-item rights
- **Free tier:** Free key
- **Repo lane:** trippedd (digitization/corpora)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Vintage natural-history plates are the prize here — but "open access" ≠ public domain on every item. [Wave 22 Lane A]

#### Papers Past (National Library of NZ) ⚠️ freely available, mostly pre-1950
- **What:** NLNZ's digitized newspaper/magazine archive — millions of searchable articles for local history and genealogy
- **URL:** https://paperspast.natlib.govt.nz
- **License:** ⚠️ "New Zealand's freely available online research tool" (verified 2026-10-07: official About page); overwhelmingly pre-1950 newspapers (out of copyright under NZ's life+50 term) — confirm per-title rights before reuse
- **Free tier:** Free
- **Repo lane:** trippedd (digitization/corpora)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strong period-text source for Australasia; no public API — harvest via the site's own interfaces within their terms. [Wave 22 Lane A]

#### TNA Discovery API ⚠️ OGL v3.0 for catalogue content
- **What:** The National Archives (UK) Discovery catalogue API — 32M+ descriptions of records across 2,500+ archives
- **URL:** https://www.nationalarchives.gov.uk/developer/
- **License:** ⚠️ nationalarchives.gov.uk content under the Open Government Licence v3.0 "except where otherwise stated" (verified 2026-10-07: site footer on the developer pages); digitized record images carry their own terms
- **Free tier:** Free
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Catalogue metadata under OGL is the safe layer; treat record images as per-item. [Wave 22 Lane A]

#### Canadiana ⚠️ public-domain focus, per-item check
- **What:** Canadian documentary-heritage digitization (CRKN) — 60M+ pages of books, newspapers, government documents, focused on public-domain printed materials
- **URL:** https://www.canadiana.ca
- **License:** ⚠️ "Worked to digitize Canadian heritage with a focus mainly on public domain printed materials" (verified 2026-10-07: Internet Archive's access-to-knowledge writeup); Heritage Project exclusivity windows have rolled back to open access — verify per collection
- **Free tier:** Free
- **Repo lane:** trippedd (digitization/corpora)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** One of the best PD Canadiana sources; still check each collection's stated terms. [Wave 22 Lane A]

#### David Rumsey Map Collection ⚠️ CC-licensed downloads, per-item copyright
- **What:** 150,000+ digitized historical maps (16th–21st c.) — the premier open map collection for period cartography
- **URL:** https://www.davidrumsey.com
- **License:** ⚠️ "By downloading any images from this site, you agree to the terms of that [Creative Commons] license" (verified 2026-10-07: davidrumsey.com/about); users must satisfy copyright holders unless materials are PD — confirm the CC variant and per-map rights
- **Free tier:** Free downloads
- **Repo lane:** trippedd (bg plates/maps)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Verify the exact CC variant on download — the site gates downloads behind license acceptance for a reason. [Wave 22 Lane A]

#### VIAF ✅ ODC-BY
- **What:** OCLC's Virtual International Authority File — 37 agencies in 29 countries' authority data linked into cluster records; the reconciliation backbone for names across national libraries
- **URL:** https://www.oclc.org/developer/api/oclc-apis/viaf.en.html
- **License:** ✅ "VIAF data is available under the Open Data Commons Attribution License (ODC-BY)" (verified 2026-10-07: OCLC Developer Network); attribution: "contains information from VIAF… made available under the ODC Attribution License"
- **Free tier:** Free API
- **Repo lane:** trippedd (research/metadata)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pairs with OpenRefine for reconciling harvested catalog metadata — attribution line required in derivatives. [Wave 22 Lane A]

#### WorldCat Search API ⚠️ WSKey required, ODC-BY linked data
- **What:** OCLC's WorldCat search API + linked-data views — the global union catalogue as an API
- **URL:** https://www.oclc.org/developer/api/oclc-apis/worldcat-search.en.html
- **License:** ⚠️ API requires WSKey + agreement; WorldCat.org linked data (incl. downloadable datasets) under ODC-BY with community norms (verified 2026-10-07: OCLC data-licensing docs); OCLC identifiers themselves are public domain
- **Free tier:** Key-gated
- **Repo lane:** trippedd (research/metadata)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Use the ODC-BY linked-data dumps where possible instead of the keyed API. [Wave 22 Lane A]

#### Wikidata ✅ CC0 structured data
- **What:** The structured-data backbone behind Wikipedia — 100M+ items (people, places, works) with a keyless JSON API and SPARQL endpoint
- **URL:** https://www.wikidata.org
- **License:** ✅ "All structured data from the main, Property, Lexeme, and EntitySchema namespaces is available under CC0" (verified 2026-10-07: Wikidata:Copyright page); text namespaces are CC BY-SA
- **Free tier:** Free, keyless
- **Repo lane:** trippedd (research/metadata)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The reconciliation target for OpenRefine/VIAF workflows — CC0 means no attribution friction on the structured data. [Wave 22 Lane A]

#### KB Sweden — LIBRIS ⚠️ national union catalogue, per-record terms
- **What:** Sweden's national library union catalogue (libris.kb.se) — authority data and bibliographic records for Swedish collections
- **URL:** https://libris.kb.se
- **License:** ⚠️ LIBRIS data is published for reuse by KB; no blanket commercial-use statement found on the public pages (checked 2026-10-07) — verify per-record/per-dataset terms before production use
- **Free tier:** Free
- **Repo lane:** trippedd (research/metadata)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Authority reconciliation for Swedish names/subjects; KB's open-data pages are the source of truth per dataset. [Wave 22 Lane A]

#### Royal Danish Library (KB Denmark) ❓ terms unverified this pass
- **What:** Denmark's national library — digital collections, historic newspapers, manuscripts (kb.dk)
- **URL:** https://www.kb.dk/en
- **License:** ❓ No clear open-data/API reuse terms found on public pages (checked 2026-10-07) — verify per collection
- **Free tier:** Free browsing
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-only until KB publishes reuse terms. [Wave 22 Lane A]

#### National Library of Wales ⚠️ per-collection rights
- **What:** Wales' national library — digital gallery of maps, photographs, manuscripts with IIIF delivery
- **URL:** https://www.library.wales/discover/digital-gallery
- **License:** ⚠️ Free browsing; no blanket reuse grant found on the digital-gallery pages (checked 2026-10-07) — verify per-item rights statements
- **Free tier:** Free
- **Repo lane:** trippedd (bg plates/research)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** IIIF endpoints make harvesting easy — which is exactly why the per-item rights check matters. [Wave 22 Lane A]

#### BNP — Biblioteca Nacional de Portugal ⚠️ per-item rights
- **What:** Portugal's national library — Biblioteca Nacional Digital with digitized books, maps, iconography
- **URL:** https://www.bnportugal.gov.pt
- **License:** ⚠️ No blanket reuse grant found on public pages (checked 2026-10-07) — verify per-item rights before reuse
- **Free tier:** Free browsing
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research source for Portuguese-language material; rights stay per item. [Wave 22 Lane A]

#### National Library of Norway — API ⚠️ keyless, per-item rights
- **What:** NB Norway's API (api.nb.no, live 2026-10-07) over the national digital collection — books, newspapers, photographs, and the digitized-audio holdings
- **URL:** https://api.nb.no
- **License:** ⚠️ API reachable and public (verified 2026-10-07); item rights per the NLN rights regime — rightscleared/PD items stream openly, everything else is on-premises (see the National Library of Norway entry's TONO/1958 note)
- **Free tier:** Free
- **Repo lane:** trippedd (research/discovery)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Programmatic route to the same 63,000-album audio holdings — filter by rights statement before any reuse. [Wave 22 Lane A]

#### NLB Singapore ❓ terms unverified this pass
- **What:** National Library Board Singapore — eResources portal, digitized newspapers (NewspaperSG), BookSG
- **URL:** https://www.nlb.gov.sg
- **License:** ❓ No clear blanket reuse terms found on public pages (checked 2026-10-07) — verify per resource
- **Free tier:** Free browsing (some resources Singapore-only)
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-only; several NLB resources are geo-restricted regardless of rights. [Wave 22 Lane A]

#### National Library of Greece ❓ terms unverified this pass
- **What:** Greece's national library — digital collections of manuscripts, newspapers, maps (nlg.gr)
- **URL:** https://www.nlg.gr
- **License:** ❓ No clear reuse terms found on public pages (checked 2026-10-07) — verify per collection
- **Free tier:** Free browsing
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-only until NLG publishes reuse terms. [Wave 22 Lane A]

#### National Library of Ireland ⚠️ IIIF delivery, per-item rights
- **What:** NLI's digital collections — photographs, manuscripts, prints with IIIF image delivery and catalogue APIs
- **URL:** https://www.nli.ie/en/udlist/digital-resources.aspx (live 2026-10-07)
- **License:** ⚠️ IIIF delivery confirmed via the digital-resources pages; no blanket reuse grant found (checked 2026-10-07) — verify per-item rights statements
- **Free tier:** Free
- **Repo lane:** trippedd (bg plates/research)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strong Irish photography holdings for period reference — rights stay per item. [Wave 22 Lane A]

#### OpenAlex ✅ CC0 scholarly metadata
- **What:** Open scholarly metadata graph — 300M+ works, authors, sources, institutions, topics; keyless REST API + SPARQL-like OQL
- **URL:** https://docs.openalex.org/how-to-use-the-api
- **License:** ✅ "All data is CC0 — no license worries, ever" (verified 2026-10-07: official API reference); free to start, no key (free key raises quota 10x)
- **Free tier:** Free keyless; free key for higher quota
- **Repo lane:** trippedd (research/metadata)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** CC0 makes this the cleanest scholarly-metadata source in the catalog — use it before Google Books for anything reused. [Wave 22 Lane A]

#### Unpaywall ⚠️ free, email-gated — data license unstated on API page
- **What:** Open database of 57M+ free scholarly articles — DOI lookup for OA locations, harvested from 50,000+ publishers/repositories
- **URL:** https://unpaywall.org/products/api
- **License:** ⚠️ "The REST API gives anyone free, programmatic access"; email required as URL parameter; 100,000 calls/day (verified 2026-10-07: official API page) — data license not stated there, verify before bulk reuse
- **Free tier:** 100k calls/day with email
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** OA-location lookup only — the articles themselves carry their publishers' licenses. [Wave 22 Lane A]
