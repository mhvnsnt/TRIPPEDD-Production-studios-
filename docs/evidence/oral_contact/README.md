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
