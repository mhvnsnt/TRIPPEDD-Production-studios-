# AYON + OpenRV review integration

Upstreams:
- https://github.com/ynput/ayon-openrv
- https://github.com/AcademySoftwareFoundation/OpenRV

Role: review/playback and version-aware artist review.

OpenRV is a high-performance, hardware-accelerated image/sequence viewer built
for VFX and animation pipelines. The AYON addon provides version/workfile
tracking and loading of image sequences and movies. The addon does not ship
OpenRV binaries, so TRIPPEDD must build/package the appropriate upstream binary
separately.

TRIPPEDD contract:
- OpenRV is a review client, not the source-of-truth database.
- Kitsu/Zou remains production tracking.
- OTIO remains editorial interchange.
- Review sessions must identify project/episode/scene/shot/version.
- Annotations/review decisions become structured production events.
- Binary licensing/build requirements remain explicit.

Promotion gate:
OpenRV build -> AYON addon install -> load EXR/sequence/MOV -> identify exact
TRIPPEDD version -> submit review event -> QC audit trail.
