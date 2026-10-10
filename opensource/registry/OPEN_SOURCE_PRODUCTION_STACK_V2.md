# TRIPPEDD Open-Source Production Stack V2

Mixed-media, artist-directed production expansion. Upstream projects remain independent; TRIPPEDD connects them through adapters, manifests, artifact lineage, and QC.

## 2D / mixed media
- Proscenio — 2D cutout animation through Blender
- OpenToonz — 2D animation production
- Pencil2D — hand-drawn 2D animation
- Synfig — vector/cutout animation
- Material Maker — procedural materials
- ArmorPaint — PBR texturing

## AI-assisted direction / generation
- ComfyUI — node-based image/video/audio workflows
- ComfyTV — Blender animation to ComfyUI bridge
- AI Movie Studio V2 — 3D storyboard, continuity, shot planning, timeline export
- Sonder Editor — ComfyUI timeline iteration
- 4brospix — manifest-driven AI animation workflow
- InvokeAI — controlled image generation
- Krita — artist-directed paint and AI-assisted retouching

## 3D / VFX / finishing
- Blender
- Natron
- OpenFX
- OpenColorIO
- OpenImageIO / OpenEXR
- OpenVDB
- OpenUSD

## Editorial / review
- OpenTimelineIO
- Kdenlive
- MLT
- OpenRV
- VapourSynth
- FFmpeg

## Production / orchestration
- Kitsu
- AYON
- Flamenco
- OpenCue
- Temporal
- NATS
- PostgreSQL
- MinIO

## TRIPPEDD creative contract
SCRIPT/STORY INTENT -> SHOT MANIFEST -> STORYBOARD -> 2D/3D BLOCKING -> CAMERA/MOTION LOCK -> ASSISTED GENERATION -> HUMAN/PRODUCER REVIEW -> COMPOSITING -> EDIT -> COLOR/AUDIO -> QC -> DELIVERY.

Every generated or assisted shot preserves source references, workflow/model metadata where available, editorial intent, artifact lineage, review state, render settings, and license/provenance metadata. AI is a co-producer/director assistant; it does not silently replace locked human editorial decisions.