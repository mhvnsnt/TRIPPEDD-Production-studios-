# RESOURCE CATALOG — Wave 5 Appendix A3 (BG plates / stock video + anime-specific tooling)

Worker: Wave 5 A3 (replacement — original worker killed by daemon restart before producing any file; restarted fresh 2026-10-07).
Scope: NEW entries only. Every candidate grepped (`grep -i`) against `docs/RESOURCE_CATALOG.md` (366 `####` entries) AND all sibling Wave-5 appendices (A1/A2/B/D) before inclusion — no duplicates. Licenses verified from upstream sources (repo LICENSE files, official terms pages) on 2026-10-07 — never assumed. Several seed assumptions were REFUTED by verification (White-box-Cartoonization is CC BY-NC-SA not MIT; IS-Net is Apache-2.0 not AGPL; Mazwai/Reshot/SplitShire are dead/pivoted — dropped; Dareful is CC-BY 4.0 not CC0). Dead or unverifiable sources were dropped, not padded.
Badge key: ✅ = commercial-safe (verified) · 🚫 = not commercial-safe (NC/research/GPL — research lane only) · ❓ = unverified or mixed per-item (read terms per item before wiring)
Copyleft found in this lane: 2 new quarantine rows (RobustVideoMatting GPL-3.0, mmd_tools GPL-3.0).

## BG plates + stock video (20 entries)

#### Met Museum Open Access ✅ commercial-safe
- **What:** 492,000+ images of public-domain artworks (paintings, prints, photos, armor, textiles) with keyless REST API + direct high-res JPEGs
- **URL:** https://www.metmuseum.org/about-the-met/policies-and-documents/open-access
- **License:** CC0 1.0 Universal (verified via official Met Open Access policy page: images of public-domain artworks available for unrestricted use under CC0, 2026-10-07)
- **Free tier:** fully free, no key, no attribution required (API: collectionapi.metmuseum.org)
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** WIRED (2026-10-07 — 3 CC0 plates downloaded + manifest; see tools/background/met-open-access/)
- **Notes:** Best single PD texture/BG-reference source — period interiors, landscapes, architecture for cartoon BG paint-overs. Filter API with isPublicDomain=true. [Wave 5]

#### Rijksmuseum Rijksstudio ✅ commercial-safe
- **What:** 700k+ digitized artworks (Dutch masters, prints, decorative arts) with free API and IIIF high-res downloads
- **URL:** https://www.rijksmuseum.nl/en/rijksstudio
- **License:** CC0 1.0 / Public Domain Mark (verified via official Rijksmuseum Information & Data Policy §3.7: works no longer/never protected by copyright get PDM and/or CC0 1.0; Rijksmuseum waives its own copyright, 2026-10-07)
- **Free tier:** fully free API (data.rijksmuseum.nl), no key for basic search
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Check per-object rights flag; ~all pre-1900 works are CC0. Strong for period/cityscape BG plates (Vermeer-era Amsterdam streets, seascapes). [Wave 5]

#### Art Institute of Chicago ✅ commercial-safe
- **What:** 50,000+ CC0 images of collection works with a single unified public API
- **URL:** https://www.artic.edu/open-access
- **License:** CC0 1.0 Universal (verified via official AIC open-access page: free, unrestricted use of 50,000+ images under CC0, 2026-10-07)
- **Free tier:** fully free, keyless public API (api.artic.edu)
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Impressionist/post-impressionist holdings (Seurat, Monet) are excellent loose-painterly BG reference. API returns IIIF image URLs directly. [Wave 5]

#### Cleveland Museum of Art Open Access ✅ commercial-safe
- **What:** 30,000+ CC0 artwork images with keyless API — the only museum source serving archival TIFFs
- **URL:** https://www.clevelandart.org/open-access
- **License:** CC0 1.0 Universal (verified via official CMA open-access page: high-res images + full collection metadata under CC0, 2026-10-07)
- **Free tier:** fully free, keyless API (openaccess-api.clevelandart.org)
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** WIRED (2026-10-07 — 3 CC0 plates downloaded + manifest; see tools/background/cleveland-open-access/)
- **Notes:** Confirm share_license_status == "CC0" per result. images.print.url = 3400px JPEG, images.full.url = archival TIFF — best source for print-res BG plates. [Wave 5]

