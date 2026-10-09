# 2026-09-10 — Episode Recovery / TRIPPEDD network Slate / God Molecule / Short Ident Gate

## Status

`HARDENING PASS RECORDED — IDENT NOT YET VERIFIED GREEN`

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

The 10–20 second proof is not a generic test card. It is a **TRIPPEDD network commercial/ident**: one recognizable recurring network mark/card language that can mutate through animation, typography, psychedelic/surreal treatment, texture, material, and motion while sampling the visual worlds of the network's properties.

The current authored proof source deliberately uses symbolic geometry and typography for **Trippedd**, **The Bastard**, **In the Bushes**, and **God Molecule**. It does not fabricate creator likeness or finished God Molecule footage.

## HARD GATE

No real episode run/cut is to be launched until the short proof completes the hardened end-to-end path and passes final QC.

A passing unit test, typecheck, workflow-start status, or synthetic test card is not sufficient proof.

## GARDEN PASS — 2026-09-10

### Fixed

1. Replaced the old `testsrc2` source in `.github/workflows/production-short-e2e-gate.yml` with a deterministic, continuously authored 240-frame Blender network-ident source.
2. Added `production/network-ident/build_network_ident.py` with restartable frame checkpoints and explicit generated-material provenance.
3. The authored source is rendered at 1280x720 / 24fps for 10 seconds, then encoded once with FFmpeg and passed into the real source-analysis/editorial build path.
4. Removed unrelated EP01 subjectivity/Bastard render jobs from the short gate. The proof now tests the network-ident production path rather than coupling its result to unrelated EP01 generated assets.
5. Added source-level ffprobe, MediaInfo, and ExifTool evidence before production assembly.
6. Added an OTIO continuity assertion requiring one assembled source clip rather than a multi-card slideshow.
7. Kept the gate manual and fail-closed; no automatic EP01 launch is permitted unless the successful gate belongs to the current `main` SHA.

### Deliberately not changed

- The real EP01 source requirement remains 19 supported media files.
- Real-source transport remains fail-closed when Google Drive media cannot be retrieved.
- Existing recovery/cache/telemetry machinery remains the production safety layer for EP01.
- God Molecule/Mars creator-likeness rules remain unchanged: actual supplied photographs are the source for likeness work; generated material may add effects, not invent a replacement person.

### Verification status

The hardening changes were committed to `main`, but the new ident gate has **not yet been declared PASS**. A real GitHub Actions execution must complete successfully before promotion is considered proven.

Latest hardening commits:

- `fde8bc19b93e675533fdf2d12508980cc94106e6` — continuous authored network-ident generator.
- `b497817a7da439c0b95ec855ddaefd6059309d1b` — hardened short E2E gate.

## OPEN-SOURCE HARDENING DIRECTION

The production stack continues to prioritize mature open-source components rather than proprietary black boxes. Current components include FFmpeg, Blender, PySceneDetect, OpenCV, faster-whisper, OpenTimelineIO, rclone, and MediaInfo, with OpenColorIO remaining a targeted candidate for color-managed network graphics where it removes a real inconsistency.

Open-source additions are to be treated as production tools, not trophies: integrate a dependency only when it removes a demonstrated bottleneck, increases recovery/repeatability, or materially improves output quality.

## RECOVERY / PRODUCTION SAFETY

Real production remains fail-closed. Source completeness cannot be inferred from a successful directory listing; missing or throttled media remains `UNKNOWN/BLOCKED`. Completed render chunks and valid cached artifacts must be salvaged rather than regenerated blindly. Telemetry must be measured; missing telemetry is not `RUNNING`.

The real EP01 workflow is gated behind the short proof. The short proof itself must not be confused with completion of EP01.

## CHAT STREAM RESILIENCE

God Molecule development and other materially relevant creative decisions are to be persisted in the GitHub production conversation archive so a ChatGPT stream interruption does not destroy production context. Chat-stream errors are treated as a separate product/session reliability problem, not as evidence that the production repository lost its state.

## Related production artifacts

- `production/network-ident/build_network_ident.py`
- `.github/workflows/production-short-e2e-gate.yml`
- `.github/workflows/promote-short-gate-to-ep01.yml`
- `.github/workflows/ep01-story-runner.yml`
- `docs/TRIPPEDD-NETWORK-SLATE.md`
- `docs/TRIPPEDD-NETWORK-STUDIO-OPERATING-MODEL.md`
- `docs/EP01-SOURCE-UNBLOCK.md`
- `docs/production-conversations/README.md`
- `scripts/production/verify-oss-stack.sh`
- GitHub issue `#16` — TRIPPEDD Live Production Telemetry

## Next production objective

**Run the hardened TRIPPEDD network ident gate. Only after the real GitHub Actions proof is green should the EP01 Story Runner be promoted/launched.**
