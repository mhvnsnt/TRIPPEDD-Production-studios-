#!/usr/bin/env python3
"""Wave 27 Lane A — libopenmpt wire proof.

Renders a self-composed minimal ProTracker MOD (own composition, synthesized
sine/square samples) through the REAL system libopenmpt
(/usr/lib/x86_64-linux-gnu/libopenmpt.so.0) via ctypes, writes a WAV, and
verifies duration / RMS / peak. No fake artifacts: every number below is
measured from the actual render.

libopenmpt license: BSD-3-Clause (commercial-safe).
"""
import ctypes
import json
import math
import os
import struct
import wave

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_PATH = os.path.join(OUT_DIR, "lane-a-openmpt-test.mod")
WAV_PATH = os.path.join(OUT_DIR, "lane-a-openmpt-test.wav")
PROOF_PATH = os.path.join(OUT_DIR, "lane-a-openmpt-proof.json")

LIB_PATH = "/usr/lib/x86_64-linux-gnu/libopenmpt.so.0"
SAMPLE_RATE = 48000

# ProTracker PAL periods (C-1 .. B-3 subset we use)
PERIOD = {
    "G-1": 570, "A-1": 508, "B-1": 453,
    "C-2": 428, "D-2": 382, "E-2": 340, "F-2": 320, "G-2": 286,
    "A-2": 254, "B-2": 227,
    "C-3": 214, "D-3": 191, "E-3": 170, "F-3": 160, "G-3": 143,
    "A-3": 127, "B-3": 113,
}


def make_sample(nbytes, freq_ratio=1.0, square=False):
    """Synthesize an 8-bit signed PCM loop. Original content."""
    data = bytearray()
    for i in range(nbytes):
        ph = 2.0 * math.pi * freq_ratio * i / nbytes
        v = math.sin(ph)
        if square:
            v = 0.8 if v >= 0 else -0.8
            v += 0.2 * math.sin(2 * ph)  # slight edge softening
        data.append(max(0, min(255, int(128 + 100 * v))))
    return bytes(data)


def note_cell(sample_no, period):
    """Encode one 4-byte ProTracker pattern cell (no effect)."""
    b0 = ((sample_no >> 4) & 0xF) << 4 | ((period >> 8) & 0xF)
    b1 = period & 0xFF
    b2 = ((sample_no & 0xF) << 4)
    b3 = 0x00
    return bytes([b0, b1, b2, b3])


