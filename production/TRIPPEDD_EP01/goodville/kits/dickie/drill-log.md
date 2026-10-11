# dickie drill log — extraction rebuild (2026-10-11)

Owner rejected the procedural sheets ("why aren't you using the image I just sent you?").
Rebuilt EXTRACTION-FIRST per USE THE IMAGE LAW.

## Extraction
- Full body cut from the source with rembg (u2net; bubba needed isnet-general-use — u2net ate his brown pants as background, and the wider crop fixed the left-arm edge).
- Band-segmented into head / torso / arm_L / arm_R / legs on the crop canvas (full-frame pieces, seamless assembly).
- Props keyed from the image: prop_chain.
- Face furniture: eyes_open + mouth_neutral extracted; variants (closed/happy/worried, open/grin/frown/ooh) drawn over flat skin sampled from the character's own face.
- Walk (4f), bent/punch arms, sit_legs: transforms of the cut pieces.

## Verification
- Assembly side-by-side vs source: pixel-identical reconstruction.
- Face variants composited and eye-checked (bubba happy+grin verified).
- No square cuts (pieces are full-frame aligned, joins seamless).

## Gap fix 2026-10-11 (owner's defect notes)
**Defect:** background remnant (junkyard gray-brown) trapped along the outer edge of viewer-right arm, under the sleeve near the flame/wolf design.
**Method (surgical alpha cleanup, PIL/numpy — no generative needed):**
1. Gridded the arm_R piece to map the defect: streak at x=[400,440], y=[440,660].
2. Pass 1: erased mid-luminance low-saturation pixels (lum 50-185, sat<55, not skin) — 954 px.
3. Pass 2: dark reddish-brown strip (lum 30-100, r>=g) — 1593 px.
4. Pass 3: speck cleanup right of arm edge (non-skin) — 628 px.
5. Pass 4: bled-edge — per-row rightmost skin pixel, erased dark non-skin within 5px — 116 px.
6. Found body_full.png had the SAME defect outside arm_R's bbox — erased 2470 bg px directly from body_full.
7. Rebuilt body_full + preview.png by compositing fixed arm_R.
**Verification:** zoomed edge check vs source image — source shows clean skin-to-background edge, no outline. Final: clean.
