# Drive Asset Recovery

This directory defines the recovery contract for external production assets, especially the God Molecule Tripo head.

Primary target:
- Drive file ID: `1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl`
- Drive URL: `https://drive.google.com/file/d/1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl/view?usp=drivesdk`

Required behavior:
1. Preserve the original bytes before any conversion.
2. Record source URL, file ID, acquisition timestamp, checksum, byte count and detected format.
3. Prefer authenticated Drive API or rclone when available.
4. Use resumable transfer and bounded retries.
5. After acquisition, inventory mesh/topology, dimensions/units, materials/textures, UVs, landmarks and rig readiness.
6. Never overwrite the original asset.
7. Gate downstream facial/likeness processing on source-integrity validation.
8. If one transport is unavailable, immediately attempt the next registered transport rather than ending the production run.

This repository intentionally records the recovery contract without claiming that the Drive bytes have already been acquired.
