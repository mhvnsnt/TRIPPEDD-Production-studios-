#!/usr/bin/env python3
"""Render parsed TVG drawings (tvgdump JSON) to SVG + PNG.

Semantics ported from the MIT-licensed web viewer in
github.com/c-probably-archived20260718/tvg (canvas.js / layer-data.js),
plus production-format rules reverse-engineered from the Rick and Morty
files (see ../progress-2026-10-30-evening.md):
- layers underlay -> colour -> line -> overlay
- a component without its own path reuses the path of the component its
  `group_ref` points at (layer-wide component index, chains allowed)
- a fill shape's components are contour SEGMENTS: they are chained by
  matching endpoints into closed loops, which are filled (even-odd)
- fill colors: TGSD color id, else a palette id found by scanning the
  raw TGSD bytes (the TGCO block), else inherited from the previous
  fill component in the shape/layer
- pencil components become outlines extruded from their thickness
  profile, sampled by arclength along the centerline within the
  profile domain. Y axis flipped (Harmony y-up -> SVG y-down).

Usage: render.py <dump.jsonl> <outdir> [--only SUBSTR] [--width PX]
"""
import json, math, os, subprocess, sys

TVGRENDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "tvgrender", "target", "release", "tvgrender")
EPS = 0.02

def cubic(p0, p1, p2, p3, n=24):
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        x = u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0]
        y = u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]
        out.append((x, y))
    return out

def quad(p0, p1, p2, n=16):
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
        y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
        out.append((x, y))
    return out

def seg_edges(segments):
    """Component path -> (start_point, edges). Edge: (kind, pts...) with
    absolute endpoints: L:(a,b) C:(a,c1,c2,b) Q:(a,c,b). Raw coords."""
    edges = []
    cur = (0.0, 0.0)
    start = None
    for seg in segments:
        ty = seg["type"]; c = seg["content"]
        if ty == "line":
            p = (c[0], c[1])
            if start is None:
                start = p; cur = p
            else:
                edges.append(("L", cur, p)); cur = p
        elif ty == "cubic":
            p1 = tuple(c[0]); p2 = tuple(c[1]); p3 = tuple(c[2])
            if start is None: start = cur
            edges.append(("C", cur, p1, p2, p3)); cur = p3
        elif ty == "quadratic":
            p1 = tuple(c[0]); p2 = tuple(c[1])
            if start is None: start = cur
            edges.append(("Q", cur, p1, p2)); cur = p2
    if start is None:
        start = cur
    return start, edges

def rev_edge(e):
    if e[0] == "L": return ("L", e[2], e[1])
    if e[0] == "C": return ("C", e[4], e[3], e[2], e[1])
    return ("Q", e[3], e[2], e[1])

def chain_endpoints(start, edges):
    if edges:
        return start, edges[-1][-1]
    return start, start

def chain_segments(comp_paths):
    """Join component (start, edges) pieces into chains by endpoints.
    Returns list of (start, edges, closed)."""
    pool = list(comp_paths)
    chains = []
    while pool:
        start, edges = pool.pop(0)
        edges = list(edges)
        cs, ce = chain_endpoints(start, edges)
        grew = True
        while grew:
            grew = False
            for i, (s2, e2) in enumerate(pool):
                if not e2: continue
                s2s, s2e = chain_endpoints(s2, e2)
                if abs(s2s[0]-ce[0]) < EPS and abs(s2s[1]-ce[1]) < EPS:
                    edges.extend(e2); ce = s2e
                elif abs(s2e[0]-ce[0]) < EPS and abs(s2e[1]-ce[1]) < EPS:
                    edges.extend([rev_edge(e) for e in reversed(e2)]); ce = s2s
                elif abs(s2e[0]-cs[0]) < EPS and abs(s2e[1]-cs[1]) < EPS:
                    edges = list(e2) + edges; cs = s2s
                elif abs(s2s[0]-cs[0]) < EPS and abs(s2s[1]-cs[1]) < EPS:
                    edges = [rev_edge(e) for e in reversed(e2)] + edges; cs = s2e
                else:
                    continue
                pool.pop(i); grew = True
                break
        closed = abs(ce[0]-cs[0]) < EPS and abs(ce[1]-cs[1]) < EPS
        chains.append((cs, edges, closed))
    return chains

