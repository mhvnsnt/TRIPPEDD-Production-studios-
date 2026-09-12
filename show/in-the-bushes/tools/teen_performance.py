#!/usr/bin/env python3
"""Procedural stick-figure teen performance layer for EP01.

Three reusable teen performers share the same low-fi construction but differ
in silhouette, timing, posture, and reaction. The goal is readable personality
without turning the opening into a crowded character-design exercise.
"""
from __future__ import annotations

import math

W, H = 1920, 1080
TEENS = [
    {"x": 560, "y": 430, "head": 45, "body": 160, "leg": 92, "offset": 0.0,
     "head_shape": "spike", "stance": 1.00, "arm_bias": 1.0},
    {"x": 760, "y": 455, "head": 43, "body": 165, "leg": 88, "offset": 1.7,
     "head_shape": "cap", "stance": 0.92, "arm_bias": 0.82},
    {"x": 950, "y": 450, "head": 44, "body": 158, "leg": 96, "offset": 3.1,
     "head_shape": "round", "stance": 1.08, "arm_bias": 0.68},
]


def esc(v):
    return f"{v:.2f}"


def clamp(t):
    return max(0.0, min(1.0, t))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def _pose_values(name):
    # lean, arm_l, arm_r, leg_l, leg_r, head_dx, head_dy, crouch, mouth
    return {
        "hang": (0, -115, 88, -25, 25, 0, 0, 0, ""),
        "talk": (1, -112, 72, -23, 24, 2, 0, 0, "<path d='M-16 8 Q0 20 16 8' fill='none'/>") ,
        "turn": (-5, -115, 92, -25, 25, -8, 0, 0, ""),
        "stare": (-7, -100, 105, -22, 30, -12, 0, 0, ""),
        "panic": (-10, -145, 125, -42, 42, -4, 0, 0, "<circle cx='0' cy='14' r='8' fill='#0b0d12' stroke='none'/>") ,
        "freeze": (-4, -130, 115, -25, 25, 0, 0, 0, ""),
        "grab": (-10, -40, 35, -28, 32, 4, 0, 0, ""),
        "turn_exit": (-14, -55, 35, -38, 42, 10, 0, 0, ""),
        "run": (-16, -125, 110, -38, 38, 12, 0, 0, ""),
        "duck": (-8, -90, 105, -30, 30, 0, 4, 58, ""),
        "hide": (-4, -65, 75, -25, 25, -8, 24, 70, ""),
        "peek": (-12, -70, 80, -28, 28, -20, 0, 62, ""),
        "crouch": (2, -75, 70, -24, 24, 0, 0, 62, ""),
        "breathe": (0, -78, 74, -24, 24, 0, 0, 58, ""),
        "look_pack": (1, -55, 55, -24, 24, 8, 18, 54, ""),
        "look_bush": (0, -75, 90, -22, 28, 28, 0, 50, ""),
        "ask": (0, -120, 45, -22, 24, -4, 0, 50, "<path d='M-14 10 Q0 2 14 10' fill='none'/>") ,
        "glance_bush": (0, -75, 88, -22, 28, 26, 0, 48, ""),
        "neutral": (0, -105, 88, -25, 25, 0, 0, 0, ""),
        "point": (0, -90, 25, -25, 25, 18, 0, 0, ""),
        "commit": (-8, -115, 18, -38, 42, 24, 0, 0, ""),
        "throw": (-20, -150, 12, -45, 48, 18, 0, 0, ""),
        "flee": (-20, -145, 125, -45, 45, 18, 0, 0, ""),
        "flee_fast": (-24, -155, 135, -52, 52, 22, 0, 0, ""),
    }[name]


def _sequence(frame, start, end, poses):
    t = clamp((frame - start) / max(1, end - start))
    if len(poses) == 1:
        return poses[0], 1.0
    u = ease(t) * (len(poses) - 1)
    i = min(len(poses) - 2, int(u))
    return poses[i], u - i


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
    return _sequence(frame, start, end, poses)


def _limb(x, y, angle_deg, length):
    r = math.radians(angle_deg - 90)
    return x + math.cos(r) * length, y + math.sin(r) * length


def _head(shape, r):
    if shape == "spike":
        return f"<path d='M{-r} 0 Q{-r*.7} {-r*.95} 0 {-r*1.05} Q{r*.45} {-r*.95} {r} 0 Q{r*.7} {r} 0 {r} Q{-r*.7} {r} {-r} 0 Z'/>"
    if shape == "cap":
        return f"<path d='M{-r} 4 Q{-r} {-r*.9} 0 {-r} Q{r} {-r*.85} {r} 4 L{r*.65} {r} L{-r*.65} {r} Z'/><path d='M{-r*.95} {-r*.15} Q0 {-r*.55} {r*.95} {-r*.15}' fill='none'/>"
    return f"<circle cx='0' cy='0' r='{r}'/>"


