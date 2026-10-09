# Production Conversation — 2026-09-11 — God Molecule Mars reference set

## User directive

Use the TRIPPEDD Production Studios repository as the production machine. Preserve the supplied God Molecule/Mars reference images and build repository-level open-source generation capability instead of silently using direct ChatGPT image generation.

## Reference observations

The supplied real photographs establish identity geometry:

- left profile
- right profile
- back of head
- visible neck and hair mass

The supplied Mars renders establish the desired treatment:

- cobalt/blue skin
- violet/indigo shadows
- white eyes
- forehead sigil
- black space background
- sparkling stars
- retro/early-3D degraded visual language

The user specifically rejected a previous failure mode where generated Mars imagery became a face-shaped cutout with missing bottom/back neck geometry. The complete head and neck must remain physically coherent.

## Command distinction

**Direct image generation:** user explicitly asks ChatGPT to generate an image. Use the direct image-generation capability.

**Repository generation:** user explicitly asks to use the repo, production studio, runners, or open-source stack. Use the TRIPPEDD repository generation path. Do not substitute direct image generation.

Repository generation must leave inspectable provenance and QC.

## New repository components

- `production/god-molecule/MARS-REFERENCE-CONTRACT.md`
- `production/god-molecule/mars-reference-manifest.json`
- `scripts/production/god-molecule/prepare-reference-set.py`
- `scripts/production/god-molecule/bootstrap-generative-stack.sh`
- `opensource/registry/GOD_MOLECULE_GENERATIVE_STACK_V1.md`

## Open-source generation stack

The repository bootstrap now includes:

- Meshroom / AliceVision for multi-view reconstruction
- COLMAP as an alternate SfM/MVS backend
- TRELLIS.2 for image-to-3D generation
- ComfyUI for controlled generative image/video workflows
- Wan2.1 for image/video generation and editing
- existing Blender / OpenTimelineIO / FFmpeg production path

Model weights remain external and must be recorded by identifier/checksum; they are not silently treated as repository source.

## Production hierarchy

1. Reference-preserving edit
2. Multi-view reconstruction
3. Deterministic 3D render
4. Controlled generative variation
5. Free generation only when explicitly requested

Identity geometry is protected from silent generative drift.

## Library preservation

The exact supplied references were also saved to the persistent **God Molecule References** library folder, with a contact sheet for review.
