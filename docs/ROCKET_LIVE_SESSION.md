# THE LIVE PRODUCTION DOOR — point `ROCKET_LIVE_SESSION_URL` here

> *"make it so Rocket can do everything you're doing, but so I can see it while it's
> happening ... and we all can be an actual production team and get this going faster."*
> — the owner, 2026-09-13

Rocket's PR #64 built the cockpit half against a fixed interface: `/health`,
`/capabilities`, `/state`, and a closed set of **named commands** with no arbitrary shell.
This is the runtime half, and it answers **those names** — so nobody has to guess an
endpoint or invent a mapping layer.

```
ChatGPT / agents  ─┐
Claude ───────────┼──►  ONE live Blender session  ◄──  Rocket  ◄──  the owner
Rocket ───────────┘        (tools/session/start.sh)
```

There is exactly one scene. Rocket is not looking at a copy, a simulation or React state.

## Start it

```bash
bash tools/session/start.sh assets/rigs/MARS_FACE.blend        # 4.0 s, stays open
./.trippedd_venv/bin/python tools/session/worker_http.py --port 8788
# then, in Rocket:  ROCKET_LIVE_SESSION_URL=http://<host>:8788
```

**Auth.** Set `TRIPPEDD_SESSION_SECRET` and every request must carry
`Authorization: Bearer <secret>` or `X-Trippedd-Secret`. With no secret the worker binds
`127.0.0.1` only and `/capabilities` says `"authRequired": false` — it never claims to be
authenticated when it is not. `/capabilities` is deliberately readable without the secret,
so a cockpit can discover that it needs one. The comparison is `hmac.compare_digest`,
because `==` on a shared secret leaks its prefix.

## Endpoints

| verb | path | what it is |
|---|---|---|
| GET | `/health`, `/state` | the authoritative live scene — blend path + **its sha256**, Blender version, every mesh with verts/faces/shape-keys/`hideRender`. Cached 1 s, because Rocket polls at 3 s and several clients may watch one Blender main thread. |
| GET | `/capabilities` | the command list, each command's params, which are privileged, the gate and measurement whitelists, `arbitraryShell: false` |
| GET | `/evidence`, `/evidence/index` | `LATEST_VISUAL_EVIDENCE.json` / the append-only `VISUAL_EVIDENCE_INDEX.json` |
| GET | `/checkpoints` | what can be rolled back to |
| GET | `/snippets` | the banked session snippets |
| POST | `/command` | `{"command": ..., "params": {...}}` — the only door Rocket needs |
| POST | `/exec`, `/snippet` | **privileged**: raw python in the live session. Claude uses these. |
| POST | `/render` | kept as shorthand for `command: "render"` |

## The named commands

| command | session? | what it does |
|---|---|---|
| `refresh` | yes | re-read the live state, bypassing the 1 s cache |
| `inspect` | yes | LEVEL 0 — counts, transforms, materials, modifiers, vertex groups, shape keys, visibility. No render, no relaunch. `{"object": "MARS_MESH"}` |
| `measure` | yes | a **banked measurement, by name**, run inside the live session. `rest_gap` returns in **0.197 s**. |
| `run_gate` | no | one of the repo's **own** gates — `mouth_proof`, `contact_gate`, `expression_gate`, `blink_regression`, `mars_face_invariant`, `visual_evidence`, and the mouth-crater measurements `skin_ab`, `cutter_breach`, `carve_prediction` |
| `render` | yes | render in the live session **and publish** — returns the artifact path and its sha256 |
| `publish` | no | publish bytes that already exist through `tools/publish_visual.py` |
| `checkpoint` | no | `save` / `list` / `verify` |

**`checkpoint restore` is deliberately NOT reachable over HTTP.** Rolling the canonical rig
back is destructive and stays a deliberate `--yes` command at a terminal — OWNER LAW #12,
nothing recovered by accident.

## What makes a reply authoritative

Rocket's own rule and this repo's rule are the same rule, so the worker enforces it:

- Every reply carries `operationId` (and `op`, the same id).
- **Reads** are authoritative because the live session answered them.
- **A mutation is authoritative only when it returns a receipt whose bytes exist and
  hash.** `render` and `publish` parse the artifact line out of `publish_visual.py`, then
  **re-hash the file here** and report `sha256Verified` and `hashAgrees`. A receipt that
  only repeats what the producer said is not independent.
- No bytes → `"authoritative": false` with `status: BLOCKED` and the reason. Never a
  fabricated success. (OWNER LAW #9 — NO BYTES = NO EVIDENCE.)
- No live Blender → `503` with `"session": false` and the command to start one. That is
  `UNAVAILABLE`, and it is not `FAIL` — `NOT_ATTEMPTED` and `FAILED` stay distinct.
- A gate that exits non-zero is a real **verdict** (`"verdict": "FAIL"`), and it is
  authoritative — the gate ran. That is not the same as the worker erroring.

## Why the command list is closed

`measure` and `run_gate` take a **name from a whitelist**, never a path or a command line.
A command that accepted a path would be an arbitrary shell wearing a different hat, and
Rocket's contract says there isn't one. Anything not on the list comes back `BLOCKED` with
the available names, so a caller is never left guessing:

```json
{"authoritative": false, "status": "BLOCKED",
 "why": "'rm -rf' is not a named measurement",
 "available": ["oral_export", "rest_gap", "tooth_occlusion", ...]}
```

`/exec` and `/snippet` are the exception and are marked `privileged` in `/capabilities`.
They exist because Claude drives the model through them; a cockpit does not need them.

## Verified, on this container

```
GET  /health                      blend + sha256 + 7 meshes, Blender 4.2.1 LTS
POST /command inspect MARS_MESH   27,865 verts · 54,720 faces · 89 keys · 11 groups
POST /command measure rest_gap    0.197 s, in-session, authoritative
POST /command run_gate skin_ab    1.371 s, PASS, "44 of 483 cells" straight out
                                  of the runtime -- a cockpit reads the crater
                                  number itself instead of being told it
POST /command measure "rm -rf"    BLOCKED, with the whitelist
POST /command shell               BLOCKED, with the command list
```

### A gate that imports `bpy` cannot run under the venv python
`mouth_proof.py` is a Blender script. Handing it to `.trippedd_venv/bin/python` is an
instant `ModuleNotFoundError`, and a cockpit would read that as "the gate failed" rather
than "the worker ran it wrong". Each gate declares its interpreter. And for a Blender
gate the exit code is not the verdict: **`blender -b` exits 0 after a script exception**
— the `rig_face.py` crash that printed a whole healthy report and wrote nothing — so a
traceback in the output is reported as `FAILED_RUN`, never as a pass.

### A worker that is already running answers with the OLD code
Restarting this worker after editing it is not optional. The first restart attempt died on
`EADDRINUSE`, printed into a log, and the port kept answering — with the previous build, so
a fix that had never executed looked like it was working. That is the exact failure already
written down in `CLAUDE.md`. **Find the listener by PORT, never by matching a command line**
(`pkill -f worker_http.py` matches the shell running the pkill and kills it):

```bash
fuser -k 8788/tcp          # or: lsof -ti:8788 | xargs kill
```