def edges_to_d(start, edges, close=False):
    def F(p): return f"{p[0]:.2f},{-p[1]:.2f}"
    d = [f"M{F(start)}"]
    for e in edges:
        if e[0] == "L": d.append(f"L{F(e[2])}")
        elif e[0] == "C": d.append(f"C{F(e[2])} {F(e[3])} {F(e[4])}")
        else: d.append(f"Q{F(e[2])} {F(e[3])}")
    if close: d.append("Z")
    return " ".join(d)

def edges_to_pts(start, edges):
    pts = [(start[0], -start[1])]
    cur = start
    for e in edges:
        if e[0] == "L":
            pts.append((e[2][0], -e[2][1])); cur = e[2]
        elif e[0] == "C":
            seg = cubic(cur, e[2], e[3], e[4])
            pts.extend((x, -y) for x, y in seg); cur = e[4]
        else:
            seg = quad(cur, e[2], e[3])
            pts.extend((x, -y) for x, y in seg); cur = e[3]
    return pts

def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return u*u*u*p0 + 3*u*u*t*p1 + 3*u*t*t*p2 + t*t*t*p3

def profile_offset(definition, side, loc):
    """Offset of one side of a thickness profile at profile-location loc.
    The profile is a chain of cubics in (loc, offset) space; x(t)=loc is
    solved by bisection (control x lies within the segment span)."""
    if len(definition) == 1:
        return definition[0][side]["offset"]
    for i in range(len(definition) - 1):
        a = definition[i]; b = definition[i + 1]
        if loc < a["loc"] - 1e-9 or loc > b["loc"] + 1e-9:
            continue
        sa = a[side]; sb = b[side]
        span = b["loc"] - a["loc"]
        x0 = a["loc"]; x3 = b["loc"]
        x1 = a["loc"] + sa["ctrl_fwd"][0] * span
        x2 = b["loc"] - sb["ctrl_back"][0] * span
        y0 = sa["offset"]; y3 = sb["offset"]
        y1 = sa["ctrl_fwd"][1]; y2 = sb["ctrl_back"][1]
        lo_t, hi_t = 0.0, 1.0
        for _ in range(40):
            mid = (lo_t + hi_t) / 2
            if _bez(x0, x1, x2, x3, mid) < loc: lo_t = mid
            else: hi_t = mid
        return _bez(y0, y1, y2, y3, (lo_t + hi_t) / 2)
    # outside the profile's loc range: clamp to the nearest end
    if loc <= definition[0]["loc"]:
        return definition[0][side]["offset"]
    return definition[-1][side]["offset"]

def center_at(pts, cum, s):
    total = cum[-1]
    target = s * total
    lo, hi = 0, len(cum) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] < target: lo = mid + 1
        else: hi = mid
    i = max(1, lo)
    seg_len = cum[i] - cum[i - 1] or 1.0
    t = (target - cum[i - 1]) / seg_len
    x = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t
    y = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t
    dx = (pts[i][0] - pts[i - 1][0]) / seg_len
    dy = (pts[i][1] - pts[i - 1][1]) / seg_len
    return (x, y), (dx, dy)

def extrude(pts, thickness, active_def):
    """Pencil outline polygon: sample the centerline by arclength; at
    each sample the profile is evaluated at loc = d0 + s*(d1-d0) so
    narrow domain windows still produce full-width strokes."""
    definition = thickness.get("definition") or active_def
    if not definition or len(pts) < 2:
        return None
    d0, d1 = thickness["domain"]
    if d1 <= d0: d0, d1 = 0.0, 1.0
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1]))
    if cum[-1] == 0: return None
    n = 32
    lpts = []; rpts = []
    for i in range(n + 1):
        s = i / n
        loc = d0 + s * (d1 - d0)
        (cx, cy), (tx, ty) = center_at(pts, cum, s)
        lo_ = profile_offset(definition, "left", loc)
        ro_ = profile_offset(definition, "right", loc)
        lpts.append((cx + ty * lo_, cy - tx * lo_))
        rpts.append((cx - ty * ro_, cy + tx * ro_))
    (ex, ey), (etx, ety) = center_at(pts, cum, 1.0)
    end_off = (abs(profile_offset(definition, "left", d1))
               + abs(profile_offset(definition, "right", d1))) / 2.0
    cap_end = (ex + etx * end_off * 1.05, ey + ety * end_off * 1.05)
    (sx, sy), (stx, sty) = center_at(pts, cum, 0.0)
    start_off = (abs(profile_offset(definition, "left", d0))
                 + abs(profile_offset(definition, "right", d0))) / 2.0
    cap_start = (sx - stx * start_off * 1.05, sy - sty * start_off * 1.05)
    return lpts + [cap_end] + rpts[::-1] + [cap_start]


