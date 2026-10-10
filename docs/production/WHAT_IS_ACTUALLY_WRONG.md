# What is actually wrong — named problems + receipts

Through-line: **almost every expensive failure was an instrument that could not express the defect.**

## Named problem classes

| Class | Examples we hit |
|-------|-----------------|
| Mesh repair | Non-manifold, weld-before-boolean, glTF shard edges |
| Retopology & triangle quality | Slivers, min angle ~0.16°, scan-following tris |
| **Deformation topology** | Missing lid/lip loops; densify multiplying fans |
| Anatomical registration | MediaPipe lids on cheeks; wrong 3D lift |
| Boolean surface surgery | Constant-y loft, commissure cut-through |
| Skinning / weight transfer | Wrong influences, candy-wrapper |
| Rig architecture | Deform vs control; blink_closure arity |
| Blendshape / FACS transfer | Blink not on painted lines |
| Collision | Lid–globe clearance; rest penetration |
| Cloth / hair | Semantic hair-as-face |
| UV / normal transfer | |
| Semantic segmentation | Hair locks, neck/ear exclusions |
| **Colour management** | Linear ID values compared to sRGB PNG |
| Render / pixel QA | hide_render; wrong buffer; rest vs open pose |

## Instrument failures (do not reintroduce)

| Instrument | Defect it could not see |
|------------|-------------------------|
| Occlusion % | Lid peeling **open** scored 84% closed |
| Min-across-column | Slit/seam **band** invisible |
| Median on ties | Blink guard median on zero canthi |
| Control that cannot fail | Uncarved scan always 0 cavity cells |
| Ray without hide_render | Geometry present, pixels absent |
| Recess p95 vs gate max | Gums failed on farthest 5% |
| Linear vs sRGB | ID 0.03 → rendered (49,49,49); 93.8% “unknown” |

## GNM oral — first full execution (2026-09-13)

Six blockers, **none geometry**:

1. `provision_oral_donors.sh` not executable  
2. System python vs `TRIPPEDD_PYTHON_BIN` (h5py install no-op)  
3. Mouth-frame schema mismatch (`center`/`corners` vs `frame.matrix`) — translated; +y into head, width 50.00 mm matched  
4. Recess p95 vs max statistic mismatch  
5. Boolean over shape keys — irrelevant; `oral_cavity.py` carves pre-rig  
6. ID render: no world/camera, wrong buffer, **linear IDs vs sRGB PNG**

**Seated:** teeth 1,868 (was 1,476), gums 1,404, tongue 933, sock 406 as `MARS_ORAL_*`; GNM jaw-open; protrusion PASS; visibility PASS.

**Pixel truth FAIL at rest:** counts oral pixels with lips **shut** (correct after fix). Threshold must require an **open-mouth / jaw-open pose** (or separate rest vs open contracts). Do not treat rest closed-mouth low oral pixel count as missing anatomy.

## Real tooling gaps (honest)

**Already in stack, often unrun:** Blender, Rigify (ships eyelid rig), PyMeshLab, libigl, trimesh, pycpd, MediaPipe (diagnostic), ICT-FaceKit, MPFB2, Rhubarb, OpenCV, **GNM oral chain**.

**Genuinely missing for jagged triangles / UVs:**

| Tool | Job |
|------|-----|
| **Instant Meshes** | Quad retopology / orientation field |
| **xatlas** | UV atlas packing |

Pull those two. Do not invent another stack diagram.

## Law

Pixels veto geometry. UNKNOWN ≠ PASS. Donor first. Protected components are assets. Receipts require reopen + SHA.
