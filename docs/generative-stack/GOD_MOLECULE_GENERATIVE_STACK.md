# God Molecule — Open-Source Generative Production Stack

Goal: give TRIPPEDD Production Studios a self-hostable, agent-callable image/video generation stack so production does not depend on consumer-service generation quotas.

## Five full projects selected

1. **ComfyUI** — orchestration / node graph
   - https://github.com/comfyanonymous/ComfyUI
   - Primary role: one reproducible graph-based control plane for image + video workflows.
   - Supports current Wan and HunyuanVideo workflows and saves workflows as JSON.
   - Use as the main agent-facing generation runtime.

2. **InvokeAI** — image creation/editing workstation
   - https://github.com/invoke-ai/InvokeAI
   - Primary role: reference-image editing, in/out-painting, canvas work, model management and repeatable image workflows.
   - Useful for Mars/God Molecule because edits should preserve supplied likeness rather than regenerate a different person.

3. **DiffSynth-Studio** — multimodel diffusion engine
   - https://github.com/modelscope/DiffSynth-Studio
   - Primary role: broad image/video/audio diffusion support, VRAM management, quantization, LoRA and model integration.
   - Its 2026 Model Integration Skills are particularly relevant to automatically adding new open models.

4. **LTX-Video / LTX-2** — production-oriented video + synchronized audio/video
   - https://github.com/Lightricks/LTX-Video
   - Primary role: image-to-video, keyframes, video extension, video-to-video and synchronized audio/video.
   - Candidate for fast iteration and longer-form generated shots.

5. **Wan2.1 / Wan video family** — high-control video generation
   - https://github.com/Wan-Video/Wan2.1
   - Primary role: T2V, I2V, first/last-frame-to-video and video editing.
   - Wan2.1 includes 1.3B and 14B variants; the 1.3B model can run around 8GB VRAM for 480p generation, while larger variants target higher quality.
   - Candidate for Mars turnaround animation, controlled transitions, environment shots and experimental sequences.

## Architecture

TRIPPEDD Production Studio
  -> production brief / scene intent
  -> reference + identity lock
  -> ComfyUI orchestration
      -> InvokeAI image/edit branch
      -> DiffSynth multimodel branch
      -> LTX video/audio branch
      -> Wan video branch
  -> deterministic post-processing / QC
  -> render queue
  -> Physical Source / Editorial timelines
  -> episode assembly

## Non-negotiable God Molecule rule

Reference-driven work is **editing/animation of the supplied character**, not unconstrained character regeneration.

For Mars:
- canonical front/left/right/back references remain the identity source;
- likeness must be measured/checked before acceptance;
- generation may change motion, lighting, environment, expression or explicitly requested transformations;
- it must not silently redesign the face, hair, proportions or recognizable identity;
- new character generation requires explicit user instruction.

## "Unlimited" generation

The software itself has no consumer-service quota. Actual throughput is bounded by available GPU/CPU/RAM/storage and model licenses. The goal is therefore an owned local/self-hosted render queue with repeatable jobs, not dependence on Gemini/Grok/ChatGPT generation quotas.

## Licensing

Do not treat all model weights as having identical licensing merely because the surrounding code is open source. The stack records code repositories separately from model/checkpoint licenses. Every model selected for a production render must pass a license/provenance check before commercial release.

## First God Molecule use cases

- Mars 4-angle reference preservation
- slow rotating Mars head
- controlled image-to-video from approved reference frames
- psychedelic environment generation
- transition shots
- abstract mind/universe imagery
- expression variants using reusable 2D/3D assets
- sound/music/audio generation where model licensing permits
- batch generation of alternatives without external service quotas

## QC principle

measure -> compare -> modify -> render -> inspect -> repeat

Every generated derivative should retain:
- source references
- model/checkpoint
- workflow
- prompt
- seed where applicable
- generation parameters
- tool/version
- provenance
- QC result
