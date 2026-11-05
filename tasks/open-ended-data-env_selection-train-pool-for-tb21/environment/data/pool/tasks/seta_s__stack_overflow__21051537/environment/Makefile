CC = gcc
CFLAGS = -std=gnu11 -fPIC -Wall -O2
LDFLAGS = -shared -lm

SRCDIR = src
LIBDIR = lib
SOURCES = $(SRCDIR)/reflect.c $(SRCDIR)/normalize.c
TARGET = $(LIBDIR)/libmathcore.so

.PHONY: all clean

all: $(TARGET)

$(LIBDIR):
	mkdir -p $(LIBDIR)

$(TARGET): $(SOURCES) $(SRCDIR)/mathcore.h | $(LIBDIR)
	$(CC) $(CFLAGS) $(LDFLAGS) -I$(SRCDIR) -o $@ $(SOURCES)

clean:
	rm -rf $(LIBDIR)
