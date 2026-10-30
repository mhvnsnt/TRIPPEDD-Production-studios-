# Sources and provenance

## N-1 donor record (PMCard3D / PMcamera) — ADOPTED, with a correction

Spec N-1 is donor-first: adopt PMCard3D / PMcamera from the Natron
CommunityScripts.

**Correction (2026-10-30, same lane, before merge):** the first draft
of this file recorded the donor as "could not be fetched". That was
**wrong**. The first clone of `NatronGitHub/natron-plugins` failed its
working-tree checkout on a full /tmp tmpfs, and the follow-up search
looked for `PMCard3D` as one word — the real files use underscores.
The donor was in the repo the whole time:

- `Transform/3D_Card/PM_Card3D.py` (+ `PM_Card3DExt.py`, `.png`, `.xml`)
  — plugin ID `natron.community.plugins.PM_Card3D`, "Poor's Man
  Card3D, create a 3D plane, to be used with PM_Camera"
  (PM_Card3D.xml package description).
- `Transform/PM_Camera/PM_Camera.py` (+ `PM_CameraExt.py`, `.png`,
  `.xml`) — plugin ID `natron.community.plugins.PM_Camera`.

**Adoption:** both plugins were fetched unmodified from
`NatronGitHub/natron-plugins` master on 2026-10-30, shipped in this
kit under `card-kit/community-donor/`, and installed into this box's
Natron 2.5.0 PyPlugs (subfolder layout, matching how the community
collection installs). Load + render verification: `test/TEST-LOG.md`
(donor section). SHA-256 of the two main files as fetched:
PM_Card3D.py `4e807c52eed5c72f…`, PM_Camera.py `3027c85030d985d3…`
(full hashes in the test log).

The studio's own `TrippeddCard25D` group remains in the kit as the
companion for flat pan-and-zoom cards (the donor pair is a real
minimal 3D system — camera + card — and is the route when a shot
needs it; see the decision rule in `CARD-PROJECTION-RECIPE.md`).

License: the natron-plugins collection is the Natron community's
open-source (GPL-family, same as Natron) PyPlug collection; the files
are Natron PyPlug-exporter output and are redistributed here
unmodified with attribution, for use inside Natron.

## N-3 recipe sources (all from mhvnsnt/cape-jones, read 2026-10-30)

- `docs/lighting/RENDER-LOOKS.md` and `production/pipeline/render_looks.py`
  — LOOK 1 PALE WASH (AgX) / LOOK 2 DEEP SATURATION (ACES 1.0 - SDR
  Video, ACES cg-config OCIO). Fetched via the GitHub API from main
  (the local cape-jones clone is sparse and does not carry these paths).
- `production/pipeline/grades.py` — the grade family: CJ_DAY
  (sat 1.35, contrast 1.08, channel matrix rr=1.05 rb=0.05 / gb=0.05 /
  br=0.08 bb=1.10), CJ_ROYAL (sat 1.45, contrast 1.10), OUTSIDE_ACID
  (sat 2.0), OUTSIDE_STORM (sat 0.85), LED_DEEP_PURPLE, LED_PARTY and
  the other static LED grades — values quoted in
  `LOOKS-AND-LED-KNOBS.md`.
- `production/pipeline/led_controller.py` — animated LED presets
  (hue/brightness time expressions over the static grades). Not ported:
  Natron groups here are the static comp form.
- `production/pipeline/comp_glow.py` — glow recipes: bloom = blur a
  copy, screen-blend back; presets `neon-sign` (glow 0.6) and
  `energy-blast` (glow 1.0) used by the LED gizmos.

## Original code in this kit

The five studio gizmo `.py` files (CJ LOOK 1/2, CJ LED ×2,
TrippeddCard25D) are original NatronEngine code written for this kit
(chain structure follows Natron's own bundled PyPlugs — Input /
Output / OFX node IDs — which are Natron's public plugin API).
Node IDs and versions were probed against the installed Natron 2.5.0
(e.g. `net.sf.openfx.SaturationPlugin` v2.0 loads in its OFX cache);
every gizmo sets parameters defensively (candidate names + static
fallbacks) so a missing optional parameter degrades the chain instead
of breaking the group. The donor files under
`card-kit/community-donor/` are **not** original — they are the
community's, unmodified (see above).
