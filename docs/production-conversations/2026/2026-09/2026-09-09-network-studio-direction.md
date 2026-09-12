# 2026-09-09 — Network / Studio Direction

## Producer

> We're doing all of those things: Off the Air, Robot Chicken, Campbell, Drewski comedy, sketch comedy, Cheech and Chong, Friday, and the broader mix of comedy, animation, scripted, music, reality and people-driven programming.

## Agent

The studio direction is now recorded as a **network/studio operating model**, not a single-format production pipeline.

The key architectural consequence is that TRIPPEDD cannot treat `episode` as the top-level abstraction. The top-level production graph needs to understand projects, formats, creators, talent, physical source, editorial versions, generated media, audio, finishing, QC, publishing and reuse. A sketch, animated short, music-driven experiment, scripted story, reality piece or long-form film should be able to enter the same studio and share the infrastructure that makes sense without being forced into the same creative process.

The model deliberately separates two simultaneous goals:

- **Vertical:** make current productions faster, more measurable, recoverable, finishable and higher quality.
- **Horizontal:** broaden what the studio can develop and produce, while making every completed production reusable as source material for the next project.

External research reinforces the architectural pattern. MTV historically described a development slate spanning comedy, scripted, animation, music and reality and later built MTV Studios around reimagining series, franchises and spin-offs. Adult Swim's *Off the Air* demonstrates a deliberately heterogeneous audiovisual format built from themes, guest curation, music and artists. citeturn0search0turn0search1turn0search3

TRIPPEDD is not being designed to imitate those networks. Their useful lesson is the **breadth of the development and production machine**: creators and ideas should be able to move between formats while the studio preserves provenance, reusable assets and institutional knowledge.

## Implementation record

- Added `docs/TRIPPEDD-NETWORK-STUDIO-OPERATING-MODEL.md`.
- Added `config/production-capability-registry.json`.
- The capability registry explicitly tracks vertical/horizontal axes, maturity, next integration, impact and dependencies.
- The current EP01 production run remains untouched while these architecture changes land.

## Live production evidence at time of entry

Run `34380107515` remains active. All twelve subjectivity chunk jobs are complete. Build job `102563831679` has completed setup, caches, media stack, Blender, subjectivity assembly, Bastard terminal tag and Node installation. **Build Story Runner cut** is currently in progress; verification and upload remain pending.

No restart or cancellation was issued.
