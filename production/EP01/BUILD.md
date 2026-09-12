# EP01 — Real Pilot Build

This is the executable production path, not a mock episode.

## 1. Ingest real source

Open **Media Ingest**, authenticate Google Drive, and scan the configured EP01 source folder. The queue streams each source to the runtime media cache instead of deleting it after analysis.

Required analysis:
- ffprobe — technical metadata
- PySceneDetect — shot boundaries
- Whisper — timed transcript
- OpenCV — sampled visual evidence when available
- Tesseract — OCR when available

## 2. Discover selects

Comedy discovery scores transcript-timed moments for escalation, reaction, awkward silence, interruption, dialogue density, and callback potential. Candidates remain `MACHINE_SUGGESTED` until human review.

## 3. Build first assembly

`src/server/pilotRenderer.ts` can build `EP01-first-assembly.mp4` from real cached media and timed comedy selects. This is deliberately a **first assembly**, not a fake final episode: it exposes the strongest real moments while the editorial story gate is still open.

The runtime output is placed at `/production/EP01-first-assembly.mp4` so the application can play it.

## 4. Build the subjective sequence

Run `production/EP01/generated/blender/build_subjectivity.py` through a real Blender installation. The resulting scene is generated material and must remain explicitly labelled as such.

Visual law:
`LIVE ACTION → DISTORTION → ANIMATION → 3D → BLENDER/CG → IMPOSSIBLE WORLD → LIVE ACTION`

The point is subjective storytelling. It is not a technology demo.

## 5. Editorial lock

Use the canonical EP01 assembly plan:
- Motel Reality
- Shumafied Item
- Decision to Get Cigars
- Walk / Bag Incident
- Joe / Goodville material
- Shumafied subjective shift
- hard return to live action
- “wasn't even shit” reaction
- acid memory
- frantic search
- lost-acid button

Physical chronology is evidence. Editorial chronology is the constructed episode.

## 6. Final gates

Before delivery:
- verify every source select against physical evidence;
- approve/reject generated subjective shots;
- build final editorial assembly;
- run technical + continuity QC;
- verify terminal button is truly terminal;
- human showrunner greenlight;
- export delivery master.

No stage is allowed to silently substitute generated material for source footage.
