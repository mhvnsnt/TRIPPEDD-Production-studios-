# LOTI Asset Map — Luck of the Irish Commercial / Green Iris Effect

**Investigation:** 2026-10-10 (visual investigation lane, checkpoint `loti-visual-investigation.json`).
**Status vocabulary:** CONFIRMED / PROBABLE / UNINSPECTABLE / GENUINELY MISSING — kept strictly separate.
**Naming correction (owner 2026-10-09):** the effect is the **GREEN IRIS EFFECT**. "Luck of the Irish" is the *commercial's* name, not the effect's. The effect = a green iris-style visual treatment (iris wipe / vignette / aperture, possibly a transition device) embedded in footage/pictures.

## The target (from `docs/creative/EP01-THE-WALK-CANON.md`, `feat/episode01-prompt-first`)

- **Shot A** — far away, slow zoom in, suspense-building → requirement `PENDING_LOTI_WIDE`
- **Shot B** — different angle, closer, suspense-building → requirement `PENDING_LOTI_CLOSEUP`
- **Shot C** — back to wide, fourth-wall break "LUCK OF THE IRISH!!!", generative handoff → requirement `PENDING_LOTI_ACTION`
- Then the fake commercial, then back to the episode.

These requirements are production targets, NOT filenames and NOT evidence of absence.

## Asset-type taxonomy (do not conflate)

`original camera footage` ≠ `edited video` ≠ `rendered VFX` ≠ `generated concept art` ≠ `storyboards` ≠ `temp refs` ≠ `finished shots`. Each candidate below is labeled by type.

## CONFIRMED (inspected, contents verified)

*No green iris effect or LOTI commercial footage confirmed in any accessible inspected media.*

| Asset | Type | What inspection found |
|---|---|---|
| 17 MP4s, `~/workspace/drive-ingest/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI/` (21.2 min total) | original camera footage | 80 sampled frames green-scored; max 2.2% green pixels — explained by store-cooler drink labels (`VID_20260906_105329690` f_008) and outdoor trees/sky (`VID_20260906_122211926` f_016). Top candidates visually inspected: no iris effect, no Irish-themed content. |
| 9/17 Whisper transcripts (`~/workspace/trippedd-ep01-transcripts/`) | audio → text | Zero mentions of "luck", "irish", "iris", "green", "leprechaun", "shamrock", "effect", "wipe". (8 transcripts still pending at investigation time.) |
| `eltorodeoroentrance_video.mp4` (38.7 MB, God Molecule Drive folder) | rendered video (wrestling entrance) | 10 frames extracted, 0% green, visually inspected: "EL TORO DE ORO" wrestling entrance — not LOTI. |
| 9 In-the-Bushes PNGs (Drive folder `1pyZAEN7DsU3OSiwnD0bBAAK1JEYvr_C1`) | generated concept art / character art | Character art (Mr. Gold, Mr. Tree, Busch, Cool Dad). Not LOTI. |
| Repo media, `origin/main` + `origin/feat/episode01-prompt-first` | mixed | Wizard Gang style refs, Mars facial linework/mouth evidence, `lost-acid-subjectivity-board.svg` — no LOTI assets by path or content review. |
| ChatGPT Library `1000168222.mp4` (12.3 MB) | rendered VFX | Per Library inspection: blue glowing cosmic-style head vs starfield = COSMIC-HEAD/Mars material. **Explicitly NOT the green iris effect — do not label it as such.** |
| ChatGPT Library `00-reference-contact-sheet.jpg` (311 KB) | temp ref | Cosmic blue head treatment, multiple portrait angles. Character/VFX reference — not confirmed as green iris. |

## PROBABLE

*None. No candidate reached probable confidence.*

## UNINSPECTABLE (existence known or claimed; contents not verified — NOT missing)

| Asset | Location | Note |
|---|---|---|
| `1000168029.png`, `1000168031.jpg`, `1000168032.jpg`, `1000168036.jpg` | ChatGPT Library | Numeric filenames; NOT inspected for Irish material. Pending owner sharing. |
| `1000167560.jpg`, `1000167561.jpg`, `1000167562.jpg`, `1000167575.png`, `1000167576.png`, `1000167577.png`, `1000167578.png` | ChatGPT Library | Generic camera-named, motel/storyboard date cluster. `NOT_YET_VISUALLY_VERIFIED`. |
| Further `10001680xx`–`10001685xx` images | ChatGPT Library | Relevance unverified. Do not bulk-label. |
| 4 Library storyboards (`Trippedd: The Lost Acid — Pilot Storyboard.png`, `The Lost Acid: A Gritty Storyboard.png`, `Motel Prayer Scene Storyboard.png`, `Goodville: Not South Park.png`) | ChatGPT Library | HISTORICAL REFERENCES / generated concept art. The Lost Acid boards are a *different earlier pilot concept*, not The Walk. Never confuse with original footage or finished LOTI assets. `NEEDS_BINARY_TRANSFER`. |
| Other Google Drive folders beyond the 4 ingested | Owner's Drive | **Access gap.** Only 4 folders were ever ingested; the LOTI material may live in folders not yet accessed. Do not declare footage missing on this basis. |
| 8 pending Whisper transcripts | `~/workspace/trippedd-ep01-transcripts/` | Transcription still running at investigation time. |

