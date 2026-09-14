#!/usr/bin/env python3
"""Assemble the oral system without touching the face shell.

Authority:
  HOST = the pre-retopo MARS_FACE checkpoint. It carries the clean facial
         surface, mouth opening/cavity, mouth sock, armature and skin weights.
  INTERIOR = current MARS_FACE. It carries the improved GNM teeth/gums/tongue.

This is deliberately NOT a lip-seam repair. It never cuts, booleans, remeshes,
triangulates, welds, or reweights MARS_MESH. It replaces only the three
standalone GNM oral interior objects:
  MARS_TEETH_UPPER (teeth + gums)
  MARS_TEETH_LOWER (teeth + gums)
  MARS_TONGUE (tongue + expression keys)

MARS_MOUTH_SOCK stays with the host because the creator's known-good mouth sock
is part of the protected opening/cavity assembly.

The output is always review-only. Canonical assets are never written.
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import bpy


ORAL_NAMES = ("MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE")
PROTECTED_HOST = ("MARS_MESH", "MARS_MOUTH_SOCK", "MARS_RIG")


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--host",
        default="assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_FACE.blend",
    )
    ap.add_argument("--interior", default="assets/rigs/MARS_FACE.blend")
    ap.add_argument("--out", default="assets/variants/MARS_FACE_ORAL_ASSEMBLY_REVIEW.blend")
    ap.add_argument(
        "--report",
        default="docs/evidence/mars/mouth/oral_interior_swap_report.json",
    )
    ap.add_argument("--list-only", action="store_true")
    return ap.parse_args(argv)


def refuse(msg: str) -> None:
    print("\n*** REFUSED: " + msg, flush=True)
    raise SystemExit(45)


def inventory():
    rows = []
    for ob in bpy.data.objects:
        rows.append(
            {
                "name": ob.name,
                "type": ob.type,
                "verts": len(ob.data.vertices) if ob.type == "MESH" and ob.data else None,
                "parent": ob.parent.name if ob.parent else None,
                "modifiers": [
                    {"type": m.type, "object": m.object.name if getattr(m, "object", None) else None}
                    for m in ob.modifiers
                ],
                "shapeKeys": (
                    [k.name for k in ob.data.shape_keys.key_blocks]
                    if ob.type == "MESH" and ob.data and ob.data.shape_keys
                    else []
                ),
            }
        )
    return rows


def assert_host(host: Path):
    for p in PROTECTED_HOST:
        if bpy.data.objects.get(p) is None:
            refuse("host is not the required pre-retopo MARS_FACE: missing " + p)
    if bpy.data.objects["MARS_MESH"].type != "MESH":
        refuse("MARS_MESH is not a mesh")
    if bpy.data.objects["MARS_RIG"].type != "ARMATURE":
        refuse("MARS_RIG is not an armature")
    # A clean host must be the 23,830-vertex pre-retopo surface, not the
    # 27,865-vertex shredded post-split surface.
    hv = len(bpy.data.objects["MARS_MESH"].data.vertices)
    if hv != 23830:
        refuse("host MARS_MESH vertex count is %d; expected clean 23,830 checkpoint surface" % hv)


def source_object_names(interior: Path):
    with bpy.data.libraries.load(str(interior), link=False) as (src, dst):
        available = set(src.objects)
    missing = [n for n in ORAL_NAMES if n not in available]
    if missing:
        refuse("current interior is missing exact GNM objects: " + ", ".join(missing))
    return available


def delete_host_interior():
    deleted = []
    for name in ORAL_NAMES:
        ob = bpy.data.objects.get(name)
        if ob is not None:
            deleted.append(
                {
                    "name": name,
                    "verts": len(ob.data.vertices) if ob.type == "MESH" and ob.data else None,
                    "shapeKeys": (
                        len(ob.data.shape_keys.key_blocks)
                        if ob.type == "MESH" and ob.data and ob.data.shape_keys
                        else 0
                    ),
                }
            )
            bpy.data.objects.remove(ob, do_unlink=True)
    return deleted


def append_current_interior(interior: Path, host_arm):
    with bpy.data.libraries.load(str(interior), link=False) as (src, dst):
        dst.objects = list(ORAL_NAMES)

    appended = []
    for ob in dst.objects:
        if ob is None:
            refuse("Blender failed to append one of the exact oral objects")
        if ob.type != "MESH":
            refuse("%s is not a mesh" % ob.name)

        # The object is already positioned in the current face. Preserve its
        # world transform exactly while changing only its rig owner.
        world = ob.matrix_world.copy()
        ob.parent = host_arm
        ob.parent_type = "OBJECT"
        ob.matrix_world = world

        # Rebind every Armature modifier to the HOST rig. Never let an object
        # retain a pointer to an armature from the interior source file.
        arm_mods = [m for m in ob.modifiers if m.type == "ARMATURE"]
        if not arm_mods:
            m = ob.modifiers.new("MARS_ORAL_HOST_RIG", "ARMATURE")
            arm_mods = [m]
        for m in arm_mods:
            m.object = host_arm

        # The GNM meshes must retain their source vertex groups/shape keys.
        if ob.name == "MARS_TONGUE":
            keys = ob.data.shape_keys.key_blocks if ob.data.shape_keys else []
            if len(keys) < 2:
                refuse("current tongue lost its expression library")
            if not any(g.name == "tongue_root" for g in ob.vertex_groups):
                refuse("current tongue has no tongue_root vertex group")
        else:
            if not any(g.name == "jaw" for g in ob.vertex_groups):
                refuse("%s has no jaw vertex group" % ob.name)

        appended.append(
            {
                "name": ob.name,
                "verts": len(ob.data.vertices),
                "shapeKeys": len(ob.data.shape_keys.key_blocks) if ob.data.shape_keys else 0,
                "worldMatrixPreserved": True,
                "armature": host_arm.name,
                "materialSlots": [m.name if m else None for m in ob.data.materials],
            }
        )
    return appended


def main():
    a = args()
    host = Path(a.host).resolve()
    interior = Path(a.interior).resolve()
    out = Path(a.out).resolve()
    report_path = Path(a.report).resolve()

    if not host.is_file():
        refuse("host not found: " + str(host))
    if not interior.is_file():
        refuse("interior not found: " + str(interior))
    if out.resolve() in (host.resolve(), interior.resolve()):
        refuse("review output must not overwrite an input blend")
    if out.name in {"MARS_FACE.blend", "MARS_ORAL.blend"}:
        refuse("review output must not use a canonical asset filename")

    if a.list_only:
        report = {"host": str(host), "interior": str(interior)}
        bpy.ops.wm.open_mainfile(filepath=str(host))
        report["host_objects"] = inventory()
        bpy.ops.wm.open_mainfile(filepath=str(interior))
        report["interior_objects"] = inventory()
        print(json.dumps(report, indent=2))
        return 0

    bpy.ops.wm.open_mainfile(filepath=str(host))
    assert_host(host)
    host_arm = bpy.data.objects["MARS_RIG"]
    host_before = inventory()

    # Check the source names before mutating the host.
    source_object_names(interior)

    deleted = delete_host_interior()
    appended = append_current_interior(interior, host_arm)

    # The protected host objects must still be exactly the same identities.
    for name in PROTECTED_HOST:
        if bpy.data.objects.get(name) is None:
            refuse("protected host object disappeared: " + name)

    # No accidental duplicates. This catches the old MARS_ORAL-host approach
    # where embedded oral geometry survived and new teeth were simply stacked on.
    for name in ORAL_NAMES:
        matches = [o for o in bpy.data.objects if o.name == name]
        if len(matches) != 1:
            refuse("oral object count is not exactly one for " + name)

    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))

    report = {
        "schema": "god-molecule.oral-interior-swap.v2",
        "status": "REVIEW_ONLY",
        "host": str(host),
        "interior": str(interior),
        "out": str(out),
        "hostSurface": {
            "object": "MARS_MESH",
            "vertices": len(bpy.data.objects["MARS_MESH"].data.vertices),
            "preserved": True,
            "topologyMutated": False,
            "booleansRun": False,
            "remeshRun": False,
            "weldRun": False,
        },
        "protectedHostObjects": list(PROTECTED_HOST),
        "deletedInterior": deleted,
        "appendedInterior": appended,
        "hostArmature": "MARS_RIG",
        "currentOralSourceObjects": list(ORAL_NAMES),
        "oralObjectCount": {n: sum(1 for o in bpy.data.objects if o.name == n) for n in ORAL_NAMES},
        "promotionBlockedUntil": [
            "open-mouth rendered pixels",
            "profile silhouette check",
            "mouth_proof material survey",
            "visual human review",
        ],
        "reason": "preserve the clean pre-retopo face/cavity/weights and replace only improved GNM oral interior",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print("ORAL_INTERIOR_SWAP: REVIEW_ONLY -> " + str(out))


if __name__ == "__main__":
    main()
