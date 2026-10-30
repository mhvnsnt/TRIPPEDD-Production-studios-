#!/usr/bin/env python3
"""Generate a RIG-MAP markdown per character from a Harmony template's
scene.xstage (node graph XML) + elements table + PALETTE_LIST.
Usage: rigmap.py <tpl_dir> <out.md>  — tpl_dir contains scene.xstage."""
import os, sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

def parse(tpl_dir):
    tree = ET.parse(os.path.join(tpl_dir, "scene.xstage"))
    root = tree.getroot()
    proj = root.attrib
    elements = {}
    el_section = root.find("elements")
    if el_section is not None:
        for el in el_section.iter("element"):
            name = el.get("elementName")
            dwgs = [d.get("name") for d in el.iter("dwg")]
            elements[name] = dwgs
    modules = []          # (type, name, group_path)
    links = []            # (out, in, inport)
    groups = []
    def walk(elem, path):
        for child in elem:
            if child.tag == "group":
                gpath = path + [child.get("name")]
                groups.append("/".join(gpath))
                walk(child, gpath)
            elif child.tag == "module":
                modules.append((child.get("type"), child.get("name"), "/".join(path)))
            elif child.tag == "linkedlist":
                for lnk in child.iter("link"):
                    links.append((lnk.get("out"), lnk.get("in"), lnk.get("inport")))
            else:
                walk(child, path)
    scenes = root.find("scenes")
    walk(scenes if scenes is not None else root, [])
    return proj, elements, modules, links, groups

def main():
    tpl_dir, out_path = sys.argv[1], sys.argv[2]
    char = os.path.basename(tpl_dir.rstrip("/")).replace(".tpl", "")
    proj, elements, modules, links, groups = parse(tpl_dir)
    census = Counter(t for t, _, _ in modules)
    reads = [(n, g) for t, n, g in modules if t == "READ"]
    pegs = [(n, g) for t, n, g in modules if t == "PEG"]
    # peg chain: follow out->in links upward from each READ
    feeds = defaultdict(list)
    for out, into, _port in links:
        feeds[into].append(out)
    def chain(start):
        seen = []
        cur = start
        for _ in range(12):
            ups = feeds.get(cur, [])
            if not ups: break
            cur = ups[0]
            if cur in seen: break
            seen.append(cur)
        return seen
    palettes = []
    pl_path = os.path.join(tpl_dir, "PALETTE_LIST")
    if os.path.exists(pl_path):
        for line in open(pl_path, errors="replace"):
            line = line.strip()
            if line and not line.startswith("ToonBoom"):
                palettes.append(line.split()[0].replace("palette-library/", ""))
    lines = []
    lines.append(f"# RIG MAP — {char} (Toon Boom Harmony template)")
    lines.append("")
    lines.append(f"- Source: `{os.path.basename(tpl_dir)}` — scene.xstage, Harmony "
                 f"{proj.get('source', 'unknown')}")
    lines.append(f"- Modules total: {len(modules)} | links: {len(links)} | "
                 f"elements (drawing columns): {len(elements)}")
    lines.append(f"- Module census: " + ", ".join(f"{t}×{c}" for t, c in census.most_common()))
    lines.append(f"- Palettes (PALETTE_LIST): {', '.join(palettes) if palettes else '(none)'}")
    lines.append("")
    lines.append("## Group tree")
    for g in groups:
        lines.append(f"- {g}")
    lines.append("")
    lines.append("## Elements = substitution sets (READ node → drawings)")
    lines.append("Each element is one body part column; its drawings are the swap set "
                 "(poses/expressions) an animator cycles through.")
    lines.append("")
    for name, _g in sorted(reads):
        dwgs = elements.get(name, [])
        lines.append(f"### {name} — {len(dwgs)} drawings")
        lines.append(", ".join(dwgs) if dwgs else "(no element entry)")
        ch = chain(name)
        if ch:
            lines.append(f"- peg chain up: {' → '.join(ch)}")
        lines.append("")
    orphan = sorted(set(elements) - {n for n, _ in reads})
    if orphan:
        lines.append("## Elements with no READ node in this scene")
        for name in orphan:
            lines.append(f"- {name}: {len(elements[name])} drawings")
        lines.append("")
    lines.append(f"## Pegs ({len(pegs)})")
    lines.append(", ".join(sorted(n for n, _ in pegs)))
    lines.append("")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print(f"{char}: {len(modules)} modules, {len(elements)} elements, "
          f"{sum(len(v) for v in elements.values())} drawings -> {out_path}")

if __name__ == "__main__":
    main()
