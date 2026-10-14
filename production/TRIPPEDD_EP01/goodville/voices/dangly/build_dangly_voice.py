#!/usr/bin/env python3
"""Build Lt. James Dangly style-alike parody voice (v2).
Policy: NO cloning. Base = ElevenLabs stock premade voice "Bill" (old male, synthetic, not a real person).
Three ranges steered via eleven_v3 delivery tags + per-range voice settings.
Generates the two canonical video lines per range -> MP3s + manifest.
"""
import sys, json, urllib.request, urllib.error, os, time

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
BASE = "https://api.elevenlabs.io/v1"

VOICE_ID = "pqHfZKP75CvOlQylNhV4"  # Bill - Wise, Mature, Balanced | old male, premade stock

OUT = os.path.expanduser("~/workspace/trippedd-studio/production/TRIPPEDD_EP01/goodville/voices/dangly")
os.makedirs(OUT, exist_ok=True)

def call(path, payload=None, raw_bytes=False):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, method="POST",
        headers={"User-Agent": UA, "Content-Type": "application/json"})
    add_surrogate_to_request(req, "custom.elevenlabs", allowed_hosts=["api.elevenlabs.io"])
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return resp.read() if raw_bytes else read_json_response(resp)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} on {path}: {e.read().decode()[:600]}")

RANGES = {
  "drunk": {"stability": 0.30, "similarity": 0.75, "style": 0.70,
    "line1": "[slurred, drunkenly, grandiose] I've seen some things...",
    "line2": ("[slurred, drunkenly, grandiose] One time... I saw a guy in traffic... "
              "[shouting] he beat up a dinosaur, ripped its head off... "
              "[mumbling, trailing off] did ungodly things... unspeakable..")},
  "sober": {"stability": 0.55, "similarity": 0.80, "style": 0.45,
    "line1": "[coldly, quietly, menacingly] I've seen some things...",
    "line2": ("[quietly, menacingly, deliberate] One time... I saw a guy in traffic. "
              "He beat up a dinosaur. Ripped its head off. Did ungodly things. Unspeakable.")},
  "calm": {"stability": 0.70, "similarity": 0.85, "style": 0.30,
    "line1": "[warmly, gently, thoughtfully] I've seen some things...",
    "line2": ("[calmly, warmly, gently] One time... I saw a guy in traffic. "
              "He beat up a dinosaur, ripped its head off... did ungodly things. Unspeakable.")},
}

LINES_CANON = {
  "line1_ive-seen-some-things": "I've seen some things...",
  "line2_dinosaur-story": ("One time... I saw a guy in traffic, he beat up a dinosaur, "
    "ripped its head off, did ungodly things, unspeakable.."),
}

manifest = {
  "voice": "Lt. James Dangly (style-alike parody scratch; NO clone)",
  "policy": "No cloning of John Dunsworth (d. 2017). Base voice = ElevenLabs premade stock voice 'Bill' (old male, synthetic, not a real person). Ranges steered by delivery tags + voice settings on eleven_v3.",
  "base_voice": {"id": VOICE_ID, "name": "Bill - Wise, Mature, Balanced", "category": "premade"},
  "model": "eleven_v3",
  "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
  "ranges": {}, "files": []}

for rname, r in RANGES.items():
    print(f"--- range: {rname} ---", flush=True)
    manifest["ranges"][rname] = {
        "tts_settings": {"stability": r["stability"], "similarity_boost": r["similarity"], "style": r["style"]}}
    for lname, key in (("line1_ive-seen-some-things", "line1"), ("line2_dinosaur-story", "line2")):
        fname = f"dangly_{rname}_{lname}.mp3"
        print(f"  TTS {fname} ...", flush=True)
        audio = call(f"/text-to-speech/{VOICE_ID}",
            {"text": r[key], "model_id": "eleven_v3",
             "voice_settings": {"stability": r["stability"], "similarity_boost": r["similarity"],
                                "style": r["style"], "use_speaker_boost": True}},
            raw_bytes=True)
        p = os.path.join(OUT, fname)
        with open(p, "wb") as f: f.write(audio)
        manifest["files"].append({"file": fname, "range": rname, "line": lname,
            "canon_text": LINES_CANON[lname], "directed_text": r[key], "bytes": len(audio)})
        time.sleep(1)

with open(os.path.join(OUT, "dangly_voice_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print("DONE:", [m["file"] for m in manifest["files"]])
