"""
THE SHARED PREVIEW SURFACE — one page that shows every agent the actual pixels.

Owner: "make it easier for ChatGPT and Claude and Grok to all show me the
evidence and show me the work just like how you do here... they always tell me
what they can't do, but I know there's a way for stuff in the repo to connect to
the thing to give them abilities."

The repo already had the two halves and nothing joined them: docs/evidence/
carries committed pixels with per-set manifests, and docs/agent-evidence/ defines
a cross-agent contract. Neither was ever RENDERED, so reading it meant opening
JSON by hand -- which is exactly the friction that ends with an agent describing
a render instead of showing it.

This bakes one self-contained page. Data is INLINED, not fetched, so it works
identically on GitHub Pages, as a raw file in a checkout, opened locally from
disk, or handed to an agent that can only read files. No build step, no server,
no CORS, no SaaS.

HONEST BY CONSTRUCTION:
  * a set with no index.json is shown as NO MANIFEST, never as a pass
  * qc.visual PENDING is rendered as PENDING -- it is not folded into PASS
  * an agent manifest naming a file that is missing from the checkout is shown
    struck through and counted as a broken claim

  ./.trippedd_venv/bin/python tools/build_evidence_gallery.py
"""
import json, os, sys, glob, html, hashlib, shutil, subprocess, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EV = os.path.join(ROOT, "docs", "evidence")
MANI = os.path.join(ROOT, "docs", "agent-evidence", "manifests")
OUT = os.path.join(EV, "index.html")
IMG = (".png", ".jpg", ".jpeg", ".webp", ".gif")
VID = (".mp4", ".webm")

def commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"

def read_json(p):
    try: return json.load(open(p))
    except Exception: return None

sets = []
for d in sorted(glob.glob(os.path.join(EV, "*"))):
    if not os.path.isdir(d): continue
    name = os.path.basename(d)
    idx = read_json(os.path.join(d, "index.json"))
    media = sorted([os.path.basename(f) for f in glob.glob(os.path.join(d, "*"))
                    if f.lower().endswith(IMG + VID)])
    if not media and not idx: continue
    qc = (idx or {}).get("qc") or {}
    vis = (qc.get("visual") or {}).get("verdict")
    status = qc.get("status")
    # a set with no manifest asserts NOTHING -- say so rather than inventing a status
    if idx is None:
        status, vis = "NO MANIFEST", None
    frames = {f.get("frame") or f.get("filename"): f for f in (idx or {}).get("frames", [])}
    extra = sorted([os.path.basename(f) for f in glob.glob(os.path.join(d, "*.json"))
                    if os.path.basename(f) != "index.json"])
    sets.append({"name": name, "status": status, "visual": vis, "media": media,
                 "frames": frames, "json": extra,
                 "source": (idx or {}).get("sourceAsset") or {},
                 "checks": ((qc.get("physical") or {}).get("checks") or [])})

claims = []
for f in sorted(glob.glob(os.path.join(MANI, "*.json"))):
    m = read_json(f)
    if not m: continue
    arts = []
    for a in m.get("artifacts", []):
        p = os.path.join(ROOT, a.get("path", ""))
        ok = os.path.isfile(p) and os.path.getsize(p) == a.get("bytes")
        arts.append({**a, "present": ok})
    claims.append({"file": os.path.basename(f), "agent": m.get("agent"),
                   "status": m.get("status"), "commit": (m.get("commit") or "")[:8],
                   "created": m.get("created", ""), "artifacts": arts,
                   "gates": m.get("gates", []), "commands": m.get("commands", []),
                   "notes": m.get("notes", [])})

broken = sum(1 for c in claims for a in c["artifacts"] if not a["present"])
DATA = {"commit": commit(), "built": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "sets": sets, "claims": claims, "brokenClaims": broken}

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mars Evidence Room</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
/* IBM Plex: a superfamily built for technical documentation. This page is mostly
   filenames, sha256 prefixes and millimetre measurements, so the mono face is
   load-bearing, not ornament. The accent is OCHRE on purpose -- every frame on
   this page is intensely blue, and a blue or violet chrome would fight the
   evidence it is framing. */
