# lib/core - Core library module
include ../../config.mk

SRCS = core.c
OBJS = $(SRCS:.c=.o)
TARGET = libcore.a

CFLAGS = $(COMMON_CFLAGS) -O2
LDFLAGS = $(COMMON_LDFLAGS)

# Include paths for dependencies
CFLAGS += -I/opt/old-includes -I.

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d /usr/local/lib
	install -m 644 $(TARGET) /usr/local/lib/
