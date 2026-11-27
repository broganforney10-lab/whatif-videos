"""Join 10 finished 3D shorts into one 16:9 YouTube compilation (~6.5 min).

  <kokoro-venv>/bin/python compile.py            # builds every compilation in COMPS
  <kokoro-venv>/bin/python compile.py tiny       # just one

Each short is trimmed before its "follow for more" outro, placed on a blurred 16:9 background,
and labelled "#N + topic" on the left panel. A narrated title card opens the video and an
outro card closes it. Output: out_comp/<key>.mp4 plus out_comp/<key>-thumb.jpg (1280x720).
"""
import glob, importlib.util, os, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/user/whatif"  # series folder (topics.py, make_videos.py)
OUT = f"{HERE}/out_comp"
W, H, FPS = 1920, 1080, 30
CLIP = 36.0  # 8 scenes x 4.5 s: the hook plus 7 facts, without the outro scene
FONT = f"{HERE}/public/fonts/InterDisplay-Black.otf"
FONT2 = f"{HERE}/public/fonts/Inter-Bold.otf"

COMPS = {
    "tiny": ("10 Tiny Things That Hold the World Together",
             "Ten tiny things that quietly hold the whole world together. Number one might surprise you.",
             "horseshoe-crabs fig-wasps krill dung-beetles ladybugs oysters parrotfish yeast gut-bacteria ball-bearings"),
    "animals": ("10 Animals the World Can't Live Without",
                "Ten animals the world can't live without. What happens if they vanish overnight?",
                "bees earthworms plankton bats vultures sharks wolves sea-otters beavers ants"),
    "tech": ("10 Inventions That Would Break Modern Life",
             "Ten inventions that would break modern life if they vanished overnight.",
             "internet gps powergrid smartphones satellites microchips barcodes atomic-clocks undersea-cables container-ships"),
    "nature": ("10 Things in Nature We Can't Lose",
               "Ten things in nature we can't afford to lose. Here's what happens if they vanish overnight.",
               "ozone magnetic-field clouds gulf-stream antarctic-ice trees amazon-rainforest coral-reefs wind sahara-dust"),
}


def run(cmd):
    subprocess.run(cmd, check=True)


