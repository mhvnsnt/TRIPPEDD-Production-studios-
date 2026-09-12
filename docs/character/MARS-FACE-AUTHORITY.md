# MARS face authority

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
