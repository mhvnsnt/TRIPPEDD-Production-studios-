# TEST LOG — SPEC A-1 Checkpoint Render Driver proof run

Date: 2026-10-30 (~15:19–15:24 CDT) · Box: this VM (2-core, ~8 GB RAM)
Blender: 4.5.3 LTS at `~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`,
headless via `xvfb-run -a env -u PYTHONPATH` (driver default).
Box discipline: all Blender work serialized under
`flock /tmp/heavy-test.lock`; the driver's own RAM gate was set to
2000 MB for the proof because other lanes held the box at ~2.4 GB
available at start (phase 2 started at 3549 MB available). The gate
itself is proven separately below with an unreachable threshold.

Scene: Blender default cube scene saved as `tiny.blend` (437,753 bytes).
Proof config: Cycles CPU, 128×72 @100%, 4 samples, denoise off,
frames 1–6, prefix `frame_`. Per-frame durations 14–37 s (first frame
includes Blender startup + BVH build).

## 1. Kill-and-resume proof (the headline test)

Phase 1 — driver started, killed (SIGTERM to the driver + Blender)
after 3 frames were on disk. The kill landed during frame 4's launch
and is honestly logged (`rc=-15`):

```
2026-10-30T20:19:34+00:00 DRIVER START blend=.../tiny.blend frames=1-6 engine=CYCLES samples=4 out=.../frames min_free_mb=2000
2026-10-30T20:19:34+00:00 resume scan: 0/6 already verified; 6 to render; first missing = frame 1
2026-10-30T20:20:11+00:00 frame 1: OK rc=0 dur=36.9s sha256=3803e66ba4b2…
2026-10-30T20:20:33+00:00 frame 2: OK rc=0 dur=21.9s sha256=556ad0d2bdcf…
2026-10-30T20:20:49+00:00 frame 3: OK rc=0 dur=15.7s sha256=51c218a09fb1…
2026-10-30T20:20:49+00:00 frame 4: FAILED rc=-15 dur=0.2s (output missing)
```

Phase 2 — same command restarted. It re-hashed frames 1–3 against
`inventory.json`, skipped them, and rendered ONLY frames 4–6:

```
2026-10-30T20:20:52+00:00 DRIVER START ...
2026-10-30T20:20:52+00:00 resume scan: 3/6 already verified; 3 to render; first missing = frame 4
2026-10-30T20:21:10+00:00 frame 4: OK rc=0 dur=17.2s sha256=f1e28be5143a…
2026-10-30T20:21:24+00:00 frame 5: OK rc=0 dur=14.4s sha256=47e42023ac74…
2026-10-30T20:21:43+00:00 frame 6: OK rc=0 dur=19.1s sha256=901005a623aa…
2026-10-30T20:21:43+00:00 verify: 6/6 frames OK
2026-10-30T20:21:43+00:00 DRIVER DONE: ALL FRAMES VERIFIED
```

Phase 2 exit code: 0. `--verify-only` afterwards: `verify: 6/6 frames OK`,
exit 0. An independent Python SHA-256 re-check of all six PNGs against
`inventory.json` printed `independent_sha256_match=True` ×6 and
`INDEPENDENT_HASH_CHECK: PASS`.

## 2. Corrupt-frame proof

`frame_0005.png` was deliberately corrupted (bytes appended), driver
re-run: hash mismatch detected, ONLY frame 5 re-rendered, set verified:

```
resume scan: 5/6 already verified; 1 to render; first missing = frame 5
frame 5: OK rc=0 dur=27.8s sha256=d0d00dd4f1c9…
verify: 6/6 frames OK
```

## 3. RAM-gate proof

With `min_free_mb=999999`, `ram_timeout_seconds=6`: the gate logged
`ram-gate: available=3609MB < required=999999MB; waiting` repeatedly,
then `ram-gate: TIMEOUT waiting for RAM` / `ABORT: RAM gate timeout`,
exit 1, and launched NO Blender process (output dir contains only
`driver.log` — no frames, no blender log).

## Notes

- The owed Cape Jones Scene 1 960×540 re-render was NOT started; this
  build is the driver + small proof only, per the build order.
- Full raw logs (driver.log, phase stdout, blender_frames.log) were
  produced in the lane working dir during the run; the excerpts above
  are verbatim from `driver.log`.
