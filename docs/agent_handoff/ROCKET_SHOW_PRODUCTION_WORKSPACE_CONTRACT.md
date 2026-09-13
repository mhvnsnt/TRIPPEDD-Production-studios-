# Rocket Show Production Workspace Contract

## Purpose

Rocket is not merely a dashboard for the TRIPPEDD production repository. It is the visual production workstation through which the owner can inspect, build, edit, preview, correct, and publish the actual show.

The repository remains the source of durable production truth. Rocket is the hands-on visual control surface over that truth.

## Core loop

`GitHub + open source tools -> Rocket workspace -> real assets/scenes/shots -> owner visual edit -> agent/tool work -> render/preview -> QC/evidence -> GitHub commit/PR -> Rocket refresh`

Every loop must operate on real project artifacts. UI-only placeholders are not production results.

## Show-production requirement

Rocket must be capable of taking the production assets, tools, manifests, scripts, media, models, rigs, environments, cameras, audio, animation, compositing, and editorial data already present in the repository and using them to actually build EP01 and subsequent episodes.

The goal is not to expose metadata about a show. The goal is to make the show.

## Owner hands-on authority

The owner must be able to visually intervene wherever an agent-generated result is wrong, including:

- model and environment placement
- mesh/line work and geometry edits
- manual rig and bone placement
- skin weights and weight painting
- facial controls, lips, eyes, brows, jaw, teeth, gums, tongue
- shape keys and expression poses
- hair/strand placement
- materials, UVs, textures and shading
- collision and physical proxy geometry
- camera placement and lens/framing
- lighting
- animation blocking, keyframes and curves
- shot timing and sequencing
- compositing and visual effects
- audio/voice timing
- editorial assembly
- final QC corrections

A correction made by the owner must be representable as a real production change and persist back into the repository workflow.

## Agent authority

Agents remain available underneath the workspace for work that benefits from automation or computation:

- analysis and measurement
- topology/geometry diagnostics
- rig generation and validation
- weight transfer candidates
- expression generation
- animation generation and cleanup
- camera/shot analysis
- media analysis
- render orchestration
- QC and evidence generation
- batch operations
- open-source tool discovery/integration
- provenance and artifact manifests
- GitHub commits, branches, PRs and recovery receipts

Agents may propose or perform changes, but must not silently overwrite a known-good component or turn an unverified result into PASS.

## Visual truth

If the owner can see a result in Rocket, the displayed result should correspond to an actual artifact, scene state, render, or deterministic preview. `UNAVAILABLE` must remain `UNAVAILABLE`; missing bytes are not evidence.

For visual/geometry questions, actual rendered pixels and editable geometry are higher authority than text summaries or statistics alone.

## Repository/open-source ingestion

Rocket must continuously be able to discover and incorporate approved repository and open-source capabilities into the workspace. New tools should become usable production capabilities, not merely appear in a list.

Integration must preserve license/provenance information and must not silently replace existing production authorities.

## Save/publish loop

Owner edits and agent edits should be:

1. applied to a working copy/branch or explicitly controlled workspace;
2. previewed visually;
3. validated against relevant physical and visual gates;
4. recorded with provenance and artifact references;
5. committed to GitHub through the normal reviewable workflow;
6. immediately consumable by Rocket on refresh.

No successful-looking UI state is sufficient without the corresponding durable artifact.

## Show-building workspaces

Rocket should evolve toward integrated workspaces rather than isolated dashboards. At minimum, the production surface should converge on:

- Asset/Model workspace
- Mesh/Line/Geometry workspace
- Rig/Pose/Weight workspace
- Facial/Expression workspace
- Hair workspace
- Materials/UV/Shading workspace
- Camera/Lighting workspace
- Animation workspace
- Shot Composition workspace
- Editorial/Timeline workspace
- Audio workspace
- Compositing/VFX workspace
- Render Results workspace
- QC/Evidence workspace
- Agent/Tool workspace
- GitHub/Publish workspace

These should share the same canonical project state rather than maintaining disconnected copies.

## Playback and final-show requirement

The owner must be able to preview the actual assembled show, move through shots/scenes, pause at a frame, enter the relevant editing workspace, make a correction, save it, and return to playback.

The production surface must therefore support the equivalent of a real DCC/editor loop: edit -> preview -> inspect -> correct -> render -> assemble -> review.

Blender is an appropriate underlying authority because it already provides modeling, rigging, animation, rendering, compositing and video editing in one open-source suite, including a Video Sequencer for combining video, image, audio and effects into a final edit. See Blender's official documentation for animation/rigging and video editing capabilities.

## Canonical-component preservation

Known-good MARS and other production components are protected assets. Rocket must expose explicit duplicate/branch/restore semantics before destructive edits. No silent regeneration, whole-face replacement, material reassignment, shape-key removal, weight loss, collision loss, or overwrite of a known-good component.

## Definition of done

Rocket's production workspace is not complete when the tabs exist. It is complete when the owner can:

1. open the actual production project;
2. see the current real assets and show state;
3. manually edit a visual/technical element;
4. preview the change immediately;
5. invoke agents/tools against the same real state;
6. inspect their results visually;
7. accept, reject, or manually correct them;
8. render the affected shot;
9. assemble and watch the actual episode;
10. save the authoritative artifacts;
11. push the result back to GitHub;
12. reopen it later without losing the work.

The system is successful when Rocket lets the owner make the show instead of merely watching agents talk about making the show.
