#!/usr/bin/env python3
"""
STAGE 2: MEASURE PENETRATION. The numbers behind tools/character/contact_gate.py.

The owner asked for this directly:

    "I think we're gonna need, like, some sort of collision detection or something,
     so hair can't, like, face through the face or, like, you know, so the tongue
     can't face through the cheeks... each piece has collision detection with the
     other stuff... so that we don't get super glitchy buggy animations unless we
     start asking for that."

contact_gate.py already knows how to JUDGE a contact receipt. Nothing produced
one. A contract with no measurement behind it is the exact shape of every failure
already written down in CLAUDE.md -- a gate with zero checks reports 0/0 PASS.

WHAT "PENETRATION" MEANS HERE, stated so the metric can express the failure:
a vertex of part A that lies INSIDE THE SOLID VOLUME of part B, with the depth
measured as its distance to B's nearest surface, in HIS OWN MILLIMETRES
(1 mm = MW/50, MW = 0.1930 = his measured inter-commissure width).

That definition is what makes the oral case correct rather than merely plausible.
His mouth cavity is CARVED OUT of MARS_MESH by a boolean, so the cavity volume is
outside the solid: a tongue sitting in the cavity reads 0 mm and a tongue pushed
through the cheek wall reads its real depth in the meat of the cheek. A naive
"is the tongue inside the head's outer shell" test would have flagged every
correct frame and passed nothing -- a metric that cannot tell the two apart is
not evidence, it is the blink-occlusion mistake again.

THE SOLVER IS NOT MINE. libigl's generalized winding number (signed_distance with
SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER) is robust on the open, self-intersecting,
non-watertight surfaces a character actually has -- which a ray-parity inside test
is not. FCL (via trimesh) does the broad phase. OWNER LAW #3.

    ./.trippedd_venv/bin/python tools/character/penetration_measure.py geom.npz \
        --pair "MARS_TONGUE->MARS_MESH:BLOCK" \
        --pair "HAIR_SIM->MARS_MESH:BLOCK" \
        --tol-mm 0.5 --out docs/evidence/collision
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from face_plate import MW, MM
except Exception:
    MW = 0.1930
    MM = MW / 50.0

import igl
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCHEMA = "trippedd.contact-measurement/v1"
MODES = {"BLOCK", "ALLOW", "STYLE_OVERRIDE"}


def die(msg: str) -> "None":
    print("\n*** REFUSED: %s\n" % msg, file=sys.stderr, flush=True)
    raise SystemExit(3)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def signed_distance(P: np.ndarray, V: np.ndarray, F: np.ndarray) -> np.ndarray:
    """igl signed distance: NEGATIVE inside the solid. Verified against a unit
    sphere (centre -0.998, r=0.5 -> -0.498, r=3.0 -> +1.993)."""
    return np.asarray(igl.signed_distance(
        np.ascontiguousarray(P, dtype=np.float64),
        np.ascontiguousarray(V, dtype=np.float64),
        np.ascontiguousarray(F, dtype=np.int32),
        igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER,
    )[0], dtype=np.float64)


def surface_side_depth(P, V, F):
    """How far a point sits BEHIND an OPEN surface, along that surface's own normal.

    For a region like his face there is no enclosed solid to be inside of -- the
    skin sub-surface is open at the hairline, and the whole cranium is hair. A
    winding number there is not well posed. The pseudonormal signed distance is:
    it takes the sign from the normal at the CLOSEST POINT, which answers exactly
    the question being asked -- is this hair vertex on the far side of his cheek.

    Points whose closest feature is the open boundary are excluded, because that
    is the one place a pseudonormal sign can flip for reasons that are not a
    penetration. Excluding them is recorded, not silent: they are counted and
    reported as `boundaryExcluded` in the receipt.
    """
    S, _, C, _ = igl.signed_distance(
        np.ascontiguousarray(P, dtype=np.float64),
        np.ascontiguousarray(V, dtype=np.float64),
        np.ascontiguousarray(F, dtype=np.int32),
        igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL,
    )
    return np.maximum(0.0, -np.asarray(S, dtype=np.float64)), np.asarray(C)


def solid_depth_on_subset(P, V, F, subset_mask):
    """Penetration into a CLOSED solid, counted only where the nearest surface
    feature belongs to a named subset of its triangles.

    This is what "is the hair through his FACE" actually asks, and it needs no
    hole filling, no pseudonormal, and no repair of a non-manifold mesh.

    Measured, the two wrong ways first:
      * B = the whole closed head solid. His mesh is 75% hair cap by vertex count,
        so a lock swinging through where the STATIC cap used to be scored 59.24 mm
        with 141,211 violating samples on a sim that had a working collider.
      * B = the face sub-surface, sign from the pseudonormal. That surface is open
        (348 boundary edges: eyes, nostrils, mouth aperture, hairline). Hair hanging
        down his BACK has its nearest feature on that boundary and the normal there
        points forward, so it read 145.38 mm "behind his face" -- and collision ON
        scored WORSE than collision OFF, which is the giveaway that the number was
        about the metric and not the hair.

    The closed surface is well posed, so "inside" is exact. igl returns the index
    of the CLOSEST FACE with the distance, so classifying the contact costs nothing:
    nearest feature in the skin subset -> a real face penetration; nearest feature
    on the hair cap -> hair against hair, reported separately and never as a face
    contact.
    """
    S, I, _, _ = igl.signed_distance(
        np.ascontiguousarray(P, dtype=np.float64),
        np.ascontiguousarray(V, dtype=np.float64),
        np.ascontiguousarray(F, dtype=np.int32),
        igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER,
    )
    S = np.asarray(S, dtype=np.float64)
    I = np.asarray(I, dtype=np.int64)
    inside = S < 0.0
    on_subset = subset_mask[np.clip(I, 0, len(subset_mask) - 1)]
    depth = np.where(inside & on_subset, -S, 0.0)
    other = int((inside & ~on_subset).sum())
    return np.maximum(0.0, depth), other


def subset_face_mask(F_all, F_sub):
    """Which triangles of the full mesh are in the subset. Matched on SORTED vertex
    index triples, so a winding difference between the two extractions cannot cause
    a silent miss -- and the match is asserted, not assumed."""
    key_all = {tuple(sorted(map(int, f))): i for i, f in enumerate(F_all)}
    mask = np.zeros(len(F_all), dtype=bool)
    hit = 0
    for f in F_sub:
        k = tuple(sorted(map(int, f)))
        if k in key_all:
            mask[key_all[k]] = True
            hit += 1
    if hit < 0.95 * len(F_sub):
        die("the subset shares only %d of its %d triangles with the full surface "
            "(%.1f%%). They are not the same vertex indexing, so the contact "
            "classification would be measuring two different meshes."
            % (hit, len(F_sub), 100.0 * hit / max(1, len(F_sub))))
    return mask


def signed_depth(P, V, F, carve=None):
    """Penetration depth in WORLD units of every point of P into solid (V,F),
    optionally with one or more solids CARVED OUT of it first.

    THE CARVE IS NOT A REFINEMENT, IT IS THE WHOLE MEASUREMENT FOR THE ORAL CASE.
    Measured on his real rig: MARS_MESH evaluates to a CLOSED shell (0 boundary
    edges) whose only boolean is the mouth APERTURE -- there is no cavity
    subtracted from it. So a tongue resting correctly in its pocket read 9.73 mm
    "inside the head" and all 146 of its vertices came back violating, while a
    tongue genuinely pushed out through the cheek would have read about the same.
    A metric that gives the same answer for the correct pose and the broken one
    is not evidence, which is the same lesson as occlusion counting a lid peeling
    an eye open as 84% closed.

    MARS_CAVITY is the air pocket -- measured, 146/146 tongue vertices inside it,
    16.44 mm deep. Carving it out leaves the actual MEAT of his head, and that is
    the only volume the tongue is forbidden to enter.

    The difference is taken with WINDING NUMBERS, not a mesh boolean: a point is
    in B \ C exactly when it is inside B and outside every C. That is exact, it
    needs no remesh per frame, and it cannot fail the way a boolean on a 47k
    triangle mesh with 12 non-manifold edges can.
    """
    sb = signed_distance(P, V, F)
    inside = sb < 0.0
    depth = np.maximum(0.0, -sb)
    for (cv, cf) in (carve or []):
        sc = signed_distance(P, cv, cf)
        inside &= (sc >= 0.0)          # carved away -> not in the solid at all
        # inside the meat, the nearest way OUT may be through the carved surface
        depth = np.minimum(depth, np.maximum(0.0, sc))
    return np.where(inside, depth, 0.0)


def part_components(V: np.ndarray, F: np.ndarray):
    m = trimesh.Trimesh(vertices=V, faces=F, process=False)
    groups = trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(len(F)))
    return [F[np.asarray(g, dtype=np.int64)] for g in groups]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("geometry", help=".npz written by export_contact_geometry.py")
    ap.add_argument("--pair", action="append", default=[],
                    help='"A->B:MODE" where MODE is BLOCK|ALLOW|STYLE_OVERRIDE')
    ap.add_argument("--tol-mm", type=float, default=0.5,
                    help="contact tolerance in HIS millimetres (default 0.5)")
    ap.add_argument("--carve", action="append", default=[],
                    help='"B=C[,C2]" subtract solids C from B before measuring, '
                         'e.g. "MARS_MESH=MARS_CAVITY" so the tongue is only '
                         'forbidden from the MEAT of his head, not from its own pocket')
    ap.add_argument("--face-subset", action="append", default=[],
                    help='"B=SUBSET" count a penetration only where the nearest '
                         'surface feature of the closed solid B is a triangle of '
                         'SUBSET (which must share B\'s vertex indexing)')
    ap.add_argument("--surface-side", action="append", default=[],
                    help="part B to treat as an OPEN surface: depth is how far A sits "
                         "behind B along B's own normal, not how far inside a solid. "
                         "Use for a region (his face) that has no enclosed volume.")
    ap.add_argument("--self", action="append", default=[],
                    help="part to also measure against ITSELF, lock vs lock")
    ap.add_argument("--out", default="docs/evidence/collision")
    ap.add_argument("--label", default="contact")
    ap.add_argument("--override-reason", default="")
    args = ap.parse_args()

    if not args.pair:
        die("no --pair given. A run that asserts nothing must never print a clean "
            "sheet: a gate with zero checks reports 0/0 PASS.")

    z = np.load(args.geometry, allow_pickle=False)
    parts = [str(p) for p in z["__parts__"]]
    specs = [str(p) for p in z["__specs__"]]
    frames = z["__frames__"]
    src_hash = sha256(args.geometry)
    os.makedirs(args.out, exist_ok=True)

    def key(spec: str) -> str:
        k = spec.replace(":", "__")
        if k not in parts:
            die("part '%s' is not in %s. It carries: %s" % (spec, args.geometry, specs))
        return k

    carve_map = {}
    for c in args.carve:
        if "=" not in c:
            die('--carve wants "B=C[,C2]", got %r' % c)
        b, _, cs = c.partition("=")
        carve_map[b.strip()] = [x.strip() for x in cs.split(",") if x.strip()]

    subset_map = {}
    for c in args.face_subset:
        if "=" not in c:
            die('--face-subset wants "B=SUBSET", got %r' % c)
        b, _, sub = c.partition("=")
        subset_map[b.strip()] = sub.strip()

    receipts, summary = [], []
    for spec in args.pair:
        body, _, mode = spec.partition(":")
        mode = mode or "BLOCK"
        if mode not in MODES:
            die("pair '%s': mode must be one of %s" % (spec, sorted(MODES)))
        if "->" not in body:
            die("pair '%s': expected A->B" % spec)
        a_spec, b_spec = (s.strip() for s in body.split("->", 1))
        ka, kb = key(a_spec), key(b_spec)

        A = z["%s/verts" % ka]                      # (frames, na, 3)
        Bv = z["%s/verts" % kb]
        Bf = z["%s/tris" % kb]
        if len(Bf) == 0:
            die("pair '%s': part '%s' has no triangles, so it has no volume to be "
                "inside of. Measuring against it would report 0 mm for everything, "
                "which is ATTEMPTED_AND_EMPTY dressed up as a PASS." % (spec, b_spec))

        sub_mask = None
        sub_name = subset_map.get(b_spec)
        if sub_name:
            sub_mask = subset_face_mask(Bf, z["%s/tris" % key(sub_name)])
            print("  %s: %d of %d triangles of %s are in the %s subset"
                  % (spec, int(sub_mask.sum()), len(Bf), b_spec, sub_name), flush=True)
        off_subset_total = 0
        carved = carve_map.get(b_spec, [])
        for c in carved:
            key(c)
        per_frame_max, per_frame_n, all_depth = [], [], []
        worst = {"mm": -1.0, "frame": None, "idx": None, "depth": None}
        for fi in range(len(frames)):
            if sub_mask is not None:
                d, other = solid_depth_on_subset(A[fi], Bv[fi], Bf, sub_mask)
                d = d / MM
                off_subset_total += other
            elif b_spec in args.surface_side:
                d, _cp = surface_side_depth(A[fi], Bv[fi], Bf)
                d = d / MM
            else:
                cg = [(z["%s/verts" % key(c)][fi], z["%s/tris" % key(c)]) for c in carved]
                d = signed_depth(A[fi], Bv[fi], Bf, cg) / MM   # -> his millimetres
            all_depth.append(d)
            viol = d > args.tol_mm
            per_frame_max.append(float(d.max()) if d.size else 0.0)
            per_frame_n.append(int(viol.sum()))
            if per_frame_max[-1] > worst["mm"]:
                worst = {"mm": per_frame_max[-1], "frame": int(frames[fi]),
                         "idx": np.nonzero(viol)[0], "depth": d}
        D = np.concatenate(all_depth) if all_depth else np.zeros(1)
        stats = {"p50": float(np.percentile(D, 50)), "p90": float(np.percentile(D, 90)),
                 "p99": float(np.percentile(D, 99)), "max": float(D.max())}
        violating = int(sum(per_frame_n))

        # ---- self collision, measured or honestly NOT_ATTEMPTED -----------------
        self_state = "NOT_ATTEMPTED"
        self_mm = None
        if a_spec in args.self:
            locks = part_components(A[0], z["%s/tris" % ka])
            if len(locks) < 2:
                self_state = "NOT_ATTEMPTED"
                self_mm = None
            else:
                worst_self = 0.0
                for fi in range(len(frames)):
                    for li, lf in enumerate(locks):
                        others = [o for oi, o in enumerate(locks) if oi != li]
                        if not others:
                            continue
                        OF = np.vstack(others)
                        idx = np.unique(lf.ravel())
                        d = signed_depth(A[fi][idx], A[fi], OF) / MM
                        worst_self = max(worst_self, float(d.max()) if d.size else 0.0)
                self_mm = worst_self
                self_state = "PASS" if worst_self <= args.tol_mm else "FAIL"

        # ---- ACTUAL PIXELS: the curve and the contact map ----------------------
        png = os.path.join(args.out, "%s_%s.png" % (args.label,
                           ("%s__%s" % (a_spec, b_spec)).replace(":", "-").replace("/", "-")))
        fig, ax = plt.subplots(1, 2, figsize=(11, 4), dpi=120)
        ax[0].plot(frames, per_frame_max, color="#b8860b", lw=1.8, label="deepest penetration")
        ax[0].axhline(args.tol_mm, color="#c0392b", ls="--", lw=1.2,
                      label="tolerance %.2f mm" % args.tol_mm)
        ax[0].set_xlabel("frame"); ax[0].set_ylabel("mm (his own)")
        ax[0].set_title("%s -> %s" % (a_spec, b_spec), fontsize=10)
        ax[0].legend(fontsize=8); ax[0].grid(alpha=.25)
        Wf = worst["frame"]; wi = list(frames).index(Wf)
        P = A[wi]
        dep = worst["depth"]
        sc = ax[1].scatter(P[:, 0] / MM, P[:, 2] / MM, c=dep, s=6,
                           cmap="inferno", vmin=0, vmax=max(args.tol_mm, stats["max"]) or 1)
        ax[1].set_aspect("equal"); ax[1].set_title("worst frame %d  (%.3f mm)" % (Wf, worst["mm"]),
                                                   fontsize=10)
        ax[1].set_xlabel("x (mm)"); ax[1].set_ylabel("z (mm)")
        fig.colorbar(sc, ax=ax[1], label="penetration mm")
        fig.tight_layout(); fig.savefig(png); plt.close(fig)

        pair_label = "%s->%s" % (a_spec, b_spec)
        if carved:
            pair_label += " (minus %s)" % ",".join(carved)
        rec = {
            "schema": SCHEMA,
            "pair": pair_label,
            "mode": mode,
            "penetrationMM": stats,
            "violatingSamples": violating,
            "toleranceMM": args.tol_mm,
            "selfCollision": self_state,
            "visualEvidence": os.path.relpath(png),
            "sourceHash": src_hash,
            "proxyHash": hashlib.sha256(
                (a_spec + "|" + b_spec + "|" + str(len(frames))).encode()).hexdigest(),
            "measurement": {
                "tool": "libigl generalized winding number (FAST_WINDING_NUMBER) "
                        "+ trimesh/FCL, on evaluated Blender geometry",
                "definition": "a vertex of A inside the SOLID volume of B; depth = "
                              "distance to B's nearest surface",
                "carvedFrom_B": carved,
                "mode_B": ("SOLID restricted to the %s subset (winding number + "
                           "closest-face classification)" % sub_name) if sub_mask is not None
                          else ("OPEN_SURFACE (pseudonormal side test)"
                                if b_spec in args.surface_side else "SOLID (winding number)"),
                "insideButNearestFeatureOffSubset": off_subset_total,
                "mmPerUnit": MM, "MW": MW,
                "frames": [int(frames[0]), int(frames[-1])],
                "samplesPerFrame": int(A.shape[1]),
                "totalSamples": int(A.shape[1] * len(frames)),
                "worstFrame": Wf,
                "perFrameMaxMM": [round(v, 5) for v in per_frame_max],
                "perFrameViolatingVerts": per_frame_n,
                "selfCollisionWorstMM": self_mm,
                "geometry": os.path.relpath(args.geometry),
            },
        }
        if mode == "STYLE_OVERRIDE":
            if not args.override_reason.strip():
                die("pair '%s' is STYLE_OVERRIDE but no --override-reason was given. "
                    "The owner asked for glitchy/exaggerated to be something we ASK "
                    "for, which means it has to be written down when it is taken.")
            rec["overrideReason"] = args.override_reason
        rp = os.path.join(args.out, "%s_%s.receipt.json" % (args.label,
                          ("%s__%s" % (a_spec, b_spec)).replace(":", "-").replace("/", "-")))
        with open(rp, "w") as fh:
            json.dump(rec, fh, indent=2, sort_keys=True)
            fh.write("\n")
        receipts.append(rp)
        summary.append((rec["pair"], mode, stats["max"], violating, self_state, rp))
        print("%-34s %-15s max %8.4f mm   violating %6d / %d   self %s"
              % (rec["pair"], mode, stats["max"], violating,
                 rec["measurement"]["totalSamples"], self_state), flush=True)

    print("\nreceipts written:")
    for _, _, _, _, _, rp in summary:
        print("  %s" % rp)
    print("\njudge them with:")
    for _, _, _, _, _, rp in summary:
        print("  ./.trippedd_venv/bin/python tools/character/contact_gate.py %s" % rp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
