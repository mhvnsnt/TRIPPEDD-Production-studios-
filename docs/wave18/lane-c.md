# Wave 18 — Lane C: wiring + smoke-testing the strongest new catalog tools (2026-10-07)

Sole sequenced lane. Stayed on main at `851742c` (Lane B's push). Four tools wired
with real proof artifacts under `tools/wave18_laneC/`; every proof was executed,
not simulated. Other lanes' working files untouched.

## Catalog pointers (one paragraph per wired tool)

**DUMB (Dynamic Universal Music Bibliotheque)** — catalog entry
`#### DUMB (Dynamic Universal Music Bibliotheque)` (Wave 18 Lane A, custom
permissive zlib-style license). The clean-licensed module-playback donor the
catalog positions against quarantined libgme (row 184). Wired as
`tools/wave18_laneC/dumb_mod2wav/mod2wav.c`, a dependency-free C renderer built
against a cmake-compiled `libdumb.a`; it loads a synthetic ProTracker M.K. MOD
(`make_smoke_mod.py` generates a 2-pattern, 4-channel C-major arpeggio so the
fixture is license-clean) and writes 16-bit stereo WAV via `duh_render_int`.
Proof `proofs/wave18_dumb/proof.wav` is 12.0s of real module audio (ffprobe:
pcm_s16le/44100/stereo; PCM RMS 674, peak 13595 — non-silent). Production value:
tracker-module BGM for games/promos without GPL baggage.

**OpenSheetMusicDisplay** — catalog entry `#### OpenSheetMusicDisplay`
(Wave 18 Lane A, BSD-3-Clause). The catalog's MusicXML-native renderer,
complement to VexFlow for the OpenScore corpora. Wired as
`tools/wave18_laneC/osmd/osmd_render.cjs`: headless Node render of the actual
CC0 score Lane A pulled (`lc5115311.mxl`, Beethoven Op.48 No.1 "Bitten") to
vector SVG. Headless lessons recorded in the script: set DOM globals before
`require`, `npm canvas` (+ system cairo) for VexFlow text metrics, stub
`offsetWidth`, pass `pageFormat: "A4_P"` — without these the page collapses to
width 0. Proof `proofs/wave18_osmd/proof.svg` (408 stavenote groups) and
`page1.png` were **visually inspected**: correct engraved notation — title,
Voice + Pianoforte staves, lyrics underlaid, dynamics. Production value:
print/promo-ready sheet-music visuals from PD scores (liner art, music-video
overlays, Wizard Gang scoring docs).

**BDSup2Sub** — catalog entry `#### BDSup2Sub` (Wave 18 Lane A, Apache-2.0).
The catalog's clean-licensed PGS tooling against the quarantined Sup2Sub-class
utilities. No prebuilt jar exists (0 GitHub releases) and Maven is blocked on
this VM (egress proxy: `Unsupported or unrecognized SSL message` fetching
plugins), so all 107 sources were compiled with `javac` using curl-fetched
`commons-cli-1.2` + `java-image-scaling-0.8.5`; `macify` (Mac-only GUI helper)
404s on Maven Central, so a documented compile-only shim stands in
(`macify-shim/`, never on the CLI path). The smoke input is a fully synthetic,
valid PGS stream (`make_smoke_sup.py`: epoch-start PCS + WDS + PDS + RLE ODS +
END at 1.0s, clearing PCS at 4.0s; bitmap from PIL/DejaVu). Proof:
`proofs/wave18_bdsup2sub/` holds SUP → VobSub (`smoke_out.sub`/`.idx`, valid v7
index, 1920x1080, timestamp 00:00:01:000) and SUP → BDN XML+PNG
(`smoke_bdn_0001.png` visually inspected: "WIZARD GANG / PGS caption smoke
test" with outline, exactly the synthetic input). Notable: BDSup2Sub's RLE
decoder uses its own dialect (read from `SupBD.java`), and it cannot export
SRT — image-based formats only, no OCR (stated in its README). Production
value: Blu-ray caption ingest/normalization for the caption pipeline.

**L-SMASH** — catalog entry `#### L-SMASH` (Wave 18 Lane A, ISC). The
catalog's clean-licensed MP4 mux core (no Bento4/GPAC license baggage). Built
cleanly (`./configure && make` → `remuxer`, `muxer`, `boxdumper`,
`timelineeditor`). `tools/wave18_laneC/lsmash/smoke_remux.sh` remuxes a 3s
captioned MP4 (h264 + aac + SRT-as-tx3g) and inventories streams/box structure.
Proof `proofs/wave18_lsmash/`: A/V survive byte-clean (3.000s). **Honest
limit:** the `remuxer` CLI drops the tx3g subtitle track (3 traks → 2;
`boxdumper --box` confirms tx3g present in source, absent in remux) — it is an
A/V remuxer in this form, not a caption-track packager; `boxdumper` still
gives full box-level visibility for caption-track QA. Verdict for the
pipeline: useful for MP4 packaging and box inspection, not for tx3g delivery.

## Honest failures / environment notes

- **DUMB examples** (`dumbout.c`) not built: need `argtable2` + Allegro4,
  neither on the VM. Wrote a smaller dependency-free renderer instead; library
  build itself is clean.
- **OSMD first render collapsed to width 0** (jsdom has no layout engine) —
  fixed with `offsetWidth` stub + `pageFormat: "A4_P"`; also required the
  `canvas` npm package (VexFlow text measurement) and DOM globals set before
  `require`. A black PNG during verification was just a transparent background
  on a dark viewer — re-rendered with white.
- **BDSup2Sub Maven build** blocked by egress proxy; **macify** absent from
  Maven Central (compile-only shim, documented). No prebuilt jar upstream.
- **L-SMASH remuxer drops tx3g** (documented above — a real limitation, not a
  setup error).
- Considered but not wired: VGMTrans (Qt build, too heavy), HivelyTracker
  (no CLI renderer), UltraBox/Slarmoo's Box (browser-only, no live browser in
  this lane), `srt2ass`/`SubMux` (❓ unverified licenses), FFMS2 (VapourSynth
  chain, out of scope).

## Evidence inventory

| Tool | Wiring | Proofs |
|---|---|---|
| DUMB | `tools/wave18_laneC/dumb_mod2wav/{make_smoke_mod.py,mod2wav.c}` | `proofs/wave18_dumb/{smoke.mod,proof.wav,report.json}` |
| OSMD | `tools/wave18_laneC/osmd/osmd_render.cjs` | `proofs/wave18_osmd/{proof.svg,page1.png,report.json}` |
| BDSup2Sub | `tools/wave18_laneC/bdsup2sub/{make_smoke_sup.py,macify-shim/,lib/}` | `proofs/wave18_bdsup2sub/{smoke.sup,smoke_out.sub,smoke_out.idx,smoke_bdn.xml,smoke_bdn_0001.png,report.json}` |
| L-SMASH | `tools/wave18_laneC/lsmash/smoke_remux.sh` | `proofs/wave18_lsmash/{src_captioned.mp4,remuxed.mp4,streams.txt,box_src.txt,box_remuxed.txt,report.json}` |

Build scratch (`src/` clones, `node_modules/`, `classes/`, `*.a`, binaries) is
git-ignored via `tools/wave18_laneC/.gitignore`; only sources + small proofs
(≤2.1MB) are committed. OSMD's npm deps live in
`tools/wave18_laneC/osmd/package.json` (lane-local install — root
`package.json`/`package-lock.json` untouched; an earlier root-level install
was reverted after npm rewrote unrelated script entries).

Commit: `Resource pull Wave 18 Lane C: 4 tools wired with proofs`.
