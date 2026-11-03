#!/usr/bin/env python3
"""Generalized Wizard Gang FLA puppet builder.

Generalized 2026-11-02 from tools/build_ashes.py (the Ashes XFL authoring engine,
PR #293) under the owner's Cape Jones -> Wizard Gang transfer order: same XFL
format, same matrix/pose machinery, driven per-character by tools/characters/<char>.json
(frame-data JSON pattern adopted from the cape-jones FD work).

All art = the character's OWN real extracted layers in
~/workspace/your_files/wizard-gang-part-libraries/<char>/rig-proof/parts/
(full-common-canvas layers, HSV segmentation + Telea inpainting upstream).
Nothing is drawn, generated, or borrowed from another character.

Rig anatomy (what the source art actually contains):
- robe split into TORSO + ROBE_SKIRT by a horizontal cut of the real robe layer
  with a shared overlap band (same method as the Ashes cut-apart, parts.json:
  torso rows ..split+ov, skirt rows split-ov.. — real pixels on both sides).
- HEAD on a neck pivot (head bbox bottom-centre). Head/arms are butt joints
  (0px measured overlap in the source segmentation) — pose ranges are modest
  and the robe-full + figure underlay layers sit beneath so a wedge never
  shows void.
- ARM_L / ARM_R on shoulder pivots where the character HAS separated arms.
  Sombra and Hollow have none in their source — their configs say so and
  their puppets ship without arm symbols (gap logged, never fabricated).
- HEADCOMP face states: OPEN / BLINK (real closed-eye layers composited) /
  LOOK_L / LOOK_R (eye layers translated) / SQUINT (eye layers y-scaled).
  Kiko has no separated eyes in her standard variant — HEADCOMP is her
  head-baked face only (gap logged).
- The 8 non-Ashes wizards are MOUTHLESS by canon: no mouth symbols are built.
  (Ashes keeps his grill — he is built by build_ashes.py, not this script.)
- Legs/hips/knees and elbows DO NOT EXIST in any character's source art
  (robe-to-the-floor designs, single-piece arms). No symbols claim them.

Usage: python3 build_puppet.py <char> [<char> ...]   (default: all configured)
Output: $WG_BUILD_OUT/<CODE>_ORIGINAL_PUPPET_<CHAR>_VERSION_001/ (XFL dir) + .fla
        WG_BUILD_OUT defaults to ~/workspace/fla-build/out
"""
import json, math, os, shutil, sys, zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_DIR = os.path.join(HERE, "characters")
OUT = os.environ.get("WG_BUILD_OUT", os.path.expanduser("~/workspace/fla-build/out"))

# ---------- matrix helpers (Flash convention, from build_ashes.py) ----------
def mat_identity(): return (1, 0, 0, 1, 0, 0)
def mat_mul(m1, m2):
    a, b, c, d, e, f = m1; g, h, i, j, k, l = m2
    return (a*g+c*h, b*g+d*h, a*i+c*j, b*i+d*j, a*k+c*l+e, b*k+d*l+f)
def mat_T(tx, ty): return (1, 0, 0, 1, tx, ty)
def mat_R(deg):
    r = math.radians(deg); co, si = math.cos(r), math.sin(r)
    return (co, si, -si, co, 0, 0)
def mat_S(sx, sy): return (sx, 0, 0, sy, 0, 0)
def about(pivot, m):
    px, py = pivot
    return mat_mul(mat_T(px, py), mat_mul(m, mat_T(-px, -py)))
def fmt(m):
    a, b, c, d, tx, ty = m
    parts = []
    if abs(a-1) > 1e-9: parts.append(f'a="{a:.5f}"')
    if abs(b) > 1e-9: parts.append(f'b="{b:.5f}"')
    if abs(c) > 1e-9: parts.append(f'c="{c:.5f}"')
    if abs(d-1) > 1e-9: parts.append(f'd="{d:.5f}"')
    if abs(tx) > 1e-9: parts.append(f'tx="{tx:.2f}"')
    if abs(ty) > 1e-9: parts.append(f'ty="{ty:.2f}"')
    return " ".join(parts) if parts else 'tx="0" ty="0"'

_id = [0]
def itemid():
    _id[0] += 1
    return f"5eed2026-{_id[0]:08x}"

