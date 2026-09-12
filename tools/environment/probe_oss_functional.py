#!/usr/bin/env python3
"""Functionally probe installed OSS tools without producing production evidence."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, tempfile, struct, zlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def run(cmd: list[str], timeout: int = 15) -> dict[str, object]:
    exe = shutil.which(cmd[0])
    if not exe:
        return {"status": "UNAVAILABLE", "command": cmd, "path": None}
    try:
        p = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=timeout)
        return {"status": "PASS" if p.returncode == 0 else "FAIL", "returncode": p.returncode,
                "path": exe, "output": (p.stdout or p.stderr).strip().splitlines()[:8]}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "FAIL", "path": exe, "error": str(exc)}

def make_png(path: Path) -> None:
    raw = b"\x00" + b"\xff\x00\x00\xff" * 2 + b"\x00" + b"\x00\xff\x00\xff" * 2
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 2, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=ROOT / ".artifacts/evidence/oss-functional-probes.json")
    args = ap.parse_args()
    result: dict[str, object] = {
        "schema": "trippedd.oss-functional-probes/v1",
        "status": "FUNCTIONAL_CAPABILITY_PROBE",
        "evidence_status": "NOT_ATTEMPTED",
        "production_evidence": False,
        "policy": {
            "synthetic_fixture_only": True,
            "functional_probe_is_not_production_evidence": True,
            "tool_availability_never_promotes_production": True,
            "capability_pass_is_not_render_pass": True,
            "exact_production_artifact_required": True,
            "visual_qc_not_attempted": True,
            "physical_qc_not_attempted": True,
        }, "checks": {}
    }
    with tempfile.TemporaryDirectory(prefix="trippedd-oss-probe-") as td:
        png = Path(td) / "fixture.png"; make_png(png)
        result["fixture"] = {"sha256": hashlib.sha256(png.read_bytes()).hexdigest(), "bytes": png.stat().st_size}
        checks = result["checks"]
        checks["oiio_iinfo_png"] = run(["iinfo", str(png)])
        checks["oiio_idiff_self"] = run(["idiff", str(png), str(png)])
        checks["oiiotool_info_png"] = run(["oiiotool", "--info", str(png)])
        checks["blender_version"] = run(["blender", "--version"])
        checks["ffmpeg_version"] = run(["ffmpeg", "-version"])
        checks["openrv_version"] = run(["rv", "-version"])
        checks["xstudio_version"] = run(["xstudio", "--version"])
        checks["cueadmin_version"] = run(["cueadmin", "--version"])
    result["summary"] = {"functional_passes": sum(v.get("status") == "PASS" for v in result["checks"].values()),
                          "functional_failures": sum(v.get("status") == "FAIL" for v in result["checks"].values()),
                          "unavailable": sum(v.get("status") == "UNAVAILABLE" for v in result["checks"].values())}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
