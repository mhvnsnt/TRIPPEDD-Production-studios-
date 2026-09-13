# Canonical Component Preservation Law

## Purpose

Prevent a working MARS component from being destroyed while another face component is being repaired.

## HARD RULE

**A known-good component is an asset, not raw material.** A face repair may not rebuild, replace, regenerate, boolean-cut, remesh, re-skin, or otherwise overwrite a known-good component merely because the current tool wants a simpler whole-face input.

For MARS this is especially strict for the oral system: teeth, gums, tongue, mouth sock/cavity, dental-arch registration, collision relationships, and their working motion are protected production assets.

## One canonical character

`MARS_CANONICAL` remains the identity authority. There is one production oral stack under `tools/character`; no silent parallel oral implementation may become authoritative.

## Required workflow

1. **Identify the canonical target.** Record the exact source `.blend`, object names, and current commit.
2. **Snapshot the known-good component before touching unrelated face work.** The snapshot must include geometry fingerprint, transforms, material slots, shape-key names/count, armature modifiers, vertex-group names, and relevant semantic object names.
3. **Work on a copy/branch.** Never use a repair operation as an implicit destructive upgrade of the protected component.
4. **Modify only the requested component.** If a tool operates on the whole face, its output must be reconciled back onto the canonical face rather than replacing protected components wholesale.
5. **Compare the protected component after the operation.** Any unexplained fingerprint change is a hard stop.
6. **Restore from the donor when a protected component changed unexpectedly.** Do not attempt to recreate it procedurally when a known-good donor exists.
7. **Publish provenance.** Record source SHA, target SHA, component manifest, operation, and validation receipt.

## MARS oral protection

Protected semantic objects/tokens include:

- `MARS_TEETH_UPPER`
- `MARS_TEETH_LOWER`
- `MARS_GUM_UPPER`
- `MARS_GUM_LOWER`
- `MARS_TONGUE`
- `MARS_MOUTH_SOCK`
- `ORAL_CAVITY`
- dental-arch registration / mouth-frame data
- oral collision/rig data and shape keys

A mouth-opening repair must not move the canonical MARS skin as a substitute for opening the oral anatomy. The prior measured failure was skin stretching across the aperture. Internal anatomy motion belongs to the existing GNM-derived oral donor until a measured MARS lip-crease rig is proven.

## Visual authority

Telemetry, ray counts, topology statistics, and manifests are diagnostic evidence. They are not visual PASS. A production mouth claim requires actual rendered pixel evidence. Blender separately controls whether objects participate in final renders and whether they are visible to ray traversal, so both states must be explicitly audited and persisted.

## Regeneration prohibition

A repair script must never silently do any of the following to protected components:

- create a new replacement mouth and discard the donor;
- regenerate teeth/gums/tongue from a generic head;
- apply whole-face remeshing that changes protected oral topology;
- reassign oral materials without recording the change;
- remove oral shape keys or armature weights;
- alter oral collision geometry without a measured receipt;
- overwrite a known-good `.blend` in place.

If the intended operation genuinely requires one of these, it must be an explicit owner-approved migration with a donor snapshot, measured before/after comparison, and rollback source.

## Failure semantics

`UNKNOWN` is never `PASS`.

A missing baseline, missing donor, missing before/after fingerprint, or missing rendered evidence means the operation is **BLOCKED**, not successful.

## Recovery rule

When a previously working component has been overwritten, recover the component from the last known-good donor/snapshot first. Do not redesign it from memory. Images and production-conversation measurements may guide validation, but the existing bytes/donor remain the primary recovery authority when available.
