# TRIPPEDD Conversation & Library Asset Recovery Inventory

**Purpose:** Preserve the TRIPPEDD-related production material discovered in ChatGPT conversation history and the accessible ChatGPT Library, and give production agents a concrete recovery map. This file is an inventory, not a claim that every listed binary has already been copied into Git.

**Created:** 2026-10-10  
**Target repository:** `mhvnsnt/TRIPPEDD-Production-studios-`  
**Primary episode:** EP01 — “THE WALK”  
**Status vocabulary:** `CONFIRMED_IN_LIBRARY`, `CONFIRMED_IN_REPO`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED`, `NOT_MATCHED_TO_LOTI`.

## Canon source of truth

- `docs/creative/EP01-THE-WALK-CANON.md` on `feat/episode01-prompt-first` defines the locked 11-segment order.
- Machine-readable canon: `src/core/canon/episode01.ts`.
- Compliance checks: `src/core/canon/canonCompliance.ts`.
- Episode/gag pipeline: `src/core/pipeline/episodes.ts`.
- Existing source-unblock guide: `docs/EP01-SOURCE-UNBLOCK.md`.
- Repo already contains a production conversation archive: `docs/PRODUCTION-CONVERSATION-ARCHIVE.md`.

The locked order is Cold Open → Motel → Shumafied → Shumafied Disappointment + Cigar Setup → **Luck of the Irish** → Cigars / The Walk → Bag Sequence → Joe → TV → Clothed and Confused → Smoking / Hanging Out.

Luck of the Irish stays between the Shumafied disappointment/cigar setup and the actual cigar trip. The commercial's three specified shots are: (A) distant wide shot with slow suspenseful zoom; (B) closer different angle; (C) wide shot with the fourth-wall break “LUCK OF THE IRISH!!!” and generative handoff. The blueprint records that additional Luck of the Irish gags exist but are not fully documented.

## Conversation-recovered production facts

- A footage log was reported as complete and merged: **17 clips, 21.2 minutes**, selects mapped to the 11 locked segments.
- The Shumafied / disappointment / cigar beats were reported to exist in audio even where the visuals do not cover them.
- Luck of the Irish, Joe, and Clothed and Confused were described as marked slates until built; this is not proof that every related source asset is missing.
- The production search that preceded this inventory covered four ingested Drive folders, the hub repository (main plus an episode branch), and the God Molecule studio. It did **not** establish that all of the user's Drive had been ingested.
- User specifically recalls existing Luck of the Irish picture/video material and a green Irish effect. Do not reject a candidate based on its filename; inspect its frames and audio.
- Never silently replace real footage with a generated storyboard, and never mark an asset “missing” until the accessible media has been visually inspected.

## Related binaries found in accessible ChatGPT Library

These files were visible through the Library inventory. They need to be transferred as original binary files into this repository (or a clearly linked media store) before they can be treated as repo-resident assets.

| Library filename | Type / size | Relevance | Status |
|---|---|---|---|
| `Trippedd: The Lost Acid — Pilot Storyboard.png` | PNG, 2,211,650 bytes | Detailed earlier pilot storyboard; hybrid live-action / generated / animation / 3D structure and production workflow | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`; not the Luck of the Irish commercial |
| `The Lost Acid: A Gritty Storyboard.png` | PNG, 2,102,626 bytes | Earlier gritty storyboard with scene beats and visual references | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`; not the Luck of the Irish commercial |
| `Motel Prayer Scene Storyboard.png` | PNG, 2,930,170 bytes | Motel-related storyboard/reference | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`; original-footage relationship unverified |
| `Goodville: Not South Park.png` | PNG, 2,127,129 bytes | Goodville gag-family visual reference | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER` |
| `1000168222.mp4` | MP4, 12,266,713 bytes | Approximately 30-second 1280×720 video; inspected frames show a blue glowing cosmic-style head against a starfield | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`; inspected content is not a confirmed Luck of the Irish match |
| `1000167560.jpg` | JPEG, 610,012 bytes | Generic camera-named image from the same date cluster as motel/storyboard material | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |
| `1000167561.jpg` | JPEG, 515,137 bytes | Generic camera-named image from the same date cluster | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |
| `1000167562.jpg` | JPEG, 657,321 bytes | Generic camera-named image from the same date cluster | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |
| `1000167575.png` | PNG, 142,797 bytes | Generic camera-named image, September 6 | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |
| `1000167576.png` | PNG, 172,302 bytes | Generic camera-named image, September 6 | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |
| `1000167577.png` | PNG, 190,155 bytes | Generic camera-named image, September 6 | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |
| `1000167578.png` | PNG, 191,927 bytes | Generic camera-named image, September 6 | `CONFIRMED_IN_LIBRARY`, `NEEDS_BINARY_TRANSFER`, `NOT_YET_VISUALLY_VERIFIED` |

