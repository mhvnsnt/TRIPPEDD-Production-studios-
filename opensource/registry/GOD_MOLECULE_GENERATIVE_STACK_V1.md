# God Molecule Generative Stack V1

## Goal

Give TRIPPEDD a real repository-level path from showrunner intent + reference photographs to repeatable 2D, 3D, and video assets.

This is not a single AI button. It is a cooperating stack.

## Full upstreams

| System | Job | License / policy | Role |
|---|---|---|---|
| ComfyUI | node-based image/video generation and controlled image editing | GPLv3 code; model-specific terms still apply | primary 2D/generative orchestration |
| TRELLIS.2 | image-to-3D reconstruction and textured asset generation | MIT code/model release; dependencies have separate terms | complete-head geometry lane |
| Meshroom | multi-view photogrammetry / object reconstruction | MPL-2.0 | source-photo geometry lane |
| AliceVision | photogrammetry engine used by Meshroom | MPL-2.0 | reconstruction backend |
| COLMAP | SfM/MVS camera and geometry reconstruction | BSD | alternate geometry backend |
| Wan2.1 | text/image/video generation and editing | Apache 2.0 model repo | video-generation lane |
| Blender | deterministic 3D scene, animation, compositing and render | GPL | canonical repeatable render lane |
| OpenTimelineIO | editorial interchange | Apache 2.0 | timeline/provenance bridge |
| FFmpeg | media encode/mux/QC | LGPL/GPL components depending on build | delivery/technical finishing |

## Identity strategy

For Mars, the default route is:

real photos
→ reference validation
→ Meshroom/COLMAP multi-view reconstruction
→ TRELLIS.2 or reconstructed mesh
→ Blender head/neck asset
→ style/material pass
→ animation
→ FFmpeg/OTIO delivery

ComfyUI and Wan2.1 are optional generative lanes around that deterministic identity anchor.

## Why this is different from the failed episode pipeline

The episode failure showed that simply concatenating source clips is not enough. For God Molecule, the system must understand:

- identity
- geometry
- orientation
- style
- scene continuity
- reusable assets
- animation
- provenance

The reference contract therefore rejects generative drift instead of treating every generated image as equally valid.

## Promotion gates

A new backend is not production merely because it is cloned.

It must pass:

1. install/provisioning check
2. executable smoke
3. real Mars reference input
4. orientation check
5. identity/geometry review
6. output compatibility check
7. provenance capture
8. recovery/resume test

## License rule

Model and checkpoint licenses are tracked separately from repository-code licenses. A backend with territory, research-only, non-commercial, or other restrictions cannot silently become a commercial production dependency.