def chain_pieces(pieces):
    """pieces: [(owner, start, edges)] -> [(start, [(owner, edge)], closed)]"""
    pool = [(o, s, list(e)) for o, s, e in pieces]
    out = []
    while pool:
        o0, start, edges = pool.pop(0)
        owned = [(o0, e) for e in edges]
        cs, ce = chain_endpoints(start, edges)
        grew = True
        while grew:
            grew = False
            for i, (o2, s2, e2) in enumerate(pool):
                if not e2: continue
                s2s, s2e = chain_endpoints(s2, e2)
                if abs(s2s[0]-ce[0]) < EPS and abs(s2s[1]-ce[1]) < EPS:
                    owned.extend((o2, e) for e in e2); ce = s2e
                elif abs(s2e[0]-ce[0]) < EPS and abs(s2e[1]-ce[1]) < EPS:
                    owned.extend((o2, rev_edge(e)) for e in reversed(e2)); ce = s2s
                elif abs(s2e[0]-cs[0]) < EPS and abs(s2e[1]-cs[1]) < EPS:
                    owned = [(o2, e) for e in e2] + owned; cs = s2s
                elif abs(s2s[0]-cs[0]) < EPS and abs(s2s[1]-cs[1]) < EPS:
                    owned = [(o2, rev_edge(e)) for e in reversed(e2)] + owned; cs = s2e
                else:
                    continue
                pool.pop(i); grew = True
                break
        closed = abs(ce[0]-cs[0]) < EPS and abs(ce[1]-cs[1]) < EPS
        out.append((cs, owned, closed))
    return out

def trace_loops(edge_list):
    """Trace closed loops from loose edges by smoothest-turn walking.
    edge_list: flat list of edge tuples (absolute endpoints).
    Returns list of (start, edges) loops. Used for zone-painted line
    art whose outline junctions branch into detail strokes, where
    exact endpoint chaining wanders off the contour."""
    import math
    def vkey(p):
        return (round(p[0] * 2) / 2, round(p[1] * 2) / 2)
    adj = {}
    for i, e in enumerate(edge_list):
        adj.setdefault(vkey(e[1]), []).append(i)
        adj.setdefault(vkey(e[-1]), []).append(i)
    def far_dir(e, from_end):
        # direction leaving the vertex at `from_end` (0: at e[1], 1: at e[-1])
        if from_end == 0:
            a, b = e[1], e[2]
        else:
            a, b = e[-1], e[-2]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1.0
        return (dx / n, dy / n)
    used = [False] * len(edge_list)
    loops = []
    for i0, e0 in enumerate(edge_list):
        if used[i0]: continue
        walk = [i0]
        local_used = {i0}
        start_key = vkey(e0[1])
        cur_key = vkey(e0[-1])
        cur = e0
        at_end = 1  # we are at cur's e[-1]
        ok = False
        for _ in range(len(edge_list) + 2):
            if cur_key == start_key and len(walk) >= 3:
                ok = True; break
            # heading = direction we were travelling when we arrived at
            # cur_key = reverse of the direction back along cur's edge.
            back = far_dir(cur, at_end)
            arr = (-back[0], -back[1])
            best, best_dot = None, -2.0
            for j in adj.get(cur_key, []):
                if j in local_used: continue
                ej = edge_list[j]
                for end in (0, 1):
                    vtx = ej[1] if end == 0 else ej[-1]
                    if vkey(vtx) != cur_key: continue
                    dd = far_dir(ej, end)
                    dot = arr[0] * dd[0] + arr[1] * dd[1]
                    if dot > best_dot:
                        best_dot, best = dot, (j, end)
            if best is None: break
            j, end = best
            ej = edge_list[j]
            walk.append(j); local_used.add(j)
            cur = ej
            at_end = 1 - end
            cur_key = vkey(ej[-1] if at_end == 1 else ej[1])
            if cur_key == start_key and len(walk) >= 3:
                ok = True; break
        if ok:
            # orient edges consistently along the walk
            oriented = []
            prev_key = None
            for n, j in enumerate(walk):
                e = edge_list[j]
                if n == 0:
                    oriented.append(e); prev_key = vkey(e[-1]); continue
                if vkey(e[1]) == prev_key:
                    oriented.append(e); prev_key = vkey(e[-1])
                else:
                    oriented.append(rev_edge(e)); prev_key = vkey(e[1])
            loops.append((oriented[0][1], oriented))
            for j in walk: used[j] = True
    return loops

