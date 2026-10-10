# Wave 25 Lane A — netlabel clean-majority sweep (batch 6) + non-Scandinavian national-library AV + caption-SaaS free tiers + PD-label deep-dive

**Entries appended: 31** (`####` entries) · **Honest negatives documented: 181 netlabel collections + SaaS/ToS diligence** · Audit date: 2026-10-07
Coordinator: append-only into RESOURCE_CATALOG.md; no renumbering. Dedup greps run pre-append (see Method). Catalog count now **2,508** honest `####` headings (was 2,477).

## Method note

- **Dedup:** every candidate name grepped (case-insensitive) against `docs/RESOURCE_CATALOG.md` before inclusion. Waves 19–24 entries skipped as dups: Netlabels.org, Kahvi, Monotonik, phonoCAKE, Acroplane, Dusted Wax Kingdom, Enough Records, 2063music, Section 27, Clinical Archives, Tokyo Dawn, Error Broadcast, 12rec, Aaahh, Maltine, Bunkai-Kei, MarginalRec, Kikapu, Zymogen, Resting Bell, mixotic, Bypass, audiotalaia, hippocamp, Petite Jolie, Stroboskop, FUSELab, laridae, ozkye, Quantum Bit, Maravines, genetic-trance/treetrunk/oloil/noisecollector (batch-4/5 clean survivors); national libraries: Gallica/BnF, BNE/BDHispánica, DDB, NDL Japan, LAC Virtual Gramophone, NB Norway, KB Sweden, Digi.kansalliskirjasto.fi, Finna, DIGAR, NLI, Delpher, ANNO/ÖNB, Polona, Kramerius, e-Helvetica, Trove, Papers Past, NLW, NL Korea, NLS, NLI Ireland, NLA oral history, NL Israel sound archive, Letonica, Greece, BNP Portugal; 78rpm: UCSB Cylinders, DAHR general, Online 78rpm Discographical Project, Belfer, IA 78RPM parent, Great 78, LoC Inventing Entertainment/Edison, NPS Edison, National Jukebox, U.S. Marine Band, old78s, Commons PD 78s, WFMU Edison's Attic, CHARM, Open Music Archive, Red Hot Jazz, Mainspring Press, DAHR Edison.
- **IA netlabel audit (batch 6):** 200 `collection:netlabels` sub-collections listed via `advancedsearch.php`; 185 not previously cataloged were license-audited (`collection:<id> AND mediatype:audio`, up to 5000 items, fields identifier/licenseurl; classification clean=CC0/PDM/plain-CC-BY, nc=BY-NC*, other=BY-SA/BY-ND, unknown=no licenseurl). Raw JSON: `docs/wave25/w25_netlabel_batch6.json`. **4 clean-majority survivors** (all cataloged): happy-new-year-recordings (5/5), kusoj (8/12, 0 NC), marly-records (2/2), 383records (3/4, 0 NC). Note: collection-detail URLs follow the canonical `archive.org/details/<identifier>` pattern from the API-returned identifiers.
- **License claims:** verified from upstream (vendor pricing/ToS pages, library regulations PDFs, rights pages) or marked ❓ with explicit "VERIFY before wiring" caveats. Secondary sources named when used (slashdot comparisons, saasworthy, toolhunter, ailab.mobi, UNESCO, Wikipedia).
- **PD-date rule (US sound recordings, MMA):** pre-1923 PD; 1923–1946 = 100 yrs from publication (through-1925 PD as of 2026-10-07; 1926 recordings go PD 2027-01-01). EU = 70 yrs from publication (pre-1956 PD). Applied per-issue in entries.
- **No artifacts fabricated:** no downloads, no audio pulls; URLs are live pages/APIs checked 2026-10-07.

## Pocket 1 — Netlabel clean-majority (4 entries)

Wave-23's 90-sweep and Wave-24's 60-sweep found near-zero clean-majority labels; batch 6 (185 more) confirms the pattern: **4 survivors, all tiny**. The IA netlabel ecosystem is overwhelmingly NC-majority or unknown-license.