def load_mv():
    sys.argv = ["mv"]
    spec = importlib.util.spec_from_file_location("mv", f"{SRC}/make_videos.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fit_text(d, text, font_path, max_w, size):
    while size > 20:
        f = ImageFont.truetype(font_path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(font_path, size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def card(path, title, sub, bg_frame=None):
    """Full-frame text card over a darkened, blurred frame (or a plain gradient)."""
    if bg_frame:
        im = Image.open(bg_frame).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
        im = Image.blend(im, Image.new("RGB", (W, H), (10, 12, 30)), 0.55)
    else:
        im = Image.new("RGB", (W, H), (16, 20, 44))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 110)
    lines = wrap(d, title.upper(), f, W - 240)
    y = H // 2 - len(lines) * 62 - 40
    for ln in lines:
        d.text((W // 2, y), ln, font=f, fill="white", anchor="mt", stroke_width=6, stroke_fill="black")
        y += 128
    if sub:
        d.text((W // 2, y + 30), sub, font=ImageFont.truetype(FONT2, 54), fill="#ffd54a", anchor="mt",
               stroke_width=3, stroke_fill="black")
    im.save(path)


def panel(path, n, name):
    """Transparent 1920x1080 overlay: '#n' and the topic name on the left blurred panel."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, max_w = 330, 560
    d.text((cx, 330), f"#{n}", font=ImageFont.truetype(FONT, 230), fill="#ffd54a", anchor="mm",
           stroke_width=8, stroke_fill="black")
    f = fit_text(d, name.upper(), FONT, max_w, 84)
    y = 520
    for ln in wrap(d, name.upper(), f, max_w):
        d.text((cx, y), ln, font=f, fill="white", anchor="mt", stroke_width=5, stroke_fill="black")
        y += f.size + 16
    im.save(path)


ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-maxrate", "1500k", "-bufsize", "3000k",
       "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]


def still_segment(png, wav, dur, out):
    a = ["-i", wav] if wav else ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", png, *a,
         "-filter_complex", f"[0:v]fade=t=in:d=0.4,fade=t=out:st={dur - 0.4}:d=0.4[v];[1:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{dur}[a]",
         "-map", "[v]", "-map", "[a]", "-t", str(dur), *ENC, out])


def clip_segment(src, overlay, out):
    f = (f"[0:v]trim=0:{CLIP},setpts=PTS-STARTPTS,split[a][b];"
         f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.18[bg];"
         f"[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0[v0];[v0][1:v]overlay=0:0,"
         f"fade=t=in:d=0.3,fade=t=out:st={CLIP - 0.3}:d=0.3[v];"
         f"[0:a]atrim=0:{CLIP},asetpts=PTS-STARTPTS,afade=t=out:st={CLIP - 0.4}:d=0.4[aud]")
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", overlay, "-filter_complex", f,
         "-map", "[v]", "-map", "[aud]", *ENC, out])


def thumb(path, title, frames):
    """1280x720: three video frames side by side with the title across the bottom."""
    im = Image.new("RGB", (1280, 720), (16, 20, 44))
    for i, fr in enumerate(frames[:3]):
        t = Image.open(fr).convert("RGB")
        t = t.resize((426, int(426 * t.height / t.width))).crop((0, 0, 426, 470))
        im.paste(t, (i * 427, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 470, 1280, 720), fill=(10, 12, 30))
    f = ImageFont.truetype(FONT, 64)
    y = 492
    for ln in wrap(d, title.upper(), f, 1220)[:3]:
        d.text((640, y), ln, font=f, fill="#ffd54a" if y == 492 else "white", anchor="mt",
               stroke_width=4, stroke_fill="black")
        y += 74
    im.save(path, quality=92)


def build(key, mv):
    title, hook, slugs = COMPS[key]
    slugs = slugs.split()
    names = {t["slug"]: t["spoken"] for t in mv.T}
    tmp = f"{OUT}/tmp-{key}"
    os.makedirs(tmp, exist_ok=True)
    srcs = []
    for s in slugs:
        hits = glob.glob(f"{HERE}/out3d/*-{s}-3d.mp4")
        assert hits, f"missing render for {s}"
        srcs.append(hits[0])
    frames = []
    for i, s in enumerate(srcs[:3]):
        fr = f"{tmp}/frame{i}.png"
        run(["ffmpeg", "-v", "error", "-y", "-ss", "10.3", "-i", s, "-frames:v", "1", fr])
        frames.append(fr)
    # intro: narrated title card
    a, sr = mv.kokoro().create(hook, voice=mv.VOICE, speed=1.05, lang="en-us")
    mv.sf.write(f"{tmp}/intro.wav", a, sr)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", f"{tmp}/intro.wav"]).decode()) + 0.6
    card(f"{tmp}/intro.png", title, "WHAT IF THEY VANISHED OVERNIGHT?", frames[0])
    segs = [f"{tmp}/s00.mp4"]
    still_segment(f"{tmp}/intro.png", f"{tmp}/intro.wav", max(dur, 4.0), segs[0])
    for i, (s, slug) in enumerate(zip(srcs, slugs), 1):
        panel(f"{tmp}/p{i}.png", i, names[slug])
        segs.append(f"{tmp}/s{i:02d}.mp4")
        clip_segment(s, f"{tmp}/p{i}.png", segs[-1])
        print(f"  {key} #{i} {slug}", flush=True)
    card(f"{tmp}/outro.png", "Which one surprised you most?", "COMMENT BELOW + SUBSCRIBE FOR MORE", frames[-1])
    segs.append(f"{tmp}/s99.mp4")
    still_segment(f"{tmp}/outro.png", None, 5.0, segs[-1])
    with open(f"{tmp}/list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in segs)
    final = f"{OUT}/{key}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c", "copy",
         "-movflags", "+faststart", final])
    thumb(f"{OUT}/{key}-thumb.jpg", title, frames)
    print(f"done {final}", flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    args = sys.argv[1:]  # load_mv() resets sys.argv, so read the arguments first
    mv = load_mv()
    for k in ([a for a in args if not a.startswith("--")] or COMPS):
        if os.path.exists(f"{OUT}/{k}.mp4") and "--force" not in args:
            print(f"skip {k} (exists)")
            continue
        build(k, mv)
