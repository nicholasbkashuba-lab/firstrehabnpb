#!/bin/sh
# webenc.sh <master.mp4> <out-prefix>   -> -hd.mp4 -hd.webm -mobile.mp4 -mobile.webm -poster.jpg
M=$1; O=$2
DN="hqdn3d=2.5:2:4:3"
TAG="-color_primaries bt709 -color_trc bt709 -colorspace bt709"
ffmpeg -v error -y -i $M -an -vf "$DN" -c:v libx264 -preset slow -crf 27 -pix_fmt yuv420p -profile:v high $TAG -movflags +faststart $O-hd.mp4
ffmpeg -v error -y -i $M -an -vf "$DN,scale=1280:720:flags=lanczos" -c:v libx264 -preset slow -crf 29 -pix_fmt yuv420p -profile:v high $TAG -movflags +faststart $O-mobile.mp4
ffmpeg -v error -y -i $M -an -vf "$DN" -c:v libvpx-vp9 -crf 38 -b:v 0 -row-mt 1 -cpu-used 2 -pix_fmt yuv420p $TAG $O-hd.webm
ffmpeg -v error -y -i $M -an -vf "$DN,scale=1280:720:flags=lanczos" -c:v libvpx-vp9 -crf 42 -b:v 0 -row-mt 1 -cpu-used 2 -pix_fmt yuv420p $TAG $O-mobile.webm
ffmpeg -v error -y -ss 0.05 -i $M -frames:v 1 -vf "scale=1600:900:flags=lanczos" -q:v 6 $O-poster.jpg
ls -la $O-*
