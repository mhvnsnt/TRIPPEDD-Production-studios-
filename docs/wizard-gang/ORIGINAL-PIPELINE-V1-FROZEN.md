# WIZARD GANG — PIPELINE ONE (original pipeline, saved + still in use)

**Status: SAVED AS PIPELINE ONE, 2026-10-29 by owner order.** This is the exact setup that
generated the first Wizard Gang episodes, logged and named so it can always be gone back to.
**Pipeline One is NOT retired** (owner clarification 2026-10-29 ~12:18 CDT): Chatterbox voices,
Viggle AI body replacement, Muse video generation as a base layer, and the pan-and-zoom
parallax shots (moving background behind the character — makes the 2D world feel 3D; owner
wants a lot MORE of these, here and on the other shows) all carry into the new real-cartoon
pipeline. The V2 real-animation stack (see `REAL-ANIMATION-V2-STACK.md`) wires around
Pipeline One to lock character identity and consistency — it does not replace it.

**Name:** `PIPELINE ONE` — "the original Wizard Gang pipeline"

**Identity/drift rule (owner 2026-10-29):** a little drift is fine — the show is
interdimensional television. Robed versions drift least. UNROBED versions must hold
face / body / skin / eyes / character design. The hood-off identity-change scene is a
deliberate comedic gag, not drift.

---

## What V1 produced

| Deliverable | File / link | Notes |
|---|---|---|
| EP01 final | `wizard-gang-ep01-16x9-dialogue-v10.mp4` | 196 MB, 301 s, 16:9, 51 inserts. Owner-locked 2026-10-13: "That's it… That's the episode." |
| EP01 on YouTube (unlisted) | 540p https://youtu.be/LEeXH8IieLc · 1080p https://youtu.be/1kdxhKfUHOI | Owner decisions still open: delete 540p dupe? flip 1080p public? |
| The 50 s pilot cut | cold open of EP01 | Also serves as show intro / ad cut. |
| EP02 delivered file | (TRIPPEDD repo history) | **Owner correction, standing:** only the first 50 s are real animation; the remaining ~4:10 are still images with pans/zooms. Never describe it as a finished animated episode. |
| Kiko song video | "Encore Anyway" MIX-v3 / MIX-v5 | D minor, 60 BPM, song cuts dead at 151.96 s, never fades. v3 https://youtu.be/q1rV-QTX1cs · v5 https://youtu.be/h8yE7G4LCFQ |

Provisional first full cut (2026-10-07, commit `c416890`, repo `mhvnsnt/TRIPPEDD-Production-studios-`):
production title **"THE SUMMIT"** — 50 s pilot v2 as cold open + ~4:10 episode material,
29-scene storyboard, 27 animated shots, 5 gap stills, 20 original per-scene audio stems,
provenance + visual/QC manifests, regenerable assembly script.

## The V1 chain, step by step (named parts)

1. **Viggle AI (model V4.5 Lite)** — character-motion generations in chunks.
   - Chunk 1: white-robe entrance, ref `muta-white-5.jpg` → `viggle-chunk1-muta-whiterobe2.mp4` (32.08 s)
   - Also: `viggle-chunk1-muta-facepaint.mp4`, `viggle-chunk2-muta-whiterobe.mp4`, `viggle-chunk3-muta-masked.mp4`, `viggle-muta-test-1.mp4`
   - Cleaned cuts: `production/WIZARD_GANG_EP01/video/viggle-chunk1-clean.mp4`, `viggle-chunk2-clean.mp4`, `viggle-chunk3-clean.mp4` (TRIPPEDD-Production-studios-)
   - Viggle status at freeze: parked, 5 free generations left.
2. **Muse media generation** — AI clips + stills (`media-generation-*` files in EP01/video):
   Kiko pier scene + continuations 1–11, gap stills, and the still-image shots that make up
   most of EP02 past the intro (stills animated by pan/zoom in the edit).
3. **Face-swap / head-swap passes** — `production/WIZARD_GANG_EP01/video/faceswap/`, `faceswap-v2/`,
   `headswap/`, `headswap-v2/`.
4. **AI body-replace notebooks** — ComfyUI/Viggle body-replace (`ai-body-replace/` folders vendored
   in TRIPPEDD-Production-studios-, TRIPPEDD-Animation-Studio, wizard-gang-storage, God-Molecule-Show-Studio).
5. **Fix-up kit** — EbSynth + RIFE interpolation + AnimeGAN (God-Molecule animation-kit);
   ToonCrafter cartoon inbetweening experiments (cape-jones, Kaggle/Colab) — **never produced
   verified output; do not claim it works.**
6. **Pocket Studio** — AI-video production hub app (`mhvnsnt/pocket-studio`, V2 live).
   V1 archived: release `vft-archive-2026-10-15` in `mhvnsnt/video-fix-tools` (5 tar parts, SHA256-verified).
   Project JSONs incl. `project-ep02-v8b.json`. Toon Mash Studio (predecessor) archived in
   `toon-mash-studio-archive`, release `backup-2026-10-15`.
7. **Voices — Chatterbox TTS zero-shot clones (THIS PART CARRIES INTO V2).**
   Commercial-safe engines only; XTTS v2 is a commercial dead-end (CPML) — prototype only, never shipped.
   - Ashes + Narrator — Bill $aber ("All 9" voice). Narrator is voice-only until owner says otherwise.
   - Static — Enzo Amore. Cipher — Lio Rush (Blackheart). Sombra Negra — Damian Priest.
   - Kiko — Keiji Mutoh reference (`~/workspace/voice-clone-work/kiko/ref/mutoh-noah-clip.mp3`).
     Mutoh is retired and alive — never make him sound dead; never reveal how the song was made in copy.
   - Theory, Onyx — real-person references, consented.
   - Lane repo: `mhvnsnt/wizard-gang-voice-pipe` (`scripts/render_voice.py`).
8. **Assembly** — ffmpeg timelines from the regenerable assembly script; grade/effects per
   `production/WIZARD_GANG_EP01/TRIP-EFFECTS-DIRECTION.md`; wavy trippy title-card treatment =
   show + TRIPPEDD network ident. Ashes keeps the grin/mouth signature in every style.
9. **Social/clips** — Facebook page clips are cut ONLY from the finished v10 (CLIP SOURCE LAW,
   DUPLICATE-CHECK LAW — check actual media, not captions).

## Where V1 lives

- EP01 production folder: `mhvnsnt/TRIPPEDD-Production-studios-` → `production/WIZARD_GANG_EP01/`
- EP01 dialogue smalls: `mhvnsnt/wizard-gang-storage` release `wg-ep01-dialogue-smalls-20261017`
- Voice lane: `mhvnsnt/wizard-gang-voice-pipe`; local work dir `~/workspace/voice-clone-work/`
- **OPEN CHECK (flagged by the 2026-10-29 audit):** EP01 masters are NOT on wizard-gang-storage's
  main tree despite older docs saying so. Masters' current location needs one dedicated check
  before anyone relies on it.

## Rules that stay true in both pipelines

- Owner hears and approves every voice before it goes in an episode.
- Canon cast (9): Ashes, Onyx, Theory, Cipher, Echo, Static, Hollow, Sombra Negra, Kiko.
  No other character names in show copy (the "Stims" incident, 2026-10-17).
- AI/ANIMATION BOUNDARY (owner 2026-10-11): AI makes PIECES. Animation runs on the cutout
  method. Generative AI may ASSIST (in-betweens, cleanup) — never as sole animator. V1 is the
  exception that proved the rule; V2 is built on it.
