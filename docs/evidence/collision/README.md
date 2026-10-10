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

---

# HAIR THROUGH HIS FACE — measured, and NOT clean yet

`hair_through_face_AB.png` — collision OFF (top) vs ON (bottom), the same frame of the
same take, with **every vertex the measurement flagged drawn on the pixels** at the size
and colour of its own depth.

| whole take, tolerance 1.0 mm | deepest | violating samples |
|---|---|---|
| collision OFF | **34.507 mm** | 663 / 445,475 |
| collision ON  | **21.881 mm** | 409 / 445,475 |

The collider helps — 37% shallower, 38% fewer — **and it is not a pass.** 21.9 mm of hair
still goes through his cheek. That is recorded as the number, not as "much better".

At the single worst ON frame (6), collision ON is *worse* than OFF: 24 verts / 21.88 mm
against 0 verts / 0.38 mm. The aggregate and the frame disagree, and both are reported.

## Two metrics had to be thrown away first, and both looked fine

1. **B = the whole closed head solid → 59.24 mm, 141,211 violating.** His mesh is 75% hair
   cap by vertex count, so a lock swinging through where the *static* cap used to be
   scored as hair through his face.
2. **B = the face sub-surface, sign from the pseudonormal → 145.38 mm, and collision ON
   scored WORSE than OFF.** That surface is open (348 boundary edges: eyes, nostrils,
   mouth aperture, hairline), so hair hanging down his BACK had its nearest feature on the
   boundary, where the normal points forward. **ON scoring worse than OFF is the giveaway**
   that the number was about the metric.

The test that works needs no hole filling and no repair: **inside the closed head solid
AND the nearest surface feature is a skin triangle.** libigl returns the closest face index
with the distance, so the classification is free. A contact whose nearest feature is on the
hair cap is counted separately as `insideButNearestFeatureOffSubset` — hair against hair,
never reported as a face contact.

## The overlay was wrong once, and it is worth writing down

The first published version of `hair_through_face_AB.png` projected the markers on **world
axes**. His head rests ~32.6° pitched back and the FRONT camera's right vector measures
(-0.995, 0.055, -0.081) — very nearly *minus* world x. So every marker was mirrored
left-for-right and sheared vertically, and it produced a completely plausible-looking
picture in which some markers appeared to float in space beside his head. Those "flying
hair verts" did not exist. The overlay now rebuilds the exact (right, up, forward) triple
from `face_plate.head_frame`, the same one the renderer built its cameras from.

**An overlay you would read as evidence is the worst thing to get quietly wrong.**

## Collider sweep, with the first condition re-tested at the end

| collider thickness | collision substeps | deepest | violating |
|---|---|---|---|
| 2.0 mm | 4 | **21.881 mm** | 409 |
| 0.5 mm | 6 | 24.695 mm | 639 |
| 1.0 mm | 12 | 27.682 mm | 419 |
| 2.0 mm | 16 | 23.496 mm | 418 |
| 2.0 mm | 10 (cloth quality 20) | 72.758 mm | 1461 |
| 3.5 mm | 6 | 79.775 mm | 1608 |
| **2.0 mm — REPEAT of row 1** | **4** | **21.881 mm** | **409** |

The repeat reproduces to the digit, so this is a measurement of the variable and not of
time — the warm-up curve that inverted a ranking once before in this project.

A thicker collider and more substeps make it **worse**, which is the useful finding: the
collider is shoving the hairline at frame 1, because the cap and the skin are the same
surface there. Collision substeps are now their own flag (`--collision-quality`) rather
than being derived from cloth quality — raising `--quality` moved both at once, which is
not an experiment.

## Still open, stated as itself

- `selfCollision` on the hair is **NOT_ATTEMPTED** in these runs (`--no-self-collide`).
- 21.9 mm of face penetration remains. Next: stop the collider pushing at the hairline,
  by excluding pinned root vertices from collision rather than by thickening the collider.

---

# THE CREEP WAS THE CLOTH SAGGING, AND INTERNAL SPRINGS FIXED IT (2026-09-13)

Owner, on the first sequence: *"it doesn't look like the hair moves or has physics at all."*
He was right, and the gate had already refused the run for exactly that reason:

```
drift (linear creep over the take): 56.78 mm
SWAY (peak-to-peak once the creep is removed): 4.20 mm
*** REFUSED: the hair CREEPS 56.78 mm and only SWAYS 4.20 mm.
```

93% of what looked like secondary motion was the cloth slowly stretching under its own
weight. Raising tension stiffness alone does not fix it — it stiffens the *sheet*, and a
dread is a solid form. Blender's cloth ships the thing that models a form: **internal
springs**, which run through the volume between opposing surfaces of a lock.

| | drift | sway | hair through his face |
|---|---|---|---|
| stretch 2000, **no** internal springs | **87.52 mm** | 11.35 mm | — |
| stretch 2000, internal springs | **1.23 mm** | 5.48 mm | — |
| final: stretch 2000, bend 8, air 1.0, internal 12 | **1.14 mm** | **5.96 mm** | **7.25 mm** |

Drift 87.52 → 1.14 mm, a 77x reduction, and **sway now exceeds creep 5-to-1** — the first
time in this project that number has been the right way round.

The face penetration fell with it, 15.15 → **7.25 mm**, without touching the collider: a
lock that holds its own form does not collapse inward through his cheek. That was not
predicted; it was measured.

Also fixed on the way: cutting the collider back from the hair **roots** removed 0 of
11,311 faces, because the root→tip gradient was seeded from the **crown** and its roots sit
on top of his head, nowhere near skin. The shove is where the cap **rests on** the scalp —
those hair vertices start at ~0 mm from the skin, so any collider thickness is an impulse
applied to them on frame 1. Cutting 6 mm around the hair's *rest* positions (93% of the
collider kept) took penetration 21.88 → 15.15 mm before internal springs took it to 7.25.

**Still open and stated as itself:** 7.25 mm of hair still enters his face, `selfCollision`
is NOT_ATTEMPTED, and 5.96 mm of sway may read as too stiff — that is a visual verdict and
it belongs to him, not to the number.

`docs/evidence/hair_motion/hair_FRONT_motion.gif` / `hair_SIDE_motion.gif` are the sequence,
because a frame is not motion.
