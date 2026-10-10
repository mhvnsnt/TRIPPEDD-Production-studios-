# 2026-09-09 — Production Machine Doctrine Expansion

## Producer direction

The studio must stop thinking narrowly about individual pipeline fixes. The required trajectory is both:

- **Vertical:** deeper production-grade capability, automation, measurement, recovery, QC, finishing, and reliability at every existing stage.
- **Horizontal:** broader capability across live-action sketch, animation, mixed media, documentary/reality, music/performance, digital shorts, promos, serialized comedy, character/franchise development, and future interactive/virtual-production work.

Open-source research is not a random library-collection exercise. It is a deliberate way to expand the studio's production horizons and remove bottlenecks. The repository should preserve the reasoning so future agents continue operating as an executive-producer/developer for the TRIPPEDD studio and network rather than optimizing only the immediate bug.

## Research direction

Reference models investigated include Adult Swim, Comedy Central, MTV, and the user's stated sketch/comedy lineage. The research points toward a creator-driven development playground, broad format slates, modular sketch/character systems, digital-to-larger-format migration, cross-format reuse, and strong creator voice.

Adult Swim's current development leadership describes its role around championing creators and projects that push animation into new territory, while its slate includes both mature animation and live-action sketch. citeturn1search6

Comedy Central has described development as finding strong, unique comedic voices and helping performers/writers/directors/producers realize their vision; its historical development slate crossed animation, sketch/variety, scripted comedy, specials, and digital. CC:Studios specifically explored short-form/long-form/digital development and migration into linear programming. citeturn1search0turn1search7turn1search8

MTV's development history demonstrates a deliberately broad canvas spanning comedy, scripted, animation, music and reality, along with attempts to create synergy between genres and formats. citeturn2search0turn2search3

The production-system implications are now encoded in `docs/PRODUCTION-MACHINE-DOCTRINE.md` and `config/production-capability-matrix.json`.

## Standards and OSS direction

The studio's deeper interoperability layer should use standards where they create leverage: OpenTimelineIO for editorial interchange; OpenAssetIO for host/asset-management boundaries; OpenColorIO for motion-picture color management; OpenUSD for scalable scene composition/interchange; and MaterialX for portable material/look development. citeturn0search1turn0search0turn0search3turn0search13

The immediate rule remains: do not vendor giant third-party binaries into Git merely to make the repository look larger. Expand the authored capability graph, provision heavy tools reproducibly, and promote integrations only after real-input validation and recovery testing.

## Implementation

- Added `docs/PRODUCTION-MACHINE-DOCTRINE.md` as a standing operating doctrine.
- Added `config/production-capability-matrix.json` to make vertical/horizontal coverage machine-readable.
- Preserve the current EP01 canonical path and active production run while these expansions are developed around it.
