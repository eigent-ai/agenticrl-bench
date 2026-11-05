# lib/crypto - Cryptographic utilities
include ../../config.mk

SRCS = crypto.c
OBJS = $(SRCS:.c=.o)
TARGET = libcrypto_util.a

CFLAGS = $(COMMON_CFLAGS) -O2
LDFLAGS = $(COMMON_LDFLAGS)

.PHONY: all clean install

all: $(TARGET)

LDFLAGS += -L$(EXTRA_LIB_DIR)/lib

$(TARGET): $(OBJS)
	$(AR) rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d /usr/local/lib
	install -m 644 $(TARGET) /usr/local/lib/
