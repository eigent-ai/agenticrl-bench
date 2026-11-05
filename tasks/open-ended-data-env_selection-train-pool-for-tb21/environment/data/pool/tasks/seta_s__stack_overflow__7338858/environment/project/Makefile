CC      = gcc
CFLAGS  = -Wall -Wextra -O2 -fPIC
LDFLAGS = -shared

TARGET = libdepth_renderer.so
SRC    = src/depth_renderer.c

$(TARGET): $(SRC) src/depth_renderer.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
