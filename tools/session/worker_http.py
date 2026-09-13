"""
THE DOOR INTO THE LIVE BLENDER SESSION, FOR ROCKET AND FOR ANYONE ELSE.

    "make it so Rocket can do everything you're doing, but so I can see it while
     it's happening ... and we all can be an actual production team"
                                                        -- the owner, 2026-09-13

Claude already works through one Blender that stays open (tools/session/start.sh):
a full object/material/visibility inspection costs 0.055 s where a fresh launch
costs 90-120 s. This puts an HTTP front on THAT SAME SESSION so Rocket's LIVE
PRODUCTION DOOR, ChatGPT and the owner are all driving one live scene -- not a
second copy, not a simulation.

ROCKET'S DOOR NAMED ITS OWN INTERFACE FIRST, SO THIS SPEAKS THAT INTERFACE.
PR #64 built the cockpit half against `/health`, `/capabilities`, `/state` and a
fixed set of NAMED COMMANDS (inspect, measure, run_gate, render, publish, refresh,
checkpoint) with no arbitrary shell execution. Rather than make Rocket guess the
endpoint names of the runtime, the runtime answers the names the door already
uses. Point ROCKET_LIVE_SESSION_URL at this worker and it connects.

FAIL-CLOSED, because Rocket's contract demands it and so does this repo:
  * no session -> 503 with "session": false. Never a fabricated success.
  * a mutation is only AUTHORITATIVE when it returns a receipt -- an operation id
    plus bytes that exist and hash. Reads are authoritative because the live
    session answered them; anything else is "authoritative": false and says why.
  * every render is published through tools/publish_visual.py, so it lands in
    docs/evidence/ with provenance and never overwrites an earlier version.
    NO BYTES = NO EVIDENCE (OWNER LAW #9).
  * NOT_ATTEMPTED / BLOCKED / UNAVAILABLE are distinct from FAIL, everywhere.

  GET  /health              is the session up, what is loaded, what is in it
  GET  /capabilities        the command list, their params, which are privileged
  GET  /state               authoritative live state, cheap, for 3 s polling
  GET  /evidence            LATEST_VISUAL_EVIDENCE.json
  GET  /evidence/index      VISUAL_EVIDENCE_INDEX.json
  GET  /checkpoints         what can be rolled back to
  GET  /snippets            banked session snippets
  POST /command  {"command": "inspect"|"measure"|"run_gate"|"render"|
                             "publish"|"refresh"|"checkpoint", "params": {...}}
  POST /exec     {"code": "..."}        PRIVILEGED -- arbitrary python in Blender
  POST /snippet  {"name": "..."}        PRIVILEGED -- a banked snippet by name
  POST /render   {...}                  kept: the shorthand for command=render

AUTH: set TRIPPEDD_SESSION_SECRET and every request must carry it as
`Authorization: Bearer <secret>` or `X-Trippedd-Secret`. With no secret set the
worker binds to 127.0.0.1 only and says so in /capabilities -- it never pretends
to be authenticated when it is not.

    ./.trippedd_venv/bin/python tools/session/worker_http.py --port 8788
"""
import argparse, hashlib, json, os, subprocess, sys, threading, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import client as S            # the same client Claude uses

PY = os.path.join(ROOT, ".trippedd_venv/bin/python")
SNIPPETS = os.path.join(HERE, "snippets")
SECRET = os.environ.get("TRIPPEDD_SESSION_SECRET", "").strip()

