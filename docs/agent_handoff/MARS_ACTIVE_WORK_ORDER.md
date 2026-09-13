# MARS ACTIVE WORK ORDER

**Status:** ACTIVE OWNER-DIRECTED WORK

Do not treat this as a suggestion list. This is the current production lane.

## A. Protect the current canonical

- Canonical MARS remains recoverable and must not be overwritten by an unpromoted experiment.
- Before every model/rig/mesh/material/texture/scan update, create a new recoverable version.
- Failed and distorted versions remain preserved and named for possible future reuse.

## B. Finish the mouth before moving on

Current working mouth is substantially improved but not finished.

Required targets, in order:

1. Perfect the lip surfaces and lip seam.
2. Eliminate visible skin stretching/columns around the mouth during rest and relevant jaw/lip poses.
3. Correct the mouth-gap / tooth-glint opening so the visible central lip parting is centered on the facial midline, not a side slit.
4. Verify the sock/vestibule never becomes a front wall and does not leak through the lip aperture.
5. Verify teeth, gums, tongue, and cavity remain anatomically contained and visually readable.
6. Test the result at rest plus representative lip/jaw shape keys and animation poses.

Use measured facial midline and measured lip landmarks. Do not solve a centerline defect by arbitrary camera changes or by moving the diagnostic camera.

## C. Visual gate

Every meaningful candidate gets actual published pixels and a sidecar manifest.

Physical gates can pass while the render fails. Visual failure blocks promotion.

Use the established evidence bus:
- `docs/evidence/LATEST_VISUAL_EVIDENCE.json`
- `docs/evidence/VISUAL_EVIDENCE_INDEX.json`
- `docs/evidence/mars/`

## D. Use production-grade transfer operations

Do not hand-roll a transfer when Blender already provides the required production operation.

For UVs, custom normals, smooth flags, seams, and vertex groups, prefer Blender's native Data Transfer facilities and measure the result. Preserve shape keys explicitly and verify them after the transfer.

## E. Versioned promotion

For every candidate:

`canonical -> checkpoint -> candidate version -> physical gates -> published pixels -> visual gates -> promotion decision`

Never skip the candidate version.

A failed candidate remains recoverable.

## F. After mouth acceptance

Do not stop production work. Continue immediately to:

1. hair integration and deformation
2. remaining facial/character-surface defects
3. texture/material quality
4. scan/model quality
5. rig and animation quality
6. shot/episode assembly
7. render/QC

At each stage, preserve the previous accepted version before making the next change.

## G. Open-source work remains active

When a missing capability slows the work, find and integrate a working open-source production tool rather than repeatedly hand-rolling partial implementations. Record provenance/license and make the tool actually usable by the production runtime.

## H. Agent behavior

Follow the owner's explicit work order. Do not silently switch objectives because another task is easier or more interesting.

When the owner says keep working, continue this lane autonomously until a real owner decision is required.
