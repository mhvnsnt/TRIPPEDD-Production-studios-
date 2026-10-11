# Likeness drill log — chet

## vs Tier A promo art
- black rectangular glasses read instantly (frames measured from key art;
  thick rims, bridge, temples) over half-lidded unimpressed eyes
- brown hair cap + small nose bump + flat mouth land the face
- green polo with collar + black undershirt V matches the key-art shirt
- extracted prop_bong.png carries the REAL key-art bong: translucent tube,
  green water, solid grip hand — verified on white, no fringe
- extracted head_keyart.png kept in-kit as the drill target

## Iterations
- pass 1: glasses extraction failed — rembg kept the dark road background
  around the black frames (opaque black corners) -> hand-built the glasses
  from measured frame geometry; the baked glasses in head_keyart.png remain
  the likeness anchor
- pass 1: bong tube looked black on the transparency checker -> verified on
  white: it is translucent pale glass, correct; kept as extracted
- pass 1: hand_grip_bong_L cropped from the bong extraction (measured skin
  bbox); _R is a mirror of _L, documented

## Still off
- hand-built glasses lack the slight lens glare of the key art; flat is
  correct for cutout language
- polo collar is simplified vs key art (two flaps + V); fine at scale
- legs/feet/shoes invented (dark pants, dark shoes): key art crops at the
  waist, so the lower body is SP-convention invention, not likeness

## Identity lock 2026-10-11 — THE BASEMENT NERD
- Classic basement-dweller: computer, video games, D&D, trading cards, anime, WoW (South Park WoW-episode archetype).
- ORIGINAL character — NOT based on a specific South Park character. Name TBD.
- Sheet built around the identity: bong + nerd-signifier props (controller, D20, trading card).

## Attempt 3 rebuild (2026-10-11) — CHET name locked (owner)
- head_base was generic placeholder — rebuilt from key-art rembg cut (1075,590)-(1265,810): brown hair, black glasses (separate layer), donor eyes/pupils/brows, drawn mouth.
- Name updated: glasses-bong-guy -> CHET (basement nerd identity).
- Nerd props built (SP-flat, new): prop_controller.png, prop_d20.png, prop_card.png. Bong prop existing.
- Variants rescaled (eyes 97,126 / mouth 95,177 / brows 95,79). Angles via feature-shift; profile from 34R.
- torso_34/back at content scale. preview_sheet.png. All verified vs key art.

## v2 rebuild — PROPER COMPOSITING (2026-10-11, subagent lane)
Follows sten v2 method exactly (commit 259b8549). Script: kits/chet/build_v2.py (reproducible).

### Measured anchors (donor = rembg u2net cut of head_keyart.png, canvas 281x229)
Programmatic detection + grid.py visual verification (--no-crop, donor-native coords).
- SKIN flat fill: (238,185,126) #EEB97E — forehead (237,185,127), cheek (239,185,125)
- GLASSES zone: x 38-208, y 66-128 (frames + temples; separate layer, transparent lenses)
- LENS L: x 78-117, y 79-116, center (97,97) | LENS R: x 129-167, y 81-118, center (149,99)
- PUPIL L: (107,96) bbox x104-109 y93-99 | PUPIL R: (138,97) bbox x136-141 y94-99
- NOSE (static, baked into blank): x 112-133, y 121-129
- MOUTH (neutral): line x 109-133, y 145-149 + lip shade y154-155
- BROWS: NONE visible in donor — glasses occupy the brow zone (no brows piece)
- Full rig.json-format record: v2/anchors.json (parts: head, glasses, eyes, pupil_L/R, nose, mouth)

### Build
- head_blank: furniture zone flat-filled (feather 2px inside rect); only skin/furniture/white
  replaced — hair (incl. sideburn strand at temple), green collar, nose preserved.
  Glasses NOT baked. Faint frame-edge ghosts where dark edge pixels keyed as hair;
  always covered by v2/glasses.png in real composites (same pattern as sten v2).
- Tight furniture (PIL getbbox, recorded offsets): v2/glasses.png (169x62 @ 38,66),
  v2/eyes_open.png (94x40 @ 76,79, whites+pupils, sits behind glasses),
  v2/mouth_neutral.png (27x13 @ 108,144).
- Partition is disjoint (eyes ring excludes glasses pixels) so compositing is exact.
- VERIFY: composite blank+eyes+glasses+mouth reconstructs donor — untouched px 0 mismatched;
  donor-opaque mismatches: 14 px, all intended flat-vs-shaded skin in the fill zone (delta ~15).
  Zoom-compared vs donor: eyes, mouth, nose pixel-faithful.
- head_34L/head_34R: SINGLE-PASS PIL AFFINE squeeze 0.85, BICUBIC, anchored at far edge
  (34L: right edge; 34R: left edge), fillcolor transparent. Zoom-checked: single lines,
  no ghosting/doubling (old warp-based ones discarded, not reused).
- v2/preview_v2.png proof strip; preview_sheet.png rebuilt with v2 tight composites.
- Old v1 pieces (head_base, glasses.png v1, full-canvas overlays) superseded by v2 — kept in
  kit for now, manifest marks v2 as current.
