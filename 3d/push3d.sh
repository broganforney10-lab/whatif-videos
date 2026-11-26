#!/bin/bash
# Copy finished 3D renders into the media branch and push any new ones.
cd /home/user/whatif-media || exit 1
mkdir -p videos3d
n=0
for f in /home/user/whatif-2d/out3d/*-3d.mp4; do
  b=$(basename "$f"); [ -f "videos3d/$b" ] && continue
  cp "$f" videos3d/ && n=$((n+1))
done
[ $n -eq 0 ] && { echo "nothing new"; exit 0; }
git add videos3d && git commit -q -m "Add $n 3D story shorts

Claude-Session: https://claude.ai/code/session_01HgA8aJodGuptK6V9j2TJ5h"
for i in 1 2 3 4; do git push -q origin media 2>&1 | tail -1; [ ${PIPESTATUS[0]} -eq 0 ] && { echo "pushed $n"; exit 0; }; sleep $((i*5)); done
echo "push failed"; exit 1
