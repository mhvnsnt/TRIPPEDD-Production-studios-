# TRIPPEDD Production Conversation Log

## 2026-09-10 — Autonomous bridge + 20-second commercial proof

- User directed continuation of TRIPPEDD Production Studios work and explicitly requested that production conversation decisions be preserved.
- Clarified that the intended GitHub "bypass" is not a security bypass: it is an independent, authorized execution path that prevents production from depending on the ChatGPT GitHub connector.
- Current architecture: GitHub Actions -> workflow_job webhook -> TRIPPEDD supervisor -> GitHub App installation token -> one-job JIT runner -> production -> QC/delivery.
- Hardened `github_app/jit_runner.py` to select the correct GitHub runner architecture instead of hard-coding x64. Supported mappings: x86_64/amd64 -> x64; aarch64/arm64 -> ARM64.
- Hardened `supervisor/autonomous_supervisor.py` with repository allowlisting, required GitHub delivery IDs, malformed-payload rejection, and bounded replay protection.
- Added `scripts/production/test-autonomous-bridge.py` for offline static hardening checks.
- Added the autonomous-bridge hardening test as a mandatory preflight step in `.github/workflows/production-short-e2e-gate.yml`.
- The 20-second proof workflow remains strict: it must generate a real MP4, JSON, OTIO, QC report, hashes/provenance, and pass duration/resolution/FPS/audio/continuity checks before being considered green.
- GitHub's current documentation confirms JIT runners can execute at most one job and are automatically removed; repository JIT configuration requires repository Administration: write. 
- No episode-scale rerun should be declared successful until the 20-second proof artifact and QC evidence are actually observed.

## 2026-09-10 — Commercial/EP01 hardening pass

- User rejected the earlier commercial as insufficiently cinematic/animated and explicitly excluded Smoke & Mirrors; the commercial scope is only TRIPPEDD, In the Bushes, The Bastard, and God Molecule.
- Added a hard commercial proof gate requiring the four-show scope and explicitly rejecting Smoke & Mirrors in the commercial generator source.
- Added a dedicated motion/duration/content validation stage before the mixed-media commercial artifact is accepted.
- EP01 Story Runner run 34523231896 was observed in GitHub as pending with zero jobs/artifacts at inspection time; it is not being treated as success.
- Repository permissions through the active GitHub connector are currently real: repository reports admin/maintain/push access.
- GitHub documentation confirms queued self-hosted jobs remain queued until a matching runner is online, which is why runner routing is a production dependency rather than something to silently call green.
- Hardened commit for this pass: 533b68f8312756ca1f343a4641b0744a86258c4d.


## 2026-09-11 — God Molecule Mars reference contract + repository-generation distinction

- User supplied eight Mars/reference images: two existing blue/space Mars renders, three real multi-angle identity photographs, and three blue back/profile style renders.
- The references are now preserved in the persistent **God Molecule References** library folder, including a generated contact sheet.
- The important visual correction is explicit: Mars may be a floating head as a character concept, but the generated asset must still contain complete physical head geometry — lower jaw, back of head, and front/side/rear neck connection. A face-shaped cutout with missing bottom/back neck geometry is a hard FAIL.
- The two command classes are now separate production concepts:
  1. **Direct image generation** = the user explicitly asks ChatGPT to generate an image; direct image generation is appropriate.
  2. **Repository generation** = the user explicitly asks to use the TRIPPEDD repo/production studio/open-source stack; route through repository workers and record provenance/QC instead of silently substituting direct image generation.
- Added `production/god-molecule/MARS-REFERENCE-CONTRACT.md` defining the identity lock, generation hierarchy, provenance requirements, and FAIL conditions.
- Added `production/god-molecule/mars-reference-manifest.json` with SHA-256 identities for all eight supplied references.
- Added `scripts/production/god-molecule/prepare-reference-set.py` to verify the exact reference set before generation.
- Added `scripts/production/god-molecule/bootstrap-generative-stack.sh` for full upstream working trees: Meshroom, AliceVision, COLMAP, TRELLIS.2, ComfyUI, and Wan2.1.
- Extended the main open-source bootstrap and candidate registry with the same geometry/video generation systems.
- The intended Mars production path is now: real reference photos -> identity/reference validation -> multi-view geometry reconstruction -> reusable Blender head/neck asset -> controlled blue/sigil/style pass -> animation -> OTIO/FFmpeg delivery.
- Generative video/image systems are supporting workers around the identity anchor, not authorities over likeness.
