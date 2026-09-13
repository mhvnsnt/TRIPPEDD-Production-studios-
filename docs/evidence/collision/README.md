# COLLISION — measured, not asserted

> *"I think we're gonna need, like, some sort of collision detection or something, so hair
> can't, like, face through the face or, like, you know, so the tongue can't face through the
> cheeks... each piece has collision detection with the other stuff... so that we don't get
> super glitchy buggy animations unless we start asking for that."* — the owner, 2026-09-13

He also said the other half out loud, and it is built in rather than bolted on later:
**glitchy, cartoony and extremely exaggerated stay available — as something we ASK for.**
That is the `STYLE_OVERRIDE` mode below. It requires a written reason, and it stays visible in
the receipt instead of quietly looking like a pass.

## The chain

```
Blender scene ──► export_contact_geometry.py ──► .npz ──► penetration_measure.py ──► receipt ──► contact_gate.py
   (evaluated:     (world-space verts + tris,   (published    (libigl winding number,   (PASS/FAIL,
    armature +      per part, per frame)         bytes)        depth in HIS mm)          exit 45)
    shape keys +
    boolean +
    cloth cache)
```

`contact_gate.py` (written on the other agent's lane) already knew how to JUDGE a contact
receipt. **Nothing produced one.** A contract with no measurement behind it is the exact shape of
every failure in `CLAUDE.md` — a gate with zero checks reports 0/0 PASS. These two stages are the
measurement.

## What "penetration" means here

A vertex of part A that lies **inside the solid volume of part B**, with the depth measured as its
distance to B's nearest surface, in **his own millimetres** (1 mm = MW/50, MW = 0.1930).

## THE METRIC COULD NOT EXPRESS THE FAILURE UNTIL IT CARVED THE CAVITY

First measurement of the tongue at rest:

| | max | violating |
|---|---|---|
| `MARS_TONGUE -> MARS_MESH` | **9.7285 mm** | 113 / 146 |

That is not a tongue defect. Measured on his real rig: `MARS_MESH` evaluates to a **closed** shell
(0 boundary edges, 12 non-manifold edges) whose only boolean is the mouth **aperture** — there is
no cavity subtracted from it. So a tongue resting correctly in its pocket reads 9.73 mm "inside
the head", and a tongue genuinely shoved out through the cheek would have read about the same.
**A metric that returns the same answer for the correct pose and the broken one is not evidence.**
Same family as occlusion scoring a lid that is peeling an eye OPEN as 84% closed.

`MARS_CAVITY` is the air pocket — measured, **146/146 tongue vertices inside it, 16.44 mm deep**.
Carving it out of B leaves the actual meat of his head, which is the only volume the tongue is
forbidden to enter. The difference is taken with **winding numbers, not a mesh boolean**: a point
is in B\C exactly when it is inside B and outside every C. Exact, no remesh per frame, and it
cannot fail the way a boolean on 47k triangles with 12 non-manifold edges can.

## Results, rest pose, tolerance 0.5 mm

| pair | max | violating | verdict |
|---|---|---|---|
| `MARS_TONGUE -> MARS_MESH (minus MARS_CAVITY)` | **0.0000 mm** | 0 / 146 | PASS |
| `MARS_TEETH_UPPER -> MARS_MESH (minus MARS_CAVITY)` | **0.5470 mm** | 2 / 80 | **FAIL** |
| `MARS_TEETH_LOWER -> MARS_MESH (minus MARS_CAVITY)` | 0.0934 mm | 0 / 80 | PASS |

The upper teeth finding is real and small: two crown vertices sit 0.547 mm into his lip, 0.047 mm
past tolerance. It is recorded as a FAIL rather than rounded away.

## PROVEN BOTH DIRECTIONS — the gate is neither vacuous nor hair-trigger

A test that only passes is not evidence. The tongue was deliberately displaced laterally, through
his cheek, and re-measured on the same chain:

| displacement | max penetration | gate |
|---|---|---|
| 0 mm (rest) | 0.0000 mm | PASS, exit 0 |
| **4 mm** | 0.0000 mm | PASS, exit 0 — *real anatomical slack; the cavity is wider than the tongue* |
| **10 mm** | **0.7194 mm** | **FAIL, exit 45** |

The 4 mm row is the important one. A gate that fired there would be a gate that cannot tell slack
from a breach, and it would make every future oral pose a fight.

## Self-collision

`selfCollision` is reported as `NOT_ATTEMPTED` unless `--self PART` is passed, in which case the
part is split into its connected components (for hair, that is lock vs lock) and every component
is measured against all the others. **`NOT_ATTEMPTED` is never written as PASS** — an analyser that
never ran cannot testify that a part is clean.

## Reproduce

```bash
vendor/blender/blender -b assets/rigs/MARS_rigged.blend -P tools/character/export_contact_geometry.py -- \
    --part MARS_TONGUE --part MARS_MESH --part MARS_CAVITY \
    --part MARS_TEETH_UPPER --part MARS_TEETH_LOWER \
    --frames 1-1 --out docs/evidence/collision/oral_rest_geometry.npz

./.trippedd_venv/bin/python tools/character/penetration_measure.py \
    docs/evidence/collision/oral_rest_geometry.npz \
    --carve "MARS_MESH=MARS_CAVITY" \
    --pair "MARS_TONGUE->MARS_MESH:BLOCK" \
    --pair "MARS_TEETH_UPPER->MARS_MESH:BLOCK" \
    --pair "MARS_TEETH_LOWER->MARS_MESH:BLOCK" \
    --tol-mm 0.5 --label oral --out docs/evidence/collision

./.trippedd_venv/bin/python tools/character/contact_gate.py \
    docs/evidence/collision/oral_MARS_TONGUE__MARS_MESH.receipt.json
```

The `.npz` files here are the **published geometry** — any agent, any model, can re-run stage 2
against them and get these numbers without a Blender or a cloth bake. OWNER LAW #2.

## The solver is not mine

libigl's **generalized winding number** (`signed_distance` with
`SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER`) is robust on the open, self-intersecting,
non-watertight surfaces a character actually has — which a ray-parity inside test is not.
FCL (through trimesh) does the broad phase. OWNER LAW #3.
