#!/usr/bin/env python3
"""Source-level render smoke tests for the In the Bushes opening.

These tests do not require FFmpeg or a desktop animation application. They
exercise the same procedural teen layer used by the character builder and parse
representative SVG frames, catching malformed SVG and regressions back to the
obsolete stick-figure asset before an expensive render is attempted.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
RIG_PATH = ROOT / "show/in-the-bushes/tools/teen_performance.py"
BUILDER_PATH = ROOT / "show/in-the-bushes/tools/build_origin_opening.py"
RENDER_PATH = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.render-plan.json"


def load_rig():
    spec = importlib.util.spec_from_file_location("teen_performance_test", RIG_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load teen performance rig")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_active_render_graph():
    plan = json.loads(RENDER_PATH.read_text(encoding="utf-8"))
    builder_text = BUILDER_PATH.read_text(encoding="utf-8")
    active_assets = [asset for shot in plan["shots"] for asset in shot.get("assets", [])]
    assert plan["activeBuilder"].endswith("build_origin_opening_character.py")
    assert plan["characterSource"].endswith("teen_performance.py")
    # The archive-only sheet may be mentioned in documentation/edit rules; it
    # must not appear in an active shot asset list or builder implementation.
    assert "teen-group-origin-states.svg" not in active_assets
    assert "teen-character-design-v1.svg" in active_assets
    assert "teen-group-origin-states.svg" not in builder_text
    assert "teen-character-design-v1.svg" in builder_text
    assert "PERFORMANCE_LAYER = load_teen_performance()" in builder_text
    assert "return PERFORMANCE_LAYER(frame, shot_id)" in builder_text


def test_procedural_layer_is_valid_svg():
    rig = load_rig()
    samples = {
        "S01": (0, 42, 83),
        "S02": (108, 125, 143),
        "S03": (144, 180, 215),
        "S04": (216, 260, 299),
        "S05": (300, 335, 371),
        "S06": (372, 395, 419),
        "S07": (420, 438, 455),
        "S08": (456, 500, 539),
        "S09": (520, 565, 610),
    }
    for shot, frames in samples.items():
        for frame in frames:
            svg = rig.performance_layer(frame, shot)
            root = ET.fromstring(svg)
            assert root.tag.endswith("g"), (shot, frame)
            assert "NaN" not in svg and "inf" not in svg.lower(), (shot, frame)
            assert "stroke-width='20'" in svg, (shot, frame)
            assert "#4a5664" in svg and "#8a6f58" in svg and "#566c63" in svg, (shot, frame)


def test_pose_interpolation_changes_geometry():
    rig = load_rig()
    a = rig.performance_layer(20, "S01")
    b = rig.performance_layer(62, "S01")
    assert a != b
    assert "translate(560.00 430.00)" in a
    assert "translate(760.00 455.00)" in a
    assert "translate(950.00 450.00)" in a


def test_busch_source_preserves_organic_aspect_ratio():
    builder_text = BUILDER_PATH.read_text(encoding="utf-8")
    assert "def busch_image(" in builder_text
    assert 'width=560, height=560, preserve="xMidYMid meet"' in builder_text
    assert 'x=1280, y=460' in builder_text
    assert "keep the character's silhouette intact" in builder_text


def test_busch_wake_transform_is_center_anchored():
    builder_text = BUILDER_PATH.read_text(encoding="utf-8")
    assert 'cx, cy = 1560, 740' in builder_text
    assert 'translate({cx} {cy}) translate(0 {y:.2f}) scale({s:.3f})' in builder_text
    assert 'translate(-{cx} -{cy})' in builder_text


if __name__ == "__main__":
    tests = [
        test_active_render_graph,
        test_procedural_layer_is_valid_svg,
        test_pose_interpolation_changes_geometry,
        test_busch_source_preserves_organic_aspect_ratio,
        test_busch_wake_transform_is_center_anchored,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print("PASS render-source smoke suite")
