#!/usr/bin/env python3
"""
SPEC T-1 "Puppet Control Sheets" -- Tahoma2D puppet scene generator.

Generates a Tahoma2D/OpenToonz `.tnz` scene that implements the studio
Puppet Control Sheet convention (see docs/CONTROL-SHEET.md):

  * a standardized hierarchy of control pegbars (CTRL_*) that group and
    drive the part columns, identical for every character,
  * one raster level per part, exposed on its own xsheet column,
  * a starter pose library: named poses stored as keyframes on the
    control pegbars in a pose block after the shot frames, plus a
    `poses.json` sidecar an animator (or the bundled ToonzScript)
    can use to apply a pose at any frame,
  * drawing-substitution levels (e.g. mouths) exposed per pose.

WHY A GENERATOR AND NOT AN IN-APP WIDGET: Tahoma2D 1.6.3 has no
master-controller / custom-widget API. Its scripting surface is
ToonzScript (QtScript/ECMAScript, File -> Run Script), which can load,
save and set cells on a scene but cannot create pegbars, keyframes or
on-canvas controls. The .tnz scene file, however, is a documented-by-
example text format, and Tahoma2D ships a headless renderer
(tcomposer). So the honest landing form for T-1 is: Python generates
the rig into the scene file; Tahoma2D animates it. See
docs/TAHOMA2D-SURFACE-NOTES.md for the full investigation.

The .tnz layout emitted here is modeled on real scenes written by
OpenToonz/Tahoma2D (levelSet / xsheet / columns / pegbars / fxnodes),
verified by rendering the generated scene with Tahoma2D 1.6.3's own
tcomposer (see test-output/VALIDATION-LOG.md).

Stdlib only. Usage:

    python3 generate_puppet_scene.py CHARACTER.json --out OUTDIR

Character JSON schema: see templates/ and examples/testpuppet.json.
"""

import argparse
import json
import math
import os
import struct
import sys
import zlib

# ---------------------------------------------------------------- PNG writer

def _png_chunk(tag, data):
    chunk = struct.pack(">I", len(data)) + tag + data
    chunk += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return chunk


