#!/usr/bin/env python3
"""Create a measured derivative-physics evidence receipt from real files."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--upstream-commit', required=True)
    ap.add_argument('--authority', required=True)
    ap.add_argument('--exact-command', required=True)
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--visual', required=True, type=Path)
    ap.add_argument('--frames', required=True, type=int)
    ap.add_argument('--max-penetration-mm', required=True, type=float)
    ap.add_argument('--violating-samples', required=True, type=int)
    ap.add_argument('--self-collision', required=True, choices=('PASS','FAIL','NOT_ATTEMPTED'))
    ap.add_argument('--canonical-source-mutated', action='store_true')
    ap.add_argument('--output-receipt', required=True, type=Path)
    args=ap.parse_args()
    for p in (args.input,args.output,args.visual):
        if not p.is_file():
            raise SystemExit(f'MISSING: {p}')
    if args.frames < 1 or args.max_penetration_mm < 0 or args.violating_samples < 0:
        raise SystemExit('INVALID: numeric evidence')
    receipt={
      'schema':'trippedd.physics-evidence/v1','status':'PASS','lane':args.lane,
      'authority':args.authority,'upstreamCommit':args.upstream_commit,
      'exactCommand':args.exact_command,
      'inputPath':str(args.input.resolve()),'outputPath':str(args.output.resolve()),'visualEvidencePath':str(args.visual.resolve()),
      'inputSha256':sha256(args.input),'outputSha256':sha256(args.output),'visualEvidenceSha256':sha256(args.visual),
      'canonicalSourceMutated':bool(args.canonical_source_mutated),'frameCount':args.frames,
      'contact':{'maxPenetrationMm':args.max_penetration_mm,'violatingSamples':args.violating_samples,'selfCollision':args.self_collision}
    }
    args.output_receipt.parent.mkdir(parents=True,exist_ok=True)
    args.output_receipt.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f'WROTE: {args.output_receipt}')
    print(f"INPUT_SHA256: {receipt['inputSha256']}")
    print(f"OUTPUT_SHA256: {receipt['outputSha256']}")
    print(f"VISUAL_SHA256: {receipt['visualEvidenceSha256']}")

if __name__=='__main__': main()
