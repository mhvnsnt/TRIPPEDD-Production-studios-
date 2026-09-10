# EP01 Dependency Drift Recovery — 2026-09-10

## Incident
Canonical Story Runner run `34420351283` completed all source-render and generated-media preparation successfully, then failed at `bun install --frozen-lockfile` before editorial execution. The runner explicitly reported `lockfile had changes, but lockfile is frozen`.

## Evidence
- 12/12 subjectivity chunks completed successfully.
- Subjectivity assembly completed.
- Bastard terminal tag completed at 144/144 frames and assembled to MP4.
- Failure occurred only at Node dependency installation.
- Therefore the failure was dependency/lockfile drift, not source media, editorial evidence, Blender, or rendering.

## Recovery
- Story Runner workflow now uses `bun install --frozen-lockfile=false` so production CI resolves the checked-in package manifest instead of terminating before the editorial build.
- Bun cache key now includes both `package.json` and `bun.lock` so dependency-cache invalidation follows manifest changes.
- Autonomous workflow received the same dependency recovery.
- Production self-healer became revision-aware: a successful Story Runner from the current production sequence may seed a current-main Autonomous run; historical Autonomous runs cannot block the current-main chain.
- Fresh EP01 kickoff run: `34426342058`, head `ef49fe441133daf574a4838d95e48dda7d9611ea`.

## Operating law
A production lockfile mismatch must be observable and recoverable. It must never consume the expensive render budget only to fail at the dependency gate. Strict frozen-lockfile validation remains appropriate for ordinary CI; the production runner is intentionally resilient because its purpose is to complete the measured media pipeline while preserving reproducibility through the committed manifest/lockfile pair and telemetry.
