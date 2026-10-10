# THE OWNER'S OWN ANNOTATION REFERENCES (2026-09-13)

Supplied by the owner from Tripo Studio. These are the **visual specification** for
where every feature is, and they are published here so no agent has to ask for them.

| file | what it is |
|---|---|
| `MARS_annotation_wireframe.png` | the grey wireframe head with every named feature overlaid: `EYE_L_upper_lid` / `_lower_lid` / `_aperture` / `_contour`, `NOSE_nostril_L_*`, `ORAL_*` (vermilion, gap, irises, corneal, gums, glint, boundary), `HAIR_ROOT` with individually numbered `LOCK_0001..LOCK_0025`, and an explicit **NECK EXCLUSION GATE** drawn in orange across the neck |
| `MARS_annotation_semantic.png` | the textured head with the `HEAD_ANATOMY` hierarchy: per-eye `aperture_ID`, `upper_lid_ID`, `lower_lid_ID`, `inner_canthus_ID`, `outer_canthus_ID`, `iris_ID`, `pupil_ID`, `corneal_center_ID`; `BROW_L/R`; `NOSE` alar rims, nostril apertures, columella, tip; `MOUTH` lip boundaries, corners, oral gap, centerline, `teeth_visible_ID`, `tongue_visible_ID`, `tooth_glint_ID`; and **EXCLUSIONS**: `neck_region_mask_ID`, `ear_L_mask_ID`, `ear_R_mask_ID` |
| `MARS_hero_starfield.png` | the character as he is meant to read — white eyes, dreads, forehead sigil |
| `MARS_tripo_source_stats.png` | the source model's own numbers: **1,940,858 faces / 1,000,504 vertices**, topology Triangle |

## What these settle

1. **The eye overlays sit ON his eyes, below the brow arcs.** That independently confirms
   the painted-sclera trace (`painted_lid_lines.json`) and confirms that the "eyelid"
   lines in `linework_3d.json`, which land on his forehead, are the wrong authority.
2. **The neck is an EXCLUSION ZONE, drawn explicitly.** Owner: *"the backside of the neck
   and the bottom side of the neck... it's not a part of the hair."* Implemented in
   `tools/hair/hair_zones.py` as a radial inner-column test, not a height cut.
   Measured: **1,106 verts identified as neck/jaw skin, 173 of which were being simulated
   as HAIR** and are now face.
3. **The ears are exclusion zones too** (`ear_L_mask_ID`, `ear_R_mask_ID`) — he has said
   "skip ears for now", so no ear channel is driven, but they must not enter the hair sim.
4. **The hair is numbered LOCKS with root→tip arrows**, not one sheet. That is the likely
   reason the current cloth reads as "jelly": it is a single connected cloth blob rather
   than individual strands with their own root and direction. NOT yet implemented.
