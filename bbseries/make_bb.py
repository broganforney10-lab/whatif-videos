"""Build voice, sound design, captions and 3D shot lists for Baseball What Ifs.

  python3 make_bb.py [slug ...]
Writes ../3d/public/bb/<id>.json and ../3d/public/bbaudio/<id>.m4a. Then render with COMP=Baseball3D.
"""
import json, math, os, re, subprocess, sys
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bb_topics import T, OUTRO  # noqa: E402

KOKORO_DIR = os.environ.get("KOKORO_DIR", "/home/claude/kokoro")
PUB = os.path.join(HERE, "..", "3d", "public")
BUILD = os.path.join(HERE, "build")
SR = 24000
FPS = 30
SCENE = 4.5
VOICE = os.environ.get("VOICE", "am_adam")
HOME = (0, 0, 4)
MOUND = (0, 0, -5.4)
BATTER = (-0.9, 0, 4.0)
CATCHER_CAM = dict(**{"from": [0.6, 1.8, 9.0]}, to=[0.35, 1.7, 7.6], look=[0, 1.3, -4])

# ---------------- voice ----------------
_K = None


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(f"{KOKORO_DIR}/kokoro.onnx", f"{KOKORO_DIR}/voices.bin")
    return _K


def say(text, slot):
    speed = 1.1
    while True:
        a, sr = kokoro().create(text, voice=VOICE, speed=speed, lang="en-us")
        if len(a) / sr <= slot or speed >= 1.5:
            break
        speed += 0.05
    return a[: int(slot * sr)].astype(np.float32), speed


def word_times(text, clip, t0):
    """Spread script words over the voiced part of the clip, weighted by length; pauses at punctuation."""
    env = np.abs(clip)
    thr = 0.04 * env.max() if env.max() > 0 else 0
    on = np.where(env > thr)[0]
    s, e = (on[0] / SR, on[-1] / SR) if len(on) else (0, len(clip) / SR)
    words = text.split()
    wts = [len(re.sub(r"[^\w]", "", w)) + 1.6 + (2.2 if re.search(r"[.,?!]$", w) else 0) for w in words]
    tot = sum(wts)
    out, cur = [], s
    for w, wt in zip(words, wts):
        d = (e - s) * wt / tot
        out.append({"w": w, "start": round(t0 + cur, 3), "end": round(t0 + cur + d * 0.85, 3)})
        cur += d
    return out


def mouth_track(v, n):
    hop = SR / FPS
    rms = np.array([np.sqrt(np.mean(v[int(f * hop):int((f + 1) * hop)] ** 2) + 1e-12) for f in range(n)])
    ref = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1.0
    m = np.clip((rms / ref - 0.08) / 0.92, 0, 1)
    m = np.convolve(m, [0.25, 0.5, 0.25], mode="same")
    return [round(float(x), 2) for x in m]


# ---------------- sound design (all synthesized) ----------------
rng = np.random.default_rng(7)
ASR = 48000


def noise(n):
    return rng.standard_normal(n).astype(np.float32)


def lowpass(x, fc):
    a = math.exp(-2 * math.pi * fc / ASR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # fine for short sfx
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def fft_band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / ASR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)


def crack():
    n = int(0.25 * ASR)
    t = np.arange(n) / ASR
    x = fft_band(noise(n), 900, 7000) * np.exp(-t * 38)
    x += 0.8 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 60)
    x += 0.6 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 25)
    return x / np.abs(x).max() * 0.9


def whoosh(d=0.45):
    n = int(d * ASR)
    t = np.arange(n) / ASR
    env = np.sin(np.pi * t / d) ** 2
    x = fft_band(noise(n), 400, 3500) * env
    return x / np.abs(x).max() * 0.35


def pop():
    n = int(0.18 * ASR)
    t = np.arange(n) / ASR
    x = np.sin(2 * np.pi * (140 - 60 * t) * t) * np.exp(-t * 30) + 0.5 * fft_band(noise(n), 200, 2500) * np.exp(-t * 55)
    return x / np.abs(x).max() * 0.8


