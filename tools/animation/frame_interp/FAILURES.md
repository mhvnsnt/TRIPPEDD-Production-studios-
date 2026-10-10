# FAILURES — frame_interp

## RIFE (ncnn Vulkan) — DEFERRED, not wired
- Tried: `rife-ncnn-vulkan-20220728-ubuntu.zip` from GitHub releases.
- Result: download timed out (curl exit 28 after 60s) in this sandbox.
- Second blocker: no Vulkan-capable GPU in the sandbox, so the ncnn Vulkan
  build could not execute here even if downloaded.
- Weights would have to live outside git anyway (>100MB rule does not apply —
  RIFE weights are ~25MB — but the missing GPU is the hard stop).
- Next step: retry on a GPU host; keep weights in /tmp, never in the repo.

## minterpolate 2-frame floor — DOCUMENTED LIMIT, not a failure
- `minterpolate` emits 0 frames when given only 2 input frames (tested with
  PNG-sequence MP4 and lavfi testsrc, both `mi_mode=mci` and `blend`).
- Minimum viable input is 3 frames. Tool harness uses 4 keyframes.