def render_entry(d):
    data = d["data"]
    main = None
    for item in data:
        if item["type"] == "main": main = item["content"]
    tags = main if main is not None else data
    palette = {}
    layers = {}
    for item in tags:
        if item["type"] == "palette":
            for col in item["content"]["colors"]:
                rgba = None; cid = None
                for t in col["tags"]:
                    if t["type"] == "color_rgba": rgba = t["content"]
                    elif t["type"] == "color_id": cid = t["content"]["id"]
                if cid is not None and rgba is not None:
                    palette[cid] = rgba
        elif item["type"].startswith("layer_"):
            layers[item["type"]] = item["content"]
    stats = {"fills": 0, "strokes": 0, "fallback_strokes": 0, "missing_colors": 0,
             "color_direct": 0, "color_tgsd": 0, "color_inherited": 0,
             "refs": 0, "refs_unresolved": 0}
    id_bytes = {cid.to_bytes(8, "little"): rgba for cid, rgba in palette.items()}

    def resolve_color(info, inherit):
        cid = info.get("color_id")
        if cid in palette:
            stats["color_direct"] += 1
            return palette[cid]
        raw = bytes(info.get("tgsd") or [])
        for ib, rgba in id_bytes.items():
            if ib in raw:
                stats["color_tgsd"] += 1
                return rgba
        if inherit is not None:
            stats["color_inherited"] += 1
            return inherit
        stats["missing_colors"] += 1
        return (0, 0, 0, 255)

    body = []
    allpts = []
    entry_has_fill = False
    for lname in ("layer_underlay", "layer_color", "layer_line", "layer_overlay"):
        lay = layers.get(lname)
        if not lay or lay["type"] != "vector": continue
        # Flatten components in layer order, remembering shape membership.
        layer_comps = []   # ctags per comp, layer-wide index
        comp_shape = []    # shape ordinal per comp
        shape_colors = {}  # shape ordinal -> resolved fill rgba (first fill)
        active_def = None
        shape_inherit = None
        # TGCO fill candidates per shape: palette ids embedded in any
        # comp's TGSD (excluding ids used directly as line colors).
        line_ids = set()
        for shape in lay["content"]:
            for comp in shape["components"]:
                for t in comp["tags"]:
                    if t["type"] == "info" and t["content"].get("type") == "pencil":
                        if t["content"].get("color_id") is not None:
                            line_ids.add(t["content"]["color_id"])
        shape_candidates = {}
        for s_ord, shape in enumerate(lay["content"]):
            cands = []
            for comp in shape["components"]:
                for t in comp["tags"]:
                    if t["type"] != "info": continue
                    raw = bytes(t["content"].get("tgsd") or [])
                    for cid in palette:
                        if cid in line_ids: continue
                        if cid.to_bytes(8, "little") in raw and cid not in cands:
                            cands.append(cid)
            shape_candidates[s_ord] = [palette[c] for c in cands]
        for s_ord, shape in enumerate(lay["content"]):
            shape_color = None
            for comp in shape["components"]:
                ctags = {t["type"]: t["content"] for t in comp["tags"]}
                info = ctags.get("info") or {}
                if info.get("type") == "fill":
                    rgba = resolve_color(info, shape_color or shape_inherit
                                         or (shape_candidates[s_ord][0]
                                             if shape_candidates[s_ord] else None))
                    if shape_color is None: shape_color = rgba
                    shape_inherit = rgba
                if "thickness" in ctags and ctags["thickness"].get("definition"):
                    ctags["_def_at_comp"] = ctags["thickness"]["definition"]
                layer_comps.append(ctags)
                comp_shape.append(s_ord)
            if shape_color is not None:
                shape_colors[s_ord] = shape_color

        def comp_segments(ctags, depth=0):
            if "path" in ctags:
                return ctags["path"]["segments"]
            info = ctags.get("info") or {}
            ref = info.get("group_ref")
            if ref is None or depth > 8 or ref >= len(layer_comps):
                return None
            stats["refs"] += 1
            return comp_segments(layer_comps[ref], depth + 1)

        # Resolve every comp's edges once.
        comp_edges = []
        for ctags in layer_comps:
            segs = comp_segments(ctags)
            if segs is None:
                info = ctags.get("info") or {}
                if info.get("group_ref") is not None and info.get("type") in ("pencil", "fill", "stroke"):
                    stats["refs_unresolved"] += 1
                comp_edges.append(None)
            else:
                comp_edges.append(seg_edges(segs))

        # Global active thickness definition in layer order.
        running_def = None
        comp_def = []
        for ctags in layer_comps:
            if "_def_at_comp" in ctags:
                running_def = ctags["_def_at_comp"]
            comp_def.append(running_def)

        # Chain all path pieces (owner comp recorded per edge).
        pieces = []
        for ci, ce in enumerate(comp_edges):
            if ce is not None and ce[1]:
                pieces.append((ci, ce[0], ce[1]))
        chains = chain_pieces(pieces)  # [(start, [(owner, edge)...], closed)]

        layer_body_fill = []
        layer_body_stroke = []
        filled_shapes = set()
        # Fills first: closed chains that contain a fill comp.
        fill_chains = []
        for cs, owned, closed in chains:
            owners = [o for o, _ in owned]
            edges = [e for _, e in owned]
            fill_owners = [o for o in owners
                           if (layer_comps[o].get("info") or {}).get("type") == "fill"]
            if closed and fill_owners:
                pts_tmp = edges_to_pts(cs, edges)
                area = 0.0
                for i in range(len(pts_tmp)):
                    x1, y1 = pts_tmp[i]; x2, y2 = pts_tmp[(i + 1) % len(pts_tmp)]
                    area += x1 * y2 - x2 * y1
                fill_chains.append((abs(area), cs, edges, comp_shape[fill_owners[0]]))
        fill_chains.sort(key=lambda z: -z[0])
        zone_use = {}
        filled_chain_idx = set()
        for _area, cs, edges, s_ord in fill_chains:
            zi = zone_use.get(s_ord, 0)
            zone_use[s_ord] = zi + 1
            cands = shape_candidates.get(s_ord) or []
            if zi < len(cands):
                rgba = cands[zi]
            else:
                rgba = shape_colors.get(s_ord, (0, 0, 0, 255))
            if True:
                color = f"rgb({rgba[0]},{rgba[1]},{rgba[2]})"
                op = f' fill-opacity="{rgba[3]/255:.3f}"' if rgba[3] < 255 else ""
                layer_body_fill.append(
                    f'<path d="{edges_to_d(cs, edges, close=True)}" fill="{color}"{op} fill-rule="evenodd"/>')
                filled_shapes.add(s_ord)
                entry_has_fill = True
                allpts.extend(edges_to_pts(cs, edges))
        # Zone fills: closed chains with NO fill comp whose owner shape
        # carries TGCO paint records (Harmony paints closed line-art
        # zones this way — e.g. a head outline whose TGSD references the
        # skin color). Continue the shape's zone counter so candidate
        # colors are consumed in area order across both passes; chains
        # beyond the candidate list stay transparent (unpainted zones).
        zone_chains = []
        for cs, owned, closed in chains:
            if not closed: continue
            owners = [o for o, _ in owned]
            if any((layer_comps[o].get("info") or {}).get("type") == "fill"
                   for o in owners):
                continue  # handled in the fill-comp pass above
            s_ord = comp_shape[owners[0]]
            if not (shape_candidates.get(s_ord) or []):
                continue  # no paint record -> not a painted zone
            edges = [e for _, e in owned]
            pts_tmp = edges_to_pts(cs, edges)
            area = 0.0
            for i in range(len(pts_tmp)):
                x1, y1 = pts_tmp[i]; x2, y2 = pts_tmp[(i + 1) % len(pts_tmp)]
                area += x1 * y2 - x2 * y1
            zone_chains.append((abs(area), cs, edges, s_ord))
        zone_chains.sort(key=lambda z: -z[0])
        for _area, cs, edges, s_ord in zone_chains:
            zi = zone_use.get(s_ord, 0)
            zone_use[s_ord] = zi + 1
            cands = shape_candidates.get(s_ord) or []
            if zi >= len(cands):
                continue  # unpainted zone
            rgba = cands[zi]
            color = f"rgb({rgba[0]},{rgba[1]},{rgba[2]})"
            op = f' fill-opacity="{rgba[3]/255:.3f}"' if rgba[3] < 255 else ""
            layer_body_fill.append(
                f'<path d="{edges_to_d(cs, edges, close=True)}" fill="{color}"{op} fill-rule="evenodd"/>')
            filled_shapes.add(s_ord)
            entry_has_fill = True
            stats["zone_fills"] = stats.get("zone_fills", 0) + 1
            allpts.extend(edges_to_pts(cs, edges))
        # Traced zone fills: shapes with paint records that still have
        # no fill (their outlines branch at junctions, so exact chaining
        # never closed them). Trace loops by smoothest-turn walking and
        # fill them with the shape's remaining candidates, area order.
        # Conservative gating: only when NO fill has been produced
        # anywhere in this drawing yet (zone-only drawings: heads, hands,
        # hair) and the shape has exactly one candidate left — multi-
        # candidate shapes keep the hollow gap rather than risk painting
        # the wrong zone the wrong color.
        if entry_has_fill:
            traced_candidates = []
        else:
            traced_candidates = list(range(len(lay["content"])))
        for s_ord in traced_candidates:
            if s_ord in filled_shapes: continue
            cands = shape_candidates.get(s_ord) or []
            if len(cands) - zone_use.get(s_ord, 0) != 1: continue
            shape_edges = []
            for ci, ce in enumerate(comp_edges):
                if comp_shape[ci] == s_ord and ce is not None and ce[1]:
                    shape_edges.extend(ce[1])
            if len(shape_edges) < 3: continue
            loops = []
            for ls, le in trace_loops(shape_edges):
                pts_tmp = edges_to_pts(ls, le)
                area = 0.0
                for i in range(len(pts_tmp)):
                    x1, y1 = pts_tmp[i]; x2, y2 = pts_tmp[(i + 1) % len(pts_tmp)]
                    area += x1 * y2 - x2 * y1
                if abs(area) > 25.0:
                    loops.append((abs(area), ls, le))
            loops.sort(key=lambda z: -z[0])
            for _area, ls, le in loops:
                zi = zone_use.get(s_ord, 0)
                zone_use[s_ord] = zi + 1
                if zi >= len(cands): break
                rgba = cands[zi]
                color = f"rgb({rgba[0]},{rgba[1]},{rgba[2]})"
                op = f' fill-opacity="{rgba[3]/255:.3f}"' if rgba[3] < 255 else ""
                layer_body_fill.append(
                    f'<path d="{edges_to_d(ls, le, close=True)}" fill="{color}"{op} fill-rule="evenodd"/>')
                filled_shapes.add(s_ord)
                entry_has_fill = True
                stats["traced_fills"] = stats.get("traced_fills", 0) + 1
                allpts.extend(edges_to_pts(ls, le))
        # Strokes: per component (junctions branch; chaining would
        # scramble the centerline). Caps are extended so neighbouring
        # segments overlap at the joints.
        for ci, ce in enumerate(comp_edges):
            if ce is None or not ce[1]: continue
            info = layer_comps[ci].get("info") or {}
            if info.get("type") not in ("pencil", "stroke"): continue
            rgba = resolve_color(info, None)
            color = f"rgb({rgba[0]},{rgba[1]},{rgba[2]})"
            op = f' fill-opacity="{rgba[3]/255:.3f}"' if rgba[3] < 255 else ""
            start, edges = ce
            pts = edges_to_pts(start, edges)
            thick = layer_comps[ci].get("thickness")
            poly = extrude(pts, thick, comp_def[ci]) if thick else None
            if poly is None and comp_def[ci]:
                poly = extrude(pts, {"definition": None, "domain": (0.0, 1.0)}, comp_def[ci])
            if poly:
                pstr = " ".join(f"{x:.2f},{y:.2f}" for x, y in poly)
                layer_body_stroke.append(f'<polygon points="{pstr}" fill="{color}"{op}/>')
                stats["strokes"] += 1
            else:
                layer_body_stroke.append(
                    f'<path d="{edges_to_d(start, edges)}" fill="none" stroke="{color}" stroke-width="3"/>')
                stats["fallback_strokes"] += 1
            allpts.extend(pts)
        # Fill shapes whose chains never closed: fill their pieces directly.
        for s_ord, shape in enumerate(lay["content"]):
            if s_ord in filled_shapes or s_ord not in shape_colors: continue
            pieces_s = []
            for ci, ce in enumerate(comp_edges):
                if comp_shape[ci] == s_ord and ce is not None and ce[1]:
                    if (layer_comps[ci].get("info") or {}).get("type") == "fill":
                        pieces_s.append(ce)
            if not pieces_s: continue
            rgba = shape_colors[s_ord]
            color = f"rgb({rgba[0]},{rgba[1]},{rgba[2]})"
            op = f' fill-opacity="{rgba[3]/255:.3f}"' if rgba[3] < 255 else ""
            ds = []
            for cs, edges, closed in chain_segments(pieces_s):
                ds.append(edges_to_d(cs, edges, close=True))
                allpts.extend(edges_to_pts(cs, edges))
            layer_body_fill.append(f'<path d="{" ".join(ds)}" fill="{color}"{op} fill-rule="evenodd"/>')
        stats["fills"] += len(layer_body_fill)
        body.extend(layer_body_fill)
        body.extend(layer_body_stroke)
    if not allpts:
        return None, stats
    xs = [p[0] for p in allpts]; ys = [p[1] for p in allpts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    pad = max(10.0, 0.04 * max(x1 - x0, y1 - y0))
    vb = f"{x0-pad:.1f} {y0-pad:.1f} {x1-x0+2*pad:.1f} {y1-y0+2*pad:.1f}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
           f'width="{x1-x0+2*pad:.0f}" height="{y1-y0+2*pad:.0f}">'
           + "".join(body) + "</svg>")
    return svg, stats

