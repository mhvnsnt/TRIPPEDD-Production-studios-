# Natron Card + LOOK Kit (SPEC N-1 + N-3)

Free-versions build map, section 5 (Nuke vs Natron): the two small specs
that close Natron's gaps for our shows.

| Spec | What shipped | Status |
|---|---|---|
| **N-1 Card projection kit** | Donor adopted: `card-kit/community-donor/` PM_Card3D + PM_Camera (Natron community scripts, unmodified, installed into Natron 2.5.0) + companion `gizmos/TrippeddCard25D.py` + `docs/CARD-PROJECTION-RECIPE.md` (all routes + decision rule) | **Shipped.** Donor load/render verified headless (test log). An earlier draft wrongly recorded the donor as unfetchable — correction in `docs/SOURCES-AND-PROVENANCE.md`. |
| **N-3 Studio gizmo pack** | `gizmos/CJLook1PaleWash.py`, `gizmos/CJLook2DeepSaturation.py`, `gizmos/CJLedDeepPurpleGlow.py`, `gizmos/CJLedPartyGlow.py` + `docs/LOOKS-AND-LED-KNOBS.md` | **Shipped + verified headless** (see `test/TEST-LOG.md`). The gizmos package the existing cape-jones recipes — they do not invent new looks. |

## What this is for

- **Wizard Gang** — Pipeline One's signature move is pan-and-zoom
  parallax over flat cards. `TrippeddCard25D` is that move as a Natron
  group: one virtual-camera pan, per-card Depth, differential motion.
- **Cape Jones** — the TV-parallel gag is a card trick (TV content card
  locked to camera, room cards at depth), and every episode finishes
  with LOOK 1 / LOOK 2 + LED grades. Those looks now exist as named
  Natron groups instead of per-shot graphs.

## Layout

```
gizmos/    Natron PyPlug groups (.py) — install into any Natron 2.5.0
           PyPlugs folder with gizmos/install_gizmos.sh
docs/      CARD-PROJECTION-RECIPE.md  — the two projection routes + rule
           LOOKS-AND-LED-KNOBS.md     — every gizmo, every knob, sources
           SOURCES-AND-PROVENANCE.md  — donor fetch record, recipe sources
test/      headless test (make image -> Natron render -> pixel metrics)
INSTALL.md install note for this box + any other Natron 2.5.0
```

## Canon sources (do not re-derive)

- LOOK 1 PALE WASH / LOOK 2 DEEP SATURATION: `mhvnsnt/cape-jones`
  `docs/lighting/RENDER-LOOKS.md` + `production/pipeline/render_looks.py`
  (PR #264). LOOK 1 = AgX (Blender built-in), LOOK 2 = ACES 1.0 - SDR
  Video via the ACES cg-config OCIO file.
- Grades + LED: `mhvnsnt/cape-jones` `production/pipeline/grades.py`,
  `production/pipeline/led_controller.py`,
  `production/pipeline/comp_glow.py`.
- Stack order (canon): **lights → render look → finish grade.**
