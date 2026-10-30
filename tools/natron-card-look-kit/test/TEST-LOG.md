# Test log — Natron card + LOOK kit

**Run:** 2026-10-30, this box, Natron **2.5.0** headless
(`~/workspace/tools/natron/natron-render.sh` → NatronRenderer),
serialized via `flock /tmp/heavy-test.lock`, RAM gate passed
(3,571 MB available at launch). Reproduce: `test/run_test.sh`.

**Method:** `make_test_image.py` (muted colour blocks, 256×256) →
one Natron graph per gizmo (`Read → gizmo → Write`, frame 1) via
`run_natron_test.py` → pixel metrics via `metrics.py` (PIL).

## Result: PASS (all five gizmos)

```
input:        mean_sat=0.3426  mean_rgb=(143.5, 139.8, 137.2)
look2:        mean_sat=0.4363  delta=+0.0937   PASS saturation up > +0.03
look1:        mean_sat=0.2592  delta=-0.0834   PASS saturation down > -0.03
led_purple:   mean_rgb=(171.5, 151.8, 180.1)   (B-R) in=-6.2 out=+8.6
                                               PASS B-R shift up > +5
led_party:    output exists (7,922 B)          PASS
card:         mean_abs_diff vs input=44.479    PASS moved (diff > 1.0)
RESULT PASS
RESULTS {'look2': True, 'look1': True, 'led_purple': True,
         'led_party': True, 'card': True}   (all Write nodes rendered)
```

Output SHA-256 (this run): out_look2 `90eca0fb…d611`, out_look1
`7cec8eef…9007`, out_led_purple `fcc2d3a5…3eb8`, out_led_party
`de6cc0b9…68c30b`, out_card `cd50c23e…8115`, input `6ea41654…e943`.

Card chain detail: knobs set from the test script —
`camPanX=40, depth=1.0, camZoom=1.0` — and logged as applied
(`CHAIN out_card knob camPanX = 40.0` etc.) before rendering.

## Grounding probes from the same run

The test script dumps the installed Natron's real plugin parameters;
the gizmos were written/fixed against these, not guesses:

- `net.sf.openfx.SaturationPlugin` v2 — param `saturation` ✓
- `net.sf.openfx.GradePlugin` v1 — `blackPoint`, `whitePoint`, `gamma`
  (a **4-dimension colour param**), `multiply`, `offset`, `mix` ✓
- `net.sf.openfx.MultiplyPlugin` v2 — param `value` ✓
- `net.sf.openfx.MergePlugin` v1 — `operation`, `mix` ✓
- `net.sf.cimg.CImgBlur` v3 — param `size` ✓
- `net.sf.openfx.CornerPinPlugin` v1 — `to1..to4`, `from1..from4` ✓
- `net.sf.openfx.TransformPlugin` v1 — `translate`, `scale`, `rotate` ✓

## Donor verification (N-1, PM_Card3D + PM_Camera)

Same box, same discipline (flock, RAM gate passed at 3,225 MB after a
wait — two earlier attempts aborted honestly at the gate / on a wiped
/tmp). Script: `test/run_donor_test.py`, donor installed from
`card-kit/community-donor/` into the Natron PyPlugs subfolders.

```
DONOR_IN_PLUGIN_IDS PM_Card3D True
DONOR_IN_PLUGIN_IDS PM_Camera True
PM_Camera CREATE True            (label PM_Camera1)
PM_Card3D CREATE True            (label PM_Card3D1, 3 inputs)
PM_Card3D CAMERA_CONNECTED_ON_INPUT 1
PM_Card3D RENDER_OUTPUT_EXISTS True  out_donor_card.png  8,203 B
donor card mean_abs_diff vs input = 140.167 (card transformed in 3D
by the donor's default camera/card settings — strongly non-identity)
out_donor_card.png SHA-256 e5bc36228e8cb11b…5192e4bb
PM_Card3D.py  SHA-256 4e807c52eed5c72fa4551d614ebc7e362603e6d8d4168fd662844bfe8814a466
PM_Camera.py  SHA-256 3027c85030d985d3187e97227898afdf04d27eefe4b39c0d7711c99d98166f60
```

**N-1 verdict: donor adopted and verified** — PM_Card3D + PM_Camera
load in Natron 2.5.0, connect (camera on card input 1), and render.

## Honest failure history (kept, not dressed up)

1. **First full run:** all 5 outputs rendered, but metrics FAILED —
   LOOK 2 saturation went *down* (−0.118) and LED B−R shift was only
   +4.1. Two causes, both fixed: (a) Grade `gamma` had its expression
   set on the red dimension only (it is a 4-dim colour param — see
   probe above); gizmos now set gamma on all dimensions. (b) The first
   test image used pure primary colours, which are already at maximum
   HSV saturation and clip under a saturation multiplier — the test
   image now uses muted, plate-like colours. An earlier partial run
   was also killed mid-render by an external session timeout (LOOK 1
   output truncated at 0 B); the re-run was detached and completed.
2. **PMCard3D / PMcamera (N-1 donor) — first draft was WRONG:**
   this lane initially recorded the donor as unfetchable (a clone
   checkout failed on a full /tmp; the search missed the underscored
   filenames `PM_Card3D.py` / `PM_Camera.py`). Corrected the same
   day, before merge: the donor was fetched from
   `NatronGitHub/natron-plugins`, adopted unmodified, and verified
   as above. Full corrected record in
   `docs/SOURCES-AND-PROVENANCE.md`.
