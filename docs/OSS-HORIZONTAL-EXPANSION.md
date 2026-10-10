# TRIPPEDD OSS Horizontal Expansion

TRIPPEDD continuously expands production capability horizontally across the Studio Capability Map while deepening the active vertical slices. Open source is a capability source, not an end in itself.

## Operating rule

A tool enters the canonical stack only after evidence. The progression is:

`DISCOVERED → RESEARCHED → CANDIDATE → INTEGRATED → SMOKE_TESTED → VALIDATED → PRODUCTION`

Failures are explicit:

`UNKNOWN → QUARANTINED → DEPRECATED → REJECTED`

## Domains covered

- Source / ingest
- Media intelligence
- Editorial
- Story Runner
- Autonomous production
- 2D / animation
- 3D / Blender
- Rendering
- Encoding / delivery
- Audio
- Color
- VFX / compositing
- QC / verification
- Assets / interchange
- Production management
- Compute / orchestration
- Observability / telemetry
- Agents / automation
- Studio UI
- Writers Room
- Network / format expansion

The machine-readable registry is `config/oss-horizontal-expansion.json`.

## Current priority OSS tracks

### Distributed rendering
OpenCue and Flamenco are complementary candidates. OpenCue provides scalable render-job scheduling, resource allocation, dependencies, worker management and web monitoring; its current documentation describes support for multi-facility, on-prem, cloud and hybrid deployments. Flamenco remains the Blender-specialized path. Neither becomes canonical until a real Blender workload passes deterministic output, worker failure, resume and telemetry gates.

### Perceptual QC
VMAF, QCTools, MediaConch and deeper container validation can augment the existing ffprobe/frame/audio checks. The deterministic baseline stays in place. New metrics must distinguish known-good from intentionally degraded fixtures.

### Asset and publishing infrastructure
OpenAssetIO, AYON and Pyblish can deepen asset identity, publishing, validation and DCC interoperability. The existing artifact/provenance contract remains authoritative.

### Scene interchange
OpenUSD and MaterialX provide a horizontal path into richer 3D, VFX, animation and interactive workflows without forcing the current editorial pipeline to adopt them prematurely.

### Audio intelligence
Silero VAD and Demucs can deepen dialogue segmentation and source separation. Model provenance and licensing are recorded independently from code licensing.

### Editorial automation
OpenTimelineIO remains the interchange backbone. MLT/Kdenlive/OpenMontage can be evaluated as optional editorial/rendering/agentic backends. Story Runner and Autonomous must remain separate editorial interpretations even when they share physical-source evidence and expensive media analysis.

### Observability
OpenTelemetry, Prometheus and Grafana are the longer-term metrics/traces backend. The durable production ledger and live telemetry channel remain the immediate source of truth until a real production OTel path passes retrieval and recovery tests.

### Delivery
SVT-AV1 can provide an optional storage/delivery codec path where compatibility permits. Bento4 can deepen MP4 container/package inspection. H.264 remains the canonical EP01 delivery path until alternatives pass benchmark and QC gates.

## Branch integration rule

GitHub branches are Development Workstreams. Do not merge stale branches wholesale. Compare each branch against current `main`, classify unique capabilities, preserve valuable changes, reconcile conflicts, validate, and integrate only the validated capability subset.

A branch being stale does not make its capability stale.

## Protection rules

- Never cancel a healthy active production run just to test a new integration.
- Preserve caches, checkpoints and completed artifacts.
- No blind reruns.
- Missing telemetry is `UNKNOWN`, not healthy.
- No timer-based fake percentages.
- No optional dependency becomes a single point of failure.
- PhysicalSourceTimeline remains authoritative for physical events.
- Final masters retain the human editorial lock.