:root{
  --ground:#f6f5f2; --panel:#ffffff; --sunk:#eceae5;
  --line:#ddd9d1; --line-soft:#e9e6e0;
  --ink:#1b1a17; --ink-dim:#6b675f; --ink-faint:#96918a;
  --accent:#a9691a; --accent-soft:#f2e5d3;
  --pass:#2f6b43; --fail:#a8322b; --idle:#7c7871; --idle-bg:#e9e6e0;
  --shadow:0 1px 2px rgba(30,26,20,.06);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#121316; --panel:#1a1c20; --sunk:#0d0e10;
  --line:#2b2f36; --line-soft:#23262c;
  --ink:#e9ebee; --ink-dim:#98a0ab; --ink-faint:#6d747e;
  --accent:#e2a44e; --accent-soft:#33291a;
  --pass:#5fbd7e; --fail:#e8736a; --idle:#7f8791; --idle-bg:#23262c;
  --shadow:0 1px 2px rgba(0,0,0,.4);
}}
:root[data-theme="dark"]{
  --ground:#121316; --panel:#1a1c20; --sunk:#0d0e10;
  --line:#2b2f36; --line-soft:#23262c;
  --ink:#e9ebee; --ink-dim:#98a0ab; --ink-faint:#6d747e;
  --accent:#e2a44e; --accent-soft:#33291a;
  --pass:#5fbd7e; --fail:#e8736a; --idle:#7f8791; --idle-bg:#23262c;
  --shadow:0 1px 2px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  font-size:15px;line-height:1.55;}
.wrap{max-width:1180px;margin:0 auto;padding-inline:18px;padding-block:28px 72px}
header{border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:22px}
h1{font-size:clamp(22px,4.4vw,30px);line-height:1.12;margin:0 0 8px;
  font-weight:600;letter-spacing:-.02em;text-wrap:balance}
.deck{color:var(--ink-dim);font-size:14px;max-width:62ch;margin:0}
.meta{margin-top:14px;display:flex;flex-wrap:wrap;gap:6px 18px;
  font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:12px;
  color:var(--ink-faint);font-variant-numeric:tabular-nums}
.meta b{color:var(--ink-dim);font-weight:500}
.alarm{color:var(--fail);font-weight:600}
nav{display:flex;gap:4px;margin:20px 0 24px;border-bottom:1px solid var(--line-soft)}
nav button{background:none;border:0;border-bottom:2px solid transparent;color:var(--ink-dim);
  font:inherit;font-size:14px;font-weight:500;padding:8px 2px;margin-right:22px;cursor:pointer}
nav button[aria-pressed=true]{color:var(--ink);border-bottom-color:var(--accent)}
nav button:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}
/* A SEVERITY RAIL, not a card. State reads at a glance from the edge, before
   any label is parsed -- which is the whole job of this surface. */
section{position:relative;background:var(--panel);border:1px solid var(--line-soft);
  border-left:3px solid var(--idle);border-radius:0 6px 6px 0;
  padding:16px 16px 18px;margin-bottom:14px;box-shadow:var(--shadow)}
section[data-s="PASS"]{border-left-color:var(--pass)}
section[data-s="FAIL"]{border-left-color:var(--fail)}
.head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.head h2{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:15px;
  font-weight:600;margin:0;letter-spacing:-.01em}
.tag{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:10.5px;
  font-weight:600;letter-spacing:.06em;text-transform:uppercase;
  padding:2px 7px;border-radius:3px;background:var(--idle-bg);color:var(--idle)}
