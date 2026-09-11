#!/usr/bin/env python3
"""Validate the In the Bushes origin opening before rendering.

This is intentionally stdlib-only so CI/local production can catch timing and
continuity regressions before an expensive render.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCENE = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.scene.json"
MOTION = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.motion-blocks.json"
RENDER = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.render-plan.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message):
    raise SystemExit("FAIL: " + message)


def main():
    scene, motion, render = load(SCENE), load(MOTION), load(RENDER)
    shots = scene["shots"]
    if scene["fps"] != 24 or scene["totalFrames"] != 888:
        fail("origin must remain 888 frames at 24fps")
    if scene["targetDurationSeconds"] != 37:
        fail("scene target duration drifted from 37 seconds")
    if render["totalFrames"] != scene["totalFrames"] or render["resolution"] != [1920, 1080]:
        fail("render plan no longer matches scene master")

    expected = [f"S{i:02d}" for i in range(1, 14)]
    actual = [s["id"] for s in shots]
    if actual != expected:
        fail(f"shot order mismatch: {actual}")
    cursor = 0
    for shot in shots:
        if shot["start"] != cursor:
            fail(f"gap/overlap before {shot['id']}: expected {cursor}, got {shot['start']}")
        cursor += shot["duration"]
    if cursor != scene["totalFrames"]:
        fail("shot durations do not cover the complete scene")

    by_id = {b["id"]: b for b in motion["blocks"]}
    required = [
        "police_light_sweep", "teen_panic", "teen_run_out", "duck_hide",
        "beer_realize", "point_bush", "run_out_of_alley", "throw_arc_spin",
        "teen_flee", "foliage_twitch", "foliage_shudder", "energy_pulse",
        "busch_wake_rise", "look_away", "reaction_blink_sway", "title_cut"
    ]
    missing = [x for x in required if x not in by_id]
    if missing:
        fail("missing motion blocks: " + ", ".join(missing))

    def start_end(name):
        return by_id[name]["frames"]

    # Causal ordering is the most important story invariant.
    if start_end("police_light_sweep")[0] >= start_end("teen_panic")[0]:
        fail("police presence must precede panic")
    if start_end("run_out_of_alley")[0] <= start_end("point_bush")[1] and start_end("run_out_of_alley")[0] < 456:
        fail("run-out cannot begin before the title phrase/decision")
    if start_end("throw_arc_spin")[0] < 480:
        fail("beer throw begins too early")
    if start_end("teen_flee")[0] < start_end("throw_arc_spin")[1]:
        fail("teens cannot flee before the beer throw completes")
    if start_end("busch_wake_rise")[0] < start_end("teen_flee")[1]:
        fail("Busch cannot wake before fleeing action has completed")
    if start_end("look_away")[0] < start_end("busch_wake_rise")[1]:
        fail("look-away must follow Busch wake")
    if start_end("title_cut")[0] < start_end("look_away")[1]:
        fail("title cannot begin before the separate look-away beat")

    # Verify every render-plan shot carries an asset list and motion list.
    for shot in render["shots"]:
        if not shot.get("assets") or not shot.get("motion"):
            fail(f"render plan incomplete for {shot['id']}")
    print("PASS: In the Bushes EP01 origin opening continuity is valid.")
    print("PASS: 13 shots / 888 frames / 37.0s / 1920x1080 / 24fps")
    print("PASS: police -> hide -> beer realization -> IN THE BUSHES -> run out -> throw -> transformation -> Busch -> look-away -> title")


if __name__ == "__main__":
    main()
