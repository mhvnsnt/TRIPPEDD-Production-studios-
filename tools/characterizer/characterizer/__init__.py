"""Characterizer - mocap bone-mapping profiles + retarget polish.

SPEC M-1 + M-2 from docs/BUILD-MAP-FREE-VERSIONS.md (TRIPPEDD stack).
Clean-room original code: behaviour studied from the public Autodesk
HumanIK documentation only. No paid tool's code, and no Rokoko plug-in
code, is included or derived from; only the bone-list UX concept is
shared with the Rokoko plug-in.

Install: copy the ``characterizer`` folder into Blender's addons folder
(or zip this folder's parent), enable "Animation: Characterizer".
Profiles live in ``../profiles/*.json`` next to this package; point the
panel's Profiles Folder at any folder of profile JSONs to use your own.
"""

bl_info = {
    "name": "Characterizer (mocap profiles + retarget polish)",
    "author": "TRIPPEDD Production Studios (clean-room build)",
    "version": (1, 2, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Characterizer",
    "description": "Named bone-mapping profiles, rest-offset-corrected "
                   "retarget baking to a new NLA-ready action, plus "
                   "stride / floor / foot-skate polish operators.",
    "category": "Animation",
}

import bpy

from . import operators, panels

_CLASSES = operators.CLASSES + panels.CLASSES


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    operators.register_scene_props()


def unregister():
    operators.unregister_scene_props()
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
