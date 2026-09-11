"""Mars head preparation helpers for Blender.

Creates a non-destructive control scaffold: collection organization,
measurement empties, facial-control placeholders, and a turntable camera.
It does not alter the source mesh or invent facial geometry.
"""
import bpy, math

ROOT="MARS_CANONICAL"
for path in [ROOT, ROOT+"/SOURCE", ROOT+"/RIG", ROOT+"/FACE_CONTROLS", ROOT+"/RENDER"]:
    parts=path.split("/")
    parent=bpy.context.scene.collection
    for part in parts:
        col=bpy.data.collections.get(part)
        if not col:
            col=bpy.data.collections.new(part)
            parent.children.link(col)
        parent=col

controls=bpy.data.collections["FACE_CONTROLS"]
for name in [
    "CTRL_JAW_OPEN","CTRL_MOUTH_SMILE","CTRL_MOUTH_FROWN",
    "CTRL_EYE_BLINK_L","CTRL_EYE_BLINK_R","CTRL_BROW_L","CTRL_BROW_R",
    "CTRL_HEAD_YAW","CTRL_HEAD_PITCH","CTRL_HEAD_ROLL"
]:
    if name not in bpy.data.objects:
        o=bpy.data.objects.new(name,None)
        o.empty_display_type="PLAIN_AXES"
        controls.objects.link(o)

cam=bpy.data.objects.get("MARS_TURNTABLE_CAMERA")
if not cam:
    data=bpy.data.cameras.new("MARS_TURNTABLE_CAMERA")
    cam=bpy.data.objects.new("MARS_TURNTABLE_CAMERA",data)
    bpy.context.scene.collection.objects.link(cam)
cam.location=(0,-4,0)
cam.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.camera=cam

print("MARS_HEAD_SETUP_READY: source mesh untouched; control scaffold and camera created")
