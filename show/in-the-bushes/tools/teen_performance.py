#!/usr/bin/env python3
"""Procedural stick-figure teen performance layer for EP01.

The opening needs characters to perform, not merely translate as one SVG. This
module renders three distinct teens from reusable body parts and changes pose,
lean, arm swing, leg placement, and head direction over time. It intentionally
stays simple so the motion can be reused in later episodes.
"""
from __future__ import annotations

import math

W, H = 1920, 1080
TEENS = [
    {"x": 560, "y": 430, "head": 45, "body": 160, "leg": 92, "offset": 0.0},
    {"x": 760, "y": 455, "head": 43, "body": 165, "leg": 88, "offset": 1.7},
    {"x": 950, "y": 450, "head": 44, "body": 158, "leg": 96, "offset": 3.1},
]


def esc(v):
    return f"{v:.2f}"


def clamp(t):
    return max(0.0, min(1.0, t))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def pose_at(frame: int, shot_id: str):
    ranges = {
        "S01": (0, 83, ["hang", "talk", "hang"]),
        "S02": (108, 143, ["hang", "turn", "stare", "panic"]),
        "S03": (144, 215, ["freeze", "grab", "turn_exit", "run"]),
        "S04": (216, 299, ["run", "duck", "hide", "peek"]),
        "S05": (300, 371, ["crouch", "breathe", "look_pack", "look_bush"]),
        "S06": (372, 419, ["ask", "glance_bush"]),
        "S07": (420, 455, ["neutral", "point", "commit"]),
        "S08": (456, 539, ["run", "throw", "flee"]),
        "S09": (520, 610, ["flee", "flee_fast"]),
    }
    if shot_id not in ranges:
        return "hang", 0.0
    start, end, poses = ranges[shot_id]
    t = clamp((frame - start) / max(1, end - start))
    u = t * (len(poses) - 1)
    i = min(len(poses) - 2, int(u)) if len(poses) > 1 else 0
    local = u - i if len(poses) > 1 else 0.0
    return poses[i], ease(local)


def _limb(x, y, angle_deg, length):
    r = math.radians(angle_deg - 90)
    return x + math.cos(r) * length, y + math.sin(r) * length


