# TRIPPEDD Open-Source Production Stack

This is the studio-level integration map for proven open-source filmmaking infrastructure. TRIPPEDD remains the production brain and `src/core/pipeline/productionGraph.ts` remains the canonical production graph. External projects are adapters, executors, interchange formats, or reference implementations — never a second competing source of truth.

## 1. Core architecture already adopted

### Showrunner Movie SDK — wholesale architecture

Use the vendored Showrunner SDK under `vendor/showrunner/` for:

- typed artifacts between production agents
- deterministic asset registry references
- pure/repeatable agent boundaries
- Scene IR and extension points
- compiler/type/constraint/evidence discipline
- independently regenerable scenes
- Stage 1 keyframe approval before Stage 2 animation
- continuity verification before expensive work

The God Molecule first-shot contract is the concrete TRIPPEDD implementation of this model.

### Blender — execution truth

Blender is the authoritative scene executor for 3D shots. A shot is not rendered because an agent says it is rendered. The executor must produce physical scene state and actual pixel bytes.

## 2. Production interchange: OpenTimelineIO

[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) is the interchange boundary for editorial timing, shot order, clip ranges, and references to external media.

TRIPPEDD should emit/read OTIO at sequence and episode boundaries, while keeping its typed production graph authoritative for identity, requirements, approvals, provenance, and QC.

Required rule:

> OTIO may describe editorial structure; it cannot certify that media exists or passed QC.

The media reference must resolve to a TRIPPEDD render receipt/evidence artifact before delivery.

## 3. Render execution: OpenCue

[OpenCue](https://github.com/AcademySoftwareFoundation/OpenCue) is the preferred open-source scale-out render manager once the first local Blender render worker is proven. It is designed for VFX/animation job scheduling and supports Blender jobs.

TRIPPEDD integration boundary:

`Shot artifact -> render job spec -> OpenCue -> Blender worker -> render files -> receipt -> QC`

OpenCue is a dispatcher, not a production authority. A successful scheduler job is not a production PASS.

For the first God Molecule shot, keep execution local/direct until the real render worker is reproducible. Then add OpenCue as the same executor behind a queue adapter.

## 4. Production tracking: Kitsu-compatible boundary

Blender Studio's open pipeline uses Kitsu together with Blender and Flamenco. TRIPPEDD already has richer typed production state, so Kitsu should be treated as an interoperability/publishing surface rather than a replacement database.

Future adapter responsibilities:

- publish approved shots/sequences
- expose artist/reviewer status
- publish versions and notes
- map TRIPPEDD work-item IDs to external tracking IDs
- never overwrite TRIPPEDD provenance or evidence

## 5. Editorial/compositing

Use FFmpeg/ffprobe for deterministic media inspection and mechanical assembly tasks. Use OpenTimelineIO for timeline interchange. The final episode should be reproducible from the production graph plus referenced media/evidence.

## 6. Vision and physical QC

QC is intentionally split:

### Physical QC

Read actual scene/render metadata and verify:

- required assets resolve to exact versions
- world/scene IDs match
- meters-per-unit and up-axis match the world contract
- camera exists and is the required camera
- required characters/props exist
- transforms and constraints obey production invariants
- frame range/fps/resolution match the shot contract
- physics constants are within declared bounds
- render output exists and is hashable

### Visual QC

Inspect actual pixels, not manifest claims:

- non-empty/retrievable image sequence
- frame dimensions and decode success
- image statistics / corruption checks
- composition and required subject presence
- identity/face checks for canonical characters
- lighting/material failures that are invisible in metadata
- contact/occlusion/deformation failures
- continuity against approved keyframes or prior shots

A physical PASS never overrides a visual FAIL, and vice versa.

## 7. Evidence contract

Every production PASS must be backed by a receipt containing at minimum:

- shot ID
- scene/world ID
- exact asset registry versions
- source scene hash
- executor and Blender version
- frame range/fps/resolution
- output file paths or object-store references
- SHA-256 hashes of the exact rendered bytes
- reopen/decode verification result
- physical QC result
- visual QC result
- verifier version
- timestamp
- upstream dependency hashes

If any upstream asset version changes, dependent shot evidence is invalidated.

## 8. Agent rule

Agents may propose artifacts and invoke bounded tools. They may not self-certify production completion.

The only trusted completion path is:

`typed artifact -> resolve -> execute -> actual bytes -> reopen exact bytes -> physical QC + visual QC -> evidence receipt -> production graph approval`

## 9. Adoption order

1. Showrunner typed artifacts/registry/Scene IR — adopted.
2. MARS_CANONICAL -> GM-WORLD-0001 -> Blender — first real proof.
3. Pixel retrieval + physical/visual QC — required gate.
4. Evidence receipt and dependency invalidation — required gate.
5. OTIO adapter — sequence/episode interchange.
6. OpenCue adapter — scale-out after local render worker is reproducible.
7. Kitsu-compatible publishing adapter — tracking interoperability.
8. Open-source render/asset infrastructure may be added behind the same contracts when it improves throughput without weakening evidence.

## Non-negotiable boundary

Open-source components are replaceable machinery. TRIPPEDD production truth is not. The production graph, typed artifacts, asset identity, render evidence, and QC gates remain the spine.