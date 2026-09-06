# TRIPPEDD Open Source Integration Matrix

This document outlines the strategy for orchestrating existing open-source production tracking, editorial interchange, and execution tools underneath the TRIPPEDD core semantic layer.

## Architecture Vision

```
TRIPPEDD STUDIO (Orchestration & Ontology)
 │
 ├── TRIPPEDD CORE (Reality/Provenance/Formats/Gags)
 │    ├── Episode, Segment, Story, Asset, Job
 │    └── Formats, Lore, Performance, Provenance
 │
 ├── ORCHESTRATION LAYER
 │    ├── Kitsu (Production Tracking)
 │    ├── OTIO (Editorial Interchange)
 │    └── OpenAssetIO (Asset Interchange)
 │
 ├── TOOL ADAPTERS
 │    └── Blender, ComfyUI, FFmpeg, Kdenlive, Unreal
 │
 └── EXECUTION
      └── OpenCue (Render Farm)
```

## Matrix

| Software / Project | License | API / SDK | Deployment | Data Model Overlap | Integration Method | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kitsu / Zou** | AGPLv3 | REST (JSON:API), Python (Gazu) | Docker / Cloud | **High**: Episodes, Sequences, Shots, Assets, Tasks, Reviews. | **Sync Adapter**: TRIPPEDD's `Episode/Segment/Asset` translates to Kitsu's `Episode/Sequence/Shot`. Sync via webhooks/REST API. | **High** |
| **OpenTimelineIO** | Apache 2.0 | C++, Python, Swift | Library | **High**: Tracks, Clips, Transitions, Markers. | **Export/Import**: Generate `.otio` files for Segments/Episodes to send to Kdenlive/Premiere. TRIPPEDD adds provenance metadata to OTIO metadata dictionaries. | **High** |
| **OpenAssetIO** | Apache 2.0 | C++, Python | Library / Daemon | **Medium**: Asset resolution and versioning. | **Resolver**: Implement a TRIPPEDD Manager plugin so DCCs (Blender, etc.) can query TRIPPEDD's Asset Registry natively. | **Medium** |
| **OpenCue** | Apache 2.0 | gRPC, Python | Distributed | **Low**: Render jobs, layers, frames. | **Job Submission**: Map TRIPPEDD `Job` entities to OpenCue submissions when physical execution requires heavy rendering. | **Low** (Initial) |
| **Kdenlive / MLT** | GPLv2+ | XML (.kdenlive), OTIO | Local Desktop | **Medium**: Timelines, Effects. | **Workflow**: Read/write OTIO timelines. Use MLT framework (via melt CLI) for automated lightweight compositing. | **Medium** |
| **Blender** | GPLv2+ | Python (bpy) | Local Desktop | **High**: Scenes, Collections, Render Layers. | **Add-on**: Custom Blender Add-on communicating with TRIPPEDD via Local Service/WebSocket or via OpenAssetIO. | **High** |
| **ComfyUI** | GPLv3 | REST / WebSocket | Local / Cloud | **Medium**: Workflows, nodes, prompt queues. | **API Adapter**: Direct REST queue submission and WebSocket listening for generation jobs. | **High** |
| **OpenPype / AYON** | Apache 2.0 | Python, GraphQL | Docker / Desktop | **High**: Pipeline orchestration, validation. | **Reference**: Borrow Pyblish validation concepts, but avoid full replacement of Kitsu. | **Low** |

## Implementation Strategy

1. **Do not fork and modify** these open-source tools unnecessarily.
2. TRIPPEDD Studio retains **Authoritative State** regarding Reality, Provenance, Formats, and Gags.
3. Kitsu acts as the underlying database/tracker for standard production status and assignments.
4. OTIO acts as the structural interchange format.