class FLA:
    def __init__(self, rootname):
        self.dir = os.path.join(OUT, rootname)
        shutil.rmtree(self.dir, ignore_errors=True)
        os.makedirs(f"{self.dir}/LIBRARY", exist_ok=True)
        os.makedirs(f"{self.dir}/bin", exist_ok=True)
        self.media = []
        self.symbols = []
        self._dat = 0
    def add_bitmap(self, name, src):
        im = Image.open(src); w, h = im.size
        href = name + os.path.splitext(src)[1].lower()
        dst = os.path.join(self.dir, "LIBRARY", href)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
        self._dat += 1
        dat = f"M {self._dat} 1335000000.dat"
        shutil.copy(src, os.path.join(self.dir, "bin", dat))
        self.media.append((name, href, w, h, dat))
        return name
    def add_symbol(self, name, timeline_xml):
        fn = name.split("/")[-1] + ".xml"
        path = os.path.join(self.dir, "LIBRARY", fn)
        with open(path, "w") as f:
            f.write(f'<DOMSymbolItem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://ns.adobe.com/xfl/2008/" name="{name}" itemID="{itemid()}" symbolType="graphic" lastModified="1335000000">\n'
                    f'  <timeline>\n    <DOMTimeline name="{name.split("/")[-1]}">\n{timeline_xml}    </DOMTimeline>\n  </timeline>\n</DOMSymbolItem>')
        self.symbols.append((name, fn))
    def document(self, width, height, fps, timeline_xml, docname, folders):
        media = "\n".join(
            f'          <DOMBitmapItem name="{n}" itemID="{itemid()}" sourceExternalFilepath="WG library" sourceLastImported="1335000000" compressionType="lossless" originalCompressionType="lossless" quality="100" href="{href}" bitmapDataHRef="{dat}" frameRight="{w*20}" frameBottom="{h*20}"/>'
            for (n, href, w, h, dat) in self.media)
        includes = "\n".join(
            f'          <Include href="{fn}" itemIcon="1" loadImmediate="false" itemID="{itemid()}" lastModified="1335000000"/>'
            for (n, fn) in self.symbols)
        fold = "\n".join(f'          <DOMFolderItem name="{fd}" itemID="{itemid()}"/>' for fd in folders)
        xml = (f'<DOMDocument xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://ns.adobe.com/xfl/2008/" width="{width}" height="{height}" frameRate="{fps}" currentTimeline="1" xflVersion="2.1" creatorInfo="WG FLA lane (XFL authored)" platform="Linux" majorVersion="11" minorVersion="5" buildNumber="325" nextSceneIdentifier="2" playOptionsPlayLoop="false">\n'
               f'     <folders>\n{fold}\n     </folders>\n'
               f'     <media>\n{media}\n     </media>\n'
               f'     <symbols>\n{includes}\n     </symbols>\n'
               f'     <timelines>\n{timeline_xml}     </timelines>\n</DOMDocument>')
        with open(f"{self.dir}/DOMDocument.xml", "w") as f: f.write(xml)
        with open(f"{self.dir}/{docname}.xfl", "w") as f: f.write("PROXY-CS5")
        os.makedirs(f"{self.dir}/META-INF", exist_ok=True)
        with open(f"{self.dir}/META-INF/metadata.xml", "w") as f:
            f.write('<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax"><rdf:Description rdf:about=""><dc:format xmlns:dc="http://purl.org/dc/elements/1.1/">application/vnd.adobe.fla</dc:format></rdf:Description></rdf:RDF></x:xmpmeta>')
    def zip_fla(self, outname):
        zpath = os.path.join(OUT, outname)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(self.dir):
                for fn in files:
                    p = os.path.join(root, fn)
                    z.write(p, os.path.relpath(p, self.dir))
        return zpath

def layer(name, frames, color="#4FFF4F", locked=False, guide=False):
    fr = "\n".join(frames)
    lk = ' locked="true"' if locked else ""
    gt = ' layerType="guide"' if guide else ""
    return (f'        <DOMLayer name="{name}" color="{color}"{lk}{gt}>\n          <frames>\n{fr}\n          </frames>\n        </DOMLayer>')

def frame(index, elements, duration=None, label=None):
    dur = f' duration="{duration}"' if duration else ""
    lab = f' name="{label}" labelType="name"' if label else ""
    el = "\n".join(elements) if elements else ""
    if el:
        el = f"\n{el}\n                    "
    return f'            <DOMFrame index="{index}"{dur}{lab} keyMode="9728">\n              <elements>{el}</elements>\n            </DOMFrame>'

def sym_inst(libname, m, tp, firstframe=None, loop="single frame"):
    ff = f' firstFrame="{firstframe}"' if firstframe is not None else ""
    return (f'                <DOMSymbolInstance libraryItemName="{libname}" symbolType="graphic"{ff} loop="{loop}">\n'
            f'                  <matrix>\n                    <Matrix {fmt(m)}/>\n                  </matrix>\n'
            f'                  <transformationPoint>\n                    <Point x="{tp[0]}" y="{tp[1]}"/>\n                  </transformationPoint>\n'
            f'                </DOMSymbolInstance>')

