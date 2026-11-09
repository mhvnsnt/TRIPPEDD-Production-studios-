# WG105 Kiko puppet — VERSION 004 (v3 cuts + floater cleanup + right-shoe restoration)

Built 2026-11-07. Puppet: `~/workspace/fla-build/out/WG105_ORIGINAL_PUPPET_KIKO_VERSION_004.fla`
(92,856,280 bytes at final build). V003 was never overwritten.

## What this pass was

Owner verdict on v3: the outline cuts are way better and the movement stays,
BUT detached paint-drip streaks and splash flecks assigned to leg/coat/arm
parts hang floating in mid-air behind and around the figure in the posed
renders — and part of Kiko's RIGHT shoe is cut off.

This pass changed NOTHING else: no re-cutting. Outline boundaries, pivots,
poses, stacking and timing are byte-for-byte the v2/v3 specs — verified
programmatically after the build (`POSES identical: True`, `PIV identical:
True`, `STACK identical: True`, and every part matrix identical for all
8 poses).

## What was done

**Pass 1 — connected-component audit of all 16 parts** (`cleanup_kiko_v4.py`).
Every disconnected component of every part was classified against the source
art (material classes: fur / ink / gold / skin vs saturated splash colour) and
judged by explicit keep rules: drawn-form masses (coat tails, mantle, fur
trim), the neck chains (the chains are drawn as many separate link
components), tights-pattern islands inside the legs' own outline, arm/hand
segments, joint-overlap strips, and pure-form components with zero splash
pigment. Everything else came off: drips, streaks, droplets, flecks, wisps.
Two structural fixes rode along:

- **Torso → thigh reassignment (6,013 px):** tights-pattern components the
  v3 torso sweep had claimed below the sash were returned to the thighs they
  belong to (thigh_L +3,771, thigh_R +2,242), instead of being deleted and
  leaving holes.
- **Ground splash discipline on the shoes (18,055 px):** both shoe masks
  were cut to hand-fitted polygons on the shoes' drawn lower outlines
  (overlay-verified on the source at full resolution): outsole bottom, toe
  front, heel back. The pools under and beside the soles are gone.

**Pass 2 — pose-verified surgical removals** (`pass2_kiko_v4.py`, 8,381 px).
The first V004 pose renders were checked at full size; the components that
still rendered as floating pieces were removed individually:

- coat_R 5,479 px splash burst + long drip streak beside the right shin
  (solo-verified on a light background: zero garment pixels — pure splash).
- coat_R 1,080 px fringe island (floated beside the hand in STEP_FORWARD).
- coat_R 483 px + coat_L 528 px trim slivers at arm height (the owner's
  "curved flecks floating near the arms").
- coat_L 349 px splash blob under the inner tail (rendered as a droplet
  floating between the legs in STEP_FORWARD), coat_L 250 px drip streak
  under the outer tail tip, coat_L 125 px + 87 px edge slivers.

**Pass 3 — heel wedges + thigh fragments** (`pass3_kiko_v4.py`, 1,693 px).
Splash-burst wedges behind both shoes' heels cut to the drawn back outline
(shoe_L −632, shoe_R −338), and three detached pattern fragments at
thigh_R's outer edge removed (723 px — they rendered as a floating squiggle
beside the leg in STEP_FORWARD; in neutral they hide under the coat tail).

## Right-shoe restoration (owner: "u cut off part of his right shoe")

Pixel-by-pixel comparison of both shoe parts against the source
(`WG_KIKO_REFERENCE_COMPLETED_GEN_20261107.png`):

- **shoe_R was missing its whole toe.** The v3 fitted polygon
  (SHOE_POLY_R, max x 974) clipped the shoe's front half: an 11,666 px
  source component — the complete toe box and front sole — plus dangling
  lace-loop segments beside the collar. Restored from the source by
  erosion/reconstruction (thick toe mass only; the splash streaks fused to
  the same source component were NOT taken): **11,625 px of toe + 232 px of
  lace-loop segments = 11,857 px restored.** A ground-pool component that
  touched the heel corner was explicitly excluded by the restore rules.
- **shoe_L was complete** — the same restore test returned 0 px; nothing
  was missing.
- Verified in the solo shoe renders and in every pose render: both shoes
  are whole, toe to heel, laces and sole lines intact.

## Floater audit (per part)

Components are 8-connected alpha components. "Floaters" = pass-1 component
removals; "pool" = the shoe ground-splash outline discipline; pass 2/3 are
the surgical removals above; "moved" = torso→thigh reassignment;
"restored" = source pixels returned to shoe_R.