def write_png(path, width, height, draw):
    """Write an RGBA PNG. `draw(x, y) -> (r, g, b, a)` per pixel."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter: none
        for x in range(width):
            raw += bytes(draw(x, y))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr)
           + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 6))
           + _png_chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)


def placeholder_drawable(part, variant):
    """A simple, clearly-a-placeholder part drawing: filled shape with a
    darker outline and a variant marker notch (so substitution drawings
    are visibly different). Returns a draw() closure."""
    w, h = part["canvas"]
    color = part.get("color", [200, 200, 200])
    dark = [max(0, c - 70) for c in color]
    shape = part.get("shape", "rect")
    cx, cy = w / 2.0, h / 2.0
    rx, ry = w * 0.32, h * 0.32

    def draw(x, y):
        dx, dy = (x - cx) / rx, (y - cy) / ry
        if shape == "ellipse":
            d = dx * dx + dy * dy
            inside, edge = d <= 1.0, d > 0.78
        else:  # rect
            inside = abs(dx) <= 1.0 and abs(dy) <= 1.0
            edge = abs(dx) > 0.86 or abs(dy) <= 1.0 and abs(dy) > 0.86
            edge = inside and (abs(dx) > 0.86 or abs(dy) > 0.86)
        if not inside:
            return (0, 0, 0, 0)
        # variant marker: filled notch whose position encodes the variant
        notch_x = cx + (variant - 1) * rx * 0.45
        if abs(x - notch_x) < 9 and abs(y - (cy - ry * 0.55)) < 9:
            return (30, 30, 30, 255)
        if edge:
            return (dark[0], dark[1], dark[2], 255)
        return (color[0], color[1], color[2], 255)

    return draw


# ------------------------------------------------------------------- tnz emit

def _param(name, default, keyframes=None):
    """One pegbar channel, in the format Tahoma2D writes:
    <x><default>v</default><keyframes><L>frame value</L>...</keyframes></x>
    Keyframes after the first carry a <prev> element (previous value)."""
    out = [f"        <{name}>", "          <default>", f"            {default:g} ",
           "          </default>"]
    if keyframes:
        out.append("          <keyframes>")
        prev = None
        for frame, value in sorted(keyframes):
            out.append("            <L>")
            if prev is not None:
                out += ["              <prev>", f"                {prev:g} ",
                        "              </prev>"]
            out.append(f"              {frame} {value:g} ")
            out.append("            </L>")
            prev = value
        out.append("            </keyframes>")
    out.append(f"          </{name}>")
    return "\n".join(out)


def _pegbar(peg_id, parent_id, channels, node_pos, extra="", name=None):
    lines = [f'      <pegbar id="{peg_id}">',
             f'        <parent handle="B" id="{parent_id}" parentHandle="B">',
             "          </parent>"]
    if name:
        lines += ["        <name>", f"          {name} ", "        </name>"]
    lines += ["        <isOpened>", "          1 ", "        </isOpened>",
             "        <center>", "          0 0 0 0 ", "        </center>",
             "        <status>", "          0 ", "        </status>"]
    # NOTE: the rotation channel serializes as <rot> in .tnz (its measure
    # name is "angle"); TStageObject::loadData rejects an <angle> tag.
    for name in ("x", "y", "rot", "sx", "sy", "sc"):
        if name in channels:
            default, keys = channels[name]
            lines.append(_param(name, default, keys))
    lines += ["        <nodePos>", f"          {node_pos[0]} {node_pos[1]} ",
              "        </nodePos>"]
    if extra:
        lines.append(extra)
    lines.append("        </pegbar>")
    return "\n".join(lines)


class IdAlloc:
    def __init__(self):
        self.n = 0

    def next(self):
        self.n += 1
        return self.n


def generate(spec, outdir):
    char = spec.get("character", "unnamed_puppet")
    slug = char.lower().replace(" ", "_")
    fps = spec.get("fps", 24)
    shot_frames = spec.get("frames", 24)
    cam_res = spec.get("camera", {}).get("res", [960, 540])
    cam_size = spec.get("camera", {}).get("size", [12.8, 7.2])
    # show templates carry the layout under "parts_template" (a character
    # file renames it to "parts" once a real character fills it in)
    parts = spec.get("parts") or spec["parts_template"]
    poses = spec.get("poses", [])
    pose_hold = spec.get("pose_hold_frames", 4)
    pose_start = shot_frames
    framecount = pose_start + max(1, len(poses)) * pose_hold

    ids = IdAlloc()
    level_id = {}
    for part in parts:
        level_id[part["name"]] = ids.next()

    # ---- placeholder / part drawings -------------------------------------
    draw_dir = os.path.join(outdir, slug)
    os.makedirs(draw_dir, exist_ok=True)
    for part in parts:
        n_drawings = part.get("drawings", 1)
        for v in range(n_drawings):
            path = os.path.join(draw_dir, f"{part['name']}.{v + 1:04d}.png")
            write_png(path, part["canvas"][0], part["canvas"][1],
                      placeholder_drawable(part, v))

    # ---- pose keyframes per control --------------------------------------
    # pose name -> frame it starts on (pose block, after the shot frames)
    pose_frames = {}
    ctrl_keys = {}  # ctrl name -> channel -> [(frame, value)]
    for i, pose in enumerate(poses):
        frame = pose_start + i * pose_hold
        pose_frames[pose["name"]] = frame
        for ctrl, channels in pose.get("transforms", {}).items():
            for ch, value in channels.items():
                ctrl_keys.setdefault(ctrl, {}).setdefault(ch, []).append(
                    (frame, float(value)))

    def ctrl_channels(name, default_x=0.0, default_y=0.0):
        keys = ctrl_keys.get(name, {})
        chans = {}
        chans["x"] = (default_x, keys.get("x"))
        chans["y"] = (default_y, keys.get("y"))
        chans["rot"] = (0.0, keys.get("angle"))
        chans["sx"] = (1.0, keys.get("sx"))
        chans["sy"] = (1.0, keys.get("sy"))
        chans["sc"] = (1.0, None)
        return chans

    # ---- columns ----------------------------------------------------------
    columns = []
    column_fx_id = {}
    pegbars = []
    # Camera + Table first (Tahoma2D writes them first, too)
    camera_block = (
        "        <camera>\n          <cameraSize>\n"
        f"            {cam_size[0]} {cam_size[1]} \n          </cameraSize>\n"
        "          <cameraRes>\n"
        f"            {cam_res[0]} {cam_res[1]} \n          </cameraRes>\n"
        "          <cameraXPrevalence>\n            1 \n"
        "          </cameraXPrevalence>\n          <interestRect>\n"
        "            0 0 -1 -1 \n          </interestRect>\n          </camera>")
    pegbars.append(
        '      <pegbar activeboth="yes" id="Camera1">\n'
        '        <parent handle="B" id="None" parentHandle="B">\n'
        "          </parent>\n        <isOpened>\n          0 \n        </isOpened>\n"
        "        <center>\n          0 0 0 0 \n        </center>\n"
        "        <status>\n          0 \n        </status>\n"
        + _param("sx", 1) + "\n" + _param("sy", 1) + "\n" + _param("sc", 1)
        + "\n        <nodePos>\n          24500 25550 \n        </nodePos>\n"
        + camera_block + "\n        </pegbar>")
    pegbars.append(_pegbar("Table", "None",
                           {"x": (0, None), "y": (0, None), "sx": (1, None),
                            "sy": (1, None), "sc": (1, None)},
                           (24500, 25450)))
    # Stage-object ids in .tnz are Tahoma's own scheme ONLY: "Table",
    # "Camera<N>", "Peg<N>", "Col<N>" (toStageObjectId() maps anything
    # else to NoneId, silently dropping the peg). The CTRL_* identity
    # therefore lives in the pegbar's <name>, and Peg numbers are
    # allocated in hierarchy order: Peg1 is always CTRL_ROOT.
    peg_id_for = {"CTRL_ROOT": "Peg1"}
    for i, part in enumerate(parts):
        peg_id_for[f"CTRL_{part['name'].upper()}"] = f"Peg{i + 2}"
    pegbars.append(_pegbar("Peg1", "Table",
                           ctrl_channels("CTRL_ROOT"), (24500, 25350),
                           name="CTRL_ROOT"))

    col_index = 0
    for part in parts:
        col_index += 1
        col_id = ids.next()
        fx_id = ids.next()
        column_fx_id[part["name"]] = fx_id
        lid = level_id[part["name"]]
        # cells: shot frames show drawing 1; substitution parts cycle
        # their drawings across the pose block so poses read differently.
        cells = []
        if part.get("drawings", 1) > 1 and poses:
            cells.append((0, shot_frames, lid, "0001"))
            for i in range(len(poses)):
                fid = f"{(i % part['drawings']) + 1:04d}"
                cells.append((pose_start + i * pose_hold, pose_hold, lid, fid))
        else:
            cells.append((0, framecount, lid, "0001"))
        cell_xml = "\n".join(
            "          <cell>\n"
            f"            {start} {count} <level id='{lid}'/>{fid} 0 \n"
            "          </cell>" for start, count, lid, fid in cells)
        columns.append(f"""      <levelColumn id='{col_id}'>
        <status>
          0
        </status>
        <cells>
{cell_xml}
          </cells>
        <fx>
          <Toonz_columnFx id='{fx_id}'>
            <params>
              </params>
            <ports>
              </ports>
            <dagNodePos>
              {25005 + col_index * 90} 25005
            </dagNodePos>
            <numberId>
              0
            </numberId>
            <name>
              LevelColumn
            </name>
            <fxId>
              ""
            </fxId>
            <opened>
              0
            </opened>
          </Toonz_columnFx>
        </fx>
      </levelColumn>""")
        # control peg for this part, parented per the character hierarchy
        parent_ctrl = part.get("parent_control", "CTRL_ROOT")
        ctrl_name = f"CTRL_{part['name'].upper()}"
        pegbars.append(_pegbar(
            peg_id_for[ctrl_name],
            peg_id_for.get(parent_ctrl, "Peg1"),
            ctrl_channels(ctrl_name,
                          default_x=part.get("offset", [0, 0])[0] / 100.0,
                          default_y=part.get("offset", [0, 0])[1] / 100.0),
            (24700 + col_index * 160, 25250 - col_index * 60),
            name=ctrl_name))
        # the column's own peg rides under its control peg
        pegbars.append(_pegbar(
            f"Col{col_index}", peg_id_for[ctrl_name],
            {"x": (0, None), "y": (0, None), "sx": (1, None),
             "sy": (1, None), "sc": (1, None)},
            (24700 + col_index * 160, 25050 - col_index * 60)))

    xsheet_fx_id = ids.next()
    output_fx_id = ids.next()
    terminal = "\n".join(
        "        <fxnode>\n"
        f"          <Toonz_columnFx id='{column_fx_id[p['name']]}'/>\n"
        "        </fxnode>" for p in parts)

    levels_xml = "\n".join(f"""      <level id='{level_id[p['name']]}'>
        {p['name']}
        <info dpiType="image"/>
        <path>
          "$scenefolder\\\\{slug}\\\\{p['name']}..png"
        </path>
      </level>""" for p in parts)
    cast_xml = "".join(f"<level id='{level_id[p['name']]}'/>" for p in parts)

    tnz = f"""<tnz framecount="{framecount}" version="71.0">
  <generator>
    "TRIPPEDD Puppet Control Sheets generator (SPEC T-1)"
  </generator>
  <properties>
    <cameras>
      <camera>
        <cameraSize>
          {cam_size[0]} {cam_size[1]}
        </cameraSize>
        <cameraRes>
          {cam_res[0]} {cam_res[1]}
        </cameraRes>
        <cameraXPrevalence>
          1
        </cameraXPrevalence>
        <interestRect>
          0 0 -1 -1
        </interestRect>
        </camera>
      </cameras>
    <outputs>
      <output name="main">
        <range>
          0 -1
        </range>
        <step>
          1
        </step>
        <shrink>
          1
        </shrink>
        <applyShrinkToViewer>
          0
        </applyShrinkToViewer>
        <fps>
          {fps}
        </fps>
        <path>
          "+outputs\\\\.png"
        </path>
        <bpp>
          32
        </bpp>
        <multimedia>
          0
        </multimedia>
        <threadsIndex>
          2
        </threadsIndex>
        <maxTileSizeIndex>
          0
        </maxTileSizeIndex>
        <subcameraPrev>
          0
        </subcameraPrev>
        <stereoscopic>
          0 0.05
        </stereoscopic>
        <resquality>
          0
        </resquality>
        <fieldprevalence>
          0
        </fieldprevalence>
        <gamma>
          1
        </gamma>
        <timestretch>
          25 25
        </timestretch>
        </output>
      <output name="preview">
        <range>
          0 -1
        </range>
        <step>
          1
        </step>
        <shrink>
          2
        </shrink>
        <applyShrinkToViewer>
          0
        </applyShrinkToViewer>
        <fps>
          {fps}
        </fps>
        <path>
          "+outputs\\\\.png"
        </path>
        <bpp>
          32
        </bpp>
        <multimedia>
          0
        </multimedia>
        <threadsIndex>
          2
        </threadsIndex>
        <maxTileSizeIndex>
          0
        </maxTileSizeIndex>
        <subcameraPrev>
          0
        </subcameraPrev>
        <stereoscopic>
          0 0.05
        </stereoscopic>
        <resquality>
          0
        </resquality>
        <fieldprevalence>
          0
        </fieldprevalence>
        <gamma>
          1
        </gamma>
        <timestretch>
          25 25
        </timestretch>
        </output>
      </outputs>
    <bgColor>
      255 255 255 0
    </bgColor>
    <markers>
      {framecount} 0
    </markers>
    <subsampling>
      1 1
    </subsampling>
    <fieldguide>
      16 1.85
    </fieldguide>
    <noteColors>
      255 235 140 255 255 160 120 255 255 180 190 255 135 205 250 255 145 240 145 255 130 255 210 255 150 245 255 255
    </noteColors>
    </properties>
  <levelSet>
    <levels>
{levels_xml}
    </levels>
    <folder name="Cast" type="default">
      <levels>
        {cast_xml}
      </levels>
      </folder>
    <folder name="Audio">
      </folder>
    </levelSet>
  <xsheet>
    <columns>
{chr(10).join(columns)}
    </columns>
    <pegbars>
{chr(10).join(pegbars)}
      <grid_dimension>
        1
      </grid_dimension>
      </pegbars>
    <fxnodes>
      <terminal>
{terminal}
      </terminal>
      <xsheet>
        <Toonz_xsheetFx id='{xsheet_fx_id}'>
          <params>
            </params>
          <ports>
            </ports>
          <numberId>
            0
          </numberId>
          <name>
            Xsheet
          </name>
          <fxId>
            ""
          </fxId>
          <opened>
            0
          </opened>
        </Toonz_xsheetFx>
      </xsheet>
      <output>
        <Toonz_outputFx id='{output_fx_id}'>
          <params>
            </params>
          <ports>
            <source>
              <Toonz_xsheetFx id='{xsheet_fx_id}'/>
            </source>
            </ports>
          <numberId>
            0
          </numberId>
          <name>
            Output
          </name>
          <fxId>
            ""
          </fxId>
          <opened>
            0
          </opened>
        </Toonz_outputFx>
      </output>
      <grid_dimension>
        1
      </grid_dimension>
      </fxnodes>
    </xsheet>
  <history>
  </history>
  </tnz>
"""

    os.makedirs(outdir, exist_ok=True)
    scene_path = os.path.join(outdir, f"{slug}.tnz")
    with open(scene_path, "w") as fh:
        fh.write(tnz)

    sidecar = {
        "character": char,
        "convention": "TRIPPEDD Puppet Control Sheets v1 (SPEC T-1)",
        "scene": os.path.basename(scene_path),
        "shot_frames": [0, shot_frames - 1],
        "pose_block_start": pose_start,
        "pose_hold_frames": pose_hold,
        "controls": ["CTRL_ROOT"] + [f"CTRL_{p['name'].upper()}" for p in parts],
        "control_pegs": peg_id_for,
        "poses": {name: {"frame": frame,
                         "transforms": next(
                             p.get("transforms", {}) for p in poses
                             if p["name"] == name)}
                  for name, frame in pose_frames.items()},
    }
    with open(os.path.join(outdir, "poses.json"), "w") as fh:
        json.dump(sidecar, fh, indent=2)
    return scene_path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("character_json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    with open(args.character_json) as fh:
        spec = json.load(fh)
    scene = generate(spec, args.out)
    print(f"wrote {scene}")
    print(f"wrote {os.path.join(args.out, 'poses.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
