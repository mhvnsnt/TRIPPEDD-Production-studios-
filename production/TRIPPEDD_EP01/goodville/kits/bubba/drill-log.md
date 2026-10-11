# bubba drill log — extraction rebuild (2026-10-11)

Owner rejected the procedural sheets ("why aren't you using the image I just sent you?").
Rebuilt EXTRACTION-FIRST per USE THE IMAGE LAW.

## Extraction
- Full body cut from the source with rembg (u2net; bubba needed isnet-general-use — u2net ate his brown pants as background, and the wider crop fixed the left-arm edge).
- Band-segmented into head / torso / arm_L / arm_R / legs on the crop canvas (full-frame pieces, seamless assembly).
- Props keyed from the image: prop_glasses.
- Face furniture: eyes_open + mouth_neutral extracted; variants (closed/happy/worried, open/grin/frown/ooh) drawn over flat skin sampled from the character's own face.
- Walk (4f), bent/punch arms, sit_legs: transforms of the cut pieces.

## Verification
- Assembly side-by-side vs source: pixel-identical reconstruction.
- Face variants composited and eye-checked (bubba happy+grin verified).
- No square cuts (pieces are full-frame aligned, joins seamless).

## Gap fix 2026-10-11 (owner's defect notes)
**Defect:** black/dark background blob above the viewer-left shoulder (rembg kept junkyard background), plus dark strips on arm piece crop edges.
**Method (surgical alpha cleanup, PIL/numpy):**
1. body_full.png: located blob via visual grid — dark gray-brown (mean RGB ~104,86,87, NOT pure black) at x=[0,100], y=[230,280]. Erased lum<130 pixels — 420 px. Plaid pattern preserved (verified).
2. arm_L.png: dark strip at top edge x=[50,119], y=[315,319] — 224 px erased.
3. arm_L_bent.png: dark strip x=[50,111], y=[305,319] — 294 px erased.
4. torso.png: clean (0 dark pixels in region).
5. Rebuilt preview.png from fixed body_full.png.
**Key lesson:** the blob was NOT pure black (lum 60-120) — a lum<60 filter misses it. Sample the actual defect color first.
**Verification:** zoomed shoulder check — clean edge, plaid intact. Final: clean.