Other numeric files are present in the Library (including several `10001680xx`, `10001682xx`, `10001683xx`, `10001684xx`, and `10001685xx` images). Their relevance to TRIPPEDD has not been verified. Do not bulk-label them as show assets without visual review. Search the Library using the date clusters and inspect thumbnails/contact sheets before assigning show/segment IDs.

## Repository material already present

- `docs/creative/EP01-THE-WALK-CANON.md` — locked editorial blueprint (found on `feat/episode01-prompt-first`).
- `docs/EP01-SOURCE-UNBLOCK.md` — source-ingestion unblock notes.
- `docs/PRODUCTION-CONVERSATION-ARCHIVE.md` — prior production discussion archive.
- `docs/TRIPPEDD-FORMAT.md`, `docs/TRIPPEDD-NETWORK-SLATE.md`, `docs/TRIPPEDD-UNIVERSE-AND-SERIES-TAXONOMY.md` — broader show/network context.
- `docs/PROGRAMMING-AND-INTERSTITIAL-GRAMMAR.md` and the TRIPPEDD grammar documents — style/transition context.
- `assets/references/` exists in the repo; inspect it before duplicating or creating a second reference library.

## Required recovery workflow

1. **Do not rename or overwrite originals.** Preserve source filename and source location in a manifest.
2. Inventory every accessible source file with filename, source folder/link, file size, media type, duration/dimensions, SHA-256 when obtainable, and access status.
3. For each video, extract representative frames across the full duration and around scene changes; create contact sheets. Review audio/transcripts as well as visuals.
4. For each candidate, record timestamp ranges, visible content, dialogue/audio clues, likely show/episode/segment, confidence, and reviewer.
5. Explicitly search for the remembered green Irish effect and commercial elements by frame content, not filename alone.
6. Map confirmed footage to `PENDING_LOTI_WIDE`, `PENDING_LOTI_CLOSEUP`, and `PENDING_LOTI_ACTION` only after visual verification. These are requirements, not filenames and not evidence of absence.
7. Keep Joe's 2D reconstruction, Goodville gag-family assets, The Lost Acid references, and The Walk source footage in separate manifest categories.
8. Binary-transfer files into `assets/references/trippedd-library-recovery/` only after each file is verified and the transfer route supports original bytes. Use Git LFS or a suitable media store for large videos rather than committing oversized binaries directly.
9. Update this inventory with actual repository paths, checksums, and commit links when the binary transfers are complete.

## Current limitations — do not misreport

- This commit records an evidence-backed inventory and recovery plan. It does **not** mean the Library binaries listed above have been copied into Git.
- The available GitHub write connector in this session supports text files and Git objects, but no direct upload path for arbitrary local binary bytes was available. Do not create fake image/video files, base64 text pretending to be media, or placeholder assets.
- The original four Drive folders' actual contents and every frame of the reported 17 source clips have not been re-inspected in this pass.
- No specific green Irish effect has yet been visually confirmed.
- “Not found in the current accessible index” must not be rewritten as “does not exist.”

## Next deliverable

Create a checksum-backed `production/media/asset-manifest.csv` and contact sheets for the available source footage; then transfer verified original binaries through a supported Git/LFS or storage route. Prioritize the 17 logged EP01 clips and every likely Luck of the Irish candidate before generating replacement material.
