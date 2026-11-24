"""Voice + caption timing for make.py. Runs inside .venv (needs chatterbox-tts, faster-whisper).

  voice.py speak <job.json>   job: {"lines": [text, ...], "cache": dir, "voice": wav|null}
                              prints JSON [{"wav": path, "seconds": float}, ...]
  voice.py words <job.json>   job: {"lines": [{"text", "wav"}...]}
                              prints JSON [[{"w", "start", "end"}, ...] per line]  (times local to each line)
  voice.py mix <job.json>     job: {"clips": [{"wav", "start"}...], "total": s, "out": path}

Captions show the script's own words (so numbers and names are spelled right);
faster-whisper only supplies the timing, matched word-by-word to the script.
"""
import difflib, hashlib, json, os, re, sys

SR_OUT = 24000


def _key(*parts):
    return hashlib.sha1("\x00".join(map(str, parts)).encode()).hexdigest()[:16]


def speak(job):
    import torch, torchaudio as ta
    os.makedirs(job["cache"], exist_ok=True)
    voice = job.get("voice")
    out, todo = [], []
    for i, text in enumerate(job["lines"]):
        wav = os.path.join(job["cache"], f"tts_{_key('turbo-checked', voice, text)}.wav")
        out.append({"wav": wav})
        if not os.path.exists(wav):
            todo.append((i, text, wav))
    if todo:
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        model = ChatterboxTurboTTS.from_pretrained(device="cpu")
        for i, text, wav in todo:
            best = None
            for attempt in range(TTS_TRIES):
                torch.manual_seed(1234 + i + 100 * attempt)
                audio = model.generate(text, audio_prompt_path=voice) if voice else model.generate(text)
                audio = _trim(audio, model.sr)
                ta.save(wav + ".part.wav", audio, model.sr)
                # TTS sometimes skips or mangles a word: listen back and retry with a new seed
                score = _heard_ratio(text, wav + ".part.wav")
                print(f"  tts {i + 1}/{len(job['lines'])} try {attempt + 1}: {score:.0%} heard  {text}", file=sys.stderr)
                if best is None or score > best[0]:
                    best = (score, audio)
                if score >= 0.999:
                    break
            ta.save(wav + ".part.wav", best[1], model.sr)
            os.replace(wav + ".part.wav", wav)
    for o in out:
        info = ta.info(o["wav"])
        o["seconds"] = info.num_frames / info.sample_rate
    return out


TTS_TRIES = 3
_WHISPER = None


def _whisper(name="small.en"):
    global _WHISPER
    if _WHISPER is None:
        from faster_whisper import WhisperModel
        _WHISPER = WhisperModel(name, device="cpu", compute_type="int8")
    return _WHISPER


def _heard_ratio(text, wav):
    """Fraction of script words that whisper hears in the clip."""
    segs, _ = _whisper().transcribe(_load16k(wav), language="en", beam_size=5)
    heard = [_norm(w) for s in segs for w in s.text.split()]
    script = [_norm(w) for w in text.split()]
    sm = difflib.SequenceMatcher(a=script, b=heard, autojunk=False)
    return sum(b.size for b in sm.get_matching_blocks()) / max(1, len(script))


def _trim(audio, sr, thresh=0.01, pad=0.08):
    """Cut leading/trailing silence so scenes start on the first word."""
    a = audio.abs().amax(dim=0)
    idx = (a > thresh).nonzero()
    if len(idx) == 0:
        return audio
    s = max(0, int(idx[0]) - int(pad * sr))
    e = min(audio.shape[-1], int(idx[-1]) + int(pad * sr))
    return audio[..., s:e]


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def words(job):
    model = _whisper(job.get("model", "small.en"))
    result = []
    for line in job["lines"]:
        script = line["text"].split()
        segs, _ = model.transcribe(_load16k(line["wav"]), word_timestamps=True, language="en", beam_size=5)
        heard = [w for s in segs for w in (s.words or [])]
        result.append(_align(script, heard))
    return result


def _load16k(path):
    """Mono 16 kHz float32 array (lets faster-whisper skip PyAV decoding)."""
    import torchaudio as ta
    a, sr = ta.load(path)
    return ta.functional.resample(a.mean(dim=0), sr, 16000).numpy().astype("float32")


def _align(script, heard):
    """Give every script word a start/end using whisper's word times."""
    times = [None] * len(script)
    sm = difflib.SequenceMatcher(a=[_norm(w) for w in script], b=[_norm(h.word) for h in heard], autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            times[blk.a + k] = (h.start, h.end)
    # unmatched words (e.g. "624,000" heard as "six hundred twenty four thousand"):
    # spread them evenly over the gap between their matched neighbours
    end_all = heard[-1].end if heard else 0.4 * len(script)
    i = 0
    while i < len(times):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(times) and times[j] is None:
            j += 1
        t0 = times[i - 1][1] if i > 0 else (heard[0].start if heard else 0.0)
        t1 = times[j][0] if j < len(times) else end_all
        if t1 <= t0:
            t1 = t0 + 0.25 * (j - i)
        step = (t1 - t0) / (j - i)
        for k in range(i, j):
            times[k] = (t0 + step * (k - i), t0 + step * (k - i + 1))
        i = j
    return [{"w": w, "start": round(s, 3), "end": round(e, 3)} for w, (s, e) in zip(script, times)]


def mix(job):
    import torch, torchaudio as ta
    total = int(job["total"] * SR_OUT) + 1
    track = torch.zeros(1, total)
    for c in job["clips"]:
        a, sr = ta.load(c["wav"])
        a = a.mean(dim=0, keepdim=True)
        if sr != SR_OUT:
            a = ta.functional.resample(a, sr, SR_OUT)
        s = int(c["start"] * SR_OUT)
        n = min(a.shape[-1], total - s)
        track[:, s:s + n] += a[:, :n]
    ta.save(job["out"], track.clamp(-1, 1), SR_OUT)
    return {"out": job["out"]}


if __name__ == "__main__":
    cmd, path = sys.argv[1], sys.argv[2]
    job = json.load(open(path))
    print(json.dumps({"speak": speak, "words": words, "mix": mix}[cmd](job)))
