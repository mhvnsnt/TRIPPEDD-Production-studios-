# EP01 source gate result — 2026-09-10

## Gate run

Source Transport Gate run: `34480885921`

Measured duration: about 28 seconds from runner start to source failure after tool installation.

## Result

`SOURCE_GATE_RCLONE=NOT_CONFIGURED`

`SOURCE_GATE_COOKIES=NOT_CONFIGURED`

The public gdown path reached the actual Drive source, but Google rejected retrieval of the first media file's public link. gdown reported that the public link could not be retrieved and indicated the file may have had many accesses.

This is a confirmed external source-transport blocker, not an episode-rendering failure.

## What was deliberately NOT done

No full EP01 Story Runner run was kicked off after this gate failed. This avoids burning another long Actions run on a source path that cannot currently ingest the footage.

## Preserved capability already on main

- multiline gdown folder-manifest parsing fix;
- authenticated rclone recovery path;
- browser-cookie-assisted gdown fallback;
- truthful PARTIAL/COMPLETE ingest states;
- prior-run subjectivity artifact salvage;
- resumable/cached Bastard terminal tag;
- real progress/heartbeat watchdog;
- final MP4/JSON/OTIO validation;
- standalone source transport gate.

## Required unblock

Configure either an authorized rclone Google Drive remote (`TRIPPEDD_RCLONE_CONFIG_B64` plus `TRIPPEDD_RCLONE_REMOTE`/`TRIPPEDD_RCLONE_PATH`) or authorized browser cookies (`TRIPPEDD_DRIVE_COOKIES_B64`). Once the source gate passes, the full production run can proceed without blindly repeating the completed visual work.
