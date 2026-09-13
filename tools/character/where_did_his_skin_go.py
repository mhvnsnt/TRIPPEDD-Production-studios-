"""
UNCARVED SCAN vs SHIPPED HEAD, SAME RAY, SAME INSTRUMENT, SIDE BY SIDE.

    banked: "His scan is perfect ... the BOOLEAN DIFFERENCE in oral_cavity.py is
    what removes his corner skin."

That conclusion came from a metric that counts cells where the nearest surface is
CAVITY -- and an UNCARVED scan has no cavity, so it scores 0 of 65 no matter what
its skin is doing. **A control that cannot fail is not a control.** So ask the
question with one instrument that works on both heads: fire the same ray at the
same (x, z) into each, and print the depth of the first surface it meets.

  no skin on the shipped head where the scan has skin  -> the carve removed it
  both heads agree                                     -> the carve is innocent
                                                          and the crater is
                                                          elsewhere or imaginary

The uncarved scan is loaded from the glTF and converted Y-up -> Z-up, because
every measured number in this repo is in the space Blender's importer produced.
The shipped head is the LIVE session's evaluated MARS_MESH.

    ./.trippedd_venv/bin/python tools/character/where_did_his_skin_go.py
"""
import argparse, json, os, sys
import numpy as np
import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def load_scan(lod):
    s = trimesh.load(os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % lod),
                     process=False)
    m = (trimesh.util.concatenate(tuple(s.geometry.values()))
         if isinstance(s, trimesh.Scene) else s)
    m.merge_vertices()
    V = np.asarray(m.vertices, dtype=np.float64)
    m.vertices = np.column_stack([V[:, 0], -V[:, 2], V[:, 1]])   # glTF Y-up -> Blender Z-up
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lod", default="LOD2")
    ap.add_argument("--shipped", default="renders/_session/MARS_MESH_rest.npz")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
    MW = anat["aperture"]["width"]
    MM = MW / 50.0
    F = np.array(anat["frame"]["matrix"], dtype=float)

    scan = load_scan(a.lod)
    d = np.load(os.path.join(ROOT, a.shipped))
    ship = trimesh.Trimesh(vertices=d["V"], faces=d["F"], process=False)
    print("uncarved scan %s : %d verts  %d faces" % (a.lod, len(scan.vertices), len(scan.faces)))
    print("shipped head       : %d verts  %d faces" % (len(ship.vertices), len(ship.faces)))

    # CONTROL: his own measured commissures must lie on BOTH surfaces, or the two
    # meshes are not in the same space and nothing below means anything.
    import igl
    corners = np.array([anat["aperture"]["cornerLeft"], anat["aperture"]["cornerRight"]])
    for name, m in (("uncarved", scan), ("shipped", ship)):
        sd, _, _, _ = igl.signed_distance(corners,
                                          np.asarray(m.vertices, dtype=np.float64),
                                          np.asarray(m.faces, dtype=np.int64),
                                          igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
        mm = np.abs(sd) / MM
        print("  CONTROL  %-9s commissures %.2f mm / %.2f mm from its surface"
              % (name, mm[0], mm[1]))
        if mm.max() > 6.0:
            print("  *** REFUSED: %s is not in the measured frame's space." % name)
            return 3

    # the ray: start well in FRONT of his face and travel along the frame's +y
    START = -60.0 * MM
    fwd = F[:3, 1] / np.linalg.norm(F[:3, 1])
    xs = np.arange(-34.0, 34.1, 1.0)
    zs = np.arange(-6.0, 6.1, 2.0)
    origins, keys = [], []
    for x in xs:
        for z in zs:
            origins.append((F @ np.array([x * MM, START, z * MM, 1.0]))[:3])
            keys.append((x, z))
    origins = np.array(origins)
    dirs = np.tile(fwd, (len(origins), 1))

    def first_hit(m):
        loc, ray_i, _ = m.ray.intersects_location(origins, dirs, multiple_hits=False)
        out = np.full(len(origins), np.nan)
        if len(ray_i):
            dep = (loc - origins[ray_i]) @ fwd
            for i, r in enumerate(ray_i):
                if np.isnan(out[r]) or dep[i] < out[r]:
                    out[r] = dep[i]
        return out / MM + (START / MM)     # express as local y, his millimetres

    hs, hp = first_hit(scan), first_hit(ship)

    # ── PER CELL FIRST. Reducing a column to its shallowest hit HIDES A SLIT:
    # if one z has a hole and the z beside it has skin, min() reports the skin
    # and the column reads "agree". The cell table is the honest one; the column
    # table below it is only a readable summary.
    cells_gone = [(keys[i], hs[i], hp[i]) for i in range(len(keys))
                  if not np.isnan(hs[i]) and (np.isnan(hp[i]) or hp[i] - hs[i] > 8.0)]
    print("\n  PER CELL (%d cells): shipped head has lost his skin in %d"
          % (len(keys), len(cells_gone)))
    if cells_gone:
        print("    x mm   z mm    uncarved      shipped")
        for (x, z), u, q in cells_gone[:40]:
            print("    %+5.0f  %+5.0f   %+8.2f   %s"
                  % (x, z, u, ("%+8.2f" % q) if not np.isnan(q) else "  nothing"))
        byx = {}
        for (x, z), u, q in cells_gone:
            byx[x] = byx.get(x, 0) + 1
        print("    lost cells by x: %s" % sorted(byx.items()))

    print("\n  first surface a ray meets, in local y mm (nan = nothing at all)")
    print("  x mm    uncarved scan        shipped head        verdict")
    print("  " + "-" * 68)
    rows, gone, agree = [], 0, 0
    for x in xs:
        idx = [i for i, k in enumerate(keys) if k[0] == x]
        su = np.nanmin(hs[idx]) if not np.all(np.isnan(hs[idx])) else np.nan
        sp = np.nanmin(hp[idx]) if not np.all(np.isnan(hp[idx])) else np.nan
        if np.isnan(su):
            v = "no scan surface either"
        elif np.isnan(sp):
            v = "SKIN GONE (nothing at all)"; gone += 1
        elif sp - su > 8.0:
            v = "SKIN GONE (+%.0f mm deeper)" % (sp - su); gone += 1
        else:
            v = "agree"; agree += 1
        if abs(x) % 3 < 1e-9 or "GONE" in v:
            print("  %+6.0f   %s   %s   %s"
                  % (x,
                     ("%+8.2f" % su) if not np.isnan(su) else "     --- ",
                     ("%+8.2f" % sp) if not np.isnan(sp) else "     --- ",
                     v))
        rows.append({"x": float(x), "uncarved": None if np.isnan(su) else round(float(su), 2),
                     "shipped": None if np.isnan(sp) else round(float(sp), 2), "verdict": v})

    print("\n  cells   where the shipped head has lost his skin : %d of %d"
          % (len(cells_gone), len(keys)))
    print("  columns where the shipped head has lost his skin : %d" % gone)
    print("  columns where the two heads agree                : %d" % agree)
    if gone == 0:
        print("\n  THE CARVE DID NOT REMOVE HIS EXTERIOR SKIN. Every column that has skin")
        print("  on the scan still has skin on the shipped head, at the same depth.")
    if a.json:
        json.dump({"schema": "trippedd.skin-ab/v1", "lod": a.lod,
                   "cellsTotal": len(keys), "cellsSkinGone": len(cells_gone),
                   "columnsSkinGone": gone, "columnsAgree": agree, "columns": rows},
                  open(os.path.join(ROOT, a.json), "w"), indent=2)
        print("  wrote %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
