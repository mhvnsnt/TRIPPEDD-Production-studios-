# THE EYE PARTS ARE NOT CALLED WHAT THE RUNBOOK CALLS THEM — read off the live rig

The eye-clearance runbook (`docs/production/EYE_CLEARANCE_RUNBOOK.md`) specifies

```
--part MARS_MESH:LID_L_UPPER --part MARS_MESH:LID_R_UPPER \
--part EYE_L_GLOBE --part EYE_R_GLOBE
```

**None of those four resolve.** Read directly out of the live session holding
`assets/rigs/MARS_FACE.blend`:

```
MESH OBJECTS          MARS_EYE_L 1926 · MARS_EYE_R 1926 · MARS_MESH 27865
                      MARS_MOUTH_SOCK 406 · MARS_TEETH_LOWER 1440
                      MARS_TEETH_UPPER 1440 · MARS_TONGUE 933
MARS_MESH GROUPS      root · neck · head · jaw · tongue_root · tongue_mid ·
                      tongue_tip · eye_L · eye_R · HAIR_WEIGHT · HAIR_PIN
```

So:

| the runbook asks for | what exists | note |
|---|---|---|
| `EYE_L_GLOBE` | **`MARS_EYE_L`** | 1,926 verts, the GNM/ICT globe, re-seated by `place_eyeballs_on_linework.py` |
| `EYE_R_GLOBE` | **`MARS_EYE_R`** | 1,926 verts |
| `MARS_MESH:LID_L_UPPER` | **nothing** | there is no lid vertex group at all |
| `MARS_MESH:LID_R_UPPER` | **nothing** | |

`eye_L` / `eye_R` on `MARS_MESH` are **armature weights for the eye bones**, not a lid
region — using them as a lid class would measure whatever the eye bone drives, which is
not the eyelid.

## The lid is defined by a measured line, not by a group

His lid region is proximity to `docs/evidence/blink_own/painted_lid_lines.json` — the
**painted sclera traced at source resolution**, which is the authority that settled the
eye saga. His drawn "eyelid" lines land on his forehead and brow ridge, 85 mm away
(`docs/evidence/blink_own/ARBITER_linework_vs_painted.png`), so a lid class built from
`linework_3d.json` would be measuring his brow.

**So a lid vertex group has to be DERIVED from those lines before the ladder can run**,
and it must be derived on whichever rig is being measured — the vertex count differs
between rigs and any group is vertex-indexed.

## And the clearance method has to match, or two instruments will contradict each other

Already banked, and it cost a turn: the globe assembly carries a **corneal bulge**, so
its farthest vertex is not its radius — 15.74 mm by centroid-plus-max-distance against
**9.57 mm** from a least-squares sphere fit, with the "centre" 3.90 mm off. `blink_proof`
measured with centroid+max and reported the lid **7.57 mm INSIDE** a globe the placement
solve had just put **0.50 mm CLEAR**. Clearance is measured **against the SURFACE,
direction by direction** (residual p95 ~4 mm — it is not a ball), never against the
fitted sphere.

The giveaway that settled it: the OLD blink key, which travels 0.00 and moves nothing,
reported the same penetration. **A shape that does not move cannot cause a collision**,
so the collision was already in the neutral pose — i.e. in the instrument.
