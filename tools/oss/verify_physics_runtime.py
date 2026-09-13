#!/usr/bin/env python3
"""Fail-closed verifier for the physics/secondary-motion OSS boundary."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
HEX40=re.compile(r"^[0-9a-f]{40}$")

def fail(msg):
    print(f"FAIL: {msg}"); return 1

def main():
    root=Path(__file__).resolve().parents[2]
    manifest=json.loads((root/'tools/oss/physics_runtime_manifest.json').read_text())
    registry=json.loads((root/'tools/oss/full_repo_registry.json').read_text())
    projects={p['path']:p for p in registry['projects']}
    if manifest.get('$schema')!='trippedd.physics-runtime/v1': return fail('wrong manifest schema')
    if manifest.get('canonical')!={'source':'MARS_source.glb','mutationAllowed':False}: return fail('canonical mutation policy is not locked')
    if manifest.get('promotion',{}).get('unknownNeverPass') is not True: return fail('UNKNOWN policy missing')
    if manifest.get('promotion',{}).get('actualPixelsRequired') is not True: return fail('actual-pixel evidence policy missing')
    lanes=manifest.get('lanes',[])
    if not lanes: return fail('no physics lanes')
    for lane in lanes:
        path=lane.get('upstreamPath'); commit=lane.get('upstreamCommit')
        if path not in projects: return fail(f'unregistered upstream: {path}')
        if not HEX40.fullmatch(str(commit or '')): return fail(f'floating/invalid pin: {path}')
        if commit != projects[path].get('commit'): return fail(f'commit mismatch: {path}')
        if not lane.get('authority','').startswith('DERIVATIVE_'): return fail(f'non-derivative authority: {path}')
        if lane.get('outputPolicy') not in {'derived_rig_only','derived_simulation_only'}: return fail(f'unsafe output policy: {path}')
    print(f"PASS: {len(lanes)} physics lanes are pinned and canonical-source safe")
    return 0
if __name__=='__main__': raise SystemExit(main())
