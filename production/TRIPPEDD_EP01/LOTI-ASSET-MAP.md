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

## Handoff to base-cut lane

No CONFIRMED green-iris/LOTI assets → **slate gaps remain** for the Luck of the Irish commercial in the EP01 base cut. Reopen this hunt when: (a) Library binaries transfer, (b) additional Drive folders are ingested, (c) remaining transcripts complete. Do not rebuild the commercial from scratch until those are exhausted. Do not silently replace real footage with generated storyboards.

## Methodology note

Filename search was never the method: 80 frames green-scored + visually checked, 9 transcripts text-searched, repo media path-reviewed, Drive folders content-listed, eltorodeoro video frame-inspected. Dense per-frame scene-cut analysis was attempted but decode throughput on 3.3 GB made it impractical in-lane; recorded here as a coverage limit, not a conclusion.
