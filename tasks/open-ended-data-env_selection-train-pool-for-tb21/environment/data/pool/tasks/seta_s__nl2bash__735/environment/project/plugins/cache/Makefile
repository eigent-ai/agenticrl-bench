# plugins/cache - Cache plugin
SRCS = cache.c
OBJS = $(SRCS:.c=.o)
TARGET = cache.so
CC = gcc-9

CFLAGS = -Wall -Wextra -fPIC -O2 -shared
LDFLAGS =

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d /usr/local/lib/plugins
	install -m 755 $(TARGET) /usr/local/lib/plugins/
