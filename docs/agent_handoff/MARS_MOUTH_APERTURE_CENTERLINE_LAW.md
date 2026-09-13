# MARS MOUTH APERTURE CENTERLINE LAW

**Status:** ACTIVE REPAIR LAW

The visible mouth opening must be governed by the measured lip aperture and facial midline, not by the extent of the carved cavity alone.

## Current finding

Ray sampling shows direct cavity/teeth hits beyond the closed-lip corners at approximately:

- left: x -28 to -18
- right: x +24 to +28
- closed-lip region: approximately x -15 to +20

Changing the cavity wall did not change the gate. Therefore the remaining side exposure is not established as cavity-wall protrusion. Treat it as a possible genuine aperture/hole until the lip boundary and skin topology are inspected.

## Required next operation

1. Preserve the current canonical checkpoint.
2. Preserve the current review state as a version before any change.
3. Locate the actual upper/lower lip boundary and facial centerline in mesh coordinates.
4. Classify every ray outside the measured lip aperture as one of:
   - lip/skin surface
   - genuine open boundary
   - cavity wall
   - tooth
   - sock
   - unknown
5. Do not move the cavity wall merely to hide an aperture defect.
6. Do not move the camera to hide the defect.
7. If a genuine open boundary exists, repair the boundary/skin topology at the lip corner using the smallest local change possible.
8. Preserve the known-good oral anatomy and shape keys.
9. Render rest and representative mouth poses after the local repair.
10. Require physical and pixel gates before promotion.

## Centerline requirement

Any intentional mouth-gap/tooth-glint opening must be centered on the measured facial midline unless the actual anatomical reference establishes otherwise.

A side slit is a visual FAIL even if the total mouth-opening or anatomy ray-count improves.

## Evidence

Publish BEFORE/AFTER pixels and the ray classification table through the existing visual evidence bus. Failed candidates remain versioned and quarantined.

Do not declare the mouth finished until lip seam, skin stretching, aperture centerline, tooth glint, oral containment, and representative facial deformation all pass together.
