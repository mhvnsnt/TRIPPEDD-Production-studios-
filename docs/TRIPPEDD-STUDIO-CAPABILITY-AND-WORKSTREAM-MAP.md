# TRIPPEDD Studio Capability & Workstream Map

## Purpose

This document is the operating vocabulary for expanding TRIPPEDD in two dimensions at once:

- **Vertical slices** deepen one production capability from intent through verified artifact.
- **Horizontal slices** extend a capability across formats, workflows, agents, compute backends, and products.

The studio is treated as a **Studio Operating System**, not a single episode editor.

## Hierarchy

Use this hierarchy when describing repo work:

`Studio Domain → Capability → Pipeline → Stage → Operation → Artifact → Evidence`

Cross-cutting concerns apply to every level:

`Telemetry · Reliability · Recovery · Caching · Provenance · Reproducibility · Performance · Security · Interoperability`

A Git branch is a **Development Workstream**. A PR is a proposed **Integration Unit** for one or more workstreams.

## Studio Domains

### 1. Development & Programming
Project creation, format development, story/segment development, Writers Room, production planning, talent, requirements, blockers, approvals, production graph, proof-of-concept migration.

### 2. Source & Ingest
Drive/local ingest, source registration, checksums, provenance, resumable transfer, proxy generation, media inventory, PhysicalSourceTimeline.

### 3. Media Intelligence
FFprobe, PySceneDetect, Whisper/faster-whisper, OpenCV, OCR/Tesseract, transcript intelligence, shot/scene detection, visual observations, evidence fusion, confidence and candidate generation.

### 4. Editorial
Editorial timeline, candidate selection, scene assembly, pacing, transitions, music/SFX placement, editorial notes, human review, greenlight.

### 5. Production Runners
Story Runner, Autonomous Production, future format-specific runners, deterministic assembly, independent-cut semantics, shared verified source/media assets without sharing editorial authorship.

### 6. Visual Production
2D animation, 3D/Blender, character/rigging, motion, generated visuals, compositing, VFX, graphics, titles, terminal tags, reusable visual assets.

### 7. Audio & Sound Finishing
Dialogue cleanup, separation, mixing, loudness, music, SFX, mastering, spatial/immersive paths.

### 8. Color & Image Finishing
Color management, OCIO, transforms, grading, HDR/SDR, image quality and finishing profiles.

### 9. Encoding & Delivery
FFmpeg/transcoding, final concat, delivery profiles, masters, platform cutdowns, social exports, archival packages, delivery validation.

### 10. QC & Verification
Technical QC, perceptual QC, artifact validation, evidence validation, regression checks, canonical-artifact gates, human editorial greenlight.

### 11. Compute & Orchestration
GitHub Actions, self-hosted runners, local execution, `act`, Blender workers, Flamenco/OpenCue candidates, queues, worker allocation, failover, checkpoint restoration, bounded retries.

### 12. Observability & Telemetry
Measured progress, percentage, completed/total, elapsed, throughput, ETA, current operation, heartbeat, logs, metrics, traces, resource telemetry, durable live channel, historical production analytics.

**Operating law:** missing telemetry is `UNKNOWN`, never fabricated progress and never silently healthy.

### 13. Assets, Interchange & Provenance
Asset registry, OpenAssetIO boundaries, OpenUSD/MaterialX/OCIO boundaries, OTIO interchange, manifests, cache identity, checksums, source lineage, artifact provenance.

### 14. Storage & Artifact Lifecycle
Caches, checkpoints, intermediate artifacts, immutable cache keys, artifact retention, retrieval, archival, deduplication, cleanup policies.

### 15. Agents & Automation
Producer, director, writer, editor, analyst, animation, render, QC, recovery, research, open-source scout, asset librarian, orchestration agents.

### 16. Studio Frontend / UX
Studio shell, project browser, episode workspace, timeline, source/evidence browser, production graph, agent console, Writers Room, render monitor, QC console, delivery console, settings, activity/history, live telemetry, recovery controls.

