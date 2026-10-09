# Wave 64 Lane A report — catalog deepening (2026-10-08)

**Lane:** A (catalog deepening) · **Branch:** wave64-lane-a · **Worktree:** ~/workspace/wave64-laneA
**Catalog:** 5,831 → **5,971** honest `####` entries (+140 net new; target 5,930+ met)
**Quarantine rows added:** 0 (docs/LICENSE_QUARANTINE.md untouched — all P4 licenses verified permissive; P1 doc-sites stay ❓ per precedent, code not catalogued, nothing quarantined)

## P1 — SDK docs round 10 (34 entries)

Console/emulator/dev-board/engine documentation not covered in rounds 1–9. Every URL verified live HTTP 200 on 2026-10-08.
- **New consoles/dev boards:** ultra64.ca (N64), n64brew.dev (N64 homebrew wiki), lxdream.org (Dreamcast emu docs), yabause.org (Saturn emu docs), Cxbx-Reloaded wiki (Xbox emu), wiiubrew.org (Wii U), switchbrew.org (Switch), vitasdk.org (Vita), docs.mamedev.org (MAME), docs.scummvm.org, wiki.easyrpg.org, docs.solarus-games.org, docs.m5stack.com (ESP32 boards)
- **Retro knowledge bases:** 8bitworkshop.com, plutiedev.com (Genesis), worldofspectrum.org, dosbox.com/wiki
- **Modern engine docs:** Godot, MonoGame, Defold (defold.com/manuals — docs.defold.com dead), Cocos, GDevelop, SDL, Stride (doc.stride3d.net — docs. subdomain dead), Flax, O3DE, Filament, OpenGL (docs.gl), Vulkan (docs.vulkan.org), WebGPU (gpuweb.github.io/gpuweb — www.gpuweb.org dead), GLFW
- **✅ on repo licenses (Pyxel precedent):** raysan5/raylib wiki (Zlib), DCurrent/openbor wiki (BSD-3-Clause; openbor.com dead/525, wiki canonical). All other doc-sites ❓ per precedent.
- **Dedup:** 0 rejections — all 34 URLs absent from catalog. (Wave 56 round-2 and Wave 62 round-8 items — tonc, psx.dev, gbadev.org, n64.dev, devkitPro wiki, 3dbrew, c64-wiki, 6502.org, ESPboy, Gamebuino, Pokitto, Thumby, Analogue openFPGA, sdk.play.date, TIC-80 wiki, PICO-8 wiki, GC-Forever, dreamcast.wiki, neogeodev pages, NESdev wiki, Pan Docs, MiSTer docs — all confirmed already cataloged and skipped.)
- **Honest drops:** 3do.cdinteractive.co.uk (dead), docs.stride3d.net (dead), www.gpuweb.org (dead), openbor.com (525 SSL).

## P2 — landmark musicdisk round 8 (19 entries)

pouët vote-sorted musicdisk chart **page 5** (`prodlist.php?type[]=musicdisk&order=thumbup&page=5`, fetched live 2026-10-08; pagination confirmed pages 4/5/6). Rounds 4–6 covered pages 2–3, round 7 covered page 4. **No held items remain** — Wave 63 resolved all 4 of Wave 61's held musicdisks.
- 19 new: Bassknecht Mix Music Disc, Star Flake, MDMOD Player (demotool/musicdisk dual), Orbtraxx #1 (4k), Xmastro (dentro), Zalza VS The World (game/musicdisk dual), BitJam Remix Compo 2, Hybrid'Elic, koolnESS, spinning wheels, Mirror, TRSi Elektroshock, happy-hardcore xmas ep 2010, Inner Spring, Popstars, Brus 4k, Shiru's 1-Bit Vol.2, DisIsSid #4 HTML, Zikdisk 2.
- Every prod page verified live on pouët (og:title + og:description: title/group/platform). Group corrections from verification: Star Flake = Maniacs Of Noise, TRSi Elektroshock = Tristar & Red Sector Inc., BitJam = BitFellas & Rebels.
- All ❓ (no license statements on scene records; NC not declared). demozoo still Cloudflare-blocked — no demozoo links claimed.
- **Dedup rejections (6):** Music Dream II (3418), ChipChop 16 (65327), Uncle Tom Sonix (59019), Coolism (53244), Music Dream I (3179), ChipChop 17 (96558) — all already #### entries; toplist vote drift moved them onto page 5. 0 pouët-ID dupes among the 19.

## P3 — PD radio-drama round 13 (44 entries)

