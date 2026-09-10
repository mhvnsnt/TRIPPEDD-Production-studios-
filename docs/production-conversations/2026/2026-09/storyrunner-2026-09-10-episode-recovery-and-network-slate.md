# 2026-09-10 — Episode Recovery / TRIPPEDD network Slate / God Molecule / Short Ident Gate

## Status

`RECONSTRUCTED FROM AVAILABLE CONTEXT`

This record preserves materially relevant production-room direction available to the connected agent. It is not a fabricated verbatim transcript.

## Canonical naming

- **Show:** Trippedd
- **Network:** TRIPPEDD network
- **Studio:** TRIPPEDD Production studios

These names are distinct and should remain distinct in repository documentation, production logs, and future generated artifacts.

## USER / SHOWRUNNER

The production priority is to stop getting trapped in diagnostics and actually get the episode made. The TRIPPEDD Production studios / TRIPPEDD network has a programming lineup including **The Bastard**, **In the Bushes**, and **Trippedd**. **God Molecule** is being developed as a recurring Trippedd segment with potential to become its own show/property. Its Mars visual direction and shader work remain part of the development record.

The immediate infrastructure objective is hardening: pull in useful open-source production tooling, eliminate known failure modes, and prove the entire production path on a short piece before spending a long render window on a real episode.

## SHORT PROOF DECISION

The 10–20 second proof is not a generic test card. It will be a **TRIPPEDD network commercial/ident** inspired by the network-card idea: a recognizable recurring network mark/card language that can mutate through animation, typography, psychedelic/surreal treatment, texture, material, and rapid transitions while briefly sampling the visual worlds of the network's properties.

The initial concept pool is:

- **Trippedd** — umbrella comedy identity / mixed-format energy.
- **The Bastard** — established reusable terminal/generated material.
- **In the Bushes** — established network property.
- **God Molecule** — developing property/segment, with the existing Mars/shader direction treated as development reference rather than fabricated footage.

The piece should read as one coherent **TRIPPEDD network** ident, not a slideshow and not a fake episode.

## HARD GATE

No real episode run/cut is to be launched until the short proof completes the hardened end-to-end path and passes final QC.

The proof is required to exercise, as applicable:

1. deterministic source materialization;
2. source analysis and evidence generation;
3. editorial assembly;
4. generated/animated material;
5. Blender/headless rendering;
6. FFmpeg media assembly;
7. JSON and OpenTimelineIO output;
8. final MP4 technical QC;
9. audio/video/duration/resolution/FPS validation;
10. machine-readable progress/telemetry contracts; and
11. artifact preservation for inspection.

A passing unit test, typecheck, or workflow-start status is not sufficient proof.

## OPEN-SOURCE HARDENING DIRECTION

The production stack continues to prioritize mature open-source components rather than proprietary black boxes. Current and planned components include FFmpeg, Blender, PySceneDetect, OpenCV, faster-whisper, OpenTimelineIO, rclone, MediaInfo, and OpenColorIO. Motion Canvas is also a candidate for a dedicated 2D/vector animation layer because its TypeScript animation model fits the network-ident/graphics use case; it should be integrated only if it improves the production path without introducing unnecessary dependency fragility.

OpenColorIO is particularly relevant to the network-ident layer because consistent color management matters when rapidly mixing the visual languages of multiple properties. MediaInfo is useful as a second independent technical-metadata/QC view alongside ffprobe.

## RECOVERY / PRODUCTION SAFETY

Real production remains fail-closed. Source completeness cannot be inferred from a successful directory listing; missing or throttled media remains UNKNOWN/BLOCKED. Completed render chunks and valid cached artifacts must be salvaged rather than regenerated blindly. Telemetry must be measured; missing telemetry is not RUNNING.

The real EP01 workflow is gated behind the short proof. The short proof itself must not be confused with completion of EP01.

## CHAT STREAM RESILIENCE

God Molecule development and other materially relevant creative decisions are to be persisted in the GitHub production conversation archive so a ChatGPT stream interruption does not destroy production context. Chat-stream errors are treated as a separate product/session reliability problem, not as evidence that the production repository lost its state.

## Related production artifacts

- `docs/TRIPPEDD-NETWORK-SLATE.md`
- `docs/TRIPPEDD-NETWORK-STUDIO-OPERATING-MODEL.md`
- `docs/EP01-SOURCE-UNBLOCK.md`
- `docs/production-conversations/README.md`
- `.github/workflows/production-short-e2e-gate.yml`
- `.github/workflows/promote-short-gate-to-ep01.yml`
- `.github/workflows/ep01-story-runner.yml`
- `scripts/production/verify-oss-stack.sh`
- GitHub issue `#16` — TRIPPEDD Live Production Telemetry

## Next production objective

**Finish the hardening pass, then run the TRIPPEDD network 10–20 second ident as the end-to-end proof. Only after that proof is genuinely green should the real EP01 Story Runner be promoted/launched.**