| part | comps v3 | comps v4 | px v3 | px v4 | floaters | pool | pass 2 | pass 3 | moved in/out | restored |
|---|---|---|---|---|---|---|---|---|---|---|
| thigh_L | 26 | 9 | 100,644 | 103,776 | 639 | 0 | 0 | 0 | +3,771 in | 0 |
| thigh_R | 96 | 20 | 103,983 | 105,236 | 266 | 0 | 0 | 723 | +2,242 in | 0 |
| shin_L | 7 | 3 | 72,523 | 72,482 | 41 | 0 | 0 | 0 | 0 | 0 |
| shin_R | 18 | 11 | 92,652 | 92,574 | 78 | 0 | 0 | 0 | 0 | 0 |
| shoe_L | 30 | 1 | 63,940 | 55,226 | 216 | 7,866 | 0 | 632 | 0 | 0 (none missing) |
| shoe_R | 34 | 2 | 52,687 | 53,544 | 473 | 10,189 | 0 | 338 | 0 | +11,857 |
| torso | 270 | 98 | 177,917 | 171,091 | 813 | 0 | 0 | 0 | −6,013 out | 0 |
| coat_L | 367 | 37 | 115,168 | 105,960 | 7,869 | 0 | 1,339 | 0 | 0 | 0 |
| coat_R | 275 | 42 | 99,476 | 88,984 | 3,450 | 0 | 7,042 | 0 | 0 | 0 |
| upper_arm_L | 1 | 1 | 32,364 | 32,364 | 0 | 0 | 0 | 0 | 0 | 0 |
| upper_arm_R | 12 | 10 | 35,286 | 35,281 | 5 | 0 | 0 | 0 | 0 | 0 |
| forearm_L | 8 | 8 | 48,581 | 48,581 | 0 | 0 | 0 | 0 | 0 | 0 |
| forearm_R | 13 | 12 | 48,519 | 48,518 | 1 | 0 | 0 | 0 | 0 | 0 |
| hand_L | 2 | 2 | 24,867 | 24,867 | 0 | 0 | 0 | 0 | 0 | 0 |
| hand_R | 3 | 3 | 24,433 | 24,433 | 0 | 0 | 0 | 0 | 0 | 0 |
| head | 12 | 11 | 165,894 | 165,891 | 3 | 0 | 0 | 0 | 0 | 0 |

Totals: 13,854 floater px + 18,055 pool px + 8,381 pass-2 px + 1,693 pass-3
px removed; 6,013 px reassigned torso→thighs; 11,857 px restored to
shoe_R. Full per-component log (1,100+ entries with bounding boxes and
keep/remove reasons) in `work/floater_audit.json`.

Component counts that stay high are by design: the torso's 98 are the drawn
chain links and pendant masses; the coats' 37/42 are the tail panels, mantle
masses and fur trim strands that other parts' claims split apart.

## Verification (own eyes, full size)

- **Neutral gate:** the v4 parts composited in stack order were diffed
  against the v3 assembled neutral (pixel-exact vs source). 31,614 changed
  px, ALL inside the allowed zones: splash areas outside the silhouette,
  the shoe_R toe restoration, and the sole/heel cuts. The KIKO pendant and
  neck chains were checked at 2× zoom — whole (an early pass nicked two fur
  trim strands over the pendant; the pure-form keep rule restored them and
  the re-diff confirmed it).
- **All 8 pose renders from the .fla were read at full size.** The owner's
  three named defects are gone: no drip streak beside the thighs (the
  5,479 px splash streak is removed), no curved flecks near the arms/toro
  (trim slivers removed), no floating droplets between the legs (inner-tail
  blob removed). Both shoes complete in every pose.
- **Solo sheet on a light background** (`proof/parts_sheet_light.png` +
  `proof/solo/<part>.png` for all 16 parts) — floaters would show against
  the light field; the parts read as clean garment/body pieces.
- Pose distinctness vs NEUTRAL (from the .fla renders): ARMS_RAISED 30.5%,
  POINT_R 22.1%, STEP_FORWARD 41.4%, HOOD_TILT_BOW 26.5%, WAVE_L 19.6%,
  GUARD 39.6%, REST_LEAN 21.6% of pixels changed — same choreography as v3
  (slightly lower than v3's numbers because removed splash no longer swings
  through the frame).

## Honest remainders — attached paint that is NOT floating

These are fused into a part's main mass (painted onto the character in the
source art itself), so a component cleanup cannot remove them without
re-cutting inside the v3-approved part boundaries, which this pass was
ordered not to do:

- An orange flame burst fused along shin_R's outer edge — splash painted
  over the leg in the source; it hugs the leg in every pose.
- Blue/purple splash fused under coat_L's outer tail tip, and splash paint
  across the coat tails' lower ends (the source paints splash over the
  tails; v3 disclosed the same).
- One coat tail-tip strand whose end shows as a small droplet between the
  thighs in STEP_FORWARD — it is attached garment (the coat's hanging tail
  tip), visible only because the legs step apart around it.
- A thin paint skin under the shoe soles at the ground-contact line,
  inside the drawn sole outline.
- A ~10 px orange edge fleck at coat_L's inner edge, visible on close
  inspection in ARMS_RAISED / WAVE_L.
- Carried over from v3, unchanged: hands clip the frame edges in
  ARMS_RAISED / WAVE_L / POINT_R (the owner-approved choreography); a full
  overhead raise can open a small crescent notch at the shoulder (the flat
  source has no art behind the arm); the dark wedge between the thighs on
  wide leg poses.

## Files

- `parts/` — 16 cleaned part PNGs (full-canvas, same canvas/pivots as v3)
- `parts.json` — same pivots/stack as v3; bboxes recomputed; shoe notes
  record the restoration
- `cleanup_kiko_v4.py`, `pass2_kiko_v4.py`, `pass3_kiko_v4.py` — the pass
- `build_kiko_v4.py`, `proof_kiko_v4.py` — v3 build chain, V004 names
- `proof/poses/pose_0..7_*.png` — pose renders FROM the .fla
- `proof/kiko_frame_strip.png` — frame strip from those renders
- `proof/kiko_real-motion_proof.mp4` — 153 frames @ 24 fps, same specs as v3
- `proof/parts_sheet_light.png`, `proof/solo/` — light-background solos
- `work/` — audit JSONs, component maps, diff overlays, check crops

Not pushed to GitHub (per brief).