def main():
    src, outdir = sys.argv[1], sys.argv[2]
    only = None; width = "768"
    args = sys.argv[3:]
    for i, a in enumerate(args):
        if a == "--only": only = args[i + 1]
        if a == "--width": width = args[i + 1]
    os.makedirs(outdir, exist_ok=True)
    summary = {"rendered": 0, "empty": 0, "errors": 0, "files": []}
    for line in open(src):
        try: d = json.loads(line)
        except Exception: continue
        if not d.get("ok"): continue
        rel = d["file"]
        if only and only not in rel: continue
        name = os.path.splitext(os.path.basename(rel))[0]
        if "/elements/" in rel:
            tpl = rel.split("/elements/")[0].split("/")[-1].replace(".tpl", "")
            elem = rel.split("/elements/")[1].split("/")[0]
            sub = os.path.join(outdir, tpl, elem)
        else:
            sub = os.path.join(outdir, "misc")
        os.makedirs(sub, exist_ok=True)
        try:
            svg, stats = render_entry(d)
        except Exception as e:
            summary["errors"] += 1
            summary["files"].append({"file": rel, "error": str(e)[:100]})
            continue
        if svg is None:
            summary["empty"] += 1
            continue
        svg_path = os.path.join(sub, name + ".svg")
        png_path = os.path.join(sub, name + ".png")
        with open(svg_path, "w") as f: f.write(svg)
        r = subprocess.run([TVGRENDER, svg_path, png_path, width],
                           capture_output=True, text=True)
        if r.returncode != 0:
            summary["errors"] += 1
            summary["files"].append({"file": rel, "error": "tvgrender: " + r.stderr[:100]})
            continue
        summary["rendered"] += 1
        summary["files"].append({"file": rel, "png": png_path, **stats})
    print(json.dumps(summary, indent=1)[:6000])

if __name__ == "__main__":
    main()
