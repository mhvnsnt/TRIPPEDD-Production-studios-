#!/usr/bin/env python3
"""Build an oral-only donor package from Google GNM Head v3.

MARS_CANONICAL is never edited. The output contains only GNM oral anatomy and
the official expression basis needed for later retargeting.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np

GROUPS = ("upper_teeth_and_gums", "lower_teeth_and_gums", "tongue")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def group_members(names, weights, name):
    if name not in names:
        raise RuntimeError(f"GNM anatomy missing required group: {name}")
    return np.flatnonzero(weights[names.index(name)] > 0.5)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--gnm-npz",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    src=Path(a.gnm_npz).resolve(); out=Path(a.output).resolve(); out.mkdir(parents=True,exist_ok=True)
    if not src.is_file() or src.stat().st_size==0: raise SystemExit("GNM_ORAL_DONOR: FAIL — source missing/empty")
    m=np.load(src,allow_pickle=False)
    v=np.asarray(m["template_vertex_positions"],dtype=np.float32)
    tris=np.asarray(m["triangles"],dtype=np.int32)
    names=[str(x) for x in m["vertex_group_names"]]
    groups=np.asarray(m["vertex_groups"],dtype=np.float32)
    upper=group_members(names,groups,GROUPS[0]); lower=group_members(names,groups,GROUPS[1]); tongue=group_members(names,groups,GROUPS[2])
    oral=np.zeros(len(v),dtype=bool); oral[np.concatenate([upper,lower,tongue])]=True
    face_mask=np.all(oral[tris],axis=1)
    faces=tris[face_mask]
    used=np.unique(faces)
    remap=np.full(len(v),-1,dtype=np.int32); remap[used]=np.arange(len(used),dtype=np.int32)
    faces=remap[faces]
    expr=np.asarray(m["expression_basis"],dtype=np.float32)
    expr_names=np.asarray(m["expression_names"])
    upper_c=v[upper].mean(0); lower_c=v[lower].mean(0)
    axis=lower_c-upper_c; axis/=max(float(np.linalg.norm(axis)),1e-8)
    lower_names=[str(n) for n in expr_names if str(n).startswith("lower_face_region_")]
    name_to_idx={str(n):i for i,n in enumerate(expr_names)}
    scores=[]
    for name in lower_names:
        d=expr[name_to_idx[name]]
        scores.append((float(np.mean(d[lower]@axis)-np.mean(d[upper]@axis)),name_to_idx[name],name))
    if not scores: raise RuntimeError("GNM_ORAL_DONOR: no lower-face basis")
    score,jaw_idx,jaw_name=max(scores,key=lambda x:abs(x[0]))
    jaw=expr[jaw_idx][used].copy()
    if score<0: jaw=-jaw
    jaw[np.isin(used,upper)]=0
    np.savez_compressed(
        out/"oral_donor.npz",
        vertices=v[used],faces=faces,
        upper_mask=np.isin(used,upper),lower_mask=np.isin(used,lower),tongue_mask=np.isin(used,tongue),
        expression_basis=expr[:,used,:],expression_names=expr_names,jaw_open_delta=jaw,
        gap_axis=axis,upper_centroid=upper_c,lower_centroid=lower_c)
    manifest={
        "schema":"god-molecule.gnm-oral-donor.v1","source":"google/GNM","license":"Apache-2.0",
        "gnm_npz_sha256":sha256(src),"source_vertices":int(len(v)),"oral_vertices":int(len(used)),
        "oral_triangles":int(len(faces)),"upper_teeth_vertices":int(len(upper)),
        "lower_teeth_vertices":int(len(lower)),"tongue_vertices":int(len(tongue)),
        "expression_dimensions":int(expr.shape[0]),"jaw_open_basis_index":int(jaw_idx),
        "jaw_open_basis_name":jaw_name,"jaw_open_score":float(score),
        "status":"DONOR_READY","mars_identity_replacement":False}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("GNM_ORAL_DONOR: VERIFIED")
    print(f"JAW_OPEN_BASIS={jaw_name} SCORE={score:.6f}")
    print(f"MANIFEST={out/'manifest.json'}")

if __name__=="__main__": main()
