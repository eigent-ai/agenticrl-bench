#!/bin/bash
set -e
cd /opt/vidpipeline
ffmpeg -y -framerate 1 -i "images/frame_%03d.jpg" -c:v libx264 -r 30 -pix_fmt yuv420 output.mp4
