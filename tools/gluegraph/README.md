# GlueGraph Destruction Kit (SPEC H-1)

Blender add-on / scripted pipeline for Houdini-style RBD destruction on
Blender's own APIs: fracture an object, hold the pieces together with a
network of **breakable** rigid-body constraints whose strength comes
from distance and material parameters, and let impacts break the bonds
progressively. Built per `docs/BUILD-MAP-FREE-VERSIONS.md` SPEC H-1
(clean-room: workflow studied from public Houdini docs, implementation
is original `bpy`/`bmesh` code).

## Layout

| File | What it is |
|---|---|
| `gluegraph_addon/fracture_core.py` | **Reusable fracture core** — see "Shared with C-2" below. |
| `gluegraph_addon/constraints.py` | Rigid-body setup + breakable constraint network + strength model. |
| `gluegraph_addon/__init__.py` | Add-on registration: panel + operators (build, explode preset, bake to cache). |
| `tests/test_gluegraph.py` | Headless proof test (stand phase vs. impact phase, measured). |
| `tests/test_log.txt` | Recorded output of the proof test on Blender 4.5.3. |

## Donor first: Cell Fracture

Blender's bundled **Cell Fracture** add-on is the fracture donor.
`fracture_core.fracture_object()` calls its operator
(`bpy.ops.object.add_fracture_cell_objects`) whenever it exists in the
running Blender and reports `method == "cell_fracture"`.

On the studio's Blender **4.5.3** build the add-on is not shipped in
`addons_core` (checked: no `object_fracture_cell` module, no fracture
operator), so the fallback runs: a Voronoi fracture on Blender's own
`bmesh.ops.bisect_plane` — seed points in the object's bounds, the mesh
clipped against every other seed's bisector plane, cut faces filled,
pieces shrunk slightly toward their centroids so they don't start in
contact. Same algorithm family as Cell Fracture, original code, and
the test log states which path produced its pieces.

Per-material settings: pass `material_profiles` —
`{material_name_or_"*": {"strength": f, "mass_scale": f, "piece_scale": f}}`.
`strength`/`mass_scale` are honoured by the constraint/mass stage.
`piece_scale` (per-material seed density) is currently honoured only
approximately on the Voronoi fallback path (uniform seeds); on the Cell
Fracture path density is the donor's global `source_limit`.

## Constraint network + impact-triggered release

For every neighbouring pair (centre distance < 0.95 × the sum of
bounding-sphere radii) an empty is created at the midpoint carrying a
`FIXED` rigid-body constraint between the two pieces:

```
strength = glue_strength · material_factor · exp(−falloff · gap) · impact_threshold
```

**Release approach (chosen, and why):** Bullet constraints are natively
breakable — `use_breaking = True` with `breaking_threshold = strength`
makes the solver remove the bond in the step where the impulse through
it exceeds the threshold. This works headless, bakes into the point
cache, and survives file reload with no Python loaded. The alternative
(a `frame_change_pre` handler watching velocities and disabling
constraints by hand) was rejected: handlers don't run reliably during
headless bakes and would make results depend on the add-on being
enabled at reopen time. Scripted (non-physical) release timing is the
only reason to revisit it.

Known measurement caveat: `bpy` exposes no per-constraint "broken"
flag, so the test measures breakage geometrically (bond separation and
piece displacement), not by reading a solver flag.

## Panel (3D Viewport → Sidebar → GlueGraph)

- **Piece Count** — target fracture pieces (2–500).
- **Glue Strength** — base breaking threshold for touching pieces.
- **Strength Falloff** — exponential decay of bond strength with gap.
- **Impact Threshold** — global multiplier on every bond's threshold.
- **Seed** — reproducible fracture.
- **Fracture + Build Glue Network** — fracture selected mesh(es), add
  rigid bodies + bonds, hide the source.
- **Explode Pieces (C-2 preset)** — radial per-piece offset (below).
- **Bake to Cache** — `bpy.ops.ptcache.bake_all`.

## Shared with C-2 (EffectorKit "explode pieces")

`gluegraph_addon/fracture_core.py` is the **single shared fracture
core** for H-1 and EffectorKit SPEC C-2 — build it once, per the build
map's cross-reference. The C-2 lane should import this module
(`fracture_object()` to make pieces, `explode_offsets(pieces, amount)`
for the radial explode vectors) instead of re-implementing fracture.
The add-on's *Explode Pieces* operator is a minimal working consumer of
that helper, included so the preset path is exercised by this lane too.

## Test

```
flock /tmp/heavy-test.lock bash -c \
  'xvfb-run -a env -u PYTHONPATH \
   ~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender \
   -b --factory-startup \
   --python tools/gluegraph/tests/test_gluegraph.py'
```

Small by design: one 12-piece wall, 65 frames. The test prints a
`GLUEGRAPH_RESULT` JSON line (pieces, constraints, stand-phase
displacement, post-impact displacement, separated bonds) and exits 0
only if the structure both stood undisturbed and broke on impact.
Measured numbers from the landing run are in `tests/test_log.txt`:
stand phase (frame 30) max displacement **0.0142 m, 0/12 pieces**
displaced > 0.15 m; after impact (frame 65) **12/12 pieces** displaced
> 0.3 m (max 9.63 m) and **15/47 bonds separated** geometrically — the
remaining bonds held, so pieces left as glued chunks rather than
confetti: progressive failure, as specced.

Two headless findings from the landing runs (Blender 4.5.3, both
measured, both baked into the test harness):

1. **Frame-jumping does not step Bullet headless.** `frame_set(1)` →
   `frame_set(30)` left a free-falling cube at its start height.
   Step sequentially through every frame, or bake the point cache
   (`ptcache.bake_all`, which the Bake to Cache operator wraps).
2. **Releasing a keyframed kinematic body to dynamic does not transfer
   its keyframe velocity** — the released sphere dropped straight down.
   The test's impactor therefore stays kinematic for its whole pass;
   contact impulse on the pieces is still physical.
