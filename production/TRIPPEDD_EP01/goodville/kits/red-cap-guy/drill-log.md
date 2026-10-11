# Likeness drill log — red-cap-guy

## vs Tier A promo art
- backwards red cap reads instantly: brick-red dome (#A32E1E sampled), dark
  back opening with hair tuft, adjustable strap — hat = identity holds
- big close-set white oval eyes match the key-art stare (centers/radii
  measured from the extraction's white blobs, incl. the slight asymmetry)
- orange side tufts + small smile + chin stubble land the face
- white tank + green bottle at chest = the key-art signature pose
- extracted head_keyart.png kept in-kit as the drill target

## Iterations
- pass 1: cap extraction included forehead+eye tops (rembg crop bled below
  the band; shadow under the band fooled the color cut) -> hand-built the cap
  from measured extraction geometry instead; cleaner and SP-flatter
- pass 1: bottle extraction's grip hand ghosted (semi-transparent in rembg) ->
  prop_bottle.png is a measured hand-build (w64 h126, neck, label band);
  hand_grip_bottle_* are skin fists built to wrap it
- pass 1: eye asymmetry kept (L 37x40 / R 30x34) per measurement, not
  symmetrized — matches the key-art read

## Still off
- hand-built cap is flatter than the key-art cap (no fabric shading); acceptable
  in cutout language, could add one shade plane later
- stubble stipple is regular; key art's is finer — needs a second pass at
  higher density
- legs/feet/shoes invented (jeans blue, white sneakers): key art crops at
  the waist, so the lower body is SP-convention invention, not likeness

## Attempt 3 rebuild (2026-10-11)
- head_base was generic placeholder — rebuilt: rembg face cut + color-keyed red cap (170,54,31) + orange hair.
- torso_base was faint outline — rebuilt: white tank via key, mirror-reconstructed occluded center (bottle prop separate).
- prop_bottle_full.png (bottle+hand) extracted clean via rembg.
- Variants rescaled (eyes 89,103 / mouth 89,163 / brows 90,73). Angles via feature-shift; profile from 34R.

## Defect repair (2026-10-11) — blank white torso silhouettes
- Root cause: white tank keyed out as background (white-on-white key too aggressive).
- Fix: re-extracted from key art via luminance key (bright + low-sat, u2net dropped
  the white tank). Kept comps 1+2 (tank body + right strap), excluded text overlay.
  Bottle-occluded center filled with median tank color (232,221,214); bottle remains
  separate prop. Green bottle-bleed cleaned. torso_34 = 0.85x squeeze of base;
  torso_back = mirrored base + raised neckline. All three show the real tank now.

## v2 PROPER COMPOSITING rebuild (2026-10-11, Sten's method)
Donor: head_keyart.png (225x291). Rerunnable builder: v2/build_v2.py.

MEASURED ANCHORS (programmatic, donor px):
- eye_L bbox (47,125)-(104,186), center (75.5,155.5); eye_R bbox (106,125)-(161,186), center (133.5,155.5)
- pupil_L bbox (84,152)-(90,159) c=(87.0,155.5); pupil_R bbox (120,152)-(126,159) c=(123.0,155.5) — pupils sit toward center (close-set stare)
- mouth smile stroke bbox (80,218)-(129,231), center (104.5,224.5) — small 30px smile
- nose stroke bbox ~(85,192)-(134,211) — kept IN head_blank (fixed feature)
- brows: NONE in key art. Thin dark lines at y~77-88 are the cap's back-opening band edge, verified zoomed. brows_neutral = empty 2x2 placeholder at (103,100).
- skin: forehead median (235,183,127); chin median (214,168,114)

Pieces: v2/head_blank.png (inpainted blank), v2/eyes_open.png 121x68 @ (44,122), v2/mouth_neutral.png 33x8 @ (88,220), v2/brows_neutral.png (empty), v2/head_34L.png + v2/head_34R.png (single-pass PIL AFFINE, squeeze 0.85, BICUBIC, far-edge anchor — Sten convention: 34L anchors RIGHT), v2/preview_v2.png, v2/anchors.json.

Defects caught during build (fixed):
1. Pupil detector grabbed a 1px eye-gap artifact as pupil_R -> constrained to blobs 30-200px with centroid inside an eye bbox.
2. Mouth threshold used sum-luminance scale (<380) which selected the whole box as furniture -> corrected to mean-lum <125 (stroke ~60-110, skin ~160+).
3. Eye outline's outer AA ring (tan pixels) escaped the strict masks and showed as pale rings in the blank -> inpaint mask = furniture dilated 2px; crops stay at the tight mask.
4. Deep eye-interior fill fell back to a flat global tone -> fallback now uses the local skin ring median per zone.

VERIFICATION: head_blank + furniture at recorded offsets reconstructs donor with max RGB diff = 0 outside furniture (asserted). Every piece inspected zoomed vs key art: no white halos (crops are exact donor pixels), no doubled/ghosted outlines in 34L/34R, cap/hair/nose/stubble preserved, likeness holds.

preview_sheet.png rebuilt: shows tight composites (blank / +eyes / +full / donor / 34L / 34R / furniture strip).
