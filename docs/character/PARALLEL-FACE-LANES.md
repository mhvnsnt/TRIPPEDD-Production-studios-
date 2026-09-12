# MARS Parallel Face Lanes

The face is developed as isolated, measurable lanes so one deformation cannot be mistaken for another.

| Lane | Owner | Authority | Current requirement |
|---|---|---|---|
| Eyes / blink | Core integration | Owner-drawn eyelid linework | OPEN/HALF/CLOSED/HALF/OPEN proof; no cheek blink |
| Nostrils / nose | Delegated worker | Owner-drawn yellow nostril rims | Separate legacy vs new key; left/right independent; depth UNKNOWN without evidence |
| Brows | Pending | Owner-drawn red brow lines | No accidental coupling into blink |
| Mouth / oral | Pending | Existing oral measurements + linework | Preserve geometry/material authority |
| Ears | Pending | Measured source geometry | No invented ear mesh |
| Hair | Pending | Measured source geometry | Geometry first, dynamics second |

## Isolation law

A lane may only claim motion produced by the controls it owns. Pre-existing shape keys are measured separately and cannot be attributed to a new rebuild. Numerical PASS never overrides a visual sequence that shows the wrong tissue moving.

## Depth law

An orthographic owner-drawn plate establishes 2-D observation. It does not establish hidden 3-D depth. When depth is not independently established by committed geometry or measurement evidence, the result is `UNKNOWN`.

## Parallel workflow

Workers may develop separate lanes simultaneously. Integration occurs only after each lane publishes its measurement receipt, exact commands, artifact hashes, and rendered motion proof. This permits eye/blink and nostril work to proceed without contaminating each other's attribution.
