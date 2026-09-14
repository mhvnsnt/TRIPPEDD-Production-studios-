# THE NAMES FOR WHAT WE HAVE BEEN FIGHTING — and which of it is already installed

Written because the owner asked what all of this is called and what fixes it. Every row
carries a receipt **from this repo**, not a general description, and every tool is marked
**HAVE / UNRUN / MISSING** — because the finding of this session is that the expensive
failures were not missing tools. They were tools we had and never ran.

## The disciplines, by their real names

| # | Discipline | What it looks like here | Receipt |
|---|---|---|---|
| 1 | **Mesh repair / manifold processing** | the scan arrived as loose triangles | 68,237 of 104,281 edges shared with nothing; welding at 1e-6 → 8 boundary edges, 0 vertices moved |
| 2 | **Retopology + triangle quality** | "a bunch of really big, ugly triangles" | `MARS_FACE` is 4.38% of the source's face triangles; single triangles wider than his eye opening. 4,689 tris under 15°, min angle 0.16° |
| 3 | **Deformation topology** | geometry that exists but cannot fold | the lid had **3 vertices** within 3 mm; 261 faces fill his entire mouth |
| 4 | **Anatomical registration** | landmarks on the wrong feature | MediaPipe's eyelid rings land on his **cheeks**, its brow ring on his **eyes**; the fit reported **0.0000 mm residual while 38.9 mm wrong** |
| 5 | **Boolean / CSG surface surgery** | the carve eating his corners | 44 of 483 cells with no exterior skin, 35 on his left |
| 6 | **Skinning / weight transfer** | severed or mis-weighted bodies | a rig cut at every joint scored a **perfect** deformation result because no piece can deform |
| 7 | **Rig architecture** | deform skeleton vs control rig | `rig_face.py` crashed before saving and printed a clean report — `blender -b` exits 0 after an exception |
| 8 | **Blendshape / FACS transfer** | named shapes onto a new head | 55 of 57 ICT shapes transferred; the 2 that could not are **recorded, not zero-filled** |
| 9 | **Collision / penetration** | hair through the face, tongue through the cheek | three definitions of "inside", and only *inside the closed solid AND nearest feature is skin* works |
| 10 | **Cloth / secondary motion** | hair that sags instead of swinging | drift 56.78 mm vs sway 4.20 mm — 93% of the "motion" was stretch |
| 11 | **UV / normals / shading transfer** | zero drift and still destroyed | 54,681 of 54,720 faces smooth with custom normals; `from_pydata` gives **0** |
| 12 | **Semantic segmentation** | hair must not become face | the 25-lock authority, neck and ear exclusions |
| 13 | **Colour management** | an ID pixel stops being its material | the view transform grades emission, **and** the PNG is sRGB while the IDs are linear: shell 0.03 expected at (8,8,8), rendered (49,49,49) |
| 14 | **Render/pixel QA** | measurement vs display truth | `hide_render=True` on all four oral parts, and **`scene.ray_cast` ignores it** — the survey reported 9.9% sock in a frame with zero sock pixels |

**The through-line is #14.** Nearly every expensive failure was an instrument that could not
express the defect: an occlusion count that scored a lid being pulled *open* as 84% closed;
a metric that took a *minimum across a slit*; a gate whose median landed on a tie; a control
that could not fail. That is why the rule is **pixels veto geometry**.

## What fixes each, and whether we have it

| Job | Tool | Status here |
|---|---|---|
| DCC, rig, cloth, render | **Blender 4.2.1 LTS** | HAVE — `vendor/blender` (a symlink into scratch; a cleanup deleted it once) |
| Control rig | **Rigify** | HAVE, bundled in that Blender. **UNRUN** — it ships a complete eyelid rig |
| Mesh repair / remesh / quality | **PyMeshLab** | HAVE |
| Geometry, winding numbers, signed distance | **libigl** | HAVE — it is what measures penetration and the crater |
| Meshes, rays, booleans | **trimesh** + **manifold3d** + **rtree** + **python-fcl** | HAVE (manifold3d added this session) |
| Non-rigid registration | **pycpd** + scipy TPS | HAVE — took eye placement 4.7 mm → 0.4 mm in one pass |
| Face landmarks | **MediaPipe** | HAVE, and **known wrong on his eyes** — use the painted authority |
| Named FACS shapes | **ICT-FaceKit** (MIT) | HAVE — `vendor/ict`, also ships eyeball, socket, occlusion, lashes, teeth |
| Oral anatomy | **Google GNM** (Apache-2.0) | HAVE — and the chain had **never once executed** until this session |
| Body/parametric | **MakeHuman / MPFB2** | HAVE — `vendor/opensource/mpfb2` |
| Lip sync | **Rhubarb** | HAVE — `vendor/rhubarb` |
| Image inspection | **OpenCV** | HAVE |
| Quad retopology | **Instant Meshes** | **MISSING** — the one real gap for #2 and #3 |
| UV atlas | **xatlas** | **MISSING** |
| Point cloud / inspection | **Open3D** | MISSING (libigl + trimesh cover most of it) |
| Automatic rigging | **Pinocchio** | MISSING, and lower value — Rigify is here and unused |

## The order that stops one stage destroying the last

Topology → bones → weights → shapes. **A boolean evaluated after the armature cuts a hole
wherever the cutter happens to be**, and a boolean cannot be applied at all over shape keys —
which is exactly why the GNM bridge appeared broken when it was simply being run at the
wrong point in the order.

And every stage produces **source → candidate → measurement → receipt**, never an overwrite.
Six tools in this repo wrote straight to `assets/rigs/MARS_FACE.blend`; two of them did it
during this session. They all take `--rig`/`--out` now.

## The two gates, and neither alone is a pass

**PHYSICAL** — counts, drifts, distances, in his own millimetres (`MW = 0.1930`, 1 mm = MW/50).
**VISUAL** — the actual published pixels, reviewed. `VISUAL_FAIL` outranks a green physical
gate, and `PENDING` is never `PASS`.

The receipt for why: teeth 13.5% / tongue 21.8% / cavity 13.7%, every physical check green,
on a frame whose crowns still read as separate pegs.
