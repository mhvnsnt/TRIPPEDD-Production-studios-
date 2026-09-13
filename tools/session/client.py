"""Talk to the live Blender session. No launch, no reload.

    python tools/session/client.py ping
    python tools/session/client.py scene
    python tools/session/client.py exec "import bpy; print(len(bpy.data.objects))"
    python tools/session/client.py exec-file tools/session/snippets/mouth_inspect.py

Importable too:  from client import send;  send("get_scene_info")
"""
import json, socket, sys, os

def send(cmd, params=None, port=None, timeout=300.0):
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
        raise RuntimeError("session closed before a complete reply")
    finally:
        s.close()

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    port = None
    if "--port" in sys.argv:
        port = sys.argv[sys.argv.index("--port") + 1]
    if not a:
        print(__doc__); return 2
    cmd = a[0]
    if cmd == "ping":
        send("get_scene_info", port=port); print("session alive"); return 0
    if cmd == "scene":
        r = send("get_scene_info", port=port)
    elif cmd == "exec":
        r = send("execute_code", {"code": a[1]}, port=port)
    elif cmd == "exec-file":
        r = send("execute_code", {"code": open(a[1]).read()}, port=port)
    elif cmd == "object":
        r = send("get_object_info", {"name": a[1]}, port=port)
    else:
        r = send(cmd, json.loads(a[1]) if len(a) > 1 else {}, port=port)
    out = r.get("result", r)
    print(out if isinstance(out, str) else json.dumps(out, indent=2)[:20000])
    return 0 if r.get("status") == "success" else 1

if __name__ == "__main__":
    raise SystemExit(main())
