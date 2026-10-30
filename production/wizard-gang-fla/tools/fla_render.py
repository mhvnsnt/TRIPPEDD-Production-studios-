#!/usr/bin/env python3
"""Minimal XFL compositor: executes the FLA files authored by build_ashes.py.
Renders a library symbol at a frame, or the document timeline at a frame,
by walking DOMSymbolInstance/DOMBitmapInstance elements and applying their
matrices (Flash semantics: full matrix maps child local -> parent local).
This exists because the local leaf renderer cannot draw bitmap/nested files
(see agent-ops renderer-contract.md); poses/clips rendered here are exactly
the transforms the .fla encodes.
"""
import argparse, os, sys
import xml.etree.ElementTree as ET
from PIL import Image

NS = "{http://ns.adobe.com/xfl/2008/}"

def mat_inv(m):
    a, b, c, d, tx, ty = m
    det = a * d - b * c
    if abs(det) < 1e-12: return None
    ia, ib, ic, idd = d / det, -c / det, -b / det, a / det
    return (ia, ib, ic, idd, -(ia * tx + ib * ty), -(ic * tx + idd * ty))

def warp(child, m, size):
    inv = mat_inv(m)
    if inv is None: return Image.new("RGBA", size, (0, 0, 0, 0))
    ia, ib, ic, idd, itx, ity = inv
    return child.transform(size, Image.AFFINE, (ia, ib, itx, ic, idd, ity), resample=Image.BILINEAR)

class FLA:
    def __init__(self, xfl_dir):
        self.dir = xfl_dir
        self.doc = ET.parse(os.path.join(xfl_dir, "DOMDocument.xml")).getroot()
        self.media = {}
        for mi in self.doc.iter(NS + "DOMBitmapItem"):
            self.media[mi.get("name")] = os.path.join(xfl_dir, "LIBRARY", mi.get("href"))
        self.symbols = {}
        libdir = os.path.join(xfl_dir, "LIBRARY")
        for root, dirs, files in os.walk(libdir):
            for fn in files:
                if fn.endswith(".xml"):
                    r = ET.parse(os.path.join(root, fn)).getroot()
                    if r.tag == NS + "DOMSymbolItem":
                        self.symbols[r.get("name")] = r.find(f"{NS}timeline/{NS}DOMTimeline")
        self._cache = {}
        self._imgcache = {}
    def img(self, path):
        if path not in self._imgcache:
            self._imgcache[path] = Image.open(path).convert("RGBA")
        return self._imgcache[path]
    def canvas_for(self, name):
        if "BG_" in name or name.endswith("_PLATE"): return (1920, 1080)
        return (400, 864)
    def active_frame(self, layer_el, f):
        best = None
        for fr in layer_el.iter(NS + "DOMFrame"):
            idx = int(fr.get("index"))
            if idx <= f: best = fr
            else: break
        return best
    def render_timeline(self, tl, f, size):
        out = Image.new("RGBA", size, (0, 0, 0, 0))
        layers = tl.find(NS + "layers")
        for layer_el in reversed(list(layers)):
            if layer_el.get("layerType") == "guide": continue
            fr = self.active_frame(layer_el, f)
            if fr is None: continue
            els = fr.find(NS + "elements")
            if els is None: continue
            for el in els:
                out.alpha_composite(self.render_element(el, f, fr, size))
        return out
    def render_element(self, el, f, fr, size):
        if el.tag == NS + "DOMBitmapInstance":
            m = self.matrix_of(el)
            return warp(self.img(self.media[el.get("libraryItemName")]), m, size)
        if el.tag == NS + "DOMSymbolInstance":
            name = el.get("libraryItemName")
            loop = el.get("loop", "loop")
            ff = int(el.get("firstFrame", 0))
            if loop == "single frame": cf = ff
            elif loop == "play once": cf = min(ff + (f - int(fr.get("index"))), 10 ** 6)
            else: cf = ff + (f - int(fr.get("index")))
            child = self.render_symbol(name, cf)
            return warp(child, self.matrix_of(el), size)
        return Image.new("RGBA", size, (0, 0, 0, 0))
    def matrix_of(self, el):
        mx = el.find(f"{NS}matrix/{NS}Matrix")
        if mx is None: return (1, 0, 0, 1, 0, 0)
        g = lambda k, d: float(mx.get(k, d))
        return (g("a", 1), g("b", 0), g("c", 0), g("d", 1), g("tx", 0), g("ty", 0))
    def render_symbol(self, name, f):
        key = (name, f)
        if key in self._cache: return self._cache[key]
        tl = self.symbols[name]
        img = self.render_timeline(tl, f, self.canvas_for(name))
        self._cache[key] = img
        return img
    def render_scene(self, f):
        w = int(self.doc.get("width")); h = int(self.doc.get("height"))
        tl = self.doc.find(f"{NS}timelines/{NS}DOMTimeline")
        return self.render_timeline(tl, f, (w, h))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("xfl_dir")
    ap.add_argument("--symbol"); ap.add_argument("--frame", type=int, default=0)
    ap.add_argument("--scene", action="store_true")
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--bg", default=None)
    a = ap.parse_args()
    fla = FLA(a.xfl_dir)
    img = fla.render_scene(a.frame) if a.scene else fla.render_symbol(a.symbol, a.frame)
    if a.bg:
        bg = Image.new("RGBA", img.size, a.bg)
        bg.alpha_composite(img); img = bg
    if a.scale != 1.0:
        img = img.resize((int(img.width * a.scale), int(img.height * a.scale)), Image.LANCZOS)
    img.save(a.out)
    print("wrote", a.out, img.size)