def teen_svg(frame: int, shot_id: str) -> str:
    pose, blend = pose_at(frame, shot_id)
    # Small stagger keeps the group from reading as one synchronized puppet.
    groups = []
    for idx, t in enumerate(TEENS):
        phase = frame * (0.35 + idx * 0.035) + t["offset"] * 35
        sway = math.sin(math.radians(phase)) * (2.5 if pose in {"hang", "breathe", "crouch"} else 1.2)
        x, y = t["x"], t["y"]
        head, body, leg = t["head"], t["body"], t["leg"]
        lean, arm_l, arm_r, leg_l, leg_r, head_dx, head_dy, crouch, mouth = _pose_values(pose)

        # Personality modifiers: impulsive commits farther, cautious protects the
        # torso, deadpan moves less and arrives slightly late.
        if idx == 0:
            lean *= 1.12
            arm_r += 5
            head_dx += 3
        elif idx == 1:
            lean *= 0.78
            arm_l *= 0.90
            arm_r *= 0.90
            head_dx -= 3
            head_dy += 2
        else:
            lean *= 0.62
            arm_l *= 0.78
            arm_r *= 0.78
            head_dx -= 6

        if shot_id == "S08" and pose == "throw":
            if idx == 0:
                arm_r, lean = 5, -24
            elif idx == 1:
                arm_r, lean = 22, -17
            else:
                arm_r, lean = 34, -10

        # Add a tiny temporal offset to each performer so the same pose does not
        # land on the same frame for everyone.
        local_phase = phase + idx * 13
        if pose in {"run", "flee", "flee_fast"}:
            stride = math.sin(math.radians(local_phase * (1.0 if pose != "flee_fast" else 1.25))) * (18 + idx * 3)
            leg_l -= stride
            leg_r += stride
            arm_l -= stride * 0.65 * t["arm_bias"]
            arm_r += stride * 0.65 * t["arm_bias"]

        lean += sway
        by = body + crouch
        hx, hy = head_dx, head_dy - crouch * 0.10
        body_top = (0, 48 + crouch * 0.25)
        body_bottom = (lean * 0.35, by)
        shoulder_y = 95 + crouch * 0.22
        hand_l = _limb(-lean * .25 - 4, shoulder_y, arm_l, 92 * t["stance"])
        hand_r = _limb(-lean * .25 + 5, shoulder_y, arm_r, 92 * t["stance"])
        foot_l = _limb(body_bottom[0], body_bottom[1], leg_l, leg + crouch * .25)
        foot_r = _limb(body_bottom[0], body_bottom[1], leg_r, leg + crouch * .25)

        # Eyes are intentionally tiny and directionally simple: head direction
        # does most of the acting at this production scale.
        eye_dx = 5 if idx == 0 else (2 if idx == 1 else 0)
        eye_dir = 1 if head_dx >= 0 else -1
        eyes = (
            f"<circle cx='{esc(-10 + eye_dx*eye_dir)}' cy='-5' r='4' fill='#0b0d12' stroke='none'/>"
            f"<circle cx='{esc(10 + eye_dx*eye_dir)}' cy='-5' r='4' fill='#0b0d12' stroke='none'/>{mouth}"
        )

        groups.append(
            f"<g transform='translate({esc(x)} {esc(y)}) rotate({esc(lean)} 0 {esc(body/2)})'>"
            f"{_head(t['head_shape'], head)}"
            f"<g fill='#0b0d12' stroke='none'>{eyes}</g>"
            f"<path d='M{esc(body_top[0])} {esc(body_top[1])} L{esc(body_bottom[0])} {esc(body_bottom[1])}' fill='none'/>"
            f"<path d='M0 {esc(shoulder_y)} L{esc(hand_l[0])} {esc(hand_l[1])}' fill='none'/>"
            f"<path d='M0 {esc(shoulder_y)} L{esc(hand_r[0])} {esc(hand_r[1])}' fill='none'/>"
            f"<path d='M{esc(body_bottom[0])} {esc(body_bottom[1])} L{esc(foot_l[0])} {esc(foot_l[1])}' fill='none'/>"
            f"<path d='M{esc(body_bottom[0])} {esc(body_bottom[1])} L{esc(foot_r[0])} {esc(foot_r[1])}' fill='none'/>"
            f"</g>"
        )
    return "<g fill='#d6d1c7' stroke='#0b0d12' stroke-width='12' stroke-linecap='round' stroke-linejoin='round'>" + "".join(groups) + "</g>"


def performance_layer(frame: int, shot_id: str) -> str:
    return teen_svg(frame, shot_id)
