# EP01 production — Bun install recovery

Date: 2026-09-10

## Evidence

Story Runner run `34426342058` completed all 12 subjectivity chunks successfully, assembled the subjectivity MP4, and reused all 12 cached Bastard terminal-tag chunks (144/144 frames). The build then failed before editorial execution at `Install Node dependencies`.

The failure was not a dependency-resolution failure. The workflow command was syntactically invalid for the installed Bun version:

`bun install --frozen-lockfile=false`

Bun rejected the flag because `--frozen-lockfile` is boolean and does not accept a value.

## Recovery

- Story Runner workflow changed to `bun install --no-save`.
- Autonomous workflow changed to the same supported install mode.
- A fresh EP01 production kickoff marker was pushed after the workflow fixes so the production run receives the repaired workflow revision rather than rerunning the failed SHA.
- Successful render/checkpoint caches remain reusable; no blind rerender is required.

## Operating law

A production recovery flag must be validated against the actual tool version in CI before being relied upon. When a cheap orchestration/configuration defect is discovered after expensive media work has completed, fix the orchestration defect and launch a fresh run that preserves the expensive outputs through durable caches.

## Next gate

Fresh Story Runner must reach the editorial build. On success, technical QC must validate the canonical artifact, then the current-main self-healer should dispatch the independent Autonomous cut with the successful Story Runner run ID so only verified generated media is reused.
