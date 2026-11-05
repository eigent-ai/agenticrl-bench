# lib/network - Network interface library
include ../../config.mk

SRCS = network.c
OBJS = $(SRCS:.c=.o)
TARGET = libnetwork.a
%.o: %.c
    $(CC) $(COMMON_CFLAGS) -c $< -o $@

LDFLAGS = $(COMMON_LDFLAGS)

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) rcs $@ $^

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d /usr/local/lib
	install -m 644 $(TARGET) /usr/local/lib/
