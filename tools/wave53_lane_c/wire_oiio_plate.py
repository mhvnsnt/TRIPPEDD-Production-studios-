#!/usr/bin/env python3
"""Wave 53 Lane C — wire_oiio_plate.py (MIT)

HDR plate wrangling for the video pipeline with OpenImageIO
(AcademySoftwareFoundation/OpenImageIO) — Apache-2.0 (verified 2026-10-08
via GitHub API spdx_id). This wire script is original MIT-licensed code;
OIIO is imported as an external library, never embedded.

What it does:
  1. Reads a REAL pipeline frame (Wave 50 caption burn-in proof PNG,
     640x360, rendered pixels) through OIIO's ImageInput.
  2. Writes it to OpenEXR (half float) with production metadata attributes,
     reads it back through ImageInput.
  3. Measures: max absolute per-channel pixel error of the EXR round-trip
     (0-1 float scale), metadata attribute round-trip equality, OIIO's own
     compute-stats cross-check (average pixel) vs numpy.
  4. Negative/positive control: PNG->JPEG (quality 95) conversion —
     expected LOSSY, so it is measured and reported but must NOT pass an
     EXR-grade gate (honest about lossy codecs).
  5. Determinism: two EXR writes -> byte-identical files.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "oiio_plate")
SRC_PNG = os.path.abspath(os.path.join(
    HERE, "..", "wave50_lane_c", "proofs", "caption_burnin",
    "proof_frame_1_5s.png"))

os.makedirs(PROOFS, exist_ok=True)


def main():
    t0 = time.time()
    import numpy as np
    import OpenImageIO as oiio

    # 1. read real input through OIIO
    inp = oiio.ImageInput.open(SRC_PNG)
    assert inp is not None, "OIIO could not open input PNG"
    spec = inp.spec()
    px = inp.read_image()  # float32 array
    inp.close()
    h, w, ch = spec.height, spec.width, spec.nchannels

    # OIIO-native stats cross-check vs numpy
    stats = oiio.ImageBufAlgo.computePixelStats(oiio.ImageBuf(SRC_PNG))
    oiio_avg = [float(v) for v in stats.avg]
    np_avg = [float(v) for v in px.reshape(-1, ch).mean(axis=0)]
    avg_agree = max(abs(a - b) for a, b in zip(oiio_avg, np_avg))

    # 2. EXR (half) write with production metadata
    exr_path = os.path.join(PROOFS, "plate_half.exr")
    exr2_path = os.path.join(PROOFS, "plate_half_b.exr")
    espec = oiio.ImageSpec(w, h, ch, oiio.HALF)
    px_half = px.astype("float16")
    espec.attribute("wave53:lane", "wave53_lane_c")
    espec.attribute("wave53:tool", "OpenImageIO plate QC")
    espec.attribute("Software", "wave53_lane_c wire_oiio_plate.py")
    espec.attribute("compression", "zip")
    for p in (exr_path, exr2_path):
        out = oiio.ImageOutput.create(p)
        assert out is not None
        out.open(p, espec)
        out.write_image(px_half)
        out.close()

    # 3. read back + measure
    back = oiio.ImageInput.open(exr_path)
    bspec = back.spec()
    px_back = back.read_image()
    back.close()
    maxdiff = float(np.abs(px.astype("float64") - px_back.astype("float64")).max())
    meta_ok = (bspec.getattribute("wave53:lane") == "wave53_lane_c"
               and bspec.getattribute("wave53:tool") == "OpenImageIO plate QC"
               and bspec.getattribute("Software")
               == "wave53_lane_c wire_oiio_plate.py")
    det_same = (open(exr_path, "rb").read() == open(exr2_path, "rb").read())
    fmt_ok = bspec.format == oiio.HALF

    # 4. lossy control: PNG -> JPEG q95 (expected lossy; measured, not gated hard)
    jpg_path = os.path.join(PROOFS, "plate_q95.jpg")
    jspec = oiio.ImageSpec(w, h, ch, oiio.UINT8)
    jspec.attribute("compression", "95")
    jout = oiio.ImageOutput.create(jpg_path)
    jout.open(jpg_path, jspec)
    jout.write_image((px * 255).round().astype("uint8"))
    jout.close()
    jback = oiio.ImageInput.open(jpg_path)
    px_jpg = jback.read_image().astype("float64") / 255.0
    jback.close()
    jpg_maxdiff = float(np.abs(px.astype("float64") - px_jpg).max())

    exr_bytes = os.path.getsize(exr_path)
    jpg_bytes = os.path.getsize(jpg_path)
    elapsed = time.time() - t0

    checks = {
        "input_read_ok": h == 360 and w == 640 and ch >= 3,
        # OIIO stats run on the UINT8 buffer, numpy on float32: tiny
        # accumulation-path difference is expected; gate at 1e-3, not 1e-6.
        "oiio_stats_agree_numpy": avg_agree < 1e-3,
        "exr_is_half": fmt_ok,
        "exr_roundtrip_maxdiff_le_0.002": maxdiff <= 0.002,
        "metadata_roundtrip": meta_ok,
        "exr_writes_byte_identical": det_same,
        "jpeg_lossy_measured": jpg_maxdiff > 0,  # honest: lossy is lossy
    }
    result = {
        "tool": "OpenImageIO",
        "upstream_license": "Apache-2.0",
        "wire_script_license": "MIT",
        "oiio_version": str(oiio.VERSION_STRING)
            if hasattr(oiio, "VERSION_STRING") else "unknown",
        "input": SRC_PNG,
        "input_whc": [w, h, ch],
        "oiio_pixelstats_avg": [round(v, 6) for v in oiio_avg],
        "numpy_avg": [round(v, 6) for v in np_avg],
        "stats_max_abs_disagree": avg_agree,
        "exr_roundtrip_max_abs_diff": maxdiff,
        "metadata_roundtrip_ok": meta_ok,
        "exr_bytes": exr_bytes,
        "jpeg_q95_max_abs_diff": round(jpg_maxdiff, 6),
        "jpeg_q95_bytes": jpg_bytes,
        "exr_determinism_byte_identical": det_same,
        "elapsed_s": round(elapsed, 2),
        "checks": checks,
        "PASS": all(checks.values()),
    }
    with open(os.path.join(PROOFS, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
