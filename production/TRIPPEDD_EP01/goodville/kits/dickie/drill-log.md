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

## Outfit variants — car trio image (2026-10-11)
- **outfit_palm_shirt_torso.png**: Dickie's black palm-tree tiki shirt torso, extracted (u2net) from the owner's car trio image. Clean edges, print intact.

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

## Full Preston Blair sheet (2026-10-11 — owner: "the full fucking Preston Blair sheet")
New: 31 pieces (66 total in kit).

### v2 face furniture architecture
Problem: v1 furniture (eyes_open, mouth_neutral) used skin-backing patches that showed as visible rectangles on the painterly-rendered face.
Fix: **head_blank.png** — extracted head with brow/eye/mouth zones filled via cheek-gradient skin clone (sampled from the character's own cheek column, USE THE IMAGE LAW). All new furniture is TRANSPARENT (no backing) and composites onto head_blank. v1 backing pieces retained for compatibility; v2 supersedes for new work.

### Brows (5, separate set — owner's key-feature directive)
neutral, angry, sad, suspicious, raised. Thick expressive bars in his hair color (87,50,32), matching his brow style.

### Eyes (8 new + worried retained)
open, closed/blink, angry (heavy lid lines), happy (closed arcs), look_L/R/up/down. White ovals (242,240,238) with dark outline, pupils (18,18,18). Geometry measured from extraction: centers (328,352)/(452,352), radii 48x68.

### Mouths (9 new + grin retained)
neutral, smile, frown, smirk (his signature asymmetric), zipper (SP zipper mouth), open, ooh, yell (big cavern), jaw_flap (dropped jaw for the Canadian nod). Mustache+goatee stay on the head; open mouths cover goatee with dark interior.

### Angle heads (4)
- head_34l/head_34r: slice-warp of head_blank (far side 0.86x) + furniture shifted toward near side, seam feathered. Verified no visible join.
- head_profile_L/R: hand-built in flat SP style from his palette (hair mass, single eye/brow, nose bump, ear, mustache/goatee in profile). R = mirror of L.

### Bodies (3)
- body_34l/body_34r: slice-warp of extracted body_full, seam feathered.
- body_back: derived from body_full — face scanline-filled with hair (back of head), print removed per-pixel (deviation from shirt-black baseline), chain removed. Verified no print ghosts.

### Hands (5)
relaxed (matches arm mitten), open, fist, point, grip (C-shape for cans). Skin tone, SP mitten style.

### Verification
Every furniture piece composited on head_blank and eye-checked zoomed. Combos verified: yell, suspicious, happy, sad, zipper, jaw-flap. Angle heads and bodies checked against source likeness. sheet_preview.png contact sheet generated.

## Outfit angles build (2026-10-11 — owner: "make his 2 or 3 outfit references... torso no head but legs too and arms, from all angles")
- **Found 2 outfits** (owner was right): (1) black wolf/flame graphic tee + gold chain, (2) black palm-tree tiki shirt with tiki bar band. No third outfit found in kit — needs owner input.
- **outfit_wolf/**: 40 pieces (8 angles × torso/arm_L/arm_R/leg_L/leg_R). Cut from body_full/body_34l/body_34r/body_back donors via color segmentation (skin vs shirt). Missing angles (profile L/R, 34back L/R) generated via likeness_gen with verbatim prompts, then cut. All verified via reconstruction — no seams.
- **outfit_palm/**: 40 pieces (8 angles × 5). Torsos via pattern transfer (palm front torso mapped onto wolf torso shapes). Arms: palm pattern on sleeves, skin kept. Legs: same pants as wolf (cleaned of graphic bleed). Note: profile angles have minor transfer artifacts; front/34/back are clean.
- Anchors: pieces align to body_full.png coordinate space. Torso neck_y=288, waist_y=631 (front).
