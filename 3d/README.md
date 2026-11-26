# What If It Vanished: 2D character versions

Remotion project that re-renders every "What if ___ vanished?" Short with **Blip**, the channel's
cartoon narrator: a mint blob with a yellow antenna who lip-syncs to the voiceover.

- Blip's **mouth** follows the loudness of the voice track, frame by frame.
- Each scene gives Blip a **mood** and pose: shocked (hook), pointing (facts and numbers),
  worried (bad news), excited ("the most valuable thing now"), thinking (questions), waving (outro).
  Blip hops when a scene changes, blinks, looks up at the text, and the antenna bulb glows.
- The topic's **emoji** pops in during the hook, then vanishes in a puff. A faded ghost of it stays.
- **Captions** are word-synced (faster-whisper timings, script spelling), with the spoken word in yellow.
- Same text, voice and background pad as the original videos; output is 1080x1920, 30 fps, ~40 s.

## Make the videos

```bash
npm i
/home/user/whatif-videos/.venv/bin/python prep.py      # public/data/*.json + public/audio/*.m4a
node render.mjs                                         # out/<id>-2d.mp4 (skips finished ones)
node render.mjs 01-moon 02-bees                         # just these (re-renders them)
npx remotion studio                                     # preview; set the `id` prop to pick a video
```

`prep.py` reads the original project in `/home/user/whatif` (topics, `build/<slug>/voice.wav`,
`out/*.mp4`). Bridges comes from the Chatterbox pipeline in `/home/user/whatif-videos`.
Rendering takes about 45 s per video on 4 CPU cores. It uses the machine's pre-installed
headless Chromium (`/opt/pw-browsers/chromium_headless_shell`).

Remotion is free for individuals and teams of up to 3 people.
