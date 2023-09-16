ffmpeg -i input.mp4 -c:v copy -c:a copy -f segment -segment_time 300 output_%03d.mp4