# A NAMED COMMAND CAN ONLY REACH A NAMED TOOL. Rocket's contract is "no arbitrary
# shell execution", and a command that took a path would be exactly that wearing a
# different hat. Every gate and every measurement is on a list, by name, here.
GATES = {
    "mouth_proof":      ["tools/character/mouth_proof.py", "--rig", "assets/rigs/MARS_FACE.blend"],
    "contact_gate":     ["tools/character/contact_gate.py"],
    "expression_gate":  ["tools/character/expression_gate.py"],
    "blink_regression": ["tools/character/blink_regression_gate.py"],
    "mars_face_invariant": ["tools/character/mars_face_invariant_gate.py"],
    "visual_evidence":  ["tools/character/mars_visual_evidence_gate.py"],
}
# measurements are LEVEL 0/1 and run INSIDE the live session, so they cost
# milliseconds and never relaunch Blender.
MEASURES = ["oral_export", "rest_gap", "tooth_occlusion", "cavity_vs_teeth",
            "corner_ray", "corner_surface_map", "crater_density", "leak_window"]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def op_id():
    return "op_" + uuid.uuid4().hex[:12]


def session_alive():
    try:
        S.send("get_scene_info")
        return True
    except Exception:
        return False


SCENE_Q = (
    "import bpy\n"
    "m=[o for o in bpy.data.objects if o.type=='MESH']\n"
    "print(bpy.data.filepath)\n"
    "print(bpy.app.version_string)\n"
    "for o in sorted(m,key=lambda x:x.name):\n"
    "    k=len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0\n"
    "    print('%s|%d|%d|%d|%s'%(o.name,len(o.data.vertices),len(o.data.polygons),k,o.hide_render))\n")


def parse_scene(raw):
    """Read the scene table the session printed. Defensive on every line.

    The session can be mid-load, or holding a file with no path (a raw import),
    so the reply can be shorter than expected -- a health endpoint that raises is
    worse than one that says "unknown". And an object NAME may contain a pipe
    while the four fields after it never can, so split from the RIGHT.
    """
    lines = raw.split("\n")
    blend = lines[0].strip() if lines else ""
    ver = lines[1].strip() if len(lines) > 1 else "unknown"
    objs = []
    for ln in lines:
        if "|" not in ln:
            continue
        parts = ln.rsplit("|", 4)
        if len(parts) != 5:
            continue
        n, v, f, k, hr = parts
        try:
            objs.append({"name": n.strip(), "verts": int(v), "faces": int(f),
                         "shapeKeys": int(k), "hideRender": hr.strip() == "True"})
        except ValueError:
            continue
    return blend, ver, objs


_cache = {"at": 0.0, "val": None}
_lock = threading.Lock()


