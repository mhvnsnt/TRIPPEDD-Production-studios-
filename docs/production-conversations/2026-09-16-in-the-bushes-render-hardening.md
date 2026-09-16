# In the Bushes — Production Conversation / Render Hardening

**Date:** 2026-09-16  
**Show:** In the Bushes  
**Sequence:** EP01 origin opening v4

## User direction

The character images supplied directly in conversation are concept references. Continue the existing production build rather than stopping to redesign the entire pipeline around the sketches.

## Production work completed

- Added a dedicated `teen_performance_v2.py` backend so the active render path no longer depends on the malformed historical teen performance source.
- Updated `build_origin_opening_character.py` to route the shared compositor through the clean backend while retaining the shared builder architecture.
- Updated the render plan and preflight to identify `teen_performance_v2.py` as the active teen character source.
- Fixed the render-source regression test so archive-only references to `teen-group-origin-states.svg` are allowed in documentation but the obsolete sheet cannot appear in active shot assets.
- Fixed malformed procedural teen SVG group closure discovered by GitHub Actions.
- Added a dedicated GitHub Actions render-proof workflow using open-source `librsvg2-bin` and FFmpeg.
- The workflow now validates timing/source integrity, syntax-checks the active backend, performs a preview render, performs the full 37-second render, and uses FFprobe to verify 888 frames at 24fps and 1920x1080 before uploading render proof.
- Corrected scene/render sequence metadata so scene, motion blocks and render plan all identify `EP01-origin-opening-v4-alley-police`.
- Updated the tools README to match the current 37-second v4 pipeline.

## Verification discoveries

GitHub Actions exposed two real defects that were not visible from static inspection:

1. Sequence metadata had drifted between scene/motion/render files.
2. The first clean procedural teen SVG implementation emitted invalid XML because a clothing helper closed the parent group before articulated limbs were appended.

Both defects were corrected and the subsequent validation stage reached PASS for the continuity contract.

## Current gate

A new render-proof run is executing from the latest branch head. The full render is not considered verified until the workflow reaches the FFprobe/QC stage successfully.

## Creative continuity

The supplied Busch sketch remains the visual reference for future Busch refinement: organic irregular green foliage silhouette, expressive face, and red shoes. Mr. Gold remains a separate character reference and is not inserted into EP01 until his story role is established.
