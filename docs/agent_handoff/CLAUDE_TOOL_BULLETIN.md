# CLAUDE / ROCKET TOOL BULLETIN

This is the persistent handoff queue for agents working on the canonical MARS character and TRIPPEDD production runtime.

## Read rule
Read this file before visual, mesh, rig, facial, hair, oral, topology, or registration work. If another agent adds a useful tool, donor, adapter, benchmark, or evidence source, update this bulletin in the same change or immediately after it.

## Canonical character law
There is ONE canonical MARS. Do not create silent competing whole-character heads or replacement characters. Component experiments must return to the canonical assembly and carry provenance.

## CANONICAL COMPONENT PRESERVATION — HARD RULE
A known-good component is an asset, not raw material. Before unrelated face work, snapshot the component's geometry, transforms, materials, shape keys, armature/weights, semantic names, and provenance. Work on a copy/branch. Change only the requested component. Compare protected components afterward and hard-stop on unexplained change.

For MARS the oral system is protected: `MARS_TEETH_UPPER`, `MARS_TEETH_LOWER`, `MARS_GUM_UPPER`, `MARS_GUM_LOWER`, `MARS_TONGUE`, `MARS_MOUTH_SOCK`, `ORAL_CAVITY`, dental-arch registration, mouth-frame data, oral collision/rig data, shape keys, and working motion. Never silently regenerate or replace these because a whole-face tool wants a simpler input. Never overwrite a known-good `.blend` in place. If a protected component changes unexpectedly, recover from the known-good donor/snapshot first rather than rebuilding from memory.

Full law: `docs/agent_handoff/CANONICAL_COMPONENT_PRESERVATION_LAW.md`.

**Hardcoded-path incident (2026-09-13):** session snippets overwrote `MARS_FACE.blend`. Caught by `checkpoint verify`; canonical restored and verifying `same`. Do not write experiment outputs to the canonical path.

## RIG PREFLIGHT
`tools/character/validate_rig_face_contract.py` — AST preflight for `blink_closure()` five-value return. Not a Blender runtime PASS.

Blink guard: judge vertices that **move**, not a median that lands on zero at the canthi. Still must fail inverted-lid regression.

## DONOR-FIRST
Before writing new geometry, cutters, remeshers, repair heuristics, rigs, facial parts, or bespoke registration code, inspect existing repository donors and approved open-source routes. Use the smallest known-good component first. Hand-roll only after a measured insufficiency is recorded.

## Critical mouth diagnosis — CONTOUR DEPTH (locked 2026-09-13)

### Retired (wrong control)
- "Boolean eats corner skin; narrowing cutter barely helped, so it isn't width."
- Control counted cells where nearest surface is cavity. Uncarved scan has **no cavity** → always scores 0. Could not demonstrate failure.
- `--slit-x` only scaled the contour rings; the cavity body remained an ellipse of half-width 36.5 mm (flare ~69.4 mm). Never a test of width.

### Measured mechanism
His inner-lip contour sweeps **11.5 mm in depth** (+4.5 mm at commissures, −7.0 mm at centre). `oral_cavity.py` lofted every ring onto a **constant y**, throwing that away. At corners, front rings sat in front of his lip line → cutter exited through cheek. At centre, rings sat 4–5 mm behind → no breach.

Same-ray, same (x,z) scan vs shipped:

| Metric | Canonical | Re-carved (contour depth) |
|--------|-----------|---------------------------|
| Cells with exterior skin gone | **44 of 483** (x −31…+28) | **4 of 483** (x −18…+17, centre) |
| Visible teeth after seam split | 5 → 72 of 240 | 9 → 88 of 240 |
| Rest leak | 538 rays | 101 of 24,321 |
| Sock corner trim | 271 faces needed | **refuses** (no longer reduces) |

35 of 44 lost cells were on the **left** — matches rest-leak asymmetry (721 left / 203 right).

Loss is a **band at the seam** (z −2…+2 mm), not a slit a min-across-column metric can see.

### Promotion gate (brutal)

```text
Candidate → mouth_proof PASS → physical proof render PASS
  → pixels reopened/inspected → SHA verified → receipt
  → only then promotion
```

Candidate path: `assets/variants/MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend`  
**NOT PROMOTED** until the gate is complete. Canonical stays untouched.

