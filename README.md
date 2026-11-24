# What If It Vanished: video generator

Makes vertical 1080x1920 Shorts/Reels for **@whatifitvanished** from a topic file.

## Make a video

```bash
python3 make.py full topics/bridges.json     # voiced video with synced captions -> bridges_short.mp4
python3 make.py silent topics/bridges.json   # old silent render, no voice
python3 make.py stills topics/bridges.json   # quick preview frames (still_*.jpg)
```

`full` runs the whole pipeline:

1. **Voiceover**: each scene's `say` line is spoken by Chatterbox Turbo (free, local, CPU is fine).
   Every take is transcribed back with faster-whisper; a take that skips words is regenerated
   with a new seed (up to 3 tries). Takes are cached in `build/tts-cache/`, so re-renders are fast.
2. **Timing**: each scene lasts as long as its line (plus a short pause), so text and voice change together.
3. **Captions**: faster-whisper gives word timings; the captions show the script's own words
   (numbers like 624,000 stay as digits), 3 words at a time, with the spoken word in yellow.
4. **Audio**: voice track normalised to -14 LUFS (the Shorts/Reels target) and muxed into the MP4.

Bridges (9 scenes, ~42 s) takes about 3 minutes the first time on a 4-core CPU and ~40 s when the voice is cached.

### Setup

Needs Python 3, ffmpeg, Pillow, and the Inter font (`/usr/share/fonts/opentype/inter/`).
The voice step runs in a venv next to `make.py`:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The first run downloads the models from Hugging Face (~2 GB for Chatterbox Turbo, ~0.5 GB for Whisper small.en).
Every Chatterbox clip carries Resemble AI's inaudible Perth watermark.

## New topic

Copy `topics/bridges.json` to `topics/<topic>.json` and edit it:

- `output`: the file name to write
- `scenes`: one entry per screen
  - `seconds`: how long it stays up
  - `kicker`: small yellow line on top
  - `big`: the huge text (use `\n` for line breaks)
  - `body`: smaller line underneath (optional)
  - `bridge`: background art: `vanish` (bridge dissolves), `gap` (empty banks) or `boats`
  - `say`: what the narrator says during this scene (falls back to the on-screen text)
  - `seconds` is now a minimum: in `full` the scene stretches to fit its `say` line
- `voice` (optional): path to a ~10 s WAV to clone a different narrator voice

The background art is bridge-themed for now. Other topics will need their own art in `make.py`.

`full` videos have the voiceover only (no music), so a quiet trending sound can still be added in the app.
