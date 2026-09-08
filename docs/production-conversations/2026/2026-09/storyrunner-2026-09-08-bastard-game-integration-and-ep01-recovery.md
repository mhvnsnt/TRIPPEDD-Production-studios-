# Storyrunner Production Room — The Bastard / Bannon Integration + EP01 Recovery

**Date:** 2026-09-08
**Property/project:** TRIPPEDD Production Studios / The Bastard / Bannon
**Layer:** Storyrunner + production engineering
**Status:** Concept captured; EP01 recovery actively in progress
**Source:** Available conversation context; engineering actions verified against GitHub

## Storyrunner idea
The user proposed that after approximately five complete standalone episodes of **The Bastard**, the series should become a substantial addition to the **Bannon** game.

The intended structure is not simply New Game+ and not a detached conventional DLC. Inside the God Within selection area, the player should see two sibling choices:

- God Within
- The Bastard

The Bastard can be selected directly and played as a standalone experience. Separately, progression through God Within can eventually discover or connect into The Bastard so the narratives can carry information and meaning across modes.

The literal Bastard show can eventually exist inside the game as full episodes, films, cutscenes, discovered media, interstitials, and/or reconstructed in-engine sequences. The game should be capable of containing the show rather than merely referencing it.

The five-episode milestone is intentionally a creative prerequisite: enough finished Bastard material should exist to establish its identity, mythology, visual language, rhythm, and continuity before the full game integration is built.

## Action taken
Captured the concept in the Bannon repository:

`docs/design/THE-BASTARD-GOD-WITHIN-MODE-INTEGRATION.md`

Commit:
`fdd8955b49738a2c7421759ab3887d738c7b8c3b`

This is documentation only; it does not prematurely modify the game runtime.

## EP01 recovery discovery
While continuing the TRIPPEDD pilot build, the latest Showrunner run failed after the corrected open-source media stack successfully installed. The actual failure was narrower than the previous dependency problem: the production transcription wrapper was not found when invoked through PATH.

The wrapper itself exists at `scripts/bin/whisper` and is executable in intent, but the workflow's PATH activation was unreliable. The workflow was changed to validate and invoke it directly as `./scripts/bin/whisper --help`.

Both EP01 workflows were patched:

- Showrunner: `2ec7149045fb066b74ff66cb0784949468453f9`
- Autonomous: `0fc935fa301e183052c46121bca26ccd3b7e986d`

The open-source stack remains intentionally CPU-oriented and avoids the unnecessary OpenAI Whisper/Torch CUDA dependency explosion.

## Production rule
Do not call EP01 finished until the actual MP4, JSON, and OTIO outputs exist, are probed/verified, artifacts are inspectable, and the final status is accurately reported. Continue fixing the pipeline rather than describing an expected result as completed.
