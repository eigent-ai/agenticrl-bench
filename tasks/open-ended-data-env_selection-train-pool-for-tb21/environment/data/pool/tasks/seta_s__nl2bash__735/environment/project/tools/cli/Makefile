# tools/cli - Command line interface
include ../../config.mk

SRCS = cli.c
OBJS = $(SRCS:.c=.o)
TARGET = cli

CFLAGS = $(COMMON_CFLAGS) -O2
LDFLAGS = $(COMMON_LDFLAGS)

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d /usr/local/bin
	install -m 755 $(TARGET) /usr/local/bin/
