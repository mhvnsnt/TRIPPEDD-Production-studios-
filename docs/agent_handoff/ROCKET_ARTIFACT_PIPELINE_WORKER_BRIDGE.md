# Rocket Artifact Pipeline → Physical Worker Bridge

Rocket's Artifact Pipeline is a client of the already-running physical production session. It must not create a second model/runtime or promote UI state as production truth.

## Endpoint

`POST /api/rocket/artifact-pipeline`

The route requires:

- `ROCKET_LIVE_SESSION_URL`
- optional `ROCKET_LIVE_SESSION_SECRET`
- `operationId`
- `editor`
- `artifactPath`
- `artifactSha256`

Optional provenance is carried through as `repo`, `branch`, `baseSha`, `operation`, `validation`, and `checkpoint`.

## Worker command

The Rocket route translates the receipt into the existing live-session command contract:

```json
{
  "command": "publish",
  "args": {
    "operationId": "...",
    "repo": "...",
    "branch": "...",
    "baseSha": "...",
    "editor": "...",
    "operation": "...",
    "artifactPath": "...",
    "artifactSha256": "...",
    "validation": {},
    "checkpoint": {},
    "source": "rocket-artifact-pipeline"
  }
}
```

The worker/session remains responsible for actually publishing the bytes. Rocket marks the operation authoritative only when the physical runtime returns an operation ID plus a receipt, artifact SHA, or commit SHA.

## Why this matters

The current physical Blender lane is a GitHub Actions evidence worker rather than an HTTP service. Its workflow installs Blender, retrieves the production assets, executes the creative shot, reopens rendered bytes, and packages/upload evidence. Rocket therefore does **not** pretend that workflow dispatch itself is a local HTTP renderer. The live-session URL is the transport boundary for the already-running runtime.

This preserves one shared state:

`ChatGPT / agents → physical runtime ← Rocket ← human owner`

and one persistence boundary:

`OPEN → EDIT → SAVE → PREVIEW → VALIDATE → CHECKPOINT → COMMIT → PUSH → REFRESH`.
