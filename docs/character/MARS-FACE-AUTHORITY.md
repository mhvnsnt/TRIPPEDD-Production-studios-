# MARS face authority

<<<<<<< HEAD
Open-source semantic authority:
- MediaPipe Face Landmarker: published eye/eyebrow topology and facial semantics.
- MediaPipe canonical_face_model.obj: fixed 468-index 3-D semantic template.
- Blender Rigify face.skin_eye: independent top/bottom eyelid chains and eye-follow behavior.
- Google GNM Head: scan-derived internal eye/oral anatomy.

Forbidden as blink authority:
- darkness thresholds
- eyebrow-shadow detection
- arbitrary eye-center radial falloff
- first-hit 2-D raycasts at folds
- hand-tuned offsets proven only by one render

The blink must use the semantic upper/lower lid sets, keep brow sets disjoint,
close against a measured lower-lid curve, and refuse if the canonical fit reports
less than 6 mm lid-to-brow separation. Oral anatomy must remain dental-arch centered.

Run: python tools/character/validate_face_authority.py

Structural PASS is not visual PASS; real Blender REST/BLINK/eye-look renders remain required.
=======
The facial pipeline has a hard separation between semantic detection and surface deformation.

## Open-source authorities

1. MediaPipe Face Mesh / Face Landmarker supplies the published 468/478 facial landmark topology and explicit eye/iris/eyebrow connections.
2. MediaPipe canonical_face_model.obj supplies the fixed 468-vertex 3-D semantic template.
3. Blender Rigify face.skin_eye is the rigging reference for independent top/bottom eyelid chains and eye-follow behavior.
4. Google GNM Head supplies scan-derived internal eye/oral anatomy instead of procedural spheres/boxes.

## Prohibited authorities

These are diagnostic only and may never drive the shipped blink:

- darkness thresholds
- eyebrow-shadow detection
- arbitrary radial falloff around the eye center
- first-hit 2-D pixel raycasts at a fold
- hand-tuned offsets whose only proof is a single render

## Blink contract

For each eye:

- upper/lower lid sets are explicit MediaPipe semantic sets;
- brow sets are explicit and disjoint;
- canonical fit must report at least 6 mm lid-to-brow separation;
- closure is defined by upper/lower margins converging on a shared measured curve;
- lid deformation may only affect vertices closer to the semantic lid curve than to the semantic brow curve;
- the eyeball remains independent of skin deformation.

## Oral contract

The GNM oral donor is registered from the dental arch centerline, not the donor lip-band centroid. The visible tooth/cavity seam must remain centered on MARS's measured mouth frame.

## Promotion

Run:

    python tools/character/validate_face_authority.py

PASS from this tool is structural only. Real Blender renders still have to be reviewed from front, mouth close-up and profile views, including REST, BLINK and eye-look poses.
>>>>>>> origin/claude/trippedd-toolchain-provisioning-8pccfc
