"""Registers the upstream addon and starts its socket server, then hands control
back to Blender's event loop -- which is the whole point: the timers that execute
commands on the main thread only fire while that loop is running.

TWO THINGS THIS HAS TO GET RIGHT, BOTH LEARNED THE EXPENSIVE WAY.

1. **addon.register() AUTO-STARTS A SERVER ON 9876 BEFORE ANYONE SETS THE PORT.**
   `register()` reads `scene.blendermcp_port`, which is still at its default when
   it runs, builds a BlenderMCPServer on 9876 and starts it. Setting the scene
   property afterwards and calling `blendermcp.start_server()` then finds
   `bpy.types.blendermcp_server` ALREADY EXISTS and merely calls `.start()` on the
   same 9876 object again. So a SECOND session can never reach its own port: it
   prints "Failed to start server: [Errno 98] Address already in use" and carries
   on. The server object has to be stopped and REBUILT on the requested port.

2. **A BOOT THAT PRINTS READY WITHOUT BINDING IS THE STALE-SERVER BUG.** That is
   exactly what happened: `SESSION_READY port=9877` was printed by a Blender whose
   socket was never bound, so every later call to 9877 came back
   ConnectionRefused -- which reads like the session was never started rather than
   like a port collision. NEVER CONFLATE NOT DONE WITH DONE AND EMPTY: this now
   CONNECTS to the port and speaks to it before it will say READY.
"""
import bpy, sys, os, socket, json, time

ROOT = os.environ.get("TRIPPEDD_ROOT", os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "vendor/blender-mcp/src/blender_mcp/bundled"))
import addon

PORT = int(os.environ.get("TRIPPEDD_SESSION_PORT", "9876"))


def fail(why):
    print("SESSION_BOOT_FAIL %s" % why, flush=True)
    raise SystemExit(1)


try:
    addon.register()
except Exception as e:
    fail("register: %s" % e)

# Whatever register() auto-started, take it down and rebuild it on OUR port.
srv = getattr(bpy.types, "blendermcp_server", None)
if srv is not None:
    try:
        srv.stop()
    except Exception:
        pass
    try:
        del bpy.types.blendermcp_server
    except Exception:
        pass

try:
    bpy.context.scene.blendermcp_port = PORT
except Exception:
    pass
try:
    bpy.types.blendermcp_server = addon.BlenderMCPServer(port=PORT)
    bpy.types.blendermcp_server.start()
except Exception as e:
    fail("start_server on %d: %s" % (PORT, e))

if not getattr(bpy.types.blendermcp_server, "running", False):
    fail("the server object on %d reports running=False" % PORT)

# ── AND PROVE IT. A bound socket that answers is the only evidence that counts.
ok, why = False, "no reply"
for _ in range(20):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("localhost", PORT))
        s.close()
        ok = True
        break
    except Exception as e:
        why = str(e)
        time.sleep(0.25)
if not ok:
    fail("nothing is listening on %d after start (%s)" % (PORT, why))

print("SESSION_READY port=%d blend=%s" % (PORT, bpy.data.filepath), flush=True)
