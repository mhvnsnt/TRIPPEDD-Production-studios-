# OSS that must still be pulled (honest list)

## Already present / in-repo — run them

Blender, Rigify (bundled face/eyelid), GNM oral chain, ICT-FaceKit eyes, PyMeshLab, libigl, trimesh, OpenCV, owner linework, eye-clearance gates.

## Genuinely missing (jagged triangles + UVs)

| Tool | Role | Notes |
|------|------|--------|
| **Instant Meshes** | Quad retopology / orientation field | Gap behind PS1/sliver topology |
| **xatlas** | UV atlas packing | Clean UV islands after retopo |

Optional candidate accelerators (verify license before ship): Remi (Blender repair→retopo→UV→bake pipeline), Pinocchio (auto skeleton), Tripo face-rig adapter (candidate only).

## Do not

- Build another stack diagram instead of provisioning Instant Meshes + xatlas
- Replace GNM oral with hand densifiers
- Claim CI contract PASS as physical MARS PASS
