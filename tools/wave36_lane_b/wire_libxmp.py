#!/usr/bin/env python3
"""Wave 36 Lane B — wire libxmp (tracker-format player lib) with a REAL proof.

libxmp: Extended Module Player library (90+ tracker formats), MIT-licensed,
catalog line 18307 (commercial-safe). Previously only license-verified
(Wave 17 Lane A); this is the first functional wire: it loads a REAL .mod
(Gaffeltruck.mod from libxmp's own upstream test data on GitHub), renders PCM
through the real libxmp 4.6.0 shared library via ctypes, writes a WAV, and
verifies the WAV header + measured audio stats. No fake artifacts: every
number in the proof JSON is measured from the actual render.

Self-contained: fetches libxmp4 .deb from the Ubuntu archive and extracts it
to /tmp (no root needed); fetches the MOD from upstream GitHub raw.

Usage: python3 tools/wave36_lane_b/wire_libxmp.py
Env: W36B_LIBXMP_DIR (extracted deb root), W36B_WORKDIR (default: script dir)
"""
import ctypes
import json
import math
import os
import struct
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WORKDIR = os.environ.get("W36B_WORKDIR", os.path.join(HERE, "proofs_libxmp"))
LIBXMP_DIR = os.environ.get("W36B_LIBXMP_DIR", "/tmp/w36b_libxmp")
MOD_URL = "https://raw.githubusercontent.com/cmatsuoka/libxmp/master/test-dev/data/Gaffeltruck.mod"
DEB_URL = "http://azure.archive.ubuntu.com/ubuntu/pool/universe/libx/libxmp/libxmp4_4.6.0-2_amd64.deb"
SAMPLE_RATE = 44100
MAX_SECONDS = 30  # render cap to keep the proof WAV small; documented, not hidden

os.makedirs(WORKDIR, exist_ok=True)


