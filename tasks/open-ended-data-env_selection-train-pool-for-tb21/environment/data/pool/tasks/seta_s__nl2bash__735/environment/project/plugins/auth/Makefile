# plugins/auth - Authentication plugin
include ../../config.mk

SRCS = auth.c
OBJS = $(SRCS:.c=.o)
TARGET = auth.so

CFLAGS = $(COMMON_CFLAGS) -O2 -shared
LDFLAGS = $(COMMON_LDFLAGS)

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

install: $(TARGET)
	install -d /usr/local/lib/plugins
	install -m 755 $(TARGET) /usr/local/lib/plugins/

install: $(TARGET)
	install -d /opt/plugins
	install -m 755 $(TARGET) /opt/plugins/

clean:
	rm -f $(OBJS) $(TARGET)
