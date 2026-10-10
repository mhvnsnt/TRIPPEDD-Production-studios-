# EP01 Finish-Gate Hardening — 2026-09-09

## Producer direction
Harden every unfinished area of the current production path before the live episode reaches it. Preserve active work, eliminate avoidable roadblocks and bottlenecks, make progress measurable, and use open-source tooling where it materially improves the step. After EP01 is real and complete, expand the same architecture into additional formats, animation, Blender/3D, graphics, VFX, and broader network production.

## Live production evidence
Canonical EP01 Story Runner run `34394290662` remains the valuable active run. At the hardening check:
- 12/12 subjectivity chunks were successful.
- Subjectivity assembly was successful.
- The build job was actively executing the resumable Bastard terminal tag.
- Story Runner assembly, verification, and upload were waiting behind the terminal tag.
- No blind rerun or cancellation was performed.

## Hardening completed in this pass

### Story Runner workflow
Commit `f01daa2e5b2a8d76fe9f7e963d768e17e26ef14`:
- changed workflow concurrency to `cancel-in-progress: false` so infrastructure changes cannot kill valuable production work;
- made Blender archive restoration actually prevent a redundant Blender download on cache hits;
- added Blender archive caching to the build job so the terminal-tag/build stage does not redownload the archive;
- added Bun install-cache persistence keyed by `bun.lock`;
- added pip download-cache persistence for the Python media stack;
- changed Node dependency installation to `bun install --frozen-lockfile`;
- raised the build-job timeout from 120 to 180 minutes to avoid an artificial timeout on a legitimately expensive assembly while the bounded self-healer remains the recovery backstop.

### Technical QC
Commit `d635054bd9e397ed76a68f0b85abb06d782c00eb`:
- retained the automatic `workflow_run` handoff;
- strengthened QC from only checking the final MP4 to requiring the final MP4, editorial JSON, OTIO, subjectivity render, and Bastard terminal tag;
- validates the editorial JSON is parseable and OTIO is non-empty;
- preserves the existing H.264 / 1920x1080 / 24fps / audio invariants;
- publishes a machine-readable QC pass manifest listing required artifacts.

### Local compute fallback
The existing fallback implementation was inspected and corrected in the surrounding hardening work. The fallback now has a real production path rather than a placeholder around the Bastard step: subjectivity -> Bastard terminal tag -> Story Runner -> QC. Its chunk contracts preserve the same resumable frame model used by the hosted path.

## Open-source strategy
Open source is being treated as production infrastructure, not library decoration.

- Flamenco is the immediate Blender-render-farm candidate. Current stable release is 3.9.3 and Blender describes it as free/open-source, self-hosted, cross-platform, customizable, and used in production at Blender Studio.
- OpenCue is the scale-out render/task-farm candidate for larger distributed animation/VFX workloads and future network expansion.
- OpenTimelineIO remains the interchange contract for editorial timelines and is already required by the Story Runner artifact gate.
- PySceneDetect remains the shot-detection layer and is already in the media stack.

Promotion remains evidence-gated: license review -> install/reprovision -> real EP01 input -> measured output -> failure recovery -> canonical artifact compatibility -> no regression.

## Remaining finish gates
1. Prove the active terminal tag completes successfully without restarting it.
2. Prove Story Runner build survives the previous failure point.
3. Prove final artifact verification and upload.
4. Prove automatic technical QC passes with all required artifacts.
5. Keep editorial/showrunner approval as the human greenlight gate.
6. After EP01 completion, validate the local/Flamenco compute route against a real production render rather than merely documenting it.
7. Then expand the capability matrix horizontally into animation, Blender/3D, graphics, VFX, compositing, color, sound, motion graphics, and additional show/project formats.

## Operating law
Do not restart valuable production to test an infrastructure improvement. Make completed work salvageable, checkpointed, measurable, and reusable first; then apply improvements to the next execution or recovery path.
