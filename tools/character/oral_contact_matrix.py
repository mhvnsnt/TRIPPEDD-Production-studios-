"""
EVERY PART AGAINST EVERY OTHER PART. ONE MATRIX.

    "collision between all parts so they sense each other and clipping fixes for
     everything are necessary"                          -- the owner, 2026-09-13

Stage 2 of the pair that keeps Blender out of the maths: the session exports
evaluated world-space geometry to a .npz (tools/session/snippets/oral_export.py),
and this measures it in the venv, where libigl and numpy 2.x live. No Blender, no
re-bake -- any agent can re-run this from the published .npz alone.

THE DEFINITION OF "INSIDE" IS THE ONE THIS PROJECT ALREADY PROVED. Not a
pseudonormal sign (that scored collision ON WORSE than OFF on this very head),
and not a mesh boolean: a libigl generalized WINDING NUMBER, which is robust on
the open shells every one of these parts actually is. Negative is inside;
verified on a unit sphere.

AND AN OPEN SHELL IS NOT A SOLID, WHICH IS WHY DIRECTION MATTERS. His teeth
arches carry 50 boundary edges, the sock 58, the tongue 40. Asking "is this
tongue vertex inside the solid of the teeth" is not the same question as asking
it the other way round, so BOTH directions are reported and neither is quietly
dropped.

  python tools/character/oral_contact_matrix.py --npz renders/_oral_contact/oral_open.npz
"""
import argparse, json, os, sys
import numpy as np
import igl


