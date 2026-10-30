# Card kit (N-1) — what's here

- **Donor (adopted, donor-first):** `community-donor/PM_Card3D/` +
  `community-donor/PM_Camera/` — the Natron community scripts
  (PMCard3D / PMcamera in the Natron docs), fetched unmodified from
  `NatronGitHub/natron-plugins` (`Transform/3D_Card/PM_Card3D.py`,
  `Transform/PM_Camera/PM_Camera.py`). Installed into this box's
  Natron 2.5.0 PyPlugs by `../gizmos/install_gizmos.sh`; load + render
  verified headless — see `../test/TEST-LOG.md`.
- **Studio companion group:** `../gizmos/TrippeddCard25D.py` — the
  fast 2.5D pan/zoom-parallax card move (Pipeline One's house move)
  that does not need a 3D camera node. The donor is the route for a
  real in-comp 3D camera; this group is the route for flat
  pan-and-zoom cards. Decision rule: `../docs/CARD-PROJECTION-RECIPE.md`.
- **Recipe:** `../docs/CARD-PROJECTION-RECIPE.md` (Route A donor in
  Natron, Route A2 studio group, Route B Blender camera-mapped
  planes — with the per-shot decision rule).
- **Correction note:** an earlier draft of this kit recorded the donor
  as "could not be fetched". That was wrong — the first clone's
  checkout failed on a full /tmp and the underscored filenames
  (`PM_Card3D.py`, not `PMCard3D.py`) were missed in the search. The
  donor was there all along; the corrected fetch record is in
  `../docs/SOURCES-AND-PROVENANCE.md`.
