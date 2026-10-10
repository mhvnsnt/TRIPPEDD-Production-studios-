# Blender OSS QA implementation notes

Use open-source Blender/MCP projects as adapters and implementation references only. Do not create a competing production authority.

The useful patterns are typed operations, real `.blend` source artifacts, staged physical QA, visual snapshots, checkpoints/restore, workspace allowlists, deterministic mock runtimes, real Blender smoke tests, and publish manifests.

First-shot implication: resolve a real `.blend` containing canonical Mars, deterministic world assembly, camera, render settings, and provenance before any pixel evidence can exist.
