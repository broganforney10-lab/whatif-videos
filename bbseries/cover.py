"""Cover + caption for each rendered video.  python3 cover.py  -> ../3d/out_bb/<id>-cover.jpg and captions.md"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bb_topics import T  # noqa: E402
from make_bb import caption  # noqa: E402

OUT = os.path.join(HERE, "..", "3d", "out_bb")
FD = "/usr/share/fonts/opentype/inter/"
YEL, NAVY = (242, 193, 78), (14, 22, 40)


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


COVER_FRAME = {"moon": 60, "120mph": 242, "mound": 377, "nogloves": 917}


def make(idx, t):
    vid = f"{idx:02d}-{t['slug']}"
    if not os.path.exists(f"{OUT}/{vid}.mp4"):
        return None
    fr = COVER_FRAME.get(t["slug"], 242)
    env = dict(os.environ, CLEAN="1", SCALE="1")
    subprocess.run(["node", "stills.mjs", vid, str(fr)], cwd=os.path.join(HERE, "..", "3d"), env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(os.path.join(HERE, "..", "3d", "stills", f"clean-{vid}.jpg")).convert("RGB")
    # cover the burnt-in graphic/caption areas with a soft gradient so the title reads cleanly
    grad = Image.new("L", (1, im.height))
    for y in range(im.height):
        grad.putpixel((0, y), int(215 * max(0, 1 - y / 820) ** 1.3))
    shade = Image.new("RGB", im.size, NAVY)
    im = Image.composite(shade, im, grad.resize(im.size))
    d = ImageDraw.Draw(im)
    title = t["title"].upper()
    f = ImageFont.truetype(FD + "InterDisplay-Black.otf", 118)
    lines = wrap(d, title, f, 960)
    y = 150
    tag = ImageFont.truetype(FD + "InterDisplay-Black.otf", 46)
    tw = d.textlength("BASEBALL WHAT IFS", font=tag)
    d.rounded_rectangle(((1080 - tw) / 2 - 24, y - 12, (1080 + tw) / 2 + 24, y + 62), 14, fill=YEL)
    d.text(((1080 - tw) / 2, y - 2), "BASEBALL WHAT IFS", font=tag, fill=NAVY)
    y += 110
    for i, l in enumerate(lines):
        w = d.textlength(l, font=f)
        d.text(((1080 - w) / 2, y), l, font=f, fill=YEL if i == len(lines) - 1 else (255, 255, 255),
               stroke_width=10, stroke_fill=NAVY)
        y += 128
    out = f"{OUT}/{vid}-cover.jpg"
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    with open(f"{OUT}/captions.md", "w") as fh:
        for idx, t in enumerate(T, 1):
            c = make(idx, t)
            fh.write(f"## {idx:02d}-{t['slug']}\n\nTitle: {t['title']} #shorts\n\n{caption(t)}\n\n")
            print(c)
