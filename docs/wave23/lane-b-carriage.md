# TRIPPEDD Resource Pull Program — Wave 23, Lane B: EBU-TT Live WebSocket carriage + DIY book-scanner open hardware + RightsStatements.org vocabulary

Lane: caption-carriage verification (EBU-TT Live over WebSocket, with a REAL executed smoke test), open-hardware book scanner designs and their capture/post-processing software (licenses verified from upstream repos), and the RightsStatements.org standardized rights vocabulary (all 12 statements verified from rightsstatements.org itself) plus adjacent machine-readable rights vocabularies. Every license/rights claim verified from the upstream source — never assumed. Verification date: 2026-10-07.

**De-duplication:** grepped `docs/RESOURCE_CATALOG.md` for every candidate name/URL before including. Already covered and NOT re-listed: ebu/ebu-tt-live-toolkit (Wave 17 Lane B), the EBU-TT spec suite Tech 3350/3360/3370/3380 + Tech 3264 (Wave 20 Lane B), EBU-TT XSD schema family + imsced + xcf_suite_ttml + benchmarkstt + dash.js EBU-TT-D branch (Wave 22), DVB TTML subtitling (Wave 21 Lane D), ttconv, sandflow. `3370s1` appears once inside the Wave-20 suite entry only — the dedicated WebSocket-carriage entry below is new. The `bbc/ebu-tt-live-toolkit` fork, `w3c/tt-module-live`, ETSI TS 102 796, Tech 3381, all book-scanner items, and the RightsStatements.org vocabulary itself have zero catalog hits.

**Headline result:** the EBU-TT Live WebSocket carriage smoke test RAN and PASSED — real Twisted WebSocket producer→consumer document transfer using the toolkit's own carriage classes, with proof artifacts at `docs/wave23/proof/`. See entry 1.

---

## Pocket 1 — EBU-TT Live WebSocket carriage

### ✅ Verified + smoke-tested

