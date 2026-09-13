#!/usr/bin/env python3
"""Fail-closed verifier for the physics/secondary-motion OSS boundary."""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SUBMODULE = re.compile(r"\[submodule \"(?P<path>[^\"]+)\"\]\n\tpath = (?P=path)\n\turl = (?P<url>[^\n]+)")


def fail(msg):
    print(f"FAIL: {msg}")
    return 1


def gitlink_sha(root: Path, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "ls-files", "--stage", "--", path],
        cwd=root, text=True, capture_output=True, check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    mode, sha, _stage, indexed_path = proc.stdout.strip().split("\t", 1)[0].split() + [proc.stdout.strip().split("\t", 1)[1]]
    if mode != "160000" or indexed_path != path:
        return None
    return sha


def submodule_urls(root: Path) -> dict[str, str]:
    text = (root / ".gitmodules").read_text()
    return {m.group("path"): m.group("url").removesuffix(".git") for m in SUBMODULE.finditer(text)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--registry", default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    manifest_path = Path(args.manifest) if args.manifest else root / "tools/oss/physics_runtime_manifest.json"
    registry_path = Path(args.registry) if args.registry else root / "tools/oss/full_repo_registry.json"
    manifest = json.loads(manifest_path.read_text())
    registry = json.loads(registry_path.read_text())
    projects = {p["path"]: p for p in registry["projects"]}
    urls = submodule_urls(root)
    if manifest.get("$schema") != "trippedd.physics-runtime/v1": return fail("wrong manifest schema")
    if manifest.get("canonical") != {"source": "MARS_source.glb", "mutationAllowed": False}: return fail("canonical mutation policy is not locked")
    if manifest.get("promotion", {}).get("unknownNeverPass") is not True: return fail("UNKNOWN policy missing")
    if manifest.get("promotion", {}).get("actualPixelsRequired") is not True: return fail("actual-pixel evidence policy missing")
    lanes = manifest.get("lanes", [])
    if not lanes: return fail("no physics lanes")
    for lane in lanes:
        path = lane.get("upstreamPath")
        commit = lane.get("upstreamCommit")
        if path not in projects: return fail(f"unregistered upstream: {path}")
        if not HEX40.fullmatch(str(commit or "")): return fail(f"floating/invalid pin: {path}")
        project = projects[path]
        if commit != project.get("commit"): return fail(f"registry commit mismatch: {path}")
        expected_url = str(project.get("repository", "")).removesuffix(".git")
        actual_url = urls.get(path)
        if actual_url != expected_url: return fail(f".gitmodules URL mismatch: {path}")
        actual_sha = gitlink_sha(root, path)
        if actual_sha is None: return fail(f"missing gitlink: {path}")
        if actual_sha != commit: return fail(f"gitlink commit mismatch: {path}")
        if not lane.get("authority", "").startswith("DERIVATIVE_"): return fail(f"non-derivative authority: {path}")
        if lane.get("outputPolicy") not in {"derived_rig_only", "derived_simulation_only"}: return fail(f"unsafe output policy: {path}")
    print(f"PASS: {len(lanes)} physics lanes are registry-, gitlink-, URL-, and canonical-source-safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
