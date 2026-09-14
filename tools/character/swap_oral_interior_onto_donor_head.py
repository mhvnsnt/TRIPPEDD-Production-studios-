#!/usr/bin/env python3
"""Clean oral assembly: good HOST head + good INTERIOR parts.

Stop trying to heal a mesh whose lip seam / boolean already shredded weights
and created non-manifold shards. Swap parts instead.

Strategy (Gemini-aligned, repo assets):
  1. Open HOST blend = known-good mouth cavity + lip topology + skin weights
     (default: assets/rigs/MARS_ORAL.blend from commit 904b419 anchor, or
     assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend).
  2. Delete ONLY interior oral meshes (teeth/gums/tongue) from HOST.
     Do not touch head surface, cavity walls, mouth sock, or armature weights
     on the shell.
  3. Append INTERIOR objects from CURRENT blend (seated tongue, improved teeth).
  4. Parent interior to HOST armature; rigid map teeth	o jaw / tongue	o tongue_*
     when those bones exist.
  5. Save REVIEW_ONLY blend. Canonical is never the default write target.

  blender -b -P tools/character/swap_oral_interior_onto_donor_head.py -- \\
    --host assets/rigs/MARS_ORAL.blend \\
    --interior assets/rigs/MARS_FACE.blend \\
    --out assets/variants/MARS_ORAL_SWAP_REVIEW.blend

Object-name patterns are loose; pass --list-only first on each file if unsure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--host",
        default="assets/rigs/MARS_ORAL.blend",
        help="Known-good head+cavity+weights blend",
    )
    ap.add_argument(
        "--interior",
        default="assets/rigs/MARS_FACE.blend",
        help="Current blend holding improved teeth/gums/tongue",
    )
    ap.add_argument(
        "--out",
        default="assets/variants/MARS_ORAL_SWAP_REVIEW.blend",
        help="Review-only output (never default to canonical path)",
    )
    ap.add_argument(
        "--list-only",
        action="store_true",
        help="Print mesh/armature names from host and interior, then exit",
    )
    ap.add_argument(
        "--report",
        default="docs/evidence/mars/mouth/oral_interior_swap_report.json",
    )
    return ap.parse_args(argv)


def die(msg: str) -> None:
    print(f"\n*** REFUSED: {msg}\n", flush=True)
    sys.exit(1)


# Host: remove these (interior only). Sock/cavity walls stay with the good head.
INTERIOR_DELETE = re.compile(
    r"(TEETH|TOOTH|GUM|TONGUE|ORAL_TEETH|ORAL_GUM|ORAL_TONGUE)",
    re.I,
)
# Never delete these from host even if name partially matches
HOST_KEEP = re.compile(
    r"(MESH|SURFACE|CANONICAL|SOCK|CAVITY|VOID|SHELL|HEAD|FACE|RIG|ARMATURE)",
    re.I,
)
# Append from interior
INTERIOR_HARVEST = re.compile(
    r"(TEETH|TOOTH|GUM|TONGUE|ORAL_TEETH|ORAL_GUM|ORAL_TONGUE)",
    re.I,
)


def is_interior_delete(name: str) -> bool:
    if not INTERIOR_DELETE.search(name):
        return False
    # Keep sock/cavity/host surface
    if re.search(r"(SOCK|CAVITY|VOID|SURFACE|MESH|CANONICAL)", name, re.I):
        if not re.search(r"(TEETH|TOOTH|GUM|TONGUE)", name, re.I):
            return False
    return True


def is_harvest(name: str) -> bool:
    if not INTERIOR_HARVEST.search(name):
        return False
    if re.search(r"(SOCK|CAVITY|VOID|SURFACE|MESH|CANONICAL|REPAIRED_SURFACE)", name, re.I):
        if not re.search(r"(TEETH|TOOTH|GUM|TONGUE)", name, re.I):
            return False
    return True


def scene_inventory():
    rows = []
    for ob in bpy.data.objects:
        rows.append(
            {
                "name": ob.name,
                "type": ob.type,
                "verts": len(ob.data.vertices) if ob.type == "MESH" and ob.data else None,
                "parent": ob.parent.name if ob.parent else None,
            }
        )
    return rows


def find_armature():
    for name in ("MARS_RIG", "RIG", "Armature"):
        ob = bpy.data.objects.get(name)
        if ob and ob.type == "ARMATURE":
            return ob
    arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    return arms[0] if arms else None


def parent_to_armature(ob, arm):
    if arm is None:
        return
    ob.parent = arm
    ob.parent_type = "OBJECT"
    # Prefer bone parenting for rigid dental / tongue when bones exist
    bones = arm.data.bones if arm.data else None
    if not bones:
        return
    n = ob.name.upper()
    bone_name = None
    if "TONGUE" in n:
        for cand in ("tongue_root", "tongue_mid", "tongue", "jaw"):
            if cand in bones:
                bone_name = cand
                break
    elif "TEETH" in n or "TOOTH" in n or "GUM" in n:
        if "LOWER" in n or "_LO" in n or "BOT" in n:
            for cand in ("jaw", "teeth_lower", "lower_teeth"):
                if cand in bones:
                    bone_name = cand
                    break
        else:
            for cand in ("head", "teeth_upper", "upper_teeth", "spine.006"):
                if cand in bones:
                    bone_name = cand
                    break
    if bone_name:
        ob.parent_type = "BONE"
        ob.parent_bone = bone_name


def main():
    a = parse_args()
    host = Path(a.host).resolve()
    interior = Path(a.interior).resolve()
    out = Path(a.out).resolve()
    if "assets/rigs/MARS_FACE.blend" in str(out) or out.name == "MARS_FACE.blend":
        die("refusing to write swap result over canonical MARS_FACE.blend — use variants/")

    if not host.is_file():
        die(f"host not found: {host}")
    if not interior.is_file():
        die(f"interior not found: {interior}")

    # --- inventory mode: load each file briefly
    if a.list_only:
        report = {"host": str(host), "interior": str(interior), "host_objects": [], "interior_objects": []}
        bpy.ops.wm.open_mainfile(filepath=str(host))
        report["host_objects"] = scene_inventory()
        bpy.ops.wm.open_mainfile(filepath=str(interior))
        report["interior_objects"] = scene_inventory()
        print(json.dumps(report, indent=2))
        return

    # 1) Open host (good cavity + weights)
    bpy.ops.wm.open_mainfile(filepath=str(host))
    host_before = scene_inventory()
    arm = find_armature()

    # 2) Delete interior-only meshes from host
    deleted = []
    for ob in list(bpy.data.objects):
        if ob.type != "MESH":
            continue
        if is_interior_delete(ob.name):
            deleted.append(ob.name)
            bpy.data.objects.remove(ob, do_unlink=True)

    # 3) Append harvest objects from interior blend
    with bpy.data.libraries.load(str(interior), link=False) as (data_from, data_to):
        want = [n for n in data_from.objects if is_harvest(n)]
        data_to.objects = want

    appended = []
    for ob in data_to.objects:
        if ob is None:
            continue
        # Link into scene
        if ob.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(ob)
        parent_to_armature(ob, arm)
        appended.append(ob.name)

    if not appended:
        die(
            "no interior objects harvested — run with --list-only and pass matching names. "
            f"interior file={interior}"
        )

    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))

    report = {
        "schema": "god-molecule.oral-interior-swap.v1",
        "status": "REVIEW_ONLY",
        "host": str(host),
        "interior": str(interior),
        "out": str(out),
        "deleted_from_host": deleted,
        "appended_from_interior": appended,
        "armature": arm.name if arm else None,
        "host_object_count_before": len(host_before),
        "note": (
            "Host keeps cavity/sock/shell/weights. Interior teeth/gums/tongue replaced. "
            "Do not promote without open-mouth pixels + SHA + mouth_proof."
        ),
        "authority": "docs/evidence/MARS_ORAL_KNOWN_GOOD_RECOVERY.json",
    }
    rep = Path(a.report)
    rep.parent.mkdir(parents=True, exist_ok=True)
    rep.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"ORAL_INTERIOR_SWAP: REVIEW_ONLY -> {out}")


if __name__ == "__main__":
    main()
