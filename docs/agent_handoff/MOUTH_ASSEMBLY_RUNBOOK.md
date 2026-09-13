# MARS mouth assembly runbook

This runbook exists for Claude and any agent working between owner turns.

## What the current evidence says

The current boolean failure is not mysterious: a linked cutter can lose the intended transform, a flat 1.3 mm plate is not a closed subtractive solid, and the two oral rigs have incompatible source-space anchors. Do not keep retrying the same operation while those facts remain true.

## Fast path

1. Identify `CANONICAL_MARS` first.
2. Identify the GLB/Blend source containing the proven open mouth.
3. In the source file itself, measure the oral parts and cutter in source/world space before linking anything.
4. Convert the proven mouth component to explicit world-space vertex coordinates and freeze that coordinate set. Do not rely on a library object's transform surviving scene linking.
5. Prefer the existing `MARS_MOUTH_SOCK` rim because its 58-edge rim was authored for this head. Measure that rim against the canonical head surface.
6. If a boolean is still required, require a CLOSED, THICK cutter that actually overlaps the head. A flat plate cannot create a subtractive opening.
7. If native Blender Boolean cannot reliably produce the opening, try the independent exact-geometry route through libigl/CGAL. libigl's CGAL boolean path resolves triangle intersections and uses exact arithmetic; it is an independent fallback, not proof that the result is anatomically correct.
8. After every operation, test the actual aperture with rays from the oral interior at jaw angles 0/10/20/30 degrees.
9. Preserve the canonical eyes, brows, hair and existing oral parts. Do not generate another whole MARS to solve the mouth.
10. Publish a render/evidence receipt before promotion.

## Hard stops

- cutter thickness < 0.5 mm
- closed-volume test fails
- intersection volume is zero
- cutter/head overlap is only inferred from object transforms
- no visible aperture after operation
- fewer than 95% of mouth escape rays pass at the tested jaw states
- component transfer damages proven eyes/brows/hair

## Open-source fallback

`libigl` provides CGAL-backed mesh boolean/CSG operations using exact arithmetic and explicit triangle meshes. It can be used when Blender's boolean path is unreliable, but the resulting mesh still requires independent Open3D/MeshLab validation and rendered anatomical proof. See the upstream libigl boolean documentation before implementing an adapter.

## Continue-work instruction

If the current mouth route fails a hard stop, Claude should record the measured reason and immediately move to the next viable route from the bulletin. Do not stop merely because one boolean implementation failed. Do not ask the owner to choose between tools when the decision can be made by the existing gates.