#### Getty Open Content Program ✅ commercial-safe
- **What:** 160,000+ high-res images of public-domain art/archives from the Getty Museum + Research Institute
- **URL:** https://www.getty.edu/projects/open-content-program/
- **License:** Public domain, no restrictions (verified via official Getty Open Content page: high-res images of public-domain artwork freely available without restrictions; appear in commercial publications/products/film, 2026-10-07)
- **Free tier:** fully free downloads, no key
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Strong antiquities/manuscript holdings (Roman, medieval) — period BG texture gold. Per-image download from collection pages. [Wave 5]

#### National Gallery of Art (NGA) Open Access ✅ commercial-safe
- **What:** 37,000+ CC0 images (American + European painting/sculpture) with bulk CSV dataset + IIIF delivery
- **URL:** https://images.nga.gov/
- **License:** CC0 1.0 (dataset-level; verified via NGA published_images.csv openaccess=1 flag mechanism documented in museum-API references, 2026-10-07)
- **Free tier:** fully free; bulk offline querying via published CSV on GitHub
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Best for bulk/offline work (no live search API needed) — filter CSV openaccess=1, then fetch IIIF full-res JPEG. Check per-image flag; not every image is open access. [Wave 5]

#### NYPL Public Domain Collections ✅ commercial-safe
- **What:** 180,000+ high-res public-domain items (NYC street photos, historic maps, botanical illustrations, manuscripts, FSA photography)
- **URL:** https://www.nypl.org/research/resources/public-domain-collections
- **License:** Public domain, no restrictions (verified via official NYPL page: "No permission required. No restrictions on use" for 180k+ PD items, 2026-10-07)
- **Free tier:** fully free, keyless API + GitHub data dumps
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Berenice Abbott's 1930s NYC + FSA photos are direct street-brawler BG reference (period city plates, signage, textures). Historic maps usable as district layout reference. [Wave 5]

#### Wellcome Collection ❓ mixed per-item
- **What:** 100,000+ historical images (manuscripts, paintings, etchings, early photography, medical ephemera) from the Wellcome Library
- **URL:** https://wellcomecollection.org/
- **License:** MIXED per item (historical Wellcome Images released under CC-BY — commercial OK with attribution; many newer archive items are CC-BY-NC or in-copyright; verified via Wellcome access-conditions pages, 2026-10-07)
- **Free tier:** fully free downloads
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Check each item's "Access conditions" before use — do not bulk-pull. Etchings/engravings are great cartoon-ink texture reference. [Wave 5]

