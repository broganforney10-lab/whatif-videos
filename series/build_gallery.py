"""Build the gallery folder: videos/, posters/, and data.js for gallery.html."""
import os, sys, json, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from topics import T
from make_videos import scenes_for, caption

G = os.path.join(HERE, "gallery")
os.makedirs(f"{G}/videos", exist_ok=True); os.makedirs(f"{G}/posters", exist_ok=True)

def poster(src, dst):
    if not os.path.exists(dst):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.2", "-i", src, "-frames:v", "1",
                        "-vf", "scale=360:-1", "-q:v", "5", dst], check=True)

items = []
bridges = "/home/user/bridges_short_voiceover.mp4"
if os.path.exists(bridges):
    shutil.copy(bridges, f"{G}/videos/00-bridges.mp4")
    poster(bridges, f"{G}/posters/00-bridges.jpg")
    items.append(dict(n=0, title="Every bridge", file="videos/00-bridges.mp4", poster="posters/00-bridges.jpg",
                      caption="What if every bridge on Earth vanished overnight? 🤯 The U.S. alone has 624,000 bridges. New York City loses 789 bridges and tunnels. By day two, shelves are empty.\n\nWhat vanishes next? Drop it in the comments 👇\nFollow @whatifitvanished for more.\n\n#whatif #hypothetical #didyouknow #facts #bridges #cities",
                      check=["624,000 U.S. bridges", "789 NYC bridges and tunnels", "~2,500 Hamburg bridges"], note="Your original from Claude chat, with the new voiceover."))
for i, t in enumerate(T, 1):
    name = f"{i:02d}-{t['slug']}"
    src = f"{HERE}/out/{name}.mp4"
    if not os.path.exists(src): continue
    shutil.copy(src, f"{G}/videos/{name}.mp4")
    poster(src, f"{G}/posters/{name}.jpg")
    sc = scenes_for(t)
    check = [f"{h} {s}".strip() if re.search(r"\d|~|HALF|BILLION|TRILLION", h) else None for _, h, s, _, _ in sc[1:-1]]
    title = sc[0][1].capitalize() if not sc[0][1].startswith("EVERY") else "Every " + t["subject"].lower()
    items.append(dict(n=i, title=title, file=f"videos/{name}.mp4", poster=f"posters/{name}.jpg",
                      caption=caption(t, i), check=[c for c in check if c], note=""))
with open(f"{G}/data.json", "w") as fh:
    fh.write("[\n" + ",\n".join(json.dumps(x, ensure_ascii=False) for x in items) + "\n]\n")
print(len(items), "items")
