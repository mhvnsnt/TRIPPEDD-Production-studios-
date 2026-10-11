# Likeness drill log — crown-hoodie (OWNER'S STAND-IN)

## vs Tier A promo art (key art)
- Matches: black beanie dome silhouette; thick angled black brows (signature);
  chin goatee; dark sideburn wedges; flat-line mouth; black hoodie; white TRIPPEDD
  crown chest logo (outline style); big white oval eyes; pupils looking left;
  peach skin #F2BB7B.
- Off: head_base is flat (key art has soft shading). The beanie is uniformly black —
  key art has subtle ribbed texture the flat fill removes (SP style). Sideburns are
  hand-drawn wedges (the key-art sideburns are thin and partially tucked under the
  beanie; extraction was noise).

## Iterations
- 2026-10-11: beanie extraction (rembg) came back 74px EMPTY (black-on-dark bg).
  Rebuilt from key-art dark key (max<85), largest component. Cleaned brows +
  background intrusion. Good dome.
- 2026-10-11: face extraction was good (solid alpha, correct colors).
- 2026-10-11: torso extraction (rembg) kept ONLY the white logo (black hoodie
  blended with bg). Hand-built black hoodie + extracted logo composited at chest.
  Logo placement verified on overlay.
- 2026-10-11: goatee extraction had logo sliver below — trimmed to top 45%. Clean.
- 2026-10-11: head_base box-fill artifacts → flattened to #F2BB7B, alpha maxed.
- 2026-10-11: hair (sideburn) isolation was noise specks — hand-drew wedges at
  measured positions, color #24211E derived from dark-hair samples.
- 2026-10-11: eyes_scheming boxy lids → redrawn curved.
- 2026-10-11: Overlay test on key art — beanie, eyes, brows, mouth all align
  perfectly. Likeness holds.

## Still off
- Legs/feet below black bar (not visible). Generic dark pants + shoes, color invented,
  marked in manifest. For the owner's stand-in, he may want to specify.
- The hoodie's drawstring/hood details are simplified (key art shows a hood collar;
  kit has a basic collar shape).
- Sideburns are an interpretation (thin in key art, partially occluded by beanie).

## Attempt 3 rebuild (2026-10-11) — owner's stand-in, extra care
- head_base.png had transparency HOLES — rebuilt via color-key from key art (660,590)-(895,810). rembg failed (black beanie dropped).
- Layers: beanie (black), hair_full (brown sideburns), donor eyes_open/pupils/brows_neutral, drawn frown mouth_closed.
- Variants rescaled to anchors (eyes 84,121 / mouth 117,187 / brows 117,70). Angles via feature-shift; profile from 34R + nose.
- torso_34/back added. preview_sheet.png. All verified vs key art.

## Defect repair (2026-10-11) — blank white eyes (no pupils)
- Root cause: pupils.png existed as separate donor but was never composited into
  head angles; also the donor had a cross-eyed error (L pupil right-of-center) +
  edge smudge artifact.
- Fix: drew clean pupils looking LEFT (17px left of eye center, per key art) on
  head_base/34L/34R/profile_R and eyes_open.png. Removed old pupil remnants +
  edge smudge. All heads verified with pupils.

## v2 rebuild (2026-10-11) — MEASURED-ANCHOR LAW, owner's stand-in, extra care
PROVEN METHOD (Sten's v2): donor from key art -> measured anchors -> head_blank + tight furniture -> clean affine angles.

**Defects found in old kit (all fixed):**
- head_base.png had SOLID BLACK eyes (zero white pixels) — key art has big WHITE ovals with pupils. Likeness defect.
- head_34L/34R + head_profile_R had ghosted/doubled outlines + ghost pupils from bad multi-pass warps.
- Old "pupils looking LEFT" fix was WRONG: key art pupils sit ~17px toward the NOSE (inward). Reproduced exactly.

**Measured anchors (donor coords, donor = key-art rect (598,512)-(878,860), 280x348; grid.py --no-crop verified):**
- eye_L (63,155)-(146,244), eye_R (148,155)-(230,244); pupil_L (121,199), pupil_R (172,199)
- brows: tight piece (50,136)-(219,156), pivot (134.5,146)
- mouth frown (brown linework, NOT black): (124,282)-(171,292), center (147,287)
- goatee (114,312)-(174,338) — kept on head_blank
- skin flat tone (242,187,124) = #F2BB7C, median of cheek/chin samples

**Extraction notes:**
- rembg avoided (black beanie); color-key + connected component + hand-verified barrier polyline (dome/brim left edge vs tree + girl's hair) + dome-top parabola trim + jaw-polygon trim.
- Girl's gold hoop earring excluded via gold mask; her black hair excluded via barrier.
- Brown frown needed brown-line mask (dark<85 missed it); fringe holes filled; specks <50px dropped.

**Angles:** single-pass PIL AFFINE, BICUBIC — 34L/34R squeeze 0.85 anchored far edge; profile_R squeeze 0.72 (steep 3/4; true profile needs a side-view donor, none in key art).
**Verify:** head_blank+furniture reconstructs donor (mean abs diff 3.05, 2.4% px >30 — AA fringe only). Every piece viewed zoomed. preview_sheet.png rebuilt with tight composites.
**Still off:** expression variants (eyes_angry etc.) are old-canvas full overlays — need re-anchoring to v2 (follow-up).
