set -e
cd /home/user/ep21
python3 tools/render21.py 31
ls seg/[0-9][0-9][0-9].mp4 | wc -l
# audio: RAW mp3 0..359.2 and 381.3667..end, 20 ms fades at the join, 0.3 s fade in, 1.5 s fade out
ffmpeg -v error -y -i src/raw.mp3 -filter_complex "[0:a]atrim=0:359.2,asetpts=PTS-STARTPTS,afade=t=out:st=359.18:d=0.02[a];[0:a]atrim=381.3667:1622.8,asetpts=PTS-STARTPTS,afade=t=in:d=0.02[b];[a][b]concat=n=2:v=0:a=1,afade=t=in:d=0.3,afade=t=out:st=1599.1:d=1.5[o]" -map "[o]" -c:a pcm_s16le -ar 48000 audio_edit.wav
ffmpeg -v error -y -f concat -safe 0 -i seg/list.txt -i audio_edit.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest "master.mp4"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,nb_frames -of compact master.mp4
