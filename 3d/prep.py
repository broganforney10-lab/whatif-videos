"""Build per-video data for the 2D character versions.

Run with the whatif-videos venv (needs torchaudio + faster-whisper):
  /home/user/whatif-videos/.venv/bin/python prep.py [slug ...]

For each video writes public/data/<id>.json and public/audio/<id>.m4a:
  scenes  - on-screen text + timing + the character's mood for each scene
  words   - caption words with start/end seconds (script spelling, whisper timing)
  mouth   - per-frame mouth openness 0..1 from the voice track (lip-sync)
"""
import importlib.util, json, os, subprocess, sys

import numpy as np
import torchaudio as ta

sys.path.insert(0, "/home/user/whatif-videos")
import voice as V  # noqa: E402  (whisper + script/word alignment helpers)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/user/whatif"
FPS = 30
SCENE = 4.5


def load_topics():
    spec = importlib.util.spec_from_file_location("topics", f"{SRC}/topics.py")
    m = importlib.util.module_from_spec(spec)
    sys.argv = ["topics"]
    spec.loader.exec_module(m)
    spec = importlib.util.spec_from_file_location("mv", f"{SRC}/make_videos.py")
    mv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mv)
    return m.T, mv.scenes_for


def mood_for(i, n, kicker, headline):
    k, h = kicker.upper(), headline.upper()
    if i == 0:
        return "shock"
    if i == n - 1:
        return "wave"
    if "VALUABLE" in k or "WINNER" in k:
        return "excited"
    if k.endswith("?") or h.endswith("?"):
        return "think"
    if any(c.isdigit() for c in h):
        return "point"
    return "worried" if i % 2 else "point"


def mouth_track(wav, n_frames):
    a, sr = ta.load(wav)
    a = a.mean(dim=0).numpy()
    hop = sr / FPS
    rms = np.array([np.sqrt(np.mean(a[int(f * hop):int((f + 1) * hop)] ** 2) + 1e-12) for f in range(n_frames)])
    ref = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1.0
    m = np.clip((rms / ref - 0.08) / 0.92, 0, 1)
    m = np.convolve(m, [0.25, 0.5, 0.25], mode="same")  # soften flicker
    return [round(float(x), 2) for x in m]


def words_for(wav, lines):
    """lines: [(text, start_s, end_s)] -> caption words in video time."""
    a, sr = ta.load(wav)
    a = a.mean(dim=0)
    a16 = ta.functional.resample(a, sr, 16000).numpy().astype("float32")
    out = []
    for text, s0, s1 in lines:
        seg = a16[int(s0 * 16000):int(s1 * 16000)]
        segs, _ = V._whisper().transcribe(seg, word_timestamps=True, language="en", beam_size=5)
        heard = [w for s in segs for w in (s.words or [])]
        for w in V._align(text.split(), heard):
            out.append({"w": w["w"], "start": round(s0 + w["start"], 3), "end": round(s0 + w["end"], 3)})
    return out


def extract_audio(mp4, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vn", "-c:a", "copy", dst], check=True)


def write(vid, data):
    os.makedirs(f"{HERE}/public/data", exist_ok=True)
    json.dump(data, open(f"{HERE}/public/data/{vid}.json", "w"), separators=(",", ":"))
    print("ok", vid, data["durationInFrames"], "frames", len(data["words"]), "words", file=sys.stderr)


def prep_topic(idx, t, scenes_for):
    vid = f"{idx:02d}-{t['slug']}"
    sc = scenes_for(t)
    n = len(sc)
    total = int(round(n * SCENE * FPS))
    voice = f"{SRC}/build/{t['slug']}/voice.wav"
    log = json.load(open(f"{SRC}/build/{t['slug']}/voice_log.json"))
    os.makedirs(f"{HERE}/public/audio", exist_ok=True)
    extract_audio(f"{SRC}/out/{vid}.mp4", f"{HERE}/public/audio/{vid}.m4a")
    scenes = []
    for i, (k, h, s, _, _) in enumerate(sc):
        scenes.append({"from": int(round(i * SCENE * FPS)), "dur": int(round(SCENE * FPS)),
                       "kicker": k, "headline": h, "sub": s, "mood": mood_for(i, n, k, h)})
    lines = [(e["text"], e["scene"] * SCENE, (e["scene"] + 1) * SCENE) for e in log]
    write(vid, {"id": vid, "emoji": t["emoji"], "subject": t["subject"], "durationInFrames": total,
                "audio": f"audio/{vid}.m4a", "scenes": scenes,
                "words": words_for(voice, lines), "mouth": mouth_track(voice, total)})


def prep_bridges():
    """Bridges uses the Chatterbox pipeline in whatif-videos (variable scene lengths)."""
    vid = "00-bridges"
    repo = "/home/user/whatif-videos"
    dump = subprocess.run(
        [sys.executable, "-c",
         "import sys, json; sys.argv=['make.py','full','topics/bridges.json']; sys.path.insert(0,'.');"
         "import make; make.prepare_voice();"
         "print(json.dumps({'starts': make.STARTS, 'scenes': make.SCENES, 'caps': make.CAPTIONS}))"],
        cwd=repo, check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    d = json.loads(dump)
    total = int(round(sum(s[0] for s in d["scenes"]) * FPS))
    n = len(d["scenes"])
    scenes = []
    for i, ((dur, k, h, s, _), st) in enumerate(zip(d["scenes"], d["starts"])):
        scenes.append({"from": int(round(st * FPS)), "dur": int(round(dur * FPS)),
                       "kicker": k, "headline": h.replace("\n", " "), "sub": s.replace("\n", " "),
                       "mood": mood_for(i, n, k, h)})
    words = [{"w": w, "start": round(a, 3), "end": round(b, 3)} for _, _, ws in d["caps"] for w, a, b in ws]
    os.makedirs(f"{HERE}/public/audio", exist_ok=True)
    extract_audio(f"{repo}/bridges_short.mp4", f"{HERE}/public/audio/{vid}.m4a")
    write(vid, {"id": vid, "emoji": "🌉", "subject": "BRIDGE", "durationInFrames": total,
                "audio": f"audio/{vid}.m4a", "scenes": scenes, "words": words,
                "mouth": mouth_track(f"{repo}/build/bridges/voice.wav", total)})


if __name__ == "__main__":
    want = set(sys.argv[1:])
    T, scenes_for = load_topics()
    if not want or "bridges" in want:
        prep_bridges()
    for idx, t in enumerate(T, start=1):
        if want and t["slug"] not in want:
            continue
        if os.path.exists(f"{HERE}/public/data/{idx:02d}-{t['slug']}.json") and "--force" not in want:
            continue
        prep_topic(idx, t, scenes_for)
