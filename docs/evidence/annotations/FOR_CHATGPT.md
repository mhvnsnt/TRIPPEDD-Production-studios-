# REFERENCE PIXELS — exact paths, for any agent to search

All on `main` in `mhvnsnt/TRIPPEDD-Production-studios-`. Machine-readable index with
sha256 for every file: **`docs/evidence/annotations/REFERENCE_PIXELS.json`**.

## THE RULE (make it permanent)

**REFERENCE PIXELS ARE IMMUTABLE.** An annotation layer may add points, curves, masks,
labels, IDs, arrows and measurements. It must **not** regenerate, repaint, restyle,
reconstruct, beautify, sharpen, alter or replace any underlying pixel. A visually
similar replacement image is **not** linework evidence — it destroys the spatial
correspondence the whole pipeline depends on. The sha256 is what makes that checkable
rather than promised.

## THE FILES

| path | sha256 (first 16) | what it is |
|---|---|---|
| `docs/evidence/annotations/MARS_hero_starfield.png` | `24cceb8e4d5053fc` | **THE IMMUTABLE PIXEL AUTHORITY.** MARS as he reads — white eyes, dreads, forehead sigil. Annotate ON TOP of this. |
| `docs/evidence/annotations/MARS_annotation_wireframe.png` | `7e495ec421f7239a` | Owner's Tripo overlay on the grey wireframe: `EYE_L_upper_lid` / `_lower_lid` / `_aperture` / `_contour`, `NOSE_nostril_L_*`, `ORAL_*`, `HAIR_ROOT` with `LOCK_0001..LOCK_0025`, and an explicit **NECK EXCLUSION GATE** |
| `docs/evidence/annotations/MARS_annotation_semantic.png` | `64fb0bd08f170c2f` | Owner's Tripo overlay on the textured head: full `HEAD_ANATOMY` hierarchy + **EXCLUSIONS** `neck_region_mask_ID`, `ear_L_mask_ID`, `ear_R_mask_ID` |
| `docs/evidence/annotations/MARS_tripo_source_stats.png` | `d93f21dec5753947` | Source model's own numbers: 1,940,858 faces / 1,000,504 vertices |
| `docs/evidence/blink_own/ARBITER_linework_vs_painted.png` | `c80dd049cf096e69` | **Read this before trusting any eye authority.** Both candidates rendered on his face at once: white dotted = `linework_3d.json` "eyelid" lines, which land on his **forehead/brow ridge**; magenta = painted eyes from his own UVs, which land on his **eyes**. 85 mm apart, same coordinate space. |
| `docs/evidence/blink_own/PAINTED_FLAT_EYES.png` | `bd8186345f730b0c` | The painted lid outline traced at SOURCE resolution, flat-lit with specular unlinked. Red = upper lid, green = lower lid. |
| `assets/references/mars_facial_linework/mars_linework_front_close.png` | `3e6558fa0bc23b17` | Earlier owner-marked plate. **Its lifted 3D lines are the ones on his forehead** — kept, but not the authority. |
| `assets/references/mars_facial_linework/mars_linework_front_full.png` | `93bb563dde9564f5` | Earlier owner-marked plate (full). |
| `docs/evidence/place/MARS_place_plate.png` | `255f6e16ae418da2` | Front ortho plate with `docs/evidence/place/position_map.npz` beside it: `pos[y][x]` IS the 3D surface point at that pixel, so a tap needs no raycast and no depth prior. 71.6% of cells hit the surface. |

## MACHINE-READABLE DERIVED DATA

| path | what |
|---|---|
| `docs/evidence/blink_own/painted_lid_lines.json` | the traced lid outline, 48 bins per lid per eye, in the rig's coordinate space. Apertures **L 6.03 mm / R 4.63 mm**. |
| `docs/evidence/place/position_map.npz` | per-pixel 3D position for the plate above (`pos`, `centre`, `right`, `up`, `fwd`, `scale`, `grid`, `mm`) |
| `docs/evidence/place/place_plate.json` | camera basis + ortho scale + surface-hit fraction for that plate |
| `docs/evidence/hair/_hairzones.npy` | per-vertex `[geodesic_mm, root→tip weight, is_hair]` for the 27,721-vertex cage, **with the neck excluded** |
| `renders/_rig_measure/painted_eyes.json` | the original painted-eye measurement (on the LOD — superseded by the source trace, kept for comparison) |

## TWO THINGS AN AGENT SHOULD NOT REDISCOVER THE HARD WAY

1. **`linework_3d.json` is not the eye authority on this mesh.** Its "eyelid" lines land
   85 mm away, on his forehead. Every blink built on it deforms his brow — which is
   exactly what the owner reported seeing. Use `painted_lid_lines.json`.
2. **The eye-region topology is bad at source.** 324 of 585 triangles under 15° in the
   raw Tripo mesh, minimum angle 0.72°. Subdividing multiplies it. Remesh, don't subdivide.
