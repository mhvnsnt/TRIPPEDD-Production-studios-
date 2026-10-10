# EP01 Asset Pull Manifest

**Date:** 2026-10-10
**Directive:** Owner 2026-10-10 — "pull all of that... everything is there, bro. It's all there."
**Recovery index:** `docs/creative/EP01-MUSE-ASHES-RECOVERY-INDEX.md` (used as primary map; cross-checked below)
**Reference copies:** `production/TRIPPEDD_EP01/reference/` (copies — originals untouched)

Status key: `RECOVERED` (in repo) · `LOCKED_CANON` (canon doc) · `LIBRARY_PENDING` (in ChatGPT Library, needs user transfer) · `GENUINE_GAP` (exhaustively searched, not found)

---

## 1. Shumafied (segments 3–4) — RECOVERED

| Asset | Path | Status |
|---|---|---|
| 8-stage visual progression design doc | `reference/shumafied/subjectivity-sequence.md` (orig: `production/EP01/generated/subjectivity-sequence.md`) | RECOVERED |
| Blender subjectivity builder | `reference/shumafied/build_subjectivity.py` (orig: `production/EP01/generated/blender/build_subjectivity.py`) | RECOVERED |
| Subjectivity storyboard (SVG) | `reference/shumafied/lost-acid-subjectivity-board.svg` (orig: `assets/references/ep01/lost-acid-subjectivity-board.svg`) | RECOVERED |
| Canon segment order | `docs/creative/EP01-THE-WALK-CANON.md` | LOCKED_CANON |

The "wasn't even shit" return beat is documented in the design doc (Editorial joke section). Segment 3 (Shumafied pack/device gag) + Segment 4 (Shumafied Disappointment + Cigar Setup) both have canon placement.

## 2. Joe (segment 8) — LIBRARY_PENDING (storyboard) / GENUINE_GAP (2D style)

| Asset | Path | Status |
|---|---|---|
| 16-panel Motel Prayer Scene Storyboard | ChatGPT Library: `Motel Prayer Scene Storyboard.png` (2,930,170 bytes) | LIBRARY_PENDING |
| Canon treatment (2D reconstruction of real event) | `docs/creative/EP01-THE-WALK-CANON.md` | LOCKED_CANON |

Per canon: the Joe encounter genuinely happened; no footage exists; it is a 2D reconstruction. The exact 2D visual style was **never written down** — owner call required before building. Do not label as recovered footage.

## 3. Clothed and Confused (segment 10) — STRUCTURE RECORDED (owner 2026-10-10)

**Owner clarification (2026-10-10):** Images were NEVER generated — correct, don't expect any. The segment structure is:

1. **Storyboard** — exists per owner; NOT found in repo or Library manifest after exhaustive search → see Genuine Gaps.
2. **Concept/treatment doc** ("how it would be") — canon treatment in `docs/creative/EP01-THE-WALK-CANON.md` (realistic Naked-and-Afraid-style survival documentary parody; NOT 2D, NOT cartoon 3D). Earlier concept seed also recovered: `reference/clothed-and-confused/seed_clothed.cjs` ("survivalist who refuses to get naked tries to survive wearing 14 layers" — Absurd, deadpan).
3. **Live footage** — the characters are actually WATCHING the Naked and Afraid show in live footage; the segment escalates out of the TV channel-change (segment 9). **CUT-NOTES.md confirms: "Channel-change and survival material not in the [17] clips."** The TV segment footage (`VID_20260906_170846691.mp4`, Harry Potter on wall TV) exists in base-cut; the channel-change/Naked-and-Afraid watching footage is not in the current clip set.

| Asset | Path | Status |
|---|---|---|
| Canon treatment | `docs/creative/EP01-THE-WALK-CANON.md` | LOCKED_CANON |
| Early concept seed | `reference/clothed-and-confused/seed_clothed.cjs` (orig: repo root `seed_clothed.cjs`) | RECOVERED |
| TV segment base footage ref | `reference/other-segments/CUT-NOTES.md` (segment 9 notes) | RECOVERED |

## 4. Goodville gag family — RECOVERED (entries) / LIBRARY_PENDING (cartoon image)

