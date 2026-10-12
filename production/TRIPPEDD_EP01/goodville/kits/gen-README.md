# gen/ — AI-generated SP-styled piece variants

**Owner directive 2026-10-11:** "use AI to take the little character sheet pieces
and try and get them more to look like South Park... make extra pieces for each
character, but keep all their other pieces from their character sheets saved."

## Rules
- Every kit's `gen/` holds AI-generated variants. **Originals are never touched.**
- Generated via `tools/image-gen/likeness_gen.py` (FLUX Kontext, image-conditioned).
- Instruction: owner's words — "make this little character piece look more like South Park"
- Each piece eye-verified for likeness. Drifted outputs discarded (see below).

## Contents (2026-10-11)
| Kit | gen/ pieces |
|-----|-------------|
| amos-jr | head_sp.png |
| old-head | head_sp.png |
| dickie | head_sp.png |
| bubba | head_sp.png, head_profile_L_sp.png (fills documented angle gap) |
| julio | head_sp.png, fullbody_sp.png (bonus) |
| sten | — (BLOCKED: all head sources damaged) |
| headband-girl | head_sp.png |
| crown-hoodie | head_sp.png |
| red-cap-guy | head_sp.png |
| chet | head_sp.png |

## Discarded for drift
- bubba v1 (lost thick glasses), julio v1 (lost beanie+beard),
  crown-hoodie v1 (generic, lost beanie), sten x3 (source corruption),
  bubba 3/4 (drifted to Dickie-like)
- _universal: sampled — hand-built pieces already SP-optimal, no generative pass needed
