#!/bin/bash
# Render the next N unfinished 3D videos in the foreground (default 2), then push them.
cd /home/user/whatif-2d || exit 1
pkill -f "node render.mjs" 2>/dev/null; rm -f out3d/*.part.mp4
ids=$(for f in $(ls public/story | sed 's/.json//' | sort -n); do [ -f out3d/$f-3d.mp4 ] || echo $f; done | grep -vE '^(00-bridges|01-moon)$' | head -${1:-2} | tr '\n' ' ')
[ -z "$ids" ] && { echo "all rendered"; exit 0; }
COMP=Story3D DATA=public/story OUT=out3d SUF=-3d timeout 570 node render.mjs $ids 2>&1 | grep -E "^done|Error"
./push3d.sh
echo "left: $(for f in $(ls public/story | sed 's/.json//'); do [ -f out3d/$f-3d.mp4 ] || echo $f; done | grep -vcE '^(00-bridges|01-moon)$')"