### 17. Visual Identity System
Authored psychedelic atmosphere, typography, motion language, surfaces, interaction language, visual hierarchy, accessibility and theme primitives. This is the studio's authored identity layer, not generic SaaS decoration.

### 18. Network & Format Expansion
Live-action sketch, animation, stop-motion/puppet, mixed media, documentary/reality, music/performance, digital short, stand-up/storytelling, promos/bumpers/interstitials, serialized comedy, character/franchise, platform cutdowns, interactive/virtual production.

## Cross-Cutting Capability Families

Every domain should be evaluated through these lenses:

- **Reliability:** can it fail safely and visibly?
- **Recovery:** can completed work resume without destructive restart?
- **Telemetry:** can a human retrieve real progress?
- **Performance:** can throughput improve without changing meaning?
- **Caching:** can verified work be reused deterministically?
- **Provenance:** can we prove where an artifact came from?
- **Reproducibility:** can the same inputs recreate the result?
- **Interoperability:** can the capability exchange data with other tools?
- **Security:** are credentials, permissions, and untrusted inputs bounded?
- **Accessibility:** can the interface and outputs be used by the intended creators?

## Vertical Slice Definition

A vertical slice is complete only when the capability crosses the whole required chain:

`intent → inputs → execution → measured progress → artifact → validation → provenance → recovery path → usable output`

Example: EP01 Story Runner is not complete merely because a renderer starts. The vertical slice reaches a verified final artifact and QC result.

## Horizontal Slice Definition

A horizontal slice extends one capability across multiple domains or formats without duplicating core primitives.

Examples:

- **Telemetry horizontal slice:** Story Runner + Autonomous + ingest + analysis + render + QC + UI + compute failover.
- **Interchange horizontal slice:** OTIO + OpenAssetIO + OpenUSD/MaterialX/OCIO where justified.
- **Recovery horizontal slice:** ingest + analysis + rendering + assembly + delivery.
- **Format horizontal slice:** reuse source truth, production graph, asset provenance, QC and delivery primitives across live-action, animation and mixed media.

## Workstream Integration Protocol

For every non-main branch:

1. Identify the workstream's domain(s) and capabilities.
2. Compare it with current `main`, not the branch's old base.
3. Classify each changed file as additive, corrective, superseding, conflicting, obsolete, or salvageable.
4. Preserve unique valuable behavior before resolving overlap.
5. Rebase/reconcile conceptually or mechanically only after protecting active production.
6. Validate dependencies, tests, workflow syntax, runtime behavior, artifact contracts, telemetry and recovery.
7. Promote only the validated subset.
8. Merge only when the integration unit is compatible with current `main` and does not regress canonical production.

**Never blindly merge a stale branch. Never discard useful work merely because its branch is behind.**

## Open-Source Promotion Vocabulary

When evaluating an external project, use these states:

`DISCOVERED → RESEARCHED → CANDIDATE → INTEGRATED → SMOKE_TESTED → VALIDATED → PRODUCTION`

Failure/retirement states:

`UNKNOWN → QUARANTINED → DEPRECATED → REJECTED`

Open source is a source of capabilities, not a reason to add dependencies. A candidate needs installation/provisioning evidence, real-input smoke evidence, production-boundary integration, measured output, provenance, recovery behavior, and regression validation before production promotion.

## EP01 Safety Rule

The active Story Runner remains canonical and protected. Infrastructure changes must not trigger unnecessary restarts. If independent evidence establishes a stall or bottleneck:

`preserve → diagnose → salvage → checkpoint → repair → restart from nearest valid state → verify telemetry → continue`

No blind reruns. Actions budget and completed work are production resources.

## Operating Language

Preferred commands:

- “Deepen the **[capability] vertical slice**.”
- “Expand **[capability] horizontally** across the relevant domains.”
- “Audit the **[domain] capability layer**.”
- “Reconcile the **[workstream]** against current `main`.”
- “Promote the OSS candidate through the **evidence gates**.”
- “Add **cross-cutting telemetry/recovery/provenance** to this pipeline.”
- “Extend the **network/format expansion layer**.”
- “Preserve the canonical path and integrate only validated improvements.”
