# Pocket Studio v2 — UI Research Doc (2026-10-11)

How the real apps lay out their screens, and what we're stealing for Pocket Studio.

---

## 1. CapCut Mobile (video editor)

**Overall:** Portrait, dark theme. Three stacked zones top→bottom: **Preview → Timeline → Toolbar**. Thin top bar with back button, project name, export (top-right).

**Preview (top, ~40% of screen):**
- Large 16:9 (or project ratio) video preview, always visible
- Playhead-synced; tap to play/pause
- Safe-area guides toggleable

**Timeline (middle, ~35%):**
- Multi-track, horizontally scrollable
- Track order top→bottom: main video → overlay/PIP → text → effects → audio
- Clips are rounded rectangles with thumbnails (video) or waveforms (audio)
- Selected clip gets white border + contextual toolbar appears above timeline
- Playhead: thin white/red vertical line with handle
- Pinch to zoom timeline; two-finger scroll

**Toolbar (bottom, ~25%):**
- Horizontal scrollable icon row: Edit, Audio, Text, Stickers, Overlay, Effects, Filters, Adjust, Transitions
- Tapping a tool opens its panel ABOVE the toolbar (replacing timeline space temporarily)
- Tools are contextual: select a video clip → trim/split/speed/volume/sfx options; select audio → fade/volume/denoise

**Key patterns to steal:**
- Preview ALWAYS visible at top — never hidden behind tabs
- Timeline directly under preview — no scrolling to find it
- Bottom toolbar = primary actions, always thumb-reachable
- Contextual tool panels slide up over timeline (don't navigate away)
- Clip selection → white border + floating action bar

---

## 2. FlipaClip (2D animation)

**Overall:** Single workspace. **Left tool rail → center canvas → bottom frame filmstrip.**

**Canvas (center, ~55%):**
- Drawing area with onion-skin ghost of prev/next frames (red/green tint)
- Pinch zoom, two-finger pan
- Current frame number displayed

**Left rail (tools):**
- Vertical icon strip: brush, eraser, lasso, fill, text, shapes
- Brush settings (size, opacity) pop out when brush selected
- Color palette above or below tools
- Layers button (stacked squares icon)

**Frame filmstrip (bottom, ~25%):**
- Horizontal scrollable thumbnails of every frame
- Current frame highlighted with border
- Tap thumbnail to jump; + button to add frame; long-press for duplicate/delete
- Play button + frame-step arrows (◀ ▶) in transport row above filmstrip

**Top bar:**
- Undo/redo, onion-skin toggle (onion icon), project name, share/export

**Key patterns to steal:**
- Onion-skin toggle always one tap away (top bar)
- Frame filmstrip = tap any frame to jump there
- Frame-step arrows for precise navigation (not just scrubbing)
- Tools on a slim rail, not a full panel — canvas stays big
- Long-press frame = contextual menu (duplicate, delete, hold duration)

---

## 3. FL Studio Mobile (DAW)

**Overall:** Five separate screens (not one crowded screen): **Playlist / Channel Rack / Piano Roll / Mixer / Browser**. Bottom tab bar switches.

**Playlist (main timeline):**
- Pattern blocks arranged on tracks (like LEGO bricks)
- Track headers on left (mute/solo/volume per track)
- Tap pattern → opens in piano roll or channel rack

**Channel Rack:**
- Vertical list of instruments, each with step-sequencer row (16 pads)
- Tap pad to toggle note; swipe for velocity

**Piano Roll:**
- Grid: pitch vertical, time horizontal
- Tap to add note, drag to move/resize
- Quantize, scale lock in toolbar

**Mixer:**
- Vertical channel strips with faders (volume), pan knobs, mute/solo
- FX slots per channel

**Top transport (all screens):**
- Play/stop/record, metronome toggle, tempo display, time signature

**Key patterns to steal:**
- ONE job per screen — don't cram mixer + timeline + piano roll together
- Bottom tab bar for mode switching (thumb-friendly)
- Transport ALWAYS visible regardless of screen
- Track headers with quick mute/solo (don't bury in menus)
- Color-coded clips by instrument/type

---

## 4. BandLab (mobile DAW)

**Overall:** Similar to FL but more streamlined. **Timeline → Mixer → Loops** via bottom tabs.

**Timeline:**
- Audio tracks show waveforms; MIDI tracks show note blocks
- Track headers: icon, name, mute/solo, volume slider (compact)
- Split/trim via selecting region → action bar appears
- Loop/duplicate via long-press

**Loop Library:**
- Searchable, categorized (drums, bass, melody...)
- Preview on tap; drag or tap+ to add to timeline at playhead

**Mixer:**
- Horizontal scrollable channel strips
- Volume fader + pan per strip, FX button per strip

**Key patterns to steal:**
- Compact track headers (don't waste horizontal space)
- Long-press clip = action menu (split, duplicate, delete, fade)
- Loop library pattern: tap to preview, tap+ to insert at playhead
- Big record button, hard to miss

---

## 5. Blender (desktop, for future 3D tab)

**Default Layout workspace (the pattern):**
- **Top-left:** 3D Viewport (biggest area — the work happens here)
- **Top-right:** Outliner (scene hierarchy tree)
- **Bottom-right:** Properties (settings for selected object)
- **Bottom-left:** Timeline (frames, keyframes, playback)

**Key patterns to steal (for a future 3D tab):**
- Viewport gets the most space — tools are secondary
- Outliner = tappable object list (select/visibility/lock per item)
- Properties panel = contextual to selection (select a clip → see its settings)
- Timeline spans the bottom, always visible

---

## Pocket Studio v2 Redesign — What Changes

### Layout (CapCut pattern)
```
┌─────────────────────────┐
│ Top bar: ← Project  Export│
├─────────────────────────┤
│                         │
│   PREVIEW (video)       │  ← always visible, ~35% height
│                         │
├─────────────────────────┤
│ Transport: ⏮ ◀ ▶ ▶ ⏭   │  ← FlipaClip frame-step + play
│ 0:00.0 / 5:44.8  [frame]│
├─────────────────────────┤
│ TIMELINE (scrollable)   │
│ [Video: scene blocks]   │
│ [Dialogue: waveforms]   │  ← CapCut/BandLab multi-track
│ [SFX] [BGM] [Notes]     │
├─────────────────────────┤
│ Bottom tabs:            │  ← FL Studio pattern
│ Edit │ Animate │ Blair │  │
│ Tools │ Mix                   │
└─────────────────────────┘
```

### Tabs (FL Studio pattern — one job per screen)
1. **Edit** (default): CapCut-style — preview + timeline + clip tools. Drag-drop audio, trim, notes.
2. **Animate**: FlipaClip-style — frame filmstrip, onion-skin toggle, frame-step arrows. For frame-level work.
3. **Blair**: Preston Blair panel — viseme sheets per character, model sheets, tap a viseme to see it large.
4. **Tools**: Grid of free creative tools by category (Video/Audio/2D/3D/Image/AI). Tap to open.
5. **Mix**: BandLab-style mixer — per-track volume faders for Dialogue/SFX/BGM.

### Interaction patterns (copied, not invented)
- Select clip → white border + floating action bar (CapCut)
- Long-press clip → menu: split, duplicate, delete, fade (BandLab)
- Frame-step ◀ ▶ buttons in transport (FlipaClip)
- Onion-skin toggle in Animate tab top bar (FlipaClip)
- Bottom tab bar always thumb-reachable (FL Studio)
- Preview never hidden (CapCut)
