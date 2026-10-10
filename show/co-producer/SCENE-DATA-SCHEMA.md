# Co-Producer Scene Data Contract

Scene data is the production handoff between writing, storyboarding, animation, audio, and rendering. It is intentionally small enough to edit by hand and structured enough for tools to consume.

## Required top-level fields

- `schema_version`
- `show`
- `episode`
- `production`
- `assets`
- `shots`
- `presets`
- `validation`

## Shot contract

Every shot has:

- `id`: stable shot identifier (`S01`, `S02`, ...)
- `start`: start time in seconds
- `end`: end time in seconds
- `camera`: reusable camera preset
- `characters`: character IDs used in the shot
- `poses`: character ID → reusable pose
- `actions`: short machine-readable action names
- `audio`: audio cue IDs

## Production rules

1. Shot time ranges must be positive and ordered.
2. Shots must not overlap.
3. Every referenced character, location, prop, camera preset, pose, or effect must be declared in the relevant manifest or preset list.
4. Shot character count must stay within the episode validation budget.
5. The scene should remain editable without changing the source asset library.
6. Renderer-specific data belongs downstream; scene data describes intent and timing, not a particular animation application.

## Design goal

A future animator should be able to turn scene JSON into an animatic without rewriting the episode plan. A future renderer should be able to consume the same data without knowing how the scene was authored.
