# libigl + CGAL exact boolean route

## Why this is in the stack

MARS currently has a mouth-opening operation where transform provenance and cutter solidity are both suspect. Blender's Boolean modifier supports Exact solving, but this pipeline benefits from an independent geometry implementation when native operations fail.

libigl exposes CGAL-backed `mesh_boolean` and CSG-tree operations over explicit triangle meshes. The implementation resolves self-intersections/mesh arrangements and uses CGAL exact arithmetic. This makes it a useful independent fallback for a closed mouth cutter or structural oral-shell operation.

## Integration rule

Do not feed it guessed transforms. Export the canonical head and cutter as explicit world-space vertices/faces after source-space measurements. Record the source hashes and coordinate-system metadata. Run the boolean. Validate the output independently with Open3D/MeshLab, then render the mouth at multiple jaw angles.

## Promotion gates

- both inputs are explicit triangle meshes
- cutter is closed and has measurable volume
- positive head/cutter overlap exists
- no unexpected self-intersections or non-manifold boundaries after the operation
- aperture exists at the intended lip rim
- oral anatomy remains separately addressable
- eyes, brows and hair are unchanged
- jaw-open rays demonstrate actual escape through the aperture
- output and metrics are committed as evidence

This route is an independent fallback. It does not override the canonical assembly law or visual evidence law.
