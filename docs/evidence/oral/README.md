# THE MOUTH IS SEALED. MEASURED, NOT INFERRED.

> *"you regressed the perfect mouth with teeth tongue gums and oral bridges, u reduce it
> to a small hole, it really bad when he opens his mouth it's stretching instead of
> opening."* — the owner

## STATUS (2026-09-13)

1. **Cavity exists** — `oral_cavity.py` voids the head; seam probe 41/41 on cavity wall.
2. **GNM oral is in the rig** — teeth 1,440 verts each, tongue 933/31 keys, mouth sock 406.
3. **Lips did not part** — best teeth visibility was ~9/240 because the seam stayed welded.
4. **Contour-depth carve** — constant-y loft discarded 11.5 mm lip-depth sweep; 44/483 → 4/483 exterior-skin loss on candidate. Width/`--slit-x` retired. Candidate not promoted until mouth_proof + pixels + SHA.
5. **Pale shards = bridges** — after seam cut, faces still span upper→lower **behind** lip front (~14 faces, ~1,008 rays at jaw 30°). Cutting measured worse. **`--drop-bridges` is the operation and was never default-on.**

## Run the shard fix (review-out, not canonical)

```bash
tools/character/run_lip_seam_drop_bridges.sh
# or:
vendor/blender/blender -b assets/rigs/MARS_FACE.blend \
  -P tools/character/split_lip_seam.py -- \
  --drop-bridges --bridge-behind-mm 1.0 \
  --review-out assets/variants/MARS_FACE_SEAM_DROP_BRIDGES_REVIEW.blend
```

Detail: `docs/agent_handoff/LIP_SEAM_DROP_BRIDGES.md`

Promotion still requires: teeth-visible ladder + proof render + reopened pixels + SHA. Canonical untouched by default.

## Historical notes (instrument bugs)

1. "Did the ray hit the head" is not visibility — compare first hit to tooth distance.
2. Tooth positions must be re-read from evaluated depsgraph at every pose.
3. Jaw-weighted cutters can close the hole as the jaw opens — aperture should be static relative to the head shell where appropriate.

MediaPipe mouth contour checked out against skin (~1.2 mm); eyelid landmarks did not. Authority is checked, not assumed.
