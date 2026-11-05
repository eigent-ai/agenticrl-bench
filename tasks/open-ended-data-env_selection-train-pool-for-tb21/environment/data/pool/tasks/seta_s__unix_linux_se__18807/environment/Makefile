OUTDIR ?= build
CC = gcc
CFLAGS = -Wall -O2

SRCS = $(wildcard src/*.c)
OBJS = $(patsubst src/%.c,$(OUTDIR)/%.o,$(SRCS))
TARGET = $(OUTDIR)/appbin

.PHONY: all clean

all: src/config.h $(TARGET)

src/config.h: src/config.h.in
	[[ -d src ]] && ./dpp

$(TARGET): $(OBJS)
	[[ -d $(OUTDIR) ]] || mkdir -p $(OUTDIR)
	$(CC) $(CFLAGS) -o $@ $^

$(OUTDIR)/%.o: src/%.c src/config.h
	[[ -d $(OUTDIR) ]] || mkdir -p $(OUTDIR)
	$(CC) $(CFLAGS) -Isrc -c $< -o $@

clean:
	rm -rf $(OUTDIR) src/config.h
