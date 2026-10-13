# Voice Work Audio Timeline Mover

Drag-and-drop timeline editor for placing voice lines and SFX on a video timeline.

## How to use
1. Open `index.html` in a browser (or present as a Muse HTML widget)
2. Tap anywhere on the timeline to move the playhead — exact timestamp shown
3. Drag any clip block left/right to reposition it
4. Tap a block to select it, move the video playhead to the cut point, hit SPLIT AT PLAYHEAD to slice a line into independently movable pieces
5. Hit COPY NEW TIMELINE and paste the result back to Muse to rebuild the mix

## Timeline format
`id|start_sec|duration|src_file|src_offset|CHARACTER|line description`

Split pieces carry their source file + offset so the rebuild knows which part of the original audio to use.

## History
Built 2026-10-13 for Wizard Gang EP01 dialogue placement (v2 → v5 mixes).
