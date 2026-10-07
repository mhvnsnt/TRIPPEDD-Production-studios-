# WIZARD GANG PILOT (SHORT_01) — PROVENANCE MANIFEST
Produced 2026-10-07. Working title only; show name NOT locked.

## Deliverables
| File | Duration | Size | SHA-256 |
|---|---|---|---|
| `wizard-gang-pilot-9x16.mp4` | 50.0s | 1080x1920 h264+aac | `661b1d9f83bf96aa4e9c01a2effff97706277c017d9742f61137f487ba41122f` |
| `wizard-gang-pilot-16x9.mp4` | 50.0s | 1920x1080 h264+aac | `fb7d3dd3b33b458fc67dc63687bcf028b8df0be437c74e4ae1ce77a0e52f` |
| `wizard-gang-pilot-16x9-v2.mp4` | 50.0s | 1920x1080 h264+aac | `29a5e07151575dbe2991c5638e7e2040305d514030291a2724db2c2da0f63c5b` |
| `audio/soundscape_50s.wav` | 50.0s | 44.1kHz stereo | built by `audio/build_soundscape.py` |

## v2 16:9 expanded reframe (owner 2026-10-07: v1 16:9 felt cropped)
v1's 16:9 center-cropped the portrait/square shot sources (02-ashes 672x1344,
04-echo 960x960, 05-static-cipher 1152x768, 07-sombra 768x1152), clipping
heads/feet. v2 rebuilds those 4 shots at true expanded 16:9: each source still
outpainted to 2048x1152 in the locked cartoonier style (owner's refs as anchors;
characters pixel-faithful, background extended, no new characters/text), then
re-animated via image-animation. The 5 full-height v1 shots (01/03/06/08a/08b)
and the title cards are reused VERBATIM from v1 (owner loves the wavy trippy
card treatment). Same shot timing, same soundscape mix. Assembly:
`assemble_v2.py` (ffmpeg: fit new shots, concat reuse+new segments, mux audio).
New finals: `shots/shot02-ashes-v2.mp4`, `shots/shot04-echo-v2.mp4`,
`shots/shot05-static-cipher-v2.mp4`, `shots/shot07-sombra-v2.mp4` (+ 16:9
intermediate stills in `shots/`). Superseded: v1 `wizard-gang-pilot-16x9.mp4`
kept for reference; the failed first ashes animation (hallucinated POLICE sign,
caught in QC) was discarded and never shipped. 9:16 master untouched.

## Source chain (per shot)
All 9 stills: generated in-session via `media.generate_image` in the owner's
LOCKED cartoonier base style, using his own art from
`assets/wizard-gang-style-refs/cartoonier/` (16 images) as style references.
Every still passed per-shot QC by the coordinator's own eyes before use.
→ `stills/` (9 .webp + generation .json receipts).

All 9 shot videos: generated via `media.generate_video` image-animation from
the stills (one generation per shot, 10s @ 24fps). QC-passed via mid-frame
checks. → `shots/`.

## Audio (100% original / license-clean)
`soundscape_50s.wav` is fully synthesized in-repo by `audio/build_soundscape.py`
(numpy: fire crackle, chains, city-night tone, sub-bass, ritual drum — the
owner-approved hybrid approach: open-source synthesis, zero sampled material).
No third-party samples. No spoken dialogue in this cut.

## Dialogue
Pilot ships soundscape-only. `DIALOGUE.md` holds 2 draft Static lines
(L1 ~0:23 shot 5; L2 ~0:40 shot 8 Kiko reveal) — OWNER APPROVAL REQUIRED
before any voice is recorded or mixed. Stock-Piper voices are RETIRED for
based-on characters (owner rejection 2026-10-07); only a genuine Enzo Amore
likeness clone may voice Static. All other cast: visual-only beats.

## Assembly
`assemble_fast.py` — ffmpeg two-stage: pre-fit each shot to the output frame
(center-crop for portrait/square sources; gentle Ken Burns lateral pan for
wide sources), concat, mux soundscape. `fix_8b.py` re-aimed the 8b pan so the
Kiko reveal opens the frame in 9:16 (defect found + fixed in QC, 2026-10-07).
`pilot_assemble.py` is the superseded MoviePy attempt (too slow), kept for
provenance only. `assemble_tmp/` = disposable intermediates, NOT committed.

## Text on screen
ONLY canon-locked cards: "WIZARD GANG" (4s) → "TRIPPEDD" (4s). "SWMG" appears
solely as jewelry engraving (canon-allowed). The words "Shadow Wizard Money
Gang" are never rendered as text. Narrator beat HELD (not produced).

## Storyboard fidelity
Shots 1–8 + shot 9 title cards per STORYBOARD.md. One QC-driven fix: shot 8b
pan re-aimed so Kiko is visible in 9:16 (was cropped out). No other deviations.
