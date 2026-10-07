### National-library digitization & OCR tooling — Wave 22 (+28)

#### Tesseract OCR ✅ commercial-safe
- **What:** The industry-standard open-source OCR engine (HP/Google heritage) — 100+ languages, LSTM models, hOCR/ALTO/PDF output; the backbone of most library digitization pipelines
- **URL:** https://github.com/tesseract-ocr/tesseract
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id tesseract-ocr/tesseract)
- **Free tier:** N/A (`apt install tesseract-ocr` / pip)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pair with OCRmyPDF for searchable-PDF production; tessdata_fast models for speed, tessdata_best for accuracy. [Wave 22 Lane A]

#### OCRmyPDF ✅ commercial-safe
- **What:** Adds an OCR text layer to scanned PDFs (Tesseract under the hood) — deskew, clean, PDF/A output; the standard "make this scan searchable" tool for library digitization
- **URL:** https://github.com/ocrmypdf/OCRmyPDF
- **License:** ✅ MPL-2.0 (verified 2026-10-07: GitHub API spdx_id ocrmypdf/OCRmyPDF)
- **Free tier:** N/A (`pip install ocrmypdf`)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** MPL-2.0 is file-level copyleft — fine as a standalone CLI step, don't embed its source files into proprietary code. [Wave 22 Lane A]

#### Kraken ✅ commercial-safe
- **What:** Modern OCR/HTR engine for historical documents — trainable recognition for early prints and handwriting; powers many national-library HTR pipelines
- **URL:** https://github.com/mittagessen/kraken
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id mittagessen/kraken)
- **Free tier:** N/A (`pip install kraken`)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Best pick when Tesseract fails on historical typefaces; ships pretrained models for early-modern print. [Wave 22 Lane A]

#### OCR-D ✅ commercial-safe
- **What:** German national-library OCR workflow framework (DFG-funded) — modular processors for binarization, layout analysis, OCR, and TEI/ALTO output; the reference digitization pipeline for historical prints
- **URL:** https://github.com/OCR-D/core
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id OCR-D/core)
- **Free tier:** N/A (pip / Docker)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Heavier than Tesseract alone, but the workflow standard for mass historical-print digitization (used by German research libraries). [Wave 22 Lane A]

#### OCRopus (ocropy) ✅ commercial-safe
- **What:** Classic Python OCR toolkit (Google/TMBDev) — LSTM line recognizer lineage that fed into Tesseract 4; still useful for custom training experiments on odd scripts
- **URL:** https://github.com/tmbdev/ocropy
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id tmbdev/ocropy)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dormant upstream (archived era) but permissively licensed and instructive; prefer Kraken for new HTR work. [Wave 22 Lane A]

#### OCR4all ✅ commercial-safe
- **What:** Web-app OCR workflow for historical prints (U. Würzburg) — wraps Calamari/OCRopus/Tesseract in a guided UI for non-technical digitization staff
- **URL:** https://github.com/OCR4all/OCR4all
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id OCR4all/OCR4all)
- **Free tier:** N/A (Docker)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Good route when OCR needs a human-in-the-loop UI rather than a batch CLI. [Wave 22 Lane A]

#### tesseract.js ✅ commercial-safe
- **What:** WebAssembly port of Tesseract — run OCR entirely in the browser or Node; powers client-side scan-to-text without a server round-trip
- **URL:** https://github.com/naptha/tesseract.js
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id naptha/tesseract.js)
- **Free tier:** N/A (npm)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Candidate for any browser-based digitization/upload UI — no backend OCR service needed. [Wave 22 Lane A]

#### EasyOCR ✅ commercial-safe
- **What:** Ready-to-use neural OCR with 80+ languages (PyTorch) — CRAFT detection + CRNN recognition; strong on scene text and mixed-language scans
- **URL:** https://github.com/JaidedAI/easyocr
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id JaidedAI/easyocr)
- **Free tier:** N/A (`pip install easyocr`)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Downloads models on first run (~100MB cache) — fine for tooling, don't vendor into repos. [Wave 22 Lane A]

#### PaddleOCR ✅ commercial-safe
- **What:** Baidu's multilingual OCR toolkit — text detection, recognition, table structure, and layout analysis; strong on CJK and document-understanding tasks
- **URL:** https://github.com/PaddlePaddle/PaddleOCR
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id PaddlePaddle/PaddleOCR)
- **Free tier:** N/A (pip / PaddlePaddle)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** PP-Structure extracts tables + layout from scans — pairs with Camelot/Tabula for tabular data recovery. [Wave 22 Lane A]