#### British Library Mechanical Curator ✅ commercial-safe
- **What:** 1,000,000+ public-domain images extracted from 17th–19th century books (maps, diagrams, illustrations, illuminated letters, landscapes)
- **URL:** https://www.flickr.com/photos/britishlibrary
- **License:** Public Domain Mark (verified via BL's official release statement: images released back into the public domain for anyone to use, remix, repurpose; Flickr Commons PD mark, 2026-10-07)
- **Free tier:** fully free, Flickr API access
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Engravings + vintage maps are ideal cartoon-BG line-art/texture material. Metadata is thin (tagged by book/year) — search by tag. Manifests also on GitHub under PD terms. [Wave 5]

#### NOAA Photo Library ✅ commercial-safe
- **What:** NOAA Digital Library photos (oceans, coasts, storms, weather, marine life, ships, aerials)
- **URL:** https://www.photolib.noaa.gov/
- **License:** U.S. public domain (verified via official noaa.gov usage page: images in the NOAA Digital Library are in the public domain and cannot be copyrighted; check per-item credit, 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Caveat: NOAA VIDEOS often contain third-party copyrighted footage — photos are the safe lane. Storm/sea/sky plates for dramatic cartoon skies. [Wave 5]

#### USGS Multimedia Gallery ✅ commercial-safe
- **What:** USGS photos + Landsat satellite imagery + topographic maps (landscapes, geology, volcanoes, rivers)
- **URL:** https://www.usgs.gov/
- **License:** U.S. public domain (verified via official USGS Copyrights and Credits: USGS-authored data and information are in the U.S. public domain, freely usable without permission; credit requested, 2026-10-07)
- **Free tier:** fully free, no key
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Landsat = free satellite BG plates for district/world maps. Watch for the small number of non-USGS images marked copyrighted on USGS pages. [Wave 5]

#### DVIDS (Defense Visual Information Distribution Service) ✅ commercial-safe
- **What:** U.S. military photo/video archive (aircraft, ships, bases, urban ops, disaster relief) — broadcast-quality stills + video
- **URL:** https://www.dvidshub.net/
- **License:** U.S. public domain unless otherwise specified (verified via official DVIDS pages: "All DVIDS Media is considered public domain and is free to use unless otherwise specified", 2026-10-07)
- **Free tier:** free with registration (download requires free account)
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Check per-item markings (some VI carries non-DoD copyright). Vehicle/aircraft/urban-ops b-roll for action BG plates. [Wave 5]

#### ESA imagery ❓ mixed per-item
- **What:** European Space Agency image/video library (Earth observation, deep space, rockets, launches)
- **URL:** https://www.esa.int/ESA_Multimedia/Images
- **License:** MIXED per item (verified via official ESA terms, 2026-10-07): default ESA portal terms restrict to educational/editorial/informational use — commercial use excluded without a licence 🚫; items expressly marked CC BY-SA 3.0 IGO ✅; ESA/Hubble images are CC-BY 4.0 ✅
- **Free tier:** free downloads
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Only pull items with an explicit CC mark (BY-SA 3.0 IGO or ESA/Hubble CC-BY 4.0). Never use default-portal-terms images in commercial output. [Wave 5]

#### Internet Archive — Moving Image Archive ✅ commercial-safe (per item)
- **What:** Full IA moving-images collection: Prelinger subset plus government films, newsreels, educational shorts, feature films with lapsed copyright
- **URL:** https://archive.org/details/movies
- **License:** Per-item (verified via IA item pages: films carrying the CC Public Domain Dedication are reusable without restriction; CHECK EACH FILM's item page, 2026-10-07)
- **Free tier:** free downloads (MP4/Ogg/MPEG2 per film)
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Broader than the Wave-5-A1 Prelinger entry (same collection family, this entry = the whole movies collection for video BG plates). ~65% of Prelinger holdings are PD. Strip soundtracks if music rights are unclear. [Wave 5]

#### Pixabay photos + video ✅ commercial-safe
- **What:** Pixabay's stock photo + video library (distinct from the catalog's existing Pixabay SFX and Pixabay Music entries) — city streets, crowds, textures, aerials, b-roll
- **URL:** https://pixabay.com/
- **License:** Pixabay Content License — free commercial use, no attribution (verified via official pixabay.com/service/license-summary; platform license, NOT CC0, 2026-10-07)
- **Free tier:** fully free, no signup for downloads
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Cannot sell unaltered copies or compile a competing stock service. Video plates usable as BG elements/reference. [Wave 5]

#### Dareful ✅ commercial-safe
- **What:** Free 4K/HD stock video clips shot by Joel Holland (VideoBlocks founder) — nature, city, aerials, timelapses
- **URL:** https://dareful.com/
- **License:** CC-BY 4.0 International (verified via official dareful.com about page: clips usable in any project incl. commercial, governed by CC-BY 4.0; attribution required, 2026-10-07)
- **Free tier:** fully free, unlimited downloads
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Seed said CC0 — corrected to CC-BY 4.0 (attribution required). 4K quality is the draw; good for cinematic cartoon-BG paint-over bases. [Wave 5]

#### Videvo ❓ mixed per-clip
- **What:** Large free + premium stock video/motion-graphics/audio library (50k+ free assets)
- **URL:** https://www.videvo.net/
- **License:** MIXED per clip (verified via Videvo license docs, 2026-10-07): free clips under Videvo Attribution License or CC-BY 3.0 (both require attribution; commercial use allowed); premium clips royalty-free (paid)
- **Free tier:** free downloads with attribution; paid tiers remove attribution
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Check each clip's license badge before use. Motion-graphics/animated-background section useful for cartoon title/BG loops. [Wave 5]

#### StockSnap.io ✅ commercial-safe
- **What:** Curated CC0 stock photos, hundreds added weekly, searchable
- **URL:** https://stocksnap.io/
- **License:** CC0 1.0 Universal (verified via official stocksnap.io/license page: every image governed exclusively by CC0, 2026-10-07)
- **Free tier:** fully free, no attribution required
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Clean modern photography — textures, skies, urban details for BG work. Review each image for IP/privacy issues per their own caveat. [Wave 5]

#### Life of Pix / Life of Vids ❓ unverified
- **What:** LEEROY creative agency's free photo (Life of Pix) + video (Life of Vids) libraries, described as no-copyright-restriction
- **URL:** https://www.lifeofpix.com/
- **License:** ❓ unverified (site timed out on fetch 2026-10-07; multiple third-party sources describe both libraries as no-copyright-restriction/public-domain — read the site's terms before wiring)
- **Free tier:** free downloads
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Small curated libraries (~600 photos); Life of Vids = PD video loops. Do not wire until the site's own license text is read. [Wave 5]

#### Openverse ✅ commercial-safe (per item)
- **What:** WordPress's openly-licensed media search engine — 800M+ images + audio aggregated across CC/PD sources with per-item license filters
- **URL:** https://openverse.org/
- **License:** Per-item CC license or public domain (verified via openverse.org: "All Openverse content is under a Creative Commons license or is in the public domain", 2026-10-07)
- **Free tier:** fully free, API available
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Filter to CC0/PDM-only for zero-bookkeeping pulls; CC-BY items need attribution tracking. Best discovery layer across the museum/PD sources above. [Wave 5]

## Dropped BG candidates (dead or unverifiable — not counted)

- **Mazwai** — DROPPED: site discontinued; mazwai.com now redirects to Freepik/Magnific (paid AI suite), free CC library gone (verified 2026-10-07).
- **Reshot** — DROPPED: retired January 2026 by Envato; no new downloads available (verified 2026-10-07).
- **SplitShire** — DROPPED: site pivoted to an AI-tools subscription service (SplitShire Apps); the free CC0 stock library is gone (verified via live splitshire.com, 2026-10-07).
- **Flickr Commons** — not added as separate entry: covered by the British Library Mechanical Curator entry (same program); avoid duplication.

## Anime-specific production tooling (24 entries)

#### White-box-Cartoonization 🚫 not commercial-safe
- **What:** CVPR2020 photo→cartoon GAN (white-box cartoon representations) — scenery/people/food cartoonization with pretrained models
- **URL:** https://github.com/SystemErrorWang/White-box-Cartoonization
- **License:** CC BY-NC-SA 4.0 (verified via upstream README License section: "Commercial application is prohibited", 2026-10-07)
- **Free tier:** fully open code + pretrained weights
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** Seed assumed MIT — REFUTED. Research-lane only: style R&D and look-dev experiments, never in shipping paths. TF1-era code; needs porting effort for modern stacks. [Wave 5]

#### Anime2Sketch ✅ commercial-safe
- **What:** Photo/anime→line-art sketch extraction (painterly sketch style) with pretrained model
- **URL:** https://github.com/Mukosame/Anime2Sketch
- **License:** MIT (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** BG line-art extraction + inking reference for cartoon BGs; pairs with colorization pipelines. Lightweight inference. [Wave 5]

#### Real-CUGAN ❓ unverified
- **What:** Bilibili AI Lab anime-image super-resolution (2x/3x/4x, waifu2x-compatible CUNet architecture), trained on million-scale anime data
- **URL:** https://github.com/bilibili/ailab/tree/main/Real-CUGAN
- **License:** ❓ unverified — no LICENSE file and no license statement in the upstream bilibili/ailab repo (checked 2026-10-07); third-party integrators claim MIT but that is NOT from upstream
- **Free tier:** free model weights + code
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Do NOT wire weights into shipping paths until upstream publishes terms. The nihui ncnn-vulkan port (MIT, next entry) is the wireable implementation — but note its weights inherit this same upstream gap. [Wave 5]

#### nihui ncnn-vulkan SR ports (realcugan / realsr / srmd) ✅ commercial-safe
- **What:** Vulkan/CPU super-resolution binaries by nihui: realcugan-ncnn-vulkan (anime), realsr-ncnn-vulkan (photo RealSR), srmd-ncnn-vulkan (denoise+SR) — no Python/CUDA needed
- **URL:** https://github.com/nihui/realcugan-ncnn-vulkan
- **License:** MIT (verified via upstream LICENSE files for realcugan-ncnn-vulkan and srmd-ncnn-vulkan; nihui's ports are uniformly MIT, 2026-10-07)
- **Free tier:** fully open, prebuilt binaries for Win/Linux/macOS
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED (2026-10-07 — binary vendored + `-h` arg-parsing proven, but inference needs Vulkan: `vkCreateInstance failed -9` on this Vulkan-less VM; full smoke test blocked on environment, NOT on the tool. See tools/upscale/proofs/realcugan-smoke-test-2026-10-07.md. Re-run on GPU hardware to promote to WIRED.)
- **Notes:** Single entry covers the three sibling ports (same author, same MIT pattern, same CLI shape). realcugan port = primary anime upscaler for plates/stills; srmd = denoise+upscale for scanned line art. [Wave 5]

#### EBSynth ✅ commercial-safe
- **What:** Example-based video stylization — paint one keyframe, propagate the style across the shot via optical flow/patch synthesis
- **URL:** https://ebsynth.com/
- **License:** Proprietary freeware — beta free for commercial AND non-commercial use (verified via official FAQ statements reported consistently: "can be used free for commercial and non-commercial purposes"; source at github.com/jamriska/ebsynth, 2026-10-07)
- **Free tier:** free beta download (Win/Mac/Linux)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Killer cartoon pipeline stage: hand-paint 1 BG keyframe → EBSynth propagates painterly style across the whole camera move. Caveat: a paid Pro version is planned — lock the beta binary in tools/ while free. [Wave 5]

#### DeOldify ✅ commercial-safe
- **What:** GAN colorization for B&W photos/video (NoGAN training) — period-photo colorization for BG reference
- **URL:** https://github.com/jantic/DeOldify
- **License:** MIT (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** Colorize B&W PD photos (NYPL FSA, LOC) into color BG-reference plates. Heavy deps (fastai-era); consider containerizing. [Wave 5]

#### CodeFormer 🚫 not commercial-safe
- **What:** Transformer-based face restoration (degraded/low-res face → high-quality) — character still cleanup
- **URL:** https://github.com/sczhou/CodeFormer
- **License:** S-Lab License 1.0 — NON-COMMERCIAL only (verified via upstream LICENSE: "Redistribution and use for non-commercial purpose"; commercial use requires contacting contributors, 2026-10-07)
- **Free tier:** fully open code + weights
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** Research-lane only. For shipping face restoration use GFPGAN (already in catalog) instead. [Wave 5]

#### RobustVideoMatting 🚫 not commercial-safe (QUARANTINED)
- **What:** Real-time robust video matting (trimap-free background removal for humans) — green-screen-free character cutout
- **URL:** https://github.com/PeterL1n/RobustVideoMatting
- **License:** GPL-3.0 (verified via upstream LICENSE, 2026-10-07) — QUARANTINED (row 76): standalone tool use/research only, never linked into shipping paths
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** For shipping matting prefer MODNet (Apache-2.0) or BiRefNet (MIT) below. [Wave 5]

#### MODNet ✅ commercial-safe
- **What:** Real-time portrait matting network (trimap-free) — fast character cutout for compositing
- **URL:** https://github.com/ZHKKKe/MODNet
- **License:** Apache-2.0 (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open + ONNX exports
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Commercial-safe alternative to RobustVideoMatting. Real-time on GPU; good for cutout passes on cartoon character renders. [Wave 5]

#### BiRefNet ✅ commercial-safe
- **What:** Bilateral-reference dichotomous segmentation — high-accuracy foreground/background segmentation, strong on fine detail
- **URL:** https://github.com/ZhengPeng7/BiRefNet
- **License:** MIT (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** SOTA-ish general segmentation; heavier than MODNet but finer edges — use for hero cutouts, MODNet for bulk. [Wave 5]

#### U-2-Net ✅ commercial-safe
- **What:** Nested U-structure salient object detection — the classic lightweight background-removal net
- **URL:** https://github.com/xuebinqin/U-2-Net
- **License:** Apache-2.0 (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open, tiny 4.7MB model (u2netp)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Smallest/fastest of the matting family — batch BG-removal on reference stills. Basis for rembg's default model. [Wave 5]

#### IS-Net (DIS — Dichotomous Image Segmentation) ✅ commercial-safe
- **What:** Highly accurate dichotomous image segmentation (ECCV 2022) — the current best general foreground segmenter; rembg's isnet model source
- **URL:** https://github.com/xuebinqin/DIS
- **License:** Apache-2.0 (verified via upstream LICENSE.md, 2026-10-07)
- **Free tier:** fully open code + weights
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Seed said AGPL → quarantine — REFUTED by upstream LICENSE.md (Apache-2.0; the AGPL label came from a third-party onnx-community repack). No quarantine needed. Best-in-class cutout for BG compositing; use isnet-general-use ONNX via rembg. [Wave 5]

#### DeepDanbooru ✅ commercial-safe
- **What:** Anime-style image tagger (ResNet-based, trained on Danbooru) — auto-tag anime stills/frames for dataset organization
- **URL:** https://github.com/KichangKim/DeepDanbooru
- **License:** MIT (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Auto-tagging for the anime asset library (poses, clothing, hair, style tags) — feeds dataset curation for training/fine-tuning loops. TF-based; containerize. [Wave 5]

#### anime-segmentation ✅ commercial-safe
- **What:** Anime/illustration-specific semantic segmentation (skin, hair, clothes, bg) with pretrained models
- **URL:** https://github.com/SkyTNT/anime-segmentation
- **License:** Apache-2.0 (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Anime-domain segmenter beats general models on cel art — part-level masks (hair/clothes/skin) for recolor, in-betweening masks, and style-transfer region control. [Wave 5]

#### VTube Studio 🚫 not commercial-safe (free tier)
- **What:** Leading Live2D VTuber runtime (face tracking, model rendering, hotkeys, item system) — Windows/macOS/iOS/Android
- **URL:** https://store.steampowered.com/app/1325860/VTube_Studio/
- **License:** Proprietary EULA (verified via official Steam EULA, 2026-10-07): free tier shows watermark; COMMERCIAL use (monetized streams etc.) requires purchasing at least one paid version/DLC (~$15 one-time)
- **Free tier:** free base app (watermarked); Remove-Watermark DLC ~$14.99 one-time
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Commercial path exists ($15 DLC) but the free tier is not commercial-safe → 🚫 badge. Companies >$200k revenue need a Company License. Live2D model editing itself needs Live2D Cubism (already in catalog as 🚫). [Wave 5]

#### Veadotube Mini ❓ unverified
- **What:** Free minimalist PNG-tuber app (reactive PNG avatars, mic-based bounce) by olmewe — itch.io
- **URL:** https://olmewe.itch.io/veadotube-mini
- **License:** ❓ unverified — freeware on itch.io; no explicit license terms found upstream (checked 2026-10-07); read bundled terms before wiring
- **Free tier:** fully free
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Simplest path to a "talking portrait" avatar for cartoon interstitials. Full paid version in development — terms may change. [Wave 5]

#### VRoid Studio ✅ commercial-safe
- **What:** pixiv's free 3D anime-character creator (exports VRM 0.x/1.0) — parametric anime avatars with hair/cloth/face editing
- **URL:** https://vroid.com/en/studio
- **License:** Proprietary freeware — commercial use of CREATED MODELS explicitly allowed (verified via official VRoid Studio Guidelines: models/textures/preset items may be sold and used commercially incl. games, goods, streaming; no credit required, 2026-10-07)
- **Free tier:** fully free (Win/Mac)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Caveats: cannot build a character-creator APP on VRoid meshes without a separate pixiv licence; some bundled items carry special clauses — check per item. Direct VRM pipeline into three-vrm/UniVRM below. [Wave 5]

#### three-vrm ✅ commercial-safe
- **What:** VRM avatar loader/runtime for three.js (VRM 0.x + 1.0, spring bones, blendshapes) — web avatar rendering
- **URL:** https://github.com/pixiv/three-vrm
- **License:** MIT (verified via upstream LICENSE, 2026-10-07)
- **Free tier:** fully open (npm)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Web-side VRM playback for the PWA (menu avatars, VTuber-style presenters). Pairs with VRoid Studio exports. [Wave 5]

#### UniVRM ✅ commercial-safe
- **What:** Reference VRM implementation for Unity (import/export VRM 1.0/0.x, glTF 2.0, runtime loading)
- **URL:** https://github.com/vrm-c/UniVRM
- **License:** MIT (verified via GitHub repo license badge + README License section, 2026-10-07)
- **Free tier:** fully open (UPM packages + unitypackages)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Unity-side VRM ingestion if any Unity tooling enters the pipeline; otherwise reference implementation for format questions. [Wave 5]

#### VRM specification ❓ unverified
- **What:** The VRM 3D-avatar file format specification (glTF 2.0 extension) — vrm.dev
- **URL:** https://github.com/vrm-c/vrm-specification
- **License:** ❓ unverified — no license file or license statement in the upstream repo (checked 2026-10-07); spec text reuse terms unclear
- **Free tier:** spec freely readable
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Reference only — implement against it via three-vrm/UniVRM (both MIT) rather than copying spec text. Do not wire until terms clarified. [Wave 5]

#### mmd_tools 🚫 not commercial-safe (QUARANTINED)
- **What:** Blender add-on for importing/exporting MMD model (.pmd/.pmx), motion (.vmd), and pose (.vpd) data
- **URL:** https://github.com/MMD-Blender/blender_mmd_tools
- **License:** GPL-3.0 (verified via GitHub repo license badge + README License section, 2026-10-07) — QUARANTINED (row 77): standalone tool use/research only, never linked into shipping paths
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** The PMX↔Blender bridge for the MMD asset lane. Usable as a standalone Blender add-on (tool use ≠ code reuse); do not import its code into pipeline scripts. [Wave 5]

#### VSeeFace ✅ commercial-safe
- **What:** Free VTuber face/hand-tracking app for VRM/VSF avatars (webcam tracking via OpenSeeFace, virtual camera output)
- **URL:** https://www.vseeface.icu/
- **License:** Proprietary freeware — commercial use allowed (verified via official terms of use: "You can use VSeeFace to stream or do pretty much anything you like, including non-commercial and commercial uses. Just don't modify it or claim you made it", 2026-10-07)
- **Free tier:** fully free, no paid tier
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Zero-cost mocap-ish face performance capture for cartoon dialogue shots; drives VRoid/VRM avatars. Windows-only. [Wave 5]

#### PmxEditor ❓ unverified
- **What:** The standard PMX/PMD model editor for MMD (bones, morphs, materials, physics, toon shading) by Hog
- **URL:** https://ux.getuploader.com/pmxeditor/ (author distribution; mirrors widely)
- **License:** ❓ unverified — freeware; no explicit upstream license terms found (checked 2026-10-07); read the bundled readme before wiring
- **Free tier:** free download
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Essential PMX surgery tool (mmd_tools explicitly defers to it). Windows-only. Do not redistribute the binary; use as a workstation tool. [Wave 5]

#### MikuMikuDance (MMD) ❓ unverified
- **What:** Yu Higuchi's freeware 3D animation program — the origin of the PMX/VMD ecosystem; huge community motion/model library (BowlRoll, NND)
- **URL:** https://sites.google.com/view/vpvp/ (VPVP official distribution)
- **License:** ❓ unverified — freeware; upstream readme terms not confirmed in this pass (checked 2026-10-07). Note: bundled Animasa starter models are NON-COMMERCIAL per model readmes — model terms are per-author regardless of software terms
- **Free tier:** free download (Windows)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Value is the motion-data ecosystem (thousands of free VMD dances/actions, each with own terms). Treat every downloaded model/motion as per-author licensed; never assume. [Wave 5]

## Entry count

44 new entries: 20 BG plates/stock video + 24 anime-specific tooling. Badges: 24 ✅ · 7 🚫 · 7 ❓ · 6 dropped-or-merged (3 dead sources dropped, 3 nihui ports merged into one entry). Quarantine rows added: 2 (76 RobustVideoMatting, 77 mmd_tools).
