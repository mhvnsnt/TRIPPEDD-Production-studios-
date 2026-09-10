# Toucan timeline renderer

Upstream: https://github.com/OpenTimelineIO/toucan
License: Apache-2.0

Role: secondary OTIO-native render/conformance path.

Toucan is a real software renderer for OTIO timelines and uses OpenTimelineIO,
OpenFX, OpenImageIO, OpenColorIO, OpenEXR and FFmpeg. It can render multi-track
timelines, transitions and effects to image sequences or movies.

TRIPPEDD integration rule:
- keep Blender as the primary 2D/3D scene renderer;
- use Toucan as an independent OTIO render/conformance backend;
- never silently substitute it for Blender;
- compare representative frames/timing against the editorial OTIO;
- promote only after a real TRIPPEDD OTIO render passes QC.

This gives the studio an independent renderer for detecting timeline/render
disagreements rather than another wrapper around FFmpeg.
