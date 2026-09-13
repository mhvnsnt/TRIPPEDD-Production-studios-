#!/usr/bin/env python3
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
GATE=ROOT/'tools/oss/physics_evidence_gate.py'
MANIFEST=ROOT/'tools/oss/physics_runtime_manifest.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest=json.loads(MANIFEST.read_text())
    lane=manifest['lanes'][0]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        input_file=root/'input.bin'; output_file=root/'output.bin'; visual_file=root/'evidence.png'
        input_file.write_bytes(b'input fixture')
        output_file.write_bytes(b'derived physics fixture')
        visual_file.write_bytes(b'actual-pixel fixture')
        good={
          'schema':'trippedd.physics-evidence/v1','status':'PASS','lane':lane['name'],
          'authority':lane['authority'],'upstreamCommit':lane['upstreamCommit'],
          'exactCommand':'blender -b MARS_derivative.blend -P simulate.py',
          'inputPath':'input.bin','outputPath':'output.bin','visualEvidencePath':'evidence.png',
          'inputSha256':digest(input_file),'outputSha256':digest(output_file),'visualEvidenceSha256':digest(visual_file),
          'canonicalSourceMutated':False,'frameCount':24,
          'contact':{'maxPenetrationMm':0.0,'violatingSamples':0,'selfCollision':'PASS'}
        }
        p=root/'good.json'; p.write_text(json.dumps(good),encoding='utf-8')
        subprocess.run([sys.executable,str(GATE),str(p)],cwd=ROOT,check=True)
        bad=json.loads(json.dumps(good)); bad['outputSha256']='b'*64
        p.write_text(json.dumps(bad),encoding='utf-8')
        result=subprocess.run([sys.executable,str(GATE),str(p)],cwd=ROOT,text=True,capture_output=True,check=False)
        assert result.returncode != 0 and 'measured hash mismatch' in result.stdout, result.stdout
        bad=json.loads(json.dumps(good)); bad['contact']['selfCollision']='NOT_ATTEMPTED'
        p.write_text(json.dumps(bad),encoding='utf-8')
        result=subprocess.run([sys.executable,str(GATE),str(p)],cwd=ROOT,text=True,capture_output=True,check=False)
        assert result.returncode != 0 and 'self-collision evidence required' in result.stdout, result.stdout
    print('PASS: physics evidence gate measures referenced files and rejects hash drift or missing required collision proof')
if __name__=='__main__': main()