def bmp_inst(libname, tx, ty):
    m = mat_T(tx, ty)
    return (f'                <DOMBitmapInstance libraryItemName="{libname}">\n'
            f'                  <matrix>\n                    <Matrix {fmt(m)}/>\n                  </matrix>\n'
            f'                </DOMBitmapInstance>')

def layers_xml(*layers):
    return "      <layers>\n" + "\n".join(layers) + "\n      </layers>\n"

def timeline(name, layers):
    return (f'          <DOMTimeline name="{name}">\n               <layers>\n'
            + "\n".join("                    " + l.replace("\n", "\n                    ") for l in layers)
            + "\n               </layers>\n          </DOMTimeline>\n")

# ---------- poses: (label, face_state, {PART: (rot_deg, dx, dy)}) ----------
POSES = [
    ("NEUTRAL",   0, {}),
    ("BLINK",     1, {}),
    ("LEAN_R",    3, {"TORSO": (2, 2, 0), "ROBE_SKIRT": (-1, 0, 0), "HEAD": (5, 2, 0),
                      "ARM_L": (0, 0, 0), "ARM_R": (0, 0, 0), "CHAIN": (3, 0, 0)}),
    ("LEAN_L",    2, {"TORSO": (-2, -2, 0), "ROBE_SKIRT": (1, 0, 0), "HEAD": (-5, -2, 0),
                      "ARM_L": (0, 0, 0), "ARM_R": (0, 0, 0), "CHAIN": (-3, 0, 0)}),
    ("BOW",       0, {"TORSO": (2, 0, 7), "HEAD": (4, 3, 14), "ROBE_SKIRT": (0, 0, 0),
                      "ARM_L": (-8, 0, 0), "ARM_R": (8, 0, 0), "CHAIN": (4, 1, 6)}),
    ("TURN_R",    3, {"TORSO": (2, 1, 0), "HEAD": (6, 2, 0), "ROBE_SKIRT": (-1, 0, 0),
                      "ARM_L": (0, 0, 0), "ARM_R": (0, 0, 0), "CHAIN": (3, 0, 0)}),
    ("ARMS_WIDE", 0, {"TORSO": (-2, 0, 0), "HEAD": (-3, 0, 0), "ROBE_SKIRT": (2, 0, 0),
                      "ARM_L": (0, 0, 7, 1.05), "ARM_R": (0, 0, 7, 1.05), "CHAIN": (-2, 0, 0)}),
    ("SETTLE",    1, {"TORSO": (1, 0, 1), "HEAD": (2, 0, 1), "ROBE_SKIRT": (-1, 0, 0),
                      "ARM_L": (-4, 0, 0), "ARM_R": (4, 0, 0), "CHAIN": (1, 0, 0)}),
]
FACE_STATES = ["OPEN", "BLINK", "LOOK_L", "LOOK_R", "SQUINT"]

