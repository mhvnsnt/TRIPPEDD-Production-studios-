# EP01 source unblock

The production code is no longer the blocker. The bounded source gate proved the remaining blocker is Google Drive transport.

## Evidence

The source gate reports:

- `SOURCE_GATE_RCLONE=NOT_CONFIGURED`
- `SOURCE_GATE_COOKIES=NOT_CONFIGURED`
- public `gdown 6.2.0` can enumerate the folder but cannot retrieve the first media file's public link because Google is throttling/limiting the shared file.

## Fastest production-safe unblock

Configure **one** authorized transport in GitHub Actions:

### Option A — authenticated rclone (preferred)

Repository secret:

- `TRIPPEDD_RCLONE_CONFIG_B64` — base64-encoded rclone configuration for an authorized Google Drive account/remote.

Repository variables:

- `TRIPPEDD_RCLONE_REMOTE` — the configured rclone remote name, e.g. `trippedd-drive`.
- `TRIPPEDD_RCLONE_PATH` — the Drive path containing the EP01 source media.

The pipeline already performs resumable, checksum-preserving recovery and emits real `RCLONE_PROGRESS` telemetry.

### Option B — browser-authenticated gdown

Repository secret:

- `TRIPPEDD_DRIVE_COOKIES_B64` — Netscape-format browser cookies for an account that is authorized to access the source media.

This keeps the existing gdown transport but gives it an authenticated browser session where permitted.

## What does NOT work

Changing download libraries, adding retries, or using another anonymous HTTP client cannot legitimately defeat Google's server-side `too many users` restriction. The production pipeline therefore refuses to pretend the source is healthy.

## After the transport gate passes

The full Story Runner workflow can run without repeating the expensive visual work unnecessarily:

- prior verified subjectivity chunks are salvaged first;
- Blender is skipped for salvaged chunks;
- Bastard frames are cached/resumable;
- media/segment/Whisper caches are retained;
- Story Runner remains separate from Autonomous;
- final MP4 + JSON + OTIO are validated before publication.
