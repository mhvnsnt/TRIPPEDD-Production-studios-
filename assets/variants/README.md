# VARIANTS — INCLUDING THE BROKEN ONES. NOTHING IS DELETED.

> *"save this version as a version that we can always get back to ... every time you update
> the model or any of the models save versions of them, we can always get back to — even if
> they're failures, distorted or fucked up versions, because we might use that or name it to
> use it later on as, like, a distorted or fucked up version. This is a real, random,
> multidimensional type of show."* — the owner, 2026-09-13

A failed repair is a **look**. These are kept, named, and recoverable.

| file | what it is | why it might be wanted |
|---|---|---|
| `MARS_FACE_REMESHED_DISTORTED.blend` | mouth region remeshed, shading never carried | his whole face shatters into hard crystalline facets — a genuine glitch/shatter look, with all 89 shape keys intact and animatable |
| `MARS_FACE_REMESHED_D_DISTORTED.blend` | remesh + native Data Transfer, UVs resampled head-wide | skin reads as dense scorched/burned triangulation — the owner's words were "third degree burns" |

Both carry the **full 89-key FACS rig and all 11 vertex groups** and deform normally, so
either can be posed and animated as-is. Neither is canonical and neither ever was.

Canonical checkpoints live in `assets/checkpoints/` and are managed by
`tools/checkpoint.py`, which refuses to overwrite one.

## `MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend` — the re-carved mouth (2026-09-13)

**NOT canonical. A candidate, published so nobody has to ask for it** (OWNER LAW #6).

The carve rebuilt with his contour's own depth instead of flat rings, then the lip
seam split and the sock repairs re-applied. What it measures against the shipped rig:

| | canonical | this candidate |
|---|---|---|
| cells where his exterior corner skin is gone | **44 of 483** (x −31 … +28) | **4 of 483** (x −18 … +17, the centre) |
| best visible teeth after the seam split | 5 → 72 of 240 | **9 → 88 of 240** |
| rest leak | 538 rays (after trimming 271 sock faces) | **101 of 24,321** |
| sock corner trim | needed, 271 faces | **REFUSED — no longer reduces anything** |

Still missing, and why it is not promoted: the densified eye region, the re-seated
eyeballs and `blink_own_L/R` are all built downstream of the rig and have to be
re-applied on top of this, and it has not been through `mouth_proof` or a visual gate.
`tools/checkpoint.py save before-contour-depth-carve` holds the canonical it would
replace.
