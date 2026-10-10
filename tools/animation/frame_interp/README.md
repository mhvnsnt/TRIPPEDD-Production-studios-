# frame_interp — ffmpeg minterpolate frame interpolator (WIRED, PROVEN)

Motion-compensated frame interpolation for episode work (slow-mo, 24->60fps
upconversion of keyframed plates, inbetween generation).

- Tool: `ffmpeg -vf minterpolate` (mi_mode=mci, mc_mode=aobmc, me_mode=bidir)
- Entrypoint: `interpolate.py` (run via `./BUILD.sh`)
- Proof: 4 synthetic keyframes (textured sprite, 120->240px travel) ->
  16 interpolated frames; every PNG reopened at 320x180; square centroid
  monotonic 139.47->219.47px; travel 80px; count 16/16. See proofs/PROOFS.md.
- Reproducible: keyframes are seeded/synthetic — identical bytes every run.

Known limits (verified in this sandbox, ffmpeg 8.1.2):
- minterpolate emits ZERO frames from a 2-frame input; minimum 3 input frames.
- Very fast synthetic motion (>60px per keyframe gap) can wobble centroids;
  keep keyframe gaps small (this is how real 24->60fps upconversion behaves).
- RIFE: attempted, DEFERRED (see FAILURES.md).

Swap the synthetic keyframes for real episode plates by replacing the
`make_frame` calls with your PNG sequence — the ffmpeg flags are unchanged.
