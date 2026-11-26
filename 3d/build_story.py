"""Merge a shot list (stories/<slug>.py) with voice data (public/data/<id>.json) -> public/story/<id>.json"""
import json, runpy, sys
vid, slug = sys.argv[1], sys.argv[2]
d = json.load(open(f"public/data/{vid}.json"))
shots = runpy.run_path(f"stories/{slug}.py")["S"]
n, total = len(shots), d["durationInFrames"]
# two shots per narration scene, split each scene in half
out, si = [], 0
for sc in d["scenes"]:
    h = sc["dur"] // 2
    for k, (f, dur) in enumerate([(sc["from"], h), (sc["from"] + h, sc["dur"] - h)]):
        shot = dict(shots[si]); shot["from"], shot["dur"] = f, dur; out.append(shot); si += 1
assert si == n, (si, n)
json.dump({"id": vid, "durationInFrames": total, "audio": d["audio"], "shots": out, "words": d["words"], "mouth": d["mouth"]},
          open(f"public/story/{vid}.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("ok", vid, n, "shots")
