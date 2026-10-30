#!/usr/bin/env python3
"""Build WG101 Ashes FLA puppet + scene (XFL authored to the Gumball-derived standard).
All character art = real library files (cut-apart set from GMSS rig-proof layers).
BG plates are authored set dressing (painted in-script), labelled as such.
"""
import json, math, os, shutil, zipfile
from PIL import Image, ImageDraw, ImageFilter

WS = "/home/hatch/workspace"
CUT = f"{WS}/your_files/wizard-gang-part-libraries/_cut-apart/ashes"
LIB = f"{WS}/your_files/wizard-gang-part-libraries/ashes"
OUT = f"{WS}/fla-build/out"
PARTS = json.load(open(f"{CUT}/parts.json"))
PIV = {p["name"]: tuple(p["pivot"]) for p in PARTS["parts"]}
BBOX = {p["name"]: tuple(p["bbox"]) for p in PARTS["parts"]}
CANVAS = (400, 864)

_id = [0]
def itemid():
    _id[0] += 1
    return f"5eed2026-{_id[0]:08x}"

def mat_identity(): return (1,0,0,1,0,0)
def mat_mul(m1, m2):
    # Flash convention: x' = a*x + c*y + tx ; y' = b*x + d*y + ty  (m2 applied first)
    a,b,c,d,e,f = m1; g,h,i,j,k,l = m2
    return (a*g+c*h, b*g+d*h, a*i+c*j, b*i+d*j, a*k+c*l+e, b*k+d*l+f)
def mat_T(tx,ty): return (1,0,0,1,tx,ty)
def mat_R(deg):
    r = math.radians(deg); co, si = math.cos(r), math.sin(r)
    return (co, si, -si, co, 0, 0)
def mat_S(sx,sy): return (sx,0,0,sy,0,0)
def about(pivot, m):
    px,py = pivot
    return mat_mul(mat_T(px,py), mat_mul(m, mat_T(-px,-py)))
def fmt(m):
    a,b,c,d,tx,ty = m
    parts = []
    if abs(a-1)>1e-9: parts.append(f'a="{a:.5f}"')
    if abs(b)>1e-9: parts.append(f'b="{b:.5f}"')
    if abs(c)>1e-9: parts.append(f'c="{c:.5f}"')
    if abs(d-1)>1e-9: parts.append(f'd="{d:.5f}"')
    if abs(tx)>1e-9: parts.append(f'tx="{tx:.2f}"')
    if abs(ty)>1e-9: parts.append(f'ty="{ty:.2f}"')
    return " ".join(parts) if parts else 'tx="0" ty="0"'

class FLA:
    def __init__(self, rootname):
        self.dir = os.path.join(OUT, rootname)
        shutil.rmtree(self.dir, ignore_errors=True)
        os.makedirs(f"{self.dir}/LIBRARY", exist_ok=True)
        os.makedirs(f"{self.dir}/bin", exist_ok=True)
        self.media = []     # (name, srcpath, w, h)
        self.symbols = []   # (name, xml)
        self._dat = 0
    def add_bitmap(self, name, src):
        im = Image.open(src); w,h = im.size
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
        fn = name.split("/")[-1] + ".xml"   # LIBRARY is flat; folders live in the symbol name (Animate format)
        path = os.path.join(self.dir, "LIBRARY", fn)
        os.makedirs(os.path.dirname(path), exist_ok=True)
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

# ---------------- media prep ----------------
def part_src(name): return f"{CUT}/parts/{name}.png"
def placement(name):
    """bitmap top-left inside canvas space for a cut-apart part file."""
    im = Image.open(part_src(name))
    if im.size == CANVAS: return (0, 0)
    b = BBOX[name]; return (b[0], b[1])

