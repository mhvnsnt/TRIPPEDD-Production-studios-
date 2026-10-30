"""Generate pyro_presets.blend: the preset library file for the Pyro Shaping Pack.

For every look in presets/*.json this builds, in its own collection:
  - the domain cube with the preset's Mantaflow domain settings,
  - the flow emitter with the preset's flow settings,
  - the matching Cycles volume material (PyroVol_<look>),
  - a text block holding the look's JSON parameter sheet verbatim.

The JSONs + pyro_lib.py are the source of truth; this .blend is a generated
convenience (append/link the collection or material into a shot file).
Regenerate with:
  blender -b --factory-startup --python build_presets.py
"""
import json
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyro_lib  # noqa: E402

OUT = os.path.join(pyro_lib.PACK_DIR, "pyro_presets.blend")


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for name in pyro_lib.list_looks():
        preset = pyro_lib.load_preset(name)
        report, domain, flow = pyro_lib.apply_look(name)
        coll = bpy.data.collections.new("Pyro_" + name)
        bpy.context.scene.collection.children.link(coll)
        for obj in (domain, flow):
            for parent in list(obj.users_collection):
                parent.objects.unlink(obj)
            coll.objects.link(obj)
        txt = bpy.data.texts.new("preset_" + name + ".json")
        txt.write(json.dumps(preset, indent=2, sort_keys=True))
        print("LIBRARY LOOK BUILT:", report)
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("SAVED", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
