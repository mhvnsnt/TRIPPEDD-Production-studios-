# TRIPPEDD Production Machine Doctrine

## Purpose

TRIPPEDD is not a narrow render app. It is a creator-owned production machine and future network operating layer: a system that can ingest reality, discover story, develop formats, plan productions, generate/assemble media, review evidence, publish finished work, learn from outcomes, and continuously improve its own production infrastructure.

The studio must expand in **two directions at the same time**:

- **Vertical depth:** make every production stage more capable, measurable, autonomous, recoverable, and professional.
- **Horizontal breadth:** add adjacent capabilities so the studio can handle more kinds of creative work: live action, sketch, animation, mixed media, documentary/reality, music-driven pieces, digital shorts, promos, specials, series packages, and eventually network-scale programming.

A feature is valuable when it increases creative range, production speed, reliability, quality, or reuse—not merely because it increases repository size.

## Executive-producer operating principles

1. **Think like a studio, not a script runner.** Every episode is one production, but the system is the factory that can produce many formats.
2. **Research before narrowing.** Study proven production patterns from animation, sketch comedy, unscripted/reality, music television, digital comedy, post/VFX, and creator-led production. Convert useful patterns into concrete software capabilities.
3. **Creator voice first.** Tools exist to amplify a creator's voice, not flatten it into generic templates.
4. **Reality is evidence.** Source media, timestamps, transcripts, visual observations, approvals, renders, QC, and publish artifacts must remain traceable.
5. **Automate mechanics; reserve human authority for taste.** Machines should ingest, classify, transcode, analyze, render, validate, checkpoint, recover, package, and report. Humans should decide what is funny, what is true to the brand, what is canon, and what ships.
6. **Never fake progress.** Progress must be measured from completed work, artifacts, bytes, frames, jobs, or validated records.
7. **Recover instead of restarting.** Cache, checkpoint, resume, isolate, and replay the smallest failed unit.
8. **Open source is leverage, not decoration.** Pull in a tool when it materially expands capability or removes production friction. Keep third-party systems reproducibly provisioned rather than bloating Git with vendor binaries.
9. **Interoperability is a first-class feature.** Prefer standards and bridges that prevent lock-in: OTIO for editorial interchange, OpenAssetIO for asset resolution/publishing boundaries, OpenColorIO for color, OpenUSD/MaterialX for scene/look interchange where justified.
10. **Every successful integration becomes institutional knowledge.** Record why it was selected, where it enters the pipeline, what evidence promoted it, and how it fails.

## Vertical trajectory

### V0 — Source truth
Physical Source Timeline, ingest manifests, media metadata, checksums, proxy generation, transcripts, shot boundaries, OCR, visual observations, source chronology, and editorial-vs-physical discrepancy detection.

### V1 — Development intelligence
Story graph, premise/beat extraction, sketch inventory, character/entity tracking, joke/idea bank, format cards, storyboard/shot planning, continuity, production requirements, blockers, and approval gates.

### V2 — Assembly and editorial
OTIO-backed timelines, deterministic segment generation, cache-aware assembly, alternate cuts, captions, music/audio branches, generated-media branches, and provenance.

### V3 — Visual production
Blender procedural scenes, 2D/3D interchange, OpenUSD/MaterialX/OCIO boundaries, compositing, motion graphics, previs, animation helpers, render checkpointing, and distributed execution.

### V4 — Sound and finishing
Dialogue cleanup, source separation, loudness/true-peak analysis, timing/pitch processing, music stems, mix validation, color/QC, perceptual quality analysis, subtitles/captions, and delivery packages.

### V5 — Publish/review
Pyblish-style validators, immutable publish manifests, review playlists, version comparison, approval state, release packaging, thumbnails, metadata, and network-ready deliverables.

### V6 — Learning loop
Postmortems, failure clustering, runtime metrics, production-cost metrics, creative outcome notes, reusable templates, tool promotion/demotion, and automated recommendations for future episodes.

## Horizontal expansion map

The studio should be able to move sideways across:

- Live-action sketch
- Improvised/sketch anthology
- Animation
- Stop-motion / puppet-style production
- Mixed live-action + animation
- Documentary / reality / vérité
- Music-video and performance packages
- Digital-first shorts
- Stand-up / storytelling
- Promos, bumpers, cold opens, interstitials
- Specials and compilations
- Serialized comedy
- Character/franchise development
- Social cutdowns and platform variants
- Future interactive / game / virtual-production extensions

The same source truth, production graph, asset identity, provenance, QC, and publish machinery should support these formats rather than spawning isolated apps.

## Network-reference lessons

### Adult Swim: creator identity + format experimentation
Adult Swim's current development leadership explicitly emphasizes championing creators and projects that push animation into new territory. Its slate also spans mature animation and live-action sketch. TRIPPEDD should therefore maintain a **development playground** instead of forcing every idea into the same episode template. citeturn1search6

