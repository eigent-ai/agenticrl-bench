CC = gcc
CFLAGS = -Wall -fPIC $(shell pkg-config --cflags libxml-2.0)
LDFLAGS = $(shell pkg-config --libs libxml-2.0)
LIBDIR = /usr/local/lib/buildproject
BINDIR = /opt/buildproject

.PHONY: all clean install

all: buildproject

libmathext.so: src/mathext.c src/mathext.h
	$(CC) $(CFLAGS) -shared -o $@ src/mathext.c

buildproject: src/main.c libmathext.so
	$(CC) $(CFLAGS) -Isrc -o $@ src/main.c -L. -lmathext $(LDFLAGS) -Wl,-rpath,$(LIBDIR)

clean:
	rm -f buildproject libmathext.so

install: libmathext.so
	mkdir -p $(LIBDIR)
	cp libmathext.so $(LIBDIR)/
	ldconfig
