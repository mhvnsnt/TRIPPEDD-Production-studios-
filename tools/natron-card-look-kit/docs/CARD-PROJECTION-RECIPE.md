# Card projection — the two routes + the decision rule (SPEC N-1)

Natron 2.5.0 has no native 3D system (Natron's own Nuke-transition
guide: "Mainly 3D functions are not implemented"). Card work therefore
takes one of two routes. Both are wired; the rule below picks per shot.

## Route A1 — in Natron, donor: PM_Card3D + PM_Camera (adopted)

The community pair (in `card-kit/community-donor/`, installed by
`gizmos/install_gizmos.sh`): **PM_Camera** is a minimal 3D camera node
for Natron; **PM_Card3D** creates a 3D plane ("card") that the camera
photographs. This is real in-comp 3D: cards sit at 3D positions, the
camera can move/rotate, cards occlude by depth as the camera moves.

**Setup:** Read (plate) → PM_Card3D (position/rotate the card on its
own knobs) → Write/merge; PM_Camera feeds the card's camera input and
is the node you animate for the camera move. One camera can drive
several cards — that is a set extension in the comp.

**Limits (honest):** it is a *minimal* 3D system ("Poor's Man") —
planes only, no geometry import, no lighting model. Anything beyond
flat cards in a small 3D space goes to Route B.

## Route A2 — in Natron: `TrippeddCard25D` (this kit's studio group)

A flat card moved by a virtual camera, inside the comp.

**Graph:** `Read (card plate) → TrippeddCard25D → Merge (over) → …`
one group instance per card/depth layer.

**Setup:**

1. One group per card. Set **Depth** per layer:
   background plate 0.3–0.6 · midground 1.0 · foreground 1.5–2.5 ·
   locked-to-camera content (TV screen content, HUD) 0.
2. Animate **Camera Pan X/Y** and **Camera Zoom** on ONE card, then
   copy those exact keyframes/values to every other card in the shot.
   The groups multiply the pan by each card's Depth — the differential
   is the parallax. (Wizard Gang pan-and-zoom: pan + slow zoom 1.0→1.15
   over the shot is the house move.)
3. Perspective: open the group, fit the **CornerPin** `to` points to
   the photographed angle of the card. Standard keystone for a card
   seen at a slight angle, 1920×1080 card, pull `K` px:
   `to1 = (K, K/2)`, `to2 = (1920-K, K/2)`, `to3 = (1920, 1080)`,
   `to4 = (0, 1080)` — top edge recedes, bottom stays planted.
   Scale the numbers for other formats.
4. Merge cards back-to-front (deepest Depth… no: **smallest Depth
   first** — farthest card at the bottom of the Merge stack).

**Limits (honest):** the card stays flat. No orbit, no occlusion by 3D
geometry, no lighting change on the card, pan range is a few hundred
pixels before edges show (overscan plates by ~15% to be safe).

## Route B — in Blender, comped in Natron (camera-mapped planes)

True camera projection: the painting/plate is texture-projected from a
real 3D camera onto planes in a real 3D space.

**Recipe:**

1. Blender scene at the shot's format/fps. Add the camera first;
   animate the camera move the shot needs (this is the master move —
   nothing is faked downstream).
2. Per layer, add a plane at its depth, sized to fill frame at that
   depth. Select plane + camera → project the plate as the plane's
   material: image texture with **Texture Coordinate = Camera**
   (or UV-project modifier from the camera's view at frame 1 for a
   static projection), `emissive/shadeless`-style material
   (Emission shader with the image, strength 1) so the plate keeps its
   comp colours — lighting is done in Natron, not re-lit here.
3. Foreground occluders (furniture, TV frame, character plates that
   must pass *in front* of a card) go in as their own planes/objects at
   their real depths — this is what Route A cannot do.
4. Render **multilayer EXR, one pass per depth layer** (view layers or
   separate render layers per plane), plus a combined beauty for
   reference. Keep renders scene-linear; do the look in Natron.
5. Natron comp: Read each EXR layer → Merge back-to-front → LOOK gizmo
   (N-3 pack) → LED gizmo if the scene is an LED scene → Write.
   Because the camera move is baked into the renders, no card groups
   are needed on this route.

**Limits:** a render round-trip per camera change; text/plates that
change per frame must be re-rendered, not re-comped.

## Decision rule — which route a shot takes

Ask in order; first YES decides:

1. **Does the camera orbit, dolly through, or change angle** (not just
   pan/zoom in the picture plane) **in a space bigger than a few
   cards**, or must real geometry occlude the cards? → **Route B.**
2. **A real 3D camera move over a handful of flat cards** (set
   extension, matte painting the camera pushes into, cards at true
   3D depths)? → **Route A1 (donor PM_Card3D + PM_Camera).**
3. **Is the pan bigger than the plate's overscan** (~15%) with a
   perspective change *during* the move, beyond what A1's planes
   give? → **Route B.**
4. Otherwise — flat pan/zoom in the picture plane, layered plates,
   TV-parallel gag, title cards, fast turnaround — → **Route A2
   (TrippeddCard25D).**

House defaults: Wizard Gang pan-and-zoom = Route A2. Cape Jones
TV-parallel gag = Route A2 (TV content card at Depth 0, room cards
at depth). Set extensions with a camera move = Route A1 first,
Route B when A1's planes are not enough.

## Donor note

Route A1 is the donor the spec asked for (PMCard3D / PMcamera from
the Natron community scripts, `NatronGitHub/natron-plugins`),
adopted unmodified — fetch record and a correction to this lane's
first (wrong) "not fetchable" draft are in
`SOURCES-AND-PROVENANCE.md`. `TrippeddCard25D` (Route A2) is the
studio's own companion group for the flat pan-and-zoom move, not a
replacement for the donor.