def build(char):
    cfg = json.load(open(os.path.join(CFG_DIR, f"{char}.json")))
    W, H = cfg["canvas"]
    parts_dir = os.path.join(cfg["folder"], "rig-proof", "parts")
    rig_dir = os.path.join(cfg["folder"], "rig-proof")
    U = char.upper()
    P = f"{cfg['code']}_{U}_PUPPET_V001"
    rootname = f"{cfg['code']}_ORIGINAL_PUPPET_{U}_VERSION_001"
    media_dir = os.path.join(OUT, "_media", char)
    os.makedirs(media_dir, exist_ok=True)

    bb = cfg["bboxes"]
    def bbox_of(layer_key):
        # manifest layer names look like '01_robe' / '02_head' / '06_arm_L'
        for k, v in bb.items():
            if k.split("_", 1)[1].lower() == layer_key.lower():
                return v
        return None
    robe_bb = bbox_of("robe") or bbox_of("body")
    head_bb = bbox_of("head")
    cx = lambda b: (b[0] + b[2]) / 2

    # waist split of the real robe layer, with shared overlap band (Ashes method)
    split_y = int(robe_bb[1] + 0.52 * (robe_bb[3] - robe_bb[1]))
    ov = max(8, int(0.035 * H))
    robe_im = Image.open(os.path.join(parts_dir, cfg["robe"])).convert("RGBA")
    torso_im = robe_im.copy(); torso_im.paste((0, 0, 0, 0), (0, split_y + ov, W, H))
    skirt_im = robe_im.copy(); skirt_im.paste((0, 0, 0, 0), (0, 0, W, split_y - ov))
    torso_path = os.path.join(media_dir, "torso.png"); torso_im.save(torso_path)
    skirt_path = os.path.join(media_dir, "robe_skirt.png"); skirt_im.save(skirt_path)

    # pivots from measured bboxes
    PIV = {
        "TORSO": (cx(robe_bb), split_y),
        "ROBE_SKIRT": (cx(robe_bb), split_y),
        "HEAD": (cx(head_bb), head_bb[3] - 0.10 * (head_bb[3] - head_bb[1])),
    }
    if cfg.get("chain"):
        chain_bb = bbox_of("chain") or bbox_of("chains")
        if not chain_bb:  # hollow: chain file exists but is absent from the manifest — measure the layer itself
            chain_bb = Image.open(os.path.join(parts_dir, cfg["chain"])).convert("RGBA").getchannel("A").getbbox()
        if chain_bb: PIV["CHAIN"] = (cx(chain_bb), chain_bb[1])
    if cfg.get("arm_L"):
        a = bbox_of("arm_L"); PIV["ARM_L"] = (a[2] - 0.18 * (a[2] - a[0]), a[1] + 0.10 * (a[3] - a[1]))
    if cfg.get("arm_R"):
        a = bbox_of("arm_R"); PIV["ARM_R"] = (a[0] + 0.18 * (a[2] - a[0]), a[1] + 0.10 * (a[3] - a[1]))
    eye_c = None
    if cfg.get("eye_L") and cfg.get("eye_R"):
        el, er = bbox_of("eye_L"), bbox_of("eye_R")
        if el and er: eye_c = ((el[0] + er[2]) / 2, (el[1] + er[3]) / 2)

    fla = FLA(rootname)
    N = {}
    def leaf(key, src):
        bmp = f"{P}/media/{key}"
        fla.add_bitmap(bmp, src)
        sym = f"{P}/WG_{U}_FRONT_{key}"
        fla.add_symbol(sym, layers_xml(layer("bitmap", [frame(0, [bmp_inst(bmp, 0, 0)])])))
        N[key] = sym
    # NOTE: no full-figure underlay — measured on Static 2026-11-02: an identity
    # full-figure copy beneath the moving layers ghosts every moved part against
    # its own neutral copy. The robe underlay below is the only gap-fill kept
    # (waist wedge between TORSO and ROBE_SKIRT, same texture, reads clean).
    leaf("ROBE_FULL", os.path.join(parts_dir, cfg["robe"]))
    leaf("TORSO", torso_path)
    leaf("ROBE_SKIRT", skirt_path)
    leaf("HEAD", os.path.join(parts_dir, cfg["head"]))
    if cfg.get("arm_L"): leaf("ARM_L", os.path.join(parts_dir, cfg["arm_L"]))
    if cfg.get("arm_R"): leaf("ARM_R", os.path.join(parts_dir, cfg["arm_R"]))
    if cfg.get("chain"): leaf("CHAIN", os.path.join(parts_dir, cfg["chain"]))
    if cfg.get("eye_L"): leaf("EYE_L", os.path.join(parts_dir, cfg["eye_L"]))
    if cfg.get("eye_R"): leaf("EYE_R", os.path.join(parts_dir, cfg["eye_R"]))
    for ex in cfg.get("extras", []):
        leaf(ex["key"], os.path.join(parts_dir, ex["file"]))
    # blink lids: composite of the character's real closed-eye layers
    has_blink = bool(cfg.get("closed"))
    if has_blink:
        lids = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for fn in cfg["closed"]:
            lids.alpha_composite(Image.open(os.path.join(rig_dir, "rig-layers", fn)).convert("RGBA"))
        lids_path = os.path.join(media_dir, "lids_closed.png"); lids.save(lids_path)
        leaf("LIDS", lids_path)

    # ---- HEADCOMP: face states ----
    has_eyes = "EYE_L" in N and "EYE_R" in N
    states = FACE_STATES if has_eyes else ["OPEN"]
    def face_elements(st):
        el = [sym_inst(N["HEAD"], mat_identity(), (0, 0))]
        if not has_eyes:
            return el
        if st == "BLINK" and has_blink:
            return el + [sym_inst(N["LIDS"], mat_identity(), (0, 0))]
        dx = {"LOOK_L": -max(2, int(0.016 * W)), "LOOK_R": max(2, int(0.016 * W))}.get(st, 0)
        m = mat_T(dx, 0)
        if st == "SQUINT":
            m = about(eye_c, mat_S(1, 0.55))
        if st == "BLINK":  # no closed layers: squint stands in, noted in proof doc
            m = about(eye_c, mat_S(1, 0.3))
        return el + [sym_inst(N["EYE_L"], m, (0, 0)), sym_inst(N["EYE_R"], m, (0, 0))]
    headcomp = f"{P}/WG_{U}_FRONT_HEADCOMP"
    fla.add_symbol(headcomp, layers_xml(
        layer("LABELS_FACE", [frame(i, [], label=s) for i, s in enumerate(states)], locked=True),
        layer("face", [frame(i, face_elements(s)) for i, s in enumerate(states)])))
    N["HEADCOMP"] = headcomp

    # ---- master puppet: one frame per pose ----
    def pose_matrix(part, spec):
        if part not in spec: return mat_identity()
        rot, dx, dy = spec[part][0], spec[part][1], spec[part][2]
        sc = spec[part][3] if len(spec[part]) > 3 else 1.0
        m = mat_mul(mat_R(rot), mat_S(sc, sc)) if sc != 1.0 else mat_R(rot)
        return mat_mul(mat_T(dx, dy), about(PIV[part], m))
    def extra_matrix(ex, spec):
        # extras follow their anchor part (head lag 0.7 for drapes/bells, arm for props)
        anchor = {"head": "HEAD", "arm_R": "ARM_R", "arm_L": "ARM_L"}.get(ex.get("follow", "head"), "HEAD")
        if anchor not in spec: return mat_identity()
        rot, dx, dy = spec[anchor][0], spec[anchor][1], spec[anchor][2]
        f = 0.7 if ex.get("follow") == "head" else 1.0
        piv = PIV.get(anchor, PIV["HEAD"])
        return mat_mul(mat_T(dx * f, dy * f), about(piv, mat_R(rot * f)))
    def frames_for(key):
        out = []
        for i, (label, face_ff, spec) in enumerate(POSES):
            if key == "HEADCOMP":
                ff = face_ff if has_eyes else 0
                el = [sym_inst(N["HEADCOMP"], pose_matrix("HEAD", spec), PIV["HEAD"], firstframe=ff)]
            elif key.startswith("EXTRA:"):
                ex = next(e for e in cfg["extras"] if e["key"] == key[6:])
                el = [sym_inst(N[ex["key"]], extra_matrix(ex, spec), PIV["HEAD"])]
            else:
                el = [sym_inst(N[key], pose_matrix(key, spec), PIV[key])]
            out.append(frame(i, el))
        return out
    master = f"{P}/WG_{U}_FRONT_PUPPET"
    mlayers = [layer("POSES_LABELS", [frame(i, [], label=p[0]) for i, p in enumerate(POSES)], locked=True)]
    if cfg.get("arm_R"): mlayers.append(layer("ARM_R", frames_for("ARM_R")))
    if cfg.get("arm_L"): mlayers.append(layer("ARM_L", frames_for("ARM_L")))
    for ex in cfg.get("extras", []):
        mlayers.append(layer(ex["key"], frames_for(f"EXTRA:{ex['key']}")))
    if cfg.get("chain"): mlayers.append(layer("CHAIN", frames_for("CHAIN")))
    mlayers.append(layer("HEADCOMP", frames_for("HEADCOMP")))
    mlayers.append(layer("TORSO", frames_for("TORSO")))
    mlayers.append(layer("ROBE_SKIRT", frames_for("ROBE_SKIRT")))
    mlayers.append(layer("ROBE_UNDERLAY", [frame(i, [sym_inst(N["ROBE_FULL"], mat_identity(), (0, 0))]) for i in range(len(POSES))]))
    fla.add_symbol(master, layers_xml(*mlayers))

    stage_layer = layer(f"WG_{U}", [frame(0, [sym_inst(master, mat_T(740, 100), (0, 0), firstframe=0)], duration=1)])
    ref_layer = layer("REF", [frame(0, [])], guide=True)
    fla.document(1920, 1080, 24, timeline("Scene 1", [ref_layer, stage_layer]), rootname, [P])
    zpath = fla.zip_fla(rootname + ".fla")
    print(f"{char}: built {zpath} ({os.path.getsize(zpath)} bytes), canvas {W}x{H}, "
          f"arms={'ARM_L' in N and 'ARM_R' in N}, eyes={has_eyes}, blink_layers={has_blink}, "
          f"split_y={split_y}, poses={len(POSES)}")
    return zpath

if __name__ == "__main__":
    chars = sys.argv[1:] or ["static", "cipher", "sombra", "kiko", "theory", "onyx", "echo", "hollow"]
    os.makedirs(OUT, exist_ok=True)
    for c in chars:
        build(c)