def build_library(fla, P):
    """Register all bitmaps + symbols shared by puppet & scene. Returns dict of names."""
    N = {}
    leaf_src = {
        "ROBE_SKIRT": part_src("robe_skirt"), "TORSO": part_src("torso"),
        "ARM_L": part_src("arm_L"), "ARM_R": part_src("arm_R"),
        "HAND_R": part_src("hand_R"), "CHAIN": part_src("chain"),
        "BRAID_L": part_src("braid_L"), "BRAID_R": part_src("braid_R"),
        "FACE": part_src("head"), "EYES": part_src("eyes"), "GRILL": part_src("grill"),
        "ROBE_FULL": part_src("robe_full"),
    }
    fla.add_bitmap(f"{P}/media/FIGURE", f"{LIB}/rig-proof/parts/00_base_full_figure.png")
    fla.add_symbol(f"{P}/WG_ASHES_FRONT_FIGURE_UNDERLAY", layers_xml(layer("bitmap", [frame(0, [bmp_inst(f"{P}/media/FIGURE", 0, 0)])])))
    N["FIGURE_UNDERLAY"] = f"{P}/WG_ASHES_FRONT_FIGURE_UNDERLAY"
    # merged lids (two library textures composited = assembly, not new art)
    lids = Image.new("RGBA", CANVAS, (0,0,0,0))
    for f in ["rig-layers/7_eye_closed_l.png", "rig-layers/8_eye_closed_r.png"]:
        lids.alpha_composite(Image.open(f"{LIB}/rig-proof/{f}").convert("RGBA"))
    lids_path = f"{OUT}/_media/lids_closed.png"; os.makedirs(f"{OUT}/_media", exist_ok=True)
    lids.save(lids_path); leaf_src["LIDS"] = lids_path
    for key, src in leaf_src.items():
        bmp_name = f"{P}/media/{key}"
        fla.add_bitmap(bmp_name, src)
        sym = f"{P}/WG_ASHES_FRONT_{key}"
        tx, ty = placement(key.lower()) if key.lower() in BBOX else (0,0)
        if key == "LIDS": tx, ty = 0, 0
        fla.add_symbol(sym, layers_xml(layer("bitmap", [frame(0, [bmp_inst(bmp_name, tx, ty)])])))
        N[key] = sym
    # eye pairs
    eyes_dir = f"{CUT}/swaps/eyes"
    pair_states = [("OPEN", "WG_ASHES_FRONT_EYE_PAIR_OPEN.png"), ("SMILE", "WG_ASHES_FRONT_EYE_PAIR_SMILE.png"),
                   ("LOOK_R", "WG_ASHES_FRONT_EYE_PAIR_LOOK_R.png"), ("LOOK_L", "WG_ASHES_FRONT_EYE_PAIR_LOOK_L.png"),
                   ("LOOK_UP", "WG_ASHES_FRONT_EYE_PAIR_LOOK_UP.png"), ("LOOK_DOWN", "WG_ASHES_FRONT_EYE_PAIR_LOOK_DOWN.png"),
                   ("ANGRY", "WG_ASHES_FRONT_EYE_PAIR_ANGRY.png"),
                   ("BW_OPEN", "base-white_WG_ASHES_FRONT_EYE_PAIR_OPEN.png"), ("BW_SMILE", "base-white_WG_ASHES_FRONT_EYE_PAIR_SMILE.png"),
                   ("BW_ANGRY", "base-white_WG_ASHES_FRONT_EYE_PAIR_ANGRY.png"), ("BW_LOOK_R", "base-white_WG_ASHES_FRONT_EYE_PAIR_LOOK_R.png")]
    pair_bmps = {}
    for st, fn in pair_states:
        bmp_name = f"{P}/media/EYE_{st}"
        fla.add_bitmap(bmp_name, f"{eyes_dir}/{fn}"); pair_bmps[st] = bmp_name
    # EYESCOMP: frame0 = baked (empty); 1.. = pair overlays at (112,78); labels layer
    eframes, elabels = [], []
    states = ["OPEN_BAKED"] + [s for s,_ in pair_states]
    for i, st in enumerate(states):
        el = [] if st == "OPEN_BAKED" else [bmp_inst(pair_bmps[st], 112, 78)]
        eframes.append(frame(i, el)); elabels.append(frame(i, [], label=st))
    eyescomp = f"{P}/WG_ASHES_FRONT_EYESCOMP"
    fla.add_symbol(eyescomp, layers_xml(
        layer("LABELS", elabels, locked=True),
        layer("eyes", eframes)))
    N["EYESCOMP"] = eyescomp
    # MOUTHCOMP: 14 Set-One shapes, native size centred on grill centre (189,170) - library registration
    mouth_dir = f"{CUT}/swaps/mouths"
    mframes, mlabels = [], []
    mouths = ["X_REST","A","B","C","D","E","F","G","H","O_ROUND","WIDE","HOLD_POSE","SMUG","BARE_TEETH"]
    for i, sh in enumerate(mouths):
        src = f"{mouth_dir}/WG_ASHES_MOUTH_{sh}.png"
        bmp_name = f"{P}/media/MOUTH_{sh}"
        fla.add_bitmap(bmp_name, src)
        im = Image.open(src)
        mframes.append(frame(i, [bmp_inst(bmp_name, 189 - im.width//2, 170 - im.height//2)]))
        mlabels.append(frame(i, [], label=sh))
    mouthcomp = f"{P}/WG_ASHES_FRONT_MOUTHCOMP"
    fla.add_symbol(mouthcomp, layers_xml(layer("LABELS", mlabels, locked=True), layer("mouths", mframes)))
    N["MOUTHCOMP"] = mouthcomp
    # HEADCOMP: face states
    # state: (label, eyescomp_ff, grill_(sx,sy) or None, lids_bool)
    face_states = [
        ("NEUTRAL", 0, None, False), ("BLINK", 0, None, True),
        ("TALK_1", 0, (1.0, 1.30), False), ("TALK_2", 0, (1.05, 1.12), False),
        ("TALK_WIDE", 0, (1.12, 1.55), False), ("SMILE", 1, (1.12, 1.55), False),
        ("LOOK_R", 2, None, False), ("ANGRY", 6, None, False),
    ]
    gp = PIV["grill"]
    def head_frames(get):
        out = []
        for i, st in enumerate(face_states):
            el = get(i, st)
            if el is not None: out.append(frame(i, el))
        return out
    headcomp = f"{P}/WG_ASHES_FRONT_HEADCOMP"
    fl = {
        "LABELS_FACE": [frame(i, [], label=st[0]) for i, st in enumerate(face_states)],
        "BRAID_L": head_frames(lambda i, st: [sym_inst(N["BRAID_L"], mat_identity(), PIV["braid_L"])]),
        "BRAID_R": head_frames(lambda i, st: [sym_inst(N["BRAID_R"], mat_identity(), PIV["braid_R"])]),
        "GRILL": head_frames(lambda i, st: [sym_inst(N["GRILL"], about(gp, mat_S(*st[2])) if st[2] else mat_identity(), gp)]),
        "LIDS": head_frames(lambda i, st: [sym_inst(N["LIDS"], mat_identity(), (0,0))] if st[3] else []),
        "EYESCOMP": head_frames(lambda i, st: [sym_inst(N["EYESCOMP"], mat_identity(), (0,0), firstframe=st[1])]),
        "FACE": head_frames(lambda i, st: [sym_inst(N["FACE"], mat_identity(), (0,0))]),
        "MOUTHCOMP_REF": head_frames(lambda i, st: [sym_inst(N["MOUTHCOMP"], mat_identity(), (0,0), firstframe=0)] if i == 0 else None),
    }
    fla.add_symbol(headcomp, layers_xml(
        layer("LABELS_FACE", fl["LABELS_FACE"], locked=True),
        layer("BRAID_L", fl["BRAID_L"]), layer("BRAID_R", fl["BRAID_R"]),
        layer("GRILL", fl["GRILL"]), layer("LIDS", fl["LIDS"]),
        layer("EYESCOMP", fl["EYESCOMP"]), layer("FACE", fl["FACE"]),
        layer("MOUTHCOMP_REF", fl["MOUTHCOMP_REF"], guide=True)))
    N["HEADCOMP"] = headcomp
    return N

# ---------------- poses ----------------
# part transform spec: (rot_deg, dx, dy) about part pivot, canvas space
POSES = [
    ("NEUTRAL",      0, {}),
    ("NEUTRAL_BLINK",1, {}),
    ("ANTICIPATION", 6, {"TORSO": (1.5,0,0), "HEAD": (-3,0,0), "ARM_L": (-6,0,0), "ARM_R": (6,0,0), "ROBE_SKIRT": (-1,0,0)}),
    ("GESTURE_WIDE", 4, {"ARM_L": (0,0,6,1.04), "ARM_R": (0,0,6,1.04), "HAND_R_WRIST": 0, "TORSO": (-2,0,0), "ROBE_SKIRT": (2.5,0,0), "HEAD": (-2.5,0,0), "CHAIN": (2,0,0)}),
    ("GESTURE_TALK1",2, {"ARM_L": (0,0,6,1.04), "ARM_R": (0,0,6,1.04), "HAND_R_WRIST": 0, "TORSO": (-2,0,0), "ROBE_SKIRT": (2.5,0,0), "HEAD": (-1,0,0), "CHAIN": (2,0,0)}),
    ("GESTURE_TALK2",3, {"ARM_L": (0,0,5,1.03), "ARM_R": (0,0,5,1.03), "HAND_R_WRIST": 0, "TORSO": (-1.5,0,0), "ROBE_SKIRT": (2,0,0), "HEAD": (-3.5,0,0), "CHAIN": (2,0,0)}),
    ("GESTURE_BLINK",1, {"ARM_L": (0,0,6,1.04), "ARM_R": (0,0,6,1.04), "HAND_R_WRIST": 0, "TORSO": (-2,0,0), "ROBE_SKIRT": (2.5,0,0), "HEAD": (-2.5,0,0), "CHAIN": (2,0,0)}),
    ("POINT",        4, {"ARM_R": (65,0,0), "HAND_R_WRIST": -15, "ARM_L": (-12,0,0), "TORSO": (3.5,0,0), "HEAD": (5,0,0), "ROBE_SKIRT": (-2,0,0), "CHAIN": (-2,0,0)}),
    ("POINT_HOLD",   6, {"ARM_R": (65,0,0), "HAND_R_WRIST": -15, "ARM_L": (-12,0,0), "TORSO": (3.5,0,0), "HEAD": (4,0,0), "ROBE_SKIRT": (-2,0,0), "CHAIN": (-2,0,0)}),
    ("SETTLE",       5, {"ARM_L": (-12,0,0), "ARM_R": (14,0,0), "TORSO": (2,0,0), "HEAD": (2,0,0), "ROBE_SKIRT": (-2,0,0), "CHAIN": (-2,0,0)}),
    ("SETTLE_BLINK", 1, {"ARM_L": (-12,0,0), "ARM_R": (14,0,0), "TORSO": (2,0,0), "HEAD": (2,0,0), "ROBE_SKIRT": (-2,0,0), "CHAIN": (-2,0,0)}),
    ("REST_X",       0, {"ARM_L": (-6,0,0), "ARM_R": (7,0,0), "TORSO": (1,0,0), "HEAD": (1,0,0), "ROBE_SKIRT": (-1,0,0)}),
    ("TRANSITION",   2, {"ARM_R": (40,0,0), "HAND_R_WRIST": 0, "ARM_L": (-8,0,0), "TORSO": (2.5,0,0), "HEAD": (3,0,0), "ROBE_SKIRT": (-2,0,0)}),
]
PART_PIVOT = {"TORSO": PIV["torso"], "ROBE_SKIRT": PIV["robe_skirt"], "ARM_L": PIV["arm_L"],
              "ARM_R": PIV["arm_R"], "CHAIN": PIV["chain"], "HEAD": PIV["head"]}

def pose_matrix(part, spec):
    if part not in spec: return mat_identity()
    rot, dx, dy = spec[part][0], spec[part][1], spec[part][2]
    sc = spec[part][3] if len(spec[part]) > 3 else 1.0
    m = mat_mul(mat_R(rot), mat_S(sc, sc)) if sc != 1.0 else mat_R(rot)
    return mat_mul(mat_T(dx, dy), about(PART_PIVOT[part], m))

def build_master(fla, P, N):
    master = f"{P}/WG_ASHES_FRONT_PUPPET"
    def frames_for(partkey, symkey=None, is_head=False, is_hand=False):
        out = []
        for i, (label, face_ff, spec) in enumerate(POSES):
            if is_head:
                el = [sym_inst(N["HEADCOMP"], pose_matrix("HEAD", spec), PART_PIVOT["HEAD"], firstframe=face_ff)]
            elif is_hand:
                m_arm = pose_matrix("ARM_R", spec)
                wrist = spec.get("HAND_R_WRIST", 0)
                m = mat_mul(m_arm, about(PIV["hand_R"], mat_R(wrist))) if wrist else m_arm
                el = [sym_inst(N["HAND_R"], m, PIV["hand_R"])]
            else:
                el = [sym_inst(N[symkey], pose_matrix(partkey, spec), PART_PIVOT[partkey])]
            out.append(frame(i, el))
        return out
    labels = [frame(i, [], label=p[0]) for i, p in enumerate(POSES)]
    underlay = []
    underlay_fig = []
    for i, (label, face_ff, spec) in enumerate(POSES):
        underlay.append(frame(i, [sym_inst(N["ROBE_FULL"], pose_matrix("TORSO", spec), PART_PIVOT["TORSO"])]))
        underlay_fig.append(frame(i, [sym_inst(N["FIGURE_UNDERLAY"], pose_matrix("TORSO", spec), PART_PIVOT["TORSO"])]))
    fla.add_symbol(master, layers_xml(
        layer("POSES_LABELS", labels, locked=True),
        layer("HAND_R", frames_for("HAND_R", is_hand=True)),
        layer("ARM_R", frames_for("ARM_R", "ARM_R")),
        layer("ARM_L", frames_for("ARM_L", "ARM_L")),
        layer("CHAIN", frames_for("CHAIN", "CHAIN")),
        layer("HEADCOMP", frames_for("HEAD", is_head=True)),
        layer("TORSO", frames_for("TORSO", "TORSO")),
        layer("ROBE_SKIRT", frames_for("ROBE_SKIRT", "ROBE_SKIRT")),
        layer("ROBE_UNDERLAY", underlay),
        layer("FIGURE_UNDERLAY", underlay_fig)))
    return master

def timeline(name, layers):
    return (f'          <DOMTimeline name="{name}">\n               <layers>\n'
            + "\n".join("                    " + l.replace("\n", "\n                    ") for l in layers)
            + "\n               </layers>\n          </DOMTimeline>\n")

# ---------------- puppet ----------------
def build_puppet():
    P = "WG101_ASHES_PUPPET_V001"
    fla = FLA("WG101_ORIGINAL_PUPPET_ASHES_VERSION_001")
    N = build_library(fla, P)
    master = build_master(fla, P, N)
    stage_layer = layer("WG_ASHES", [frame(0, [sym_inst(master, mat_T(740, 100), (0,0), firstframe=0)], duration=1)])
    ref_layer = layer("REF", [frame(0, [])], guide=True)
    fla.document(1920, 1080, 24, timeline("Scene 1", [ref_layer, stage_layer]),
                 "WG101_ORIGINAL_PUPPET_ASHES_VERSION_001", [P])
    return fla.zip_fla("WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla")

# ---------------- BG plates (authored set dressing) ----------------
def paint_bg():
    os.makedirs(f"{OUT}/_media", exist_ok=True)
    far = Image.new("RGB", (1920, 1080))
    px = far.load()
    for y in range(1080):
        t = y / 1080
        c = tuple(int(a + (b - a) * t) for a, b in zip((10, 14, 34), (26, 36, 66)))
        for x in range(0, 1920, 8):
            for dx in range(8):
                px[x + dx, y] = c
    d = ImageDraw.Draw(far, "RGBA")
    d.ellipse([1420, 90, 1560, 230], fill=(232, 226, 190, 255))
    far = far.filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(far, "RGBA")
    d.ellipse([1395, 65, 1585, 255], outline=(200, 200, 170, 60), width=10)
    import random; random.seed(7)
    for _ in range(90):
        x, y = random.randint(0, 1919), random.randint(0, 420)
        d.point((x, y), fill=(200, 205, 230, 160))
    # far skyline
    x = 0
    while x < 1920:
        w = random.randint(90, 220); h = random.randint(120, 300)
        d.rectangle([x, 1080 - h - 180, x + w, 1080], fill=(13, 19, 40, 255))
        x += w + random.randint(4, 30)
    d.rectangle([0, 900, 1920, 1080], fill=(16, 22, 44, 255))
    far.save(f"{OUT}/_media/bg_far.png")
    mid = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(mid)
    d.rectangle([0, 830, 1920, 1080], fill=(9, 13, 28, 255))
    for bx, bw, bh in [(60, 300, 420), (1560, 300, 470), (420, 180, 260), (1330, 170, 300)]:
        d.rectangle([bx, 830 - bh, bx + bw, 830], fill=(9, 13, 28, 255))
        d.rectangle([bx - 14, 830 - bh, bx + bw + 14, 830 - bh + 22], fill=(9, 13, 28, 255))
    for wx, wy in [(120, 560), (180, 640), (1620, 520), (1700, 620), (470, 640), (1390, 600)]:
        d.rectangle([wx, wy, wx + 26, wy + 36], fill=(240, 190, 90, 210))
    mid.save(f"{OUT}/_media/bg_mid.png")
    near = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(near)
    d.rectangle([0, 0, 130, 1080], fill=(4, 6, 13, 255))
    d.rectangle([1790, 0, 1920, 1080], fill=(4, 6, 13, 255))
    d.rectangle([0, 0, 1920, 60], fill=(4, 6, 13, 255))
    d.polygon([(130, 1080), (330, 1080), (130, 830)], fill=(4, 6, 13, 255))
    d.polygon([(1790, 1080), (1590, 1080), (1790, 830)], fill=(4, 6, 13, 255))
    near.save(f"{OUT}/_media/bg_near.png")

# ---------------- scene ----------------
def build_scene():
    paint_bg()
    P = "Scene attributes/CHARACTERS/WG101_ASHES_PUPPET_V001"
    fla = FLA("WG101ARRIVAL_Sc001_Clean_V001_ASH")
    N = build_library(fla, P)
    master = build_master(fla, P, N)
    bgs = {}
    for key in ["far", "mid", "near"]:
        bmp = f"Scene attributes/BACKGROUNDS/WG_BG_{key.upper()}"
        fla.add_bitmap(bmp, f"{OUT}/_media/bg_{key}.png")
        sym = f"Scene attributes/BACKGROUNDS/WG_BG_{key.upper()}_PLATE"
        fla.add_symbol(sym, layers_xml(layer("plate", [frame(0, [bmp_inst(bmp, 0, 0)])])))
        bgs[key] = sym
    # shot plan: (frame, master_ff) keys; matrix keys (frame, tx, ty, s)
    ff_keys = [(0,0),(8,1),(10,2),(14,3),(20,4),(26,5),(32,3),(38,6),(40,7),(48,8),(52,12),(58,9),(64,11),(66,10),(68,11)]
    mat_keys = [(0, 560, 196, 0.72), (36, 540, 178, 0.77), (71, 522, 158, 0.81)]
    def interp(f):
        for (f0, *v0), (f1, *v1) in zip(mat_keys, mat_keys[1:]):
            if f0 <= f <= f1:
                t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
                return tuple(a + (b - a) * t for a, b in zip(v0, v1))
        return mat_keys[-1][1:]
    def ff_at(f):
        cur = ff_keys[0][1]
        for kf, ff in ff_keys:
            if f >= kf: cur = ff
        return cur
    char_frames = []
    for f in range(0, 72, 2):
        tx, ty, s = interp(f)
        m = mat_mul(mat_T(tx, ty), mat_S(s, s))
        dur = 2 if f < 70 else 2
        char_frames.append(frame(f, [sym_inst(master, m, (0, 0), firstframe=ff_at(f))], duration=dur))
    def plate_frames(sym, drift, s0, s1):
        out = []
        for f in range(0, 72, 2):
            t = f / 71
            s = s0 + (s1 - s0) * t
            m = mat_mul(mat_T(drift * t, 0), about((960, 540), mat_S(s, s)))
            out.append(frame(f, [sym_inst(sym, m, (0, 0))], duration=2))
        return out
    layers = [
        layer("audio", [frame(0, [], duration=72)], locked=True),
        layer("framecounter", [frame(0, [], duration=72)], guide=True),
        layer("fieldguide", [frame(0, [], duration=72)], guide=True),
        layer("FG_NEAR", plate_frames(bgs["near"], -70, 1.0, 1.05)),
        layer("ASHES", char_frames),
        layer("BG_MID", plate_frames(bgs["mid"], -26, 1.01, 1.07)),
        layer("BG_FAR", plate_frames(bgs["far"], -10, 1.02, 1.08)),
        layer("layout", [frame(0, [], duration=72)], guide=True),
    ]
    fla.document(1920, 1080, 24, timeline("Scene 1", layers),
                 "WG101ARRIVAL_Sc001_Clean_V001_ASH",
                 ["Scene attributes", "Scene attributes/BACKGROUNDS", "Scene attributes/CHARACTERS", P])
    return fla.zip_fla("WG101ARRIVAL_Sc001_Clean_V001_ASH.fla")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("puppet:", build_puppet())
    print("scene:", build_scene())