Per-show per-episode deep dives on 8 established-✅PD shows (Wave 59 badge-discipline ruling: ✅ with established-PD note + item-level licenseurl-absent stated honestly). Every item verified via archive.org metadata API 2026-10-08 (HTTP 200, title match, open access, ≤2 audio files, <60 files).
- 6 Fort Laramie (3 carry CC0 1.0 item marks) · 6 Broadway Is My Beat · 4 Candy Matson · 6 The Witch's Tale · 5 Exploring Tomorrow · 5 Gang Busters · 6 Hall of Fantasy · 6 Let George Do It
- Uneven counts are honest: Candy Matson/Exploring Tomorrow/Gang Busters clean singles genuinely scarce.
- **Honest negatives:** 20+ access-restricted Boxcars711/KYAG pods (private=true audio), 6 collection exclusions (10–406 files), 1 wrong-show exclusion (mis-titled "Blair Of The Mounties"), 1 modern re-recording exclusion (Candy Matson Black Cat "rerecorded from private script"), 3 same-episode dupe avoidances (Boatwright's Story, Devil Doctor, Time Heals/First Baby In Space).
- **Pre-append dedup:** 0 identifier dupes. No character-rights shows (no Lone Ranger/Shadow/Green Hornet).

## P4 — demoscene tooling round 2 + caption/subtitle OSS tail (43 entries)

The brief's new angle evaluated both: **caption tail is exhausted** (24 tools already cataloged: libass, ffsubsync, autosub, pysubs2, webvtt-py, whisperx, insanely-fast-whisper, whisper-jax, whisper-webui, Aegisub, EasyOCR, PaddleOCR, RapidOCR, argos-translate, subliminal, vosk, Montreal Forced Aligner, gentle, auditok, auto-editor, moviepy, doctr, srt, pycaption). Demoscene tooling round 2 yielded far more — 39 new + the 4 surviving caption tools (libjass, keras-ocr, pywhispercpp, pydub).
- **Shader/GPU (10):** glslViewer (BSD-3), glslang (BSD-style), SPIRV-Tools (Apache-2.0), SPIRV-Cross (Apache-2.0), DirectXShaderCompiler (LLVM), shaderc (Apache-2.0), glsl-optimizer (MIT, aras-p canonical — ardatan fork gone), SwiftShader (Apache-2.0), ANGLE (BSD-3), Dawn (BSD-3).
- **Engines/frameworks (26):** PlayCanvas, openrndr, thi.ng, Filament, The-Forge, DiligentEngine, LumixEngine, Cocos, GDevelop, MonoGame (Ms-PL), Kha (zlib), Starling (BSD), openfl, three.js, Babylon.js, A-Frame, react-three-fiber, twgl.js (greggman canonical), luma.gl, deck.gl, regl, OGRE, LÖVE (zlib), HaxeFlixel, FNA (Ms-PL), heaps — all MIT/BSD/zlib/Ms-PL/Apache-2.0, every license verified upstream (GitHub API spdx_id or raw LICENSE read; 15 NOASSERTION gaps resolved by direct license-text reads).
- **Compression (2):** lz4 (BSD-2-Clause for lib/ — GPL-2.0 parts are CLI/examples, noted), zstd (BSD).
- **Audio (1):** madmom (BSD-3-Clause source; model files separate terms, noted).
- **Caption survivors (4):** libjass (Apache-2.0), keras-ocr (MIT), pywhispercpp (MIT), pydub (MIT).
- **Zero quarantine rows** — no copyleft in this pocket. LGPL doctrine still PENDING OWNER VERDICT (unchanged).
- **Honest drops:** FlaxEngine (custom EULA, not verified permissive), Away3D core (no canonical repo).

## Verification method (all pockets)

- P1: curl HTTP status per URL (200 required); GitHub API for repo-license badges; two ✅ only where repo LICENSE is permissive (Pyxel precedent).
- P2: pouët prodlist page 5 fetched; each prod.php verified via og:title/og:description.
- P3: archive.org metadata API per identifier (title, licenseurl, audio file count, private flags).
- P4: GitHub API spdx_id + raw LICENSE reads for all 15 NOASSERTION cases.
- Dedup: grep pre-append per candidate (identifier/URL/title). ~30 rejections across pockets (normal per wave).

## Counts

- Catalog: 5,831 → **5,971** (+140: 34 + 19 + 44 + 43). Verified with `grep -c '^#### '`.
- Quarantine: 602 rows (unchanged, +0).
- Target 5,930+: **met**.
