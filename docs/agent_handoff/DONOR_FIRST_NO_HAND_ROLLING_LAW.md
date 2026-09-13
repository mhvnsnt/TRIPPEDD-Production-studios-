# Donor-First / No-Hand-Rolling Law

**Status: HARD LAW**  
**Scope:** MARS facial, oral, mesh, rig, topology, and component-repair work.

## Law

> **DO NOT HAND-ROLL A REPLACEMENT WHEN A PROVEN DONOR OR EXISTING OPEN-SOURCE TOOL ALREADY SOLVES THE JOB.**

A known-good component, repair script, Blender operator, open-source project, or existing repository artifact is the default implementation. Hand-authored replacement geometry/code is the **last resort**, not the first move.

## Required decision order

Before writing new geometry-generation code, cutter code, placement heuristics, rig logic, or repair logic, Claude MUST:

1. **Search the repository first.** Find existing donors, scripts, runbooks, manifests, evidence, adapters, and previous successful outputs.
2. **Search the open-source stack second.** Check the bulletin and approved/open-source projects already available to the pipeline.
3. **Prefer donor/component transfer.** If a donor already contains the required anatomy, transfer/attach/merge that component into `MARS_CANONICAL`.
4. **Prefer an existing repair chain.** If a script such as an oral-repair runner already exists, use and extend it before inventing a new one.
5. **Use deterministic open-source operations before bespoke geometry.** Existing Blender, libigl/CGAL, MeshLab/PyMeshLab, Open3D, trimesh, Rigify, facial-rig, transfer, and remeshing capabilities outrank hand-coded substitutes when their gates fit the problem.
6. **Only then hand-roll.** New code is permitted only when repository/open-source discovery has failed to produce a viable route or an adapter is genuinely missing.
7. **Record the reason.** A hand-rolled fallback MUST state what was searched, what existing route was rejected, why it was rejected, and what measurable gate the new implementation provides.

## Anti-patterns explicitly forbidden

- Inventing a new mouth cutter while a proven oral donor exists.
- Rebuilding oral anatomy that already exists in a known-good GLB.
- Writing a bespoke Boolean implementation when Blender/libigl/CGAL already provides the operation.
- Replacing a known-good eye/hair/face component because integrating the donor is harder.
- Recreating an existing repository script under a new name instead of using/fixing it.
- Creating another whole MARS model merely because component transfer is inconvenient.
- Treating a successful script execution as proof that the donor/assembly is visually or anatomically correct.

## MARS oral exception handling

For the current oral problem, the preferred route is explicitly:

`MARS_CANONICAL` → locate proven oral donor → run existing oral-repair/assembly chain → measure donor in source space → freeze explicit world-space component data → transfer/attach → reconcile materials/UVs/weights/shape keys → validate oral gates → render proof.

A Boolean cutter is **not** the default solution. If a Boolean is actually required, use an existing closed-volume Boolean route (Blender Exact or libigl/CGAL) and prove its inputs before invoking it. A hand-cut flat-sheet cutter is prohibited as a shortcut.

## Continuous-work requirement

When discovery finds a donor or existing tool, Claude must stop hand-rolling the duplicate and switch to the donor/tool route. If the route fails, fix or adapt the existing route first, then try the next open-source route. Do not burn owner tokens by asking for permission to rediscover the same shelf.

## Evidence requirement

Every donor transfer must leave a receipt containing:
- canonical source path/hash;
- donor source path/hash;
- component name;
- source and target bounds/units;
- placement/registration method;
- material/UV/armature/weight/shape-key mapping status;
- pre/post physical metrics;
- render/evidence hashes;
- rejected routes and reason, if any.

`UNKNOWN` is never PASS. No bytes means no evidence.
