import subprocess, sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
ts = [1, 3.5, 5.5, 8, 10, 12.5, 14.5, 17, 19, 21.5, 23.5, 26, 28, 30.5, 32.5, 35, 37, 39.5]
W = Image.new("RGB", (180 * 9, 640))
for i, t in enumerate(ts):
    p = f"/tmp/vs_{i}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf", "scale=180:320", p], check=True)
    W.paste(Image.open(p), ((i % 9) * 180, (i // 9) * 320))
W.save(out, quality=85)
