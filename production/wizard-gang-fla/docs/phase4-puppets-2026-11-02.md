# Phase 4 — FLA puppets for the full Wizard Gang cast (2026-11-02)

Owner's order (verbatim, 2026-11-02):

> Look at all the stuff in our Cape Jones repo that would help us and copy it over to wizard gang and start making foas of the characters and good clean industry standard and production studio grade tools and software 100% wired up and helping u

("foas" = FLAs — the standing 2026-10-30 FLA program order, Wizard Gang first.)

This document is the Phase 4 status record: the generalized puppet builder, the
eight new cast puppets (WG102–WG109; WG101 Ashes landed in PR #293), their
validation results, their motion proofs, and every known gap — logged, not
hidden. Phase 3 (the finished Ashes arrival-scene proof) lands in the same PR:
`proof/WG101ARRIVAL_Sc001_V001.mp4`, `proof/frame_strip.png`,
`proof/poses_sheet.png`, `proof/structure_sheet.png`, `proof/frames/f053–f071`.

## Toolchain (all in `production/wizard-gang-fla/tools/`)

| Stage | Tool |
|---|---|
| Build | `build_puppet.py` + `characters/<char>.json` (generalized from `build_ashes.py`, PR #293; frame-data JSON pattern adopted from the cape-jones FD work) |
| Validate / parse | `validate_puppet.py` wrapping the FLA-programme XFL parser (`parse_xfl.py`) |
| Render / proof | `wg_render.py` (generalized XFL compositor, canvas from character config) + `make_proof.py` (pose stills, motion clip, frame strip, pose sheet, pixel-diff motion numbers) |
| Template gate | `tools/transferred/check_template_gate.py` (transferred from cape-jones, PR #299) |

All art is each character's OWN real extracted layers from
`wizard-gang-part-libraries/<char>/rig-proof/parts/` (full-common-canvas layers,
HSV segmentation + Telea inpainting upstream). Nothing is drawn, generated, or
borrowed from another character. Per-character isolation holds end to end.

## Validation — all 9 puppets parse clean (exit 0, 2026-11-02)

Full JSON dumps: `proof/validation/<PUPPET>.json`. Every document is
1920×1080 @ 24 fps. The `PUPPET` symbol of each WG102–109 puppet carries the
same 8 labelled pose frames: NEUTRAL / BLINK / LEAN_R / LEAN_L / BOW / TURN_R /
ARMS_WIDE / SETTLE.

| Puppet | Media | Symbols | PUPPET symbol | HEADCOMP face states | Notes |
|---|---|---|---|---|---|
| WG101 Ashes | 39 | 18 | 13 frames / 10 layers (NEUTRAL…TRANSITION) | 8 (NEUTRAL…ANGRY) | + EYESCOMP 12 states, MOUTHCOMP 14 grill states — Ashes only |
| WG102 Static | 10 | 12 | 8 frames / 8 layers | 5 (OPEN/BLINK/LOOK_L/LOOK_R/SQUINT) | |
| WG103 Cipher | 10 | 12 | 8 frames / 8 layers | 5 | |
| WG104 Sombra Negra | 8 | 10 | 8 frames / 6 layers | 5 | **no arm symbols — source has no separated arms (gap)** |
| WG105 Kiko | 9 | 11 | 8 frames / 10 layers | **1 (OPEN only)** | **no separated eye layers in source (gap)** |
| WG106 Theory | 10 | 12 | 8 frames / 8 layers | 5 | |
| WG107 Onyx | 12 | 14 | 8 frames / 10 layers | 5 | extras from source: staff + bell parts |
| WG108 Echo | 10 | 12 | 8 frames / 8 layers | 5 | eye_L and eye_R share one source layer (as extracted) |
| WG109 Hollow | 8 | 10 | 8 frames / 6 layers | 5 | **no arm symbols; source is a half-body bust (gap)** |

Face canon holds: no non-Ashes puppet contains a mouth symbol (the other eight
are mouthless void faces by canon); Ashes keeps his diamond grill in every
state (MOUTHCOMP, 14 labelled frames).

## Kiko's 66 MB .fla — investigated, genuine

WG105 is 66,326,317 bytes where the rest of the cast is 4–10 MB. It is **not**
duplicated media. Her source canvas is 1060×1945 (from the owner-approved
`kiko-tanaka-robed.webp`) — roughly 4.3× the pixels of the next-largest cast
canvas — and all 9 of her parts are full-canvas layers at that resolution
(measured content: ROBE_FULL occupies 43% of canvas; arms/chain/drapes
0.6–1.7% each — small parts riding a big canvas). The LIBRARY `.png` +
`bin/*.dat` pairing visible in the zip listing is intrinsic to the .fla format
and present in every puppet. Verdict: genuine hi-res layers; landed as-is.

## Motion proof — what it is, honestly

Per character, in `proof/puppets/<char>/`: the 8 pose stills rendered **from
the .fla itself** (`wg_render.py` draws exactly the transforms the .fla
encodes), a 96-frame clip (12 frames per pose @ 24 fps, hard cuts — production
on-twos style holds), a frame strip of all 8 poses, and a 4-pose sheet.

The poses are real per-part transforms on real pivots: head rotates on the
neck pivot (bottom-centre of the head bbox), torso leans and bows on the
torso/skirt split, eyes translate/scale for LOOK and SQUINT, the crossed
sleeve mass spreads for ARMS_WIDE. This is **not** idle sway, a blink loop, or
a whole-character slide — each of the 8 frames is a distinct encoded pose.

Measured pose-to-pose change (% of pixels changed between consecutive proof
stills, computed from the stills; mean |diff| values are in the lane log,
`agent-ops/cape-jones-to-wizard-gang-2026-11-02.md`). BLINK is an eyelid-only
change and reads near zero, as it should:

| Transition | Static | Cipher | Sombra | Theory | Onyx | Kiko | Echo | Hollow |
|---|---|---|---|---|---|---|---|---|
| NEUTRAL → BLINK | 0.7% | 0.3% | 0.0% | 0.7% | 0.2% | 0.0% | 1.0% | 0.4% |
| BLINK → LEAN_R | 25.4% | 29.2% | 11.6% | 20.1% | 19.7% | 47.6% | 26.5% | 18.4% |
| LEAN_R → LEAN_L | 33.7% | 37.6% | 16.0% | 26.7% | 25.6% | 54.1% | 34.2% | 24.2% |
| LEAN_L → BOW | 38.3% | 40.7% | 13.7% | 30.4% | 29.4% | 52.3% | 36.0% | 21.8% |
| BOW → TURN_R | 33.2% | 36.7% | 10.0% | 25.6% | 24.7% | 45.8% | 32.9% | 18.1% |
| TURN_R → ARMS_WIDE | 41.4% | 45.1% | 16.3% | 31.9% | 31.7% | 55.5% | 40.2% | 23.9% |
| ARMS_WIDE → SETTLE | 39.1% | 41.9% | 14.5% | 30.0% | 29.5% | 53.7% | 37.1% | 20.8% |

Two honest readings from the numbers: **Kiko's BLINK is exactly 0.0%** — she
has no eye layers (gap #3), so her BLINK frame is pixel-identical to NEUTRAL;
the number proves no blink was faked. **Sombra is the subtlest mover in the
cast** (10–16% where the others run 18–55%): no arms, dark-on-dark art, and
his blink is near-invisible at proof scale (his eyes are small white slits in
a dark hood). His poses are real encoded transforms — the silhouette shifts
measurably frame to frame — but they read subtly, and that is stated here
rather than dressed up.

What the sources do **not** contain, and the puppets therefore do not claim:
legs, hips, knees, elbows. Every cast design is robe-to-the-floor with
single-piece crossed arms; poses stay inside the measured arm envelope
(inward/small rotations + drop-and-scale) because the robe chest-centre has
no pixels underneath a wider swing (the same property recorded for Ashes in
`parts.json`).

## Known defects (own-eyes QC of the strips, 2026-11-02)

- **Static** — roughest of the cast: his extracted head layer contains a dark
  rectangular block that reads as a block around the face in several poses;
  neighbour-figure fragments sit at both frame edges (present in his source
  composite check too); chest-band slice offsets appear in BOW / TURN_R where
  the torso/skirt overlap band shifts under rotation.
- **Cipher** — a horizontal seam line crosses the sleeve mass in several
  poses (torso/skirt band edge); a tan bar fragment protrudes at the left
  edge at waist height in every frame (neighbour fragment inside a source
  layer); his chain mass renders noisy — it is a dense chain cluster as
  extracted.
- **Ashes (from Phase 3 QC)** — the inpainted robe fill (dark maroon blocks)
  reveals at the robe edges on wide moves; the scene strip is a slow push-in
  and the poses read subtly at scene scale (crossed-arms source + shot
  design); at figure scale the pose sheet shows the distinct poses.
- Sombra and Hollow ship without arm motion (no separated arms exist). For
  them ARMS_WIDE moves the robe/torso mass only — the label is kept for cast
  consistency and the limitation is stated here, not hidden.

## Gaps logged (not fabricated, not stalled on)

1. Sombra Negra — no separated arm layers in source → no arm symbols.
2. Hollow — half-body bust source, no separated arms → bust puppet, no arm symbols, no lower robe.
3. Kiko — no separated eye layers in her standard variant → HEADCOMP is her
   head-baked face only (no BLINK/LOOK/SQUINT states).
4. Cast-wide — no legs/elbows exist in any source; no symbols claim them.
5. Onyx — source part files carry duplicate arm/bell naming upstream; the
   config resolves to the audited set (staff + bells as extras).

## Template gate — run, result read honestly

`tools/transferred/check_template_gate.py` was run over every
`proof/puppets/<char>/` folder and over `proof/` as a whole before landing.
Its donor-deliverable check passes: there are **no FINAL-named files and no
donor art, voice, or lines anywhere in this landing** (FREE-GAME RULE — tools
and method only). The gate still exits 1 on these folders for its second
check, which hardcodes the cape-jones donor pull's own talking-test file
(`TALKING-TEST-TEMPLATE-AUDIO-20261101.mp4`) and fails any folder that does
not contain it. That check is specific to the donor template folder it was
written for; Wizard Gang proof folders are not donor talking-test templates,
and no file was renamed or fabricated to satisfy it. Recorded here so the
exit code is never misread either way.

## Landing

Branch `cjwg/fla-phase3-4-20261102` off main `5c79a316` (post PR #299).
Contents: Phase 3 scene proof files; the 8 new `.fla` puppets; the Phase 4
tools (`build_puppet.py`, `wg_render.py`, `make_proof.py`,
`validate_puppet.py`, `characters/*.json`); per-character proof packages under
`proof/puppets/`; validation dumps under `proof/validation/`; this document;
a PROGRAM-LOG entry. The `_clipframes/` intermediates (96 PNGs per character)
are not landed — the MP4s are the proof of record.
