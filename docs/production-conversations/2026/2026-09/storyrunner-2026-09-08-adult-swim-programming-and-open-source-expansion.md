# Storyrunner Production-Room Record — Adult Swim Programming + Open-Source Expansion

**Date:** 2026-09-08
**Property:** TRIPPEDD Production Studios
**Layer:** STORYRUNNER
**Status:** RESEARCH + DECISION
**Participants:** USER_SHOWRUNNER, CHATGPT/AGENT

## User direction

The showrunner directed the studio to continue building while EP01 Autonomous renders, keep watching the autonomous workflow, and research the larger production language around TRIPPEDD rather than treating the pilot as the only problem.

The requested research scope includes Adult Swim's long-running programming/interstitial history, the user's established influences including `Off the Air` and `Xavier: Renegade Angel`, and open-source software that can strengthen any part of production, finishing, scheduling, audio, asset management, rendering, QC, or delivery.

## Production decision

TRIPPEDD should be modeled as a **programming ecosystem**, not merely an episode renderer.

A new `ProgramClock` data model was added on the upgrade branch. It treats episodes, segments, bumps, interstitials, network IDs, fake commercials, promos, viewer cards, cold opens, tags, and shorts as first-class program units while preserving physical-source truth and human editorial authority.

## Adult Swim research conclusions

Adult Swim's history demonstrates that interstitial material can become part of a show's/network's identity rather than merely filling commercial breaks. Historical packages evolved substantially over time, including early pool footage, safety-manual material, black-and-white text cards, scenic IDs, Toonami material, and viewer-oriented formats. BumpWorthy independently archives multiple categories of this material.

The lesson for TRIPPEDD is not imitation. The useful architectural lesson is:

**The space between episodes can itself be programming.**

That creates room for original:

- fake commercials;
- public-service-style absurdity;
- network IDs;
- viewer cards;
- music-led visual fragments;
- recurring micro-characters;
- Bannon/The Bastard interstitials;
- production-room artifacts;
- callbacks and continuity jokes;
- episode promos and future-story teases;
- intentionally mundane buttons after extreme material.

## Open-source research conclusions

The existing stack remains centered on FFmpeg/FFprobe, OpenCV, PySceneDetect, Tesseract, faster-whisper, OpenTimelineIO, Blender, Kdenlive/MLT, Natron, OpenColorIO, OpenAssetIO, and OpenCue.

Additional open-source candidates worth integrating where they solve a real production problem include:

- **Ardour** for serious multitrack audio recording, editing, mixing, automation, and video-synchronized audio work.
- **OBS Studio** for capture, monitoring, live production, reference recording, and future audience/live workflows.
- **OpenCue** for distributed rendering once render workload justifies a farm; its current release line includes a distributed scheduler and browser-based management.
- **OpenAssetIO** as the asset-resolution/publishing boundary rather than another monolithic asset database.
- **Kdenlive/MLT** as an open editorial/render backend alongside the internal OTIO-driven assembly system.

Open-source dependencies should be adopted as real capabilities with executable health checks and provenance, not as a shopping list. Archived or weakly maintained projects remain optional and should not become hidden required dependencies.

## Creative principle

The studio should keep the established distinction between:

`PHYSICAL SOURCE → EVIDENCE → EDITORIAL INTERPRETATION → GENERATED MATERIAL → PROGRAMMING / DELIVERY`

and should never use the programming layer to rewrite physical chronology.

The AI is not the aesthetic. The decisions are the aesthetic.
