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

## Outfit variants — car trio image (2026-10-11)
- **outfit_blue_work_shirt_torso.png**: Bubba's solid blue work shirt torso (chest pockets, buttons), extracted from the owner's car trio image. NOTE: isnet-general-use kept a black car-interior wedge at bottom-right; u2net's cut was cleaner (no wedge, hand intact) — used the u2net version. Model choice matters per-piece; test both.

## v2 cleanup pass (2026-10-11 — owner: "a lil messy, keep em but make better ones")

v1 flaws found (eyes on, zoomed):
- pose_lean_over: car mass was a lumpy black blob; light rim/halo where arms met the black.
- outfit torsos (both): hard straight bottom cuts (square-cut violation).
- bubba torso: black fringe remnants on left edge.
- head_no_beanie: minor hair-edge roughness.

v2 fixes (all cuts from /home/hatch/workspace/user/files/1000173536_14_nhu1.png):
- rembg model per piece: u2net won for Julio head (isnet left dark RGB contamination on the face) and Bubba (no car wedge); isnet-general-use won for Dickie and Julio lean (detail); u2net_human_seg FAILED on Julio (blacked out the face) — do not use for dark-shaded faces.
- pose_lean_over_v2: removed car window/door/mirror + Bubba's shirt chunk; kept clean car-roof band as the lean surface with a shaped bottom edge.
- Both torsos: curved hems via sinusoidal alpha mask (no square cuts).
- Edge treatment everywhere: 3px MinFilter erode + 0.7-0.8px Gaussian feather (kills halo/fringe).
- Side-fringe killer: near-white pixel removal in edge zones.
- v1 files untouched alongside v2 per owner.

## Full-piece set (2026-10-11, car trio image)
- 5 pieces: upper_with_face, head_sep, torso_sep, arm_L_sep, arm_R_sep
- Method: u2net wide extraction (isnet left intrusions / blacked faces). Slab separation with 30px feathered overlaps; pieces composite seamlessly (verified by reassembly).
- Neck lines: below chin/goatee/beard. No face parts in torso pieces.

## 2026-10-11 — Full Preston Blair sheet v1 (subagent)
Expression set: 5 brows (neutral/angry/sad/suspicious/raised, his softer style),
6 new eyes (angry, look L/R/up/down, open_standalone for under-glasses),
4 new mouths (smile, grin_big w/ teeth, yell_cavern, zipper). All hand-built
on 415x805 registered canvas, verified composited.
mouth_neutral rebuilt clean (original had shirt fragment caught in extraction).
head_nobrows: 3 attempts (brows sit at y~195-225, higher than first estimated).
Hands x5 (open/fist/point/grip/relaxed), SP mitten style, his skin tone.
torso_back: derived via adjacent plaid cloning, 7 buttons removed (count them,
not 5), pocket flaps softened.
PENDING: 3/4 L/R + profile heads. 5 attempts failed likeness gate: gen.py
img2img drifted (double glasses frames, 4 pupils), ai_edit kept likeness but
refused the turn, mesh/affine warps seamed, hand-drawn profiles bowl-cut
drifted. Per LIKENESS LAW nothing ships until it looks like HIM. Path:
owner's ChatGPT angle turn, or self-hosted Qwen/Kontext.
sheet_preview.png: model sheet v1 (2400x3000).
