# VRM-Addon-for-Blender headless smoke test — Wave 10 Lane A

**Wire-up:** `vrm_smoke.py` installs saturday06/VRM-Addon-for-Blender v4.7.2
(dual MIT OR GPL-3.0-or-later — **MIT option chosen** for commercial safety)
into a scratch Blender user-scripts dir, enables it headless, and imports
the three-vrm sample VRM (`VRM1_Constraint_Twist_Sample.vrm`, MIT repo
pixiv/three-vrm).

**Run:**
```bash
BLENDER_USER_SCRIPTS=/tmp/vrmwire/user VRM_PATH=/path/to/model.vrm \
  OUT_DIR=./proofs blender --background --python vrm_smoke.py
```
(The scratch `user/addons/io_scene_vrm` dir is NOT committed — download the
release zip and unzip it there; the addon zip and sample VRM stay out of git.)

**Proof (2026-10-07, Blender 4.0.2 headless):**
- `proofs/vrm_import_census.json` — addon enabled: true; 1 armature,
  **167 bones** (J_Bip_* humanoid naming, hips root present), 5 meshes
  (Body/Face/Hair + the sample's own Cube/Icosphere test props)
- `proofs/vrm_import_thumb.png` — 256px workbench render of the imported
  character, **visually verified**: full-body anime figure, arms in T-pose,
  head/torso/legs intact. (Sample's Cube/Icosphere test props hidden for the
  shot; documented in the script.)

**Production use:** this is the VRM↔Blender bridge for the anime pipeline —
import VRM characters, retarget/animate in Blender, export onward.
