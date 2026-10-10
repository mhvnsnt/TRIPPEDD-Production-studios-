#!/usr/bin/env python3
"""WIZARD GANG EP01 'THE SUMMIT' — assembly (ffmpeg two-stage, pilot method).

Stage 1: normalize every segment to 1920x1080 / 30fps / h264 yuv420p, exact
durations (shots are 10.0s @24fps, mixed aspect ratios — scale-to-fill +
center-crop, NEVER stretched).
Stage 2: concat demuxer (-c copy) for video; pilot audio + show mix for audio;
mux to final 1920x1080 MP4.

Video timeline (show block = 250.14s, mirrors audio mix structure exactly):
  0.1s white match-cut flare, S10 12, S11 16, S12 20, S13 32 (10s x3 loop + 2s
  freeze), Act-2 beats per stem durations with 0.42s white flashes on each of
  the 12 whoosh-hits (mix bakes them in), S27 25 (10+10+5 freeze), S28 20
  (10s shot stretched to 16.4s so the flash bloom lands on the audio flash hit
  at 16.4s, 2s freeze, 1.6s fade to black), S29 5 (2.5+2.5 cards).
Cold open: pilot v2 re-encoded (content as-is) + show block = 300.14s.
Audio: pilot soundscape (upmixed mono->stereo) 0:00-0:50 + full show mix
0:50-5:00, no voices, no ducking.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
PILOT = os.path.abspath(os.path.join(HERE, "..", "WIZARD_GANG_SHORT_01",
                                     "wizard-gang-pilot-16x9-v2.mp4"))
MIX = os.path.join(HERE, "audio", "ep01_full_mix_0050-0500.wav")
TMP = os.path.join(HERE, "assemble_tmp")  # disposable intermediates, NOT committed
OUT = os.path.join(HERE, "wizard-gang-ep01-16x9.mp4")

FIT = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"
VENC = ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-r", "30", "-an"]

def run(cmd):
    print("+", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], flush=True)
        sys.exit(1)

def seg(name, src=None, ss=0.0, dur=None, vf_extra=None, color=None):
    """Build one normalized segment (skip if already built)."""
    path = os.path.join(TMP, name + ".mp4")
    if os.path.exists(path):
        print(f"skip {name} (exists)", flush=True)
        return path
    vf = FIT if src else "format=yuv420p,fps=30"
    if vf_extra:
        vf = vf + "," + vf_extra
    if color:
        cmd = (["ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i",
                f"color={color}:size=1920x1080:rate=30:duration={dur}",
                "-vf", vf] + VENC + ["-t", str(dur), path])
    else:
        cmd = (["ffmpeg", "-y", "-v", "error", "-ss", str(ss)]
               + (["-t", str(dur)] if dur else [])
               + ["-i", src, "-vf", vf] + VENC + [path])
    run(cmd)
    return path

def main():
    os.makedirs(TMP, exist_ok=True)
    S = lambda f: os.path.join(SHOTS, f)
    s10a = S("media-generation-s10a-summons-rooftop-0-8f3bc516-3814-4973-ad04-05a1f44bd1c6.mp4")
    s10b = S("media-generation-s10b-summons-flare-0-e95ed086-08b3-43d8-bb6c-381be5849238.mp4")
    s11a = S("media-generation-s11a-summit-push-0-8a1c8294-fcf7-4f54-bf9c-06607c9479f1.mp4")
    s11b = S("media-generation-s11b-wink-pan-0-57bee83e-7235-423c-baa7-31569639c685.mp4")
    s11c = S("media-generation-s11c-ritual-fail-0-f0d2e2cd-5c18-48c1-8ba9-0bdb597935db.mp4")
    s12a = S("media-generation-s12a-rollcall-table-0-b7e6106c-b6b4-4291-b468-cf30dd60b253.mp4")
    s12b = S("media-generation-s12b-rollcall-lineup-0-01dd3cec-8588-4276-b1e3-a3acd7e27f26.mp4")
    s13  = S("media-generation-s13-bbq-derail-v2-0-3cb85e24-1efc-404b-87a3-70a03896e0f3.mp4")
    s14  = S("media-generation-s14-dice-game-0-a1c6e612-01be-4ab4-9cf7-0c49dca8cd20.mp4")
    s15  = S("media-generation-s15-arcade-v2-0-68ea590b-2e75-44de-a6ca-886ac1969290.mp4")
    s16  = S("media-generation-s16-basketball-v2-0-f6979bca-0f2f-4228-85f1-e64df77ba79c.mp4")
    s17  = S("media-generation-s17-bodega-v2-0-2956874b-0980-42a7-9bd3-a51c34bf0bab.mp4")
    s18  = S("media-generation-s18-night-market-v2-0-a6d8b9d7-67b4-4a33-a225-a3297a19e277.mp4")
    s19  = S("media-generation-s19-subway-0-2750cb4d-fe0f-4006-b9b5-16ee63280796.mp4")
    s20  = S("media-generation-s20-bridge-0-bdc78dc5-bd71-4ea6-be07-d4b8462577ad.mp4")
    s21  = S("media-generation-s21-parking-garage-0-f9b7c78f-e5b4-4c47-94d7-02c3994181ef.mp4")
    s22  = S("media-generation-s22-skate-park-v3-0-9e15172e-1308-41d2-9c8e-6885003348c1.mp4")
    s23  = S("media-generation-s23-studio-v2-0-d70096d2-55e0-480b-bcf9-92c20eedde59.mp4")
    s24  = S("media-generation-s24-sombra-plushie-0-f3bfa068-9074-4151-a1cf-1c7d7da62c8b.mp4")
    s25a = S("media-generation-s25a-grill-flare-0-f17c117b-8bfd-4a14-a5ad-52352ee69721.mp4")
    s25b = S("media-generation-s25b-bbq-coverup-v2-0-664d2f46-dac3-4c79-b565-d01ba07e6456.mp4")
    s26  = S("media-generation-s26-kiko-pier-callback-0-862c4954-3a4e-4c11-89a2-14e4cb35e9cf.mp4")
    s27a = S("media-generation-s27a-fireworks-0-6504ae0f-4453-420e-b6f9-dc0f93c6d582.mp4")
    s27b = S("media-generation-s27b-embers-0-de628c80-b744-43ac-b09b-f65019ffcf62.mp4")
    s28  = S("media-generation-s28-group-photo-v2-0-214a0dc4-0e56-446a-b73e-0021b8987270.mp4")
    s29a = S("media-generation-s29a-title-wizard-gang-0-f62d0f2d-71b5-4d3b-99f4-abe7e63409b8.mp4")
    s29b = S("media-generation-s29b-ident-trippedd-0-7610d7db-d9ac-42de-bfb0-03e5fa513160.mp4")

    order = []
    # --- cold open: pilot v2, content as-is (re-encoded for concat compat) ---
    pilot_seg = os.path.join(TMP, "seg_pilot.mp4")
    if not os.path.exists(pilot_seg):
        run(["ffmpeg", "-y", "-v", "error", "-i", PILOT,
             "-c:v", "libx264", "-crf", "16", "-preset", "medium",
             "-pix_fmt", "yuv420p", "-r", "30", "-an", pilot_seg])
    order.append(pilot_seg)

    # --- show block ---
    order.append(seg("seg00_flash_open", color="white", dur=0.1))
    order.append(seg("seg01_s10a", s10a, dur=6.0))
    order.append(seg("seg02_s10b", s10b, dur=6.0))
    order.append(seg("seg03_s11a", s11a, dur=6.0))
    order.append(seg("seg04_s11b", s11b, dur=5.0))
    order.append(seg("seg05_s11c", s11c, dur=5.0))
    order.append(seg("seg06_s12a", s12a, dur=10.0))
    order.append(seg("seg07_s12b", s12b, dur=10.0))
    # S13: 10s BBQ x3 loops (30s) + 2s freeze on last frame = 32s
    order.append(seg("seg08_s13", s13, dur=10.0,
                     vf_extra="loop=loop=2:size=300,tpad=stop_mode=clone:stop_duration=2"))
    # Act 2: beats + 0.42s white flashes on the mix's whoosh-hits
    beats = [(s14, 10.0), (s15, 10.0), (s16, 9.0), (s17, 9.0), (s18, 10.0),
             (s19, 9.0), (s20, 8.0), (s21, 8.0), (s22, 9.0), (s23, 9.0),
             (s24, 10.0)]
    for i, (shot, d) in enumerate(beats, start=9):
        order.append(seg(f"seg{i:02d}_beat", shot, dur=d))
        order.append(seg(f"seg{i:02d}_flash", color="white", dur=0.42))
    order.append(seg("seg21_s25a", s25a, dur=2.1))   # flare cut lands on audio hit @2.1s
    order.append(seg("seg22_s25b", s25b, dur=3.9))
    order.append(seg("seg23_flash", color="white", dur=0.42))
    order.append(seg("seg24_s26", s26, ss=2.0, dur=8.0))  # skip group open, land on Kiko push-in
    # S27: fireworks 10 + embers 10 + 5s freeze (Onyx burger payoff frame)
    order.append(seg("seg25_s27a", s27a, dur=10.0))
    order.append(seg("seg26_s27b", s27b, dur=10.0,
                     vf_extra="tpad=stop_mode=clone:stop_duration=5"))
    # S28: stretch 10s->16.4s (flash bloom lands on audio flash @16.4s),
    # 2s freeze, 1.6s fade to black
    order.append(seg("seg27_s28", s28, dur=10.0,
                     vf_extra="setpts=PTS*1.64,tpad=stop_mode=clone:stop_duration=2,"
                              "fade=t=out:st=18.4:d=1.6"))
    order.append(seg("seg28_s29a", s29a, dur=2.5))
    order.append(seg("seg29_s29b", s29b, dur=2.5))

    # --- stage 2a: concat video ---
    lst = os.path.join(TMP, "concat.txt")
    with open(lst, "w") as f:
        for p in order:
            f.write(f"file '{p}'\n")
    video = os.path.join(TMP, "video_only.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", video])

    # --- stage 2b: audio (pilot mono->stereo + show mix) ---
    audio = os.path.join(TMP, "audio.m4a")
    run(["ffmpeg", "-y", "-v", "error", "-i", PILOT, "-i", MIX,
         "-filter_complex",
         "[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];"
         "[a0][1:a]concat=n=2:v=0:a=1,aresample=48000[a]",
         "-map", "[a]", "-c:a", "aac", "-b:a", "192k", audio])

    # --- stage 2c: mux ---
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", audio,
         "-c", "copy", "-movflags", "+faststart", "-shortest", OUT])
    print("wrote", OUT, flush=True)

if __name__ == "__main__":
    main()
