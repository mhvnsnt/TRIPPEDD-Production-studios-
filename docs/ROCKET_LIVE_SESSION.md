# Rocket Live Session Door — contract

Rocket is a **control / observation surface**, not the production runtime.

Authority lives only in the physical session that answers this contract.

## Endpoint

Set:

```text
ROCKET_LIVE_SESSION_URL=<base URL of the running physical session>
```

Do not invent hostnames. Do not fall back to a local mock.

## Required routes

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET | `/capabilities` | Named commands this session supports |
| GET | `/state` | Authoritative session state (poll ~3s) |
| POST | `/command` | Execute a **named** command only |

## Named commands (no arbitrary shell)

| Command | Role |
|---------|------|
| `inspect` | Read scene / object / part inventory |
| `measure` | Run a measurement tool; return receipt |
| `run_gate` | Run a fail-closed gate; return gate result |
| `render` | Render; reopen bytes; report `sha256` |
| `publish` | Publish artifact through named path + hash |
| `refresh` | Refresh authoritative state |
| `checkpoint` | Snapshot / verify checkpoint |

Every reply **must** include:

- `operationId`
- for artifacts: path + `sha256` + `sha256Verified` / `hashAgrees` when re-hashed on the runtime

If any of those are missing, Rocket must treat the result as **NON-AUTHORITATIVE**.

Synthetic UI / State Bus demo events are **not** production truth. Session Health must poll real `/health`. Disconnect/degraded state comes from actual health responses, not timers.

## Mapped production tools (examples)

### measure

| Intent | Tool |
|--------|------|
| Eye clearance ladder skeleton | `tools/character/eye_clearance_ladder.py` |
| Penetration (globe-class pairs) | `tools/character/penetration_measure.py` |
| Lip seam + drop bridges | `tools/character/run_lip_seam_drop_bridges.sh` → `split_lip_seam.py --drop-bridges` |
| Oral / crater cell counts | existing oral survey gates on the session |

### run_gate

| Intent | Tool |
|--------|------|
| Eye clearance filled receipt | `tools/character/eye_clearance_gate.py` (`--verify-renders`) |
| Lip seam bridges dropped | `tools/character/lip_seam_bridge_gate.py` |
| Contact / penetration BLOCK | `tools/character/contact_gate.py` |
| Linework eye authority | `tools/character/linework_eye_authority_gate.py` |
| Blink regression | `tools/character/blink_regression_gate.py` |
| Oral render visibility | `tools/character/audit_mars_oral_render_visibility.py` |

### render / publish

Reopen exact PNG/MP4 bytes on the runtime. Record SHA-256. UI state is never evidence. **Pixels veto:** numerical/gate PASS cannot promote when proof pixels fail.

## Fail-closed rules for the door

- UNKNOWN is never PASS
- No artifact bytes = IMAGE_UNAVAILABLE
- Missing implementation = NOT_IMPLEMENTED
- Visual FAIL overrides numerical PASS
- Rocket must not fabricate Blender execution, hashes, or PASS while the runtime is unavailable

## Eye clearance (parallel track)

Contract: `tools/character/eye_clearance_contract.json`  
Runbook: `docs/production/EYE_CLEARANCE_RUNBOOK.md`  
Handoff: `docs/agent_handoff/EYE_CLEARANCE_HANDOFF.md`

Flow: export geom (eyes present, globe-class) → ladder → penetration_measure → fill receipt → renders + SHA → `eye_clearance_gate.py`.

## Oral: contour depth + drop bridges

- Contour-depth candidate only: `assets/variants/MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend`
- Shards: `tools/character/run_lip_seam_drop_bridges.sh` (review-out default; never canonical by default)
- Detail: `docs/agent_handoff/LIP_SEAM_DROP_BRIDGES.md`
- Not promoted until mouth_proof + pixels + SHA. Canonical untouched.

## Bannon transfer

Same door pattern later for Bannon builds:

```text
command → physical runtime → operationId → real artifact + SHA → QC → only then PASS
```

No second imitation of game state. No greenlight without reopened bytes.
