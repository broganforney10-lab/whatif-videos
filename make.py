import math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/"
BLACK = ImageFont.truetype(F + "InterDisplay-Black.otf", 150)
BIG = ImageFont.truetype(F + "InterDisplay-Black.otf", 210)
HEAD = ImageFont.truetype(F + "Inter-ExtraBold.otf", 84)
BODY = ImageFont.truetype(F + "Inter-SemiBold.otf", 58)
SMALL = ImageFont.truetype(F + "Inter-Bold.otf", 40)
ACCENT = (255, 196, 61)

# scene: (duration, kicker, big, body, bridge_mode)
import json
TOPIC = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "topics/bridges.json"))
SCENES = [(sc["seconds"], sc["kicker"], sc["big"], sc.get("body", ""), sc.get("bridge", "gap")) for sc in TOPIC["scenes"]]

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def background():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H
        c = (int(8 + 14 * k), int(14 + 22 * k), int(34 + 40 * k))
        d.line([(0, y), (W, y)], fill=c)
    # water
    wy = 1450
    for y in range(wy, H):
        k = (y - wy) / (H - wy)
        d.line([(0, y), (W, y)], fill=(int(10 + 10 * k), int(40 + 20 * k), int(70 + 25 * k)))
    return img

BG = background()
WATER_Y = 1450

def draw_water(d, t):
    for i in range(14):
        y = WATER_Y + 30 + i * 32
        off = (t * 60 + i * 37) % 160
        for x in range(-160, W + 160, 160):
            d.line([(x + off, y), (x + off + 70, y)], fill=(70, 120, 160), width=3)

def draw_bridge(d, alpha, t=0.0, broken=False):
    """Suspension bridge across the water; alpha 0..1."""
    if alpha <= 0:
        return
    col = tuple(int(c * alpha + bg * (1 - alpha)) for c, bg in zip((205, 215, 230), (20, 50, 85)))
    deck_y = WATER_Y - 70
    left, right = -40, W + 40
    towers = [260, 820]
    # deck
    d.rectangle([left, deck_y, right, deck_y + 22], fill=col)
    for tx in towers:
        d.rectangle([tx - 18, deck_y - 330, tx + 18, WATER_Y + 40], fill=col)
    # main cable
    pts = []
    for i in range(0, 101):
        x = towers[0] + (towers[1] - towers[0]) * i / 100
        u = (x - (towers[0] + towers[1]) / 2) / ((towers[1] - towers[0]) / 2)
        y = deck_y - 330 + (1 - u * u) * 300
        pts.append((x, y))
    d.line(pts, fill=col, width=7)
    for x, y in pts[::6]:
        d.line([(x, y), (x, deck_y)], fill=col, width=3)
    d.line([(left, deck_y - 10), (towers[0], deck_y - 330)], fill=col, width=7)
    d.line([(towers[1], deck_y - 330), (right, deck_y - 10)], fill=col, width=7)

def draw_gap(d):
    # stumps on each bank where the bridge used to be
    deck_y = WATER_Y - 70
    col = (60, 80, 110)
    d.rectangle([-10, deck_y, 120, deck_y + 22], fill=col)
    d.rectangle([W - 120, deck_y, W + 10, deck_y + 22], fill=col)
    d.polygon([(0, WATER_Y), (150, WATER_Y), (120, deck_y + 22), (0, deck_y + 22)], fill=(40, 55, 75))
    d.polygon([(W, WATER_Y), (W - 150, WATER_Y), (W - 120, deck_y + 22), (W, deck_y + 22)], fill=(40, 55, 75))

def draw_boats(d, t):
    for i, (bx, speed) in enumerate([(150, 70), (600, -50), (350, 40)]):
        x = (bx + speed * t) % (W + 200) - 100
        y = WATER_Y + 90 + i * 110
        d.polygon([(x, y), (x + 170, y), (x + 140, y + 40), (x + 30, y + 40)], fill=ACCENT)
        d.rectangle([x + 55, y - 45, x + 115, y], fill=(230, 230, 240))

