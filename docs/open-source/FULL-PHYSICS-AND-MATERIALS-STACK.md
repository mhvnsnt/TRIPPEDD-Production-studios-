# Full Physics / Materials / Tissue OSS Stack

The production umbrella keeps complete upstream projects as pinned submodules. These projects are tools and research lanes; they do not automatically become authority over canonical MARS geometry.

## Added in this tranche

| Project | Pinned commit | Role | License/adoption |
|---|---|---|---|
| Tissue | `d2e8393cac351a07b74b4ff1aed2e4ca758f4e7c` | computational design, tessellation, lattice/surface construction | GPL-2.0-or-later |
| RigFlex | `ddce51fc70011d29188a8a387ea6bfdfc2a39f25` | secondary/jiggle motion on rigs | upstream license review required |
| SimuSama | `4545bfe7a7a96dec5b2ffcdec45c1ec33f3ac1fd` | MPM fluid/soft-body research lane | no declared license; research-only |
| Molecular Plus | `fb2e780d9fa5c166e60e66b44a6c347745167c52` | particles, granular, soft-body, fluid-like and destruction effects | GPL-3.0-or-later |

## Production architecture

### Character construction
Blender + Blender Addons + Tissue + BlenRig + facial-animation + facial autorigging tools.

### Soft tissue / secondary motion
Native Blender XPBD is the first production path. RigFlex and Molecular Plus are alternate/research solvers. SimuSama is retained as a complete MPM research project until its licensing is clarified.

### Water / tears / rain / smoke
Blender's Mantaflow remains the baseline. Blender's current fluid system supports liquid and gas simulation; external projects may accelerate or extend this only after reproducible smoke tests and license review.

### Agent-controlled production
mcp-blender operates Blender as a complete tool while the repo's evidence gates remain authoritative. Agents must see actual rendered pixels and overlays rather than relying on backend assertions.

## Non-negotiable rules

1. Whole project first; adapters second.
2. Pin exact upstream commits; floating references are forbidden.
3. Preserve upstream license/attribution and bundled dependency licenses.
4. Never let an external rigging/AI/landmark system silently rewrite owner-drawn MARS facial authority.
5. Canonical source geometry remains immutable.
6. Numerical QC and actual-pixel visual evidence are both required.
7. UNKNOWN never becomes PASS.
