# Muse / Ashes — EP01 Creative Material Recovery Index

**Purpose:** One entry point for Muse, Ashes, and production agents to locate recovered material and distinguish repository files from source files that still need to be transferred.

**Canonical repo:** `mhvnsnt/TRIPPEDD-Production-studios-`  
**Episode canon:** `docs/creative/EP01-THE-WALK-CANON.md` and `src/core/canon/episode01.ts`  
**Recovery status:** Index only; do not claim untransferred ChatGPT Library binaries are present in Git.

## Read this first — hard rules

1. Preserve canon and original filenames. Do not silently rename, merge, reorder, or replace source assets.
2. The visual effect the creator asked to locate is the **green iris effect** — not “Luck of the Irish.” Search the existing footage for the effect and record exact filename + timecode after visual confirmation. Do not infer that a blue cosmic-head clip is the green iris.
3. **Luck of the Irish** is separately an EP01 commercial segment with a locked placement in the episode canon. Do not confuse the effect hunt with that segment.
4. Keep recovered originals, generated boards, AI proposals, and confirmed canon in distinct categories.
5. For missing style details, record **UNKNOWN / ASK CREATOR**. Do not invent the Joe 2D style or claim missing source media has been recovered.
6. Keep the locked EP01 segment order in the canonical files. This index is not permission to edit that order.

## Material map

| Topic | Known repository location / source | Status and handling |
|---|---|---|
| Episode order and treatments | `docs/creative/EP01-THE-WALK-CANON.md`; `src/core/canon/episode01.ts` | Canon source of truth. Read before assembly. |
| Shumafied | EP01 canon: Shumafied pack/device gag; followed by “Shumafied Disappointment + Cigar Setup” | Canon segment documented. Search production/source footage for original takes, dialogue, stills and inserts; inventory exact paths before claiming complete. |
| Joe reference / reconstruction | `Motel Prayer Scene Storyboard.png` in ChatGPT Library (see recovery manifest); EP01 canon describes Joe as a 2D reconstruction of a real event with no footage of the event | Library binary not yet confirmed copied into Git. Exact 2D visual style is not documented: ask creator before building. Preserve as reconstruction, never label as recovered footage. |
| Clothed and Confused | `docs/creative/EP01-THE-WALK-CANON.md`; `src/core/canon/episode01.ts` | Canon treatment is realistic survival-documentary parody, not 2D or cartoon-like 3D. Search for original treatment/notes and production assets; do not genericise. |
| Goodville Geography | `src/core/pipeline/episodes.ts` and EP01 canon notes | Existing gag family entry; documentary gag using real interview material (“45 minutes away”). Find and index source footage. |
| Goodville Cartoon | `src/core/pipeline/episodes.ts` and EP01 canon notes | Existing gag family entry; animated cutaway set in Goodville, TN. Additional Goodville gags are known but not fully inventoried; mark missing items as unresolved rather than inventing them. |
| Lost Acid — pilot board | ChatGPT Library: `Trippedd: The Lost Acid — Pilot Storyboard.png` | 2,211,650 bytes in prior Library inventory. Binary transfer still required; keep distinct from alternate board. |
| Lost Acid — gritty board | ChatGPT Library: `The Lost Acid: A Gritty Storyboard.png` | 2,102,626 bytes in prior Library inventory. Time-coded gritty live-action reference. Keep as earlier/alternate until canon status is confirmed. |
| Motel / Joe prayer board | ChatGPT Library: `Motel Prayer Scene Storyboard.png` | 2,930,170 bytes in prior Library inventory; 16-panel motel/Joe prayer sequence. Binary transfer still required. |
| Generated Lost Acid board | `assets/references/ep01/lost-acid-generated-board.manifest.json`; `assets/references/ep01/lost-acid-subjectivity-board.svg` | Repository has generated/reference manifest and SVG companion. This is not the same thing as the two Library PNG boards. Manifest records the PNG as a local generated artifact, not confirmed as committed. |
| Green iris effect | Existing footage to be visually inspected; see `assets/references/ep01/library-recovery-manifest.md` and `docs/EP01-SOURCE-UNBLOCK.md` | Target remains unverified. Do not call `1000168222.mp4` the green iris effect: previous frame inspection described a blue glowing cosmic-style head, not a confirmed match. |
| Other EP01 source media | `assets/references/ep01/library-recovery-manifest.md`; `docs/EP01-SOURCE-UNBLOCK.md` | Follow source transport and checksum-verification process before treating files as recovered. |

## Known Library inventory — preserve exact filenames

The following were recorded in the source-media recovery manifest. They are **not** asserted to be present as binaries in this repository until verified:

- `Motel Prayer Scene Storyboard.png` — 2,930,170 bytes
- `Trippedd: The Lost Acid — Pilot Storyboard.png` — 2,211,650 bytes
- `The Lost Acid: A Gritty Storyboard.png` — 2,102,626 bytes
- `1000168222.mp4` — 12,266,713 bytes; blue cosmic-head imagery reported, green-iris match unconfirmed
- `00-reference-contact-sheet.jpg` — 311,501 bytes; character/VFX reference, green-iris match unconfirmed

Use `assets/references/ep01/library-recovery-manifest.md` as the detailed source-media inventory and update it when files are transferred or new Library filenames are supplied. Do not rename source files to make them appear more descriptive.

## Where agents should look

- **Canon / locked order:** `docs/creative/EP01-THE-WALK-CANON.md`, `src/core/canon/episode01.ts`
- **Goodville gag family:** `src/core/pipeline/episodes.ts`
- **Source-media transport:** `docs/EP01-SOURCE-UNBLOCK.md`
- **Library recovery inventory:** `assets/references/ep01/library-recovery-manifest.md`
- **Generated Lost Acid board provenance:** `assets/references/ep01/lost-acid-generated-board.manifest.json`
- **Generated SVG board:** `assets/references/ep01/lost-acid-subjectivity-board.svg`
- **Pilot ending:** `docs/pilot/EP01-ENDING-LOST-ACID.md`

## Required manifest update format

For every new item found, record:

- Exact original filename and source repository/path (or “ChatGPT Library — transfer pending”).
- Asset type (video, still, storyboard, treatment, script, audio, generated reference).
- Related gag/segment.
- Provenance (original capture / creator document / generated proposal / unknown).
- Current status: `RECOVERED`, `LOCKED_CANON`, `MISSING_SOURCE`, `GENERATED_REFERENCE`, or `UNKNOWN_ASK_CREATOR`.
- For footage effects: verified timecode and reviewer; never claim visual confirmation from filename alone.
- Transfer/checksum status when binary media is added.

## Immediate next actions

1. Use the documented authorized source-media transport in `docs/EP01-SOURCE-UNBLOCK.md`; do not bypass access controls.
2. Transfer the three named storyboard PNGs into `assets/references/ep01/source/` with original filenames and checksums.
3. Search and log source footage for Shumafied, Joe references, Clothed and Confused, Goodville gags, Lost Acid, and the **green iris effect**.
4. Update the detailed recovery manifest with actual paths and verified transfer status.
5. Keep this index synchronized so Muse/Ashes can find the material without treating a reference or proposal as recovered source.