def particles(d, t, seed=7):
    rnd = random.Random(seed)
    for _ in range(260):
        x0 = rnd.uniform(0, W)
        y0 = rnd.uniform(WATER_Y - 420, WATER_Y)
        vy = rnd.uniform(-120, -40)
        vx = rnd.uniform(-40, 40)
        x = x0 + vx * t
        y = y0 + vy * t
        a = max(0, 1 - t / 1.4)
        if a <= 0:
            continue
        r = rnd.uniform(2, 6)
        c = (int(205 * a + 20 * (1 - a)), int(215 * a + 40 * (1 - a)), int(230 * a + 70 * (1 - a)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def text_center(d, y, txt, font, fill, spacing=10):
    lines = txt.split("\n")
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((W - w) / 2 - bb[0], y - bb[1]), ln, font=font, fill=fill)
        y += h + spacing
    return y

def fade_col(c, a):
    return tuple(int(v * a) for v in c)

def frame(si, f):
    dur, kicker, big, body, mode = SCENES[si]
    t = f / FPS
    img = BG.copy()
    d = ImageDraw.Draw(img)
    draw_water(d, t + si * 3)
    if mode == "vanish":
        # bridge visible, then dissolves from 1.8s to 3.0s
        if t < 1.8:
            draw_bridge(d, 1.0)
        else:
            k = (t - 1.8) / 1.2
            draw_bridge(d, max(0, 1 - k))
            draw_gap(d)
            particles(d, t - 1.8)
    elif mode == "boats":
        draw_gap(d)
        draw_boats(d, t)
    else:
        draw_gap(d)

    a1 = ease(t / 0.35)
    a2 = ease((t - 0.25) / 0.4)
    a3 = ease((t - 0.6) / 0.4)
    y = 450
    kf = HEAD
    while d.textbbox((0, 0), kicker, font=kf)[2] > W - 100:
        kf = ImageFont.truetype(F + "Inter-ExtraBold.otf", kf.size - 4)
    y = text_center(d, y + (1 - a1) * 40, kicker, kf, fade_col(ACCENT, a1)) + 40
    font = BIG if "\n" not in big and len(big) <= 8 else BLACK
    y = text_center(d, y + (1 - a2) * 60, big, font, fade_col((255, 255, 255), a2), spacing=20) + 50
    if body:
        text_center(d, y + (1 - a3) * 30, body, BODY, fade_col((210, 220, 235), a3), spacing=18)
    # brand
    text_center(d, 1840, "@whatifitvanished", SMALL, (150, 170, 200))
    # progress bar
    total = sum(s[0] for s in SCENES)
    done = sum(s[0] for s in SCENES[:si]) + t
    d.rectangle([0, 0, int(W * done / total), 10], fill=ACCENT)
    # fade to black at end of scene / in at start
    k = min(1.0, t / 0.15, (dur - t) / 0.15)
    if k < 1:
        img = Image.blend(Image.new("RGB", (W, H)), img, max(0, k))
    return img

def render_scene(si, out):
    dur = SCENES[si][0]
    n = int(round(dur * FPS))
    tmp = out.replace(".mp4", ".part.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20",
                          "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for f in range(n):
        p.stdin.write(frame(si, f).tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.rename(tmp, out)

if __name__ == "__main__":
    if sys.argv[1] == "stills":
        for si, f in [(0, 10), (0, 70), (1, 60), (6, 60), (8, 60)]:
            frame(si, f).save(f"still_{si}_{f}.jpg", quality=90)
    else:
        files = []
        for si in range(len(SCENES)):
            out = f"scene{si}.mp4"
            render_scene(si, out)
            files.append(out)
        with open("list.txt", "w") as fh:
            fh.write("".join(f"file '{x}'\n" for x in files))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "list.txt",
                        "-c", "copy", "-movflags", "+faststart", TOPIC["output"]], check=True)
