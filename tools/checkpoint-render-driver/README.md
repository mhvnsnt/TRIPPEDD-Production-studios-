# Checkpoint Render Driver — SPEC A-1

Frame-resumable, RAM-gated Cycles render driver for Blender. Formalizes
the Cape Jones render pattern (BUILD-MAP-FREE-VERSIONS.md §8, SPEC A-1)
into a reusable, configurable tool: long renders survive VM restarts,
OOM kills and lane interruptions, losing at most one frame.

## Donor / prior art (DONOR FIRST)

This is a formalization, not an invention. The proven pattern comes from
the Cape Jones render lanes (2026-10-29, local lane):

- `render_driver_v2.sh` (Cape Jones render work) — one frame per Blender
  invocation, resume-from-first-missing by scanning for the first absent
  `frame_%04d.png`, free-RAM gate (>3400 MB available) before each frame
  launch, per-frame OK/FAIL logging, sample-drop fallback after repeated
  failures, a `flock` single-instance guard.
- `render_take.py` (Cape Jones EP01 Scene 1; also mirrored in
  mhvnsnt/cape-jones production work) — the in-Blender take script:
  explicit Cycles settings (CPU, samples, adaptive threshold, OIDN
  denoise, persistent data), fixed resolution, single frame range per
  invocation.

What this build adds over the donor: generality (any .blend / frame
range / resolution / samples via CLI or JSON config), a **hash-verified
JSON inventory** (the donor only checked file existence — a truncated
or corrupt frame would have passed), corrupt-frame re-render, bounded
per-frame retries, a final full-set verification pass, `--verify-only`
mode, and an optional ffmpeg stitch (off by default).

## Files

| File | Role |
|---|---|
| `checkpoint_render_driver.py` | The driver (stdlib only). Owns the loop: RAM gate → one Blender process per frame → hash + inventory → resume scan → final verify. |
| `render_one.py` | Runs *inside* Blender; applies settings from a JSON blob and renders exactly one frame. |
| `run.sh` | Thin wrapper: `./run.sh <args…>` = the driver. |
| `config.example.json` | Full example config (960×540, 32 samples, frames 1–81 — the owed Cape Jones Scene 1 shape; NOT run by this build). |
| `tests/TEST-LOG.md` | The kill-and-resume proof run, with log excerpts. |

## Usage

```bash
# CLI
./run.sh --blend scene.blend --output-dir frames/ \
         --frame-start 1 --frame-end 81 \
         --resolution-x 960 --resolution-y 540 --samples 32 \
         --blender ~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender

# or config file (CLI args override config values)
./run.sh --config config.example.json

# verify an existing frame set without rendering anything
./run.sh --config config.example.json --verify-only
```

On this VM, Blender headless needs X: the driver wraps each launch in
`xvfb-run -a env -u PYTHONPATH` automatically when `xvfb-run` exists
(disable with `--no-xvfb`).

## How resume works

State lives in the output directory:

- `inventory.json` — per frame: filename, SHA-256, byte size, status
  (`rendered`/`adopted`), duration, finish time. Written atomically
  after every frame.
- `driver.log` — timestamped per-frame status lines.
- `blender_frames.log` — appended raw Blender output per frame.

On start the driver re-hashes every frame in range:

- hash matches inventory → skipped;
- file exists but no inventory entry → **adopted** (hashed + recorded,
  not re-rendered);
- missing, empty, size- or hash-mismatched → re-rendered, starting from
  the first such frame.

Exit codes: `0` = full set verified, `1` = incomplete / gate timeout,
`2` = usage/environment error.

## RAM gate

Before *every* frame launch the driver reads `MemAvailable` and waits
(`--ram-poll-seconds`, default 15 s) until it is at or above
`min_free_mb` (default 3000 MB). `--ram-timeout-seconds` (default 0 =
wait forever) bounds the wait; on timeout the driver aborts having
launched nothing for that frame.

## Optional stitch

`--stitch` (with `--stitch-output`) assembles an mp4 with ffmpeg at the
config `fps` — **only after full verification passes, and off by
default**. The driver's job is frames + proof, not assembly.

## Proof

See `tests/TEST-LOG.md`: a 6-frame 128×72 / 4-sample render of the
default cube scene on Blender 4.5.3 — driver killed mid-run after
frame 3, restarted, resumed from frame 4 only, all hashes verified;
plus a corrupt-frame re-render test and a RAM-gate blocking demo.
