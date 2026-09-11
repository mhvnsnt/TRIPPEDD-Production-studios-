# God Molecule — Oral Anatomy / Facial Animation Direction

Date: 2026-09-11

## Problem
MARS_CANONICAL is a closed-mouth scan. A jaw bone or blendshape cannot reveal anatomy that is absent from the source geometry. The current render moves the outer lips incorrectly while never producing a real oral opening.

## Decision
Do not hand-model every facial expression and do not replace the Mars identity with a generic head.

Use Google GNM Head v3 as the open-source anatomical donor (Apache-2.0), with GNM-Studio as the constrained identity-fit/runtime reference.

## Identity rule
MARS_CANONICAL remains immutable and is the exterior likeness source of truth. GNM is restricted to oral anatomy, mouth/lip deformation, jaw-open behavior, tongue/teeth motion and expression retargeting where the scan lacks anatomy.

## Production path
MARS_CANONICAL → front/three-quarter reference renders → GNM-Studio constrained identity fit → measured mouth/lip correspondence → GNM oral/lip patch → align to measured Mars mouth landmarks → expression/jaw retarget → Rhubarb phoneme timing → independent blink/gaze → objective QC.

## Required gates
jaw_open creates a visible inner-mouth gap; lower teeth move with the jaw while upper teeth stay anchored; tongue stays bounded; MM closes; AA/OH opens; EE spreads; FF reaches upper teeth; both eyelids close; vertex/pixel travel is measured; Mars source hash remains unchanged; UNKNOWN is never PASS.

## Open-source policy
Do not add another generic face generator for this problem. Prove GNM first.