#!/usr/bin/env python3
"""fountain_to_animatic_wg.py -- .fountain screenplay -> timed animatic MP4 (title-card cut).

Wizard Gang adaptation of Cape Jones `production/pipeline/fountain_to_animatic.py`
(CJ main @ 2026-11-13, 10,158 B, read in full). The CJ parser, card renderer and
ffmpeg concat are unchanged; the WG deltas are marked WG-ADAPT below.

WG-ADAPT 1 -- EP02 HAS NO FOUNTAIN SCRIPT. EP02's only dialogue record is the
18 `text` fields in the pocket-studio timeline JSONs (see EP02-OUTLINE.md §4).
So this script gains `--from-ep02-json`: it builds one title card per EP02 scene
(s10-s29 + intro + tail) from `ep02_dialogue_18.json` + the scene table in this
file, using the REAL scene durations from the outline -- not word-count estimates.
Run that first; the Fountain path is for when a real WG Fountain script exists.

WG-ADAPT 2 -- defaults follow WG-TIMING-STANDARD.md (PR #306): 24 fps on twos.
A 30 fps delivery is a conversion of the 24 fps master, not a re-animation.

WG-ADAPT 3 -- card footer says `wizard-gang . fountain_to_animatic_wg` and the
title defaults to `WIZARD GANG -- EP02`. No Cape Jones names, art or dialogue
are carried over (FREE-GAME RULE: craft transfers, the other show's content
does not). The CJ docstring's paired scripts (`../script-tools/fountain_to_cues.py`,
`build_animatic.py`) do NOT exist in cape-jones -- checked 2026-11-13, code
search 0 hits -- so they are not referenced as inputs here.

Usage:
  python3 fountain_to_animatic_wg.py script.fountain -o animatic.mp4
  python3 fountain_to_animatic_wg.py --from-ep02-json ep02_dialogue_18.json -o ep02_animatic.mp4
  python3 fountain_to_animatic_wg.py --from-ep02-json ep02_dialogue_18.json -o ep02_animatic.mp4 --keep-cards cards/
  python3 fountain_to_animatic_wg.py script.fountain -o animatic.mp4 --audio voices.mp3
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1280, 720
BG = (16, 16, 22)
FG = (235, 235, 240)
DIM = (150, 150, 160)
ACCENT = (255, 176, 32)

# WG-ADAPT 1: EP02 scene table, from EP02-OUTLINE.md §2 (PR #303).
# Scene id, start (s), duration (s). Intro is locked; gap + tail have no bed.
WG_EP02_SCENES = [
    ("intro", 0.0, 50.0),
    ("s10", 50.0, 12.0),
    ("s11", 62.0, 16.0),
    ("s12", 78.0, 20.0),
    ("s13", 98.0, 32.0),
    ("s14", 130.0, 10.0),
    ("s15", 140.0, 10.0),
    ("s16", 150.0, 9.0),
    ("s17", 159.0, 9.0),
    ("s18", 168.0, 10.0),
    ("s19", 178.0, 9.0),
    ("s20", 187.0, 8.0),
    ("s21", 195.0, 8.0),
    ("s22", 203.0, 9.0),
    ("s23", 212.0, 9.0),
    ("s24", 221.0, 10.0),
    ("s25", 231.0, 6.0),
    ("s26", 237.0, 8.0),
    ("s27", 250.0, 25.0),
    ("s28", 275.0, 20.0),
    ("s29", 295.0, 5.0),
    ("tail", 300.0, 44.81),
]

WG_EP02_SCENE_NAMES = {
    "intro": "Locked intro (0:00-0:50, do not touch)",
    "s10": "s10 The Summons",
    "s11": "s11 The Meeting",
    "s12": "s12 Order of Business",
    "s13": "s13 The Derail Begins",
    "s14": "s14 Dice Game",
    "s15": "s15 Arcade",
    "s16": "s16 Basketball",
    "s17": "s17 Bodega",
    "s18": "s18 Night Market",
    "s19": "s19 Subway",
    "s20": "s20 Bridge",
    "s21": "s21 Parking Garage",
    "s22": "s22 Skate Park",
    "s23": "s23 Studio",
    "s24": "s24 Carnival",
    "s25": "s25 Grill Incident",
    "s26": "s26 The Pier",
    "s27": "s27 The Adjuction",
    "s28": "s28 The Photo Button",
    "s29": "s29 Ident",
    "tail": "Tail (5:00-5:44.81, no scene bed)",
}


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def is_scene_heading(line):
    s = line.strip()
    if s.startswith(".") and not s.startswith(".."):
        return True
    return bool(re.match(r"^(INT|EXT|EST|INT\.?/EXT\.?|INT\.?\s*/\s*EXT\.?)[\.\s]", s))


def is_transition(line):
    s = line.strip()
    if s.startswith(">"):
        return True
    return s.endswith("TO:") and s == s.upper() and len(s) < 40


def is_character(line):
    s = line.strip()
    if not s or len(s) > 60:
        return False
    if s.startswith("@"):
        return True
    if not s[0].isupper():
        return False
    core = re.sub(r"\s*\(.*?\)\s*", "", s)
    if not core:
        return False
    letters = [c for c in core if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper())
    return upper / len(letters) > 0.7 and not is_scene_heading(s) and not is_transition(s)


def is_parenthetical(line):
    s = line.strip()
    return s.startswith("(") and s.endswith(")")


def parse_fountain(path):
    """Return (title_meta dict, [scene dicts]). Scene: heading, blocks=[(kind,text)]."""
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    lines = raw.split("\n")

    # Title page: Key: value lines at the very top before first blank-line+content
    meta = {}
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)$", lines[i])
        if m and i < 40:
            meta[m.group(1).strip()] = m.group(2).strip()
            i += 1
            continue
        if lines[i].strip() == "" and i < 40:
            i += 1
            continue
        break
    # Only keep title page if we actually saw keys before content
    body = lines[i:]

    scenes = []
    cur = {"heading": "UNTITLED", "blocks": []}
    in_dialogue = False

    def push_scene():
        if cur["blocks"] or cur["heading"] != "UNTITLED":
            scenes.append(cur)

    for line in body:
        s = line.strip()
        if not s:
            in_dialogue = False
            continue
        if s.startswith("#"):
            continue  # section/synopsis marker
        if s.startswith("=") and s.endswith("=") and len(s) > 2:
            continue  # synopsis
        if is_scene_heading(s):
            push_scene()
            cur = {"heading": s.lstrip(".").strip(), "blocks": []}
            in_dialogue = False
        elif is_transition(s):
            cur["blocks"].append(("transition", s.lstrip(">").strip()))
            in_dialogue = False
        elif is_character(s):
            name = s.lstrip("@").strip()
            cur["blocks"].append(("character", name))
            in_dialogue = True
        elif in_dialogue and is_parenthetical(s):
            cur["blocks"].append(("parenthetical", s))
        elif in_dialogue:
            cur["blocks"].append(("dialogue", s))
        else:
            if s.startswith(">") and s.endswith("<"):
                cur["blocks"].append(("centered", s[1:-1].strip()))
            else:
                cur["blocks"].append(("action", s))
                in_dialogue = False
    push_scene()
    # drop the leading empty scene if file started with a heading-less preamble
    if scenes and scenes[0]["heading"] == "UNTITLED" and not scenes[0]["blocks"]:
        scenes.pop(0)
    return meta, scenes


def build_ep02_scenes(dialogue_path):
    """WG-ADAPT 1: build scenes from the EP02 dialogue JSON (real WG record).

    Returns (meta, scenes) in the same shape as parse_fountain, but durations
    come from the real scene table above, and blocks carry the real lines with
    their real timeline times. Scenes with no dialogue get an action block
    noting that (12 of 20 scenes have zero dialogue -- outline §1).
    """
    with open(dialogue_path, encoding="utf-8") as f:
        data = json.load(f)
    lines = data["lines"] if isinstance(data, dict) else data
    by_scene = {}
    for ln in lines:
        by_scene.setdefault(ln.get("scene", "?"), []).append(ln)
    meta = {"Title": "WIZARD GANG -- EP02",
            "Source": "ep02_dialogue_18.json (EP02-OUTLINE.md §4, pocket-studio timeline JSONs)"}
    scenes = []
    for sid, start, dur in WG_EP02_SCENES:
        blocks = [("action", f"{WG_EP02_SCENE_NAMES[sid]} -- {start:.0f}s, {dur:.0f}s")]
        for ln in by_scene.get(sid, []):
            blocks.append(("character", ln["character"].upper()))
            blocks.append(("dialogue", f"{ln['text']}  [{ln['at']:.1f}s]"))
        if sid not in by_scene:
            blocks.append(("action", "(no dialogue in this scene)"))
        scenes.append({"heading": WG_EP02_SCENE_NAMES[sid],
                       "blocks": blocks, "duration": dur})
    return meta, scenes


def scene_duration(scene, wpm):
    words = 0
    for kind, text in scene["blocks"]:
        n = len(text.split())
        if kind == "dialogue":
            words += n
        elif kind == "action":
            words += n * 0.35  # action reads faster / gets less screen time
    return max(2.0, words / (wpm / 60.0) + 1.0)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def render_card(scene, idx, n, duration, meta):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    fb, fr, fs = font(FONT_BOLD, 54), font(FONT_REG, 30), font(FONT_REG, 24)

    # top bar
    d.rectangle([0, 0, W, 130], fill=(24, 24, 32))
    d.rectangle([0, 130, W, 134], fill=ACCENT)
    d.text((48, 26), f"SCENE {idx + 1}/{n}", font=font(FONT_BOLD, 28), fill=ACCENT)
    # SUCCESSOR FIX 2026-11-14: heading at 54pt overflowed the card and ran
    # under the duration text (seen own-eyes on block-a frame: "12s" clipped,
    # "6.8s" overlapping the heading). Truncate with ellipsis to fit W-96-140.
    heading = scene["heading"]
    max_hw = W - 96 - 150
    while len(heading) > 1 and d.textlength(heading, font=fb) > max_hw:
        heading = heading[:-2] + "…"
    d.text((48, 62), heading, font=fb, fill=FG)
    d.text((W - 48 - d.textlength(f"{duration:.1f}s", font=fr), 62),
           f"{duration:.1f}s", font=fr, fill=DIM)

    y = 180
    shown = 0
    for kind, text in scene["blocks"]:
        if shown >= 8 or y > H - 90:
            break
        if kind == "character":
            y += 10
            d.text((80, y), text.upper(), font=font(FONT_BOLD, 30), fill=ACCENT)
            y += 44
        elif kind == "dialogue":
            for ln in wrap(d, text, fr, W - 220)[:2]:
                d.text((110, y), ln, font=fr, fill=FG)
                y += 38
            shown += 1
        elif kind == "action":
            for ln in wrap(d, text, fr, W - 160)[:3]:
                d.text((80, y), ln, font=fr, fill=(200, 200, 208))
                y += 38
            shown += 1
        elif kind == "parenthetical":
            d.text((110, y), text, font=fs, fill=DIM)
            y += 32
        elif kind == "transition":
            d.text((W - 80 - d.textlength(text, font=fs), y), text, font=fs, fill=DIM)
            y += 36
    # footer
    title = meta.get("Title", "")
    if title:
        d.text((48, H - 56), title[:80], font=fs, fill=DIM)
    d.text((W - 48 - d.textlength("fountain_to_animatic_wg", font=fs), H - 56),
           "fountain_to_animatic_wg", font=fs, fill=(90, 90, 100))
    return img


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{r.stderr[-2000:]}", file=sys.stderr)
        sys.exit(1)
    return r


def main():
    ap = argparse.ArgumentParser(description=".fountain (or EP02 JSON) -> timed title-card animatic MP4")
    ap.add_argument("script", nargs="?", help=".fountain file (omit with --from-ep02-json)")
    ap.add_argument("--from-ep02-json", help="EP02 dialogue JSON (ep02_dialogue_18.json): build cards from the real EP02 record")
    ap.add_argument("-o", "--out", required=True, help="output mp4")
    ap.add_argument("--audio", help="voice/music track laid under the animatic")
    ap.add_argument("--wpm", type=float, default=150, help="dialogue words per minute (Fountain path only)")
    ap.add_argument("--fps", type=float, default=24, help="WG timing standard: 24 fps on twos")
    ap.add_argument("--size", default="1280x720")
    ap.add_argument("--keep-cards", help="directory to keep per-scene card PNGs")
    args = ap.parse_args()

    global W, H
    W, H = map(int, args.size.split("x"))

    if args.from_ep02_json:
        meta, scenes = build_ep02_scenes(args.from_ep02_json)
        durations = [s["duration"] for s in scenes]
        print(f"EP02 mode: {len(scenes)} scenes from {args.from_ep02_json} (real scene durations)")
    else:
        if not args.script:
            ap.error("give a .fountain script or --from-ep02-json")
        meta, scenes = parse_fountain(args.script)
        if not scenes:
            print("No scenes found in script.", file=sys.stderr)
            sys.exit(1)
        durations = [scene_duration(s, args.wpm) for s in scenes]
    if not args.from_ep02_json:
        meta.setdefault("Title", "WIZARD GANG -- EP02")

    tmp = tempfile.mkdtemp(prefix="fountain_animatic_wg_")
    cards_dir = args.keep_cards or tmp
    os.makedirs(cards_dir, exist_ok=True)

    total = sum(durations)
    print(f"{len(scenes)} scenes, total {total:.1f}s @ {args.fps} fps")

    segs = []
    for i, (scene, dur) in enumerate(zip(scenes, durations)):
        card = render_card(scene, i, len(scenes), dur, meta)
        path = os.path.join(cards_dir, f"card_{i:03d}.png")
        card.save(path)
        seg = os.path.join(tmp, f"seg_{i:03d}.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(args.fps),
             "-i", path, "-t", f"{dur:.2f}", "-vf", f"scale={W}:{H}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(args.fps), seg])
        segs.append(seg)

    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    video = os.path.join(tmp, "video.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", video])

    if args.audio:
        # pad/trim audio to animatic length
        run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", args.audio,
             "-filter_complex",
             f"[1:a]apad=whole_dur={total:.2f},atrim=0:{total:.2f}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "160k", "-shortest", args.out])
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", video, "-c", "copy", args.out])

    print(f"Wrote {args.out} ({total:.1f}s)")
    if not args.keep_cards:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
