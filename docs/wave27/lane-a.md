# Wave 27 — Lane A notes: catalog deepening (2618 → 2701)

**Branch:** `wave27-lane-a` (from 8662ea1) · **Status:** ready to commit · **Do NOT push/merge** (coordinator merges sequentially) · **Untouched:** `production/WIZARD_GANG_EP01/` (another worker's uncommitted changes)

## Final honest count
- `grep -c '^#### ' docs/RESOURCE_CATALOG.md` = **2701** (+83 new: 17 PD score archives + 13 chiptune tools + 53 caption burn-in SaaS)
- 83 entries carry `[Wave 27 Lane A]`; 7 new quarantine rows **256–262** in `docs/LICENSE_QUARANTINE.md`.

## Wired tool (real proof, no fakes)
- **libopenmpt** — PASSED 2026-10-07 ~21:35 EDT. `ctypes` wire against system `/usr/lib/x86_64-linux-gnu/libopenmpt.so.0` (apt had no `openmpt123`/`libopenmpt-dev`; runtime lib was present). Self-composed ProTracker MOD rendered: 4 channels, 7.68 s, 373,440 frames @48 kHz, peak 0.5733, RMS 0.1789, all 4 checks true.
- Artifacts in `tools/wave27-lane-a/`: `wire_openmpt.py`, `lane-a-openmpt-test.mod` (2,492 B), `lane-a-openmpt-test.wav` (1.49 MB), `lane-a-openmpt-proof.json`. No catalog entry written for libopenmpt — an existing Wave 12 Lane A entry (catalog line ~12853) already covers it.
- **Game_Music_Emu** — cataloged but flagged QUARANTINED against existing row 184 (LGPL-2.1); no new quarantine row, never wired into shipping paths.

## Honest negatives (rejected, not appended)
1. **EasySub** — dropped as a duplicate of the Wave 13 Lane C entry (catalog line 14973, easysub.com).
2. **Offeo** — dropped; 2026-10-07 caption-feature search returned no auto-caption evidence.
3. **faster-whisper** — dropped; existing entry at catalog line 2062 (SYSTRAN/faster-whisper).
4. **Simon Says** — dropped; existing Wave 13 Lane C entry (simonsaysai.com).
5. **Covered by Waves 24 Lane B / 26 Lane B** (dropped before verification): Submagic, Happy Scribe, Loom, Rev/Rev AI/Temi, Descript, Kapwing, OpusClip, Maestra, Otter.ai, Notta, Zeemo, Sonix, Vizard, Tella, Screen Studio, Capsho, api.video, Bunny Stream, Wistia, Web Captioner, Wisecut, SyncWords, Wordly, Nova AI, Audext, FlexClip, Pictory, YouTube Studio auto-captions.
6. **Bubbles** — caption feature unverified; dropped. **ScreenRec** — no caption feature; dropped.
7. **Schism Tracker / Furnace / MilkyTracker app / 0CC-FamiTracker** — existing quarantine rows; not re-added. **Chant21** — wrong pocket (covered elsewhere, not caption).

## Replacements (genuinely new, verified 2026-10-07)
- **Gglot** (gglot.com; $14.99–$149/mo; subtitles + translation + API) — EasySub slot.
- **KwiCut** (Wondershare; $7.99/mo; auto-generated subtitles; free trial) — Offeo slot.
- **Scripsy** (scripsy.ai; YouTube transcription + summaries, SRT export, $4/mo, free trial) — faster-whisper slot.
- **AddSubtitle.ai** (Talecast; browser-based subtitling + lip-sync dubbing, API; $15/mo) — SimonSays slot.

## License badges (all verified from upstream 2026-10-07, never assumed)
- Pocket 1: 5 ✅ commercial-safe (BandMusic PDF Library, RISM Online, E. Azalia Hackley Collection, lutemusic.org, NLW Welsh traditional music); rest ⚠️/❓ per-work.
- Pocket 2 ✅ commercial-safe: libmodplug (PD), vgmstream (ISC), VGMToolbox (MIT), MilkyPlay (BSD-3-Clause), PicoTracker (BSD-3-Clause), NEZPlug (zlib/libpng). ⚠️: vgm2wav (LGPL-2.1), Game_Music_Emu (LGPL-2.1, quarantined row 184), ACID64 (closed freeware), Beepola (freeware/unverified), PixiTracker (proprietary demo), Audio Overload (freeware), ASMA (per-tune rights vary).
- Quarantine 256–262 (all GPL-2.0 / GPL-2.0-or-later / GPL-2.0+): xmp-cli, UADE, sidplayfp, ASAP, lazyusf2, QMMP, NotSo Fatso.
- Pocket 3: all 53 ❓ unverified (proprietary SaaS, ToS not reviewed); URLs verbatim from 2026-10-07 searches.

## URL rules compliance
- All URLs verbatim from search-result Full-URLs lists or verbatim in result body text. VideofaST = `https://videofa.st/en/add-subtitles-to-video/` (not videofast.com).
- `https://www.elevate.io/` and `https://www.plainscribe.com` appear verbatim in result bodies (not Full-URLs lists) — flagged here.

## Pre-append dedup
- All 83 appended names grepped against the catalog pre-append. The only hits (Animaker, SimonSays, faster-whisper) were investigated: Animaker had no `####` entry (only a URL mention in another entry) → safe; SimonSays and faster-whisper had real entries → dropped.
