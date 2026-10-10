# Luck of the Irish — Green Iris Effect: Build Notes

**Status: COMPONENTS PREPPED — FINAL RENDER ON HOLD** (owner 2026-10-10: footage must be edited/arranged first; the base-cut lane arranges Shots A/B/C from the 17 clips, then the final green iris render happens on that arranged footage).

**Spec source:** `src/core/pipeline/effects.ts` (`EffectOrchestrator.runLuckOfTheIrish`), `src/core/pipeline/gags.ts` (`LUCK_OF_THE_IRISH_DISCLAIMERS`), `src/components/JobsPipeline.tsx` (title/disclaimer prompts), `docs/creative/EP01-THE-WALK-CANON.md` (Shots A/B/C). CLAUDE.md: A and C share one camera setup, B is the other angle; ad runs A, B, C.

## Components (all visually verified)

1. **`hood-leprechaun-transform-test.webp`** — image-edit of a real EP01 frame (two people chilling outside motel room 226, `VID_20260906_104606093` f_002) with the exact spec prompt: "Hood Leprechaun, 8k, photorealistic, glowing green iris, wearing green track suit". Likeness preserved, character changed: glowing green eyes, green tracksuits, shamrock detail. This is the transform target look.

2. **`green-iris-transition-demo.mp4`** (5s, 1280x720) — the reusable That's-all-folks template, demonstrated on the test frames: source footage (1.5s) → emerald-green iris closes in (1s) → full green swap point → iris opens (1s) revealing the leprechaun transform → freeze hold (1.5s). Verification frames: `iris-t2.png` (iris closing), `iris-t3.png` (iris opening on the transform).

3. **`mask.mp4`** — the reusable iris mask (grayscale): full-white → circle shrinks to 0 over 1s → circle grows back over 1s → full-white. Apply via `maskedmerge` against any A/B pair: trim 0–2.5s for the close, 2.5–5s for the open. Rebuild command (ffmpeg `geq`):
   ```
   lum='if(lte(hypot(X-640,Y-360),800*lt(T,1.5)+800*(2.5-T)*gte(T,1.5)*lt(T,2.5)+800*(T-2.5)*gte(T,2.5)*lt(T,3.5)+800*gte(T,3.5)),255,0)'
   ```
   Iris color used: emerald `0x00A86B`.

4. **`title-card.mp4`** (4s) — "LUCK OF THE IRISH™" in bold emerald green (`0x50C878`) typography on black, subtitle "Nobody knows what it is." (per the JobsPipeline titlePrompt).

5. **`disclaimers-card.mp4`** (8s) — all 13 `LUCK_OF_THE_IRISH_DISCLAIMERS`, white fine-print on black, wrapped and verified readable (per the JobsPipeline disclaimerPrompt: "Leprechaun magic not guaranteed. Void where prohibited." energy).

## What waits on the base cut

- The final render composites the green iris transition onto the ARRANGED Shots A/B/C from the base-cut lane (checkpoint `trippedd-ep01-basecut.json`): Shot A (far, slow zoom) → Shot B (closer angle) → Shot C (wide, "LUCK OF THE IRISH!!!") → GREEN IRIS EFFECT → title card → disclaimers → back to episode.
- Transform target for the final: run the hood-leprechaun image-edit on the actual Shot C freeze frame when it lands.
- Audio bed: added at final assembly (template is video-only by design).

## Verification log

- Transform test: opened and read — same two people, same pose/framing, green glowing eyes, green tracksuits. PASS.
- Iris demo: frames at t=1/2/2.5/3/4 — iris closes on source, full-green swap, iris opens on transform. Reads clearly. PASS.
- Title card: frame read — bold emerald type, legible. PASS.
- Disclaimers: frame read — all 13 present and readable, none clipped. PASS (after one rewrap fix).

## FINAL RENDER (2026-10-10) — luck-of-the-irish-commercial-final.mp4

**Status: BUILT AND VERIFIED.** 53.4s, 1920x1080, h264+aac, 1600 frames.

**Source:** `VID_20260906_160938849` (base-cut lane find) — Shot A [0:00–0:12] far/slow-zoom chilling → Shot B [0:12–0:30] closer angle, "Look at the Irish." spoken ~0:18 (production audio kept) → Shot C [0:30–0:35] fourth-wall break direct to camera. A,B,C order per CLAUDE.md.

**Effect beat (owner: right time, right scene):** Shot C ends on the t=35 direct-to-camera freeze frame → 0.5s hold → green iris closes (1.5s, linear, soft edge, emerald 0x00A86B — That's-all-folks style) → 0.3s green hold → iris opens (1.5s) revealing the hood-leprechaun transform (exact spec prompt on the actual Shot C frame: same grin/dreadlocks/beard, glowing green iris eyes, green tracksuit — likeness preserved) → 2.5s hold → title card (4s) → 13 disclaimers (8s).

**Audio:** production audio through Shot C; synthesized noise-swell whoosh across the 3.3s transition; silence on transform hold/title/disclaimers.

**Build notes:** maskedmerge misbehaved (blended ~50/50 regardless of mask); xfade circlecrop/circleopen closed too fast (non-linear). Final uses hand-rolled linear iris via geq mask → alphamerge → overlay. First concat attempt (demuxer) broke video past 35s; final uses single-pass concat filter. All 8 beats frame-verified + audio levels checked (speech -24.4dB, whoosh -19.6dB, cards -91dB).
