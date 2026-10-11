# Likeness drill log — Amos Jr.

Tier B (hand-built / extracted production kit) vs Tier A (key art "main ad").

## vs Tier A promo art
- Matches: shaggy brown hair, stoned heavy-lidded eyes, mustache + chin goatee,
  white tank top, right-shoulder tattoo, blue BEER can with red circle — all
  carried by key-art extractions (smart-extract rembg ladder) and parent-verified
  donors. Hand-built pieces use eyedropper-sampled key-art colors only.
- The folded-beer arm IS the key-art pose (extracted, not invented).

## Iterations
- 2026-10-11: eyes_open v1 clipped the lid tops (bbox too tight) → v2 widened
  bbox, lids + pupils intact, accepted.
- 2026-10-11: arm_folded_beer v1 kept a dark backdrop smudge at the shoulder →
  v2 tightened bbox, 1 component, accepted.
- 2026-10-11: hand_fist_can — 3 rembg rounds kept goatee-blur smudges; manual
  alpha cleanup cut a notch in the wrist. Abandoned: derived clean from the
  accepted arm_folded_beer extraction instead. Accepted.
- 2026-10-11: mouth_closed v1 drew a frown arc (wrong PIL angle range) → v2
  quadratic-bezier smug line with tooth strip, accepted.
- 2026-10-11: mouth_open v1/v2 had the teeth as a floating white bar above the
  oval → v3 teeth strip drawn inside the oval, accepted.
- 2026-10-11: arm_punch v1 was a uniform bar (defect per no-rectangle-limbs law);
  v2 boxed fist was also killed. Parent rebuilt: tapered shaft, rounded ends,
  distinct mitten fist + thumb nub gripping the can. Do not overwrite.
- 2026-10-11: prop_beer_can donor carried a dark extraction smudge top-left →
  cleaned in-memory (luminance<115), proving_run original untouched.
- 2026-10-11: torso_mirrored_punch built by parent via mirror-reconstruction
  (right half intact). Seam invisible at natural size.
- 2026-10-11: torso_mirrored_punch REDO (owner correction: first mirror went
  too high — to shoulders/chin, cut the chin, and the polygon arm-removal mask
  left a squared under-arm edge). Rebuilt from body_full: mirror ONLY y>=215
  (mid-chest down); rows 0-214 pixel-identical to original (head/chin/neck/
  shoulders untouched). Rounded under-arm curve, junk components removed
  (1300px). No square cuts per new KIT-SPEC law 8.
- 2026-10-11: torso_no_arm.png NEW (owner directive): torso WITHOUT the side
  arm for punch poses. Mirrored lower + left arm skin replaced with sampled
  tank color, dark specks cleaned, deltoid-tank junction alpha-feathered for
  a rounded shoulder contour. Reads whole on its own; separate punch arm
  poses over it.

## Still off
- Mouth pieces are stylized SP shapes, not pixel traces — close at show scale.
- arm_down: his left arm is half-occluded in the key art (kid character in
  front); proportions estimated from body_full, not directly measured.
- hand_open is generic (no open hand in key art).
