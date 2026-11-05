# tools/monitor - System monitor tool
include ../../config.mk

SRCS = monitor.c
OBJS = $(SRCS:.c=.o)
TARGET = monitor

CFLAGS = $(COMMON_CFLAGS) -O2
LDFLAGS = $(COMMON_LDFLAGS)
include ../../legacy.mk

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