### Comedy Central: creator-driven development + multiple forms
Comedy Central has historically described development around finding performers, writers, directors, and producers with a strong unique voice and helping them realize it. Its development slate has crossed animation, sketch/variety, scripted comedy, specials, and digital work. TRIPPEDD should model development as a portfolio, not a single pipeline. citeturn1search0turn1search2

Its CC:Studios experiment is especially relevant: concepts could be developed for digital distribution in short-form, long-form, animation, or other formats, with successful digital concepts able to migrate into linear programming. TRIPPEDD should support the same **short → proof → expanded production** trajectory without requiring a network gate first. citeturn1search7turn1search8

### MTV: broad-canvas programming + format reuse
MTV's development history demonstrates the value of a broad slate spanning comedy, scripted, animation, music, and reality, plus projects designed to move between genres and platforms. TRIPPEDD should therefore make format conversion and cross-format development a core capability. citeturn2search0turn2search3

MTV's development model also repeatedly emphasized distinctive, creator-driven content and franchise/library re-imagination. That argues for a reusable **format DNA** layer: a show concept should carry tone, audience, visual language, recurring characters, segment grammar, production requirements, and possible derivatives. citeturn2search4turn2search5

### Sketch-comedy references: recurring characters + modular production
MADtv's long-running structure demonstrates the usefulness of a modular sketch inventory with recurring characters, parody targets, impressions, and reusable production patterns. Workaholics demonstrates a creator-led scripted comedy where the core creative team writes/acts/directs within a repeatable episodic machine. TRIPPEDD should capture recurring characters, locations, props, jokes, setups/payoffs, performers, and production dependencies as reusable graph entities. citeturn1search131turn1search10

## OSS and standards strategy

The existing capability map is only the starting layer. The studio should continuously evaluate:

- **Editorial:** OpenTimelineIO, MLT/Kdenlive/Olive/Shotcut, Fountain/Markdown/JSON Schema.
- **Media intelligence:** FFmpeg/FFprobe, MediaInfo, ExifTool, BWF MetaEdit, OpenCV, PySceneDetect, Faster-Whisper, Tesseract.
- **3D/VFX:** Blender, OpenUSD, MaterialX, OpenColorIO, OpenVDB, Natron, Embree.
- **Asset interoperability:** OpenAssetIO.
- **Audio:** Demucs, aubio, Rubber Band, Audacity/Ardour where a real workflow needs them.
- **QC/publishing:** Pyblish, VMAF, FFprobe/MediaInfo, provenance manifests.
- **Production management:** Kitsu/Zou and compatible asset/production-management boundaries.
- **Render/compute:** GitHub Actions now; Blender Flamenco when render distribution becomes the bottleneck; OpenCue only if measured scale justifies it.
- **Observability:** JSONL events now; OpenTelemetry/Prometheus/Grafana when distributed execution warrants them.
- **Authored UI:** React/Vite, Tailwind, Motion, React Flow, Three.js/React Three Fiber where those create real production surfaces rather than decorative dashboards.

OpenUSD is especially relevant to horizontal expansion because it is designed for scalable interchange and composition of geometry, shading, lighting, physics, and other scene data across DCC applications. citeturn0search3turn0search4 MaterialX provides an open, renderer-independent representation for rich material and look-development data. citeturn0search13 OpenColorIO is explicitly geared toward motion-picture production and visual effects/color workflows. citeturn0search0 OpenAssetIO provides a common API boundary between host tools and asset-management systems, reducing custom integration glue. citeturn0search1

## Promotion gate

No tool becomes a dependency merely because it is interesting. Promotion requires:

1. License and maintenance check.
2. Reproducible installation.
3. Real TRIPPEDD input smoke test.
4. Defined production boundary.
5. Measured output.
6. Provenance record.
7. Failure and recovery test.
8. Demonstrated benefit over the existing path.
9. No regression to the canonical EP01 route.

## The machine we are building

The target is a **creator operating system** with a production graph at its center:

`SOURCE → TRUTH → DEVELOPMENT → PLAN → CREATE → ASSEMBLE → REVIEW → QC → PUBLISH → LEARN`

Each arrow should be observable, resumable, interchangeable, and increasingly automated. Each node should be replaceable by a better open or proprietary implementation without rewriting the entire studio.

The repository therefore should grow primarily in authored orchestration, adapters, contracts, schemas, tests, UI, production intelligence, recovery mechanisms, and integration surfaces. Heavy third-party runtimes belong in reproducible environments and caches. A small Git footprint is acceptable; a small capability graph is not.

## Standing instruction

When evaluating any future change, ask two questions:

**Vertical:** Does this make an existing production capability deeper, faster, more reliable, more measurable, more recoverable, or more professional?

**Horizontal:** Does this open a meaningful new production direction, format, medium, workflow, or reuse path?

If neither answer is yes, the change is probably noise. If either answer is strongly yes, investigate it. If both are yes, prioritize it.
