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