def teen_svg(frame: int, shot_id: str) -> str:
    pose, _ = pose_at(frame, shot_id)
    groups = []
    for t in TEENS:
        phase = frame * 0.35 + t["offset"] * 35
        sway = math.sin(math.radians(phase)) * (2.5 if pose in {"hang", "breathe", "crouch"} else 1.2)
        x, y = t["x"], t["y"]
        head, body, leg = t["head"], t["body"], t["leg"]
        lean = 0.0
        arm_l, arm_r = -115, 88
        leg_l, leg_r = -25, 25
        head_dx = head_dy = 0
        crouch = 0
        mouth = ""

        if pose == "talk":
            arm_r, mouth = 72, "<path d='M-16 8 Q0 20 16 8' fill='none'/>"
        elif pose == "turn":
            lean, head_dx = -5, -8
        elif pose == "stare":
            lean, head_dx, arm_l, arm_r = -7, -12, -100, 105
        elif pose == "panic":
            lean, arm_l, arm_r, leg_l, leg_r = -10, -145, 125, -42, 42
            mouth = "<circle cx='0' cy='14' r='8' fill='#0b0d12' stroke='none'/>"
        elif pose == "freeze":
            lean, arm_l, arm_r = -4, -130, 115
        elif pose == "grab":
            lean, arm_l, arm_r = -10, -40, 35
        elif pose == "turn_exit":
            lean, arm_l, arm_r, leg_l, leg_r = -14, -55, 35, -38, 42
        elif pose == "run":
            stride = math.sin(phase) * 18
            lean, arm_l, arm_r = -16, -125 + stride, 110 + stride
            leg_l, leg_r = -38 - stride, 38 - stride
        elif pose == "duck":
            crouch, lean, arm_l, arm_r = 58, -8, -90, 105
        elif pose == "hide":
            crouch, lean, arm_l, arm_r, head_dy = 70, -4, -65, 75, 24
        elif pose == "peek":
            crouch, lean, head_dx, arm_l, arm_r = 62, -12, -20, -70, 80
        elif pose == "crouch":
            crouch, lean, arm_l, arm_r = 62, 2, -75, 70
        elif pose == "breathe":
            crouch = 58 + math.sin(phase) * 3
            lean, arm_l, arm_r = math.sin(phase * .7) * 2, -78, 74
        elif pose == "look_pack":
            crouch, head_dx, head_dy, arm_l, arm_r = 54, 8, 18, -55, 55
        elif pose == "look_bush":
            crouch, head_dx, arm_l, arm_r = 50, 28, -75, 90
        elif pose == "ask":
            crouch, arm_l, arm_r, head_dx = 50, -120, 45, -4
            mouth = "<path d='M-14 10 Q0 2 14 10' fill='none'/>"
        elif pose == "glance_bush":
            crouch, head_dx, arm_l, arm_r = 48, 26, -75, 88
        elif pose == "point":
            arm_r, arm_l, head_dx = 25, -90, 18
        elif pose == "commit":
            lean, arm_r, arm_l, head_dx = -8, 18, -115, 24
        elif pose == "throw":
            lean, arm_r, arm_l, leg_l, leg_r = -20, 12, -150, -45, 48
        elif pose == "flee":
            stride = math.sin(phase) * 25
            lean, arm_l, arm_r = -20, -145 + stride, 125 + stride
            leg_l, leg_r = -45 - stride, 45 - stride
        elif pose == "flee_fast":
            stride = math.sin(phase * 1.35) * 32
            lean, arm_l, arm_r = -24, -155 + stride, 135 + stride
            leg_l, leg_r = -52 - stride, 52 - stride

        lean += sway
        by = body + crouch
        hx, hy = head_dx, head_dy - crouch * 0.10
        body_top = (0, 48 + crouch * 0.25)
        body_bottom = (lean * 0.35, by)
        shoulder_y = 95 + crouch * 0.22
        hand_l = _limb(-lean * .25 - 4, shoulder_y, arm_l, 92)
        hand_r = _limb(-lean * .25 + 5, shoulder_y, arm_r, 92)
        foot_l = _limb(body_bottom[0], body_bottom[1], leg_l, leg + crouch * .25)
        foot_r = _limb(body_bottom[0], body_bottom[1], leg_r, leg + crouch * .25)

        groups.append(
            f"<g transform='translate({esc(x)} {esc(y)}) rotate({esc(lean)} 0 {esc(body/2)})'>"
            f"<circle cx='{esc(hx)}' cy='{esc(hy)}' r='{head}' fill='#d6d1c7'/>"
            f"<path d='M{esc(body_top[0])} {esc(body_top[1])} L{esc(body_bottom[0])} {esc(body_bottom[1])}' fill='none'/>"
            f"<path d='M0 {esc(shoulder_y)} L{esc(hand_l[0])} {esc(hand_l[1])}' fill='none'/>"
            f"<path d='M0 {esc(shoulder_y)} L{esc(hand_r[0])} {esc(hand_r[1])}' fill='none'/>"
            f"<path d='M{esc(body_bottom[0])} {esc(body_bottom[1])} L{esc(foot_l[0])} {esc(foot_l[1])}' fill='none'/>"
            f"<path d='M{esc(body_bottom[0])} {esc(body_bottom[1])} L{esc(foot_r[0])} {esc(foot_r[1])}' fill='none'/>"
            f"{mouth}</g>"
        )
    return "<g fill='#d6d1c7' stroke='#0b0d12' stroke-width='12' stroke-linecap='round' stroke-linejoin='round'>" + "".join(groups) + "</g>"


def performance_layer(frame: int, shot_id: str) -> str:
    return teen_svg(frame, shot_id)
