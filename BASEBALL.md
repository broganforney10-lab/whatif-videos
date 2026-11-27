# Baseball What Ifs: one idea in, finished Short out

Every video is written as code and rendered frame by frame (Remotion + three.js). No AI video model, no credits.

## Make a new video

1. Add a topic to `bbseries/bb_topics.py`: a hook plus exactly 7 scenes. Each scene is
   `(kicker, HEADLINE, sub, narration ~12 words, act)`.
   Acts: `pitch swing homer swingmiss stat think crowd crowdsad hurt glove glove2` (ballpark),
   `moonstand moonstand2 moonswing moonflight moonflight2 moonpitch moonwide` (moon set).
2. Build voice, sound design, captions and shots:
   `cd bbseries && python3 make_bb.py <slug>` (writes `3d/public/bb/<id>.json`, `3d/public/bbaudio/<id>.m4a`)
3. Check the frames before the full render:
   `cd 3d && node stills.mjs <id>` then `python3 ../sheet.py <id> /tmp/sheet.jpg`
4. Render: `COMP=Baseball3D DATA=public/bb OUT=out_bb SUF="" CONC=2 node render.mjs <id>`
5. Cover + caption: `cd bbseries && python3 cover.py` (writes `out_bb/<id>-cover.jpg` and `out_bb/captions.md`)

## Setup

- `cd 3d && npm i`
- `pip install kokoro-onnx soundfile` and download `kokoro-v1.0.onnx` + `voices-v1.0.bin` from the
  thewh1teagle/kokoro-onnx GitHub release into `$KOKORO_DIR` (default `/home/claude/kokoro`).
- Chromium: `render.mjs` / `stills.mjs` use `/opt/pw-browsers/chromium_headless_shell`.

## Rules that keep quality up

- Hook in the first line. Every scene gets a number or a strong word as its HEADLINE.
- Facts must be widely sourced; round numbers and say "about".
- Look at the contact sheet before rendering: no empty frames, no face blocking the lens.
