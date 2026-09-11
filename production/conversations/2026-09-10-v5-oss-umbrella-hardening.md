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
