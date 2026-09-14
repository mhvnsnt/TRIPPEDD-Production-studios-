# Rocket Live Production Session Door

## Purpose

Rocket and the production agents must operate on the same physical production state. Rocket is the visual/control surface; the live production session remains the execution authority.

This bridge deliberately does **not** pretend that a ChatGPT conversation itself is an HTTP service. It exposes the existing live production runtime through a narrow, authenticated door.

## Configuration

- `ROCKET_LIVE_SESSION_URL` — base URL of the already-running production session/runtime.
- `ROCKET_LIVE_SESSION_SECRET` — optional shared secret. When configured, Rocket requires `x-rocket-live-session-secret`.

No URL means `UNAVAILABLE`; there is no local mock fallback.

## Read contract

`GET /api/rocket/live-session?target=health|capabilities|state`

The upstream runtime provides:

- `/health`
- `/capabilities`
- `/state`

`state` is authoritative only when returned successfully by the physical runtime.

## Command contract

`POST /api/rocket/live-session`

```json
{
  "command": "inspect|measure|run_gate|render|publish|refresh|checkpoint",
  "args": {}
}
```

Rocket cannot send arbitrary shell commands through this door. The command allowlist is intentionally narrow and can be expanded only as a named production capability is implemented and validated.

A successful mutation must return an `operationId`, receipt, or artifact SHA-256. Without one, Rocket reports `AWAITING_RECEIPT` rather than claiming that the operation completed authoritatively.

## Shared-state rule

The runtime is the shared source of truth. Rocket reads state from it and sends named operations back to it. Local React state is presentation/cache only and must never be promoted to authoritative production state.

The artifact pipeline remains the persistence boundary:

`OPEN → EDIT → SAVE → PREVIEW → VALIDATE → CHECKPOINT → COMMIT → PUSH → REFRESH`

## Character/model lane

For MARS, the existing bridge contract remains in force: God Molecule is the character/creative laboratory and TRIPPEDD is the executable production/evidence/QC/provenance authority. `MARS_CANONICAL` remains immutable; derived work is promoted only through executable gates and human-visible evidence.

The live door therefore lets Rocket observe and drive the same measurement, gate, render, and publish operations already used by the production agents without creating a third model stack.