#### doctr ✅ commercial-safe
- **What:** Mindee's document-OCR library — end-to-end detection + recognition with a clean PyTorch API; built for production document pipelines
- **URL:** https://github.com/mindee/doctr
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id mindee/doctr)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Good middle ground between Tesseract (classic) and PaddleOCR (heavy) for scripted digitization. [Wave 22 Lane A]

#### Donut ✅ commercial-safe
- **What:** Naver Clova's OCR-free document understanding transformer — reads documents end-to-end without a separate OCR step (receipts, forms, tickets)
- **URL:** https://github.com/clovaai/donut
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id clovaai/donut)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-grade; useful when layout is too broken for classic OCR pipelines. [Wave 22 Lane A]

#### olmOCR ✅ commercial-safe
- **What:** AllenAI's open-source document-OCR pipeline — high-throughput PDF-to-text for building training corpora from digitized books
- **URL:** https://github.com/allenai/olmocr
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id allenai/olmocr)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Built for million-page-scale corpus building (the pipeline behind OLMo's training data) — overkill for single scans, right-sized for archive-scale work. [Wave 22 Lane A]

#### MMOCR ✅ commercial-safe
- **What:** OpenMMLab's comprehensive text-detection/recognition toolbox — 14+ algorithms in one framework for OCR research and benchmarking
- **URL:** https://github.com/open-mmlab/mmocr
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id open-mmlab/mmocr)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Benchmark harness for comparing OCR models on our own scan samples before committing to one engine. [Wave 22 Lane A]

#### RapidOCR ✅ commercial-safe
- **What:** Lightweight ONNX-based OCR (PaddleOCR models, no Paddle dependency) — fast CPU inference for scripted digitization
- **URL:** https://github.com/RapidAI/RapidOCR
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id RapidAI/RapidOCR)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The quick-win OCR when PaddleOCR's full install is too heavy. [Wave 22 Lane A]

#### Surya ✅ commercial-safe
- **What:** Datalab's document-OCR toolkit — line-level detection/recognition in 90+ languages plus layout analysis and reading-order detection
- **URL:** https://github.com/datalab-to/surya
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id datalab-to/surya)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Reading-order detection is the differentiator — multi-column historical layouts come out in the right sequence. [Wave 22 Lane A]

#### scikit-image ✅ commercial-safe
- **What:** Python image-processing library (NumPy/SciPy ecosystem) — the scriptable workhorse for scan cleanup: thresholding, denoising, deskew measurement
- **URL:** https://github.com/scikit-image/scikit-image
- **License:** ✅ BSD-3-Clause (verified 2026-10-07: LICENSE.txt in repo states BSD-3-Clause)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Use for pre-OCR cleanup stages before handing off to Tesseract/Kraken. [Wave 22 Lane A]

#### pyvips ✅ commercial-safe
- **What:** Python binding for libvips — streaming, low-memory image processing for huge scans (newspaper broadsheets, maps) that choke PIL/OpenCV
- **URL:** https://github.com/libvips/pyvips
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id libvips/pyvips)
- **Free tier:** N/A (pip; needs libvips)
- **Repo lane:** trippedd (digitization/OCR)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** libvips itself is LGPL — fine as a system dependency, don't statically link it into shipped binaries. [Wave 22 Lane A]

#### Cantaloupe ✅ commercial-safe
- **What:** Feature-rich IIIF image server (Java) — dynamic tiling, rotation, format conversion for digitized collections; the standard self-hosted IIIF endpoint
- **URL:** https://github.com/cantaloupe-project/cantaloupe
- **License:** ✅ NCSA Open Source License (verified 2026-10-07: LICENSE.txt in repo, develop branch)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** If we ever serve our own scan collections, this is the IIIF server to stand up. [Wave 22 Lane A]

#### Loris ✅ commercial-safe
- **What:** Python IIIF image server (W3C/IIIF Image API 2.x/3.x) — simpler alternative to Cantaloupe for serving digitized images with deep-zoom
- **URL:** https://github.com/loris-imageserver/loris
- **License:** ✅ BSD-3-Clause (verified 2026-10-07: LICENSE-Loris.txt carries the BSD 3-clause text)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Lighter than Cantaloupe; good for small archive pilots. [Wave 22 Lane A]

