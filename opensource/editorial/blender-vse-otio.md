# Blender VSE ↔ OpenTimelineIO bridge

Upstream references:
- https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- Blender VSE OTIO support work (2026)

Role: native editorial interchange between Blender's Video Sequence Editor and
the TRIPPEDD OTIO timeline.

The 2026 Blender GSoC work added/advanced OTIO import/export for movie, sound,
image/image-sequence strips, transitions/effects, scene/meta strips and
metadata round trips. The work is still represented by WIP upstream changes,
so TRIPPEDD treats this as an integration target, not a falsely completed
native feature.

TRIPPEDD contract:
- OTIO remains the editorial interchange truth.
- Blender remains a DCC/editor/render participant.
- A round-trip test must compare clip identity, timing, transitions, effects,
  audio and metadata.
- Unsupported constructs fail visibly and become QC findings.
- No silent flattening or guessed media paths.

Promotion gate:
known fixture -> Blender VSE import -> edit -> OTIO export -> structural
comparison -> media relink validation -> render/QC artifact.
