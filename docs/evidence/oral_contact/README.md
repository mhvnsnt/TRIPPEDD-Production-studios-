# WHY HIS TEETH LOOK RAGGED — MEASURED IN ONE SESSION, NOT TEN LAUNCHES (2026-09-13)

Every number below came from **one Blender process that stayed open**. The slowest
call was 0.98 s; most were under 0.2 s. The same questions cost ten separate
Blender launches earlier in this session.

## IT IS NOT THE TOOTH GEOMETRY, AND IT IS NOT THE GUMS

| part | verts | tris | non-manifold | degenerate | boundary | face area med / max |
|---|---|---|---|---|---|---|
| `MARS_TEETH_UPPER` | 1,440 | 2,828 | **0** | **0** | 50 | 0.99 / 22.0 mm² |
| `MARS_TEETH_LOWER` | 1,440 | 2,828 | **0** | **0** | 50 | 0.87 / 22.3 mm² |
| `MARS_TONGUE` | 933 | 1,824 | **0** | **0** | 40 | 2.20 / 5.8 mm² |
| `MARS_MOUTH_SOCK` | 406 | 752 | **0** | **0** | 58 | 9.35 / 36.2 mm² |
| `MARS_MESH` | 27,865 | 55,591 | 15 | **0** | 178 | 0.42 / 383.8 mm² |

Clean topology everywhere in the oral assembly. So the ragged white slivers are
not broken crowns.

## WHAT ACTUALLY BLOCKS EACH CROWN

800 crown vertices — the most forward teeth-material vertices of both arches — each
given one ray to the camera. `MARS_TEETH_*` carries **both** the teeth and the gum
material, so "which object did the ray hit" cannot answer this; the material index
of the hit **face** can.

| blocker | share |
|---|---|
| **his own skin** (`tripo_mat…`) | **37%** |
| **the carved cavity wall** (`MARS_ORAL_MAT`) | **23%** |
| *visible* | *17%* |
| lower teeth in front of upper — correct self-occlusion | 14% |
| **`MARS_MOUTH_SOCK`** | **7%** |
| upper teeth self-occlusion | 2% |
| tongue | 1% |
| **`MARS_*_GUM` material** | **1 vertex of 800** |

**His gums block one vertex out of eight hundred.** The crowns read as jagged
slivers because three surfaces sit *in front of them*, and you are seeing the teeth
through the gaps.

## AND THEY ARE MEASURABLY IN FRONT, NOT INFERRED

Depth is measured along his mouth frame's own axis; smaller is nearer the camera.

    upper crowns, front edge (5th pct)      y  +1.34 mm
    MARS_MOUTH_SOCK, front edge (5th pct)   y  +0.06 mm   -> 1.28 mm IN FRONT
    MARS_ORAL_MAT cavity wall (5th pct)     y  -2.18 mm   -> 3.52 mm IN FRONT

A vestibule lining belongs **behind** the crowns and the carved cavity wall is the
**back** of the mouth. Both are in front of his teeth.

## THE SOCK FIX IS MEASURED AND READY; THE CAVITY IS NOT A PLACEMENT PROBLEM

Four candidates A/B'd inside the live session in **0.14 s total**, nothing saved:

    as-is                      133 / 800 crowns visible
    sock pushed back 2.0 mm    147 / 800      <- the whole benefit
    sock pushed back 4.0 mm    147 / 800
    sock pushed back 6.0 mm    148 / 800
    sock hidden entirely       148 / 800      <- the ceiling

2 mm recovers 14 of the 15 crowns the sock costs. But it moves the big number not
at all: **his own head still blocks 479 of 800 either way.** That is the same
finding as the lip seam — 261 faces fill his whole mouth — and it is still
topology, not placement.

## NEXT, AND IN THIS ORDER
1. Recess the sock 2 mm — free, measured, and `build_mars_oral_bridge.py` already
   has `recess_object_behind_plane()` for exactly this (donor-first).
2. The carved cavity wall is 3.52 mm in front of the crowns. Either the carve is
   too shallow or the teeth sit too far forward — measure which against the GNM
   donor before moving anything.
3. Retopology of the mouth region (PyMeshLab, now installed). Cutting has now
   measured neutral-or-worse four separate times.

---

# THE PINK RING WAS THE VESTIBULE LINING'S FRONT WALL (2026-09-13)

> *"there's this pink circular ring that's hanging down in front of the top teeth ...
> it's all fighting each other."* — the owner

He is describing `MARS_MOUTH_SOCK`, and the ray table names it. From z +2 down to z −12
the sock was **the first thing the camera met right across his mouth**, at 0.4–15 mm depth
— in front of his teeth and in front of his tongue. A vestibule lining lines the inside of
his lips and cheeks. **It has no wall across the mouth opening.**

Two measured corrections, both saved to `assets/rigs/MARS_FACE.blend`:

**1. Recessed 2.28 mm, to sit 1.00 mm behind his crowns.** Not a number someone liked —
his crowns' front edge is measured in the same pose and the sock is moved to clear it.

    sock front edge   +0.06 mm  ->  +2.34 mm   (crowns +1.34 mm)
    sock blocking his crowns    53 vertices  ->  3
    sock vertices through HIS SKIN   9 at up to 3.25 mm  ->  0

**2. Opened its front wall — 67 faces.** The criterion is not "forward of the crowns"
(the recess already handled those; only 18 of 195 qualified and the ring was still there).
It is **the wall that hides something**: a sock face the camera meets first with his tongue
or his teeth directly behind it, found by carrying the ray on through and seeing what it
reaches. 67 faces, over 963 rays.

    sock blocking his crowns     3  ->  0
    crowns visible             147  ->  148 of 800
    rays reaching NOTHING        0  ->  0 of 5,307   (no hole through his head)

## THE COLLISION MATRIX, AND THE READING THAT WAS WRONG

Every part against every other, libigl generalized winding number, **0.8 s**. The raw table
says `TEETH_UPPER 14.46 mm inside MESH, 582 verts`, which looks like his teeth are buried
in his skull. **It is not a defect.** igl returns the closest face with the distance, so
each of those 582 vertices can be classified, and **all 582 are nearest the carved cavity
wall** — his teeth are in his mouth, where they belong. Same for his lower teeth (155/155)
and his tongue (133/133). A gate on the raw number fires on correct anatomy.

Containment that is anatomy is now **declared with its reason** rather than silently
dropped: his teeth and tongue sit inside the vestibule lining, so that pair is expected.

What is left, and it is small and real:

    MOUTH_SOCK  through TEETH_UPPER   1.660 mm   60 verts
    TONGUE      through TEETH_LOWER   1.127 mm   42 verts

## STILL WRONG, AND IT IS THE SAME THING AS BEFORE

> *"there's still some lip skin and stuff stretching and tearing towards the teeth and mouth
> from the top and bottom lips"*

Correct. **His own head still blocks 479 of 800 crown rays** — 37% skin, 23% carved cavity
wall — and that number did not move for the sock work, because it never was the sock.
**261 faces fill his entire mouth**, some with edges longer than his lip aperture. Cutting
has now measured neutral-or-worse four times. The next operation is **retopology** of the
mouth region with PyMeshLab, which is installed.
