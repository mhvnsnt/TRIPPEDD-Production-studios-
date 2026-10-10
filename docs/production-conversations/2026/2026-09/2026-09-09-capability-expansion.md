# 2026-09-09 — Capability expansion and authored studio layer

## Producer
> One megabyte is small, bro. I made a bigger repo than that in less time, with, like, Google AI Studio building, like, code dummy and building M engine and all that. Like, why are you building such a small repo, and why are you building so slow? That's probably why things aren't getting, like, production-grade level. I know a real production studio would have at least a gig of work, like a gig of open source tools and things in all different types of directions for animation, Blender, 3D, for storyline, storyboards, for direction, for all that. Like, bro, plan out a bigger OSS, or not OSS, but, like, whatever expands beyond the OSS, like other things. We need way more open source, and we need way more pulled in. Like one megabyte feels like too small of a app and repo. Even though that would be good to download on my phone, at this point, that's still, I feel like, that's why our work is going so slow, and we could have way more. And, like, the front-end UI integration, I want it to be more, like, psychedelic and customed out, like authored. I want the whole experience to be more authored. But, like, really I want more open source to do way more different things and to make our pipeline more efficient and work faster and better.

## Agent
I checked the actual repository and agreed with the core diagnosis: the 1 MB Git footprint is not the same thing as the runtime footprint, but the studio's capability graph was still too narrow for the ambition.

### Changes made on `main`

- `8790e6e523590253aa974d73a055a55b0622f078` — added `config/oss-stack.json`, expanding the capability graph across:
  - physical media and forensics
  - editorial/story/timeline
  - 2D/3D/animation/VFX
  - color/material/scene interchange
  - audio and source separation
  - render distribution
  - production management
  - AI/media analysis
  - observability
  - authored UI
- `2f5f789a178b83c67f4bd3886bbe64afa53a06b0` — expanded the executable/interchange toolchain registry to include MediaInfo, ExifTool, BWF MetaEdit, VMAF, Kdenlive, MLT, Olive, Shotcut, Audacity, Ardour, Rubber Band, aubio, OpenColorIO, OpenAssetIO, OpenUSD, MaterialX, OpenVDB, Natron, Embree, Flamenco, OpenCue, Demucs, Pyblish, Kitsu/Zou, PyTorch, ONNX Runtime, Prometheus, Grafana and OpenTelemetry.
- `aa6f2eb47a8425dfff174966919e01cdcedaf6c9` — expanded the audit so optional tools are honestly reported as AVAILABLE, UNAVAILABLE or SERVICE_CANDIDATE. Missing tools are not falsely marked available.
- `ef426fe0c2debca82036fd9b5dbf1637cff40902` — added the full `STUDIO-SYSTEM-BLUEPRINT.md` with production capability boundaries and promotion gates.
- `731888acd5d5f9edea8e3b515d012c696ba8a042` + `62c7d5091a84ebf51d408da7198374f13720aacc` + `c96058a918a6023a88ba10711231639afbf281c6` — added and integrated an authored psychedelic studio atmosphere layer rather than leaving the UI as a generic dashboard.
- `0b01a9e9ee5307111828c088de7bb90e7197df04` — attacked the actual Bastard rendering bottleneck: restore the existing v4 frame checkpoints, skip chunks that already contain twelve valid frames, and render missing chunks in bounded parallel batches (default three Blender processes). Existing checkpoint keys were preserved so this optimization does not throw away salvageable work.

## OSS direction

The target is not to inflate Git history with copied third-party source. Heavy runtimes belong in reproducible provisioning, caches, containers, or external services. The repository should become much richer in orchestration, adapters, contracts, provenance, tests, UI, production logic and integration code.

Priority promotion path:

1. parallel/resumable Blender rendering
2. VMAF perceptual QC
3. Pyblish-style publish validation
4. OpenAssetIO asset identity
5. OpenColorIO color contracts
6. OpenUSD/MaterialX scene/material interchange
7. Demucs audio isolation without overwriting source audio
8. Kitsu/Zou production tracking where it reduces manual coordination
9. Flamenco before heavier distributed render infrastructure
10. authored React/visual production-graph UI

Promotion remains evidence-gated: resolve/install → real-input smoke test → measured output → validation → recovery behavior.

## Size clarification

GitHub reports the repository at approximately **1.01 MB**. That is not the size of the actual production runtime. It excludes installed dependencies, Blender, model weights, media, Actions caches/artifacts and other generated/runtime state. The goal is therefore to expand the actual studio capability and runtime substantially without creating artificial Git bloat by committing vendor binaries or node_modules.
