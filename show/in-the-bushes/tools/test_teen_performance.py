#!/usr/bin/env python3
"""Stdlib-only regression checks for the active EP01 teen performance rig."""
from __future__ import annotations
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
RIG_PATH=HERE/"teen_performance_v2.py"

def load_rig():
    spec=importlib.util.spec_from_file_location("teen_performance_v2_test",RIG_PATH)
    assert spec and spec.loader
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_mid_transition_is_interpolated():
    mod=load_rig()
    start=mod.pose(144,"S03",0); mid=mod.pose(168,"S03",0); end=mod.pose(215,"S03",0)
    assert mid!=start and mid!=end
    assert any(isinstance(a,(int,float)) and isinstance(b,(int,float)) and a!=b for a,b in zip(start,mid))

def test_performers_do_not_react_on_same_frame():
    mod=load_rig()
    poses=[mod.pose(170,"S03",i) for i in range(3)]
    assert len({tuple(round(v,4) for v in p) for p in poses})==3

def test_throw_timing_is_staggered():
    mod=load_rig()
    poses=[mod.pose(515,"S08",i) for i in range(3)]
    assert len({tuple(round(v,4) for v in p) for p in poses})==3

def test_cast_has_real_character_design_language():
    mod=load_rig()
    assert [p["style"] for p in mod.TEENS]==["hoodie","jacket","tee"]
    svg=mod.performance_layer(40,"S01")
    # Guard against regression back to head-and-lines-only stick figures.
    assert "hoodie" not in svg
    assert "#4a5664" in svg and "#8a6f58" in svg and "#566c63" in svg
    assert "<path" in svg and "stroke-width='20'" in svg
    # Distinct head treatments are encoded by the three style-specific head paths.
    assert svg.count("fill='#272d35'") == 1
    assert svg.count("fill='#303944'") == 1
    assert svg.count("fill='#1f242a'") == 1

if __name__=="__main__":
    test_mid_transition_is_interpolated()
    test_performers_do_not_react_on_same_frame()
    test_throw_timing_is_staggered()
    test_cast_has_real_character_design_language()
    print("PASS: active teen performance regression checks")
