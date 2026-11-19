#!/usr/bin/env python3
"""TRIPPEDD NETWORK bump generator — Adult Swim-inspired original interstitials.
Renders 10 bumps in vertical (720x1280) and horizontal (1280x720), 30fps, silent.
All content original. Study the FORM of AS bumps; none of their actual copy.
"""
import os, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.expanduser("~/workspace/trippedd-bumps")
VERT = (720, 1280)
HORZ = (1280, 720)
FPS = 30
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TAG = "[trippedd]"

def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def pipe_ffmpeg(path, w, h, fps, dur):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(fps), "-i", "-",
           "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "20", "-preset", "medium", path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

def draw_centered_text(img, lines, size, color=(255,255,255), y_off=0, bold=True, stroke=0):
    d = ImageDraw.Draw(img)
    f = font(size, bold)
    # measure total block height
    hs = []
    ws = []
    for ln in lines:
        bb = d.textbbox((0,0), ln, font=f, stroke_width=stroke)
        ws.append(bb[2]-bb[0]); hs.append(bb[3]-bb[1])
    total = sum(hs) + int(size*0.35)*(len(lines)-1)
    y = img.height//2 - total//2 + y_off
    for ln, lh, lw in zip(lines, hs, ws):
        x = img.width//2 - lw//2
        d.text((x, y), ln, font=f, fill=color, stroke_width=stroke,
               stroke_fill=(0,0,0) if stroke else None)
        y += lh + int(size*0.35)
    return img

def draw_corner_tag(img, size=28):
    d = ImageDraw.Draw(img)
    f = font(size, bold=False)
    bb = d.textbbox((0,0), TAG, font=f)
    d.text((img.width-(bb[2]-bb[0])-28, img.height-(bb[3]-bb[1])-24),
             TAG, font=f, fill=(200,200,200))

def black_frame(w, h):
    return np.zeros((h, w, 3), dtype=np.uint8)

