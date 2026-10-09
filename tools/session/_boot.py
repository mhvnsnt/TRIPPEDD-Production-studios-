"""Registers the upstream addon and starts its socket server, then hands control
back to Blender's event loop -- which is the whole point: the timers that execute
commands on the main thread only fire while that loop is running."""
import bpy, sys, os
ROOT = os.environ.get("TRIPPEDD_ROOT", os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "vendor/blender-mcp/src/blender_mcp/bundled"))
import addon
try:
    addon.register()
except Exception as e:
    print("SESSION_BOOT_FAIL register: %s" % e, flush=True)
    raise
port = int(os.environ.get("TRIPPEDD_SESSION_PORT", "9876"))
try:
    bpy.context.scene.blendermcp_port = port
except Exception:
    pass
try:
    bpy.ops.blendermcp.start_server()
except Exception as e:
    print("SESSION_BOOT_FAIL start_server: %s" % e, flush=True)
    raise
print("SESSION_READY port=%d blend=%s" % (port, bpy.data.filepath), flush=True)