def sd(P, V, F):
    S = igl.signed_distance(np.ascontiguousarray(P, dtype=np.float64),
                            np.ascontiguousarray(V, dtype=np.float64),
                            np.ascontiguousarray(F, dtype=np.int32),
                            igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
    return np.asarray(S[0], dtype=np.float64), np.asarray(S[1], dtype=np.int64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="renders/_oral_contact/oral_open.npz")
    ap.add_argument("--export-json", default="renders/_oral_contact/oral_export.json")
    ap.add_argument("--out", default="renders/_oral_contact/contact_matrix.json")
    ap.add_argument("--tol-mm", type=float, default=0.25,
                    help="below this a contact is touching, not clipping")
    ap.add_argument("--gate-mm", type=float, default=1.0)
    a = ap.parse_args()

    z = np.load(a.npz)
    meta = json.load(open(a.export_json)) if os.path.exists(a.export_json) else {}
    MM = float(meta.get("mmPerUnit") or 0.0)
    if MM <= 0:
        print("*** REFUSED: the export carries no mmPerUnit, so nothing can be stated "
              "in his millimetres", flush=True)
        return 1
    parts = sorted({k.split("/")[0] for k in z.files if k.endswith("/verts")})
    print("parts: %s" % ", ".join(p.replace("MARS_", "") for p in parts), flush=True)

    G = {p: (z["%s/verts" % p], z["%s/tris" % p]) for p in parts}
    rows, worst = [], []
    for A in parts:
        for B in parts:
            if A == B: continue
            PA, _ = G[A]; VB, FB = G[B]
            S, _I = sd(PA, VB, FB)
            inside = S < 0.0
            n = int(inside.sum())
            depth = float((-S[inside]).max()) / MM if n else 0.0
            mean = float((-S[inside]).mean()) / MM if n else 0.0
            gap = float(S.min()) / MM          # nearest approach when nothing is inside
            rows.append({"a": A, "b": B, "vertsInside": n, "ofVerts": int(len(PA)),
                         "maxDepthMM": round(depth, 4), "meanDepthMM": round(mean, 4),
                         "nearestGapMM": round(gap, 4)})
            if depth > a.tol_mm:
                worst.append((depth, n, A, B))

    print("\n%-18s %-18s %8s %10s %10s %10s"
          % ("A (its verts)", "inside B's solid", "count", "max mm", "mean mm", "nearest"), flush=True)
    for r in sorted(rows, key=lambda x: -x["maxDepthMM"]):
        if r["vertsInside"] == 0 and r["nearestGapMM"] > 2.0: continue
        print("%-18s %-18s %8s %10.3f %10.3f %10.3f"
              % (r["a"].replace("MARS_", ""), r["b"].replace("MARS_", ""),
                 "%d/%d" % (r["vertsInside"], r["ofVerts"]),
                 r["maxDepthMM"], r["meanDepthMM"], r["nearestGapMM"]), flush=True)

    print("\nclipping deeper than %.2f mm:" % a.tol_mm, flush=True)
    if not worst:
        print("  none", flush=True)
    for d, n, A, B in sorted(worst, reverse=True):
        print("  %-18s into %-18s %7.3f mm  (%d verts)"
              % (A.replace("MARS_", ""), B.replace("MARS_", ""), d, n), flush=True)

    # ── THE ONLY VERSION OF THE QUESTION THAT MEANS ANYTHING ────────────────
    # MARS_MESH is a CLOSED head shell, so "his teeth are inside MARS_MESH" is
    # TRUE AND CORRECT -- his teeth live in his head. This project has been caught
    # by that before (a tongue read 9.73 mm / 113 of 146 violating at REST purely
    # because the head is closed). The question that matters is whether the teeth
    # sit inside the CARVED CAVITY, which is air, or inside solid skull material.
    #
    # igl returns the closest FACE with the distance, so the classification is
    # free: a tooth vertex inside the head whose nearest surface is an ORAL_MAT
    # face is in the cavity; one whose nearest surface is his SKIN is buried in
    # material that should have been carved away.
    cav = {}
    hv, hf = G.get("MARS_MESH", (None, None))
    tp = z["MARS_MESH/triPoly"] if "MARS_MESH/triPoly" in z.files else None
    oralmask = None
    for k in z.files:
        if k.startswith("MARS_MESH/mat/") and "ORAL" in k.upper():
            oralmask = z[k]
    if hv is not None and tp is not None and oralmask is not None:
        tri_is_cavity = oralmask[np.clip(tp, 0, len(oralmask) - 1)].astype(bool)
        print("\nof his head's %d triangles, %d are carved cavity wall"
              % (len(tp), int(tri_is_cavity.sum())), flush=True)
        for A in parts:
            if A == "MARS_MESH": continue
            PA, _ = G[A]
            S, I = sd(PA, hv, hf)
            ins = S < 0.0
            if not ins.any():
                cav[A] = {"inside": 0}; continue
            near_cav = tri_is_cavity[np.clip(I[ins], 0, len(tri_is_cavity) - 1)]
            d = (-S[ins]) / MM
            cav[A] = {"inside": int(ins.sum()),
                      "nearestIsCavityWall": int(near_cav.sum()),
                      "nearestIsHisSkin": int((~near_cav).sum()),
                      "maxDepthIntoSkinMM": round(float(d[~near_cav].max()), 3) if (~near_cav).any() else 0.0}
            print("  %-18s inside his head %4d verts -- nearest surface is the cavity "
                  "wall for %4d, HIS SKIN for %4d (deepest %.2f mm)"
                  % (A.replace("MARS_", ""), cav[A]["inside"], cav[A]["nearestIsCavityWall"],
                     cav[A]["nearestIsHisSkin"], cav[A]["maxDepthIntoSkinMM"]), flush=True)

    out = {"schema": "trippedd.oral-contact-matrix/v1", "insideHeadClassified": cav, "npz": a.npz,
           "mmPerUnit": MM, "pose": meta.get("pose"), "jawDeg": meta.get("jawDeg"),
           "tolMM": a.tol_mm, "gateMM": a.gate_mm,
           "method": "libigl generalized winding number; negative is inside. Both "
                     "directions of every pair are reported because these parts are "
                     "OPEN shells (teeth 50 boundary edges, sock 58, tongue 40) and "
                     "A-inside-B is not the same question as B-inside-A.",
           "expectedContainment": {"%s inside %s" % k: v for k, v in {
               ("MARS_TEETH_UPPER","MARS_MOUTH_SOCK"):"his teeth sit inside the vestibule lining",
               ("MARS_TEETH_LOWER","MARS_MOUTH_SOCK"):"his teeth sit inside the vestibule lining",
               ("MARS_TONGUE","MARS_MOUTH_SOCK"):"his tongue sits inside the vestibule lining"}.items()},
           "pairs": rows,
           "worst": [{"a": A, "b": B, "maxDepthMM": round(d, 4), "verts": n}
                     for d, n, A, B in sorted(worst, reverse=True)]}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=2)
    print("\nmatrix -> %s" % a.out, flush=True)
    # THE GATE READS THE CLASSIFIED NUMBER, NOT THE RAW ONE. Raw, "TEETH_UPPER
    # 14.46 mm inside MESH" looks like his teeth are buried in his skull; every one
    # of those 582 vertices is nearest the CAVITY WALL, i.e. his teeth are in his
    # mouth, where they belong. A gate on the raw depth fires on correct anatomy
    # and would have sent someone off to "fix" it. Only a part inside his head
    # whose nearest surface is HIS SKIN is through something.
    over = []
    for A, c in cav.items():
        if c.get("nearestIsHisSkin", 0) and c.get("maxDepthIntoSkinMM", 0.0) > a.gate_mm:
            over.append((c["maxDepthIntoSkinMM"], c["nearestIsHisSkin"], A, "HIS SKIN"))
    # CONTAINMENT THAT IS ANATOMY, DECLARED WITH ITS REASON RATHER THAN SILENTLY
    # DROPPED. MARS_MOUTH_SOCK is the vestibule LINING -- a bag his teeth and
    # tongue sit inside. "TEETH_UPPER is 11.5 mm inside MOUTH_SOCK, 1198 of 1440
    # verts" is that bag doing its job, and a gate that fires there is a gate that
    # fires on a correct mouth. The same is true of anything inside MARS_MESH,
    # which is a closed head shell (see insideHeadClassified above -- that one is
    # resolved by WHICH SURFACE is nearest, not by exempting it).
    # This is the only exemption list, it is short, and each line says why.
    EXPECTED = {
        ("MARS_TEETH_UPPER", "MARS_MOUTH_SOCK"): "his teeth sit inside the vestibule lining",
        ("MARS_TEETH_LOWER", "MARS_MOUTH_SOCK"): "his teeth sit inside the vestibule lining",
        ("MARS_TONGUE", "MARS_MOUTH_SOCK"):      "his tongue sits inside the vestibule lining",
    }
    for d, n, A, B in worst:
        if A == "MARS_MESH" or B == "MARS_MESH": continue      # closed-shell artifact
        if (A, B) in EXPECTED:
            print("  expected: %-16s inside %-16s %7.3f mm -- %s"
                  % (A.replace("MARS_", ""), B.replace("MARS_", ""), d, EXPECTED[(A, B)]),
                  flush=True)
            continue
        if d > a.gate_mm: over.append((d, n, A, B))
    print("", flush=True)
    if over:
        for d, n, A, B in sorted(over, reverse=True):
            print("GATE FAIL: %-16s through %-16s %7.3f mm (%d verts)"
                  % (A.replace("MARS_", ""), B.replace("MARS_", ""), d, n), flush=True)
        return 45
    print("GATE: nothing is through anything by more than %.2f mm" % a.gate_mm, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
