# Integration Priority V2

1. Blender + Flamenco + OpenUSD + OpenColorIO/OpenImageIO/OpenEXR
2. ComfyUI + ComfyTV + Blender blocking/camera references
3. Proscenio/OpenToonz/Synfig for authored 2D layers
4. Natron/OpenFX for compositing and keying
5. OpenTimelineIO + Kdenlive/MLT/OpenRV for editorial and review
6. Kitsu + AYON for shot/asset/task coordination
7. Temporal + NATS + PostgreSQL + MinIO for durable orchestration and artifact state
8. OpenCue as the scale-out render scheduler when Flamenco capacity is insufficient

Rule: integrate incrementally with health checks and rollback. Do not replace working TRIPPEDD paths until the new backend passes an isolated adapter test and a representative media test.

Commercial V4/V5: use 3D blocking and camera motion as the authoritative motion skeleton; use AI generation for selected texture/paint/video passes, 2D authored animation for graphic/comedic beats, and Natron/OCIO for compositing/color. This prevents another static-card result while retaining human direction.

Episode 1 Autonomous Cut: automated shot selection, transcript alignment, continuity checks, render orchestration, QC and bounded recovery.

Episode 1 Story Runner Cut: preserve human story intent, shot notes and editorial decisions while allowing AI co-production for selects, cleanup, graphics, transitions, sound design suggestions and alternate takes.
