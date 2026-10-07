# SOMBRA NEGRA — Locked Likeness & Attire Inventory (EP02 character reference set)

Reference still rendered 2026-10-07 via Blender 4.0.2 headless
(EEVEE, neutral gray background, front view, full body in frame).
No owner anchor image was supplied for Sombra Negra in this task — likeness notes below
are observed from the GLB only. Do NOT treat them as owner-locked.

## Observed likeness (from `SOMBRA_NEGRA.glb`)
- **Face/head:** white face paint/mask, RED eyes, long black hair worn back.
- **Build:** tall, muscular.
- **Signature features:** skeleton-ribcage vest (white ribs on black), pendant necklace,
  black pants, black boots with straps, black/white wristbands. T-pose in the GLB.

## Attire inventory (GLB -> render)
| GLB file | Render | Status |
|---|---|---|
| `SOMBRA_NEGRA.glb` | `sombra-negra-base-front.png` | RENDERED with exclusions (see defects) |

No `_repaired` variant exists for Sombra Negra.

## Defects / gaps
- **Junk geometry in the GLB:** `Object_42` (a 34x58x23-unit environment piece) and
  `Object_4` (a 6x1.3x5.9 slab) were excluded from framing/render via the render
  script's exclude list — without exclusion the character renders as a speck.
- **Unidentified shard geometry:** dark angular shards fan out behind the thighs/hips.
  Differential renders excluding `Object_40` and `Object_44` did NOT remove them, so they
  are likely part of the leg/pants mesh or a tattered-garment piece. **Needs owner/artist
  call:** intentional shredded-coat design or broken mesh.
- **Orientation note:** this GLB faces -Y in Blender space (camera side `-y`) — every
  other character GLB faces +X. Flagged for the animation/rig pipeline.
- The GLB is a multi-part model (~20 meshes); the still composites them all.
- No alt attire GLB exists for Sombra Negra.