def cheer(d=2.6):
    n = int(d * ASR)
    t = np.arange(n) / ASR
    env = np.minimum(1, t / 0.3) * np.exp(-np.maximum(0, t - 0.8) * 1.4)
    x = fft_band(noise(n), 300, 3200) * env * (1 + 0.25 * np.sin(2 * np.pi * 5.5 * t))
    return x / np.abs(x).max() * 0.45


def crowd_bed(dur):
    n = int(dur * ASR)
    t = np.arange(n) / ASR
    x = fft_band(noise(n), 250, 2200) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.13 * t) * np.sin(2 * np.pi * 0.31 * t))
    return x / np.abs(x).max() * 0.09


def music(dur, bpm=96):
    n = int(dur * ASR)
    t = np.arange(n) / ASR
    out = np.zeros(n, np.float32)
    beat = 60 / bpm
    chords = [(110, 164.81, 220), (98, 146.83, 196), (87.31, 130.81, 174.61), (98, 146.83, 196)]
    for b in range(int(dur / beat) + 1):
        s = int(b * beat * ASR)
        k = np.arange(min(int(0.3 * ASR), n - s)) / ASR
        if len(k) <= 0:
            continue
        kick = np.sin(2 * np.pi * (55 + 90 * np.exp(-k * 30)) * k) * np.exp(-k * 9)
        out[s:s + len(k)] += 0.55 * kick
        hs = int((b + 0.5) * beat * ASR)
        hk = np.arange(min(int(0.05 * ASR), max(0, n - hs))) / ASR
        if len(hk):
            out[hs:hs + len(hk)] += 0.12 * fft_band(noise(len(hk)), 6000, 14000) * np.exp(-hk * 80)
    bar = beat * 4
    for i in range(int(dur / bar) + 1):
        s, e = int(i * bar * ASR), min(n, int((i + 1) * bar * ASR))
        tt = np.arange(e - s) / ASR
        c = chords[i % len(chords)]
        pad = sum(np.sin(2 * np.pi * f * tt) for f in c) / 3
        out[s:e] += 0.12 * pad * np.minimum(1, tt / 0.15) * np.minimum(1, (bar - tt) / 0.15)
    return out / np.abs(out).max() * 0.16


def place(track, clip, at, gain=1.0):
    s = int(at * ASR)
    if s >= len(track):
        return
    e = min(len(track), s + len(clip))
    track[s:e] += clip[: e - s] * gain


# ---------------- shots ----------------
def cam(f, t, look, look2=None, fov=45):
    c = {"from": list(f), "to": list(t), "look": list(look), "fov": fov}
    if look2:
        c["lookTo"] = list(look2)
    return c


def pitcher(**kw):
    return dict(dict(pos=list(MOUND), heading=0, pose="point", hat="cap", talk=True), **kw)


def batter(**kw):
    return dict(dict(pos=list(BATTER), heading=math.pi / 2, pose="carry", hat="helmet", bat="rest", talk=False), **kw)


PITCH = dict(**{"from": [0.35, 2.05, -4.6]}, to=[0, 0.95, 4.7], arc=0.25)


