# Rocket Live Session Wiring Contract

## Authority

Rocket is a cockpit over the already-running physical production runtime. This bridge does not create a second session and does not synthesize runtime state.

The bridge is fail-closed:

- missing `ROCKET_LIVE_SESSION_URL` => unavailable
- failed health/capabilities/state request => unavailable
- unsupported command => blocked
- mutation without an operation receipt, receipt object, or artifact SHA => `AWAITING_RECEIPT`
- no simulated success path exists

## Runtime surface

The default endpoint contract is:

- `GET /health`
- `GET /capabilities`
- `GET /state`
- `POST /command`

The deployed runtime may expose equivalent endpoints at different paths. Rocket supports explicit path configuration through:

- `ROCKET_LIVE_SESSION_HEALTH_PATH`
- `ROCKET_LIVE_SESSION_CAPABILITIES_PATH`
- `ROCKET_LIVE_SESSION_STATE_PATH`
- `ROCKET_LIVE_SESSION_COMMAND_PATH`

The bridge sends only the named commands:

`inspect`, `measure`, `run_gate`, `render`, `publish`, `refresh`, `checkpoint`.

## Evidence rule

A successful HTTP response is not itself authoritative evidence. A mutation becomes authoritative only when the runtime returns at least one durable proof field:

- `operationId`, or
- `receipt`, or
- `artifactSha256`.

For publish/render operations, the downstream artifact contract still requires real artifact bytes, SHA-256, reopen/inspection, validation, and remote verification before PASS.

## Deployment rule

Do not populate the live-session URL with a local development URL, mock server, browser-only state, or simulated worker. The value must identify the existing physical production runtime.

Secrets are environment-only and must never be committed to this repository.
