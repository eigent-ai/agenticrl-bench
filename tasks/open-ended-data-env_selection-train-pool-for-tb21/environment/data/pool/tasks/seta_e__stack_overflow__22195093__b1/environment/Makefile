CC = gcc
CFLAGS = -Wall -std=c11
SRC = src/dateutils.c src/taskctl.c
OUT = build/taskctl

all: $(OUT)

$(OUT): $(SRC) src/dateutils.h
	@mkdir -p build
	$(CC) $(CFLAGS) -Isrc -o $(OUT) $(SRC)

clean:
	rm -rf build

.PHONY: all clean
