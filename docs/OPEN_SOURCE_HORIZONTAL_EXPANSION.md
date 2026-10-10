# TRIPPEDD Open-Source Horizontal Expansion

This is the operating map for expanding TRIPPEDD across the Studio Capability Map. Open source is selected by capability fit and evidence, not by library count.

## Operating rule

For every Studio Domain, continuously:

1. discover relevant maintained open-source capabilities;
2. compare them with the existing deterministic path;
3. integrate only where they materially improve capability, performance, interoperability, quality, recovery, or cost;
4. run real-input smoke tests in isolation;
5. measure output and throughput;
6. verify provenance and artifact compatibility;
7. exercise failure/recovery/resume;
8. promote only after regression checks pass.

A missing measurement is `UNKNOWN`, never a successful state.

## Domain coverage

| Domain | Horizontal OSS focus |
|---|---|
| Development / Production | Kitsu, AYON, OpenAssetIO, workflow/revision tooling |
| Media Ingest | GStreamer, FFmpeg ecosystem, MediaInfo-compatible inspection |
| Media Intelligence | Whisper/faster-whisper, Silero VAD, OpenCV, PySceneDetect, OCR |
| Editorial | OpenTimelineIO, MLT, Kdenlive-compatible interchange |
| Story Runner / Autonomous | agentic pipeline patterns, checkpoints, deterministic manifests, local workflow reproduction |
| Animation / 2D | Krita, OpenToonz-class pipelines, interchange and frame caches |
| 3D / Blender | Blender, OpenUSD, MaterialX, OpenImageIO, OpenEXR |
| Rendering | Blender headless, Flamenco, OpenCue, local worker execution |
| Encoding / Transcoding | FFmpeg, SVT-AV1, VapourSynth and codec-specific backends |
| Audio | SoX, Ardour, Demucs, VAD and loudness tooling |
| Color | OpenColorIO / ACES-compatible transforms |
| VFX / Compositing | frei0r, OpenImageIO, OpenEXR and node/compositing candidates |
| QC / Validation | VMAF, MediaConch, QCTools, ffprobe and artifact integrity checks |
| Assets / Interchange | OpenAssetIO, OpenUSD, MaterialX, content-addressed manifests |
| Compute / Orchestration | GitHub Actions, self-hosted runners, act, Flamenco, OpenCue |
| Observability | OpenTelemetry, Prometheus, Grafana, durable production ledger |
| Studio UI | Grafana/operator surfaces as infrastructure; TRIPPEDD remains the authored studio UI |
| Storage / Artifacts | content-addressed caches, manifests, resumable artifact stores |
| AI / Agents | local model runtimes, tool registries, structured agent contracts and temporal tooling |
| Writers Room | structured text/asset provenance, review and approval tooling |
| Network / Formats | Godot and interactive runtimes, social/delivery tooling, format-specific encoders |
| Delivery / Distribution | FFmpeg, MediaConch, codec backends, platform derivative generation |

## Current promotion order

### Protect EP01
Active Story Runner and Autonomous production remain canonical. OSS experiments run beside production and consume verified caches/artifacts where possible. No candidate is allowed to trigger a blind cancellation/restart.

### Deepen first
- deterministic media inspection and QC;
- resumable rendering and checkpoint recovery;
- compute failover beyond hosted Actions;
- editorial/interchange interoperability;
- telemetry and historical production metrics;
- asset/provenance identity;
- audio/color finishing.

### Expand next
- 2D and 3D animation pipelines;
- documentary/reality source intelligence;
- music/performance workflows;
- social-native derivatives;
- interactive/game extensions;
- multi-format delivery.

## Maturity vocabulary

`DISCOVERED → RESEARCHED → CANDIDATE → INTEGRATED → SMOKE_TESTED → VALIDATED → PRODUCTION`

Failure/retirement states:

`UNKNOWN → QUARANTINED → DEPRECATED → REJECTED`

## Branch reconciliation

GitHub branches are Development Workstreams. Their useful capabilities are reconciled against current `main` non-destructively. A stale branch is not automatically obsolete, and a large branch is not automatically merged wholesale.

The unit of value is the capability, not the branch.

## Telemetry contract

Every long-running production operation must expose measured:

- overall percentage;
- elapsed time;
- throughput/rate;
- ETA when calculable;
- current operation;
- heartbeat;
- artifact/evidence identity.

If those measurements cannot be retrieved, the operation is `UNKNOWN` rather than `in_progress` by assertion.
