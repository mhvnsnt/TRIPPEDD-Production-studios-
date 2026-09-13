"""Talk to the live Blender session. No launch, no reload.

    python tools/session/client.py ping
    python tools/session/client.py scene
    python tools/session/client.py exec "import bpy; print(len(bpy.data.objects))"
    python tools/session/client.py exec-file tools/session/snippets/<snippet>.py

Importable too:  from client import send;  send("get_scene_info")
"""
import json, socket, sys, os

# ── A WORKER OPERATION MUST NEVER BE ABLE TO KILL THE WORKER ────────────────
# execute_code runs inside Blender's OWN interpreter, so a bare SystemExit --
# from a snippet's fail-closed guard, or from any library that calls sys.exit()
# -- takes Blender down with it. The next call then returns
# ConnectionRefusedError, which reads exactly like the session was never started
# rather than like a guard firing. That has now cost time twice.
#
# So every snippet is wrapped here, at the one place all of them pass through:
# SystemExit and every other exception become a STRUCTURED FAILURE printed back
# to the caller, and the session stays alive. A snippet's own `return` still
# works, because the wrap is a function.
_HEAD = "import traceback as _tb\ndef _trippedd_op():\n"
_TAIL = (
    "\ntry:\n"
    "    _trippedd_op()\n"
    "except SystemExit as _e:\n"
    "    print('SNIPPET_EXIT code=%s -- the session is still alive' % (_e.code,))\n"
    "except Exception:\n"
    "    print('SNIPPET_FAILED')\n"
    "    print(_tb.format_exc())\n"
)


def guard(code):
    """Indent the snippet into a function so nothing inside it can reach Blender."""
    body = "\n".join(("    " + ln if ln.strip() else ln) for ln in code.split("\n"))
    return _HEAD + body + "\n" + _TAIL


def send(cmd, params=None, port=None, timeout=600.0):
    port = int(port or os.environ.get("TRIPPEDD_SESSION_PORT", "9876"))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(("localhost", port))
    try:
        s.sendall(json.dumps({"type": cmd, "params": params or {}}).encode())
        chunks = []
        while True:
            c = s.recv(8192)
            if not c:
                break
            chunks.append(c)
            try:
                return json.loads(b"".join(chunks).decode())
            except json.JSONDecodeError:
                continue
        raise RuntimeError("the session closed before a complete reply -- it may have died")
    finally:
        s.close()


def unwrap(r):
    """Peel the addon's reply down to the text the snippet actually printed.

    THE ADDON NESTS ITS RESULT TWICE. blender-mcp answers

        {"status": "success", "result": {"executed": true, "result": "<printed>"}}

    so `r.get("result")` is a DICT, and stringifying it hands every caller a JSON
    envelope that merely CONTAINS the answer -- with the real newlines escaped to
    \n, so every line-oriented parser downstream sees exactly one line and reports
    an empty scene. The /health endpoint printed the whole scene table inside a
    single "blend" string for precisely this reason. Peel while the payload is a
    dict carrying a "result".
    """
    out = r.get("result", r) if isinstance(r, dict) else r
    seen = 0
    while isinstance(out, dict) and "result" in out and seen < 8:
        out = out["result"]
        seen += 1
    return out if isinstance(out, str) else json.dumps(out)


def run(code, port=None):
    """Run guarded code and return its printed output as a string."""
    return unwrap(send("execute_code", {"code": guard(code)}, port=port))


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else None
    if not a:
        print(__doc__)
        return 2
    cmd = a[0]
    if cmd == "ping":
        send("get_scene_info", port=port)
        print("session alive")
        return 0
    if cmd == "scene":
        r = send("get_scene_info", port=port)
    elif cmd == "exec":
        r = send("execute_code", {"code": guard(a[1])}, port=port)
    elif cmd == "exec-file":
        r = send("execute_code", {"code": guard(open(a[1]).read())}, port=port)
    elif cmd == "object":
        r = send("get_object_info", {"name": a[1]}, port=port)
    else:
        r = send(cmd, json.loads(a[1]) if len(a) > 1 else {}, port=port)
    out = unwrap(r)
    print(out[:20000])
    if "SNIPPET_FAILED" in out or "SNIPPET_EXIT" in out:
        return 1
    return 0 if r.get("status") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
