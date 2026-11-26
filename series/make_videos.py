"""Render the 'What if every ___ vanished overnight?' shorts.

Usage: python make_videos.py [slug ...]   (no args = all topics, skipping ones already rendered)
Needs: Pillow, kokoro-onnx, soundfile, ffmpeg. Kokoro model files path in KOKORO_DIR.
"""
import os, sys, json, subprocess, textwrap
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from topics import T

KOKORO_DIR = os.environ.get("KOKORO_DIR", "/tmp/claude-0/-home-user/9ce2b150-ed7a-5615-9005-57f0eb1d3b0b/scratchpad/vo")
OUT = os.path.join(HERE, "out"); BUILD = os.path.join(HERE, "build")
W, H, FPS = 1080, 1920, 30
SCENE = 4.5; N_SCENES = 9; DUR = SCENE * N_SCENES
HANDLE = "@whatifitvanished"
VOICE = "am_michael"

NAVY_TOP, NAVY_BOT = (14, 21, 48), (27, 38, 80)
YELLOW, WHITE, GREY = (245, 184, 46), (255, 255, 255), (214, 219, 232)
WATER, WAVE = (22, 46, 78), (44, 82, 122)
HORIZON = 1380

FD = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(FD + name, size)
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# ---------- static layers ----------
def make_static():
    os.makedirs(BUILD, exist_ok=True)
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        f = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * f) for a, b in zip(NAVY_TOP, NAVY_BOT)))
    d.rectangle([0, HORIZON, W, H], fill=WATER)
    d.line([(0, HORIZON), (W, HORIZON)], fill=(60, 98, 140), width=4)
    bg.save(f"{BUILD}/bg.png")
    # seamless water tile, 2 periods wide so it can scroll by one period
    tile = Image.new("RGBA", (W * 2, H - HORIZON - 8), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    rng = np.random.default_rng(7)
    for row, y in enumerate(range(30, tile.height, 46)):
        x = rng.integers(0, 120)
        while x < W:
            ln = int(rng.integers(40, 120))
            for k in (0, W):
                td.rounded_rectangle([x + k, y, x + k + ln, y + 6], 3, fill=WAVE + (255,))
            x += ln + int(rng.integers(60, 180))
    tile.save(f"{BUILD}/water.png")
    top = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    f = font("Inter-SemiBold.otf", 34)
    tw = td.textlength(HANDLE, font=f)
    td.text(((W - tw) / 2, H - 110), HANDLE, font=f, fill=(255, 255, 255, 150))
    top.save(f"{BUILD}/top.png")
    Image.new("RGBA", (W, 12), YELLOW + (255,)).save(f"{BUILD}/bar.png")

# ---------- scene cards ----------
def wrap_fit(draw, text, fname, max_size, min_size, max_w, max_lines):
    for size in range(max_size, min_size - 1, -6):
        f = font(fname, size)
        words, lines, cur = text.split(), [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if draw.textlength(t, font=f) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur); cur = w_
        lines.append(cur)
        if len(lines) <= max_lines and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines
    return f, lines

def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI_FONT, 109)
    im = Image.new("RGBA", (180, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    bb = im.getbbox()
    im = im.crop(bb) if bb else im
    r = size / max(im.size)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)

def card(path, kicker, headline, sub, emoji=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 420
    if kicker:
        fk, kl = wrap_fit(d, kicker, "Inter-ExtraBold.otf", 54, 36, 940, 2)
        for l in kl:
            tw = d.textlength(l, font=fk)
            d.text(((W - tw) / 2, y), l, font=fk, fill=YELLOW); y += int(fk.size * 1.2)
        y += 18
    fh, hl = wrap_fit(d, headline, "InterDisplay-Black.otf", 200, 90, 980, 3)
    for l in hl:
        tw = d.textlength(l, font=fh)
        d.text(((W - tw) / 2, y), l, font=fh, fill=WHITE); y += int(fh.size * 1.02)
    y += 30
    if sub:
        fs, sl = wrap_fit(d, sub, "Inter-Medium.otf", 46, 34, 900, 3)
        for l in sl:
            tw = d.textlength(l, font=fs)
            d.text(((W - tw) / 2, y), l, font=fs, fill=GREY); y += int(fs.size * 1.3)
    if emoji:
        e = emoji_img(emoji, 300)
        ey = max(y + 40, HORIZON - e.height - 30)
        im.alpha_composite(e, ((W - e.width) // 2, min(ey, HORIZON - 60)))
    im.save(path)

def scenes_for(t):
    subj = t["subject"]; spoken = t["spoken"]
    every = not subj.startswith(("THE ", "EARTH'S", "ANTARCTICA'S", "GREENLAND'S"))
    head = ("EVERY " + subj) if every else subj
    sub = "on Earth vanished overnight?" if every else "vanished overnight?"
    hook_say = f"What if every {spoken} on Earth vanished overnight?" if every else f"What if {spoken} vanished overnight?"
    sc = [("WHAT IF", head, sub, hook_say, t["emoji"])]
    sc += [(k, h, s, n, None) for k, h, s, n in t["scenes"]]
    sc.append(("FOLLOW FOR MORE", "WHAT VANISHES NEXT?", "Comment below", "What vanishes next? Comment below, and follow for more.", None))
    return sc

# ---------- audio ----------
_K = None
def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(f"{KOKORO_DIR}/kokoro.onnx", f"{KOKORO_DIR}/voices.bin")
    return _K

def narration(lines, path):
    k = kokoro(); sr = 24000
    out = np.zeros(int(DUR * sr), dtype=np.float32); log = []
    for i, text in enumerate(lines):
        slot = SCENE - 0.35; speed = 1.05
        while True:
            a, sr = k.create(text, voice=VOICE, speed=speed, lang="en-us")
            if len(a) / sr <= slot or speed >= 1.45: break
            speed += 0.05
        a = a[: int(slot * sr)]
        s = int((i * SCENE + 0.12) * sr); out[s:s + len(a)] += a
        log.append(dict(scene=i, secs=round(len(a) / sr, 2), speed=round(speed, 2), text=text))
    sf.write(path, out, sr)
    return log

def pad_track():
    p = f"{BUILD}/pad.wav"
    if os.path.exists(p): return p
    expr = ("0.5*sin(2*PI*110*t)+0.35*sin(2*PI*164.81*t)+0.3*sin(2*PI*220*t)+0.2*sin(2*PI*261.63*t)")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    f"aevalsrc='{expr}':s=48000:d={DUR}",
                    "-af", "tremolo=f=0.15:d=0.5,lowpass=f=700,afade=t=in:d=2,afade=t=out:st=%.1f:d=2.5,volume=0.08" % (DUR - 2.5),
                    p], check=True)
    return p

# ---------- render ----------
def render(t, idx):
    slug = t["slug"]; name = f"{idx:02d}-{slug}"
    final = f"{OUT}/{name}.mp4"
    if os.path.exists(final) and "--force" not in sys.argv: return None
    bd = f"{BUILD}/{slug}"; os.makedirs(bd, exist_ok=True)
    sc = scenes_for(t)
    for i, (k, h, s, _, e) in enumerate(sc):
        card(f"{bd}/c{i}.png", k, h, s, e)
    log = narration([x[3] for x in sc], f"{bd}/voice.wav")
    pad = pad_track()
    inp = ["-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", f"{BUILD}/bg.png",
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", f"{BUILD}/water.png",
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", f"{BUILD}/top.png",
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", f"{BUILD}/bar.png"]
    for i in range(N_SCENES):
        a = i * SCENE
        inp += ["-loop", "1", "-framerate", str(FPS), "-ss", "0", "-t", str(SCENE), "-itsoffset", str(a), "-i", f"{bd}/c{i}.png"]
    inp += ["-i", f"{bd}/voice.wav", "-i", pad]
    f = [f"[0:v][1:v]overlay=x='-mod(t*36,{W})':y={HORIZON + 8}[v0]",
         "[v0][2:v]overlay=0:0[v1]",
         f"[v1][3:v]overlay=x='-{W}+{W}*t/{DUR}':y=0[v2]"]
    cur = "v2"
    for i in range(N_SCENES):
        a, b = i * SCENE, (i + 1) * SCENE
        f.append(f"[{4 + i}:v]format=rgba,fade=t=in:st={a}:d=0.35:alpha=1,fade=t=out:st={b - 0.3}:d=0.3:alpha=1[c{i}]")
        f.append(f"[{cur}][c{i}]overlay=x=0:y='34*max(0,1-(t-{a})/0.4)':eof_action=pass:enable='between(t,{a},{b})'[o{i}]")
        cur = f"o{i}"
    f.append(f"[{cur}]format=yuv420p[vout]")
    f.append(f"[{4 + N_SCENES}:a]aresample=48000,volume=1.0[va];[{5 + N_SCENES}:a]aresample=48000[pa];"
             f"[va][pa]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    os.makedirs(OUT, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(f),
           "-map", "[vout]", "-map", "[aout]", "-t", str(DUR), "-r", str(FPS),
           "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", final + ".tmp.mp4"]
    subprocess.run(cmd, check=True)
    os.replace(final + ".tmp.mp4", final)
    json.dump(log, open(f"{bd}/voice_log.json", "w"), indent=1)
    return log

def caption(t, idx):
    sc = scenes_for(t)
    hook = sc[0][3]
    facts = " ".join(s[3] for s in sc[1:4])
    return f"{hook} 🤯 {facts}\n\nWhat vanishes next? Drop it in the comments 👇\nFollow {HANDLE} for more.\n\n#whatif #hypothetical #didyouknow #facts {t['tags']}"

if __name__ == "__main__":
    make_static()
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    for idx, t in enumerate(T, 1):
        if want and t["slug"] not in want: continue
        log = render(t, idx)
        fast = [l for l in (log or []) if l["speed"] >= 1.3]
        print(f"{idx:02d} {t['slug']}: {'skipped (exists)' if log is None else 'done'}"
              + (f"  fast lines: {[(l['scene'], l['speed']) for l in fast]}" if fast else ""), flush=True)
    with open(f"{OUT}/captions.md", "w") as fh:
        for idx, t in enumerate(T, 1):
            fh.write(f"## {idx:02d}-{t['slug']}.mp4\n\n{caption(t, idx)}\n\n")
