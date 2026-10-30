#!/usr/bin/env python3
"""Make the kit's test image: saturated colour blocks + mid grey + white.
Deterministic, no external assets. 256x256 PNG."""
import sys
from PIL import Image

def main(path):
    img = Image.new("RGB", (256, 256))
    px = img.load()
    blocks = [
        (170, 100, 80), (100, 160, 90), (90, 100, 170), (160, 90, 150),
        (170, 150, 90), (90, 150, 150), (128, 128, 128), (240, 240, 240),
    ]
    for by in range(2):
        for bx in range(4):
            c = blocks[by * 4 + bx]
            for y in range(by * 128, by * 128 + 128):
                for x in range(bx * 64, bx * 64 + 64):
                    px[x, y] = c
    img.save(path)
    print("wrote", path)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "test_input.png")
