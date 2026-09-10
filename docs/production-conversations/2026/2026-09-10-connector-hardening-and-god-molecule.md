# 2026-09-10 — Connector-independent execution hardening + God Molecule context

## Record type

**Reconstructed production-room record.** This entry preserves the material context available in the current conversation; it is not presented as a verbatim transcript.

## Production infrastructure

The showrunner repeatedly directed the production system to stop depending on a broken/disabled ChatGPT↔GitHub execution path and to continue doing real repository work.

The production architecture was clarified as a legitimate **connector-independent execution bridge**, not a security bypass:

- GitHub workflow queues a production job.
- A TRIPPEDD supervisor receives the authenticated `workflow_job` webhook.
- The supervisor verifies HMAC-SHA256, deduplicates GitHub delivery IDs, enforces the allowed repository, and checks the production runner label.
- A GitHub App installation access token is obtained for the authorized repository.
- GitHub's JIT runner endpoint provisions a one-job ephemeral runner.
- Production executes on that runner.
- Artifacts, QC, provenance, and diagnostics remain in GitHub independently of the ChatGPT session.

## Hardening completed

The JIT bridge was hardened so that:

1. `TRIPPEDD_ALLOWED_REPOSITORY` is mandatory and fails closed when absent.
2. The GitHub App private key must exist and be owner-only readable.
3. The runner installation must contain an executable `run.sh`.
4. The JIT configuration is passed directly to the runner and is not persisted to disk.
5. Installation access tokens remain scoped to the target repository.
6. The short commercial gate now calls the hardened connector-independent bridge contract.
7. A new production document records the boundary and security rules.

GitHub's current documentation confirms repository-level JIT runner configuration through the REST API and requires repository Administration: write permission for the authenticated GitHub App installation. JIT runners are intended for one-job ephemeral execution.

## 20-second commercial proof

The first gate triggered by the bridge-test addition failed immediately at the old static hardening check because the JIT source had intentionally been strengthened and the old test expected its previous source shape.

That failure was useful and was not allowed to become a production/render failure.

The gate was corrected to use the new hardened contract. New gate run:

**34517270493 — Production Short E2E Gate**

Current observed state:

- bridge hardening check: PASS
- runner preflight: PASS
- setup Bun: IN PROGRESS
- media/render stack: pending
- commercial generation: pending
- editorial assembly: pending
- QC: pending
- artifact upload: pending

This run is therefore the current 20-second proof attempt after hardening.

## EP01 status at the same time

The real EP01 Story Runner remains separate and was not restarted.

Run **34515641641** remains the active production run at the time of this record. Its source transport preflight succeeded and its build job reached the source-driven EP01 build step. No blind restart was performed.

## God Molecule / TRIPPEDD creative context

The production-room discussion established **God Molecule** as the working title for a recurring TRIPPEDD segment and potential standalone series.

Creative DNA discussed:

- Osamu Sato's *Eastern Mind: The Lost Souls of Tong-Nou* / `東脳`
- *LSD: Dream Emulator*
- *Xavier: Renegade Angel*
- psychedelic/stony comedy
- early CD-ROM / low-poly / pre-rendered CG
- dream logic, discontinuity, spiritual symbolism, and deadpan absurdity
- TRIPPEDD's broader anthology/randomness language

The segment is intended to be **AI co-authored/co-produced rather than fully AI-generated**: the showrunner owns the source material, likeness, voice, taste, music, and final editorial choice; AI assists with analysis, asset preparation, motion/texture variants, transcription, scripts, and production automation.

### Mars character

Mars is the lead character concept for God Molecule.

The approved design direction is a **disembodied floating head**, derived from the showrunner's actual supplied photographs rather than generating a replacement person:

- preserve the exact facial likeness and head shape from the source photograph
- preserve dreadlocks and beard
- deep cobalt/blue treatment with controlled violet/indigo shadows
- solid white eyes
- the God Molecule forehead sigil embossed/raised into the skin
- black/void background
- small multicolor sparkling stars
- low-resolution, low-frame-rate, early-90s pre-rendered CG language
- palette/banding/dithering applied as a post-process to unify the look

**Critical image-generation rule:** future Mars imagery must be edits/effects applied to the supplied photographs. Do not synthesize a new-looking person or substitute another face. When multiple source photos are supplied for different angles, use those actual angle photographs as the corresponding source images rather than inventing new camera angles or facial geometry.

### God Molecule visual system

The intended production language includes:

- 8–16 color palette derived from real reference frames
- hard/banded lighting
- colored lights rather than realistic white lighting
- flat shading
- low polygon counts
- warped textures
- intentional vertex/visual jitter
- 12–15 fps target for the degraded aesthetic
- approximately 640×480 internal/render language for the retro layer
- 256-color/pixel-grid/dither finishing
- Blender + FFmpeg + open-source image/video tooling
- optional 3D head later from a real multi-angle photo set

The earlier supplied shader/look is treated as a production tool reference, but palette values should ultimately be sampled from actual reference frames.

## Source-chronology / authorship rule

The studio's existing distinction remains active:

- physical source chronology
- editorial chronology
- story canon
- series canon
- autonomous discoveries
- showrunner decisions

The production archive should preserve this distinction rather than flattening it.

## Next production objective

Do not spend another long EP01 render window until the hardened short commercial gate proves the full ingest → analysis → editorial → render → QC → delivery path.

If the short gate passes, use that verified path as evidence for the next EP01 production step.

