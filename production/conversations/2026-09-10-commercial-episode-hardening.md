# Production Conversation — 2026-09-10

User directed continuation of TRIPPEDD production hardening.

## Creative correction
The existing 20-second network commercial was judged insufficient because it behaved too much like a static title card. The requested commercial is a genuinely moving mixed-media ident: partially AI/co-authored, grounded in the four existing TRIPPEDD shows, incorporating TRIPPEDD branding, with animation/motion, music/SFX, and surreal psychedelic/Adult-Swim/Robot-Chicken energy. A successful technical MP4 alone is not sufficient proof.

## EP01 deliverables
Keep these distinct and independently QC'd:
- EP01 Autonomous Cut
- EP01 Story Runner Cut
- EP01 Pilot Master / salvage package

Existing EP01 material must remain salvageable and reusable.

## Hardening requirement
The 20-second E2E gate must exercise the actual creative commercial path rather than using a deterministic black/title-card source as the sole proof. QC must reject a static-image masquerading as video and must verify duration, resolution, FPS, frame activity/scene variation, non-silent audio, MP4 integrity, JSON/OTIO/provenance artifacts, and final QC PASS.

## Connector reality
GitHub repository access is currently available for repository operations, but some discovery/execution operations have timed out or are not exposed. Do not claim a commit/run occurred unless the tool returns a real GitHub result.

## Current commercial builder
scripts/production/build-network-commercial.py is the active deterministic mixed-media commercial builder. It currently contains four five-second visual segments for THE BASTARD, GOD MOLECULE, SMOKE & MIRRORS, and TRIPPEDD, with moving geometric overlays, scanlines/grain/palette treatment, TRIPPEDD wordmark, and generated audio. It is a stronger baseline than the former static proof but must be integrated into the real E2E gate and improved toward authored mixed-media animation.

## Working principle
AI is a co-author/tool, not a replacement for the user's source material or taste. Preserve authorship, source evidence, checkpoints, artifacts, and measurable QC.