.tag.PASS{background:none;color:var(--pass);box-shadow:inset 0 0 0 1px currentColor}
.tag.FAIL{color:var(--fail);background:none;box-shadow:inset 0 0 0 1px currentColor}
.n{margin-left:auto;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  font-size:12px;color:var(--ink-faint);font-variant-numeric:tabular-nums}
.why{color:var(--ink-dim);font-size:13.5px;margin:8px 0 0;max-width:68ch}
.grid{display:grid;gap:10px;margin-top:14px;
  grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}
figure{margin:0;border:1px solid var(--line);border-radius:4px;overflow:hidden;
  background:var(--sunk)}
figure img,figure video{width:100%;display:block;background:#000;cursor:zoom-in}
figcaption{padding:6px 8px;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  font-size:10.5px;color:var(--ink-faint);word-break:break-all;line-height:1.4}
.checks{margin-top:14px;border-top:1px solid var(--line-soft)}
.checks div{display:flex;gap:9px;align-items:flex-start;padding:7px 0;
  border-bottom:1px solid var(--line-soft);font-size:13.5px}
.checks .tag{flex:none;margin-top:2px}
.files{margin-top:12px;font-size:12.5px;color:var(--ink-faint);
  font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;word-break:break-all}
.files a{color:var(--accent);text-decoration:none;margin-right:14px}
.files a:hover{text-decoration:underline}
.gates{display:flex;flex-wrap:wrap;gap:5px;margin-top:11px}
.gate{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11.5px;
  padding:3px 8px;border-radius:3px;border:1px solid var(--line);
  color:var(--ink-dim);font-variant-numeric:tabular-nums}
.gate.PASS{border-color:var(--pass);color:var(--pass)}
.gate.FAIL{border-color:var(--fail);color:var(--fail)}
.miss{text-decoration:line-through;color:var(--fail)}
pre{background:var(--sunk);border:1px solid var(--line-soft);border-radius:4px;
  padding:10px;overflow-x:auto;margin:11px 0 0;
  font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11.5px;
  color:var(--ink-dim);line-height:1.6}
.empty{color:var(--ink-dim);font-size:13.5px;max-width:64ch}
.lb{position:fixed;inset:0;background:rgba(10,9,8,.95);display:none;
  align-items:center;justify-content:center;z-index:50;padding:16px;cursor:zoom-out}
.lb.on{display:flex}
.lb img{max-width:100%;max-height:100%;object-fit:contain}
@media(max-width:520px){.grid{grid-template-columns:repeat(auto-fill,minmax(132px,1fr))}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body><div class="wrap">
<header>
  <h1>Mars Evidence Room</h1>
  <p class="deck">Every published frame in the Mars facial pipeline, with the gate
  that judged it. A set with no manifest is shown as <b>no manifest</b>, never as a
  pass &mdash; and an agent claim naming a file missing from the checkout is struck
  through and counted.</p>
  <div class="meta" id="meta"></div>
</header>
<nav id="bar"></nav>
<div id="body"></div>
</div><div class="lb" id="lb"><img id="lbi" alt="Enlarged evidence frame"></div>
<script>const D = __DATA__;</script>
<script>
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;
if(x!==undefined)e.textContent=x;return e};
const rail=s=>s==='PASS'?'PASS':s==='FAIL'||s==='VISUAL_FAIL'?'FAIL':'IDLE';
const tagc=s=>s==='PASS'?'PASS':(s==='FAIL'||s==='VISUAL_FAIL')?'FAIL':'';
const meta=document.getElementById('meta');
[['sets',D.sets.length],['agent claims',D.claims.length],
 ['commit',D.commit],['built',D.built]].forEach(([k,v])=>{
  const s=el('span');s.appendChild(el('b',null,k+' '));
  s.appendChild(document.createTextNode(v));meta.appendChild(s)});
if(D.brokenClaims){const s=el('span','alarm',D.brokenClaims+' broken claim(s)');
  meta.appendChild(s)}
if(D.portable){const s=el('span',null,'downscaled mirror');meta.appendChild(s)}
const lb=document.getElementById('lb'),lbi=document.getElementById('lbi');
lb.onclick=()=>lb.classList.remove('on');
addEventListener('keydown',e=>{if(e.key==='Escape')lb.classList.remove('on')});
function card(s){
 const sec=el('section');sec.dataset.s=rail(s.status);
 const h=el('div','head');
 h.appendChild(el('h2',null,s.name));
 h.appendChild(el('span','tag '+tagc(s.status),(s.status||'—').replace('NO MANIFEST','no manifest')));
 // don't say it twice: a set whose status is VISUAL_FAIL already carries the verdict
 if(s.visual && s.status!=='VISUAL_FAIL')
   h.appendChild(el('span','tag '+tagc(s.visual),'visual '+s.visual));
 h.appendChild(el('span','n',s.media.length+' frames'));
 sec.appendChild(h);
 if(s.status==='NO MANIFEST')
   sec.appendChild(el('p','why','The pixels are committed, but no index.json states '+
     'what they prove. That is NOT_ATTEMPTED, not a pass.'));
 if(s.media.length){
  const g=el('div','grid');
  s.media.forEach(m=>{
   const f=el('figure');const src=s.name+'/'+m;
   if(/\.(mp4|webm)$/i.test(m)){const v=document.createElement('video');
    v.src=src;v.controls=true;v.muted=true;v.loop=true;v.playsInline=true;f.appendChild(v);}
   else{const i=document.createElement('img');i.src=src;i.loading='lazy';i.alt=m;
    i.onclick=()=>{lbi.src=src;lb.classList.add('on')};f.appendChild(i);}
   const d=s.frames[m];
   f.appendChild(el('figcaption',null,m+(d&&d.pose?'  '+d.pose:'')));
   g.appendChild(f);});
  sec.appendChild(g);}
 if(s.checks&&s.checks.length){
  const c=el('div','checks');
  s.checks.forEach(k=>{const d=el('div');
   d.appendChild(el('span','tag '+(k.pass?'PASS':'FAIL'),k.pass?'pass':'fail'));
   d.appendChild(el('span',null,(k.check||'')+(k.detail?' — '+k.detail:'')));
   c.appendChild(d);});
  sec.appendChild(c);}
 if(s.json&&s.json.length){
  const f=el('div','files');f.appendChild(document.createTextNode('measurements  '));
  s.json.forEach(j=>{const a=el('a',null,j);a.href=s.name+'/'+j;f.appendChild(a)});
  sec.appendChild(f);}
 return sec;}
function claimCard(c){
 const sec=el('section');sec.dataset.s=rail(c.status);
 const h=el('div','head');
 h.appendChild(el('h2',null,c.agent));
 h.appendChild(el('span','tag '+tagc(c.status),c.status));
 h.appendChild(el('span','n',c.created+'  '+c.commit));
 sec.appendChild(h);
 if(c.gates.length){const g=el('div','gates');
  c.gates.forEach(x=>{const b=el('span','gate '+tagc(x.result));
   b.textContent=x.name+' = '+x.result+(x.detail?'  ·  '+x.detail:'');g.appendChild(b)});
  sec.appendChild(g);}
 const f=el('div','files');f.appendChild(document.createTextNode('artifacts  '));
 c.artifacts.forEach(a=>{const short=a.path.replace('docs/evidence/','');
  if(a.present){const n=el('a',null,short);n.href=short;f.appendChild(n)}
  else{f.appendChild(el('span','miss',short));
       f.appendChild(document.createTextNode(' missing from checkout  '))}});
 sec.appendChild(f);
 if(c.commands.length)sec.appendChild(el('pre',null,c.commands.join('\n')));
 if(c.notes.length)sec.appendChild(el('p','why',c.notes.join('  ')));
 return sec;}
const views={
 'Evidence':()=>D.sets.map(card),
 'Agent claims':()=>D.claims.length?D.claims.map(claimCard):
   [el('p','empty','No agent has filed a manifest yet. tools/agent_evidence.py '+
     'hashes the bytes itself, so a claim cannot name a file that is not in the '+
     'checkout, and it refuses PASS with no gates.')],
};
const bar=document.getElementById('bar'),body=document.getElementById('body');
function show(k){body.innerHTML='';views[k]().forEach(n=>body.appendChild(n));
 [...bar.children].forEach(b=>b.setAttribute('aria-pressed',String(b.textContent===k)))}
Object.keys(views).forEach(k=>{const b=el('button',null,k);
 b.type='button';b.onclick=()=>show(k);bar.appendChild(b)});
show('Evidence');
</script></body></html>"""

def write(path, data):
    open(path, "w").write(PAGE.replace("__DATA__", json.dumps(data)))

write(OUT, DATA)

# ---- PORTABLE COPY, for anywhere the repo tree is not reachable --------------
# docs/evidence is 106 MB across 138 files, past what a hosted preview accepts.
# --portable writes a downscaled mirror plus the same page, so the surface can be
# handed to someone on a phone or to an agent that cannot clone. It is a MIRROR,
# never the record: the committed originals stay full resolution and the manifest
# hashes still refer to them.
if "--portable" in sys.argv:
    dest = sys.argv[sys.argv.index("--portable") + 1]
    from PIL import Image
    MAXPX = 900
    os.makedirs(dest, exist_ok=True)
    # PNG IS THE WRONG FORMAT FOR A PHOTOGRAPHIC MIRROR. Measured: the same frames
    # at 900 px come to 66 MB as PNG and a fraction of that as JPEG, and the limit
    # that matters is the hosted one. The committed originals stay PNG.
    n_img = n_json = 0
    D2sets = []
    for s_ in sets:
        os.makedirs(os.path.join(dest, s_["name"]), exist_ok=True)
        media2, frames2 = [], {}
        for m in s_["media"]:
            src = os.path.join(EV, s_["name"], m)
            if m.lower().endswith(IMG):
                out_name = os.path.splitext(m)[0] + ".jpg"
                im = Image.open(src)
                if max(im.size) > MAXPX:
                    r = MAXPX / max(im.size)
                    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))),
                                   Image.LANCZOS)
                im.convert("RGB").save(os.path.join(dest, s_["name"], out_name),
                                       "JPEG", quality=86, optimize=True, progressive=True)
            else:
                out_name = m
                shutil.copy2(src, os.path.join(dest, s_["name"], out_name))
            media2.append(out_name)
            if m in s_["frames"]: frames2[out_name] = s_["frames"][m]
            n_img += 1
        D2sets.append({**s_, "media": media2, "frames": frames2})
        for j in s_["json"]:
            shutil.copy2(os.path.join(EV, s_["name"], j), os.path.join(dest, s_["name"], j))
            n_json += 1
    D2 = dict(DATA); D2["sets"] = D2sets
    D2["portable"] = ("Downscaled mirror at %d px for portability. The committed originals "
                      "in docs/evidence/ are full resolution PNG and are what the "
                      "manifest hashes refer to." % MAXPX)
    write(os.path.join(dest, "index.html"), D2)
    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(dest) for f in fs)
    print("portable -> %s  (%d images, %d measurement files, %.1f MB)"
          % (dest, n_img, n_json, total / 1048576))
print("gallery -> %s  (%.0f KB)" % (os.path.relpath(OUT, ROOT), os.path.getsize(OUT) / 1024))
for s in sets:
    print("  %-13s %-12s %s%3d file(s)"
          % (s["name"], s["status"] or "-",
             ("visual %-8s " % s["visual"]) if s["visual"] else " " * 16, len(s["media"])))
print("  %d agent claim(s), %d broken" % (len(claims), broken))
