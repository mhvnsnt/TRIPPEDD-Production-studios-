# MC105ORIGINAL_PUPPET_KIKO_VERSION_005

Puppet package for Kiko (body plan: humanoid, 24 fps).
Rig, model sheet, pose slots and the ROM battery live in this folder.
Part library files live in parts/ (hands links SHARED/hands); assigned rig constraints live in constraints/.
Harmony construction profile: the node network, substitution charts and linked .plt palette live in harmony/.
Shadows are never baked into puppet art; they are added in compositing.

## Source of truth — WG105 v4

This package is VERSION 005: the same 16 v4 parts, same pivots, same stack,
same 8-pose choreography as WG105 v4 (WG105_ORIGINAL_PUPPET_KIKO_VERSION_004.fla,
92,856,280 B) — re-expressed through the BlairWitch rig/sheet/puppet system
(Harmony construction, standard tier). It does NOT overwrite v4.

**`kiko_v4_mapping.json` is the real binding.** The BlairWitch `kiko.rig.json`
is a generic humanoid scaffold (pivots null; generic ear/nose/mouth/belt
elements with no v4 art). The mapping file binds scaffold layers to Kiko's
actual v4 part PNGs — real pivots, bboxes, stack order, the 8 pose specs
(rot/dx/dy), proof keyframe timing, and a sha256 per part — so the binding
is verifiable. The 16 part PNGs (43 MB) are NOT duplicated here; they live
at `production/wizard-gang-fla/kiko-v4/parts/<name>.png` (see mapping file
for repo-relative paths + hashes).

## Verification (measured, not claimed)

- **Pose math:** the reimplementation renders all 8 poses vs the v4 .fla
  renders — NEUTRAL pixel-exact (0.00), all others mean|diff| 0.71–1.38
  (resampling-level only). Full table: `verification/verify_8poses.json`.
- **ROM battery:** `ROM-RESULTS.md` — head turn/tilt, limb swing, torso
  bend, extreme hold PASS (measured ranges); jaw/blink/walk-cycle N/A
  (no such art in v4 — not faked as passes). Checklist: `ROM-CHECKLIST.md`.
- **Palette:** sampled from the assembled v4 neutral (`spec.json`).

## Proofs (`proofs/`)

- `kiko_model_sheet_v005.png` — model sheet image (real v4 art).
- `kiko_blairwitch_v005_proof.mp4` — 153 frames @24fps, 444x786, same
  keys/timing/size as the v4 proof (real motion across distinct poses).
- `kiko_side_by_side_v4_vs_blairwitch_v005.mp4` + `kiko_side_by_side_strip.png`
  — v4 FLA proof vs BlairWitch v005 proof, frame-matched.
- `poses/pose_<i>_<NAME>.png` — the 8 v4 poses re-rendered through the rig.
