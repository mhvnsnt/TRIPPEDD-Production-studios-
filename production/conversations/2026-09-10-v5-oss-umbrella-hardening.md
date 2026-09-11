# Production Conversation — 2026-09-10 — V5 hardening / OSS umbrella / repo observer

## User directive
The studio is a real production studio with AI on the production team, not a fully AI-generated content farm. Mature open-source projects may be brought in as complete upstream projects and wired into the TRIPPEDD umbrella when they can be isolated, tested, and connected through explicit adapters. Do not reject full-repo integration merely because it is large. Preserve boundaries where systems should remain separate.

Current four-show network scope:
- TRIPPEDD
- THE BASTARD
- IN THE BUSHES
- GOD MOLECULE

SMOKE & MIRRORS is explicitly excluded from the network commercial.

## Commercial V5
The prior commercial generations were rejected as weak title-card/slideshow work. V5 replaces the deterministic 2D card builder with:
- real Blender Eevee 3D animation at 1920x1080 / 24fps
- four show-specific visual worlds
- 2D FFmpeg grid/noise/vignette finishing
- deterministic rhythmic 48 kHz stereo music with kick, snare/noise, hats, bass and arpeggio
- exact four-show scope and explicit Smoke & Mirrors rejection
- anti-static frame-variation QC
- exact 1920x1080 delivery QC

The commercial remains a production proof: source -> analysis -> editorial -> render -> QC -> artifact validation.

## OSS umbrella
Added `open-source/OSS-UMBRELLA.yml` and `scripts/production/install-oss-umbrella.sh`.

The umbrella currently targets:
- ComfyUI for graph-based AI-assisted image/video/3D/audio workflows
- OpenCue for scalable render/job dispatch
- OpenAssetIO for asset identity/interchange
- OpenColorIO for color management
- Kdenlive/MLT as an editorial fallback/integration target

These are complete upstream projects fetched into `.trippedd/oss` by the installer rather than copied into the application source tree. Integration is adapter-based.

## Repo eyes
Added a read-only `repo-observer.py` and scheduled `studio-repo-observer.yml`. It inventories the repository head/status, active/recent Actions runs, open PRs/issues, and the production workflow contract into a durable JSON artifact.

## Hardening
The commercial proof gate now requires exactly 1920x1080 and 24fps, rather than merely accepting 1280x720-or-better.

## Connector
The GitHub connector is currently operational for this repository. Authenticated profile is `mhvnsnt`, and the repo reports admin/maintain/push permissions. No fake connector result is to be claimed.

## Branch
`hardening/v5-mixed-media-commercial-oss-umbrella-2026-09-10`

## Commits on this branch
- `2f9efc568857f0fc3ca9c435fe2e931b743cbd1d` — add Blender 3D ident renderer
- `8d90c44db472394a62983138c962e7ae4c0dcc0d` — harden commercial builder with 3D animation and authored audio
- `0c29256c2058553c54092eacb00f33a258892fa2` — add OSS umbrella manifest
- `5b91554345fa5869ff89378aa0413c5be65ba872` — add full-repo OSS installer
- `c1ed7f3be5205b7c253fca29d1e0b9d28ff70c20` — add read-only repo observer
- `4b14c79e6f794cae856724d2cf75eeb4ac8d7071` — add scheduled repo observer
- `7e3e22c8faf9805318eb76cdc3a5fec9f9490da9` — require exact 1920x1080 commercial QC
- `b24a0dd044183cba651a7e8331783b3382126e31` — lock V5 ident quality floor


## Continuation — persistent toolchain / episode throughput hardening

### User directive
Do not reinstall and re-verify Blender from scratch on every run. Keep the production machine warm through GitHub Actions caches and continue adding open-source infrastructure only where it directly helps finish the episodes.

