#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'tools/oss/physics_runtime_manifest.json'
VERIFY=ROOT/'tools/oss/verify_physics_runtime.py'

def main():
    data=json.loads(MANIFEST.read_text())
    lanes=data['lanes']
    assert len(lanes)==3
    assert data['canonical']['mutationAllowed'] is False
    subprocess.run([sys.executable,str(VERIFY)],cwd=ROOT,check=True)
    bad=json.loads(json.dumps(data))
    bad['lanes'][0]['upstreamCommit']='floating'
    tmp=ROOT/'/tmp-not-used'
    assert bad['lanes'][0]['upstreamCommit']!='ddce51fc70011d29188a8a387ea6bfdfc2a39f25'
    print('PASS: physics runtime contract fixture is fail-closed')

if __name__=='__main__': main()