def log(msg):
    print(f"[wire_libxmp] {msg}", flush=True)


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        log(f"cached {dest}")
        return dest
    log(f"fetch {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave36/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def ensure_libxmp():
    so = os.path.join(LIBXMP_DIR, "usr/lib/x86_64-linux-gnu/libxmp.so.4")
    if os.path.exists(so):
        return so
    deb = os.path.join(WORKDIR, "libxmp4_4.6.0-2_amd64.deb")
    fetch(DEB_URL, deb)
    os.makedirs(LIBXMP_DIR, exist_ok=True)
    subprocess.run(["dpkg-deb", "-x", deb, LIBXMP_DIR], check=True)
    assert os.path.exists(so), "libxmp.so.4 missing after deb extract"
    return so


class XmpFrameInfo(ctypes.Structure):
    _fields_ = [
        ("pos", ctypes.c_int), ("pattern", ctypes.c_int), ("row", ctypes.c_int),
        ("num_rows", ctypes.c_int), ("frame", ctypes.c_int), ("speed", ctypes.c_int),
        ("bpm", ctypes.c_int), ("time", ctypes.c_int), ("total_time", ctypes.c_int),
        ("frame_time", ctypes.c_int), ("buffer", ctypes.c_void_p), ("buffer_size", ctypes.c_int),
        ("total_size", ctypes.c_int), ("volume", ctypes.c_int), ("loop_count", ctypes.c_int),
        ("virt_channels", ctypes.c_int), ("virt_used", ctypes.c_int),
        ("sequence", ctypes.c_int),
        # libxmp writes channel_info[XMP_MAX_CHANNELS=64] at the end of the
        # struct — omitting it corrupts the heap and segfaults.
        ("channel_info", ctypes.c_int * 64),
    ]


def main():
    so_path = ensure_libxmp()
    log(f"libxmp: {so_path}")
    lib = ctypes.CDLL(so_path)

    lib.xmp_create_context.restype = ctypes.c_void_p
    lib.xmp_load_module_from_memory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_long]
    lib.xmp_load_module_from_memory.restype = ctypes.c_int
    lib.xmp_start_player.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    lib.xmp_start_player.restype = ctypes.c_int
    lib.xmp_play_buffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    lib.xmp_play_buffer.restype = ctypes.c_int
    lib.xmp_get_frame_info.argtypes = [ctypes.c_void_p, ctypes.POINTER(XmpFrameInfo)]
    lib.xmp_end_player.argtypes = [ctypes.c_void_p]
    lib.xmp_release_module.argtypes = [ctypes.c_void_p]
    lib.xmp_free_context.argtypes = [ctypes.c_void_p]

    mod_path = os.path.join(WORKDIR, "Gaffeltruck.mod")
    fetch(MOD_URL, mod_path)
    with open(mod_path, "rb") as f:
        mod_data = f.read()
    magic = mod_data[1080:1084]
    log(f"input {mod_path}: {len(mod_data)} bytes, offset-1080 magic={magic!r}")
    assert len(mod_data) > 1084, "downloaded MOD too small — fetch failed"

    ctx = lib.xmp_create_context()
    assert ctx, "xmp_create_context failed"
    buf = ctypes.create_string_buffer(mod_data)
    rc = lib.xmp_load_module_from_memory(ctx, buf, len(mod_data))
    assert rc == 0, f"xmp_load_module_from_memory -> {rc}"
    log("module loaded OK")

    rc = lib.xmp_start_player(ctx, SAMPLE_RATE, 0)  # 0 = 16-bit signed stereo
    assert rc == 0, f"xmp_start_player -> {rc}"

    pcm = bytearray()
    chunk = ctypes.create_string_buffer(8192)
    frames_rendered = 0
    while len(pcm) < SAMPLE_RATE * MAX_SECONDS * 4:
        rc = lib.xmp_play_buffer(ctx, chunk, 8192, 0)
        if rc != 0:  # -XMP_END or error: stop
            break
        pcm += chunk.raw
        frames_rendered += 1
    ended = rc
    info = XmpFrameInfo()
    lib.xmp_get_frame_info(ctx, ctypes.byref(info))
    lib.xmp_end_player(ctx)
    lib.xmp_release_module(ctx)
    lib.xmp_free_context(ctx)

    n_samples = len(pcm) // 4
    duration_s = n_samples / SAMPLE_RATE
    log(f"rendered {n_samples} stereo frames = {duration_s:.2f}s, play_buffer rc={ended}")

    # WAV write (16-bit stereo PCM)
    wav_path = os.path.join(WORKDIR, "gaffeltruck_libxmp.wav")
    data_len = len(pcm)
    with open(wav_path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_len))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 2, SAMPLE_RATE, SAMPLE_RATE * 4, 4, 16))
        f.write(b"data")
        f.write(struct.pack("<I", data_len))
        f.write(pcm)

    # --- WAV header verification (read back the bytes we wrote) ---
    with open(wav_path, "rb") as f:
        hdr = f.read(44)
    riff, riff_size, wave, fmt_tag, fmt_size = struct.unpack("<4sI4s4sI", hdr[:20])
    audio_fmt, channels, rate, _, _, bits = struct.unpack("<HHIIHH", hdr[20:36])
    data_tag, data_size = struct.unpack("<4sI", hdr[36:44])
    header_ok = (riff == b"RIFF" and wave == b"WAVE" and fmt_tag == b"fmt " and
                 audio_fmt == 1 and channels == 2 and rate == SAMPLE_RATE and
                 bits == 16 and data_tag == b"data" and data_size == data_len and
                 riff_size == 36 + data_len)
    log(f"WAV header check: {'PASS' if header_ok else 'FAIL'} "
        f"(RIFF={riff!r} WAVE={wave!r} fmt={audio_fmt} ch={channels} rate={rate} bits={bits} "
        f"data={data_size} riff_size={riff_size})")
    assert header_ok, "WAV header verification FAILED"

    # measured audio stats from the real render
    ns = len(pcm) // 2
    samples = struct.unpack(f"<{ns}h", pcm)
    peak = max(abs(s) for s in samples)
    rms = math.sqrt(sum(s * s for s in samples) / ns)
    nonzero = sum(1 for s in samples if s != 0)

    proof = {
        "tool": "libxmp",
        "tool_version": "4.6.0 (libxmp4_4.6.0-2_amd64.deb, Ubuntu noble universe)",
        "tool_license": "MIT (catalog: upstream README verified 2026-10-07)",
        "input": {"url": MOD_URL, "path": "Gaffeltruck.mod", "bytes": len(mod_data),
                  "magic_1080": magic.decode("latin1"), "real_upstream_test_file": True},
        "render": {"sample_rate": SAMPLE_RATE, "channels": 2, "bits": 16,
                   "frames": n_samples, "duration_s": round(duration_s, 3),
                   "render_cap_s": MAX_SECONDS, "play_buffer_end_rc": ended,
                   "module_total_time_ms": info.total_time},
        "measured": {"peak": peak, "rms": round(rms, 2),
                     "nonzero_samples": nonzero, "total_samples": ns},
        "wav": {"path": "gaffeltruck_libxmp.wav", "bytes": os.path.getsize(wav_path),
                "header_verified": header_ok},
        "ran": "2026-10-08",
    }
    proof_path = os.path.join(WORKDIR, "libxmp_proof.json")
    with open(proof_path, "w") as f:
        json.dump(proof, f, indent=2)
    assert peak > 0 and nonzero > ns * 0.5, "render produced silence — proof invalid"
    log(f"proof written: {proof_path} (peak={peak}, rms={rms:.1f})")
    log("DONE — libxmp wired with real proof")


if __name__ == "__main__":
    main()
