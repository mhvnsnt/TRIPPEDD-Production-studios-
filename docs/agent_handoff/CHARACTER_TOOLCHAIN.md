# MARS character toolchain (registry pointer)

**Authoritative draft contract:** PR #65 — `config/mars-character-toolchain.json`  
Commit on branch: `d4694570b3f52c7199fdb4140956a42da8fae3bb`  
**Status: draft / unmerged.** Not “working” until physical execution + receipts exist per lane.

## Principle

Strongest existing donor/tool per layer. Preserve prior artifacts. Promote only from physical evidence. Pixels veto geometry. UNKNOWN ≠ PASS.

## Status classes (do not collapse)

| Status | Meaning |
|--------|--------|
| `approved` | In production use on this repo |
| `canonical` | Authority for that subsystem (e.g. GNM oral) |
| `approved_candidate` / `candidate_for_physical_validation` | May be wired; **not** proven on MARS yet |
| physical validation pending | No live worker receipt for that tool against MARS |

## Oral exception (non-negotiable)

Generic face/retopo tools **do not** replace the GNM oral chain:

```text
GNM donor → run_mars_oral_repair.sh → visibility → pixel-ID → aperture survey
  → --drop-bridges only if measured residual
  → proof render → SHA → promotion
```

See `docs/agent_handoff/ORAL_GNM_FIRST.md`.

## Face / eyes

Owner-drawn linework + ICT/GNM eye donors override generic landmarks when they disagree.  
Eye clearance: contract + ladder + gate on main.  
Tripo Face Rig (mdj128/facial-animation): **candidate** only — visual weight review required; cannot replace oral/eye donors without evidence.

## Pipeline order (from toolchain JSON)

```text
source_snapshot → semantic_registration → source_mesh_measurement
  → repair_only_if_measured → retopology_candidate → triangle_quality_QA
  → deformation_topology_QA → protected_component_diff
  → skinning → weight_QA → Rigify → facial_rig_candidate
  → expression/blink → deformation_QA
  → real_render → reopen_pixels → SHA256 → receipt → promotion
```

Never destroy the previous artifact. Each stage consumes a **verified candidate**.

## MARS priority (head first)

eyes → eyelids → eyebrows → nostrils → mouth/oral → hair → ears → expressions  
then body/hand rigging.

## Rocket

Live door requires `operationId` + receipt/SHA. HTTP 200 alone is not authoritative. No invented `ROCKET_LIVE_SESSION_URL`.

## Next work (execution, not more registries)

For each lane: registered → provisioned → **physically executed** → measured → visually inspected → proven → promoted.
