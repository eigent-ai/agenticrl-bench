# lib/utils - Utility functions
include ../../config.mk

TARGET = libutils.a
CFLAGS = $(COMMON_CFLAGS) -O2
SRC = utils.c
LDFLAGS = $(COMMON_LDFLAGS)
INSTALL_DIR = /usr/local/lib

.PHONY: all clean install

# Build configuration
PREFIX = /usr/local
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d $(INSTALL_DIR)
	install -m 644 $(TARGET) $(INSTALL_DIR)/