def trippy_frame(w, h, t, seed=0.0, sat=1.0):
    """Animated tie-dye interference pattern."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xn = xx / w * 6.2831
    yn = yy / h * 6.2831
    r = np.sin(xn*2.0 + t*1.3 + seed) + np.sin(yn*3.0 - t*0.7 + seed*1.7)
    g = np.sin((xn+yn)*1.5 + t*0.9 + seed + 2.1) + np.sin(xn*4.0 - t*1.1)
    b = np.sin((xn-yn)*2.0 - t*1.0 + seed + 4.2) + np.sin(yn*2.5 + t*0.6)
    r = np.clip((r/2*sat*0.5+0.5)*255, 0, 255)
    g = np.clip((g/2*sat*0.5+0.5)*255, 0, 255)
    b = np.clip((b/2*sat*0.5+0.5)*255, 0, 255)
    return np.stack([r, g, b], axis=-1).astype(np.uint8)

def wave_distort(arr, t, amp=18.0, freq=0.012):
    """Horizontal sine wave displacement — wavy trippy feel."""
    h, w, _ = arr.shape
    yy = np.arange(h)
    shift = (np.sin(yy*freq*6.2831*8 + t*2.0)*amp).astype(np.int32)
    out = np.zeros_like(arr)
    xx = np.arange(w)
    for y in range(h):
        out[y] = np.roll(arr[y], shift[y], axis=0)
    return out

def fade(arr, alpha):
    return (arr.astype(np.float32)*alpha).astype(np.uint8)

# ---------- bump definitions: (slug, seconds, render_fn) ----------
def b01_stay_trippedd(w, h, n):
    """5s black card network ID."""
    for i in range(n):
        a = min(1.0, i/12)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 96 if w <= 720 else 84
        draw_centered_text(img, ["STAY", "TRIPPEDD"], sz)
        draw_corner_tag(img)
        yield np.array(img)

def b02_couch(w, h, n):
    """5s deadpan one-liner."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 44 if w <= 720 else 40
        draw_centered_text(img, ["you're not stuck.", "you're just watching tv."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b03_trippy_id(w, h, n):
    """10s wavy tie-dye network ID."""
    for i in range(n):
        t = i / FPS
        bg = wave_distort(trippy_frame(w, h, t, seed=1.3), t, amp=14)
        img = Image.fromarray(bg)
        sz = 72 if w <= 720 else 64
        draw_centered_text(img, ["TRIPPEDD", "NETWORK"], sz, stroke=3)
        yield np.array(img)

def b04_tonight(w, h, n):
    """10s fake schedule card."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["tonight:", "wizard gang.", "then more wizard gang."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b05_dear_trippedd(w, h, n):
    """10s sarcastic viewer Q&A."""
    lines1 = ["dear trippedd:", '"is this for kids?"']
    lines2 = ["no.", "", "next question."]
    for i in range(n):
        img = Image.fromarray(black_frame(w, h))
        sz = 48 if w <= 720 else 42
        if i < n//2:
            draw_centered_text(img, lines1, sz, bold=False)
        else:
            draw_centered_text(img, lines2, sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b06_typewriter(w, h, n):
    """15s typewriter thought."""
    full = "we spent four years building this network. you're watching it on a phone."
    chars = int(len(full) * min(1.0, n / (n*0.75)))
    for i in range(n):
        img = Image.fromarray(black_frame(w, h))
        upto = int(len(full) * min(1.0, i / (n*0.7)))
        txt = full[:upto] + ("_" if (i//8) % 2 == 0 and upto < len(full) else "")
        # wrap
        words, lines, cur = txt.split(" "), [], ""
        d = ImageDraw.Draw(img)
        f = font(40 if w <= 720 else 36, bold=False)
        for wd in words:
            test = (cur + " " + wd).strip()
            if d.textlength(test, font=f) > w - 90:
                lines.append(cur); cur = wd
            else:
                cur = test
        lines.append(cur)
        draw_centered_text(img, lines, 40 if w <= 720 else 36, bold=False)
        if upto >= len(full):
            draw_corner_tag(img, 24)
        yield np.array(img)

def b07_wg_promo(w, h, n):
    """15s Wizard Gang promo card."""
    for i in range(n):
        t = i / FPS
        bg = wave_distort(trippy_frame(w, h, t, seed=4.1, sat=0.8), t, amp=10)
        # darken for text legibility
        bg = (bg.astype(np.float32)*0.55).astype(np.uint8)
        img = Image.fromarray(bg)
        sz = 60 if w <= 720 else 54
        a = min(1.0, i/15)
        if a > 0:
            draw_centered_text(img, ["wizard gang.", "new episodes.", "eventually."], sz, stroke=2)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b08_cd_promo(w, h, n):
    """15s Concrete Dragon game promo."""
    for i in range(n):
        img = Image.fromarray(black_frame(w, h))
        sz = 52 if w <= 720 else 46
        a = min(1.0, i/12)
        if a > 0:
            draw_centered_text(img, ["concrete dragon.", "it's $4.99.", "that's cheaper", "than your coffee."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b09_ambient_drift(w, h, n):
    """30s slow ambient mood piece."""
    for i in range(n):
        t = i / FPS * 0.5  # slow
        bg = trippy_frame(w, h, t, seed=7.7, sat=0.7)
        bg = (bg.astype(np.float32)*0.6).astype(np.uint8)
        img = Image.fromarray(bg)
        sz = 44 if w <= 720 else 40
        # text fades in middle third
        mid = n//2
        span = n//4
        if abs(i-mid) < span:
            al = 1.0 - abs(i-mid)/span
            txt = Image.new("RGB", (w, h))
            draw_centered_text(txt, ["breathe in.", "breathe out.", "the cartoons will",
                                     "be here when", "you get back."], sz, bold=False)
            base = np.array(img).astype(np.float32)
            tl = np.array(txt).astype(np.float32)
            mask = (tl.sum(axis=-1, keepdims=True) > 30).astype(np.float32)*al
            out = base*(1-mask) + tl*mask
            img = Image.fromarray(out.astype(np.uint8))
        if i > n-30:
            draw_corner_tag(img, 24)
        yield np.array(img)

def b10_the_meeting(w, h, n):
    """30s deadpan 'how this network runs' bit."""
    part1 = ["this network is run by", "one guy,"]
    part2 = ["an android phone,"]
    part3 = ["and seventeen", "free gpu accounts."]
    for i in range(n):
        img = Image.fromarray(black_frame(w, h))
        sz = 52 if w <= 720 else 46
        q = i / n
        if q < 0.33:
            draw_centered_text(img, part1, sz, bold=False)
        elif q < 0.62:
            draw_centered_text(img, part1 + [""] + part2, sz, bold=False)
        else:
            draw_centered_text(img, part1 + [""] + part2 + [""] + part3, sz, bold=False)
        if q > 0.9:
            draw_corner_tag(img, 24)
        yield np.array(img)

def b11_schedule_rumor(w, h, n):
    """10s fake schedule card — the schedule is a rumor."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the schedule", "is a rumor.", "the episodes arrive", "when they arrive."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b12_werewolf_forecast(w, h, n):
    """15s show promo — tonight's forecast: werewolves."""
    for i in range(n):
        t = i / FPS
        bg = wave_distort(trippy_frame(w, h, t, seed=9.4, sat=0.8), t, amp=10)
        bg = (bg.astype(np.float32)*0.55).astype(np.uint8)
        img = Image.fromarray(bg)
        sz = 60 if w <= 720 else 54
        a = min(1.0, i/15)
        if a > 0:
            draw_centered_text(img, ["tonight's forecast:", "werewolves.", "dress accordingly."], sz, stroke=2)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b13_comments_focus_group(w, h, n):
    """10s deadpan one-liner — the comments section is not a focus group."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the comments section", "is not a focus group."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b14_dsw_promo(w, h, n):
    """15s show promo — damn shit's wild."""
    for i in range(n):
        t = i / FPS
        bg = wave_distort(trippy_frame(w, h, t, seed=11.8, sat=0.8), t, amp=10)
        bg = (bg.astype(np.float32)*0.55).astype(np.uint8)
        img = Image.fromarray(bg)
        sz = 60 if w <= 720 else 54
        a = min(1.0, i/15)
        if a > 0:
            draw_centered_text(img, ["damn shit's wild.", "the name is the review."], sz, stroke=2)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b15_rerun_new(w, h, n):
    """10s deadpan one-liner — the rerun is also new."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the rerun is also new.", "you weren't paying", "attention the first time."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b16_it_is(w, h, n):
    """15s show promo — it is what it is."""
    for i in range(n):
        t = i / FPS
        bg = wave_distort(trippy_frame(w, h, t, seed=13.2, sat=0.8), t, amp=10)
        bg = (bg.astype(np.float32)*0.55).astype(np.uint8)
        img = Image.fromarray(bg)
        sz = 60 if w <= 720 else 54
        a = min(1.0, i/15)
        if a > 0:
            draw_centered_text(img, ["it is what it is.", "it was what it was.", "it will be what it is."], sz, stroke=2)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b17_tv_on(w, h, n):
    """10s deadpan one-liner — the tv is on, nobody's watching."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the tv is on.", "nobody's watching.", "perfect audience."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b18_never_sleeps(w, h, n):
    """10s deadpan one-liner — this channel never sleeps, it just stares."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["this channel", "never sleeps.", "it just stares."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b19_static_show(w, h, n):
    """10s deadpan one-liner — the static is part of the show."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the static is", "part of the show.", "do not adjust your set."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b20_buffering(w, h, n):
    """10s deadpan one-liner — the buffering is part of the show."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the buffering", "is part of the show.", "sit with it."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b21_early_late(w, h, n):
    """10s deadpan one-liner — you're early, the episode is late."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["you're early.", "the episode is late.", "we're all just here now."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b22_remote_gone(w, h, n):
    """10s deadpan one-liner — the remote is gone, the channel stays."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the remote is gone.", "the channel stays.", "that's the deal."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b23_still_here(w, h, n):
    """10s deadpan one-liner — the episode ended an hour ago, you're still here."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the episode ended an hour ago.", "you're still here.", "so are we."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b24_between_shows(w, h, n):
    """10s deadpan one-liner — this is not a test, this is the part between the shows."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["this is not a test.", "this is also not the show.", "it's the part between the shows."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b25_up_next(w, h, n):
    """10s deadpan one-liner — up next: more of this."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["up next: more of this.", "after that: also this.", "the schedule has spoken."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b26_still_on(w, h, n):
    """10s deadpan one-liner — the tv is still on, so are you."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the tv is still on.", "so are you.", "neither of you is leaving."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b27_next_week(w, h, n):
    """10s deadpan one-liner — the episode you wanted is next week."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the episode you wanted", "is next week.", "this one is tonight."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b28_no_ads(w, h, n):
    """10s deadpan one-liner — there are no ads here, only the show."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["there are no ads here.", "there is only the show.", "and this."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b29_channel_changed(w, h, n):
    """10s deadpan one-liner — the channel changed, you're still on it."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the channel changed.", "you're still on it.", "that's not an accident."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b30_missed_nothing(w, h, n):
    """10s deadpan one-liner — you missed nothing, it all happened while you were here."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["you missed nothing.", "it all happened", "while you were here."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b31_episode_started(w, h, n):
    """10s deadpan one-liner — the episode started ten seconds ago."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the episode started", "ten seconds ago.", "you're already behind."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b32_schedule_pencil(w, h, n):
    """10s deadpan one-liner — the network has a schedule, written in pencil."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the network has a schedule.", "it's written in pencil.", "the pencil is lying."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b33_guide_wrong(w, h, n):
    """10s deadpan one-liner — the show is on, the guide is wrong."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the show is on.", "the guide is wrong.", "trust the show."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b34_schedule_checked_out(w, h, n):
    """10s deadpan one-liner — we checked the schedule, it checked out."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["we checked the schedule.", "the schedule checked out.", "nobody knows where it went."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b35_lost_remote(w, h, n):
    """10s deadpan one-liner — we lost the remote, we found the show."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["we lost the remote.", "we found the show.", "fair trade."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b36_guide_says_nothing(w, h, n):
    """10s deadpan one-liner — the guide says nothing is on."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the guide says nothing is on.", "the guide has never", "watched this channel."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b37_tv_wants(w, h, n):
    """10s deadpan one-liner — we asked the tv what it wants to watch."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["we asked the tv", "what it wants to watch.", "it said this."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b38_two_buttons(w, h, n):
    """10s deadpan one-liner — the remote has two buttons now."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the remote has two buttons now.", "both of them are", "this channel."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b39_volume_down(w, h, n):
    """10s deadpan one-liner — we turned the volume down, the show got louder."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["we turned the volume down.", "the show got louder.", "we're not touching it again."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b40_somewhere_tv(w, h, n):
    """10s deadpan one-liner — somewhere, a tv is on, it's this channel."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["somewhere, a tv is on.", "it's this channel.", "it has always been this channel."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b41_day_off(w, h, n):
    """10s deadpan one-liner — the tv asked for a day off, we gave it the show instead."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["the tv asked for a day off.", "we gave it the show instead."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

def b42_no_off_switch(w, h, n):
    """10s deadpan one-liner — this channel has no off switch, only a volume knob that goes up."""
    for i in range(n):
        a = min(1.0, i/10)
        fr = fade(black_frame(w, h), a)
        img = Image.fromarray(fr)
        sz = 52 if w <= 720 else 46
        draw_centered_text(img, ["this channel has no off switch.", "it has a volume knob.", "it only goes up."], sz, bold=False)
        draw_corner_tag(img, 24)
        yield np.array(img)

BUMPS = [
    ("01-stay-trippedd", 5, b01_stay_trippedd, "5s black-card network ID — STAY TRIPPEDD"),
    ("02-couch", 5, b02_couch, "5s deadpan one-liner"),
    ("03-trippy-id", 10, b03_trippy_id, "10s wavy tie-dye network ID"),
    ("04-tonight", 10, b04_tonight, "10s fake schedule card"),
    ("05-dear-trippedd", 10, b05_dear_trippedd, "10s sarcastic viewer Q&A"),
    ("06-typewriter", 15, b06_typewriter, "15s typewriter thought"),
    ("07-wg-promo", 15, b07_wg_promo, "15s Wizard Gang promo"),
    ("08-cd-promo", 15, b08_cd_promo, "15s Concrete Dragon game promo"),
    ("09-ambient-drift", 30, b09_ambient_drift, "30s slow ambient mood piece"),
    ("10-the-meeting", 30, b10_the_meeting, "30s deadpan 'how this network runs' bit"),
    ("11-schedule-rumor", 10, b11_schedule_rumor, "10s fake schedule card — the schedule is a rumor"),
    ("12-werewolf-forecast", 15, b12_werewolf_forecast, "15s show promo — tonight's forecast: werewolves"),
    ("13-comments-focus-group", 10, b13_comments_focus_group, "10s deadpan one-liner — the comments section is not a focus group (added 2026-10-27, batch 3)"),
    ("14-dsw-promo", 15, b14_dsw_promo, "15s show promo — damn shit's wild, the name is the review (added 2026-10-27, batch 3)"),
    ("15-rerun-new", 10, b15_rerun_new, "10s deadpan one-liner — the rerun is also new (added 2026-10-30, batch 4)"),
    ("16-it-is", 15, b16_it_is, "15s show promo — it is what it is (added 2026-10-30, batch 4)"),
    ("17-tv-on", 10, b17_tv_on, "10s deadpan one-liner — the tv is on, nobody's watching, perfect audience (added 2026-11-01, batch 5)"),
    ("18-never-sleeps", 10, b18_never_sleeps, "10s deadpan one-liner — this channel never sleeps, it just stares (added 2026-11-02, batch 5)"),
    ("19-static-show", 10, b19_static_show, "10s deadpan one-liner — the static is part of the show, do not adjust your set (added 2026-11-04, batch 6)"),
    ("20-buffering", 10, b20_buffering, "10s deadpan one-liner — the buffering is part of the show, sit with it (added 2026-11-05, batch 6)"),
    ("21-early-late", 10, b21_early_late, "10s deadpan one-liner — you're early, the episode is late (added 2026-11-06, batch 7)"),
    ("22-remote-gone", 10, b22_remote_gone, "10s deadpan one-liner — the remote is gone, the channel stays (added 2026-11-06, batch 7)"),
    ("23-still-here", 10, b23_still_here, "10s deadpan one-liner — the episode ended an hour ago, you're still here (added 2026-11-07, batch 8)"),
    ("24-between-shows", 10, b24_between_shows, "10s deadpan one-liner — this is not a test, this is the part between the shows (added 2026-11-07, batch 8)"),
    ("25-up-next", 10, b25_up_next, "10s deadpan one-liner — up next: more of this, after that: also this (added 2026-11-08, batch 9)"),
    ("26-still-on", 10, b26_still_on, "10s deadpan one-liner — the tv is still on, so are you (added 2026-11-08, batch 9)"),
    ("27-next-week", 10, b27_next_week, "10s deadpan one-liner — the episode you wanted is next week (added 2026-11-10, batch 10)"),
    ("28-no-ads", 10, b28_no_ads, "10s deadpan one-liner — there are no ads here, only the show (added 2026-11-10, batch 10)"),
    ("29-channel-changed", 10, b29_channel_changed, "10s deadpan one-liner — the channel changed, you're still on it (added 2026-11-11, batch 11)"),
    ("30-missed-nothing", 10, b30_missed_nothing, "10s deadpan one-liner — you missed nothing, it all happened while you were here (added 2026-11-11, batch 11)"),
    ("31-episode-started", 10, b31_episode_started, "10s deadpan one-liner — the episode started ten seconds ago, you're already behind (added 2026-11-12, batch 12)"),
    ("32-schedule-pencil", 10, b32_schedule_pencil, "10s deadpan one-liner — the network has a schedule, written in pencil, the pencil is lying (added 2026-11-12, batch 12)"),
    ("33-guide-wrong", 10, b33_guide_wrong, "10s deadpan one-liner — the show is on, the guide is wrong, trust the show (added 2026-11-13, batch 13)"),
    ("34-schedule-checked-out", 10, b34_schedule_checked_out, "10s deadpan one-liner — we checked the schedule, the schedule checked out (added 2026-11-13, batch 13)"),
    ("35-lost-remote", 10, b35_lost_remote, "10s deadpan one-liner — we lost the remote, we found the show, fair trade (added 2026-11-14, batch 14)"),
    ("36-guide-says-nothing", 10, b36_guide_says_nothing, "10s deadpan one-liner — the guide says nothing is on (added 2026-11-14, batch 14)"),
    ("37-tv-wants", 10, b37_tv_wants, "10s deadpan one-liner — we asked the tv what it wants to watch (added 2026-11-15, batch 15)"),
    ("38-two-buttons", 10, b38_two_buttons, "10s deadpan one-liner — the remote has two buttons now (added 2026-11-15, batch 15)"),
    ("39-volume-down", 10, b39_volume_down, "10s deadpan one-liner — we turned the volume down, the show got louder (added 2026-11-17, batch 16)"),
    ("40-somewhere-tv", 10, b40_somewhere_tv, "10s deadpan one-liner — somewhere, a tv is on, it's this channel (added 2026-11-17, batch 16)"),
    ("41-day-off", 10, b41_day_off, "10s deadpan one-liner — the tv asked for a day off, we gave it the show instead (added 2026-11-18, batch 17)"),
    ("42-no-off-switch", 10, b42_no_off_switch, "10s deadpan one-liner — this channel has no off switch, only a volume knob that goes up (added 2026-11-18, batch 17)"),
]

def render_one(slug, secs, fn, w, h, subdir):
    n = secs * FPS
    path = os.path.join(OUT, subdir, f"bump-{slug}-{secs}s.mp4")
    p = pipe_ffmpeg(path, w, h, FPS, secs)
    for fr in fn(w, h, n):
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    print(f"  wrote {path}", flush=True)
    return path

def main():
    os.makedirs(OUT, exist_ok=True)
    thumbs = []
    for slug, secs, fn, desc in BUMPS:
        print(f"bump {slug} ({secs}s) — {desc}", flush=True)
        pv = render_one(slug, secs, fn, *VERT, "vert")
        ph = render_one(slug, secs, fn, *HORZ, "horiz")
        # grab mid frame for contact sheet
        thumbs.append((slug, secs, pv))
    # contact sheet
    cols = 5
    tw, th = 144, 256
    rows = math.ceil(len(thumbs)/cols)
    sheet = Image.new("RGB", (cols*tw, rows*(th+24)), (20,20,20))
    d = ImageDraw.Draw(sheet)
    lf = font(14, bold=False)
    for idx, (slug, secs, pv) in enumerate(thumbs):
        cap = subprocess.run(["ffmpeg","-y","-v","error","-ss",str(secs//2),
                              "-i",pv,"-frames:v","1","-f","image2pipe",
                              "-vcodec","png","-"], capture_output=True)
        im = Image.open(__import__("io").BytesIO(cap.stdout)).convert("RGB").resize((tw,th))
        x, y = (idx%cols)*tw, (idx//cols)*(th+24)
        sheet.paste(im, (x,y))
        d.text((x+4, y+th+4), f"{slug} {secs}s", font=lf, fill=(220,220,220))
    sheet.save(os.path.join(OUT, "contact-sheet.png"))
    print("contact sheet saved", flush=True)

if __name__ == "__main__":
    main()
