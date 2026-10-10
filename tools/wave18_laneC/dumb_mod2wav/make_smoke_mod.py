#!/usr/bin/env python3
"""Generate a tiny, valid ProTracker 4-channel MOD (M.K.) with a real melody.

Synthetic on purpose: we own every byte, so the DUMB render proof is
reproducible and license-clean (no third-party module needed).
"""
import struct, math, sys

TITLE = b"TRIPPEDD-SMOKE-MOD.."    # 20 bytes
assert len(TITLE) == 20

# One instrument: 64-sample sine-ish pluck, 8-bit signed
N_SMP = 64
sample = bytes(int(100 * math.sin(2 * math.pi * i / N_SMP) * (1 - i / (2 * N_SMP))) & 0xFF
               if int(100 * math.sin(2 * math.pi * i / N_SMP) * (1 - i / (2 * N_SMP))) >= 0
               else (256 + int(100 * math.sin(2 * math.pi * i / N_SMP) * (1 - i / (2 * N_SMP)))) & 0xFF
               for i in range(N_SMP))

# Amiga periods for one octave + a fifth (C-2 .. G-2), ProTracker table
PERIODS = {
    "C-2": 428, "D-2": 381, "E-2": 339, "F-2": 320,
    "G-2": 285, "A-2": 254, "B-2": 227, "C-3": 214,
}

# 4-bar melody, one note per 4 rows (16th feel at speed 6), 4 channels:
# ch0 = lead, ch1 = bass root, ch2 = fifth, ch3 = octave pops
LEAD = ["C-3", None, "E-3" if False else "G-2", None, "A-2", None, "G-2", None,
        "F-2", None, "A-2", None, "G-2", None, None, None]
BASS = ["C-2", None, None, None, "F-2", None, None, None,
        "C-2", None, None, None, "G-2", None, None, None]

def note_bytes(period, inst):
    if period is None:
        return b"\x00\x00\x00\x00"
    b0 = (inst & 0x10) | ((period >> 8) & 0x0F)
    b1 = period & 0xFF
    b2 = ((inst & 0x0F) << 4)
    return bytes([b0, b1, b2, 0x00])

patterns = []
for pat in range(2):
    rows = []
    for r in range(64):
        step = (r // 4) % 16
        rows.append(note_bytes(PERIODS.get(LEAD[step]), 1) +
                    note_bytes(PERIODS.get(BASS[step]), 1) +
                    note_bytes(PERIODS.get("G-2" if pat == 0 else "A-2") if r % 16 == 0 else None, 1) +
                    note_bytes(PERIODS.get("C-3") if r % 32 == 8 else None, 1))
    patterns.append(b"".join(rows))

out = bytearray()
out += TITLE
# 31 sample headers; sample 1 = our pluck, rest empty
for i in range(31):
    if i == 0:
        hdr = struct.pack(">22sHBBHH", b"PLUCK", N_SMP // 2, 0, 64, 0, 1)
    else:
        hdr = struct.pack(">22sHBBHH", b"", 0, 0, 0, 0, 1)
    out += hdr
out += bytes([2, 0])          # song length 2, restart 0
out += bytes([0, 1] + [0] * 126)  # pattern table
out += b"M.K."
for p in patterns:
    out += p
out += sample

path = sys.argv[1] if len(sys.argv) > 1 else "smoke.mod"
open(path, "wb").write(bytes(out))
print(f"wrote {path} ({len(out)} bytes, ProTracker M.K., 2 patterns, 4 channels)")
