#!/bin/bash
# Relaunch the detached 3D batch render for any videos not finished yet (no-op if already running).
cd /home/user/whatif-2d || exit 1
pgrep -f "node render.mjs" >/dev/null && { echo "already running"; exit 0; }
rm -f out3d/*.part.mp4
ids=$(for f in $(ls public/story | sed 's/.json//' | sort -n); do [ -f out3d/$f-3d.mp4 ] || echo $f; done | grep -vE '^(00-bridges|01-moon)$' | tr '\n' ' ')
[ -z "$ids" ] && { echo "all done"; exit 0; }
COMP=Story3D DATA=public/story OUT=out3d SUF=-3d setsid nohup node render.mjs $ids >> out3d/batch.log 2>&1 < /dev/null & disown
echo "relaunched for $(echo $ids | wc -w) videos"
