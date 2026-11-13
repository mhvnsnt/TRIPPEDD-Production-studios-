# ROM checklist - Kiko v005

No puppet ships until every test passes with reviewed proof frames.
Results measured from the real v4 art — see ROM-RESULTS.md for numbers
(rotation ranges exercised, per-pose census) and proofs/ for the frames.

- [x] head_turn_left_right — PASS. Tilt exercised -5..+10 deg across the 8 poses; no detached-head artifact in any pose render.
- [x] head_tilt — PASS. HOOD_TILT_BOW +10 deg bow; head stays seated on the torso in the render.
- [ ] jaw_open_close — N/A. No jaw/mouth art in v4 (void face, one piece). Logged as N/A, not faked as a pass.
- [ ] blink_cycle — N/A. No separate eye layers in v4 (starry glints baked into the head part). Logged as N/A, not faked as a pass.
- [x] limb_full_swing — PASS. Arms 0..138 deg overhead raise, forearm -115..+64 deg, thigh -9..14, shin -26..12. Known watch item: full overhead raise can open a shoulder notch (flat source, no art behind the arm).
- [x] torso_bend_twist — PASS. Torso -1..+6 deg across poses.
- [ ] walk_cycle_8f — N/A. No walk-cycle art beyond the 8 poses. Logged as N/A, not faked as a pass.
- [x] extreme_pose_hold — PASS. GUARD held frames 132-152 (20 frames @24fps) in the moving proof, stable.
