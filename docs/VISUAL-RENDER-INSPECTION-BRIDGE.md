# Visual Render Inspection Bridge

The production repo now has an evidence-first render inspection path.

It preserves original media, extracts representative video frames with ffmpeg,
records SHA-256 and ffprobe metadata, and uploads the packet as a GitHub Actions
artifact. It never declares visual quality from telemetry alone.

This mirrors the important part of a screenshot-driven agent workflow: the
vision-capable agent receives actual rendered pixels and can inspect them.

The GitHub connector can retrieve the Actions artifact after a render completes.
The assistant can materialize it, inspect the keyframes, compare before/after
packets, and report what is actually visible.

A repository cannot install a new native ChatGPT tool into the ChatGPT runtime.
This bridge therefore creates a stable connector-readable evidence contract
rather than pretending to modify the platform's built-in tool registry.
