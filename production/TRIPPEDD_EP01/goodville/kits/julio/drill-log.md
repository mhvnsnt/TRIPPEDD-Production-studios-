# julio drill log — extraction rebuild (2026-10-11)

Owner rejected the procedural sheets ("why aren't you using the image I just sent you?").
Rebuilt EXTRACTION-FIRST per USE THE IMAGE LAW.

## Extraction
- Full body cut from the source with rembg (u2net; bubba needed isnet-general-use — u2net ate his brown pants as background, and the wider crop fixed the left-arm edge).
- Band-segmented into head / torso / arm_L / arm_R / legs on the crop canvas (full-frame pieces, seamless assembly).
- Props keyed from the image: prop_beanie, prop_tumbler.
- Face furniture: eyes_open + mouth_neutral extracted; variants (closed/happy/worried, open/grin/frown/ooh) drawn over flat skin sampled from the character's own face.
- Walk (4f), bent/punch arms, sit_legs: transforms of the cut pieces.

## Verification
- Assembly side-by-side vs source: pixel-identical reconstruction.
- Face variants composited and eye-checked (bubba happy+grin verified).
- No square cuts (pieces are full-frame aligned, joins seamless).

## Gap fix 2026-10-11 (owner's defect notes)
**Defect:** junkyard background showing through on cup-holding arm (viewer-right) below the elbow, between arm and shirt/jeans pocket.
**Method (surgical alpha cleanup, PIL/numpy):**
1. arm_R piece: erased gray junkyard pixels (lum 50-185, sat<55, not skin, not black shirt) at x=[395,445], y=[540,640] — 2260 px.
2. Found body_full.png had a LARGER patch of the same junkyard (4874 px) at x=[370,445], y=[525,675] — erased directly (lum 50-210, not skin, not black).
3. Rebuilt body_full + preview.png.
**Verification:** zoomed check — arm, shirt, jeans edges clean, no background remnants. Final: clean.
