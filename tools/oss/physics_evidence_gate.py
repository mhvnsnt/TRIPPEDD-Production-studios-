#!/usr/bin/env python3
"""Fail-closed promotion gate for derivative physics evidence."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
HEX40=re.compile(r"^[0-9a-f]{40}$")
HEX64=re.compile(r"^[0-9a-f]{64}$")

def fail(msg):
    print(f"FAIL: {msg}")
    return 1

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def evidence_path(root: Path, receipt_path: Path, value: str) -> Path:
    p=Path(value)
    if not p.is_absolute():
        p=receipt_path.parent/p
    return p.resolve()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("receipt")
    ap.add_argument("--manifest",default="tools/oss/physics_runtime_manifest.json")
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]
    receipt_path=Path(args.receipt).resolve()
    receipt=json.loads(receipt_path.read_text())
    manifest=json.loads((root/args.manifest).read_text())
    if receipt.get("schema") != "trippedd.physics-evidence/v1": return fail("wrong evidence schema")
    if receipt.get("status") != "PASS": return fail("evidence status is not PASS")
    if receipt.get("canonicalSourceMutated") is not False: return fail("canonical source mutation is forbidden")
    lane=next((x for x in manifest["lanes"] if x.get("name")==receipt.get("lane")),None)
    if lane is None: return fail("lane is not registered")
    if receipt.get("upstreamCommit") != lane.get("upstreamCommit") or not HEX40.fullmatch(str(receipt.get("upstreamCommit",""))): return fail("upstream pin mismatch")
    if receipt.get("authority") != lane.get("authority"): return fail("authority mismatch")
    if not receipt.get("exactCommand"): return fail("exact command missing")
    for key in ("inputSha256","outputSha256","visualEvidenceSha256"):
        if not HEX64.fullmatch(str(receipt.get(key,""))): return fail(f"invalid {key}")
    paths=("inputPath","outputPath","visualEvidencePath")
    for key in paths:
        if not receipt.get(key): return fail(f"{key} missing")
    for path_key, hash_key in (("inputPath","inputSha256"),("outputPath","outputSha256"),("visualEvidencePath","visualEvidenceSha256")):
        path=evidence_path(root, receipt_path, receipt[path_key])
        if not path.is_file(): return fail(f"evidence file missing: {path_key}")
        actual=sha256(path)
        if actual != receipt[hash_key]: return fail(f"measured hash mismatch: {hash_key}")
    if int(receipt.get("frameCount",0)) < 1: return fail("no simulation frames")
    contact=receipt.get("contact",{})
    if contact.get("violatingSamples") != 0: return fail("contact violations present")
    if contact.get("selfCollision") == "FAIL": return fail("self-collision failed")
    if lane.get("selfCollisionEvidenceRequired") and contact.get("selfCollision") != "PASS": return fail("self-collision evidence required")
    print(f"PASS: {receipt['lane']} physics evidence is promotion-safe and hashes match measured files")
    return 0

if __name__=='__main__': raise SystemExit(main())
