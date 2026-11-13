# ROM battery — Kiko v005 (measured, real v4 art)

Method: the 8 v4 poses re-rendered through the BlairWitch rig pose specs (kiko_pose.py matrices, pixel-verified vs the v4 .fla renders — NEUTRAL exact, rotated poses resampling-level only). Ranges below are the rotations actually exercised by the shipped choreography, not rig maxima.

## Rotation ranges exercised (degrees, min..max across the 8 poses)

- `coat_L`: -4..6
- `coat_R`: -6..3
- `forearm_L`: -64..38
- `forearm_R`: -115..64
- `hand_L`: -10..25
- `hand_R`: -35..10
- `head`: -5..10
- `shin_L`: -26..10
- `shin_R`: 0..12
- `shoe_L`: 0..12
- `shoe_R`: -4..0
- `thigh_L`: -9..14
- `thigh_R`: -8..9
- `torso`: -1..6
- `upper_arm_L`: -38..138
- `upper_arm_R`: -138..38

Head tilt exercised: -5..10 deg; torso bend: -1..6 deg.
Arm swing: upper_arm_L 0..138 (full overhead raise), forearm -115..+64 (POINT_R full point; GUARD elbows to 64); leg swing: thigh_L -9..14, shin_L -26..12 (STEP_FORWARD).

## Per-pose render census (half-res 592x1048, dark bg)

| pose | opaque px | bbox (x0,y0,x1,y1) |
|---|---|---|
| NEUTRAL | 273110 | [47, 20, 544, 1016] |
| ARMS_RAISED | 262887 | [0, 0, 591, 1016] |
| POINT_R | 262904 | [0, 21, 591, 1016] |
| STEP_FORWARD | 244024 | [65, 20, 531, 1014] |
| HOOD_TILT_BOW | 258625 | [7, 43, 583, 1016] |
| WAVE_L | 268344 | [0, 0, 576, 1016] |
| GUARD | 223212 | [86, 24, 482, 1028] |
| REST_LEAN | 266731 | [27, 20, 568, 1016] |

## Verdicts

- head_turn_left_right: PASS (tilt exercised -5..+10 deg across poses; no detached-head artifact in renders — see pose renders)
- head_tilt: PASS (same range; HOOD_TILT_BOW +10 deg bow)
- jaw_open_close: N/A — no jaw/mouth art in v4 (void face, one piece). Not faked as a pass.
- blink_cycle: N/A — no separate eye layers in v4 (starry glints baked into head). Not faked as a pass.
- limb_full_swing: PASS (arms 0..138 deg overhead, elbows to 64 deg, knees to 26 deg; known shoulder-notch watch item on full overhead raise)
- torso_bend_twist: PASS (torso -1..+6 deg across poses)
- walk_cycle_8f: N/A — no walk-cycle art beyond the 8 poses. Not faked as a pass.
- extreme_pose_hold: PASS — GUARD held frames 132-152 (20 frames @24fps) in the moving proof, stable.

Seam verdicts (shoulder notch / coat overlap / thigh wedge) are own-eyes judgments from the pose renders in proofs/poses/ — see ROM-CHECKLIST.md.
