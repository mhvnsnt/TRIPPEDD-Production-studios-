# Oral protrusion gate — 2026-09-11

## Production contract

MARS_CANONICAL remains immutable. Oral anatomy is a derived subsystem.

The failed oral render exposed a false success condition: a pink oral object could intersect/protrude through the lips while the aperture survey reported zero teeth/tongue/gum hits. The production gate therefore separates placement evidence from creative anatomy evidence.

## Required order

1. Identify every oral donor by object name, material, and collection.
2. Load the measured mouth-frame plane.
3. Measure each donor's signed front distance to that plane.
4. Recess all donors behind the plane by the configured clearance.
5. Solidify the cavity cutter inward only.
6. Rebuild the cavity from the recessed anatomical sock.
7. Fail closed if any oral donor remains in front of the lip plane.
8. Survey only rays that reach behind the aperture plane.
9. Require non-zero teeth/tongue/gum evidence behind the plane.
10. Produce REST/OPEN/profile/front renders for human review.

## Current gates

- PROTRUSION_GATE: placement only.
- CREATIVE_ORAL_ANATOMY: requires placement PASS plus visible oral-anatomy hits behind the plane.
- HUMAN_REVIEW_REQUIRED: always true for the creative anatomy transition.

No telemetry frame, generated replacement head, or visual guess can turn a failed gate into PASS.

## Current implementation

- tools/character/build_mars_oral_bridge.py
  - measured mouth frame
  - donor recession
  - inward-only cavity solidification
  - fail-closed protrusion check
  - MARS_CANONICAL identity preservation
- tools/character/survey_oral_aperture.py
  - object/material/collection inventory
  - signed placement measurement
  - aperture ray evidence
  - teeth/tongue/gum fractions
  - fail-closed creative-anatomy gate

Next only after this gate: jaw/lip separation, Rhubarb audio timing, expressions, blinking, performance render, then seeded environment and Gaussian-splat fusion.
