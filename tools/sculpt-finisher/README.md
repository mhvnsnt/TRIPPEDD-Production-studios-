# Sculpt Finisher (Z-2) + FlowRetopo wrapper (Z-1)

Free-versions build-out, BUILD-MAP section 3 (ZBrush): `docs/BUILD-MAP-FREE-VERSIONS.md`
SPEC Z-2 + SPEC Z-1. One Blender add-on: `sculpt_finisher.py`.

**Donor first — this add-on hand-rolls no remesher, no unwrapper, no baker.**
It is original `bpy` orchestration of donors that already exist:

| Chain step | Donor |
|---|---|
| Voxel-remesh cleanup | Blender built-in Voxel Remesh (DynaMesh analog) |
| Quad retopo | Blender built-in QuadriFlow (ZRemesher analog) |
| UV unwrap + pack | Blender built-in Smart UV Project + Pack Islands |
| Detail transfer | Blender built-in Multires modifier + Cycles bake, selected-to-active (Project-All analog) |
| Export | Blender built-in glTF (GLB) / STL exporters |
| Z-1 stage 2 | **Instant Meshes** — free external field-aligned remesher (Jakob et al.), official pre-built binary |

## Install

Copy `sculpt_finisher.py` into Blender (4.0+, developed/tested on 4.5.3)
via *Edit → Preferences → Add-ons → Install*, enable
"Sculpt Finisher + FlowRetopo". Panel: **View3D → Sidebar → Sculpt Finisher**.

## Z-2 — Sculpt Finisher

Select a sculpt, press **Run Sculpt Finisher (Z-2)**. The chain runs end to
end on a **duplicate** (`<name>_FINISHED`); the original is never modified:

1. **Voxel-remesh cleanup** (toggle, voxel size)
2. **QuadriFlow retopo** (toggle; target faces + symmetry shared with Z-1)
3. **UV unwrap + pack** (toggle, island margin)
4. **Add Multires** (toggle, levels) — parked during baking so it can't
   fight the bake
5. **Bake** (toggle per map: Normal / AO / Color) from the high-res
   original onto the duplicate, Cycles selected-to-active, PNGs written
   to the bake dir
6. **Export preset**: Game (GLB), Print (STL), Both, or None

Progress is reported in the status bar and every step logs
`[SculptFinisher] step n/N: <name> OK/FAILED` to the console.
**Fail-soft:** a failing step logs its name and error, stops the chain,
keeps the duplicate renamed `<name>_FAILED_<step>` for inspection, and
leaves the original untouched.

## Z-1 — FlowRetopo wrapper

Select a mesh, press **Run FlowRetopo (Z-1)**. Works on a duplicate
(`<name>_RETOPO`) and returns a **checked mesh** — the result line carries
verts/edges/faces, quad/tri/ngon split, non-manifold edges, boundary
edges, loose verts and degenerate faces.

1. **Density from vertex colors**: if the mesh has a POINT-domain color
   attribute (one named like `*density*` wins, else the first), its mean
   luminance scales the base target faces by 0.5×–1.5× (brighter paint =
   denser retopo). The note is logged either way.
2. **QuadriFlow with symmetry** runs first.
3. **Instant Meshes round-trip** runs next *if* its binary is available:
   OBJ out → `<binary> in.obj -o out.obj -f <faces> -r 4 -p 4` → OBJ in.
   The IM result is adopted only when it checks at least as clean
   (non-manifold edges) as the QuadriFlow result; the decision and both
   counts are logged.

### Instant Meshes: status and honest availability

Verified on this studio box 2026-10-30: the official free pre-built Linux
binary from the upstream README
(<https://instant-meshes.s3.eu-central-1.amazonaws.com/instant-meshes-linux.zip>,
source: <https://github.com/wjakob/instant-meshes>) downloads, runs
(`--help` OK, no missing libs), and batch-remeshes correctly, so on this
box the Z-1 IM leg **runs for real** (see `TEST_LOG.md`).

The wrapper resolves the binary in this order: panel path →
`$INSTANT_MESHES_BIN` → `PATH` → `~/workspace/tools/instant-meshes/`.
If none is found, Z-1 still completes on QuadriFlow and the result line
states `Instant Meshes: unavailable: <reason + official download URL>` —
documented, never faked.

## Test

`TEST_LOG.md` holds the real headless run (Blender 4.5.3, blobby displaced
icosphere with a painted `Density` vertex-color attribute): full Z-2 chain
→ GLB + 3 baked maps on disk, Z-1 with the IM leg, and a fail-soft probe
(export dir blocked → chain stops at `export`, original untouched).

Re-run:

```sh
flock /tmp/heavy-test.lock bash -c \
  'xvfb-run -a env -u PYTHONPATH /path/to/blender-4.5.3 -b \
     --factory-startup --python test_finisher.py -- --out /tmp/sf_out'
```
