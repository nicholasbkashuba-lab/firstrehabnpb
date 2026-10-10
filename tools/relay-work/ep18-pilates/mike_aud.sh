#!/bin/bash
# mike_aud.sh T0 T1 URL : fetch bytes for cam [T0,T1], extract audio, free the bytes
set -e; cd /home/user/ep18
python3 mike_slice.py $1 $2 "$3"
ffmpeg -v error -y -ss $1 -i Mike.mov -t $(python3 -c "print($2-$1)") -map 0:a:0 -ac 1 -ar 8000 mka_$1.wav
read lo hi a b < <(tail -1 mike_ranges.txt)
fallocate -p -o $lo -l $((hi-lo)) Mike.mov
du -h Mike.mov
