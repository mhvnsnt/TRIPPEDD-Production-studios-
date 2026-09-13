# Full-Repo Open-Source Umbrella

The production stack treats useful open-source software as complete tools, not snippets. Each selected project is pinned as a Git submodule under `third_party/oss/` so the whole upstream repository remains available to agents and builders.

## Pinned full projects

| Project | Full repo path | Primary use | License / policy |
|---|---|---|---|
| Blender | `third_party/oss/blender` | Core DCC, animation, rendering, geometry, physics, Mantaflow | GPL-2.0-or-later; upstream license files govern |
| Blender Addons | `third_party/oss/blender-addons` | Rigify, Mesh Tissue and the wider official addon toolbox | GPL-2.0-or-later where applicable; retain upstream notices |
| facial-animation | `third_party/oss/facial-animation` | Facial rigging, expressions, mouth/teeth/tongue, lip-sync, QA and agent skills | MIT |
| Open Mocap Blender | `third_party/oss/open-mocap-blender` | Offline body/hand capture and retargeting | MIT |
| BlenRig | `third_party/oss/BlenRig` | Auto-rigging, skinning, deform cages, advanced facial system | Preserve upstream license/attribution |
| FacialAutoRigger | `third_party/oss/FacialAutoRigger` | Independent facial autorig/shape-key experiment | MIT |
| ARKit Creator Blender Addon | `third_party/oss/ARKit-Creator-Blender-Addon` | 52-shape facial expression baking workflow | MIT |
| BlendCap | `third_party/oss/BlendCap` | Full body/hand/face markerless capture and retargeting | GPL-3.0-or-later plus separate third-party dependency licenses; source/reference-first until dependency clearance |
| mcp-blender | `third_party/oss/mcp-blender` | Agent-facing Blender inspection, rigging, animation and physics control | Verify upstream license before redistribution |

## Wiring rule

A submodule is the **whole tool**. We do not copy one convenient script and pretend that is the project. Production adapters call into the complete project where useful, while the MARS authority/gates remain outside the upstream projects.

The canonical MARS mesh and owner-drawn facial linework remain immutable authorities. Third-party tools are builders, drivers, observers, capture systems, or simulation systems. They cannot silently redefine anatomy.

## Reality-production lanes

- **Character construction:** Blender + Rigify/BlenRig + FacialAutoRigger + facial-animation + ARKit Creator.
- **Performance:** Open Mocap Blender + BlendCap + ARKit tooling.
- **Agent control/inspection:** mcp-blender + the repo's evidence gates.
- **Soft tissue / cloth / hair:** Blender's native physics stack first; external full solvers may be added only after license and reproducibility review.
- **Water / rain / tears:** Blender Mantaflow inside the full Blender source tree is the baseline fluid tool. A separate liquid solver can be pinned later if it is genuinely open, redistributable and reproducible.
- **Topology / tissue:** the full Blender Addons tree keeps Mesh Tissue and related modeling utilities available instead of extracting isolated pieces.
- **Rendering:** Blender is the canonical local render engine; generated media can be assembled from real simulations, captures, procedural animation, authored geometry, and optional generative-media stages.

## Adoption gate

Every full-project addition must record:

1. upstream URL and pinned commit;
2. license and dependency-license status;
3. exact integration lane;
4. version/toolchain requirements;
5. reproducible bootstrap/install path;
6. input/output hashes where an adapter transforms production data;
7. numerical QC;
8. actual-pixel visual evidence when visual output is claimed;
9. rollback/update path;
10. `UNKNOWN` never becomes `PASS`.

Submodules are intentionally pinned rather than floating at `main`: an upstream update is a measured dependency update, not an invisible production change.
