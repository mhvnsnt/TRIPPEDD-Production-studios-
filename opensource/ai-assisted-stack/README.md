# TRIPPEDD AI-Assisted Production Stack

This layer deliberately separates **AI generation** from **production authorship**.

## Operating model

Producer intent
→ AI planning / assistance
→ deterministic/open-source production tools
→ human approval
→ render
→ QC
→ deliver

AI may propose shots, timing, dialogue, sound design, animation blocking, assets, or code. It does not silently replace the editorial/production authority.

## Tool families

### Speech / transcription
- whisper.cpp / Whisper-compatible local inference for transcription and timing.
- faster-whisper can be used where Python deployment is preferable.

### Audio
- FFmpeg for deterministic media operations.
- FFmpeg filters and local DSP are the authoritative finishing layer.
- Generative audio is treated as source material that must pass editorial/QC before delivery.

### Timeline / interchange
- OpenTimelineIO remains the interchange contract between editorial and downstream render systems.

### 3D / animation
- Blender remains the canonical scene/animation authoring environment.
- Flamenco handles Blender farm execution.
- OpenCue handles larger parallel task/frame workloads.

## Promotion gates

An AI-assisted artifact is promoted only when:

1. It is traceable to a production request.
2. The source/model/tool and generation parameters are recorded when available.
3. The artifact is independently inspectable.
4. It survives deterministic technical QC.
5. Human/editorial approval is recorded when the artifact affects story, performance, or final creative direction.

## Non-goals

This stack is not an “AI video button.” It is a cooperative production layer around the studio's existing tools, footage, animation, editorial decisions, and render infrastructure.
