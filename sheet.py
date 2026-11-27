import glob, sys
from PIL import Image

vid, out = sys.argv[1], sys.argv[2]
fs = sorted(glob.glob(f"/home/claude/bb/3d/stills/{vid}-*.jpg"), key=lambda f: int(f.rsplit("-", 1)[1][:-4]))
ims = [Image.open(f).resize((180, 320)) for f in fs]
W = Image.new("RGB", (180 * 9, 320 * ((len(ims) + 8) // 9)))
for i, im in enumerate(ims):
    W.paste(im, ((i % 9) * 180, (i // 9) * 320))
W.save(out, quality=85)
