#!/usr/bin/env python3
"""Pixel metrics for the kit test outputs (PIL only).

Assertions:
  LOOK2 mean saturation > input + 0.03   (deep saturation must saturate)
  LOOK1 mean saturation < input - 0.03   (pale wash must desaturate)
  LED purple: output mean B - mean R increases vs input (violet tint)
  CARD: output differs from input (pan applied) — mean abs diff > 1.0
Prints one line per check + RESULT PASS/FAIL; exit code follows.
"""
import os
import sys
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/n1-test-out"

def load(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        return None
    return Image.open(p).convert("RGB")

def mean_sat(img):
    hsv = img.convert("HSV")
    px = list(hsv.getdata())
    return sum(p[1] for p in px) / (len(px) * 255.0)

def mean_rgb(img):
    px = list(img.getdata())
    n = len(px)
    return tuple(sum(p[i] for p in px) / n for i in range(3))

def mean_abs_diff(a, b):
    if a.size != b.size:
        b = b.resize(a.size)
    pa, pb = list(a.getdata()), list(b.getdata())
    return sum(abs(pa[i][c] - pb[i][c]) for i in range(len(pa)) for c in range(3)) / (len(pa) * 3)

def main():
    inp = load("test_input.png")
    if inp is None:
        print("METRICS FAIL: test_input.png missing"); return 1
    sat_in = mean_sat(inp); rgb_in = mean_rgb(inp)
    print(f"input: mean_sat={sat_in:.4f} mean_rgb={tuple(round(v,1) for v in rgb_in)}")
    checks = []
    l2 = load("out_look2.png")
    if l2 is None:
        checks.append(("LOOK2 output exists", False))
    else:
        s = mean_sat(l2); print(f"look2: mean_sat={s:.4f} delta={s - sat_in:+.4f}")
        checks.append(("LOOK2 saturation up > +0.03", s > sat_in + 0.03))
    l1 = load("out_look1.png")
    if l1 is None:
        checks.append(("LOOK1 output exists", False))
    else:
        s = mean_sat(l1); print(f"look1: mean_sat={s:.4f} delta={s - sat_in:+.4f}")
        checks.append(("LOOK1 saturation down > -0.03", s < sat_in - 0.03))
    led = load("out_led_purple.png")
    if led is None:
        checks.append(("LED purple output exists", False))
    else:
        r = mean_rgb(led); d_in = rgb_in[2] - rgb_in[0]; d_out = r[2] - r[0]
        print(f"led_purple: mean_rgb={tuple(round(v,1) for v in r)} (B-R) in={d_in:.1f} out={d_out:.1f}")
        checks.append(("LED purple B-R shift up > +5", d_out > d_in + 5))
    party = load("out_led_party.png")
    checks.append(("LED party output exists", party is not None))
    card = load("out_card.png")
    if card is None:
        checks.append(("CARD output exists", False))
    else:
        d = mean_abs_diff(inp, card); print(f"card: mean_abs_diff vs input={d:.3f}")
        checks.append(("CARD moved (diff > 1.0)", d > 1.0))
    ok = True
    for name, passed in checks:
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
