# Production Conversation — 2026-09-21 — Bush Transformation Correction

## Showrunner correction

The visual storyboard was repeatedly depicting the beer can as if it were becoming animated. The showrunner clarified the intended canon:

> The can does not come to life. The bush does.

## Canon locked

- Beer cans remain ordinary, inanimate props.
- Beer is the catalyst that reaches the bush.
- The bush itself reacts first: stillness → twitch → shudder → compression/rebound → supernatural pulse.
- The foliage is the animated subject during S09.
- Busch emerges from that transformed bush in S10.
- The cans remain ordinary objects on the ground afterward.
- No anthropomorphic beer-can face, body, personality, or character animation belongs in the origin sequence.

## Technical correction

The active origin builder previously used the entire generic beer throw kit as a repeated layer. That kit contains a six-pack, loose cans, and spill artwork on one canvas, which made prop staging ambiguous and could make the storyboard/render read incorrectly.

The production pass now splits the prop kit into:
- `generic-six-pack.svg`
- `generic-can.svg`
- `generic-beer-spill.svg`

A foliage-only transformation asset was added:
- `busch/busch-transform.svg`

The active builder now uses the foliage-only transformation state during S09 and reserves the Busch character asset for the wake/reveal phase.

## Continuity rule

**Beer causes the bush to become Busch. Beer does not become Busch.**

## Verification added

Render-source tests now check that:
- the legacy combined beer kit is not used by the active builder;
- the foliage-only transformation asset is present;
- the transformation asset contains no face/can character treatment;
- focused ordinary beer prop assets parse as valid SVG.

