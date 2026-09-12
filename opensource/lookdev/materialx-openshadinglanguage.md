# MaterialX + Open Shading Language look-development layer

Upstreams:
- https://github.com/AcademySoftwareFoundation/MaterialX
- https://github.com/AcademySoftwareFoundation/OpenShadingLanguage

Role: portable material/shader interchange and look-development layer across
Blender, renderers, compositing and future DCC workers.

Why it belongs here:
ASWF identifies MaterialX as an open standard for platform-independent rich
material/look-development exchange, and OSL as the de facto shading/pattern
language used by physically based renderers. Both are established production
pipeline projects.

TRIPPEDD contract:
- Blender remains the primary authoring DCC.
- MaterialX is the portable material/look representation.
- OSL is shader logic, not production orchestration.
- OpenColorIO governs color transforms.
- OpenEXR is the HDR interchange target.
- Any conversion must preserve provenance and fail QC on unsupported nodes;
  never silently flatten a look.

Promotion gate:
pinned upstream revisions + shader/material fixture + Blender round-trip +
rendered comparison + QC artifact.
