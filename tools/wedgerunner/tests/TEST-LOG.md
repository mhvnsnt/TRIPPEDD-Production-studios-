# WedgeRunner test log — 2026-10-30

Environment: Blender 4.5.3 (`~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`),
headless under `xvfb-run -a env -u PYTHONPATH`, whole test run serialized
under a heavy-test `flock` (lock file on workspace disk — `/tmp` is a
512 MB tmpfs that was at 100% during this lane, filled by other lanes'
scratch; nothing of theirs was touched). Free-RAM gate checked before
the run: 3,572 MB available at first check (test wedge is tiny:
≤120×96 px, 8 Cycles samples).

## Finding during the test (fixed, documented in README)
First run used `BLENDER_EEVEE_NEXT`: every variant aborted —
`Couldn't open libEGL.so.1` (no loadable EGL/GPU stack for Eevee on
this VM). Switched the example/test wedges to the studio's proven
headless pattern, **Cycles on CPU** (the Cape Jones `render_proof.py`
donor pattern), with `cycles.device: CPU`. Re-test passed in full.

## Run 1 — resilience wedge (`examples/test_wedge_with_broken.json`, 4 variants)

```
[wedgerunner] ok_small: ok (28.48s)
[wedgerunner] broken_deliberate: failed (18.51s)
[wedgerunner] ok_big_after_broken: ok (16.49s)
[wedgerunner] ok_wide_after_broken: ok (28.02s)
[wedgerunner] done: 3/4 ok -> test_out/summary.json   (runner exit 0, non-strict)
```

Verified against the files on disk afterwards (not just the runner's word):
- `summary.json` counts: total 4, ok 3, failed 1, timeout 0.
- Each ok variant: render exists, SHA-256 in summary == SHA-256 recomputed
  from disk; sizes 6,824 / 9,991 / 9,696 bytes; resolutions 96×96, 96×96,
  120×80 as wedged; renders genuinely differ (306 / 700 / 660 distinct
  colours — different cube scale, colour and light energy per variant).
- `broken_deliberate` (`__fail__: true`): status `failed`, Blender exit
  code 1, no render file, its `blender.log` contains the deliberate-failure
  RuntimeError — and the two variants after it still completed.
- Contact sheet: `contact_sheet.png` 768×278, 20,479 bytes, non-trivial
  (copy kept as `tests/sample_contact_sheet.png`); `index.html` preview
  page written (1,807 bytes). Sample summary kept as
  `tests/sample_summary.json`.

## Run 2 — shipped example wedge (`examples/example_wedge.json`, 3 variants)

```
[wedgerunner] small_red: ok (19.6s)
[wedgerunner] big_green_bright: ok (17.41s)
[wedgerunner] wide_blue_dim: ok (17.97s)
[wedgerunner] done: 3/3 ok   (runner exit 0)
```
Render sizes 11,447 / 16,105 / 14,974 bytes — all three distinct.
