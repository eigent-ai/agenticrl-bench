CC=gcc
CFLAGS=-Wall -g -I/usr/include/x86_64-linux-gnu
LDFLAGS=-L/usr/local/include/ffmpeg -libavformat -libavcodec -libavutil -lswscale

all: video_info

video_info: video_info.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f video_info output.mp4 metadata.json
