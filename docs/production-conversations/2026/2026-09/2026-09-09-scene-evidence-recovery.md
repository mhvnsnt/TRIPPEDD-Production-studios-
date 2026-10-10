# 2026-09-09 — Scene-evidence recovery

## Producer direction

Continue upgrading the production stack, pull in open-source capabilities where they materially improve the studio, and finish EP01 without wasting completed work.

## Failure found from real logs

Canonical Story Runner run `34394290662` reached the build stage with all 12 subjectivity chunks, subjectivity assembly, and Bastard terminal tag complete. The Bastard action restored all 12 cached chunks (144/144 frames) and assembled `ep01_bastard_tag.mp4` successfully at 393,498 bytes.

The actual failure was later in `bun run pilot:build:public`: analysis reported `19/19` source jobs usable, but comedy discovery returned zero candidates, so the renderer correctly emitted `WAITING_FOR_EVIDENCE` and exited 2. The problem was not a render failure and not missing source media; the editorial evidence layer had no transcript-derived gag candidates.

## Recovery

`src/server/comedyDiscovery.ts` now preserves PySceneDetect shot-boundary ranges as explicitly low-confidence `MACHINE_SUGGESTED` scene evidence when transcript-derived discovery is empty. These candidates are labelled as scene evidence and never represented as transcript-derived comedy claims.

This preserves the physical source timeline and gives the Story Runner a source-grounded rough assembly path even when Whisper produces no usable segments. Human editorial greenlight remains downstream.

The EP01 production kickoff marker was advanced to commit `823c9aad53e57b2c99f3d73a35d660c616806bf4` so the next canonical run checks out the recovery code on current `main`, rather than replaying the failed run's old commit.

## Open-source / stack direction

Continue evaluating self-hosted GitHub Actions runners and ARC runner scale sets as the compute escape hatch when hosted Actions capacity becomes the constraint. GitHub documents self-hosted runners and ARC scale sets as supported autoscaling paths. Keep Flamenco 3.9.3 as the stable Blender render-farm target and keep promotion evidence-gated.

## Operating law

Do not confuse `19/19 source jobs usable` with `19/19 editorial selects found`. Technical analysis success must not strand production when one evidence modality is empty; the pipeline should degrade to another measured evidence modality without inventing facts.
