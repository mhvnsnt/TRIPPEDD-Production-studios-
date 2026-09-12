# TRIPPEDD Production Conversation — 2026-09-10

## Commercial revision request
User reviewed the first 20-second network proof and correctly rejected it as a finished commercial: it was effectively a still title card with a low hum. The technical proof demonstrated file generation, but it did not demonstrate the intended creative production quality.

Creative requirement now locked:
- The network commercial must be an actual moving mixed-media ident, not a still.
- It should feel co-authored: user-authored TRIPPEDD identity/themes plus procedural/AI-assisted production rather than generic AI slop.
- It should combine 2D/3D/procedural motion language, psychedelic/Adult Swim-style title-card energy, and show-specific themes.
- TRIPPEDD branding must be visually present throughout.
- The proof must contain meaningful motion and a real musical/audio bed.
- A technical gate must reject a static image and near-silent audio.

## Implementation
Added:
- `scripts/production/build-network-commercial.py`
- Four 5-second moving visual worlds representing the current TRIPPEDD creative identities used for the network ident: THE BASTARD, GOD MOLECULE, SMOKE & MIRRORS, and TRIPPEDD NETWORK.
- Animated geometric planes, grids, grain, moving wordmark, show titles, palette changes, and a procedural electronic bed.
- Deterministic 20s / 1280x720 / 24fps / AAC output.

Hardened:
- `.github/workflows/production-short-e2e-gate.yml` now builds the creative commercial after the deterministic source proof.
- Added anti-still QC using sampled frame hashes; fewer than 8 unique sampled frames fails the gate.
- Added audio loudness QC; an excessively quiet/hum-only result fails.
- Added creative commercial artifact upload: `TRIPPEDD-NETWORK-COMMERCIAL-MIXED-MEDIA`.

## Commits
- `cf76b082bb4dc16f4e4fa88132221842b1d34b09` — added kinetic commercial builder.
- `98766d69315daf5a1bd0cb458f454495557dcb47` — hardened the proof workflow against still-frame/silent output.

## EP01 naming requirement
Keep these as separate deliverables:
- EP01 Autonomous Cut
- EP01 Story Runner Cut
- EP01 Pilot Master (promotion target only after comparison/QC)
Do not collapse the two cuts into one generic EP01 artifact.
