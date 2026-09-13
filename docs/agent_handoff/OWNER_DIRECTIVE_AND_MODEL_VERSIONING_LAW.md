# OWNER DIRECTIVE + MODEL VERSIONING LAW

Status: PERMANENT
Applies to Claude, Rocket, ChatGPT, workers, and production agents.

## 1. EXPLICIT OWNER DIRECTIONS

An explicit owner instruction is the active work order. Agents must execute the requested work before unrelated improvements.

If the requested route fails, find the next viable tool or open-source route immediately while continuing toward the same requested outcome. Do not silently replace the owner's objective with an agent-preferred objective.

Creative exploration is allowed where the owner explicitly grants it or leaves implementation details open. Existing production laws remain constraints, but they are not a reason to ignore a compatible explicit task.

## 2. CURRENT MARS WORK ORDER

The requested production sequence is:

1. Perfect mouth and lips.
2. Remove remaining lip and facial skin stretching.
3. Correct the mouth-gap / tooth-glint opening so it is centered anatomically rather than drifting to one side.
4. Perfect teeth, gums, tongue, cavity, and mouth-sock integration without damaging canonical oral work.
5. Perfect hair and remaining character-surface defects.
6. Increase texture, material, scan, and model quality.
7. Continue into animation, shot construction, episode assembly, rendering, and QC.
8. Continue integrating useful open-source production tools whenever they materially accelerate these goals.

Implementation may improve, but the objectives must not be silently replaced or reordered.

## 3. VERSION EVERY MODEL CHANGE

Before changing a production model, rig, mesh, material, texture, scan, or animation, create a recoverable checkpoint/version of the current state.

Every meaningful version records:
- version identifier
- parent version
- source artifact path
- source Git commit
- source SHA-256 when available
- resulting artifact path
- resulting SHA-256 when available
- tool/script and parameters
- physical gate result
- visual gate result
- promotion status

Never delete failed or distorted versions automatically. A failed version may contain reusable geometry, deformation, topology, texture, scan, hair, lighting, or animation information.

## 4. CANONICAL PRESERVATION

Review and experimental versions stay separate from canonical production assets.

Canonical is changed only after the candidate passes the applicable physical AND visual gates.

More topology, more vertices, or a green physical test is not sufficient reason to replace a known-good canonical asset.

## 5. PHYSICAL + VISUAL PROMOTION GATE

Promotion requires both structural/physical gates and actual rendered-pixel gates.

Pixels have veto authority. UNKNOWN, UNAVAILABLE, PENDING, or unreviewed visual evidence is never PASS.

## 6. VISUAL EVIDENCE IS AUTOMATIC

Every meaningful render is published through the repository evidence mechanism before the result is declared available.

Do not ask the owner to ferry screenshots between agents. The repository is the shared visual evidence bus for ChatGPT, Claude, Rocket, CI, and production workers.

## 7. BLENDER SESSION EFFICIENCY

Do not repeatedly launch Blender for independent questions that can be answered by one persistent session. Batch compatible inspections and A/B renders into one session.

A worker operation must not terminate a persistent Blender session with sys.exit/SystemExit. Convert operation failures into structured errors and keep the session alive when possible.

When Blender already provides a production-grade operation, prefer it over a hand-written approximation. For mesh attribute transfer, prefer Blender's native Data Transfer facilities before inventing a parallel transfer implementation.

## 8. OPEN-SOURCE ROUTING

When requested work exposes a missing capability, find and integrate an appropriate open-source tool rather than hand-rolling a weaker substitute. The integration must become a working production capability with provenance recorded.

## 9. ROCKET IS THE HUMAN VISUAL WORKSTATION

Rocket is the human-facing preview and hands-on production interface.

Agents must expose real production artifacts so Rocket can watch actual episodes and shots, inspect models, view diagnostic layers, manually correct visual details, save those corrections to authoritative artifacts, preview them, and preserve the result in GitHub.

## 10. CONTINUE THE OWNER'S WORK

When the owner says keep working, continue the active owner-requested production lane autonomously. Do not turn it into a status-only response or switch to unrelated optimization.

Routine unblocked work should continue without waiting for another prompt.

## 11. HANDOFF RECEIPT

Every agent handoff records:
- owner-requested objective
- actual changes
- canonical version
- candidate/review versions
- evidence paths and hashes
- physical verdict
- visual verdict
- next exact requested operation
- known blockers

The next agent resumes the owner's work order rather than inventing a new one.
