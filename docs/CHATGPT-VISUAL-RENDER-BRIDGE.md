# ChatGPT visual render bridge

Anthropic's current guidance describes computer-use verification as
screenshot-driven and notes that video can be analyzed by breaking it into
frames. TRIPPEDD now has the corresponding durable evidence boundary:

render -> preserve original -> extract keyframes -> Actions artifact -> vision inspection

For ChatGPT, the existing GitHub connector can read workflow runs and download
Actions artifacts. The visual packet is named VISUAL-RENDER-INSPECTION-<run-id>.
Once downloaded, its keyframes are the actual pixels the assistant can inspect
and show back in the conversation.

The repo cannot add a new first-party ChatGPT tool. If a future MCP/connector
endpoint is attached to this project, its stable operations should be:

- render(scene, frame_start, frame_end)
- screenshot(frame_or_time)
- inspect_image
- inspect_video
- compare_visual_packets
- fetch_render_artifact
- render_status

All operations should return files plus provenance. Never turn telemetry-only
success into a visual PASS.
