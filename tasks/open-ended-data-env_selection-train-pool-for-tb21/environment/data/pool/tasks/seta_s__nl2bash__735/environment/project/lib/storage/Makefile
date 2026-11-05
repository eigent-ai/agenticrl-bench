# lib/storage - Storage backend
SRCS = storage.c
CC = /opt/old-toolchain/bin/gcc
OBJS = $(SRCS:.c=.o)
TARGET = libstorage.a

CFLAGS = -Wall -Wextra -fPIC -O2
LDFLAGS =

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
