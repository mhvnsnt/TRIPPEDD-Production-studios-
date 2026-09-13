#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
WRITER=ROOT/'tools/oss/write_physics_evidence_receipt.py'
GATE=ROOT/'tools/oss/physics_evidence_gate.py'
MANIFEST=ROOT/'tools/oss/physics_runtime_manifest.json'

def main():
    manifest=json.loads(MANIFEST.read_text())
    lane=manifest['lanes'][0]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        inp=root/'input.blend'; out=root/'derived.blend'; visual=root/'frame.png'; receipt=root/'receipt.json'
        inp.write_bytes(b'canonical-derived fixture input')
        out.write_bytes(b'derived simulation output')
        visual.write_bytes(b'actual pixels')
        subprocess.run([
          sys.executable,str(WRITER),'--lane',lane['name'],'--upstream-commit',lane['upstreamCommit'],
          '--authority',lane['authority'],'--exact-command','blender -b input.blend -P simulate.py',
          '--input',str(inp),'--output',str(out),'--visual',str(visual),'--frames','24',
          '--max-penetration-mm','0','--violating-samples','0','--self-collision','PASS',
          '--output-receipt',str(receipt)
        ],cwd=ROOT,check=True)
        data=json.loads(receipt.read_text())
        assert data['status']=='PASS'
        assert data['canonicalSourceMutated'] is False
        subprocess.run([sys.executable,str(GATE),str(receipt)],cwd=ROOT,check=True)
    print('PASS: receipt writer hashes real files and emits a gateable physics receipt')
if __name__=='__main__': main()
