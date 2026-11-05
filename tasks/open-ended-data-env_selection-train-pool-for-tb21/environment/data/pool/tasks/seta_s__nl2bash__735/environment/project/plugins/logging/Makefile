# plugins/logging - Logging plugin
include ../../config.mk

SRCS = logging.c
OBJS = $(SRCS:.c=.o)
TARGET = logging.so

CFLAGS = $(COMMON_CFLAGS) -O2 -shared
LDFLAGS += -L/opt/old-libs

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
