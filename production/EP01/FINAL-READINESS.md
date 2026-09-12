# EP01 Final Readiness

This file is the operational gate checklist for the real pilot master.

## Required gates

- [ ] Real source assembly exists and is playable.
- [ ] Generated subjectivity sequence is rendered from `production/EP01/generated/blender/build_subjectivity.py` and approved for editorial use.
- [ ] `EDITORIAL-LOCK.json` exists and contains the exact locked media sequence, including the generated subjectivity asset where approved.
- [ ] `QC-PASS.json` exists and records successful technical/editorial QC.
- [ ] `SHOWRUNNER-GREENLIGHT.json` exists and records explicit final approval.
- [ ] `EP01-FINAL.mp4` is rendered and probe-verified.

## Canonical ending

The pilot ends on the lost-acid button. The disappearance is not solved. Nothing follows the terminal button.

## Provenance rule

Generated material is editorial/subjective material. It must never be represented as physical source evidence. The source timeline remains authoritative for what physically happened.

## Important

Do not create gate JSON files merely to make the build pass. Each gate represents a real production decision or verification. The final-master renderer intentionally blocks until these gates exist.