def shots_for(act, sc, emo, board):
    """Two shots (A, B) for a scene. sc = (kicker, headline, sub, narration, act)."""
    head = sc[1]
    pr = lambda ch, p, s=0.8, a="grow": dict(ch=ch, pos=p, s=s, anim=a)
    if act == "pitch":
        A = dict(cam=CATCHER_CAM, actors=[pitcher(pose="idle", pose2="point", poseAt=0.35), batter()],
                 ball=dict(PITCH, t0=0.45, t1=0.62, trail=14), board=board, crowd=0.3)
        B = dict(cam=cam([1.2, 2.6, -9.5], [0.8, 2.3, -8.4], [0, 1.2, 4]), actors=[pitcher(pose="point"), batter()],
                 ball=dict(PITCH, t0=0.12, t1=0.42, trail=16), props=[pr("💥", [0, 1.1, 4.6], 0.9, "pop")], board=board, crowd=0.4)
        return A, B, [("whoosh", 0.47 * 0.5), ("pop", 0.62 * 0.5), ("whoosh", 0.5 + 0.13 * 0.5), ("pop", 0.5 + 0.42 * 0.5)]
    if act in ("swing", "homer"):
        A = dict(cam=cam([-3.6, 2.7, 9.8], [-3.1, 2.5, 8.9], [0, 1.2, -3]), actors=[pitcher(pose="point", talk=False),
                 batter(bat=dict(a0=2.0, a1=-1.5, t0=0.52, t1=0.64))],
                 ball=dict(PITCH, t0=0.28, t1=0.6, trail=12), board=board, crowd=0.4, shake=0.6)
        if act == "homer":
            B = dict(cam=cam([0, 3.2, 11], [0, 4.5, 9.5], [0, 2, -2], [4, 9, -30]), actors=[batter(pose="cheer", bat=None, talk=True)],
                     ball=dict(**{"from": [0, 1.0, 4]}, to=[8, 3, -42], arc=18, t0=0.0, t1=0.95, trail=18),
                     props=[pr("🎆", [6, 12, -36], 4, "pop"), pr("🎉", [-6, 10, -36], 3.5, "pop")], board="HOME RUN!", crowd=1)
            return A, B, [("whoosh", 0.3 * 0.5), ("crack", 0.6 * 0.5), ("cheer", 0.55)]
        B = dict(cam=cam([-1.5, 1.4, 6.5], [-3, 2.5, 7.5], [0, 1.4, 3], [4, 2, -18]), actors=[batter(pose="point", bat=None, talk=True)],
                 ball=dict(**{"from": [0, 1.0, 4]}, to=[9, 0.4, -24], arc=3, t0=0.0, t1=0.7, trail=18),
                 props=[pr(emo[0], [1.3, 2.6, 3.4], 0.7, "float")] if emo else [], board=board, crowd=0.7)
        return A, B, [("whoosh", 0.3 * 0.5), ("crack", 0.6 * 0.5), ("cheer", 0.6)]
    if act == "swingmiss":
        A = dict(cam=cam([-3.6, 2.7, 9.8], [-3.1, 2.5, 8.9], [0, 1.2, -3]), actors=[pitcher(pose="point", talk=False),
                 batter(bat=dict(a0=2.0, a1=-1.5, t0=0.62, t1=0.72))],
                 ball=dict(PITCH, t0=0.35, t1=0.55, trail=14), board=board, crowd=0.3)
        B = dict(cam=cam([1.6, 1.6, 7.5], [1.0, 1.7, 6.3], [-0.9, 1.5, 4]), actors=[batter(pose="shock", pose2="sad", poseAt=0.5, bat=None, talk=True)],
                 props=[pr("❌", [-0.2, 2.7, 4.2], 0.8, "pop"), pr("❓", [-1.6, 2.6, 4.0], 0.6, "float")], board="STRIKE 3", crowd=0.1)
        return A, B, [("whoosh", 0.36 * 0.5), ("pop", 0.55 * 0.5)]
    if act in ("stat", "think", "crowd", "crowdsad", "hurt", "glove", "glove2", "wave"):
        pos = [0, 0, -1.0]
        if act == "stat":
            A = dict(cam=cam([3.2, 1.6, 6.5], [2.0, 2.2, 5.0], [0, 5.5, -20]), actors=[dict(pos=pos, heading=0.5, pose="point", hat="cap")],
                     board=board, crowd=0.3)
            B = dict(cam=cam([0, 1.8, 3.4], [0, 1.75, 2.4], [0, 1.55, -1]), actors=[dict(pos=pos, heading=0, pose="shock", hat="cap")],
                     props=[pr(e, [x, 2.55, -0.7], 0.6, "float") for e, x in zip(emo[:2], [-1.0, 1.0])], board=board, crowd=0.3)
            return A, B, [("cheer", 0.2)]
        if act == "think":
            A = dict(cam=cam([0, 1.7, 5.2], [0, 1.7, 3.6], [0, 1.5, -1]), actors=[dict(pos=pos, heading=0, pose="think", hat="cap")],
                     props=[pr("❓", [0.9, 2.6, -0.8], 0.6, "float")], board=board, crowd=0.15)
            B = dict(cam=cam([-3, 1.2, 4], [-1.6, 1.5, 3.2], [0, 1.6, -1]), actors=[dict(pos=pos, heading=-0.4, pose="think", pose2="shock", poseAt=0.6, hat="cap")],
                     props=[pr(e, [1.1, 2.5, -0.7], 0.6, "pop") for e in emo[:1]], board=board, crowd=0.15)
            return A, B, []
        if act in ("crowd", "crowdsad"):
            happy = act == "crowd"
            A = dict(cam=cam([-10, 4, -12], [10, 4, -12], [0, 5, -40]), actors=[], board=board, crowd=1 if happy else 0.05)
            B = dict(cam=cam([0, 1.7, 4.4], [0, 1.8, 3.2], [0, 1.5, -1]),
                     actors=[dict(pos=pos, heading=0, pose="cheer" if happy else "sad", hat="cap")],
                     props=[pr(e, [x, 2.6, -0.6], 0.6, "float") for e, x in zip(emo[:2], [-1.1, 1.1])], board=board, crowd=1 if happy else 0.05)
            return A, B, [("cheer", 0.2)] if happy else []
        if act == "hurt":
            A = dict(cam=cam([3, 1.9, -0.5], [1.6, 1.8, -2.4], [0, 1.4, -5.4]), actors=[pitcher(pose="point", pose2="shock", poseAt=0.4)],
                     props=[pr("💥", [-0.45, 1.55, -5.0], 0.8, "pop")], board=board, crowd=0.2)
            B = dict(cam=cam([0, 1.9, -2.2], [0, 1.8, -3.2], [0, 1.5, -5.4]), actors=[pitcher(pose="sad")],
                     props=[pr("🤕", [0.9, 2.5, -5.2], 0.6, "float"), pr("🩹", [-0.9, 2.4, -5.2], 0.55, "float")], board=board, crowd=0.05)
            return A, B, [("pop", 0.25)]
        if act in ("glove", "glove2"):
            f = [3.5, 0, -6.5]
            A = dict(cam=cam([5.5, 1.6, -1.5], [4.6, 1.7, -2.6], [3.5, 1.3, -6.5]), actors=[dict(pos=f, heading=-2.6, pose="idle", pose2="shock", poseAt=0.55, hat="cap")],
                     ball=dict(**{"from": [0, 1.0, 4]}, to=[3.4, 1.2, -6.1], arc=1.2, t0=0.15, t1=0.55, trail=14),
                     props=[pr("💥", [3.4, 1.3, -5.9], 0.9, "pop")], board=board, crowd=0.4)
            B = dict(cam=cam([3.5, 1.8, -3.4], [3.5, 1.75, -4.3], [3.5, 1.5, -6.5]), actors=[dict(pos=f, heading=0, pose="sad", hat="none")],
                     props=[pr("✋", [2.6, 2.4, -6.2], 0.6, "float"), pr("🔥" if act == "glove" else "🧤", [4.4, 2.4, -6.2], 0.6, "float")], board=board, crowd=0.1)
            return A, B, [("crack", 0.08), ("pop", 0.55 * 0.5)]
        if act == "wave":
            A = dict(cam=cam([0, 1.7, 5.5], [0, 1.75, 3.8], [0, 1.5, -1]), actors=[dict(pos=pos, heading=0, pose="wave", hat="cap")],
                     props=[pr("⚾", [1.1, 2.6, -0.7], 0.6, "float"), pr("❓", [-1.1, 2.6, -0.7], 0.6, "float")], board="FOLLOW!", crowd=0.8)
            B = dict(cam=cam([0, 1.8, 3.6], [0, 6, 13], [0, 1.4, -1], [0, 3, -20]), actors=[dict(pos=pos, heading=0, pose="cheer", hat="cap")],
                     board="FOLLOW!", crowd=1, night=True)
            return A, B, [("cheer", 0.5)]
    # ---- moon ----
    sp = dict(hat="space")
    if act in ("moonstand", "moonstand2"):
        A = dict(cam=cam([2.2, 1.4, 6.5], [1.2, 1.6, 4.8], [0, 1.6, 0], [-1, 3, -6]), actors=[dict(pos=[0, 0, 0.5], heading=0.2, pose="idle", pose2="shock", poseAt=0.5, **sp)])
        B = dict(cam=cam([-2.6, 0.7, 5], [-2.0, 0.9, 4.2], [8, 9, -40], [12, 11, -50]), actors=[dict(pos=[0, 0, 0.5], heading=0.6, pose="point", **sp)],
                 props=[pr(e, [-1.2, 2.6, 0.3], 0.6, "float") for e in emo[:2]])
        return A, B, []
    MF = dict(**{"from": [0, 1.0, 4]}, to=[30, 0.4, -230], arc=60, r=0.45)
    if act == "moonswing":
        A = dict(cam=cam([-3.6, 2.4, 9.8], [-3.0, 2.2, 8.8], [0, 1.4, 0]), actors=[batter(hat="space", bat=dict(a0=2.0, a1=-1.5, t0=0.45, t1=0.58))],
                 ball=dict(**{"from": [0.4, 1.4, 0.5]}, to=[0, 1.0, 4.4], arc=0.1, t0=0.25, t1=0.55, trail=10), shake=0.55)
        B = dict(cam=dict(follow=True, **{"from": [3.5, -0.6, 5]}, to=[3, -1.2, 4.5], look=[0, 0, 0], fov=50),
                 actors=[batter(hat="space", pose="cheer", bat=None, talk=True)], ball=dict(MF, t0=0.0, t1=6.0, trail=20))
        return A, B, [("crack", 0.52 * 0.5)]
    if act in ("moonflight", "moonflight2"):
        A = dict(cam=dict(follow=True, **{"from": [-4, 1.5, 6]}, to=[-5, 2.5, 6.5], look=[0, 0, 0], fov=50), actors=[],
                 ball=dict(MF, t0=-0.5, t1=3.5, trail=24))
        B = dict(cam=cam([40, 25, -40], [38, 30, -70], [10, 30, -80], [20, 20, -140], fov=50), actors=[],
                 ball=dict(MF, t0=-1.2, t1=1.4, trail=24, r=0.9),
                 props=[pr("⏱️", [-8, 34, -95], 7, "float")] if act == "moonflight2" else [pr("📏", [-8, 34, -95], 7, "float")])
        return A, B, []
    if act == "moonpitch":
        A = dict(cam=CATCHER_CAM, actors=[pitcher(hat="space", pose="idle", pose2="point", poseAt=0.35), batter(hat="space")],
                 ball=dict(PITCH, t0=0.45, t1=0.7, trail=14, arc=0.25))
        B = dict(cam=cam([1.2, 2.6, -9.5], [0.8, 2.3, -8.4], [0, 1.2, 4]), actors=[pitcher(hat="space", pose="shock"), batter(hat="space")],
                 ball=dict(PITCH, t0=0.1, t1=0.5, trail=16), props=[pr("➡️", [0, 3.0, 0], 1.0, "pop")])
        return A, B, []
    if act == "moonwide":
        A = dict(cam=cam([0, 2, 9], [0, 30, 40], [0, 1, 0], [0, 0, -20]), actors=[dict(pos=[0, 0, 0.5], heading=0, pose="wave", **sp)])
        B = dict(cam=cam([0, 1.7, 4.2], [0, 1.8, 3.2], [0, 1.6, 0]), actors=[dict(pos=[0, 0, 0.5], heading=0, pose="shock", **sp)],
                 props=[pr("📏", [-1.0, 2.6, 0.6], 0.6, "float"), pr("🏟️", [1.0, 2.6, 0.6], 0.6, "float")])
        return A, B, []
    raise ValueError(act)


