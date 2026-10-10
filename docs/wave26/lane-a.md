# Wave 26 Lane A — PD score-archive continuation + retro-tracker ecosystem depth

**Entries appended: 55** (`####` headings) · **Quarantine rows added: 12 (239–250)** · Audit date: 2026-10-07
Coordinator: append-only into RESOURCE_CATALOG.md; no renumbering, no rewrites of earlier entries. Catalog count now **2,563** honest `####` headings (was 2,508). Branch: `wave26-lane-a`.

## Method note

- **Dedup:** every candidate grepped (case-insensitive) against `docs/RESOURCE_CATALOG.md` `####` headings before inclusion; quarantine candidates also grepped against `docs/LICENSE_QUARANTINE.md`. Skipped as already-cataloged: IMSLP, Mutopia, Musopen, Kunst der Fuge, RISM, Gallica, Contemplator, Sonic Pi, FoxDot, OpenGoldberg, CPDL/ChoralWiki, sfxr, jsfxr, RFXGEN, DDSP/SVC, Demucs, Spleeter, librosa, Airwindows, Tone.js, howler.js, SoLoud, miniaudio, Pure Data, Orca, STK, VCV Rack, TidalCycles, Surge XT, Dexed, ZynAddSubFX, Ardour, MuseScore (desktop app row 177; site entry exists), LilyPond, hls.js, video.js, shaka-player, NYPL, British Library (Mechanical Curator/Sounds), SLUB Dresden, DPlayer, PMDWin, Nyquist, VICE.
- **Dn-FamiTracker** maps to existing quarantine row 123 — catalog entry added for discoverability, no new row.
- **SoundTracker (Unix):** existing catalog `❓` entry ("believed GPL") left untouched per append-only rule; GPL-2.0-or-later now verified (Wikipedia + sourceforge git) and recorded as quarantine row 249.
- **License claims:** verified from upstream — GitHub API `spdx_id`, raw LICENSE/COPYING/README fetches, SourceForge license fields, vendor/official terms pages — or badged ❓/⚠️/🚫 honestly. Secondary sources named where used (Wikipedia, KVR, project provenance docs).
- **Environment deviation:** /tmp is a full 512M tmpfs (Lane B's worktree occupies 502M — not touched); worktree created at `~/workspace/agent-ops/w26-lane-a` with sparse-checkout `docs/` only, branch `wave26-lane-a` (pre-existing locally, clean at main tip f449372).

## Pocket 1 — PD score-archive continuation (25 entries)

Mix is deliberately honest: 2 ✅ (Open Hymnal Project, and none other fully clean), 7 ⚠️, 9 ❓, 7 🚫. Notable: **Early Music Online is NONCOMMERCIAL** (BL copyright + JISC Open Education licence — PD-era music, NC digitizations); NinSheetMusic/VGMusic are fan-transcription archives of copyrighted game music; GilvaSunner (Nintendo takedown) and 8bitcollective documented as dead; Project2612/Zophar's Domain/SMS Power as rip-risk negatives.

## Pocket 2 — Retro-tracker ecosystem depth (30 entries)

11 ✅ permissive (Arkos Tracker 3 MIT, Micromod BSD-3-Clause, jfxr BSD-3-Clause, DaisySP MIT, Meyda MIT, DeaDBeeF zlib, Audacious BSD, PortAudio/RtAudio/RtMidi/PortMidi MIT), 7 ⚠️/❓ (LittleGPTracker license conflict, BeRoTracker/uFMOD freeware, XPMCK unverified, libOPNMIDI/WildMIDI/libmikmod LGPL — no new quarantine rows per standing LGPL rule), 12 🚫 quarantined.

### License corrections caught this wave (training-data assumptions overturned by upstream verification)
- **Cmajor is NOT ISC** — dual GPL-3.0-or-later / commercial (LICENSE.md).
- **libADLMIDI is NOT MIT** — GPL-3.0 (API spdx).
- **Aldrin is NOT BSD** — GPL-2.0 (SourceForge).
- **BeRoTracker is NOT public domain** — freeware, no open grant.
- **uFMOD is NOT public domain** — freeware (Wikipedia); only its XM-spec doc was PD-released.
- **Psycle current code is GPL-2.0** — only Arguru's v1.0 sources were PD.
- **LittleGPTracker: unresolved conflict** — canonical repo LICENSE says BSD-3-Clause (© 2018 "Discodirt") while all active community forks assert GPLv3 (Marc Nostromo). Badged ⚠️, flagged do-not-wire.

### Dropped / not included (diligence record)
- MiniFMOD — PD status unverifiable this pass (mirrors carry no license text).
- Buze (Buzz clone) — could not verify license or canonical upstream.
- MMA (Musical MIDI Accompanist) — license not verifiable from upstream this pass (mellowood.ca not fetched).
- ASAP / UADE / ProTrekkr / RMT / Aodix — not verified this pass; left for a later lane rather than badged blind.
- Fonts (Bravura/Leland/Emmentaler/Noto Music/Petaluma/Sebastian/Gonville), Basic Pitch, madmom, Pilot, AudioKit, Teensy Audio, Alda — cut for pocket discipline (kept the 55-count target); all verified-absent from catalog, available as follow-up candidates.

## Wiring — 1 tool with real proof

**Meyda 5.6.3 (MIT)** — `docs/wave26/proofs/meyda-smoke/`: synthesized 2 s WAV (440 Hz + 880 Hz, no copyrighted audio) → `node meyda-smoke.js` → real feature output (`meyda-smoke-output.json` + `PROOFS.md`). Sanity checks pass: chroma peak bin 9 = A (440 Hz), rolloff ≈ 1038 Hz, ZCR = 10/frame. API note: v5.6.3 names the extractor `zcr` (not `zeroCrossingRate`); script corrected and re-run — committed output is from the passing run. Pipeline use: per-cue audio descriptors (brightness/energy/pitch-class) for scoring/SFX matching.

## Quarantine rows added (239–250)

239 libADLMIDI GPL-3.0 · 240 ChibiTracker GPL-2.0 · 241 JSIDPlay2 GPL-2.0 · 242 Cardinal GPL-3.0 · 243 Strudel AGPL-3.0 · 244 BespokeSynth GPL-3.0 · 245 Cmajor GPL-3.0-or-later · 246 Psycle GPL-2.0 · 247 FamiTracker-original GPL-2.0 · 248 Aldrin GPL-2.0 · 249 SoundTracker-Unix GPL-2.0-or-later · 250 mikmod-player GPL-2.0. All research-lane only, never wired into shipping paths.
