#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
GATE=ROOT/'tools/oss/physics_evidence_gate.py'
MANIFEST=ROOT/'tools/oss/physics_runtime_manifest.json'

def main():
    manifest=json.loads(MANIFEST.read_text())
    lane=manifest['lanes'][0]
    good={
      'schema':'trippedd.physics-evidence/v1','status':'PASS','lane':lane['name'],
      'authority':lane['authority'],'upstreamCommit':lane['upstreamCommit'],
      'exactCommand':'blender -b MARS_derivative.blend -P simulate.py',
      'inputSha256':'a'*64,'outputSha256':'b'*64,'visualEvidenceSha256':'c'*64,
      'canonicalSourceMutated':False,'frameCount':24,
      'contact':{'maxPenetrationMm':0.0,'violatingSamples':0,'selfCollision':'PASS'}
    }
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'good.json'; p.write_text(json.dumps(good),encoding='utf-8')
        subprocess.run([sys.executable,str(GATE),str(p)],cwd=ROOT,check=True)
        bad=json.loads(json.dumps(good)); bad['contact']['selfCollision']='NOT_ATTEMPTED'
        p.write_text(json.dumps(bad),encoding='utf-8')
        result=subprocess.run([sys.executable,str(GATE),str(p)],cwd=ROOT,text=True,capture_output=True,check=False)
        assert result.returncode != 0 and 'self-collision evidence required' in result.stdout, result.stdout
    print('PASS: physics evidence gate accepts complete evidence and rejects missing required collision proof')
if __name__=='__main__': main()