### Honest negatives (not entries — diligence record)
- **NC-majority:** rejected-netlabel (25/27), xv_parowek, coda-netlabel (18/19), bricolodge (23/24), feedbackloop-label (28/29), ilimitadaedicoes (22/26), 45rpm-records (110/110), year-of-the-butterfly (18/18), digital_output, netwaves-records, embriones-netlabel (29/30), ringe-raja-records, catching_leaves, community-skratch-releases (36/37), geekcore, devzero, stigae, bake-the-break, earfreemusic, aesthesea, workaholicsheteronymous, micromotiv, Ptl001, zigurartists, arteqcue, aventuel-label (40/41), basspistol, surrism-phonoethics (232/238 — largest NC-majority this wave), norient, universal-communication, diymusicians, ricardoteruel, rory-tory, second-family-records, 8digits, cybergrape, laverna (75/96), kusoj excluded (clean), marly-records excluded (clean), mp3death, glamslam, soundscapist, sutemos, fresh-poulp, meatronic, aullidosrecords, nexsound, sucumusic (42/42), hallo-excentrico (67/68), agitator-records, 3loop, eclectro, bedlamchamber, rskp-label (77/81), antenalab, twolefthands, the-lovely-moon, alter-sonic-records, mb-recordings, pitjamajusto, underlabel, thevegetablekingdom, lemoness, archivo_veintidos, metanoia, brecords, mad-block-records, 76-zec, yo-netlabel, auflegware-label, yip-records, human-sound (90/93), acustronica, watchpineapplepress, signal_zero, whenfrankbecamefrancine, elektroblef, nigredo-records, linear-obsessional-recordings (84/98).
- **Unknown-majority (unverifiable):** lalala4e-netlabel (25/25), goodmusic4you (30/30), embajadoresdelamusicacolombiana (226/226 — largest unknown), aklass, toxic-fly, majelis-taklim (mislabeled religious-sermon collection), slowsound, rory-tory, vetch, slmc-label, lo-music, arteqcue, diymusicians, frigida (59/76 unknown), 4-4-2, skeksis86, dreamnoiserecords, hnnetlabel, netlabels-Fridge, tibprod (89/90 unknown), lacedmilk (90/91 unknown), ecologyattackrecords (61/61), APNrecords, end-of-music (76/136 unknown), x-line, lii-netlabel, sfn, laidback_electronica, desert-vibe, austronica? (see acustronica), dwdrecords, sarutras-music.
- **SA/ND-majority (not commercial-safe):** raccoon-raver (12/13 other), amorfus (19/19 other), murmure-intemporel excluded (190/190 NC), slapart (17/32 other), language_lab (32/71 other), tranzmitter (58/83 other — 11 clean but SA/ND-majority, excluded).
- **Empty/zero-audio collections:** facilityrecords, muskedonner, the-inbetweens-company, ugo-capeto, manufracture, spoonplustenmusic, grond-murmure, netlable-Naometria-Sonitus, retrospective-zoology, nationstate-label, rcrecords, filamentxylin, fakebeat-label, datalog-label, catbird-records, omsamadhirecords, somnolescent, metro-map-records.
- **Near-misses:** cornslaw-industries (9 clean / 72 — NC-majority), techkilla (1/71), second-family-records (2/31), 001records (1/18), earstroke (1/28), buckrambeats (1/19), plaza-of-the-mind (2/6 — 1 NC), acoustic-firework-records (3/12 — 7 NC), mp3death (6/63), num-num-nah-records (8/105 — 39 NC), thesyntheticawakening (1/23), honeygears-robojazz, gravid? (gravy-sounds 1 other), blackrock-records.

## Pocket 2 — Non-Scandinavian national-library AV (9 entries)

1. **NSK Zagreb Digital Collections** ⚠️ — best terms page found: PD-labeled items unrestricted (download/share/modify) with source notice; copyrighted items private-study-only (REGULA1.pdf §9, verified).
2. **dLib.si (Slovenia/NUK)** ⚠️ — OCR'd press back to late 1700s, music sheets, maps; per-item rights.
3. **MEK (Hungary)** ⚠️ — grant covers nonprofit/private-study only; authors retain commercial rights (verified from vmek.oszk.hu permission doc).
4. **Biblioteca Nacional Digital Brasil (bndigital + Hemeroteca memoria.bn.br)** ⚠️ — UNESCO PBDL: ~13M PD images, per-record rights.
5. **Internet Culturale (Italy)** ⚠️ — MIC BY NC regime: commercial reuse of digitized heritage requires authorization + fee (verified via Wikimedia diff 2022/2023). Reference/research only for commercial pipelines.
6. **BEIC BeicDL (Milan)** ⚠️ — 27k objects; Paolo Monti archive partially open-licensed; Italian MIC caveat may apply.
7. **Bibliotheca Alexandrina DAR** ⚠️ — tiered access: PD books full, copyrighted 5% research-only; AV largely on-premises. DAF digitization tool is GPL-2.0 → code-quarantine candidate (not a catalog entry).
8. **Tímarit.is / Handrit.is (Iceland — Nordic, NOT Scandinavian)** ⚠️ — open-access newspapers/manuscripts; life+70 cutoff.
9. **Biblioteca Nacional de Portugal** — dropped as dup (catalog line 23108 already covers BNP ⚠️).

## Pocket 3 — Caption SaaS free tiers with honest ToS caveats (7 entries)