Do not re-run width/`--slit-x` as the primary fix. Do not restore radial/height skin deformation for jaw open.

## Pixel truth
Geometry/raycast ≠ pixel truth. `hide_render=True` on oral objects produced false "no teeth" pixel reads. Use `audit_mars_oral_render_visibility.py` + `render_mars_oral_pixel_truth.py`. Persist visibility with `--output-blend`.

## MARS crease/seam route
`derive_mars_lip_crease_candidates.py` scores real mesh edges; does not move vertices. Contiguous chain + pixel proof before deformation authority.

## Current MARS oral route
`CANONICAL_MARS` → `GNM_ORAL_DONOR` → oral bridge → **contour-depth carve (candidate)** → render-visibility gate → pixel-ID render → mouth_proof → SHA/receipt → promote only if green.

Tools: `oral_cavity.py`, `build_gnm_oral_donor.py`, `run_mars_oral_repair.sh`, `survey_oral_aperture.py`, `audit_mars_oral_render_visibility.py`, `render_mars_oral_pixel_truth.py`, `derive_mars_lip_crease_candidates.py`, `validate_rig_face_contract.py`, `assets/donor/gnm_oral/`.

## Current eye route — clearance active

Do **not** invent a new eyeball.

| Asset | Path |
|-------|------|
| Linework | `assets/references/mars_facial_linework/` (P0 binaries present) |
| Donor | `assets/donor/gnm_eyes/` (1926 verts, ICT-FaceKit) |
| Contract | `tools/character/eye_clearance_contract.json` |
| Ladder | `tools/character/eye_clearance_ladder.py` |
| Gate | `tools/character/eye_clearance_gate.py` (`--verify-renders`) |
| Runbook | `docs/production/EYE_CLEARANCE_RUNBOOK.md` |
| Handoff | `docs/agent_handoff/EYE_CLEARANCE_HANDOFF.md` |

Hard rules: globe-class only; rest before blink; local travel; PASS needs ladder + reopened renders + SHA. Baseline 14.24 mm centre / 0.49 mm nearest.

Export via `export_contact_geometry.py` (`OBJECT` or `OBJECT:VERTEX_GROUP`).

## Live session door

Contract: `docs/ROCKET_LIVE_SESSION.md`  
Branch: `rocket/live-session-bridge` (draft until runtime URL demonstrated).

Named commands only: `inspect` `measure` `run_gate` `render` `publish` `refresh` `checkpoint`.  
Every reply: `operationId`. Artifacts: path + sha256 + sha256Verified.  
No `ROCKET_LIVE_SESSION_URL` → unavailable/blocked. No mock fallback.

Rocket displays runtime receipts; it does not copy measurements into competing state.

## Registration route
`tools/visual_anatomy/component_registration.py` — Kabsch/Procrustes first; Open3D ICP optional refinement only.

## Approved tool families
Blender / Rigify, ICT-FaceKit, GNM oral, MediaPipe (diagnostic only), PyMeshLab, CGAL, Instant Meshes, OpenSubdiv, Open3D, libigl, existing facial-animation routes.

## Evidence law
UNKNOWN is never PASS. No artifact bytes = IMAGE_UNAVAILABLE. Visual FAIL overrides numerical PASS. Motion claims need sequences. Reopen exact PNG/MP4 + SHA-256. Geometry/raycast ≠ pixel truth.

## Current queue
1. **Oral promotion gate:** candidate contour-depth → mouth_proof → proof render → pixels + SHA → receipt → only then promote. Canonical untouched.
2. **Rocket live URL:** point `ROCKET_LIVE_SESSION_URL` at real session; prove door; keep bridge draft until demonstrated.
3. **Eye clearance ladder:** export globe-class geom → ladder → penetration_measure → gate `--verify-renders` → Shrinkwrap after rest clean.
4. **Protect oral system:** no writes to canonical path; checkpoint before experiments.
5. **Lip seam:** contiguous crease chain + pixel proof before deformation authority.
6. **Pixel truth / render visibility** for oral donor objects.
7. **Eye weld-first** after clearance baseline locked.
8. Component registration, shape-key/UV/weight preservation, deterministic QA.
9. Open-source discovery only when it improves a queue item.
