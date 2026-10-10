# THE MOUTH REMESH LANE: FOUR VISUAL FAILURES, ABANDONED. NOTHING PROMOTED.

> *"why don't know why these things have turned into science experiments instead of
> surgical open source one, two, and dones."* — the owner

He is right. Four attempts, four visual failures, and the canonical rig is byte-identical
to the checkpoint taken before any of them. **His character was never touched.** Every
render that looks burned or melted is a quarantined file under `renders/_remesh/`.

## WHAT THE CANONICAL RIG CONTAINS RIGHT NOW

    MARS_MESH           27,865 verts · 89 shape keys · 54,681/54,720 faces smooth
                        custom split normals · UVMap
    MARS_TEETH_UPPER     1,440 verts · visible
    MARS_TEETH_LOWER     1,440 verts · visible
    MARS_TONGUE            933 verts · visible
    MARS_MOUTH_SOCK        406 verts · visible   (recessed 2.28 mm, front wall opened)

and the measured gains from earlier today are all still in it: lip seam cut and split,
teeth **5 → 72 of 240**, oral anatomy **7.58% → 15.24%** of frame, REST identical.

## THE FOUR FAILURES, EACH A DIFFERENT LOST ATTRIBUTE

The remesh GEOMETRY was never shown to be bad. PyMeshLab rebuilt the region correctly and
locally every time — 530 → 6,812 verts there, and all 27,335 vertices outside it exactly
where they were, 0.000000 mm. **Every failure was in carrying attributes onto new topology.**

| # | what was carried | what broke | evidence |
|---|---|---|---|
| 1 | positions, 89 keys, 11 groups | **no smooth flag, no custom normals** — face shattered into facets | `mars/a_b/after_mouth_remesh_VISUAL_FAIL.v001.png` |
| 2 | + smoothing, + custom normals (hand-rolled) | **torn UVs** from my own per-loop transfer | `mars/a_b/after_remesh_with_shading_VISUAL_FAIL.v001.png` |
| 3 | + Blender's native Data Transfer | **mouth SHUT** — my swap removed the object's vertex groups after the transfer wrote weights into them, so the armature drove nothing; and POLYINTERP_NEAREST resampled UVs across the whole head | `mars/a_b/D_native_data_transfer_VISUAL_FAIL.v001.png` |
| 4 | + groups preserved, + exact UVs restored on 53,112 untouched faces | skin destroyed | this file |

Every physical gate was green in all four: rest drift 0.000000 mm, shape-key drift
0.000000 mm, 89 of 89 keys still moving, 0 nearest-surface lookup failures.

**That pattern is the finding.** A scanned head carrying custom split normals, UV seams and
89 shape keys does not survive having its topology replaced under it — each attempt loses a
different attribute, and a gate that only measures geometry cannot see any of it.

## WHAT IS ACTUALLY DOCUMENTED FOR THIS, IN THIS REPO, AND WAS NOT USED

`CLAUDE.md`, *THE FACE PIPELINE WAS RENDERING THE GAME LOD*:

> **THE FIX IS NOT TO RE-RIG AT HIGH RESOLUTION** — it is Blender's own SURFACE_DEFORM:
> the low-res cage keeps the armature, shape keys and every banked measurement; the
> full-resolution mesh is bound to it and renders.

That is the surgical operation for this exact problem and it **cannot damage the canonical
rig**, because the canonical mesh stays the cage and is not modified at all. The four
blockers to that bind, and the fix for each, are already written down in the same section.

## ON GOOGLE GNM

GNM is the **oral donor** and it is in use — `MARS_TEETH_UPPER/LOWER` (1,440 verts each,
teeth + gum materials), `MARS_TONGUE` (933 verts, 31 expressions) and `MARS_MOUTH_SOCK`
(406 verts) in the canonical rig are GNM geometry, from `assets/donor/gnm_oral/`. GNM
supplies oral anatomy; it does not retopologize a scanned head, so it was never the tool
for this particular defect.

## THE FAILED EXPERIMENTS ARE KEPT

All four renders, their sidecars and their sha256 are in `docs/evidence/mars/a_b/` as
regression evidence, per the owner's standing rule on never deleting generated content.