def build_mod():
    # Own composition: 8-bar chiptune-ish phrase, 64 rows, 4 channels.
    # ch0 (sine lead): C E G E | A G E C  ; ch1 (square bass): C G C G
    lead = [(0, "C-3"), (8, "E-3"), (16, "G-3"), (24, "E-3"),
            (32, "A-3"), (40, "G-3"), (48, "E-3"), (56, "C-3")]
    bass = [(0, "C-2"), (16, "G-1"), (32, "C-2"), (48, "G-1")]

    samples = [
        ("LEAD_SINE", make_sample(256), 64),          # sample 1
        ("BASS_SQUARE", make_sample(128, square=True), 48),  # sample 2
    ]

    mod = bytearray()
    mod += b"LANE-A-OPENMPT-TEST".ljust(20, b"\x00")[:20]
    for idx, (name, data, vol) in enumerate(samples, start=1):
        mod += name.encode("ascii").ljust(22, b"\x00")[:22]
        mod += struct.pack(">H", len(data) // 2)   # length in words
        mod += bytes([0])                          # finetune
        mod += bytes([vol])                        # volume
        mod += struct.pack(">H", 0)                # repeat start (words)
        mod += struct.pack(">H", len(data) // 2)   # repeat length (words) = full loop
    for _ in range(31 - len(samples)):             # unused sample slots
        mod += bytes(30)
    mod += bytes([1])      # song length: 1 position
    mod += bytes([0])      # restart position
    mod += bytes([0] * 128)  # pattern table (position 0 -> pattern 0)
    mod += b"M.K."

    pattern = bytearray(1024)
    empty = bytes(4)
    for ch in range(4):
        for row in range(64):
            pattern[(row * 4 + ch) * 4:(row * 4 + ch) * 4 + 4] = empty
    for row, n in lead:
        cell = note_cell(1, PERIOD[n])
        pattern[(row * 4 + 0) * 4:(row * 4 + 0) * 4 + 4] = cell
    for row, n in bass:
        cell = note_cell(2, PERIOD[n])
        pattern[(row * 4 + 1) * 4:(row * 4 + 1) * 4 + 4] = cell
    mod += bytes(pattern)
    for _, data, _ in samples:
        mod += data
    return bytes(mod)


def main():
    mod_data = build_mod()
    with open(MOD_PATH, "wb") as f:
        f.write(mod_data)
    print(f"Wrote MOD: {MOD_PATH} ({len(mod_data)} bytes)")

    lib = ctypes.CDLL(LIB_PATH)
    lib.openmpt_module_create_from_memory2.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t,
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char_p),
        ctypes.c_void_p,
    ]
    lib.openmpt_module_create_from_memory2.restype = ctypes.c_void_p
    lib.openmpt_module_get_num_channels.argtypes = [ctypes.c_void_p]
    lib.openmpt_module_get_num_channels.restype = ctypes.c_int32
    lib.openmpt_module_get_duration_seconds.argtypes = [ctypes.c_void_p]
    lib.openmpt_module_get_duration_seconds.restype = ctypes.c_double
    lib.openmpt_module_read_float_stereo.argtypes = [
        ctypes.c_void_p, ctypes.c_int32, ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float),
    ]
    lib.openmpt_module_read_float_stereo.restype = ctypes.c_size_t
    lib.openmpt_module_destroy.argtypes = [ctypes.c_void_p]

    buf = ctypes.create_string_buffer(mod_data, len(mod_data))
    err = ctypes.c_int(0)
    errmsg = ctypes.c_char_p()
    mod = lib.openmpt_module_create_from_memory2(
        buf, len(mod_data), None, None, None, None,
        ctypes.byref(err), ctypes.byref(errmsg), None)
    if not mod:
        raise RuntimeError(f"openmpt rejected the MOD (err={err.value}, "
                           f"msg={errmsg.value!r})")
    nch = lib.openmpt_module_get_num_channels(mod)
    duration = lib.openmpt_module_get_duration_seconds(mod)
    print(f"libopenmpt OK: channels={nch} duration={duration:.3f}s")

    total = int(duration * SAMPLE_RATE) + SAMPLE_RATE  # headroom
    left_t = (ctypes.c_float * total)()
    right_t = (ctypes.c_float * total)()
    got = lib.openmpt_module_read_float_stereo(
        mod, SAMPLE_RATE, total, left_t, right_t)
    lib.openmpt_module_destroy(mod)
    print(f"rendered frames: {got}")

    frames = [(left_t[i], right_t[i]) for i in range(got)]
    peak = max(max(abs(l), abs(r)) for l, r in frames)
    rms = math.sqrt(sum(l * l + r * r for l, r in frames) / (2 * got))

    pcm = bytearray()
    for l, r in frames:
        pcm += struct.pack("<h", max(-32768, min(32767, int(l * 32767))))
        pcm += struct.pack("<h", max(-32768, min(32767, int(r * 32767))))
    with wave.open(WAV_PATH, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(bytes(pcm))
    print(f"Wrote WAV: {WAV_PATH} ({os.path.getsize(WAV_PATH)} bytes)")

    proof = {
        "library": LIB_PATH,
        "library_license": "BSD-3-Clause (commercial-safe)",
        "mod_bytes": len(mod_data),
        "mod_channels": nch,
        "duration_seconds_measured": round(duration, 3),
        "frames_rendered": got,
        "sample_rate": SAMPLE_RATE,
        "peak_amplitude": round(peak, 4),
        "rms_amplitude": round(rms, 4),
        "wav_bytes": os.path.getsize(WAV_PATH),
        "checks": {
            "duration_within_expected_3_to_12s": 3.0 <= duration <= 12.0,
            "frames_match_duration": abs(got - duration * SAMPLE_RATE) < SAMPLE_RATE,
            "audio_non_silent_rms_gt_0.01": rms > 0.01,
            "no_clipping_peak_le_1.0": peak <= 1.0,
        },
    }
    with open(PROOF_PATH, "w") as f:
        json.dump(proof, f, indent=2)
    print(json.dumps(proof, indent=2))
    assert all(proof["checks"].values()), "SMOKE TEST FAILED"
    print("SMOKE TEST PASSED")


if __name__ == "__main__":
    main()