EMO = {"pitch": "⚾", "pitcher": "⚾", "ball": "⚾", "elbow": "💪", "arms": "💪", "fans": "🙌", "strikeouts": "❌", "blink": "👀",
       "guess": "🤷", "seconds": "⏱️", "second": "⏱️", "half": "📏", "mile": "📏", "feet": "📏", "air": "💨", "moon": "🌕",
       "gravity": "🪐", "golf": "⛳", "1971": "🚀", "record": "🏆", "fastest": "⚡", "speed": "⚡", "spin": "🌀", "curveballs": "🌀",
       "history": "📜", "1893": "📜", "1894": "📜", "2021": "🧪", "tested": "🧪", "offense": "💥", "averages": "📈", "exploded": "📈",
       "gloves": "🧤", "barehanded": "✋", "errors": "❌", "fingers": "🖐️", "scores": "🔢", "catchers": "🧤", "line": "💨",
       "human": "🧍", "probably": "🤔", "love": "❤️"}


def emojis(text):
    out = []
    for w in re.findall(r"[\w']+", text.lower()):
        e = EMO.get(w)
        if e and e not in out:
            out.append(e)
    return out or ["⚾"]


def build(idx, t):
    vid = f"{idx:02d}-{t['slug']}"
    scenes = [t["hook"]] + t["scenes"] + [OUTRO]
    n = len(scenes)
    dur = n * SCENE
    nfr = int(round(dur * FPS))
    voice = np.zeros(int(dur * SR), np.float32)
    words, log = [], []
    for i, sc in enumerate(scenes):
        clip, spd = say(sc[3], SCENE - 0.35)
        s = int((i * SCENE + 0.12) * SR)
        voice[s:s + len(clip)] += clip
        words += word_times(sc[3], clip, i * SCENE + 0.12)
        log.append((i, round(spd, 2), round(len(clip) / SR, 2)))
    os.makedirs(f"{BUILD}/{vid}", exist_ok=True)
    sf.write(f"{BUILD}/{vid}/voice.wav", voice, SR)
    # shots + sfx
    shots, sfx = [], []
    moon = t["set"] == "moon"
    for i, sc in enumerate(scenes):
        f0 = int(round(i * SCENE * FPS))
        d = int(round(SCENE * FPS))
        h1 = d // 2
        emo = emojis(" ".join(sc[:4]))
        board = "WHAT IF?"
        A, B, ev = shots_for(sc[4], sc, emo, board)
        for sh, a, b in ((A, f0, h1), (B, f0 + h1, d - h1)):
            sh = dict(sh)
            sh.update({"from": a, "dur": b, "set": "moon" if moon else "park"})
            if "moon" in sc[4]:
                sh["set"] = "moon"
            if moon:
                sh["actors"] = [dict(a, hat="space") for a in sh["actors"]]
            shots.append(sh)
        for kind, at in ev:
            sfx.append((kind, i * SCENE + at * SCENE))
    # mix
    adur = dur
    track = np.zeros(int(adur * ASR), np.float32)
    v48 = np.interp(np.arange(int(adur * ASR)) / ASR, np.arange(len(voice)) / SR, voice).astype(np.float32)
    track += v48
    track += music(adur)
    if not moon:
        track += crowd_bed(adur)
    bank = {"crack": crack(), "whoosh": whoosh(), "pop": pop(), "cheer": cheer()}
    for kind, at in sfx:
        if moon and kind in ("cheer",):
            continue
        place(track, bank[kind], at, 0.9 if kind != "cheer" else 0.8)
    fade = int(1.5 * ASR)
    track[-fade:] *= np.linspace(1, 0, fade)
    sf.write(f"{BUILD}/{vid}/mix.wav", track, ASR)
    os.makedirs(f"{PUB}/bbaudio", exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{BUILD}/{vid}/mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-c:a", "aac", "-b:a", "192k", f"{PUB}/bbaudio/{vid}.m4a"], check=True)
    data = dict(id=vid, durationInFrames=nfr, audio=f"bbaudio/{vid}.m4a", shots=shots,
                scenes=[dict(**{"from": int(round(i * SCENE * FPS))}, dur=int(round(SCENE * FPS)), kicker=s[0], headline=s[1], sub=s[2])
                        for i, s in enumerate(scenes)],
                words=words, mouth=mouth_track(voice, nfr))
    os.makedirs(f"{PUB}/bb", exist_ok=True)
    json.dump(data, open(f"{PUB}/bb/{vid}.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(vid, "speeds", [l[1] for l in log], flush=True)
    return vid


def caption(t):
    facts = " ".join(s[3] for s in t["scenes"][:3])
    return (f"{t['hook'][3]} ⚾ {facts}\n\nWhat should we test next? Drop it in the comments 👇\n"
            f"Follow for more.\n\n#whatif #baseball #shorts {t['tags']}")


if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("-")]
    for idx, t in enumerate(T, 1):
        if want and t["slug"] not in want:
            continue
        build(idx, t)
