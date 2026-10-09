# Production Conversation Log — 2026-09-10

## User direction

The production system must stop depending on a fragile ChatGPT-to-GitHub execution path. The goal is a legitimate GitHub App + workflow_job + just-in-time ephemeral runner architecture, with durable supervision and recovery.

The immediate production objective is to harden the pipeline first, prove it with a cheap 20-second commercial test, verify the generated artifacts and recovery behavior, salvage usable Episode 1 material for the pilot, and only then return to the expensive episode run.

The user explicitly corrected “guarding commit” to **hardening** the pipeline. “Harden” means strengthening gates, recovery, telemetry, artifact validation, source transport, and runner lifecycle so failures are detected and recovered instead of hidden or allowed to consume hours.

## God Molecule / TRIPPEDD creative direction

The user wants the previously discussed God Molecule concept preserved as a future recurring TRIPPEDD segment and potentially a standalone show.

Creative references discussed:
- Osamu Sato / Eastern Mind (Tōnō)
- LSD: Dream Emulator
- Xavier: Renegade Angel
- Adult Swim / Comedy Central / MTV-style programming
- Robot Chicken / anthology / Off the Air randomness
- psychedelic, surreal, minimal, dream-logic comedy

Core production principle: AI is a co-author/co-producer and production assistant, not a replacement for the user's source material or creative judgment.

For the user's character imagery, preserve the actual supplied photographs and likeness. Apply edits/effects to the source image rather than generating a new person. Future angle work must use the user's supplied images as the identity reference.

God Molecule / Mars visual direction:
- disembodied floating head
- black/space-like background
- small sparkly stars may be used
- cobalt/indigo treatment
- solid white eyes
- forehead sigil embossed into the skin
- low-resolution, low-frame-rate, limited-palette, banded/ridged early-3D aesthetic
- palette and visual treatment should be derived from the actual reference frames rather than invented generically

## Pipeline rule

The 20-second commercial proof is the gate. Do not start another expensive episode render until the proof produces and validates its complete artifact set.

Required proof artifacts:
- MP4
- JSON
- OTIO
- QC report
- hashes/provenance

Required proof checks:
- duration
- resolution
- FPS
- audio where required
- OTIO structure
- JSON validity
- QC PASS
- artifact existence and integrity

## GitHub execution architecture

The repository is intended to use:
GitHub -> workflow_job -> TRIPPEDD supervisor -> GitHub App authentication -> JIT ephemeral runner -> production -> artifact persistence -> teardown.

This is an authorization-preserving execution architecture, not a bypass of GitHub security.

## Operational sequence

1. Harden the source transport and production gates.
2. Correct the commercial FFmpeg construction.
3. Harden attempt-isolated telemetry and watchdog behavior.
4. Validate JIT runner routing and teardown.
5. Run the 20-second commercial proof.
6. Inspect logs and artifacts.
7. Fix each real failure found.
8. Repeat until the commercial gate is PASS.
9. Salvage verified Episode 1/pilot artifacts.
10. Resume the full episode only after the proof gate is green.

This log records the production direction and decisions from this conversation so future production work can continue from the same state.
