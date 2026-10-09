"""
AUDIO -> VISEME TRACK. Real phoneme timing, not a written cadence.

The talking test so far animated a rhythm I made up. It looked like speech
because a repeating open/close reads as speech, but it was not saying anything —
the mouth was not following any actual voice. Rhubarb Lip Sync analyses the
audio and returns Preston-Blair mouth shapes with real timestamps, and those
timestamps drive the rig.

Rhubarb's shapes map onto this rig's measured visemes:
  A  closed, P/B/M                  -> viseme_MM
  B  slightly open, teeth together  -> viseme_EE
  C  open                           -> viseme_AA (partial)
  D  wide open, "aa"                -> viseme_AA
  E  rounded, "ao"/"er"             -> viseme_OH (partial)
  F  puckered, "uw"/"ow"/"w"        -> viseme_OH
  G  F/V, lip to teeth              -> viseme_FF
  H  L, tongue up                   -> viseme_AA (partial)
  X  rest                           -> everything at zero

Jaw opening is derived from the shape, not invented: a wide "D" opens the jaw
far, "A" and "X" close it. The mouth shape and the jaw are the two halves of the
same phoneme, so they are emitted together.

  vendor/blender/blender ... (this runs OUTSIDE blender)
  python3 tools/character/audio_to_visemes.py <audio.wav> [--fps 24] [--out track.json]
"""
import sys, os, json, subprocess, shutil

args = [a for a in sys.argv[1:] if not a.startswith("--")]
def opt(f, d):
    return sys.argv[sys.argv.index(f) + 1] if f in sys.argv else d

if not args:
    sys.exit("usage: audio_to_visemes.py <audio.wav> [--fps 24] [--out track.json]")
AUDIO = os.path.abspath(args[0])
FPS = float(opt("--fps", "24"))
OUT = os.path.abspath(opt("--out", "renders/_lipsync/viseme_track.json"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)

if not os.path.exists(AUDIO):
    sys.exit("no audio at " + AUDIO)

rhubarb = opt("--rhubarb", os.path.join("vendor", "rhubarb", "rhubarb"))
if not os.path.exists(rhubarb):
    sys.exit("rhubarb not found at %s — fetch the release from\n"
             "  https://github.com/DanielSWolf/rhubarb-lip-sync/releases" % rhubarb)

# ── run the real analyser ────────────────────────────────────────────────────
# --recognizer phonetic works without a transcript. With one, "pocketSphinx"
# is more accurate, but a transcript is not always available and inventing one
# would put words in his mouth that he did not say.
cmd = [rhubarb, "-f", "json", "-r", "phonetic", "--machineReadable", AUDIO]
proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
if proc.returncode != 0:
    sys.exit("rhubarb failed (%d):\n%s" % (proc.returncode, proc.stderr[-600:]))

try:
    data = json.loads(proc.stdout)
except json.JSONDecodeError:
    sys.exit("rhubarb returned unparseable output:\n" + proc.stdout[:500])

cues = data.get("mouthCues", [])
if not cues:
    sys.exit("rhubarb found no mouth cues in this audio — it contains no usable speech")

# ── map to THIS rig's measured shape keys ───────────────────────────────────
# (shapeKey, weight, jawDegrees)
SHAPE_MAP = {
    "A": ("viseme_MM", 1.00, 0.0),
    "B": ("viseme_EE", 0.85, 4.0),
    "C": ("viseme_AA", 0.55, 8.0),
    "D": ("viseme_AA", 1.00, 15.0),
    "E": ("viseme_OH", 0.60, 7.0),
    "F": ("viseme_OH", 1.00, 10.0),
    "G": ("viseme_FF", 1.00, 3.0),
    "H": ("viseme_AA", 0.45, 6.0),
    "X": (None, 0.0, 0.0),
}

duration = max(c["end"] for c in cues)
frame_count = int(round(duration * FPS))
track = []
for f in range(frame_count):
    t = f / FPS
    cue = next((c for c in cues if c["start"] <= t < c["end"]), None)
    letter = cue["value"] if cue else "X"
    shape, weight, jaw = SHAPE_MAP.get(letter, (None, 0.0, 0.0))
    track.append({"frame": f, "t": round(t, 4), "rhubarb": letter,
                  "shapeKey": shape, "weight": weight, "jawDegrees": jaw})

counts = {}
for c in cues:
    counts[c["value"]] = counts.get(c["value"], 0) + 1

out = {
    "source": os.path.relpath(AUDIO, os.getcwd()) if AUDIO.startswith(os.getcwd()) else AUDIO,
    "analyser": "Rhubarb Lip Sync 1.13.0, phonetic recognizer",
    "durationSec": round(duration, 3),
    "fps": FPS,
    "frameCount": frame_count,
    "cueCount": len(cues),
    "shapeHistogram": counts,
    "mouthCues": cues,
    "track": track,
}
json.dump(out, open(OUT, "w"), indent=2)

spoken = sum(1 for c in cues if c["value"] != "X")
print("Rhubarb: %d mouth cues over %.2fs (%d are speech, %d rest)"
      % (len(cues), duration, spoken, len(cues) - spoken))
print("  shapes: " + ", ".join("%s x%d" % (k, v) for k, v in sorted(counts.items())))
print("  -> %d frames at %gfps" % (frame_count, FPS))
if spoken < 3:
    print("  WARNING: almost no speech shapes. This audio may be too noisy or too quiet.")
print("→ " + OUT)
