CC      = gcc
CFLAGS  = -O2 -Wall -Wextra

.PHONY: all debug clean

all: scale_clamp

scale_clamp: scale_clamp.c
	$(CC) $(CFLAGS) -o scale_clamp scale_clamp.c

debug: scale_clamp.c
	$(CC) -O0 -g -Wall -Wextra -o scale_clamp_debug scale_clamp.c

clean:
	rm -f scale_clamp scale_clamp_debug