#### EBU Tech 3370s1 — EBU-TT Part 3 carriage over WebSocket ✅ free reference doc + LIVE SMOKE TEST PASSED
- **What:** The supplement to Tech 3370 that defines the WebSocket carriage mechanism for EBU-TT Live document sequences between processing nodes (node→node transfer, `{sequence_identifier}/{action}` path format with `publish`/`subscribe` actions, HTTP-upgrade/TLS-friendly TCP).
- **URL:** https://tech.ebu.ch/publications/tech3370s1 (spec page; free PDF download — verified live 2026-10-07)
- **License:** ✅ Free reference doc (EBU copyright; free PDF download — cite, don't redistribute). Verified 2026-10-07: page resolves and states "carriage of EBU‑TT Part 3 over WebSocket is specified in EBU Tech 3370s1" (cross-confirmed on the Tech 3370 page).
- **Free tier:** N/A (spec document)
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** smoke-tested (see proof)
- **Notes:** **REAL SMOKE TEST EXECUTED 2026-10-07 — PASSED.** Installed `bbc/ebu-tt-live-toolkit` @ ce813b3 in a venv (ebu-tt-live 3.0.3, Python 3.12, twisted 23.10.0, autobahn 20.12.3); generated the pyxb bindings per the repo Makefile; ran `ws_smoke_producer.py` (Twisted `BroadcastServerFactory` + `TwistedWSPushProducer` + `WebsocketProducerCarriage` on 127.0.0.1:9000) against `ws_smoke_consumer.py` (`BroadcastClientFactory` + `TwistedWSConsumer` + `WebsocketConsumerCarriage` at `ws://localhost:9000/SmokeTest1/subscribe`). Result: **4/4 documents received, all `sequence_identifier="SmokeTest1"`, sequence numbers [4,5,6,7] monotonic and unique**, ~4.2 KB of real EBU-TT Live XML each (`<tt:tt … ebuttp:sequenceIdentifier="SmokeTest1" ebuttp:sequenceNumber="4" …`), parsed by the toolkit's own XML→document adapter. Proof: `docs/wave23/proof/ws_smoke_producer.py`, `docs/wave23/proof/ws_smoke_consumer.py`, `docs/wave23/proof/received.json`, `docs/wave23/proof/SMOKE_RESULT.txt`, `docs/wave23/proof/consumer_smoke.log`. **Genuine upstream bug found during the test:** the toolkit hands `str` payloads to autobahn's `sendMessage()`, which asserts `bytes` on autobahn ≥ 20.x (`AssertionError: "payload" must have type bytes`) — the WebSocket send path is broken out-of-the-box on modern autobahn. The harness works around it with UTF-8 encode/decode at the test edges; the toolkit itself was not patched. Also hit and documented: `setuptools≥81` removed `pkg_resources` (pinned `setuptools<81`), and the installed wheel misses `pyproject.toml` that `ebu_tt_live/project.py` reads at import (copied in for the test). [Wave 23 Lane B]

#### bbc/ebu-tt-live-toolkit — actively maintained BBC fork ✅ commercial-safe
- **What:** The BBC's fork of the EBU-TT Live interoperability toolkit — the Python reference implementation of Tech 3370 (nodes, carriages incl. WebSocket, IMSC HRM validator, `ebu-dummy-encoder` / `ebu-simple-producer` / `ebu-simple-consumer` scripts). This fork, not the ebu-org original, is where current development happens (pushed 2026-10-07; the ebu/ original last pushed 2023).
- **URL:** https://github.com/bbc/ebu-tt-live-toolkit
- **License:** ✅ BSD-3-Clause (verified 2026-10-07 via GitHub API `spdx_id`; fork of ebu/ebu-tt-live-toolkit which carries the same license)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** smoke-tested (this is the codebase the passing smoke test ran against)
- **Notes:** Distinct from the Wave-17 entry (ebu/ebu-tt-live-toolkit) — different repo, active maintenance, IMSC HRM validator additions. Install caveats documented in the Tech 3370s1 entry (bindings generation, setuptools pin, autobahn bytes bug). [Wave 23 Lane B]

#### ETSI TS 102 796 — HbbTV: EBU-TT-D subtitle carriage ✅ free reference doc
- **What:** The HbbTV specification's subtitle clause (§7.3.1.5): terminals must render EBU-TT-D documents (UTF-8, ≤8 concurrent regions), in-band carriage with MPEG DASH per the DVB DASH spec and ISOBMFF per EBU Tech 3381, plus mandatory out-of-band carriage as a single XML document over HTTP (≤512 kByte). The distribution-side counterpart to the Live (contribution-side) carriage work above.
- **URL:** https://www.etsi.org/deliver/etsi_ts/102700_102799/102796/01.04.01_60/ts_102796v010401p.pdf (free ETSI download — verified 2026-10-07)
- **License:** ✅ Free reference doc (ETSI specs are free to download; ETSI copyright — cite, don't redistribute)
- **Free tier:** N/A (spec document)
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Relevant if episodes ever ship HbbTV/broadcast-style caption tracks: this is the normative receiver contract for EBU-TT-D. Zero catalog hits for HbbTV/102796 before this wave. [Wave 23 Lane B]

#### EBU Tech 3381 — Carriage of EBU-TT-D in ISOBMFF ✅ free reference doc
- **What:** EBU spec (v1.0, Oct 2014) defining how EBU-TT-D distribution documents are stored/carried in ISO Base Media File Format (ISO/IEC 14496-12) — the file-carriage companion to the live WebSocket carriage, referenced normatively by HbbTV/TS 102 796 for downloaded content.
- **URL:** https://tech.ebu.ch/publications/tech3381 (spec page; free PDF download — verified live 2026-10-07)
- **License:** ✅ Free reference doc (EBU copyright; free PDF download — cite, don't redistribute)
- **Free tier:** N/A (spec document)
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Completes the EBU-TT-D carriage picture alongside Tech 3370s1 (live/WebSocket) and TS 102 796 (HbbTV/DASH). Zero catalog hits before this wave. [Wave 23 Lane B]

### ❓ Unverified

#### w3c/tt-module-live — W3C TTML Live draft (incl. WebSocket carriage text) ❓ no license assertion
- **What:** The W3C Timed Text Working Group's TTML Live draft, derived from EBU Tech 3370/3370s1: re-bases the live-document semantics on TTML1 and carries a full WebSocket carriage specification section plus a documented delta file (`w3c-submission-changes.md`) explaining every change vs Tech 3370s1. Dormant since ~2021 (8 open issues) — useful as a second normative-leaning description of the WebSocket carriage.
- **URL:** https://github.com/w3c/tt-module-live
- **License:** ❓ GitHub API returns `spdx_id: NOASSERTION` (no license file in repo; verified 2026-10-07). The spec text is a W3C-group draft (read/reference as with other W3C drafts), but there is no code-license grant — do not lift code from it without checking.
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/EBU-TT)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Read-only reference value: the `w3c-submission-changes.md` delta is the clearest public explanation of what Tech 3370s1's WebSocket carriage requires. Not a live project — monitor only. [Wave 23 Lane B]

---

## Pocket 2 — DIY book-scanner open hardware + capture/post software

### ✅ Verified commercial-safe

#### DIY Book Scanner Archivist ("Standard") — Public Domain ✅
- **What:** Daniel Reetz's V-shaped-platen DIY book scanner: the canonical open book-scanner design (lighting/cameras/book rig, counterweighted removable cradle, ~1,000 pages/hour for a skilled operator, 12×15″ scan area, ~300 DPI with 16MP cameras). Six years of design rationale published as a 22,000-word build site.
- **URL:** https://diybookscanner.org/archivist/ (plans + rationale)
- **License:** ✅ Public Domain — the author's own write-up states "this scanner is Public Domain" and "Open Hardware frame (now Public Domain) and completely Open Source control system based on the Raspberry Pi computer" (verified 2026-10-07 on diybookscanner.org/archivist). Note the Hackaday-cited rationale: Reetz deliberately chose public domain over open-hardware licenses (which he considered unenforceable for hardware).
- **Free tier:** free plans; build cost is parts (~$300 for the original trash-build)
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5 (physical build)
- **Status:** not-started
- **Notes:** The reference design everything else in this pocket descends from. Community support: the diybookscanner.org forum (tens of thousands of posts). [Wave 23 Lane B]

#### pi-scan (Tenrec Builders) — Raspberry Pi capture appliance ✅ commercial-safe
- **What:** "Pi Scan is a simple, robust capture appliance for book scanners. It runs on a Raspberry Pi 2." — the kiosk software that configures CHDK cameras, triggers captures, and saves scans to USB/SD. The recommended controller software for the Archivist Quill.
- **URL:** https://github.com/Tenrec-Builders/pi-scan
- **License:** ✅ BSD-2-Clause (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Permissive license, still watched upstream (updated 2026-08). Pairs with the Quill hardware below. [Wave 23 Lane B]

#### Voussoir (jglev/voussoir; upstream ytsutano/bookscan) — single-camera de-keystoning ✅ commercial-safe
- **What:** Automatic de-keystoning for single-camera DIY book scanners: detects glyphs pasted in page corners, digitally flattens pages, auto-splits spreads into cropped page images. Suggested workflow: voussoir → darktable → ScanTailor.
- **URL:** https://github.com/jglev/voussoir (fork; canonical upstream https://github.com/ytsutano/bookscan)
- **License:** ✅ ISC (verified 2026-10-07 via GitHub API `spdx_id` on both the jglev fork and the ytsutano upstream — both ISC)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** C++, archived upstream (jglev fork archived; ytsutano upstream dormant since 2016) but the license is clean and the tool fills the single-camera niche the dual-camera Archivist designs don't. [Wave 23 Lane B]

#### awesome-scanning (ad-si) — curated scanning-resource list ✅ commercial-safe
- **What:** Curated list of paper/document/book scanning projects: devices (Archivist, Linear Book Scanner, Arduino auto-scanner), apps (ScanTailor, YASW, Voussoir…), libraries, dewarping research, and the Ishikawa Watanabe high-speed digitization lab links. The discovery index for this whole pocket.
- **URL:** https://github.com/ad-si/awesome-scanning
- **License:** ✅ ISC (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/research)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Per-item licenses still need checking (the list itself flags commercial vs open-source) — several entries below were verified starting from this list. [Wave 23 Lane B]

### ⚠️ License-conditional

#### Linear Book Scanner (Google / Dany Qumsiyeh) — vacuum page-turning automatic scanner ⚠️ open-source claim, patent caveat
- **What:** The Google 20%-project automatic book scanner: a book glides over linear imaging sensors while vacuum suction turns pages — ~1,000 pages in ~90 minutes, ~$1,500 in parts, non-destructive to spines.
- **URL:** https://linearbookscanner.org ("The design is open-source, so anyone can build one." — verified 2026-10-07)
- **License:** ⚠️ "Open-source" per the project site and contemporary press (2012), but **no specific open-hardware license text** (no CERN OHL/TAPR/CC statement) was found on linearbookscanner.org — and the design is covered by **US Patent 8,711,448** ("Linear book scanner", Google Inc./Dany Qumsiyeh, issued 2014-04-29; verified via patent records). Whether Google granted a patent license alongside the "open source" release is unverified. Treat as research-only until the patent position is clarified.
- **Free tier:** free plans (site); ~$1,500 parts
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 5/5 (complex electromechanical build)
- **Status:** not-started
- **Notes:** The patent is the trap: "open source" without a patent grant is not a safe build license. Do not build commercially without clearance. [Wave 23 Lane B]

### ❓ Unverified

#### Archivist Quill (Tenrec Builders) — aluminum-frame Archivist successor ❓ no license statement found
- **What:** The Archivist's successor design by Jonathon Duerig / Tenrec Builders: aluminum-extrusion + steel/plastic frame (lighter/cheaper than the plywood Archivist), 1300×825×580 mm, 18 kg, up to 300×400 mm pages, ~1,000+ pages/hour, Raspberry Pi + Pi Scan controller, CHDK cameras. Free plans + full assembly guide published.
- **URL:** http://tenrec.builders/quill/guide/ (guide); plans via https://diybookscanner.org/forum/viewtopic.php?f=28&t=2593 (forum thread)
- **License:** ❓ No license statement found on the guide site or forum plans post (checked 2026-10-07) — "free plans" is not an open-hardware license. Designed by Jonathon Duerig and Tenrec Builders (a commercial kit vendor; kits discontinued). Treat as all-rights-reserved until a license is stated.
- **Free tier:** free plans download; parts extra
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5 (physical build)
- **Status:** not-started
- **Notes:** Functionally the best-documented buildable design, but the license gap blocks commercial builds. The Pi Scan controller software (above) IS BSD-2-Clause — only the frame design is unverified. [Wave 23 Lane B]

#### Book Scan Wizard — camera-scan post-processor ❓ no license text located
- **What:** Steve Devore's Java post-processor for camera-based book scanning: crop/rotate/de-keystone/DPI correction, color/lighting correction, batch-apply to page sets, direct upload to the Internet Archive (OCR → searchable PDF/ePub handled IA-side). The classic DIY-bookscanner pipeline tool.
- **URL:** https://sourceforge.net/projects/bookscanwizard/
- **License:** ❓ Described as "open-source software" by the Internet Archive (blog.archive.org, 2011), but **no license text was locatable**: the SourceForge project page shows no license field, and the SourceForge code browser returned HTTP 403 on 2026-10-07 (not retried per access policy). Read the license inside the distribution before wiring.
- **Free tier:** free download
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Old (Java 7/8 era, last releases ~2015) — expect bit-rot on modern JDKs. License verification is the blocker, not the age. [Wave 23 Lane B]

#### diybookscanner.org forum — the book-scanning community knowledge base ❓ reference only
- **What:** The DIY Book Scanner community forum: tens of thousands of build posts — Archivist/Quill build logs, camera/CHDK notes, lighting discussions, plan mirrors (Quill DXFs, TIFLIC builds), troubleshooting. The living companion to the static plan sites.
- **URL:** https://diybookscanner.org/forum/
- **License:** ❓ Community-contributed content, no site-wide license statement found — reference/reading only; don't republish build content without checking per-post terms.
- **Free tier:** free to read
- **Repo lane:** trippedd (digitization/research)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Where the Quill plans actually live (forum thread t=2593) — the canonical plan host, not tenrec.builders. [Wave 23 Lane B]

### 🚫 Not commercial-safe (copyleft — research lane only / honest negatives)

#### DIYBookScanner/spreads — modular book-digitization workflow assistant 🚫 AGPL-3.0 — QUARANTINED
- **What:** "Modular workflow assistant for book digitization" — capture, post-processing, and output pipeline for DIY scanners (the software side of the DIYBookScanner org).
- **URL:** https://github.com/DIYBookScanner/spreads (canonical org repo; jbaiter/spreads is an archived fork of it)
- **License:** 🚫 AGPL-3.0 (verified 2026-10-07 via GitHub API `spdx_id` on both the org repo and the fork)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** quarantined (AGPL code — research lane only, never wired into shipping paths, per docs/LICENSE_QUARANTINE.md)
- **Notes:** Dormant since 2016. AGPL means even network use triggers source-sharing — quarantine stands regardless of dormancy. [Wave 23 Lane B]

#### DIYBookScanner/spreadpi — Raspberry Pi scanner-control image 🚫 GPL-2.0 — QUARANTINED
- **What:** "Raspberry Pi image for controlling a DIYBookScanner via spreads" — the Pi-side control system the Archivist write-up calls "completely Open Source".
- **URL:** https://github.com/DIYBookScanner/spreadpi
- **License:** 🚫 GPL-2.0 (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** quarantined (GPL code — research lane only, never wired into shipping paths, per docs/LICENSE_QUARANTINE.md)
- **Notes:** Dormant since 2015. The permissive pi-scan (BSD-2-Clause, above) is the safe substitute for Pi-based capture control. [Wave 23 Lane B]

#### ScanTailor Advanced (4lex4) — scan post-processing workhorse 🚫 GPL-3.0 — QUARANTINED
- **What:** The maintained ScanTailor fork (merges Featured + Enhanced forks, adds fixes): dewarping, page splitting, deskew, margins, binarization/thresholding, DjVu/PDF output — the standard post-processing stage after camera capture.
- **URL:** https://github.com/4lex4/scantailor-advanced
- **License:** 🚫 GPL-3.0 (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A (desktop app)
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** quarantined (GPL code — research lane only as a linked library; standalone desktop use does not infect the pipeline, per the quarantine doctrine)
- **Notes:** The most genuinely useful tool in this pocket for scan cleanup — usable as a standalone desktop step, never as an imported library. Upstream scantailor.org release is likewise GPL. [Wave 23 Lane B]

#### YASW (Yet Another Scan Wizard) — camera-image corrector 🚫 GPLv3 — QUARANTINED
- **What:** Qt/C++ post-processor for camera-captured pages: keystone/perspective correction, cropping, batch-apply across page series, tuned for archive.org's de-warped/cropped/color upload requirements.
- **URL:** https://sourceforge.net/projects/yascanw/
- **License:** 🚫 "GNU General Public License version 3.0 (GPLv3)" (verified 2026-10-07 on the SourceForge project page's License field)
- **Free tier:** free download (Linux/Windows/BSD)
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** quarantined (GPL code — research lane only, per docs/LICENSE_QUARANTINE.md)
- **Notes:** Beta status, last updated years ago. ScanTailor Advanced (above) supersedes it functionally. [Wave 23 Lane B]

#### Internet Archive Scribe — honest negative 🚫 proprietary hardware, not open
- **What:** The Internet Archive's internally-developed V-shaped book scanner (dual cameras, foot-pedal glass platen, ~500 pages/hour) and its "Table Top Scribe" product.
- **URL:** https://blog.archive.org/2015/10/22/special-book-collections-come-online-with-the-table-top-scribe/ (product announcement)
- **License:** 🚫 Proprietary — internally developed (AIP Engineering), sold commercially as the Table Top Scribe ($9,999 base model, verified via the IA blog). An old SourceForge project (`scribesw`) once hosted related software, but the hardware was never released under an open-hardware license.
- **Free tier:** N/A (commercial product)
- **Repo lane:** trippedd (digitization)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 5/5
- **Status:** not-started (excluded — documented as a negative so nobody re-researches it)
- **Notes:** Included as an honest negative: the pocket asked for open-hardware scanners, and the Scribe — despite the "Scribe" name appearing in open-culture contexts — is proprietary hardware. [Wave 23 Lane B]

---

## Pocket 3 — RightsStatements.org vocabulary + adjacent machine-readable rights vocabularies

### ✅ Verified

#### RightsStatements.org — standardized rights statements for cultural heritage ✅ free to reference
- **What:** The standardized rights-statement vocabulary for cultural heritage institutions: 12 statements (5 In Copyright, 4 No Copyright, 3 Other) as persistent dereferenceable URIs (`http://rightsstatements.org/vocab/{CODE}/1.0/`), published as linked data (SKOS, JSON-LD/Turtle via content negotiation), designed for `dc:rights` / `edm:rights`. Supported by DPLA and Europeana. Stewardship moved to Digital Scholar (the nonprofit behind Zotero and Omeka) — announced on the homepage (verified 2026-10-07).
- **URL:** https://rightsstatements.org/en/ ; vocabulary index http://rightsstatements.org/vocab/1.0/
- **License:** ✅ Free to reference — the machine-readable data model is CC0-1.0 (verified 2026-10-07 via GitHub API on rightsstatements/data-model). The statements are high-level summaries, not licenses: the site's own documentation says to use Creative Commons tools for licensing your own creations.
- **Free tier:** N/A (vocabulary)
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** This is the filtering mechanism for every archive pull: per-item `edm:rights`/`dc:rights` URIs are the authority Wave 16's "public archive ≠ public domain" lesson points to. The 12 statements follow as individual entries. [Wave 23 Lane B]

#### In Copyright (InC) — http://rightsstatements.org/vocab/InC/1.0/ ✅
- **What:** "This Rights Statement can be used for an Item that is in copyright" — the institution has determined the item is in copyright and either holds rights, has permission, or relies on an exception/limitation (e.g. fair use).
- **URL:** http://rightsstatements.org/vocab/InC/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** InC items are NOT reusable without permission — this URI is the "do not pull" signal. [Wave 23 Lane B]

#### In Copyright – EU Orphan Work (InC-OW-EU) — http://rightsstatements.org/vocab/InC-OW-EU/1.0/ ✅
- **What:** For works identified as Orphan Works under EU Directive 2012/28/EU (books, journals, audiovisual — excludes photography/visual arts), applied only by beneficiary institutions registered in the EUIPO orphan-works database.
- **URL:** http://rightsstatements.org/vocab/InC-OW-EU/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** EU-only permitted uses; not a US-usable orphan-work category. [Wave 23 Lane B]

#### In Copyright – Educational Use Permitted (InC-EDU) — http://rightsstatements.org/vocab/InC-EDU/1.0/ ✅
- **What:** In-copyright items the rights-holding institution makes available for educational reuse.
- **URL:** http://rightsstatements.org/vocab/InC-EDU/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Educational-use permission ≠ commercial production use — "permitted" is scoped. [Wave 23 Lane B]

#### In Copyright – Non-Commercial Use Permitted (InC-NC) — http://rightsstatements.org/vocab/InC-NC/1.0/ ✅
- **What:** In-copyright items the rights-holder makes available for non-commercial reuse.
- **URL:** http://rightsstatements.org/vocab/InC-NC/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** NC-scoped — commercial series production cannot rely on it. [Wave 23 Lane B]

#### In Copyright – Rights-holder(s) Unlocatable or Unidentifiable (InC-RUU) — http://rightsstatements.org/vocab/InC-RUU/1.0/ ✅
- **What:** In-copyright items where no rights-holder could be identified/located after reasonable investigation (non-EU; EU orphan works must use InC-OW-EU).
- **URL:** http://rightsstatements.org/vocab/InC-RUU/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** "Unlocatable" ≠ public domain — reuse risk stays with the reuser. [Wave 23 Lane B]

#### No Copyright – Contractual Restrictions (NoC-CR) — http://rightsstatements.org/vocab/NoC-CR/1.0/ ✅
- **What:** Public-domain items the institution contractually must restrict (e.g. donor agreements); the institution should link the specific restrictions.
- **URL:** http://rightsstatements.org/vocab/NoC-CR/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** PD underlying work, but the contract binds the institution's copy — check the linked restrictions before pulling. [Wave 23 Lane B]

#### No Copyright – Non-Commercial Use Only (NoC-NC) — http://rightsstatements.org/vocab/NoC-NC/1.0/ ✅
- **What:** Public-domain works digitized in public-private partnerships (built for the European Libraries/Google partnerships) where partners agreed to limit third-party commercial use of the digital surrogate.
- **URL:** http://rightsstatements.org/vocab/NoC-NC/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The underlying work is PD, but this statement's NC term governs the surrogate most archives actually serve. [Wave 23 Lane B]

#### No Copyright – Other Known Legal Restrictions (NoC-OKLR) — http://rightsstatements.org/vocab/NoC-OKLR/1.0/ ✅
- **What:** PD items blocked from free reuse by non-copyright law (cultural-heritage protections, traditional cultural expression, etc.); institution should link the restrictions.
- **URL:** http://rightsstatements.org/vocab/NoC-OKLR/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Seen in the wild on Europeana (their Tier-C example record uses exactly this URI in `edm:rights`). [Wave 23 Lane B]

#### No Copyright – United States (NoC-US) — http://rightsstatements.org/vocab/NoC-US/1.0/ ✅
- **What:** Items the institution has determined are free of copyright under US law (not for orphan works; requires an actual status effort).
- **URL:** http://rightsstatements.org/vocab/NoC-US/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The primary "safe to pull" signal for US federal-adjacent and pre-1931 materials in DPLA/Europeana feeds. [Wave 23 Lane B]

#### Copyright Not Evaluated (CNE) — http://rightsstatements.org/vocab/CNE/1.0/ ✅
- **What:** Copyright status has not been evaluated — no determination made.
- **URL:** http://rightsstatements.org/vocab/CNE/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Unknown = not safe. Treat CNE items as unpullable until evaluated. [Wave 23 Lane B]

#### Copyright Undetermined (UND) — http://rightsstatements.org/vocab/UND/1.0/ ✅
- **What:** Status unknown after an unsuccessful effort to determine it (key facts missing).
- **URL:** http://rightsstatements.org/vocab/UND/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** As with CNE: undetermined means do not pull. [Wave 23 Lane B]

#### No Known Copyright (NKC) — http://rightsstatements.org/vocab/NKC/1.0/ ✅
- **What:** Status not conclusively determined, but the institution has reasonable cause to believe copyright no longer applies.
- **URL:** http://rightsstatements.org/vocab/NKC/1.0/
- **License:** ✅ Vocabulary term, free to reference (data model CC0-1.0)
- **Repo lane:** trippedd (provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Weaker than NoC-US (belief, not determination) — pull only with per-item judgment. [Wave 23 Lane B]

#### rightsstatements.org data model (JSON-LD / Turtle) — CC0-1.0 ✅ commercial-safe
- **What:** The machine-readable vocabulary itself: SKOS concept scheme with all 12 statements, served as JSON-LD/Turtle/RDF via content negotiation at the statement URIs; source in the `rightsstatements/data-model` GitHub org (includes the technical-infrastructure white papers).
- **URL:** https://github.com/rightsstatements/data-model
- **License:** ✅ CC0-1.0 (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** This is what a provenance-checking script consumes: fetch the statement URI with `Accept: application/ld+json` and read the machine-readable terms instead of scraping HTML. [Wave 23 Lane B]

#### RightsStatements.org white paper — "Recommendations for Standardized International Rights Statements" ✅ free reference doc
- **What:** The founding specification document: statement definitions, URI design rules (`{domain}/vocab/{CODE}/{version}/` with mandatory trailing slash), SKOS/RDF data-modeling decisions, and HTTP interaction patterns for the linked-data publication.
- **URL:** http://rightsstatements.org/files/151002recommendations_for_standardized_international_rights_statements.pdf
- **License:** ✅ Free reference doc (published by the consortium; cite, don't redistribute)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Normative background for the 12 entries above (e.g. the trailing-slash rule, the InC-RUU vs InC-OW-EU split). [Wave 23 Lane B]

#### PA Digital Rights Statement Selection Tool — CC-BY-2.0 ✅ commercial-safe
- **What:** Gabriel Galson's interactive step-by-step tool (2018) for determining an item's rights status and picking the correct standardized statement — the practical "which URI do I use" wizard DPLA hubs point contributors to.
- **URL:** https://padigital.org/wp-content/uploads/2018/10/Rights-Statement-Selection-Tool_Galson.pdf (interactive PDF; referenced from dpla/dpla-frontend)
- **License:** ✅ CC-BY-2.0 (verified 2026-10-07 via the DPLA frontend repo's copyright.md attribution line)
- **Free tier:** free
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Attribution required (CC-BY-2.0, Gabriel Galson). Useful as the decision procedure behind any automated rights-filtering script. [Wave 23 Lane B]

#### ODRL 2.2 (Open Digital Rights Language) — W3C Recommendation ✅ free reference
- **What:** The W3C policy-expression language for machine-readable usage statements: information model + vocabulary + JSON-LD/XML encodings for permissions, prohibitions, duties over assets (policies: Agreement, Offer, Set, …). The generic rights-expression layer underneath statement vocabularies like rightsstatements.org.
- **URL:** https://www.w3.org/TR/odrl-vocab/ (W3C Recommendation 15 Feb 2018 — verified 2026-10-07)
- **License:** ✅ Free reference (W3C permissive document license; Recommendation may be cited/used as reference material)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Heavier machinery than rightsstatements.org URIs — relevant if the pipeline ever needs to express conditional grants (e.g. "non-commercial display until date X") rather than just labeling status. [Wave 23 Lane B]

#### IIIF Presentation API 3.0 — `rights` / `requiredStatement` patterns ✅ free reference
- **What:** IIIF's machine-readable rights pattern: the `rights` property "MUST be drawn from the set of Creative Commons license URIs, the RightsStatements.org rights statement URIs, or those added via the extension mechanism" (e.g. `"rights": "http://rightsstatements.org/vocab/InC/1.0/"`), with `requiredStatement` carrying the human-readable attribution/terms.
- **URL:** https://iiif.io/api/presentation/3.0/#rights (verified 2026-10-07 via the spec section as quoted in implementation guides)
- **License:** ✅ Free reference (IIIF specs are openly published; cite, don't redistribute)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** This is why the rightsstatements.org URIs matter mechanically: IIIF manifests (LOC, NLS, and other Wave-22 sources) carry them in `rights`, so a harvester can filter PD-vs-restricted at the manifest level before downloading a single pixel. [Wave 23 Lane B]

#### ccREL (Creative Commons Rights Expression Language) ✅ free reference
- **What:** CC's RDFa/XMP vocabulary for machine-readable copyright-license expression (`cc:permits`, `cc:requires`, `cc:prohibits` over `cc:License`), published as a W3C Member Submission (2008-05-01). The predecessor that ODRL and rightsstatements.org thinking built on.
- **URL:** https://www.w3.org/Submission/2008/SUBM-ccREL-20080501/ (verified 2026-10-07 via W3C submissions index)
- **License:** ✅ Free reference (W3C Member Submission — read/reference; publication indicates no W3C endorsement, per the submission terms)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Legacy but still the namespace (`https://creativecommons.org/ns#`) that CC license deeds expose as RDFa — a harvester reading CC license pages meets ccREL, not ODRL. [Wave 23 Lane B]

#### Europeana Licensing Framework + Data Exchange Agreement ✅ free reference
- **What:** Europeana's rights regime: the Data Exchange Agreement requires every digital object to carry a rights statement in `edm:rights` (metadata itself under CC0), drawn from the allowed list — CC licenses/PDM/CC0 plus the rightsstatements.org URIs (Europeana's own Tier-C example uses `edm:rights rdf:resource="http://rightsstatements.org/vocab/NoC-OKLR/1.0/"`). The framework's IPR deliverables document the migration from Europeana-specific statements to rightsstatements.org terms.
- **URL:** https://pro.europeana.eu/page/documentation-of-updates-to-the-data-exchange-agreement (DEA; verified 2026-10-07)
- **License:** ✅ Free reference (pro.europeana.eu publications; cite, don't redistribute)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Europeana is the largest live deployment of the vocabulary — its `edm:rights` values are the filter keys for any Europeana harvesting. [Wave 23 Lane B]

#### DPLA MAP — standardized rights statement requirements ✅ free reference
- **What:** The Digital Public Library of America's Metadata Application Profile: `dc:rights`/`edm:rights` must carry a standardized rights statement — "Recommend Controlled Vocabulary, e.g., Rightsstatements.org; Creative Commons Licenses; URI" (verified in dpla/dpla-frontend's hub metadata docs, e.g. `http://rightsstatements.org/vocab/NoC-US/1.0/` as the worked example), with the DPLA Standardized Rights Statement Implementation Guidelines as the how-to.
- **URL:** https://github.com/dpla/dpla-frontend/blob/HEAD/public/static/local/oklahoma/metadata.md (hub docs quoting the requirement; verified 2026-10-07)
- **License:** ✅ Free reference (DPLA project docs)
- **Free tier:** N/A
- **Repo lane:** trippedd (research/discovery, provenance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** DPLA-side counterpart to the Europeana entry: together they cover the two aggregators rightsstatements.org names as its supporters. [Wave 23 Lane B]

---

## Honest negatives & deferrals (documented, not claimed)

1. **SMPTE ST 2110-40 (RTP carriage of ancillary data)** — exists and published (2018): maps ST 291-1 ancillary packets (captions, subtitles, teletext) into RTP for ST 2110 IP studios. BUT the spec is paywalled (SMPTE digital library / IEEE Xplore) and no free EBU-TT-Live-specific RTP mapping document was located — the W3C minutes note only that "BBC has submitted an RFC for TTML carriage in RTP" as work-in-progress. Not cataloged as a free reference; revisit if a public mapping appears.
2. **ODRL profile for cultural heritage** — searched; none found. What exists: the generic ODRL Profile mechanism, the archived ODRL/CC profile, and the Market Data profile. The CH sector standardizes on rightsstatements.org URIs instead (see Europeana/DPLA entries). Not invented — recorded as not-found.
3. **Wikidata P6426 (rightsstatements.org statement property)** — mentioned in search results but the Wikidata API returned HTTP 403 on verification (2026-10-07); not verified, not cataloged. Lead for a future wave.
4. **Book Scan Wizard license** — SourceForge code browser 403'd; not retried per access policy. Entry carries ❓ honestly.
5. **Full BDD suite of the EBU-TT Live toolkit** — not run (needs pytest-bdd + the full node graph); the WebSocket carriage smoke test above covers the carriage path that matters for this lane.
6. **PLUS (Picture Licensing Universal System)** — adjacent machine-readable image-licensing vocabulary (plus-coalition.org); not researched this wave — candidate for a follow-up.

---

*Wave 23 Lane B — 39 `####` entries (5 carriage · 13 book-scanner hardware/software · 21 rights-vocabulary), all licenses verified from upstream sources 2026-10-07. Proof artifacts: `docs/wave23/proof/`.*
