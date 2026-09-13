# MARS CORNER SKIN REPAIR PROTOCOL

**Status:** ACTIVE NEXT PASS

This protocol is the single repair lane after the verified 7/8 mouth state. Do not combine it with remeshing, cavity-wall edits, camera edits, or unrelated tool integration.

## Verified diagnosis

At rest, repeated uncontaminated ray windows show the same corner leak pattern:

- left corner crossings: approximately x -28 to -18 mm
- right corner crossings: approximately x +24 to +28 mm
- closed lip surface: approximately x -15 to +20 mm
- repeated corner counts: 919 / 919 / 908 / 911 / 908

The previous `corner 5 / middle 0` reading is invalid because the uncarved scan reference remained visible in the diagnostic scene and occluded the rays. It must never be treated as evidence.

The previous `|x| > 16 mm AND depth > 12 mm` vertex selection is also invalid. It selected 22,998 vertices across most of the head and moved 3,217 vertices by as much as 41 mm. The gate refused the candidate and nothing was saved.

## Physical cause

The rest cross-section establishes that the canonical head's corner skin was carved inward by approximately 38–52 mm:

- x -28: cavity at +38.2
- x -24: cavity at +44.7
- x -18: cavity at +51.8
- x -15: skin at +0.3
- x 0: skin at -4.9
- x +28: cavity at +39.2

Moving the cavity-wall vertices deeper did not change the leak count. The remaining repair is therefore the **caved facial skin**, not the cavity wall.

## Repair target

Pull only the caved commissure skin forward onto the matching uncarved scan surface.

The repair selection MUST be bounded by distance to measured lip landmarks / lip-line geometry and by local facial-region connectivity. Never select mouth corners using a global lateral coordinate plus depth threshold.

The uncarved scan is a **temporary geometric reference only**. Remove or hide it from every diagnostic/render gate before measuring or publishing evidence. A reference object must never be allowed to occlude a truth ray.

## Safe transfer strategy

1. Preserve the verified canonical checkpoint `mouth-7of8-corners-trimmed`.
2. Create a fresh candidate version before changing geometry.
3. Load the uncarved scan only as a temporary source/reference.
4. Build a small, explicitly bounded commissure vertex group from measured lip-line distance and local connectivity.
5. Reject the candidate if the selection escapes the local commissure region.
6. Transfer the corner skin toward the uncarved scan using a controlled projection/shrinkwrap operation with a strict distance limit.
7. Do not alter oral anatomy, teeth, gums, tongue, cavity wall, sock, shape-key topology, or camera.
8. Remove/hide the reference object before running `mouth_proof.py`.
9. Run the existing gate BEFORE any additional repair work.
10. Publish rest pixels and the ray classification/evidence sidecar.
11. Only promote if the physical gates and pixels both pass.

Blender's Shrinkwrap supports a target, vertex-group influence, projection direction, and a projection distance limit; those controls are appropriate for constraining this local transfer rather than moving an unconstrained head region. citeturn0search0turn1search3

## Hard rejection conditions

Reject and save nothing as canonical if any candidate:

- changes vertices outside the measured commissure selection;
- changes oral anatomy or shape-key structure unexpectedly;
- changes the center lip closure;
- creates a new side slit;
- improves the ray metric only because the reference object remains visible;
- changes the camera to conceal the defect;
- skips the existing 7/8 baseline gate;
- lacks BEFORE/AFTER pixels and a candidate manifest.

## Promotion gate

The intended result is simple: the existing center lip closure remains intact, while the caved corner skin returns to the character's own uncarved surface so cavity/teeth/sock are no longer directly visible outside the commissures.

A better aggregate ray percentage is insufficient. The visual result must show closed corners, centered intentional tooth glint, no side slit, and preserved oral anatomy.
