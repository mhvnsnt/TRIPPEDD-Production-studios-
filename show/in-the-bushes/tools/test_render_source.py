#!/usr/bin/env python3
"""Source-level render smoke tests for the In the Bushes opening."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3]
RIG_PATH=ROOT/"show/in-the-bushes/tools/teen_performance_v2.py"
BUILDER_PATH=ROOT/"show/in-the-bushes/tools/build_origin_opening.py"
RENDER_PATH=ROOT/"show/in-the-bushes/animatic/ep01-origin-opening-v2.render-plan.json"
BUSCH_WAKE=ROOT/"show/in-the-bushes/assets/busch/busch-wake.svg"
BUSCH_LOOK=ROOT/"show/in-the-bushes/assets/busch/busch-look-away.svg"
BUSCH_REACTION=ROOT/"show/in-the-bushes/assets/busch/busch-reaction.svg"
def load_rig():
    spec=importlib.util.spec_from_file_location("teen_performance_v2_test",RIG_PATH)
    assert spec and spec.loader
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def test_active_render_graph():
    plan=json.loads(RENDER_PATH.read_text())
    builder=BUILDER_PATH.read_text()
    active=[a for s in plan["shots"] for a in s.get("assets",[])]
    assert plan["activeBuilder"].endswith("build_origin_opening_character.py")
    assert plan["characterSource"].endswith("teen_performance_v2.py")
    assert "teen-group-origin-states.svg" not in active
    assert "teen-character-design-v1.svg" in active
    assert "PERFORMANCE_LAYER = load_teen_performance()" in builder
def test_procedural_layer_is_valid_svg():
    rig=load_rig()
    samples={"S01":[0,42,83],"S03":[144,180,215],"S04":[216,260,299],"S07":[420,438,455],"S08":[456,500,539],"S09":[520,565,610]}
    for shot,frames in samples.items():
        for frame in frames:
            svg=rig.performance_layer(frame,shot); root=ET.fromstring(svg)
            assert root.tag.endswith("g"); assert "NaN" not in svg and "inf" not in svg.lower()
            assert "#4a5664" in svg and "#8a6f58" in svg and "#566c63" in svg
            assert "stroke-width='20'" in svg
def test_pose_interpolation_changes_geometry():
    rig=load_rig(); a=rig.performance_layer(20,"S01"); b=rig.performance_layer(62,"S01")
    assert a!=b
    assert "translate(560 430)" in a and "translate(760 455)" in a and "translate(950 450)" in a
def test_busch_source_preserves_organic_aspect_ratio():
    builder=BUILDER_PATH.read_text()
    assert "def busch_image(" in builder
    assert 'width=560, height=560, preserve="xMidYMid meet"' in builder
    assert "x=1280, y=460" in builder
def test_busch_concept_traits_are_present_in_wake_family():
    for path in (BUSCH_WAKE, BUSCH_LOOK, BUSCH_REACTION):
        svg=path.read_text()
        ET.fromstring(svg)
        assert "#36a94f" in svg
        assert "#ef3038" in svg
        assert "No beer branding" in svg
if __name__=="__main__":
    for test in (test_active_render_graph,test_procedural_layer_is_valid_svg,test_pose_interpolation_changes_geometry,test_busch_source_preserves_organic_aspect_ratio,test_busch_concept_traits_are_present_in_wake_family):
        test(); print(f"PASS {test.__name__}")
    print("PASS render-source smoke suite")
