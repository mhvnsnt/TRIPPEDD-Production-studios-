# EP01 blocker audit — 2026-09-10

## Producer direction

The episode path is now the priority. Before another production run, audit the complete path for blockers, preserve salvageable work, remove avoidable rerender/reinstall bottlenecks, and keep real progress telemetry visible.

## Findings and fixes

### 1. Google Drive source transport was the hard blocker
The previous EP01 run completed all subjectivity rendering and the Bastard terminal tag, then failed during public Google Drive ingest because the shared-download path was throttled.

The source transport now has an explicit recovery ladder:

1. Existing local/cache media.
2. Authenticated rclone Google Drive transport when configured.
3. Browser-cookie-assisted gdown public transport when configured.
4. Resumable per-file gdown downloads.
5. Truthful PARTIAL/FAILED states; no fake COMPLETE state.

The preflight now probes the real source transport before expensive downstream work and records which transport was actually available.

### 2. gdown multiline manifest parsing was a real code defect
The folder JSON parser previously assumed a one-line/final-line representation. It now extracts the complete JSON array from the returned stdout, including multiline output.

### 3. Completed subjectivity work was being thrown away on later runs
Run `34428807358` has all 12 subjectivity chunk artifacts available. The Story Runner workflow now attempts to salvage each prior chunk before downloading Blender or rerendering it. Each salvaged chunk is independently verified as exactly 12 non-empty frames and is re-uploaded into the current run's artifact namespace.

This makes prior verified work a checkpoint, not disposable output.

### 4. Production artifact validation remains downstream of real output
The Story Runner build still requires MP4 + JSON + OTIO, then ffprobe/MediaInfo inspection and `pilot:validate` before publishing the production artifact.

### 5. Progress remains evidence-gated
`watch-progress.sh` continues to require an observable production ledger and fresh heartbeat. Missing telemetry is UNKNOWN, not healthy RUNNING. Percent, work, elapsed time, measured rate and ETA are derived from the ledger rather than wall-clock guesses.

## Remaining external dependency

The one blocker that code alone cannot manufacture is authorized access to the source media if Google continues returning its server-side download restriction. rclone is wired for an authenticated Drive remote, but the workflow cannot invent the operator's Google credentials or repository secret. Public gdown remains a fallback and does not bypass Google's server-side quota.

The workflow therefore fails fast on source transport rather than spending hours rendering an episode that cannot ingest its source footage.

## Operating rule from this audit

Do not blindly rerun. Reuse verified artifacts, cache expensive work, probe external dependencies early, measure every production stage, and only start the next full episode run after the source transport gate has evidence of a usable path.
