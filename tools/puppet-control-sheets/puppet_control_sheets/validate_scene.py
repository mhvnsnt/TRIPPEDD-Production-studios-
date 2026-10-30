#!/usr/bin/env python3
"""
Structural validator for a Puppet Control Sheets scene.

NOTE: .tnz is XML-*like* but not guaranteed well-formed XML (real
Tahoma2D/OpenToonz scene files fail strict XML parsing), so this
validator does a tolerant structural scan instead of ElementTree.
The authoritative load test is Tahoma2D itself -- render a frame with
tcomposer (see README / test-output/VALIDATION-LOG.md).

Checks:
  * every part level in the levelSet exists as files on disk,
  * CTRL_ROOT exists and every CTRL_* pegbar's parent chain reaches Table,
  * every part column's Col<N> pegbar is parented to its CTRL_<PART> peg,
  * every pose in poses.json has matching keyframes on its control pegs,
  * tag balance for the main containers.

Usage: python3 validate_scene.py SCENE.tnz [--poses poses.json]
Exit code 0 = all checks passed.
"""

import argparse
import json
import os
import re
import sys


def pegbars(tnz):
    out = {}
    for m in re.finditer(r'<pegbar[^>]* id="([^"]+)">(.*?)</pegbar>',
                         tnz, re.S):
        body = m.group(2)
        parent = re.search(r'<parent[^>]* id="([^"]+)"', body)
        name = re.search(r'<name>\s*(\S+)\s*</name>', body)
        out[m.group(1)] = {
            "parent": parent.group(1) if parent else None,
            "name": name.group(1) if name else None,
            "body": body,
        }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("--poses")
    args = ap.parse_args(argv)
    failures = []

    def check(ok, label):
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            failures.append(label)

    with open(args.scene) as fh:
        tnz = fh.read()
    scene_dir = os.path.dirname(os.path.abspath(args.scene))

    check(tnz.lstrip().startswith("<tnz"), "tnz root element present")
    for tag in ("levelSet", "xsheet", "columns", "pegbars", "fxnodes"):
        # <xsheet> legitimately appears twice: the sheet itself and the
        # xsheet node inside <fxnodes> (real Tahoma2D files do this too)
        check(tnz.count(f"<{tag}>") == tnz.count(f"</{tag}>") >= 1,
              f"<{tag}> balanced and present")

    pegs = pegbars(tnz)
    # Tahoma stage-object ids are Peg<N>/Col<N>/Table/Camera<N>; the
    # CTRL_* identity is the pegbar <name>. Map name -> id.
    by_name = {v["name"]: k for k, v in pegs.items() if v["name"]}
    check("CTRL_ROOT" in by_name, "CTRL_ROOT control peg present")
    root_id = by_name.get("CTRL_ROOT")
    check(pegs.get(root_id, {}).get("parent") == "Table",
          "CTRL_ROOT parented to Table")

    def reaches_table(peg_id, seen=None):
        seen = seen or set()
        while peg_id not in ("Table", "None", None):
            if peg_id in seen or peg_id not in pegs:
                return False
            seen.add(peg_id)
            peg_id = pegs[peg_id]["parent"]
        return peg_id == "Table"

    ctrls = sorted(n for n in by_name if n.startswith("CTRL_"))
    for c in ctrls:
        check(reaches_table(by_name[c]), f"{c} parent chain reaches Table")

    # levels + files on disk
    levels = re.findall(
        r"<level id='(\d+)'>\s*(\S+)\s*<info[^/]*/>\s*<path>\s*\"([^\"]+)\"",
        tnz)
    check(len(levels) > 0, f"{len(levels)} levels declared")
    for _lid, name, path in levels:
        rel = path.replace("$scenefolder\\\\", "").replace("\\\\", "/")
        base = os.path.join(scene_dir, os.path.dirname(rel),
                            os.path.basename(rel).replace("..", ".0001."))
        check(os.path.exists(base), f"level {name}: first drawing on disk")

    # each level has a column; each column peg rides under its CTRL peg
    col_pegs = sorted(p for p in pegs if re.fullmatch(r"Col\d+", p))
    check(len(col_pegs) == len(levels),
          f"one column peg per level ({len(col_pegs)}/{len(levels)})")
    for cp in col_pegs:
        parent = pegs[cp]["parent"]
        parent_name = pegs.get(parent, {}).get("name")
        check(parent_name is not None and parent_name.startswith("CTRL_"),
              f"{cp} parented under a control peg ({parent} = {parent_name})")

    if args.poses and os.path.exists(args.poses):
        with open(args.poses) as fh:
            sidecar = json.load(fh)
        for pose_name, pose in sidecar.get("poses", {}).items():
            frame = pose["frame"]
            for ctrl, channels in pose.get("transforms", {}).items():
                body = pegs.get(by_name.get(ctrl, ""), {}).get("body", "")
                for ch, value in channels.items():
                    ch = {"angle": "rot"}.get(ch, ch)  # tnz tag name
                    pat = (rf"<{ch}>.*?<L>(?:\s*<prev>.*?</prev>)?\s*"
                           rf"{frame} {float(value):g}\s*</L>")
                    check(re.search(pat, body, re.S) is not None,
                          f"pose {pose_name}: {ctrl}.{ch} keyframe "
                          f"@f{frame} = {value}")
    print("RESULT:", "PASS" if not failures else f"FAIL ({len(failures)})")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
