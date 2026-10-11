# Pocket Studio v2

Mobile timeline editor for Wizard Gang EP02. The owner drags dialogue clips on his phone; the app exports a project JSON; `build.py` renders the final MP4.

## Files

- `app.html` — the complete single-file web app (deployed as artifact `pocket-studio-v2`)
- `project-ep02-v8b.json` — full project data with waveform peaks (source of truth)
- `project-embed.json` — compact version embedded in the app
- `project-compact.json` — intermediate
- `audio-durations.json` — durations for all 48 audio files
- `build.py` — ffmpeg builder: project JSON → rendered MP4

## Project JSON format

```json
{
  "name": "EP02 v8b (edited)",
  "base_video": "trippedd-studio/production/WIZARD_GANG_EP01/wizard-gang-ep02-final-v8b.mp4",
  "duration": 344.81,
  "clips": [
    {
      "id": "h1",
      "track": "dialogue",
      "file": "voice-delivery/voice-onyx-h1.mp3",
      "original_at": 84.0,
      "at": 86.0,
      "duration": 2.64,
      "volume": 1.0,
      "label": "H1 Onyx",
      "character": "onyx",
      "text": "We are adjourning nothing."
    }
  ],
  "ducks": [
    {"at": 84.0, "duration": 3.0, "to": 0.5, "label": "Duck Static under Onyx H1"}
  ],
  "notes": [
    {"at": 93.0, "text": "volume spike here"}
  ]
}
```

## Builder

```bash
# Render from a project file (exported from the app)
python3 build.py /path/to/ep02-project-123.json -o wizard-gang-ep02-final-v9.mp4

# Dry run (print ffmpeg command)
python3 build.py project-ep02-v8b.json -o out.mp4 --dry
```

How it works:
1. Mutes base audio at every clip's `original_at` (clean move, no doubles)
2. Places every clip at its `at` with its `volume`
3. Applies ducks (volume automation on base)
4. Video passes through untouched; only audio is rebuilt

## Workflow

1. Owner opens Pocket Studio v2 on phone
2. Drags clips, adds notes, records voice
3. Hits Save → project JSON downloaded + copied
4. Owner sends JSON to agent
5. Agent runs `build.py` → new cut
6. Agent uploads review copy → owner reviews in app (paste new URL)

## Clip IDs in v8b

| ID | Label | At | Character |
|----|-------|----|-----------|
| n1 | N1 Narrator | 52.0s | narrator |
| l1 | L1 Static | 56.0s | static |
| l2 | L2 Static | 66.0s | static |
| whisper | Ritual whisper | 75.0s | ashes |
| l3 | L3 Static | 82.0s | static |
| h1 | H1 Onyx | 84.0s | onyx |
| l6 | L6 Static | 96.0s | static |
| l7-ashes | L7 Ashes | 113.0s | ashes |
| c4 | C4 Cipher | 121.0s | cipher |
| l10 | L10 Static | 151.0s | static |
| l18 | L18 Static | 222.0s | static |
| c1 | C1 Cipher | 256.0s | cipher |
| l17 | L17 Static | 261.0s | static |
| c2 | C2 Cipher | 263.0s | cipher |
| h3 | H3 Sombra | 281.0s | sombra |
| c3 | C3 Cipher | 282.0s | cipher |