| Asset | Path | Status |
|---|---|---|
| Goodville Geography + Cartoon gag entries | `reference/goodville/goodville-gag-entries.md` (extracted from `src/core/pipeline/episodes.ts`) | RECOVERED |
| Goodville Geography doc gag | Canon: real interview, "45 minutes away" | LOCKED_CANON |
| `Goodville: Not South Park.png` | ChatGPT Library (per prior inventory) | LIBRARY_PENDING |

## 5. Lost Acid ending — RECOVERED (docs) / LIBRARY_PENDING (boards)

| Asset | Path | Status |
|---|---|---|
| Pilot ending doc | `reference/lost-acid/EP01-ENDING-LOST-ACID.md` (orig: `docs/pilot/EP01-ENDING-LOST-ACID.md`) | RECOVERED |
| Generated board manifest + SVG | `reference/lost-acid/lost-acid-generated-board.manifest.json`, `reference/shumafied/lost-acid-subjectivity-board.svg` | RECOVERED |
| Pilot storyboard (PNG) | ChatGPT Library: `Trippedd: The Lost Acid — Pilot Storyboard.png` (2,211,650 bytes) | LIBRARY_PENDING |
| Gritty storyboard (PNG) | ChatGPT Library: `The Lost Acid: A Gritty Storyboard.png` (2,102,626 bytes) | LIBRARY_PENDING |

## 6. Other segments — RECOVERED (base-cut documented)

Cigars, Bag Sequence, TV, Smoking/Hanging Out all have base-cut footage documented in `reference/other-segments/CUT-NOTES.md` and `reference/other-segments/EP01-SEGMENTS.md`. Cold Open, Motel exist in locked order.

---

## ChatGPT Library — USER TRANSFER NEEDED (exact filenames)

Transfer these binaries into `assets/references/ep01/source/` with original filenames + checksums (per `docs/EP01-SOURCE-UNBLOCK.md` transport):

1. `Motel Prayer Scene Storyboard.png` — 2,930,170 bytes — 16-panel EP01 motel/Joe prayer sequence: motel walkway, Mars and Tanesha, Joe's prayer request, Tic Tac exchange, name exchange, departures/reappearance.
2. `Trippedd: The Lost Acid — Pilot Storyboard.png` — 2,211,650 bytes — TRIPPEDD pilot board: live-action search, psychedelic visual shift, animation/3D concepts, return to live action, final defeat.
3. `The Lost Acid: A Gritty Storyboard.png` — 2,102,626 bytes — Time-coded gritty live-action storyboard, lost-acid sequence (earlier/alternate board).
4. `Goodville: Not South Park.png` — size unconfirmed — Goodville cartoon reference.

**Do NOT transfer:** `1000168222.mp4` and `00-reference-contact-sheet.jpg` are NOT the green iris effect (frame inspection showed blue cosmic-head imagery). The green iris remains an effect to locate in existing footage with visual confirmation + timecode.

---

## GENUINE GAPS (honest — searched all branches, docs/, production/, assets/, src/)

1. **Joe 2D visual style** — never written down anywhere. Owner call required before building. (Canon doc itself flags this.)
2. **Clothed and Confused storyboard** — owner says it exists; not found in any repo branch or the Library manifest. May be in the Library under a different filename — needs owner to confirm exact filename.
3. **Naked-and-Afraid watching footage** — not in the 17 transcribed clips (CUT-NOTES confirmed). May exist in owner's Library/footage under a different name.
4. **Shumafied source takes** — design doc exists; original pack/device takes live in the 17 clips (segment 3 base footage) but were not individually inventoried here.

---

## Cross-check vs recovery index

The recovery index (`docs/creative/EP01-MUSE-ASHES-RECOVERY-INDEX.md`) covered: canon sources, Shumafied canon, Joe storyboard (Library), Clothed and Confused canon, Goodville entries, Lost Acid boards (Library + generated), green iris handling. **Material this pull found that the index did not list:** `production/EP01/generated/subjectivity-sequence.md` (full 8-stage design doc), `production/EP01/generated/blender/build_subjectivity.py`, `seed_clothed.cjs` (early 14-layers concept seed), the owner's 2026-10-10 Clothed-and-Confused structure clarification (storyboard + concept + live-footage-of-watching), and the CUT-NOTES confirmation that channel-change/survival footage is absent from the 17 clips.