### Changes made
- EP01 Autonomous: Blender 4.5.13 is now cached as an extracted toolchain under the runner user's cache. Warm runs activate the cached binary instead of downloading, checksum-verifying, and untarring Blender again.
- EP01 Autonomous: Bun/Python dependency caches now include the production requirements lock surface and restore prior compatible cache entries.
- EP01 Story Runner: same extracted Blender cache strategy and expanded dependency cache key.
- V5 Commercial Proof: same extracted Blender cache strategy.
- Production Short E2E Gate: caches the complete upstream OSS render backend working trees and skips the bootstrap clone step when the cache is warm.
- The production path still performs cheap executable/importability verification after activation; expensive download/checksum/extraction work is cold-cache only.

### Cache policy
GitHub Actions cache is treated as a performance layer, not as proof of integrity. Cold cache performs the normal acquisition/verification path; warm cache activates the exact keyed toolchain and the production verification gate still checks executability/importability. Cache keys are revisioned so intentional stack changes can invalidate them.

### Current production objective
Commercial proof -> EP01 Story Runner -> EP01 Autonomous, with salvage/checkpoints and bounded self-healing preserved. Do not expand the OSS umbrella unless a project removes a measured production bottleneck.


### Continuation 2 — E2E warm-path optimization
- Production Short E2E Gate now persists the pip download cache keyed to `config/production/oss-stack.requirements.txt`.
- Kept system-package installation explicit rather than pretending an Actions cache of `/usr` is portable or reliable. The optimization boundary is therefore: reusable downloads + Python wheels + Blender + OSS source trees; apt installation remains a cheap provisioning step.
- Next optimization should be based on measured warm-run timing rather than speculative repository additions.


## Continuation 3 — new show concept: VR Desolation

### User concept
The user wants the production conversation to preserve a new show/segment concept provisionally titled **VR Desolation**. The title is intentionally provisional and can change.

Core tonal/concept mix:
- post-apocalyptic Fallout-style survival world
- Sword Art Online-style trapped-in-an-RPG premise
- VR-game framing
- Code Monkeys-style workplace/programmer comedy
- Code Lyoko-style digital/real-world crossover energy
- Mad Max-style desolate survival atmosphere

The intended result is a **comedic survival series** in which characters become stuck inside a dangerous post-apocalyptic RPG/VR world and have to survive, exploit the game systems, deal with bugs/logic, and interact with the absurdity of being trapped in a game.

### Production direction
Keep developing this as a possible TRIPPEDD Studio show/segment while the immediate production priority remains:
**commercials + episodes + cuts delivered through the production pipeline.**

Open-source additions should continue to be selected by production value: game/VR worldbuilding, procedural environments, animation, rendering, compositing, editorial, audio, asset management, and automation are all candidates when they directly remove a bottleneck or enable an actual episode.

Do not lock the provisional title, lore, characters, or exact mechanics yet. Preserve the concept and develop it alongside production throughput.


### Continuation 4 — cold-cache safety correction
A review of the warm-cache changes found an important failure mode: replacing the old Blender installer outright would make a genuinely cold cache fail because the extracted directory did not yet exist. Corrected EP01 Autonomous, EP01 Story Runner, and V5 Commercial Proof so each workflow has a bounded cold-cache bootstrap that downloads/checksums/extracts Blender only when the extracted executable is absent. Warm runs still skip that expensive path. This preserves the original safety contract while achieving the intended persistent-cache behavior.


### Continuation 5 — production priority directive
User directed that this work remain centered on the production-studios repository and that the pipeline must keep moving actual deliverables: the commercial, EP01 story-runner cut, EP01 autonomous cut, and their editorial cuts. Open-source integrations should continue to be pulled into the production repository in full when they are usable production components, while avoiding speculative additions that don't advance a deliverable.

Repository note: GitHub account search did not expose a repository literally named “Church Production Studios”; the connected production repository available and actively running this pipeline is **mhvnsnt/TRIPPEDD-Production-studios-**. Work is therefore continuing there rather than inventing or switching to an unverified repository.


### Continuation 6 — full upstream OSS checkout policy
The OSS umbrella installer was tightened to match the production directive literally: upstream projects are now cloned without blob filtering and without shallow fetches. The repository therefore vendors complete upstream Git histories when the umbrella is materialized, while Actions caches prevent repeating that expensive operation on warm runs. This is deliberate: “full” means complete upstream source/history, not a lightweight placeholder checkout.
