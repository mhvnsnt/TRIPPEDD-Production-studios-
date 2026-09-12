#!/usr/bin/env python3
"""Small stdlib-only regression checks for the EP01 teen performance rig."""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("teen_performance", HERE / "teen_performance.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_mid_transition_is_interpolated():
    start = MOD.pose_at(144, "S03", 0)
    mid = MOD.pose_at(168, "S03", 0)
    end = MOD.pose_at(215, "S03", 0)
    assert mid != start
    assert mid != end
    assert any(isinstance(a, (int, float)) and isinstance(b, (int, float)) and a != b
               for a, b in zip(start, mid))


def test_performers_do_not_react_on_same_frame():
    poses = [MOD.pose_at(170, "S03", i) for i in range(3)]
    assert len({tuple(round(v, 4) if isinstance(v, (int, float)) else v for v in p) for p in poses}) == 3


def test_throw_timing_is_staggered():
    # At the same global frame, performers can occupy different points in the
    # run -> throw -> flee arc because their delay/tempo values differ.
    poses = [MOD.pose_at(515, "S08", i) for i in range(3)]
    assert len({tuple(round(v, 4) if isinstance(v, (int, float)) else v for v in p) for p in poses}) == 3


if __name__ == "__main__":
    test_mid_transition_is_interpolated()
    test_performers_do_not_react_on_same_frame()
    test_throw_timing_is_staggered()
    print("PASS: teen performance regression checks")