## GENUINELY MISSING

*Cannot be declared yet.* The green iris effect has not been found in accessible inspected media, but UNINSPECTABLE items above (Library binaries, un-ingested Drive folders, pending transcripts) must be exhausted first. "Not found in the current accessible index" ≠ "does not exist."

## Recovery routes (from repo docs)

- `docs/EP01-SOURCE-UNBLOCK.md`: authorized Drive transport via `TRIPPEDD_RCLONE_CONFIG_B64` + `TRIPPEDD_RCLONE_REMOTE` / `TRIPPEDD_RCLONE_PATH`, or authorized browser cookies.
- `docs/production/TRIPPEDD-CONVERSATION-LIBRARY-ASSET-RECOVERY.md` (commit `6f16f30f`): Library inventory + transfer plan; binaries → `assets/references/trippedd-library-recovery/` via Git LFS or media store (no fake/placeholder binaries).
- `assets/references/ep01/library-recovery-manifest.md` (commit `d7363894`): verified Library items index.

## MAJOR FIND (2026-10-10, verified in repo source): THE EFFECT EXISTS AS BUILT CODE

**CODE = PRESENT. RENDERED MEDIA = MISSING.** The green iris effect was built as a pipeline — its code, prompts, and gag copy are in the repo, but its rendered outputs (transformed leprechaun frames, green iris transition video, title card, disclaimer) have NOT been located. Do not claim the outputs exist.

### The pipeline — `src/core/pipeline/effects.ts` (origin/main, verified)

`EffectOrchestrator.runLuckOfTheIrish` (lines 26–66), three stages:
1. **Extract Frame** — ffmpeg `extract_frame` from the base plate video.
2. **Transform Frame** — ComfyUI `transform_character`, prompt: `"Hood Leprechaun, 8k, photorealistic, glowing green iris"` (line 43). Variant in `src/components/JobsPipeline.tsx:161`: `"Hood Leprechaun, 8k, photorealistic, glowing green iris, wearing green track suit"`.
3. **Green Iris & Freeze** — ffmpeg `green_iris_freeze`: That's-all-folks-style iris in/out, freeze frame, parameters for iris color/thickness, open/close direction, center position, timing/easing, optional sparkle glow + optional commercial title reveal (`LuckOfTheIrishParams`, lines 4–16).

`EffectOrchestrator.generateCommercialPackage` (lines 68–110) chains the full commercial: iris result → ComfyUI title card (`"Commercial title card: LUCK OF THE IRISH, bold green typography, 4k"`) → ComfyUI disclaimer (`"Legal disclaimer screen, white text on black background, fine print"`) → ffmpeg `concatenate_sequence`.

### The gag copy — `src/core/pipeline/gags.ts` (verified)

`LUCK_OF_THE_IRISH_DISCLAIMERS` — all 13 present (ids 001–013), e.g. 001 `CANONICAL_ORIGINAL`: "Luck of the Irish is not responsible for luck, Ireland, leprechauns, gold, or any resulting bullshit." 007: "Side effects may include confusion, confidence, temporary wealth, permanent stupidity, and unexplained green objects."

### The registered asset — `src/core/assets/registry.ts` (verified)

`ast_leprechaun_v001` → `/assets/luck_leprechaun_v001.png`, registered as ComfyUI `concept_art`, `verificationState: 'UNVERIFIED'`, sceneId `sc_04_irish`, project `prj_luck_01`. **The PNG file itself is NOT in the repo** (verified: `git ls-tree` empty). Registration without binary = the concept art was planned/referenced, never committed.

### What this changes

- The hunt for the green iris effect is now TWO hunts: (a) rendered outputs of this pipeline (transformed frames, iris transition video) — searched accessible media, **not found**; (b) the pipeline's *inputs* (which base-plate footage it ran on) — unknown.
- The pipeline is runnable: given a base plate + ComfyUI + ffmpeg, the effect can be REGENERATED rather than only searched for. That's an owner decision (regenerate vs. keep hunting originals).
- Shot mapping: the pipeline's iris+freeze+title+disclaimer sequence corresponds to Shot C (fourth-wall break "LUCK OF THE IRISH!!!" + generative handoff) and the fake commercial itself. Shots A/B (suspense zooms) have no corresponding code found.

## Handoff to base-cut lane

No CONFIRMED green-iris/LOTI assets → **slate gaps remain** for the Luck of the Irish commercial in the EP01 base cut. Reopen this hunt when: (a) Library binaries transfer, (b) additional Drive folders are ingested, (c) remaining transcripts complete. Do not rebuild the commercial from scratch until those are exhausted. Do not silently replace real footage with generated storyboards.

## Methodology note

Filename search was never the method: 80 frames green-scored + visually checked, 9 transcripts text-searched, repo media path-reviewed, Drive folders content-listed, eltorodeoro video frame-inspected. Dense per-frame scene-cut analysis was attempted but decode throughput on 3.3 GB made it impractical in-lane; recorded here as a coverage limit, not a conclusion.