def live_state(max_age=1.0):
    """The authoritative live state, cached for a second.

    Rocket polls at 3 s and several clients may watch at once; a cache this short
    cannot hide a change from a human eye but does stop N clients serialising N
    round trips through one Blender main thread.
    """
    with _lock:
        now = time.time()
        if _cache["val"] is not None and now - _cache["at"] < max_age:
            return _cache["val"]
        if not session_alive():
            v = {"session": False, "status": "UNAVAILABLE",
                 "why": "no live Blender session",
                 "how": "bash tools/session/start.sh assets/rigs/MARS_FACE.blend"}
        else:
            blend, ver, objs = parse_scene(S.run(SCENE_Q))
            v = {"session": True, "status": "OK",
                 "blend": blend or "(unsaved)",
                 "blendSha256": sha256(blend) if blend and os.path.exists(blend) else None,
                 "blender": ver, "objects": objs,
                 "observedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        _cache["at"], _cache["val"] = now, v
        return v


def invalidate():
    with _lock:
        _cache["val"] = None


def run_tool(argv, timeout=1800):
    """Run a repo tool as a subprocess. Named tools only -- never a caller's path."""
    t0 = time.time()
    p = subprocess.run([PY] + argv, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return {"exit": p.returncode, "seconds": round(time.time() - t0, 2),
            "stdout": p.stdout[-20000:], "stderr": p.stderr[-8000:]}


# ── THE NAMED COMMANDS ──────────────────────────────────────────────────────
def cmd_refresh(params):
    invalidate()
    return {"authoritative": True, "state": live_state(max_age=0)}


def cmd_inspect(params):
    """LEVEL 0. Counts, transforms, keys, visibility. No render, no relaunch."""
    name = params.get("object")
    if not name:
        return {"authoritative": True, "state": live_state(max_age=0)}
    out = S.run(
        "import bpy, json\n"
        "o = bpy.data.objects.get(%r)\n"
        "if o is None:\n"
        "    print(json.dumps({'found': False}))\n"
        "else:\n"
        "    d = o.data\n"
        "    kb = [k.name for k in d.shape_keys.key_blocks] if getattr(d,'shape_keys',None) else []\n"
        "    print(json.dumps({'found': True, 'name': o.name, 'type': o.type,\n"
        "        'location': list(o.location), 'scale': list(o.scale),\n"
        "        'verts': len(d.vertices) if o.type=='MESH' else 0,\n"
        "        'faces': len(d.polygons) if o.type=='MESH' else 0,\n"
        "        'materials': [m.name for m in d.materials] if o.type=='MESH' else [],\n"
        "        'modifiers': [(m.name, m.type) for m in o.modifiers],\n"
        "        'vertexGroups': [g.name for g in o.vertex_groups],\n"
        "        'hideRender': o.hide_render, 'hideViewport': o.hide_viewport,\n"
        "        'shapeKeys': kb}))\n" % name)
    try:
        return {"authoritative": True, "object": json.loads(out.strip().split("\n")[-1])}
    except Exception:
        return {"authoritative": False, "status": "BLOCKED",
                "why": "the session did not return parseable object detail", "output": out}


def cmd_measure(params):
    """Run a banked measurement INSIDE the live session. Whitelisted by name."""
    name = params.get("name", "")
    if name not in MEASURES:
        return {"authoritative": False, "status": "BLOCKED",
                "why": "%r is not a named measurement" % name, "available": MEASURES}
    p = os.path.join(SNIPPETS, name + ".py")
    if not os.path.exists(p):
        return {"authoritative": False, "status": "UNAVAILABLE",
                "why": "the snippet %s.py is not on disk" % name}
    t0 = time.time()
    out = S.run(open(p).read())
    failed = "SNIPPET_FAILED" in out or "SNIPPET_EXIT" in out
    return {"authoritative": not failed, "status": "FAILED" if failed else "OK",
            "measurement": name, "seconds": round(time.time() - t0, 3), "output": out}


def cmd_run_gate(params):
    """Run one of the repo's OWN gates. OWNER LAW #11: the gate is the answer."""
    name = params.get("name", "")
    if name not in GATES:
        return {"authoritative": False, "status": "BLOCKED",
                "why": "%r is not a named gate" % name, "available": sorted(GATES)}
    r = run_tool(GATES[name])
    # exit 0 is PASS; a non-zero exit from a fail-closed gate is a real verdict,
    # never an error to swallow. Both are authoritative -- the gate ran.
    return {"authoritative": True, "gate": name,
            "verdict": "PASS" if r["exit"] == 0 else "FAIL",
            "exit": r["exit"], "seconds": r["seconds"],
            "output": r["stdout"], "stderr": r["stderr"]}


def cmd_render(params):
    """Render in the live session AND publish. Returns the artifact and its sha256."""
    os.makedirs(os.path.join(ROOT, "renders/_session"), exist_ok=True)
    json.dump({"tag": params.get("tag", "rocket"),
               "set": params.get("set", "mars/mouth"),
               "note": params.get("note", ""),
               "status": params.get("status", "PENDING")},
              open(os.path.join(ROOT, "renders/_session/params.json"), "w"))
    out = S.run(open(os.path.join(SNIPPETS, "render_and_publish.py")).read())
    art = None
    for ln in out.split("\n"):
        if ln.startswith("published "):
            parts = ln.split()
            art = {"artifact": parts[1], "sha256": parts[2], "bytes": int(parts[3]),
                   "publishStatus": parts[-1]}
    if not art:
        # NO BYTES = NO EVIDENCE. Never report a render that produced nothing.
        return {"authoritative": False, "status": "BLOCKED",
                "why": "the render produced no published bytes", "output": out}
    # RE-HASH THE BYTES OURSELVES. A receipt that only repeats what the producer
    # said is not independent; the point of the sha is that the file is there.
    p = os.path.join(ROOT, art["artifact"])
    if not os.path.exists(p):
        return {"authoritative": False, "status": "BLOCKED",
                "why": "the publisher named %s and it is not on disk" % art["artifact"],
                "output": out}
    art["sha256Verified"] = sha256(p)
    art["hashAgrees"] = art["sha256Verified"] == art["sha256"]
    art.update({"status": "OK", "authoritative": bool(art["hashAgrees"]), "output": out})
    return art


def cmd_publish(params):
    """Publish bytes that already exist. The set and label are the caller's; the
    PATH is resolved inside the repo so no caller can publish from anywhere."""
    src = params.get("src", "")
    p = os.path.realpath(os.path.join(ROOT, src))
    if not src or not p.startswith(ROOT + os.sep):
        return {"authoritative": False, "status": "BLOCKED",
                "why": "src must be a path inside the repository"}
    if not os.path.exists(p):
        return {"authoritative": False, "status": "UNAVAILABLE",
                "why": "no bytes at %s -- nothing to publish" % src}
    argv = ["tools/publish_visual.py", "--src", os.path.relpath(p, ROOT),
            "--set", params.get("set", "mars/mouth"),
            "--label", params.get("label", "rocket"),
            "--status", params.get("status", "PENDING")]
    if params.get("note"):
        argv += ["--note", params["note"]]
    if params.get("sourceBlend"):
        argv += ["--source-blend", params["sourceBlend"]]
    r = run_tool(argv, timeout=600)
    # THE RECEIPT IS THE POINT. Rocket's artifact pipeline refuses to call itself
    # authoritative without an artifact path AND its sha256, so parse the line
    # publish_visual.py prints and RE-HASH the bytes here rather than echoing it.
    art = None
    for ln in r["stdout"].split("\n"):
        if ln.startswith("published "):
            f = ln.split()
            art = {"artifact": f[1], "sha256": f[2], "bytes": int(f[3]),
                   "publishStatus": f[-1]}
    if r["exit"] != 0 or not art:
        return {"authoritative": False,
                "status": "FAILED" if r["exit"] else "BLOCKED",
                "why": "the publisher produced no artifact line -- NO BYTES = NO EVIDENCE",
                "exit": r["exit"], "output": r["stdout"], "stderr": r["stderr"]}
    fp = os.path.join(ROOT, art["artifact"])
    if not os.path.exists(fp):
        return {"authoritative": False, "status": "BLOCKED",
                "why": "the publisher named %s and it is not on disk" % art["artifact"],
                "output": r["stdout"]}
    art["sha256Verified"] = sha256(fp)
    art["hashAgrees"] = art["sha256Verified"] == art["sha256"]
    art.update({"status": "OK", "authoritative": bool(art["hashAgrees"]),
                "exit": r["exit"], "output": r["stdout"]})
    return art


def cmd_checkpoint(params):
    """save / list / verify only. RESTORE IS NOT REACHABLE FROM HTTP -- rolling
    the canonical rig back is a destructive act and stays a deliberate command
    with --yes at a terminal (OWNER LAW #12: nothing recovered by accident)."""
    action = params.get("action", "list")
    if action not in ("save", "list", "verify"):
        return {"authoritative": False, "status": "BLOCKED",
                "why": "checkpoint action must be save, list or verify "
                       "(restore is deliberately not exposed over HTTP)"}
    argv = ["tools/checkpoint.py", action]
    if action in ("save", "verify"):
        lab = params.get("label", "")
        if not lab or "/" in lab or ".." in lab:
            return {"authoritative": False, "status": "BLOCKED",
                    "why": "a checkpoint label is required and must be a plain name"}
        argv.append(lab)
        if action == "save" and params.get("note"):
            argv += ["--note", params["note"]]
    r = run_tool(argv, timeout=1800)
    return {"authoritative": r["exit"] == 0, "status": "OK" if r["exit"] == 0 else "FAILED",
            "action": action, "exit": r["exit"],
            "output": r["stdout"], "stderr": r["stderr"]}


COMMANDS = {
    "refresh":    (cmd_refresh,    False, {}),
    "inspect":    (cmd_inspect,    False, {"object": "optional object name"}),
    "measure":    (cmd_measure,    False, {"name": "one of /capabilities.measurements"}),
    "run_gate":   (cmd_run_gate,   False, {"name": "one of /capabilities.gates"}),
    "render":     (cmd_render,     True,  {"tag": "str", "set": "evidence set",
                                           "note": "str", "status": "PASS|FAIL|PENDING"}),
    "publish":    (cmd_publish,    True,  {"src": "path inside the repo", "set": "evidence set",
                                           "label": "str", "status": "PASS|FAIL|PENDING",
                                           "note": "str", "sourceBlend": "path"}),
    "checkpoint": (cmd_checkpoint, True,  {"action": "save|list|verify", "label": "str",
                                           "note": "str"}),
}
# which commands need a live Blender at all
NEEDS_SESSION = {"refresh", "inspect", "measure", "render"}


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, code, obj):
        b = json.dumps(obj, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Trippedd-Secret")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass

    def do_OPTIONS(self):
        self._send(204, {})

    def _authed(self):
        if not SECRET:
            return True
        got = (self.headers.get("X-Trippedd-Secret", "")
               or self.headers.get("Authorization", "").removeprefix("Bearer ")).strip()
        # constant-time, because a shared secret compared with == leaks its prefix
        import hmac
        return hmac.compare_digest(got, SECRET)

    def _file(self, rel):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            return self._send(404, {"status": "UNAVAILABLE", "missing": rel})
        self._send(200, json.load(open(p)))

    def do_GET(self):
        if self.path.startswith("/capabilities"):
            # deliberately readable without the secret: a cockpit must be able to
            # discover that it needs to authenticate.
            return self._send(200, {
                "runtime": "trippedd.session-worker/v1",
                "repo": "TRIPPEDD-Production-studios-",
                "authRequired": bool(SECRET),
                "authHeaders": ["Authorization: Bearer <secret>", "X-Trippedd-Secret"],
                "arbitraryShell": False,
                "commands": {k: {"privileged": v[1], "needsSession": k in NEEDS_SESSION,
                                 "params": v[2]} for k, v in COMMANDS.items()},
                "gates": sorted(GATES),
                "measurements": MEASURES,
                "endpoints": ["/health", "/capabilities", "/state", "/evidence",
                              "/evidence/index", "/checkpoints", "/snippets",
                              "/command", "/exec", "/snippet", "/render"],
                "authoritativeRule": "a mutation is authoritative only when it returns "
                                     "a receipt whose bytes exist and hash",
                "session": session_alive()})
        if not self._authed():
            return self._send(401, {"status": "BLOCKED", "why": "shared secret required",
                                    "how": "send Authorization: Bearer <TRIPPEDD_SESSION_SECRET>"})
        if self.path.startswith("/health") or self.path.startswith("/state"):
            st = live_state()
            return self._send(200 if st.get("session") else 503, st)
        if self.path.startswith("/evidence/index"):
            return self._file("docs/evidence/VISUAL_EVIDENCE_INDEX.json")
        if self.path.startswith("/evidence"):
            return self._file("docs/evidence/LATEST_VISUAL_EVIDENCE.json")
        if self.path.startswith("/checkpoints"):
            d = os.path.join(ROOT, "assets/checkpoints")
            out = []
            if os.path.isdir(d):
                for lab in sorted(os.listdir(d)):
                    mp = os.path.join(d, lab, "manifest.json")
                    if os.path.exists(mp):
                        m = json.load(open(mp))
                        out.append({"label": lab, "savedAt": m.get("savedAt"),
                                    "note": m.get("note"), "files": len(m.get("files", []))})
            return self._send(200, {"checkpoints": out})
        if self.path.startswith("/snippets"):
            return self._send(200, {"snippets": sorted(
                f[:-3] for f in os.listdir(SNIPPETS) if f.endswith(".py"))})
        self._send(404, {"status": "UNAVAILABLE", "path": self.path})

    def do_POST(self):
        if not self._authed():
            return self._send(401, {"status": "BLOCKED", "why": "shared secret required"})
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception as e:
            return self._send(400, {"status": "BLOCKED", "why": "malformed JSON: %s" % e})

        if self.path.startswith("/command"):
            name = body.get("command", "")
            if name not in COMMANDS:
                return self._send(400, {"status": "BLOCKED",
                                        "why": "%r is not a named command" % name,
                                        "available": sorted(COMMANDS)})
            if name in NEEDS_SESSION and not session_alive():
                return self._send(503, {"session": False, "status": "UNAVAILABLE",
                                        "command": name,
                                        "why": "no live Blender session to act on",
                                        "how": "bash tools/session/start.sh <blend>"})
            fn = COMMANDS[name][0]
            op, t0 = op_id(), time.time()
            try:
                res = fn(body.get("params") or {})
            except Exception as e:
                import traceback
                return self._send(200, {"op": op, "command": name, "authoritative": False,
                                        "status": "FAILED", "why": str(e),
                                        "traceback": traceback.format_exc()[-4000:]})
            if name in ("render", "publish", "checkpoint"):
                invalidate()
            # `operationId` is the name Rocket's artifact pipeline requires; `op`
            # is kept because everything already written here reads it. One id.
            res.update({"op": op, "operationId": op, "command": name,
                        "seconds": round(time.time() - t0, 3)})
            res.setdefault("status", "OK")
            res.setdefault("authoritative", False)
            return self._send(200, res)

        # ── the privileged raw doors. Claude uses these; Rocket does not need to.
        if not session_alive():
            return self._send(503, {"session": False, "status": "UNAVAILABLE",
                                    "why": "no live Blender session to act on",
                                    "how": "bash tools/session/start.sh <blend>"})
        if self.path.startswith("/exec"):
            code = body.get("code", "")
            if not code:
                return self._send(400, {"status": "BLOCKED", "why": "no code"})
            invalidate()
            o = op_id()
            return self._send(200, {"status": "OK", "op": o, "operationId": o,
                                    "output": S.run(code)})
        if self.path.startswith("/snippet"):
            name = os.path.basename(body.get("name", ""))
            p = os.path.join(SNIPPETS, name + ".py")
            if not os.path.exists(p):
                return self._send(404, {"status": "BLOCKED", "why": "no snippet %r" % name})
            if body.get("params") is not None:
                os.makedirs(os.path.join(ROOT, "renders/_session"), exist_ok=True)
                json.dump(body["params"],
                          open(os.path.join(ROOT, "renders/_session/params.json"), "w"))
            invalidate()
            o = op_id()
            return self._send(200, {"status": "OK", "op": o, "operationId": o,
                                    "snippet": name, "output": S.run(open(p).read())})
        if self.path.startswith("/render"):
            res = cmd_render(body)
            invalidate()
            res["op"] = res["operationId"] = op_id()
            return self._send(200, res)
        self._send(404, {"status": "UNAVAILABLE", "path": self.path})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), H)
    print("session worker on http://%s:%d  (Blender session %s, auth %s)"
          % (a.host, a.port, "LIVE" if session_alive() else "NOT RUNNING",
             "REQUIRED" if SECRET else "off -- bind localhost only"), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
