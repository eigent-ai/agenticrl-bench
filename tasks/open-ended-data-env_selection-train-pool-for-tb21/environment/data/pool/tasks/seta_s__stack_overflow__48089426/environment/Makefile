CC      = gcc
CFLAGS  = -O2 -Wall -mindirect-branch=thunk-extern -fcf-protection=none
BINARY  = build/dispatcher

all: $(BINARY)

$(BINARY): src/dispatcher.c | build
	$(CC) $(CFLAGS) -Iinclude -o $@ $<

build:
	mkdir -p build

clean:
	rm -rf build
