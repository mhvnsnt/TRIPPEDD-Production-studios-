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

## Outfit variants — car trio image (2026-10-11)
Source: owner's ChatGPT car trio (1000173536_14_nhu1.png) — Julio HATLESS with black hair, leaning over the car.

### New pieces (all extracted, USE THE IMAGE LAW)
- **head_no_beanie.png**: full hatless head cut (u2net). The beanie-off cut the outfit plan was waiting on.
- **prop_hair.png**: hair-only layer. Made by luminance-keying dark pixels in the top half of the head cut, then keeping ONLY the connected component touching the top edge — this excluded the eyebrows, which the first pass caught. (Lesson: brows sit inside the hair's bounding region; connected-component-from-top-edge is the correct separator. A stale viewer cache made it look like the brows survived — verified clean on white composite + pixel scan: 0 dark px in brow zone.)
- **pose_lean_over.png**: Julio's upper body leaning on the car roof, arms folded. u2net cut of the full region.

### REUSABLE POSE PATTERN: lean-over-a-surface
Owner's note: this "leaning over" pose should become a sheet pose pattern for other characters (leaning over a desk, counter, car). Pattern spec:
- Upper body pitched forward ~15-20°, forearms folded/resting on the surface edge.
- The surface itself is part of the piece (dark mass under the arms here = car roof; recolor/replace per scene).
- To build for another character: extract or pose their upper body the same way, keep the surface as a separate swappable layer.
- Documented here so future sheets (Amos at a counter, old head at a desk) follow the same pattern.

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
- NOTE: folded-arms pose — torso is visible shirt fragments (shirt hidden behind arms/beard); arm_L is small (left arm mostly hidden). Honest to the pose.
