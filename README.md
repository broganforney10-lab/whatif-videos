# What If It Vanished: video generator

Makes vertical 1080x1920 Shorts/Reels for **@whatifitvanished** from a topic file.

## Make a video

```bash
python3 make.py full topics/bridges.json     # renders bridges_short.mp4
python3 make.py stills topics/bridges.json   # quick preview frames (still_*.jpg)
```

Needs Python 3 with Pillow, ffmpeg, and the Inter font (`/usr/share/fonts/opentype/inter/`).

## New topic

Copy `topics/bridges.json` to `topics/<topic>.json` and edit it:

- `output`: the file name to write
- `scenes`: one entry per screen
  - `seconds`: how long it stays up
  - `kicker`: small yellow line on top
  - `big`: the huge text (use `\n` for line breaks)
  - `body`: smaller line underneath (optional)
  - `bridge`: background art: `vanish` (bridge dissolves), `gap` (empty banks) or `boats`

The background art is bridge-themed for now. Other topics will need their own art in `make.py`.

Videos come out silent. Add a trending sound when posting from the Instagram or YouTube app.
