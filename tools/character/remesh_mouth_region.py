"""
STAGE B -- REBUILD THE TOPOLOGY OF HIS MOUTH REGION, AND NOTHING ELSE.

    261 faces fill his entire mouth. Some carry edges longer than his whole lip
    aperture, against a head whose median face is 0.59 mm2. Cutting that region
    has now measured neutral-or-worse four separate times -- one plane cannot
    follow a crease that curves across a 22 mm face, and a 13 mm2 face cannot
    carry a lip. It does not need another cut; it needs geometry.

PULLED, NOT WRITTEN: PyMeshLab (MeshLab's own engine). Its isotropic explicit
remesher takes `selectedonly`, so the mouth region is rebuilt IN PLACE while the
rest of his head is untouched and still attached to it -- which removes the
extract-a-patch-and-stitch-it-back step where this kind of repair usually dies.

THE GATE THAT MATTERS IS NOT THE FACE COUNT. It is that every vertex OUTSIDE the
region is byte-identical afterwards. If the remesher wanders outside its
selection, every measurement banked against this head is void and the shape-key
transfer stops being a local operation.

  python tools/character/remesh_mouth_region.py --target-mm 1.2
"""
import argparse, json, os, sys
import numpy as np
import pymeshlab as ml


def read_ply(path):
    with open(path) as f:
        head, line = [], f.readline()
        while True:
            head.append(line.strip())
            if line.strip() == "end_header":
                break
            line = f.readline()
        nv = nf = 0
        props = []
        cur = None
        for h in head:
            if h.startswith("element vertex"): nv = int(h.split()[-1]); cur = "v"
            elif h.startswith("element face"): nf = int(h.split()[-1]); cur = "f"
            elif h.startswith("property") and cur == "v": props.append(h.split()[-1])
        V = np.array([[float(x) for x in f.readline().split()] for _ in range(nv)])
        F = np.array([[int(x) for x in f.readline().split()[1:4]] for _ in range(nf)], dtype=np.int64)
    return V, F, props


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ply", default="renders/_remesh/head_rest.ply")
    ap.add_argument("--meta", default="renders/_remesh/head_rest.json")
    ap.add_argument("--out", default="renders/_remesh/head_remeshed.ply")
    ap.add_argument("--target-mm", type=float, default=1.2)
    ap.add_argument("--max-surf-mm", type=float, default=0.4)
    ap.add_argument("--iterations", type=int, default=6)
    ap.add_argument("--drift-mm", type=float, default=1e-4,
                    help="how far a vertex OUTSIDE the region may move. It may not.")
    a = ap.parse_args()

    meta = json.load(open(a.meta))
    MM = float(meta["mmPerUnit"])
    V0, F0, props = read_ply(a.ply)
    qi = props.index("quality")
    sel0 = V0[:, qi] > 0.5
    P0 = V0[:, :3]
    print("in:  %d verts, %d tris, %d flagged (%.0f mm radius)"
          % (len(P0), len(F0), int(sel0.sum()), meta["radiusMM"]), flush=True)

    ms = ml.MeshSet()
    ms.load_new_mesh(a.ply)
    ms.compute_selection_by_scalar_per_vertex(minq=0.5, maxq=2.0)
    ms.compute_selection_transfer_vertex_to_face(inclusive=False)
    m = ms.current_mesh()
    print("pymeshlab sees %d selected verts, %d selected faces"
          % (m.selected_vertex_number(), m.selected_face_number()), flush=True)
    if m.selected_face_number() < 50:
        print("*** REFUSED: only %d faces selected -- nothing to rebuild"
              % m.selected_face_number()); return 1

    ms.meshing_isotropic_explicit_remeshing(
        iterations=a.iterations, selectedonly=True, adaptive=False,
        targetlen=ml.PureValue(a.target_mm * MM),
        checksurfdist=True, maxsurfdist=ml.PureValue(a.max_surf_mm * MM),
        splitflag=True, collapseflag=True, swapflag=True,
        smoothflag=True, reprojectflag=True)
    ms.save_current_mesh(a.out, save_vertex_quality=False, binary=False)
    V1, F1, _ = read_ply(a.out)
    P1 = V1[:, :3]
    print("out: %d verts, %d tris  (%+d verts, %+d tris)"
          % (len(P1), len(F1), len(P1) - len(P0), len(F1) - len(F0)), flush=True)

    # ── THE GATE: HIS HEAD OUTSIDE THE MOUTH MUST NOT HAVE MOVED ───────────
    # PyMeshLab keeps untouched vertices at the FRONT of the array in this
    # filter, but that is an implementation detail, so it is checked rather than
    # assumed -- and checked by POSITION, which cannot be fooled by reordering.
    # BY POSITION, NOT BY INDEX. The first version of this gate compared P1[i] to
    # P0[i] and reported 244.49 mm -- PyMeshLab REORDERS its vertices, so that was
    # measuring the reordering, not any movement. I had even written the comment
    # saying index alignment was an implementation detail and then relied on it.
    # The question is only ever "is there still a vertex exactly where that one
    # was", and a KD-tree answers it whatever the order.
    from scipy.spatial import cKDTree
    keep = np.nonzero(~sel0)[0]
    tree = cKDTree(P1)
    dist, _idx = tree.query(P0[keep], k=1)
    same_prefix = float(dist.max()) / MM if len(keep) else 0.0
    lost = int((dist / MM > a.drift_mm).sum())
    print("untouched vertices: %d checked by POSITION, worst displacement %.6f mm, "
          "%d without an exact match" % (len(keep), same_prefix, lost), flush=True)
    if same_prefix > a.drift_mm:
        print("*** REFUSED: the remesher moved vertices OUTSIDE the mouth region by "
              "%.6f mm. Every measurement banked against this head would be void."
              % same_prefix)
        return 1

    json.dump({"schema": "trippedd.mouth-remesh/v1",
               "in": {"verts": int(len(P0)), "tris": int(len(F0)),
                      "flagged": int(sel0.sum())},
               "out": {"verts": int(len(P1)), "tris": int(len(F1))},
               "targetEdgeMM": a.target_mm, "maxSurfDistMM": a.max_surf_mm,
               "iterations": a.iterations,
               "untouchedDriftMM": float(same_prefix), "untouchedChecked": int(len(keep)),
               "engine": "pymeshlab meshing_isotropic_explicit_remeshing selectedonly",
               "ply": a.out},
              open(os.path.join(os.path.dirname(a.out), "remesh.json"), "w"), indent=2)
    print("remeshed -> %s" % a.out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
