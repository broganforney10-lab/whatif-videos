# What If It Vanished: full video pipeline

This branch holds everything used to make and schedule the channel's Shorts.

| Folder | What it does |
|---|---|
| `make.py`, `voice.py` | Single-video pipeline: script, Chatterbox voiceover, faster-whisper captions, MP4 (see README.md). |
| `series/` | The 130-topic series. `topics.py`, `topics2.py` and `topics3.py` hold every script (7 scenes each). `make_videos.py` narrates each topic with Kokoro (voice `am_michael`) and renders the original card-style video plus `voice.wav` and `voice_log.json`. |
| `3d/` | Remotion project that turns each narrated topic into the 3D cartoon-story version (the style now being posted). |

## Making a new batch

1. **Write scripts.** Add a new `series/topicsN.py` in the same format and `exec` it at the end of `series/topics.py` (like `topics3.py`). Keep each narration line short (about 12 words) so it fits its 4.5 s scene.
2. **Narrate.** From `series/`, run `make_videos.py <slug> ...` with Python that has `kokoro-onnx`, `soundfile`, `numpy` and Pillow. Set `KOKORO_DIR` to a folder holding `kokoro.onnx` and `voices.bin` from the kokoro-onnx release.
3. **Prep the 3D data.** From `3d/`, run `python prep.py <slug> ...` (needs torchaudio and faster-whisper, e.g. the `.venv` from `requirements.txt`). It reads the narration from the series folder; adjust the `SRC` path at the top of `prep.py` if it lives somewhere other than `/home/user/whatif`.
4. **Shot lists.** `python3 gen_story.py` creates `public/story/<id>.json` for every new video: set, character pose, camera move and emoji props for each shot.
5. **Render.** Run `npm i` once, then `./chunk3d.sh 2` repeatedly (two videos per run, about 3.5 minutes each on a 4-core CPU). Finished files go to `out3d/` and are pushed to the `media` branch by `push3d.sh`.
6. **Schedule.** Each post uses the video's raw GitHub URL (`https://raw.githubusercontent.com/<owner>/<repo>/media/videos3d/<id>-3d.mp4`), the caption from `make_videos.py`'s `caption()`, Instagram Reel + YouTube Short, 8 AM and 4 PM America/Detroit.

## Where the finished videos are

Branch `media`: `videos/` (original style), `videos2d/` (2D character), `videos3d/` (3D story, the scheduled ones).