#### Mirador ✅ commercial-safe
- **What:** Configurable IIIF viewer (JS) — multi-window comparison of digitized manuscripts/maps; the viewer most national libraries embed
- **URL:** https://github.com/ProjectMirador/mirador
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id ProjectMirador/mirador)
- **Free tier:** N/A (npm)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Drop-in viewer for any IIIF manifest (Gallica, LOC, NLS) — comparison mode is ideal for before/after restoration review. [Wave 22 Lane A]

#### Universal Viewer ✅ commercial-safe
- **What:** IIIF viewer for books, maps, audio, and video (used by the British Library, NLS) — embeddable, accessibility-focused
- **URL:** https://github.com/universalviewer/universalviewer
- **License:** ✅ MIT (verified 2026-10-07: LICENSE.txt in repo, dev branch)
- **Free tier:** N/A (npm)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Handles AV + 3D as well as images — broader than Mirador if the collection mixes media. [Wave 22 Lane A]

#### biiif ✅ commercial-safe
- **What:** Static IIIF generator — build IIIF Presentation manifests from a folder of images + metadata, no server needed
- **URL:** https://github.com/IIIF-Commons/biiif
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id IIIF-Commons/biiif)
- **Free tier:** N/A (npm)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Fastest route to a IIIF-presentable scan set: folder in, manifest out, host on any static host. [Wave 22 Lane A]

#### node-iiif (Samvera) ✅ commercial-safe
- **What:** Node.js IIIF Image API processor — on-the-fly resize/crop/tile for image servers; the engine behind several Samvera repository stacks
- **URL:** https://github.com/samvera/node-iiif (npm package `iiif-processor`)
- **License:** ✅ Apache-2.0 (verified 2026-10-07: npm registry license field for iiif-processor)
- **Free tier:** N/A (npm)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Embeddable alternative to running a full IIIF server when you only need image-API transforms. [Wave 22 Lane A]

#### RAIS ✅ commercial-safe
- **What:** University of Oregon's IIIF image server (Go) — S3-native, Docker-ready, built for library digital collections at scale
- **URL:** https://github.com/uoregon-libraries/rais-image-server
- **License:** ✅ CC0-1.0 (verified 2026-10-07: GitHub API spdx_id uoregon-libraries/rais-image-server)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** CC0 dedication is the most permissive server option here; Go binary deploys as a single file. [Wave 22 Lane A]

#### Annona ✅ commercial-safe
- **What:** IIIF annotation studio (NCSU Libraries) — create and publish W3C Web Annotations against IIIF manifests; story-building over digitized collections
- **URL:** https://github.com/NCSU-Libraries/annona
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id NCSU-Libraries/annona)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/IIIF)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Annotation layer for IIIF collections — useful for marking up reference plates and map details. [Wave 22 Lane A]

#### Recogito 2 ✅ commercial-safe
- **What:** Pelagios' semantic annotation platform for texts and maps — link digitized material to gazetteers (Pleiades, GeoNames); the scholarly standard for geo-annotating collections
- **URL:** https://github.com/pelagios/recogito2
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id pelagios/recogito2)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (digitization/annotation)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Geo-tagging pipeline for map/plate collections — annotations export as open data. [Wave 22 Lane A]

#### OpenRefine ✅ commercial-safe
- **What:** Data-cleaning workbench for messy catalog metadata — faceted transforms, reconciliation against Wikidata/VIAF; the librarian's ETL tool
- **URL:** https://github.com/OpenRefine/OpenRefine
- **License:** ✅ BSD-3-Clause (verified 2026-10-07: GitHub API spdx_id OpenRefine/OpenRefine)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (digitization/metadata)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Reconcile any harvested catalog metadata against Wikidata/VIAF before ingesting. [Wave 22 Lane A]

#### JabRef ✅ commercial-safe
- **What:** Bibliography manager (Java) — BibTeX/BibLaTeX reference handling for research notes backing the catalog's provenance claims
- **URL:** https://github.com/JabRef/jabref
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id JabRef/jabref)
- **Free tier:** N/A
- **Repo lane:** trippedd (research)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Keeps the citation trail behind license/rights research auditable. [Wave 22 Lane A]