Verified from upstream pricing/ToS pages or marked ❓ with explicit verify-before-wiring caveats:
1. **Nova A.I.** ⚠️ — Free = 30 min subtitles/mo, watermarked (wearenova.ai/pricing, verified).
2. **Wavel AI** ⚠️ — Free = $0/10 credits BUT "NO Exports" for AI subtitles on free tier (wavel.ai/api-pricing, verified) — cataloged as diligence, not a wiring target.
3. **Dubverse** ⚠️ — Free = 20 credits/mo WITH .SRT export (saasworthy/aihungry plan tables).
4. **quso.ai (ex-vidyo.ai)** ⚠️ — Free = 75 min/mo (multiple 2026 comparisons).
5. **Type Studio** ❓ — free tier exists (toolhunter.ai); limits + vendor URL unpinned — do not wire until vendor site visited.
6. **AWS Transcribe** ❓ — reported 60 min/mo free (12 mo); training-opt-out caveat.
7. **Google Cloud Speech-to-Text** ❓ — reported 60 min/mo free.

**Dropped as dups (already cataloged, no new angle):** Deepgram free credit ❓ (line 6740), AssemblyAI ✅ (9668), Otter.ai ✅ (9718), Notta ✅ (9788), TurboScribe ❓ (13942), Gladia ❓ (13912 — free-tier claims differ: catalog says €50 no-expiry credits, 2026-10-07 sources say ~10 hrs/mo → flagged for Wave-26 reconciliation), Flixier ❓ (13852), Azure AI Speech ✅ (9548), Descript free-tier audit ⚠️ (18642), Clipchamp ⚠️ (18490), Amara ✅ (18570 — note: platform went AGPL→proprietary Jan 2020; does not change the ✅ for platform use, but self-hosting is no longer possible), CapCut ToS audit ⚠️ (18652 — perpetual content-license caveat already cataloged).
**Honest negatives:** Munch (NO free plan — paid from ~$49/mo per dataconomy/squeezegrowth/sendshort; one source reports a one-video trial), Castmagic (no free plan, per thetoolsverse), SubEasy (free tier not verifiable this pass — no URL grounding).

## Pocket 4 — PD label deep-dive (8 entries)

Label-specific DAHR deep-dives (all ⚠️, same streaming terms as the cataloged DAHR general entry — noncommercial streaming, PD items downloadable; verified via library.ucsb.edu):
1. **DAHR — Columbia** (Rust/Brooks Master Book Discography; 6,000 pre-1925 sides digitized for the Jukebox)
2. **DAHR — OKeh** (Laird/Rust 1918–1934; race-records/jazz/blues arm)
3. **DAHR — Brunswick** (Laird 1916–1931)
4. **DAHR — Decca** (1930s–40s; fewer pre-1926 sides — date-verify every issue)
5. **DAHR — Berliner Gramophone** (1890s–1900; ALL sides pre-1923 → PD per MMA; compositions checked per title)
6. **DAHR — Zonophone** (Victor budget arm)
7. **Public Domain 4U** ❓ — PD-music collection; per-track audit deferred to Wave 26
8. **Tinfoil.com** ❓ — Edison cylinder reference; rights unaudited
9. **ARSC** ❓ — research org (arsc-audio.org verified); the rights-reasoning reference for the pocket (Copyright & Fair Use committee, Guide to Audio Preservation)
10. **EMI Archive Trust** ❓ — Hayes archive; rights-holder contact of last resort for HMV/Columbia/Parlophone era (UMG-owned)

**Dropped as dups:** CHARM ❓ (line 24342), Open Music Archive ✅ (3510), Red Hot Jazz Archive ⚠️ (24775), Mainspring Press ⚠️ (24797).

## Quarantine

**Zero GPL/AGPL software finds this lane.** All entries are data collections, label metadata, or proprietary-ToS SaaS. The only copyleft-adjacent item encountered (BA's DAF digitization workflow tool, GPL-2.0) is a code tool mentioned in a note, not cataloged as an entry — flagging here for the coordinator in case a quarantine row is wanted. No new `docs/LICENSE_QUARANTINE.md` rows needed.

## Failures / open items for coordinator

- **Gladia free-tier discrepancy:** catalog entry says "€50 no-expiry credits"; 2026-10-07 sources say "~10 hrs/month". Needs a Wave-26 re-verify against gladia.io pricing.
- **Type Studio:** free tier confirmed to exist but limits + vendor site URL unpinned — needs a live-browser visit.
- **Amara platform closure (AGPL→proprietary, Jan 2020):** audit note against existing ✅ entry (18570) — coordinator to decide if the badge should shift to ⚠️.
- **Netlabel pocket is exhausted:** 90 + 60 + 185 = 335 IA netlabel collections audited across Waves 23–25; only clean-majority survivors are tiny (largest: Maravines 94% from Wave 24, kusoj 8/12 this wave). Recommend closing the netlabel pocket and moving remaining effort to other pockets.
- **IA `advancedsearch.php`:** `facets` parameter still rejected server-side ([UNSUPPORTED_VALUE]) — client-side classification from full field pulls continues to be the workaround.
